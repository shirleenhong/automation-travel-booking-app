import sys
import os
sys.path.append('..')

from locust import HttpLocust, TaskSet, task, events
from requests.auth import HTTPBasicAuth
import json
from common.additional_handlers import additional_success_handler, additional_failure_handler

WORK_DIR = os.path.dirname(__file__)
events.request_success += additional_success_handler
events.request_failure += additional_failure_handler

global other_services_build_request
global other_services_parse_request
global remarks_services_build_request
global remarks_services_parse_request

with open('../test_data/other_services_build_request.json', 'r') as os_build:
    other_services_build_request = json.load(os_build)
with open('../test_data/other_services_parse_request.json', 'r') as os_parse:
    other_services_parse_request = json.load(os_parse)
with open('../test_data/remarks_services_build_request.json', 'r') as remarks_build:
    remarks_services_build_request = json.load(remarks_build)
with open('../test_data/remarks_services_parse_request.json', 'r') as remarks_parse:
    remarks_services_parse_request = json.load(remarks_parse)

class RemarksServiceTasks(TaskSet):

    def on_start(self):
        self.client.params = {'clientId': 'PowerExpress'}

    def authentication_header(self):
        client_id = "PowerExpress"
        client_secret = "immense35eardrum67groped"
        token_url = "https://perf.remarks-services.us-west-2.cbt-aws-cwt.com/connect/token"
        token_response = self.client.post(token_url, auth=HTTPBasicAuth(client_id, client_secret),\
                     data={'grant_type': 'client_credentials'})
        return {'Authorization': 'Bearer ' + token_response.json()['access_token']}         

    @task(1)
    def other_services_build(self):
        self.client.post('v1/OtherServices/build/', json=other_services_build_request, \
            headers=self.authentication_header())

    @task(1)
    def other_services_parse(self):
        self.client.post('v1/OtherServices/parse/', json=other_services_parse_request, \
            headers=self.authentication_header())

    @task(1)
    def remarks_services_build(self):
        self.client.post('v1/Remarks/build/', json=remarks_services_build_request, \
            headers=self.authentication_header())

    @task(1)
    def remarks_services_parse(self):
        self.client.post('v1/Remarks/parse/', json=remarks_services_parse_request, \
            headers=self.authentication_header())

    # @task(1)
    # def itinerary(self):
    #     self.client.post('build', json=payload, headers={'Authorization': 'Bearer ' + \
    #                     self.generate_token()})
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure("Remarks post failed, code: {}".format(response.status_code))

class RemarksServices(HttpLocust):
    host = 'https://perf.remarks-services.us-west-2.cbt-aws-cwt.com/api/'
    task_set = RemarksServiceTasks
    min_wait = 1000
    max_wait = 5000