import requests
import pprint

from OffloadedTasks import OffloadedTasks

from api_localsettings import REQUEST_URL1

# crawl_url(request)
# extract_features(request)
# query_model(request)
# show_result(request)

def create_request_model_from_values(uid, sha, url):
    obj = OffloadedTasks()
    obj.set_request_values(uid, sha, url)
    return obj

def request_single_queueobject():
    r = requests.get(REQUEST_URL1)
    json_response = r.json()
    print "request_single_queueobject: ", json_response
    if not json_response:
        return None
    for k,v in json_response.iteritems():
        print k, v
        obj = create_request_model_from_values(k, v['sha'], v['analysis_url'])
    return obj


if __name__ == "__main__":
    obj = request_single_queueobject()
