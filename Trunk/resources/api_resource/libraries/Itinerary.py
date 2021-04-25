# Itinerary Schema
# Author: 

_version_ = '1.0' 

import sys
import os
import re
import io
import string
from robot import utils

class Itinerary:

    def get_fare_remarks(self, currency, quote_number, airline, routing, fare, tax, gst,
                         fuel_surcharge, transaction_fee, merchant_fee, total_amount, is_default, changes="Changes subject to fare",
                         cancellation="Cancellation Before departure: with fee", re_route="Not Permitted", valid_on="QF", min_stay= "Min 2 days", max_stay= "Max 1 month", total_for_all_tickets="1234.55"):
        """
            Return Air Fare Remarks
        """
        
        fare_remarks = self._generate_fare_remarks(currency, quote_number, airline, routing, fare, tax, gst,
                         fuel_surcharge, transaction_fee, merchant_fee, total_amount, is_default, changes,
                         cancellation, re_route, valid_on, min_stay, max_stay, total_for_all_tickets)
        return fare_remarks
    
    def get_policy_check_remarks(self, reason, advice, status):
        """
            Return Policy Check Remarks
        """
        
        policy_check_remarks = self._generate_policy_check_remarks(reason, advice, status)
        return policy_check_remarks
    
    def get_alternate_offer_remarks(self, currency, number, airline, routing, fare_basis,
                                    fare_including_taxes, more_info, changes, cancellation,
                                    valid_on, re_route, min_stay, max_stay):
        """
            Return Alternate Fare Remarks
        """
        alternate_offer_remarks = self._generate_alternate_offer_remarks(currency, number, airline, routing, fare_basis,
                                    fare_including_taxes, more_info, changes, cancellation,
                                    valid_on, re_route, min_stay, max_stay)
        return alternate_offer_remarks
    
    def _generate_fare_remarks(self, *argv):
        fare_remarks = [
            "************* ITINERARY QUOTE PER PASSENGER ***************",
            "QUOTE NUMBER: " + str(argv[1]),"AIRLINE: " + str(argv[2]),
            "ROUTING: "+ str(argv[3]),
            "FARE: " + str(argv[0]) + ' ' + str(argv[4]),
            "TAX: " + str(argv[0]) + ' ' + str(argv[5]),
            "GST: " + str(argv[0]) + ' ' + str(argv[6]),
            "SVC FEE FOR SURCHARGE: " + str(argv[0]) + ' ' + str(argv[7]),
            "TRANSACTION FEE: " + str(argv[0]) + ' ' + str(argv[8]),
            "MERCHANT FEE: " + str(argv[0]) + ' ' + str(argv[9]),
            "TOTAL AMOUNT: "+ str(argv[0]) + ' ' + str(argv[10])]
        
        restrictions = self._identify_fare_restrictions(str(argv[11]),str(argv[12]),str(argv[13]),str(argv[14]),
                                                        str(argv[15]),str(argv[16]),str(argv[17]))
        fare_remarks.extend(restrictions)

            #"TOTAL FOR ALL TICKETS: "+ str(argv[0]) + ' ' + str(argv[17])]
        return fare_remarks

    def _identify_fare_restrictions(self, is_default, *argv):
        restrictions = []
        print is_default
        if (is_default.lower() == 'false'):
            restrictions.append("CHANGES: "+ str(argv[0]))
            restrictions.append("CANCELLATION: "+ str(argv[1]))
            restrictions.append("RE ROUTE: "+ str(argv[2]))
            restrictions.append("VALID ON: "+ str(argv[3]))
            restrictions.append("MIN STAY: "+ str(argv[4]))
            restrictions.append("MAX STAY: "+ str(argv[5]))
            restrictions.append("ALL PRICES SUBJECT TO CHANGE AT ANYTIME WITHOUT NOTICE")
        else:
            restrictions.append("THIS TICKET MAY BE SUBJECT TO PENALTIES OR FARE INCREASE.")
            restrictions.append("CHANGES/CANCELLATION MAY BE SUBJECT TO A PENALTY OR FARE")
            restrictions.append("INCREASE UP TO AND INCLUDING THE TOTAL COST OF THE TICKET.")
            restrictions.append("NO REFUND FOR UNUSED PORTION ON CERTAIN FARES. TO RETAIN")
            restrictions.append("VALUE OF YOUR TICKET, YOU MUST CANCEL THE RESERVATION")
            restrictions.append("ON OR BEFORE YOUR TICKETED DEPARTURE TIME.")
            restrictions.append("ALL PRICES SUBJECT TO CHANGE AT ANYTIME WITHOUT NOTICE")
        return restrictions
    
    def _generate_alternate_offer_remarks(self):
        alternate_offer_remarks = [
            "*OFFER**ALTERNATE FARE: " + str(argv[1]) + "*",
            "*OFFER**AIRLINE: "+ str(argv[2]) + "*",
            "*OFFER**ROUTING: " + str(argv[3]) + "*",
            "*OFFER**FARE BASIS: " + str(argv[4]) + "*",
            "*OFFER**FARE INCLUDING AIRLINE TAXES: " + str(argv[0]) + ' ' + str(argv[5]) + "*",
            "*OFFER**MORE INFO: " + str(argv[6]) + "*",
            "*OFFER**CHANGES: " + str(argv[7]) + "*",
            "*OFFER**CANCELLATION: " + str(argv[8]) + "*",
            "*OFFER**VALID ON: "+ str(argv[9]) + "*",
            "*OFFER**REROUTE: "+ str(argv[10]) + "*",
            "*OFFER**MINIMUM STAY: "+ str(argv[11]) + "*",
            "*OFFER**MAXIMUM STAY: "+ str(argv[12]) + "*",
            "*OFFER**QUOTE PROVIDED EXCLUDES ALL APPLICABLE FEES AND CHARGES*",
            "*OFFER**ALL PRICES SUBJECT TO CHANGE WITHOUT NOTICE*",
            "*OFFER**.............................................*"]
        return alternate_offer_remarks
    
    def _generate_policy_check_remarks(self, *argv):
        policy_check_remarks = [
            "****************************************************",
            "POLICY WARNING",
            "REASON: " + str(argv[0]),
            "ADVICE: "+ str(argv[1]),
            "STATUS: " + str(argv[2])]
        return policy_check_remarks
