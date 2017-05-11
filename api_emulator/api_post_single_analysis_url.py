import requests  
import simplejson

from api_localsettings import POST_SINGLE_ANALYSIS_URL1, TEST_ANALYSISURL

def send_url_to_analyse(data):
    headers = {'content-type': 'application/json'}
    server_response = requests.post(POST_SINGLE_ANALYSIS_URL1, data=simplejson.dumps(data), headers=headers)
    print "send_analysis_response: ", server_response.content, server_response.status_code
    return server_response


if __name__ == "__main__":

    data = {'analysis_url': TEST_ANALYSISURL }
    resp = send_url_to_analyse(data)
    print resp

