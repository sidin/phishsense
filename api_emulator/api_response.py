import requests  
import simplejson

from OffloadedTasks import OffloadedTasks

from api_localsettings import RESPONSE_URL1

def send_analysis_response(data):
    headers = {'content-type': 'application/json'}
    server_response = requests.post(RESPONSE_URL1, data=simplejson.dumps(data), headers=headers)
    print "send_analysis_response: ", server_response


if __name__ == "__main__":
    data = {'data':[
                    {'uid': 'uid',
                     'download_path':'download_path',
                     'analysis_stage': 'analysis_stage',
                     'features': 'features',
                     'answer': 'answer',
                     'comments': 'comments'}
            ]}
    send_analysis_response(data)

