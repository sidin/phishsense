import os
import sys

BASE_DIR = os.path.dirname(__file__)
DUMP_LOCATION = os.path.join(BASE_DIR, '../crawled_files')

BUSINESS_STEPS_PATH = os.path.join(BASE_DIR, '../businesslogic')
sys.path.append(BUSINESS_STEPS_PATH)
from invoke_steps import step1, step2, step3

DJANGO_SERVER_HOST = "localhost"
DJANGO_SERVER_PORT = "8111"
BULK_COUNT = 1

REQUEST_URL1 = "http://%s:%s/phishsense/api/v1/request_task/" % (DJANGO_SERVER_HOST, DJANGO_SERVER_PORT)
REQUEST_URL2 = "http://%s:%s/phishsense/api/v1/request_task_bulk/%d" % (DJANGO_SERVER_HOST, DJANGO_SERVER_PORT, BULK_COUNT)
RESPONSE_URL1 = "http://%s:%s/phishsense/api/v1/respond_task_results/" % (DJANGO_SERVER_HOST, DJANGO_SERVER_PORT)
POST_SINGLE_ANALYSIS_URL1 = "http://%s:%s/phishsense/api/v1/post_single_analysisurl/" % (DJANGO_SERVER_HOST, DJANGO_SERVER_PORT)
GET_VERDICT_URL = "http://%s:%s/phishsense/api/v1/get_single_verdict/" % (DJANGO_SERVER_HOST, DJANGO_SERVER_PORT)


TEST_ANALYSISURL = 'http://timesofindia.indiatimes.com/tech/tech-news/Flipkart-announces-next-Big-Billion-Sale-dates/articleshow/49138784.cms?'
