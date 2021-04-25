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

class ApacServiceTask(TaskSet):

    def on_start(self):
        auth_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOiJQb3dlciBFeHByZXNzIn0.LKK4C3niIf80Vt0tTKNv_TevgaHeohFZmJxg7rABnGk'
        self.client.headers = {'Authorization': auth_token}

    def load_random_country(self):
        countries = ['sg', 'hk', 'in']
        return "{}".format(random.choice(countries))

    @task(1)
    def air_transactions(self):
        params = {'airlineCode': 'CX', 'bookingClasses':'', 'ccVendorCode': 'AX', \
            'ccType':'NRCC', 'clientAccountNmumber': '3050300003'}
        self.client.get("air-transactions/", params=params)

    @task(1)
    def air_transactions_put(self):
        json_string = """{"airlineCode":"5J","clientAccountNumber":"3377100023","countryCode":"IN","fopCode":"INV"}"""
        payload = json.loads(json_string)
        self.client.put("air-transactions/", json=payload)

    # @task(1)
    # def air_transactions_airline_code(self):
    #     #Update the test data
    #     airline_code = 'CX'
    #     self.client.get("air-transactions/" + airline_code)            
    #         if response.status_code != 200:
    #             response.failure("Error code: {} reason: {}".format(response.status_code, response.reason))

    @task(1)
    def airline_rules(self):
        self.client.get("airline-rules/")

    @task(1)
    def airports_airport_code(self):
        airport_code = 'DEL'
        self.client.get("airports/" + airport_code)            

    @task(1)
    def app_info(self):
        self.client.get("app-info/")            

    @task(1)
    def caches(self):
        self.client.get("caches/")            

    @task(1)
    def caches_cache_name(self):
        cache_name = 'air-transactions'
        self.client.get("caches/" + cache_name)            

    @task(1)
    def caches_evict_cache_name(self):
        cache_name = 'air-transactions'
        self.client.get("caches/evict/" + cache_name)            

    @task(1)
    def clients_client_account_number(self):
        client_account_number = '2077200001'
        self.client.get("clients/" + client_account_number)            

    @task(2)
    def client_req(self):
        json_string = """{"clientId":1827,"name":"Genpact Mobility Services Pvt Ltd","clientAccountNumber":"3377100023","pricingId":20,"exemptTax":false,"mfProducts":[{"productCode":"0","subjectToMf":false,"standard":false},{"productCode":"1","subjectToMf":false,"standard":false},{"productCode":"2","subjectToMf":false,"standard":false},{"productCode":"3","subjectToMf":false,"standard":false},{"productCode":"4","subjectToMf":false,"standard":false},{"productCode":"6","subjectToMf":false,"standard":false},{"productCode":"7","subjectToMf":false,"standard":false},{"productCode":"8","subjectToMf":false,"standard":false},{"productCode":"9","subjectToMf":false,"standard":false},{"productCode":"12","subjectToMf":false,"standard":false},{"productCode":"13","subjectToMf":false,"standard":false},{"productCode":"14","subjectToMf":false,"standard":false},{"productCode":"15","subjectToMf":false,"standard":false},{"productCode":"16","subjectToMf":false,"standard":false},{"productCode":"17","subjectToMf":false,"standard":false},{"productCode":"18","subjectToMf":false,"standard":false},{"productCode":"19","subjectToMf":false,"standard":false},{"productCode":"24","subjectToMf":false,"standard":false},{"productCode":"25","subjectToMf":false,"standard":false},{"productCode":"26","subjectToMf":false,"standard":false},{"productCode":"27","subjectToMf":false,"standard":false},{"productCode":"28","subjectToMf":false,"standard":false},{"productCode":"35","subjectToMf":false,"standard":false},{"productCode":"36","subjectToMf":false,"standard":false},{"productCode":"37","subjectToMf":false,"standard":false},{"productCode":"39","subjectToMf":false,"standard":false},{"productCode":"40","subjectToMf":false,"standard":false},{"productCode":"43","subjectToMf":false,"standard":false},{"productCode":"50","subjectToMf":false,"standard":false},{"productCode":"66","subjectToMf":false,"standard":false},{"productCode":"85","subjectToMf":false,"standard":false},{"productCode":"86","subjectToMf":false,"standard":false},{"productCode":"87","subjectToMf":false,"standard":false}],"standardMfProduct":false,"applyMfCc":true,"applyMfBank":false,"merchantFee":0,"lccSameAsInt":false,"lccDdlFeeApply":"TF","intDdlFeeApply":"TF"}""" 
        payload = json.loads(json_string)        
        self.client.put("clients/", json=payload)            

    @task(2)
    def exchange_order_country_code_eo_number(self):
        eo_number = '1808100491'
        self.client.get("exchange-order/" + self.load_random_country() + "/" + eo_number)            

    @task(2)
    def exchange_order_country_code_record_locator(self):
        record_locator = '1808100491'
        self.client.get("exchange-order/" + self.load_random_country() + "/" + record_locator)            

    @task(2)
    def exchange_order_car_vendors(self):
        self.client.get("exchange-order/car-vendors")            

    @task(2)
    def exchange_order_in_eo_number(self):
        eo_number = '1808100491'
        self.client.get("exchange-order/in/" + eo_number)            

    @task(2)
    def exchange_order_in_record_locator(self):
        record_locator = '1808100491'
        self.client.get("exchange-order/in/" + record_locator)            

    @task(2)
    def exchange_order_pdf_eo_number(self):
        eo_number = '1808100491'
        self.client.get("exchange-order/pdf/" + eo_number)            

    @task(2)
    def exchange_order_room_types(self):
        self.client.get("exchange-order/room-types/")            

    @task(2)
    def exchange_order_vmpd(self):
        self.client.get("exchange-order/vmpd/")            

    @task(2)
    def exchange_orders(self):
        country = self.load_random_country()
        if country == 'in':
            country = "IN"
        params = {'countryCode': country}
        self.client.get("exchange-orders", params=params)            

    @task(2)
    def exchange_order(self):
        json_string = """{"accountNumber":"3377100023","agentId":"jf","agentName":"user","countryCode":"IN","eoAction":"Email","eoNumber":"1234567","productCode":"05","raiseCheque":"yes","recordLocator":"ABC123","status":"New","total":100}"""
        payload = json.loads(json_string)        
        self.client.put("exchange-order/", json=payload)            

    @task(2)
    def insurance(self):
        self.client.get("insurance")            

    @task(2)
    def obt_list(self):
        self.client.get("obt-list/" + self.load_random_country())            

    @task(2)
    def report_headers(self):
        self.client.get("report-headers/" + self.load_random_country())            

    @task(2)
    def product_country_code(self):
        self.client.get("products/" + self.load_random_country())            

    @task(2)
    def remarks(self):
        json_string = """{"countryCode":"in","productType":"CI","remarkType":"E","text":"test"}"""
        payload = json.loads(json_string)        
        self.client.put("remarks/", json=payload)            

    @task(2)
    def remarks_country_code_product_type_remark_type(self):
        product_types = ['CT', 'CX', 'HL', 'TR', 'VI']
        remark_types = ['E', 'I']
        remarks_category = u"/".join([self.load_random_country(), \
                random.choice(product_types), random.choice(remark_types)])
        # overiding exception response
        self.client.get("remarks/" + remarks_category)

    @task(2)
    def other_services_fees(self):
        json_string = """{"airSegmentCount":0,"airlineCommissionPercent":3,"airlineOverheadCommission":0,"airlineOverheadCommissionByPercent":true,"airlineOverheadCommissionPercent":2,"baseFare":1000,"cityCode":"SIN","clientAccountNumber":"1026100093","clientOverheadCommissionPercent":100,"commissionEnabled":true,"discountEnabled":true,"discountPercent":100,"fee":100,"feeOverride":true,"gstEnabled":true,"markupEnabled":false,"merchantFeePercent":3,"othTax1":2,"othTax2":1,"othTax3":3,"overheadCommissionEnabled":true,"platCarrier":"0Z","product":{"gstPercent":1.4,"ot1Percent":0.05,"ot2Percent":0.05},"tripType":"I","yqTax":5}"""
        payload = json.loads(json_string)        
        self.client.post("other-service-fees/air-fees/in/", json=payload)            

    @task(2)
    def other_services_fees_non_air_fees_in(self):
        json_string = """{"ccType":"","clientAccountNumber":"2077200001","commission":3,"commissionByPercent":false,"commissionPercent":0,"discount":3,"discountByPercent":false,"discountPercent":0,"costAmount":3,"fopMode":3,"fopNumber":"","fopType":"INV","product":{"gstPercent":14.0,"ot1Percent":0.5,"ot2Percent":0.5,"productCode":"8"}}""" 
        payload = json.loads(json_string)
        self.client.post("other-service-fees/non-air-fees/in", json=payload)            

    #POST
    # @task(1)
    # def exchange_order_country_code(self):
    #     self.client.post("exchange-order/" + self.load_random_country())

    # @task(1)
    # def exchange_order_in(self):
    #     self.client.post("exchange-order/in")

    # @task(1)
    # def exchange_order_in(self):
    #     self.client.post("other-service-fees/air/fees/" + self.load_random_country())

    # @task(1)
    # def exchange_order_country_code(self):
    #     self.client.get("exchange-order/" + self.load_random_country())

    # @task(1)
    # def exchange_order_email_eo_number(self):
    #     eo_number = 
    #     self.client.get("exchange-order/email/" + eo_number)

    # @task(1)
    # def other_services_nett_cost(self):
    #     self.client.post("other-service-fees/nett-cost/")

    # @task(1)
    # def other_services_non_air_fees_country_code(self):
    #     self.client.post("other-service-fees/non-air-fees/" + self.load_random_country())
    # @task(1)
    # def other_services_fees_visa_fees(self):
    #     self.client.post("other-service-fees/visa-fees")

    # @task(1)
    # def service_fees(self):
    #     self.client.post("service-fees")

class ApacServices(HttpLocust):
    host = "https://perf.apac-services.us-west-2.cbt-aws-cwt.com/apac-services-rest/api/"
    task_set = ApacServiceTask
    min_wait = 60000
    max_wait = 120000