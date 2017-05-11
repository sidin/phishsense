import requests
import pprint

from OffloadedTasks import OffloadedTasks

from api_localsettings import REQUEST_URL2

def create_request_model_from_values(uid, sha, url):
    obj = OffloadedTasks()
    obj.set_request_values(uid, sha, url)
    return obj

def request_queueobjects():
    request_holder = []
    r = requests.get(REQUEST_URL2)
    json_response = r.json()
    print json_response
    for k,v in json_response.iteritems():
        obj = create_request_model_from_values(k, v['sha'], v['analysis_url'])
        request_holder.append(obj)
    for each in request_holder:
        print each


if __name__ == "__main__":
    request_queueobjects()
