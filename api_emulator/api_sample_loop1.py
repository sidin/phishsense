from api_request_single_task import request_single_queueobject
from api_response import send_analysis_response


def run_sample_loop():
    obj = request_single_queueobject()
    if obj is None:
        print 'Requests could not be fetched.'
        return
    obj.perform_steps()
    response_dict = obj.provide_response_dict()
    send_analysis_response(response_dict)


if __name__ == "__main__":
    run_sample_loop()

