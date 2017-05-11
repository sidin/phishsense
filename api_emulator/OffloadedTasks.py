import os
import pprint
import socket

import api_localsettings

class OffloadedTasks(object):
    def __init__(self):
        self.final_response = {}
        self.uid = None
        self.sha = None
        self.analysis_url = None
        self.download_path = None
        self.analysis_stage = None
        self.features = None
        self.answer = None
        self.comments = {'worker_hostname': socket.gethostname(),
                         'worker_ipaddress': socket.gethostbyname(socket.gethostname())}

    def set_request_values(self, uid, sha, url):
        self.uid = uid
        self.sha = sha
        self.analysis_url = url

    def provide_response_dict(self):
        response_dict = {}
        response_dict['uid'] = self.uid
        response_dict['download_path'] = self.download_path
        response_dict['analysis_stage'] = self.analysis_stage
        response_dict['features'] = self.features
        response_dict['answer'] = self.answer
        response_dict['comments'] = self.comments
        response_dict['sha'] = self.sha
        return response_dict

    def perform_steps(self):
        download_path = api_localsettings.step1(api_localsettings.DUMP_LOCATION, self.analysis_url)
        self.download_path = os.path.abspath(download_path)
        self.analysis_stage = 1
        print 'Step 1 completed. %s' % (self.download_path,)
        api_localsettings.step2()
        print 'Step 2 placeholder'
        api_localsettings.step3()
        print 'Step 3 placeholder'

    def __str__(self):
        return "uid: %s  sha: %s  url: %s" % (self.uid, self.sha, self.analysis_url)

