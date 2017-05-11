from django.conf.urls import url

from . import views, loginviews

app_name = 'modelqueue'

urlpatterns = [
    url(r'^$', views.IndexPageView.as_view(), name='index'),
    url(r'^index/$', views.IndexPageView.as_view(), name='index'),
    url(r'^status/(?P<uuid>[0-9a-z-]+)/$', views.check_status, name='check_status'),
    url(r'^signin/$', loginviews.signin, name='signin'),

    # URLs for various stages of finding verdict - Django way
    url(r'^crawl_url/$', views.crawl_url, name='crawl_url'),
    url(r'^extract_features/$', views.extract_features, name='extract_features'),
    url(r'^query_model/$', views.query_model, name='query_model'),
    url(r'^show_result/$', views.show_result, name='show_result'),

    # URLs enabling offloading tasks to caller (enabling REST APIs)
    url(r'^api/v1/request_task/$', views.request_task, name='request_task'),
    url(r'^api/v1/request_task_bulk/(?P<count>[0-9]+)/$', views.request_task_bulk, name='request_task_bulk'),
    url(r'^api/v1/respond_task_results/$', views.respond_task_results, name='respond_task_results'),
    url(r'^api/v1/post_single_analysisurl/$', views.post_single_analysisurl, name='post_single_analysisurl'),
    url(r'^api/v1/get_single_verdict/$', views.get_single_verdict, name='get_single_verdict'),
]
