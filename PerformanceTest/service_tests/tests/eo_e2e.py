import sys
import os
sys.path.append('..')

import json
import random
from locust import HttpLocust, TaskSet, task, events
from common.additional_handlers import additional_success_handler, additional_failure_handler

WORK_DIR = os.path.dirname(__file__)
events.request_success += additional_success_handler
events.request_failure += additional_failure_handler

global create_eo_request

eo_number="1903202133"
#
# with open('../test_data/create_eo.json', 'r') as create_eo:
#     create_eo_request = json.load(create_eo)

class ApacServiceTask(TaskSet):

    def on_start(self):
        auth_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOiJQb3dlciBFeHByZXNzIn0.LKK4C3niIf80Vt0tTKNv_TevgaHeohFZmJxg7rABnGk'
        self.client.headers = {'Authorization': auth_token}

    def load_random_country(self):
        countries = ['sg', 'hk']
        return "{}".format(random.choice(countries))


    @task(1)
    def exchange_order(self):
        json_string = '[{"recordLocator": "RCR123", "countryCode": "SG", "status": "New", "total": 250, "productCode": "37",\
        "uniqueId": "UEXR493_{ab897573-a443-44fe-80de-b7b5335f5a7b}", "accountNumber": "1009001","passengerName": "BEAR/SGOTHERS",\
        "serviceInfo": {"vendorContactPerson": "", "sellingFareToClient": 0, "nettCost": 250, "nettFare": 0,"grossFare": 0, "tax1": 0,\
        "tax2": 0, "nettCostInEo": 0, "vendorHandling": 0,"merchantFeeVendorHandlingFlag": false, "merchantFeeVendorHandling": 0, \
        "cwtHandling": 0,"merchantFeeCwtHandlingFlag": false, "merchantFeeCwtHandling": 0, "publishedFare": 0,"sellingPrice": 800, \
        "commission": 497.66, "discount": 0, "gst": 0, "gstAbsorb": true,"merchantFee": 0, "merchantFeeAbsorb": true, "uatp": false,\
        "totalSellingPrice": 747.66,"serviceFee": 0, "tfInNrcc": false, "fuelSurcharge": 0, "countryCode": "Singapore","type": "Other",\
        "entries": "SGL", "validityLength": 0, "validityType": "02","processingType": "NOR", "processingLength": 0, "visaNumber": "0123456",\
        "passengerId": "","formOfPayment": {"fopType": "INVOICE", "creditCardNumber": ""}},"vendor": {"code": "021238", "name": "Carlson Wagonlit GST",\
        "address1": "INTERCOMPANY - TRADE","address2": "", "city": "SIN", "supportEmail": "sgtest@test.com","contactInfo": [{"type": "Email",\
        "detail": "", "preferred": true},{"type": "Phone", "detail": "", "preferred": true},{"type": "Fax", "detail": "", "preferred": true}],\
        "country": "", "creditTerms": 0,"misc": false, "sortKey": "CWT GST", "contactPerson": "", "merchantFeeAbsorb": false},"agentId": "UEXR493",\
        "pcc": "SINWL2101", "agentName": "Waseem Pasha", "raiseCheque": "","pdfDescriptions": ["Visa Handling Fee", "FOR SINGAPORE",\
        "OTHER VISA - Single ENTRIES - VALID 0 Month(s)","PROCESSING - Normal - 0 Days"]}]'
        response = self.client.post("exchange-order/" + "sg", json=json.loads(json_string))
        global eo_number
        if response.text[3:11] == "eoNumber":
            eo_number = response.text[14:24]

    @task(6)
    def exchange_order_country_code_record_locator(self):
        record_locator = 'ABC123'
        self.client.get("exchange-order/" + self.load_random_country() + "/" + record_locator)

    @task(5)
    def exchange_order_country_code_eo_number(self):
        global eo_number
        # eo_number = '1903202133'
        self.client.get("exchange-order/" + self.load_random_country() + "/" + eo_number)

    @task(5)
    def exchange_order_pdf_eo_number(self):
        global eo_number
        # eo_number = '1903202133'
        self.client.get("exchange-order/pdf/" + eo_number)

    @task(6)
    def exchange_order_pull_eo(self):
        global eo_number
        json_string = """
        {
                        "accountNumber":"3377100023",
                        "agentId":"U060SXT",
                        "agentName":"sharad",
                        "countryCode":"SG",
                        "eoNumber":"""+eo_number+""",
                        "productCode":"06",
                        "uniqueId":"U060SXT_{ab897573-a443-44fe-80de-b7b5335f5a7b}",
                        "accountNumber":"1009001",
                        "passengerName":"BEAR/SGOTHERS",
                        "pcc": "SINWL2101",
                        "raiseCheque":"yes",
                        "recordLocator":"ABC123",
                        "status":"Pending"
        }
        """
        payload = json.loads(json_string)
        self.client.put("exchange-order/", json=payload)

class ApacServices(HttpLocust):
    host = "https://perf.apac-services.us-west-2.cbt-aws-cwt.com/apac-services-rest/api/"
    task_set = ApacServiceTask
    min_wait = 60000
    max_wait = 120000
