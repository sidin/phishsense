import simplejson
import hashlib
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.http import HttpResponseBadRequest

from .forms import URLForm
from .models import InvestigateUrlModel, PhishVerdictModel, OffloadTasksModel
from .modelqueue_utils import ViewsHelper
from rest_framework import viewsets, status

from .serializers import UserSerializer
from load_commonutils import get_ts_instance

v_helper = ViewsHelper()


class IndexPageView(FormView):
    template_name = 'modelqueue/index.html'
    form_class = URLForm

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = self.request.META.get('REMOTE_ADDR')
        context['layout'] = self.request.GET.get('layout', 'vertical')
        context['ipaddress'] = ipaddress
        context['user'] = self.request.user
        context['UI_PROJECT_TITLE'] = settings.UI_PROJECT_TITLE
        return context

    def post(self, request, *args, **kwargs):
        form = URLForm(request.POST)
        if form.is_valid():
            analysis_url = form.cleaned_data['analysis_url']
            print "analysis_url : ", analysis_url
            pvm = v_helper.start_analysis(analysis_url)
            context = {'pvm': pvm }
            context['UI_PROJECT_TITLE'] = settings.UI_PROJECT_TITLE
            return render(request, 'modelqueue/resultpage.html', context)
        else:
            # TODO: Handle here for invalid cases
            print "invalid"
        return HttpResponse("Ok")


def check_status(request, uuid):
    pvm = get_object_or_404(PhishVerdictModel, unique_id=uuid)
    if pvm.analysis_stage == 0:
        crawl_url(request)
        time.sleep(0.1)
        extract_features(request)
        time.sleep(0.1)
        query_model(request)
        time.sleep(0.1)
        show_result(request)
        time.sleep(0.1)
    elif pvm.analysis_stage == 1:
        extract_features(request)
        time.sleep(0.1)
        query_model(request)
        time.sleep(0.1)
        show_result(request)
        time.sleep(0.1)
    elif pvm.analysis_stage == 2:
        query_model(request)
        time.sleep(0.1)
        show_result(request)
        time.sleep(0.1)
    elif pvm.analysis_stage == 3:
        show_result(request)
        time.sleep(0.1)
    else:
        # TODO: What should be the default action?
        pass

    pvm = get_object_or_404(PhishVerdictModel, unique_id=uuid)
    context = {'pvm': pvm }
    context['UI_PROJECT_TITLE'] = settings.UI_PROJECT_TITLE
    return render(request, 'modelqueue/resultpage.html', context)


def crawl_url(request):
    pending_crawling = PhishVerdictModel.objects.filter(analysis_stage=0)
    for each_pending_url in pending_crawling:
        v_helper.crawl_page(each_pending_url)
    # TODO: Consider appropriate response type
    return HttpResponse("Ok")


def extract_features(request):
    pending_feature_extraction = PhishVerdictModel.objects.filter(analysis_stage=1)
    for each_pending_feature_extraction in pending_feature_extraction:
        v_helper.extract_features(each_pending_feature_extraction)
    # TODO: Consider appropriate response type
    return HttpResponse("Ok")


def query_model(request):
    pending_querying_model = PhishVerdictModel.objects.filter(analysis_stage=2)
    for each_pending in pending_querying_model:
        v_helper.query_model(each_pending)
    # TODO: Consider appropriate response type
    return HttpResponse("Ok")


def show_result(request):
    pending_for_results = PhishVerdictModel.objects.filter(analysis_stage=3)
    for each_pending in pending_for_results:
        v_helper.provide_result(each_pending)
    # TODO: Consider appropriate response type
    return HttpResponse("Ok")


def request_task(request):
    """Returns 1 pending request for offline processing"""
    pending_crawling = PhishVerdictModel.objects.filter(analysis_stage=0)[:1]
    task_dict = {}
    for each_pending in pending_crawling:
        time_sha = hashlib.sha1(get_ts_instance()).hexdigest()
        otm = OffloadTasksModel(phish_verdict_model=each_pending, time_sha=time_sha)
        otm.save()
#         each_pending.each_pending = 5
#         each_pending.save()
        task_dict[otm._uid] = {}
        task_dict[otm._uid]['sha'] = time_sha
        task_dict[otm._uid]['analysis_url'] = otm._analysis_url
    print "request_task: ", task_dict
    jresponse = simplejson.dumps(task_dict)
    return HttpResponse(jresponse, content_type='application/json')


def request_task_bulk(request, count):
    pending_crawling = PhishVerdictModel.objects.filter(analysis_stage=0)[:count]
    task_dict = {}
    for each_pending in pending_crawling:
        time_sha = hashlib.sha1(get_ts_instance()).hexdigest()
        otm = OffloadTasksModel(phish_verdict_model=each_pending, time_sha=time_sha)
        otm.save()
#         each_pending.each_pending = 5
#         each_pending.save()
        task_dict[otm._uid] = {}
        task_dict[otm._uid]['sha'] = time_sha
        task_dict[otm._uid]['analysis_url'] = otm._analysis_url
    print "request_task_bulk: ",task_dict
    jresponse = simplejson.dumps(task_dict)
    return HttpResponse(jresponse, content_type='application/json')


@csrf_exempt
def respond_task_results(request):
    # TODO: Lets comply with csrf
    if request.method=='POST':
        received_json_data = simplejson.loads(request.body)
        print "received_json_data: ",received_json_data
        if v_helper.is_response_valid(received_json_data):
            # Update the Model based on the values recieved
            status, message = v_helper.update_from_api_response(received_json_data)
            if status:
                jresponse = simplejson.dumps({'message': message, 'status': status})
                return HttpResponse(jresponse, content_type='application/json')
            else:
                return HttpResponseBadRequest()

    return HttpResponseBadRequest()


@csrf_exempt
def post_single_analysisurl(request):
    # TODO: Lets comply with csrf
    if request.method=='POST':
        received_json_data = simplejson.loads(request.body)
        print "received_json_data: ",received_json_data
        if v_helper.is_analysisurl_request_valid(received_json_data):
            pvm = v_helper.start_analysis(received_json_data['analysis_url'])
            jresponse = simplejson.dumps({'uid': str(pvm.unique_id)})
            print 'jresponse: ',jresponse
            return HttpResponse(jresponse, content_type='application/json')
    return HttpResponseBadRequest()

@csrf_exempt
def get_single_verdict(request):
    # TODO: Lets comply with csrf
    if request.method=='POST':
        received_json_data = simplejson.loads(request.body)
        print "received_json_data: ",received_json_data
        status, msg = v_helper.process_get_verdict(received_json_data)
        print 'status, msg: ',status, msg
        if status:
            jresponse = simplejson.dumps({'uid': received_json_data['uid'], 'verdict':  msg })
            print 'jresponse: ',jresponse
            return HttpResponse(jresponse, content_type='application/json')
    return HttpResponseBadRequest()


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

