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

class ApacServiceTaskHK(TaskSet):
    eo_number = "1904206106"
    def on_start(self):
        auth_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOiJQb3dlciBFeHByZXNzIn0.LKK4C3niIf80Vt0tTKNv_TevgaHeohFZmJxg7rABnGk'
        self.client.headers = {'Authorization': auth_token}

    @task(2)
    def obt_list(self):
        self.client.get("obt-list/" + "HK")

    @task(2)
    def product_country_code(self):
        self.client.get("products/" + "HK")

    @task(15)
    def get_misc_fees_request(self):
        json_string = """
                    {
                      "clientAccountNumber": "3050300003",
                      "fopType": "CX",
                      "gstAbsorb": true,
                      "gstPercent": 0,
                      "merchantFeeAbsorb": true,
                      "nettCost": 0,
                      "sellingPrice": 0
                    }
                    """
        payload = json.loads(json_string)
        self.client.post("other-service-fees/" + "non-air-fees/" + "hk", json=payload)

    @task(3)
    def exchange_order_1(self):
        json_string = '[{"recordLocator": "RCR123", "countryCode": "HK", "status": "New", "total": 250, "productCode": "18",\
        "uniqueId": "UEXR493_{ab897573-a443-44fe-80de-b7b5335f5a7b}", "accountNumber": "3050300003","passengerName": "BEAR/HKOTHERS",\
        "serviceInfo": {"vendorContactPerson": "", "sellingFareToClient": 0, "nettCost": 250, "nettFare": 0,"grossFare": 0, "tax1": 0,\
        "tax2": 0, "nettCostInEo": 0, "vendorHandling": 0,"merchantFeeVendorHandlingFlag": false, "merchantFeeVendorHandling": 0, \
        "cwtHandling": 0,"merchantFeeCwtHandlingFlag": false, "merchantFeeCwtHandling": 0, "publishedFare": 0,"sellingPrice": 800, \
        "commission": 497.66, "discount": 0, "gst": 0, "gstAbsorb": true,"merchantFee": 0, "merchantFeeAbsorb": true, "uatp": false,\
        "totalSellingPrice": 747.66,"serviceFee": 0, "tfInNrcc": false, "fuelSurcharge": 0, "countryCode": "Hongkong","type": "Other",\
        "entries": "HKL", "validityLength": 0, "validityType": "02","processingType": "NOR", "processingLength": 0, "visaNumber": "0123456",\
        "passengerId": "","formOfPayment": {"fopType": "INVOICE", "creditCardNumber": ""}},"vendor": {"code": "021238", "name": "Carlson Wagonlit GST",\
        "address1": "INTERCOMPANY - TRADE","address2": "", "city": "SIN", "supportEmail": "hktest@test.com","contactInfo": [{"type": "Email",\
        "detail": "", "preferred": true},{"type": "Phone", "detail": "", "preferred": true},{"type": "Fax", "detail": "", "preferred": true}],\
        "country": "", "creditTerms": 0,"misc": false, "sortKey": "CWT GST", "contactPerson": "", "merchantFeeAbsorb": false},"agentId": "UEXR493",\
        "pcc": "HKGWL2102", "agentName": "Waseem Pasha", "raiseCheque": "","pdfDescriptions": ["Visa Handling Fee", "FOR HONGKONG",\
        "OTHER VISA - Single ENTRIES - VALID 0 Month(s)","PROCESSING - Normal - 0 Days"]}]'
        self.client.post("exchange-order/" + "hk", json=json.loads(json_string))

    @task(3)
    def exchange_order_2(self):
        json_string = '[{"recordLocator": "RCR123", "countryCode": "HK", "status": "New", "total": 250, "productCode": "12",\
        "uniqueId": "UEXR493_{ab897573-a443-44fe-80de-b7b5335f5a7b}", "accountNumber": "3050300003","passengerName": "BEAR/HKOTHERS",\
        "serviceInfo": {"vendorContactPerson": "", "sellingFareToClient": 0, "nettCost": 250, "nettFare": 0,"grossFare": 0, "tax1": 0,\
        "tax2": 0, "nettCostInEo": 0, "vendorHandling": 0,"merchantFeeVendorHandlingFlag": false, "merchantFeeVendorHandling": 0, \
        "cwtHandling": 0,"merchantFeeCwtHandlingFlag": false, "merchantFeeCwtHandling": 0, "publishedFare": 0,"sellingPrice": 800, \
        "commission": 497.66, "discount": 0, "gst": 0, "gstAbsorb": true,"merchantFee": 0, "merchantFeeAbsorb": true, "uatp": false,\
        "totalSellingPrice": 747.66,"serviceFee": 0, "tfInNrcc": false, "fuelSurcharge": 0, "countryCode": "Hongkong","type": "Other",\
        "entries": "HKL", "validityLength": 0, "validityType": "02","processingType": "NOR", "processingLength": 0, "visaNumber": "0123456",\
        "passengerId": "","formOfPayment": {"fopType": "INVOICE", "creditCardNumber": ""}},"vendor": {"code": "021238", "name": "Carlson Wagonlit GST",\
        "address1": "INTERCOMPANY - TRADE","address2": "", "city": "SIN", "supportEmail": "sgtest@test.com","contactInfo": [{"type": "Email",\
        "detail": "", "preferred": true},{"type": "Phone", "detail": "", "preferred": true},{"type": "Fax", "detail": "", "preferred": true}],\
        "country": "", "creditTerms": 0,"misc": false, "sortKey": "CWT GST", "contactPerson": "", "merchantFeeAbsorb": false},"agentId": "UEXR493",\
        "pcc": "HKGWL2102", "agentName": "Waseem Pasha", "raiseCheque": "","pdfDescriptions": ["Visa Handling Fee", "FOR HONGKONG",\
        "OTHER VISA - Single ENTRIES - VALID 0 Month(s)","PROCESSING - Normal - 0 Days"]}]'
        self.client.post("exchange-order/" + "hk", json=json.loads(json_string))

    @task(3)
    def exchange_order_country_code_record_locator(self):
        record_locator = 'RCR123'
        # self.client.get("exchange-order/" + self.load_random_country() + "/" + record_locator)
        self.client.get("exchange-order/" + "hk" + "/" + record_locator)

    @task(2)
    def exchange_order_country_code_eo_number(self):
        # global eo_number
        # eo_number = '1903202133'
        self.client.get("exchange-order/" + "hk" + "/" + self.eo_number)
        # self.client.get("exchange-order/" + self.load_random_country() + "/" + eo_number)

    @task(1)
    def exchange_order_pdf_eo_number(self):
        # global eo_number
        # eo_number = '1903202133'
        self.client.get("exchange-order/pdf/" + self.eo_number)

    @task(1)
    def itinerary_remarks(self):
        self.client.get("remarks/hk/cx/i")

    @task(1)
    def exchange_order_remarks(self):
        self.client.get("remarks/hk/cx/e")

    @task(3)
    def update_exchange_order(self):
        # global eo_number
        json_string = """
        {
                        "accountNumber":"3050300003",
                        "agentId":"U060SXT",
                        "agentName":"sharad",
                        "countryCode":"HK",
                        "eoNumber":"""+self.eo_number+""",
                        "productCode":"12",
                        "uniqueId":"U060SXT_{ab897573-a443-44fe-80de-b7b5335f5a7b}",
                        "passengerName":"BEAR/HKOTHERS",
                        "pcc": "HKGWL2102",
                        "raiseCheque":"yes",
                        "recordLocator":"RCR123",
                        "status":"Completed"
        }
        """
        payload = json.loads(json_string)
        self.client.put("exchange-order/", json=payload)

