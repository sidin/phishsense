import requests  
import simplejson

from api_localsettings import GET_VERDICT_URL

def get_verdict_single(data):
    headers = {'content-type': 'application/json'}
    server_response = requests.post(GET_VERDICT_URL, data=simplejson.dumps(data), headers=headers)
    print "send_analysis_response: ", server_response.content, server_response.status_code
    return server_response


if __name__ == "__main__":
    data = {'uid': 'fd8684ae-987d-4334-a793-9270a9e29af5' }
    resp = get_verdict_single(data)
    print resp

