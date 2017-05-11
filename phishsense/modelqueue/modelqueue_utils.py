import os
import sys
import hashlib
import datetime

from django.conf import settings

from .models import InvestigateUrlModel, PhishVerdictModel, OffloadTasksModel

from load_commonutils import step1, step2, step3


class ViewsHelper(object):
    """
    Class to help views for Business Logic
    """

    def whether_need_to_re_evaluate(self, ppvm):
        """Business Logic to decide whether we need to re-evaluate this URL"""
        # Currently it will always re-evaluate, Can put date condition or other business logic here
        return True

    def evaluate_previously_analysed_url(self, piumf):
        """
        Get a InvestigateUrlModel and return a PhishVerdictModel
        """
        pvm = PhishVerdictModel.objects.filter(investigate_url = piumf)[0]
        re_evaluate_decision = self.whether_need_to_re_evaluate(pvm)
        if re_evaluate_decision:
            pvm = PhishVerdictModel(investigate_url=piumf)
            pvm.save()
        else:
            # The previous evaluation holds good. Log here.
            pass
        return pvm

    def evaluate_url(self, analysis_url):
        """
        Method to perform the following:
        1. Verify whether the provided URL is seen before in the database
        2a. If Yes, get the most recent PhishVerdictModel of it.
        2b. If No, create one
        From 2a -> Based on some factor `X()` decide whether we need to re-evaluate it
        If yes, generate a PhishVerdictModel and provide a UUID to the caller to track back later
        If no, provide the result to the user
        """
        url_sha = hashlib.sha1(analysis_url).hexdigest()
        iumf, created = InvestigateUrlModel.objects.get_or_create(url_sha = url_sha,
                                                         defaults={'analysis_url': analysis_url})
        if created:
            pvm = PhishVerdictModel(investigate_url=iumf)
            pvm.save()
        else:
            pvm = self.evaluate_previously_analysed_url(iumf)
        return pvm

    def start_analysis(self, analysis_url):
        # 1. Get/Create InvestigateUrlModel
        # 2. Based on some logic, decide whether to perform phishverdict test again
        # 3. If No above, return older phishverdict result
        # 4. Else, crawl URL for content and save web page content
        # 5. Extract features
        # 6. Query Model
        # 7. Show Result
        pvm = self.evaluate_url(analysis_url)
        return pvm

    def crawl_page(self, pvm):
        """Method to get the PhishVerdictModel and crawl the web page"""
        # Crawl the web page here
        saved_filename = step1(settings.DUMP_LOCATION, pvm.investigate_url.analysis_url)
#         saved_filename = crawlHelper.go(pvm.investigate_url.analysis_url)
        # Change the PhishVerdictModel state
        pvm.analysis_stage = 1
        pvm.internal_download_path = os.path.abspath(saved_filename)
        pvm.modified_date = datetime.date.today()
        pvm.save()

    def extract_features(self, pvm):
        """Method to get the PhishVerdictModel and extract the features"""
        # TODO: Extract the features here
        step2()
        # Change the PhishVerdictModel state
        pvm.analysis_stage = 2
        pvm.modified_date = datetime.date.today()
        pvm.save()

    def query_model(self, pvm):
        """Method to get the PhishVerdictModel and query the model"""
        # TODO: Query the model here
        step3()
        # Change the PhishVerdictModel state
        pvm.analysis_stage = 3
        pvm.modified_date = datetime.date.today()
        pvm.save()

    def provide_result(self, pvm):
        """Method to get the PhishVerdictModel and provide the results"""
        # Change the PhishVerdictModel state
        pvm.analysis_stage = 4
        pvm.modified_date = datetime.date.today()
        pvm.save()

    def is_response_valid(self, received_json_data):
        """Method to verify that the API response adheres to the structure expected"""
        required_keys = ['uid', 'download_path', 'analysis_stage', 'features', 'answer', 'comments', 'sha']
        intersection = set(required_keys).intersection(received_json_data)
        if len(intersection) < len(required_keys):
            return False
        else:
            return True

    def is_analysisurl_request_valid(self, received_json_data):
        """Method to verify that the API response adheres to the structure expected"""
        if received_json_data.has_key('analysis_url'):
            return True
        else:
            return False

    def process_get_verdict(self, received_json_data):
        """Method to verify that the API response adheres to the structure expected"""
        if received_json_data.has_key('uid'):
            #TODO: Sort by date and send the latest verdcit/result
            pvm = PhishVerdictModel.objects.filter(unique_id=received_json_data['uid'])
            if pvm:
                if pvm[0].is_phishing() is None:
                    return False, 'UID In Process'
                else:
                    return True, pvm[0].is_phishing()
            else:
                return False, "Not Found"
        else:
            return False, "Need UID"

    def update_from_api_response(self, received_json_data):
        PhishVerdictModel.objects
        otmodel = OffloadTasksModel.objects.get(time_sha=received_json_data['sha'])
        print 'update_from_api_response otmodel: ',otmodel
        if otmodel:
            if str(otmodel.phish_verdict_model.unique_id) != received_json_data['uid']:
                # TODO: Log/Report here
                return False, settings.MESSAGE_API_UID_TAMPERING
            else:
                otmodel.phish_verdict_model.internal_download_path = received_json_data['download_path']
                otmodel.phish_verdict_model.comments = received_json_data['comments']
                otmodel.phish_verdict_model.analysis_stage = received_json_data['analysis_stage']
                # TODO: Uncomment following once we have the values coming from API
                #otmodel.phish_verdict_model.features = received_json_data['features']
                #otmodel.phish_verdict_model.answer = received_json_data['answer']
                otmodel.phish_verdict_model.save()
                return True, "OK"
        else:
            # TODO: Log/Report here
            return False, settings.MESSAGE_API_UID_TAMPERING