class ApacServiceTaskSG(TaskSet):
    eo_number = "1904206106"
    def on_start(self):
        auth_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOiJQb3dlciBFeHByZXNzIn0.LKK4C3niIf80Vt0tTKNv_TevgaHeohFZmJxg7rABnGk'
        self.client.headers = {'Authorization': auth_token}

    def load_random_country(self):
        countries = ['sg', 'hk']
        return "{}".format(random.choice(countries))

    @task(2)
    def obt_list(self):
        # self.client.get("obt-list/" + self.load_random_country().upper())
        self.client.get("obt-list/" + "SG")

    @task(2)
    def product_country_code(self):
        self.client.get("products/" + "SG")

    @task(8)
    def get_misc_fees_request(self):
        json_string = """
                    {
                      "clientAccountNumber": "1009001",
                      "fopType": "CX",
                      "gstAbsorb": true,
                      "gstPercent": 0,
                      "merchantFeeAbsorb": true,
                      "nettCost": 0,
                      "sellingPrice": 0
                    }
                    """
        payload = json.loads(json_string)
        self.client.post("other-service-fees/" + "non-air-fees/" + "sg", json=payload)

    @task(1)
    def exchange_order_1(self):
        json_string = '[{"recordLocator": "RCR123", "countryCode": "SG", "status": "New", "total": 250, "productCode": "32",\
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
        self.client.post("exchange-order/" + "sg", json=json.loads(json_string))

    @task(1)
    def exchange_order_2(self):
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
        self.client.post("exchange-order/" + "sg", json=json.loads(json_string))

    @task(3)
    def exchange_order_country_code_record_locator(self):
        record_locator = 'RCR123'
        # self.client.get("exchange-order/" + self.load_random_country() + "/" + record_locator)
        self.client.get("exchange-order/" + "sg" + "/" + record_locator)

    @task(2)
    def exchange_order_country_code_eo_number(self):
        self.client.get("exchange-order/" + "sg" + "/" + self.eo_number)
        # self.client.get("exchange-order/" + self.load_random_country() + "/" + eo_number)

    @task(1)
    def exchange_order_pdf_eo_number(self):
        self.client.get("exchange-order/pdf/" + self.eo_number)

    @task(2)
    def itinerary_remarks(self):
        self.client.get("remarks/sg/cx/i")

    @task(2)
    def exchange_order_remarks(self):
        self.client.get("remarks/sg/cx/e")

    @task(1)
    def update_exchange_order(self):
        json_string = """
        {
                        "accountNumber":"3377100023",
                        "agentId":"U060SXT",
                        "agentName":"sharad",
                        "countryCode":"SG",
                        "eoNumber":"""+self.eo_number+""",
                        "productCode":"06",
                        "uniqueId":"U060SXT_{ab897573-a443-44fe-80de-b7b5335f5a7b}",
                        "passengerName":"BEAR/SGOTHERS",
                        "pcc": "SINWL2101",
                        "raiseCheque":"yes",
                        "recordLocator":"ABC123",
                        "status":"Pending"
        }
        """
        payload = json.loads(json_string)
        self.client.put("exchange-order/", json=payload)

class ApacServicesHK(HttpLocust):
    weight = 1
    host = "https://perf.apac-services.us-west-2.cbt-aws-cwt.com/apac-services-rest/api/"
    task_set = ApacServiceTaskHK
    min_wait = 20000
    max_wait = 120000

class ApacServicesSG(HttpLocust):
    weight = 1
    host = "https://perf.apac-services.us-west-2.cbt-aws-cwt.com/apac-services-rest/api/"
    task_set = ApacServiceTaskSG
    min_wait = 20000
    max_wait = 120000

