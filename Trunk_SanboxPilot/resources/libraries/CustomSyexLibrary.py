# Library for Field Format Checker using the Builtin function on Python
# Author: Sunny Postrado

_version_ = '1.0' 

import sys
import os
import win32clipboard
#from datetime import datetime, timedelta
import datetime
import time
import re
import io
import subprocess
import string
from robot import utils

class CustomSyexLibrary:
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    def check_format_alphanumeric(self, text, minlen, maxlen):
        """ Check if string is alphanumeric and satisfies the minimum and maximum length

        Examples:
        
        | ${result} =  | Check Format Alphanumeric    | TEXTA  |   1   |    5  |  # Result is True    |
        | ${result} =  | Check Format Alphanumeric    | TEX43  |   1   |    5  |  # Result is True    |
        | ${result} =  | Check Format Alphanumeric    | 12345  |   1   |    5  |  # Result is True    | 
        | ${result} =  | Check Format Alphanumeric    | TEXTA  |   1   |    4  |  # Result is False   |
        | ${result} =  | Check Format Alphanumeric    | TE     |   3   |    3  |  # Result is False   |
        | ${result} =  | Check Format Alphanumeric    | TEX4#  |   1   |    5  |  # Result is False   |
        """
        try:
            if text.isalnum() and self._length_min_max(text, minlen, maxlen):
                return True
            else:
                return False
        except ValueError, err:
            raise AssertionError(err)

    def check_format_alpha(self, text, minlen, maxlen):
        """ Check if string consists of letters only and satisfies the minimum and maximum length

        Examples:
        
        | ${result} =   | Check Format Alpha    | TEXTA   |    1  |    5  |  # Result is True    |
        | ${result} =   | Check Format Alpha    | TEX43   |    1  |    5  |  # Result is False   |
        | ${result} =   | Check Format Alpha    | 12345   |    1  |    5  |  # Result is False   | 
        | ${result} =   | Check Format Alpha    | TEXTA   |    1  |    4  |  # Result is False   |
        | ${result} =   | Check Format Alpha    | TE      |    3  |    3  |  # Result is False   |
        | ${result} =   | Check Format Alpha    | TEXA#   |    1  |    5  |  # Result is False   |
        """
        try:
            if text.isalpha() and self._length_min_max(text, minlen, maxlen):
                return True
            else:
                return False
        except ValueError, err:
            raise AssertionError(err)

    def check_format_numeric(self, text, minlen, maxlen):
        """ Check if string is numeric and satisfies the minimum and maximum length

        Examples:
        
        | ${result} =   | Check Format Numeric    | 12345   |    1  |    5  |  # Result is True    |
        | ${result} =   | Check Format Numeric    | 123TE   |    1  |    5  |  # Result is False   |
        | ${result} =   | Check Format Numeric    | 12345   |    1  |    5  |  # Result is False   | 
        | ${result} =   | Check Format Numeric    | 12345   |    1  |    4  |  # Result is False   |
        | ${result} =   | Check Format Numeric    | 12      |    3  |    3  |  # Result is False   |
        | ${result} =   | Check Format Numeric    | 1234#   |    1  |    5  |  # Result is False   |
        """
        try:
            if text.isdigit() and self._length_min_max(text, minlen, maxlen):
                return True
            else:
                return False
        except ValueError, err:
            raise AssertionError(err)

    def _length_min_max(self, text, lmin, lmax):
        try:
            if len(text) >= int(lmin) and len(text) <= int(lmax):
                return True
            else:
                return False
        except ValueError, err:
            raise AssertionError(err)

    def get_home_dir_path(self):
        """To obtain the home directory path
        """
        try:
            hpath = os.path.expanduser('~')

            return hpath
        except ValueError, err:
            raise AssertionError(err)

    def get_data_from_clipboard_old(self):
        try:
            time.sleep(2)
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return data
        except ValueError, err:
            raise AssertionError(err)
        
    def get_data_from_clipboard(self):
        try:
            time.sleep(2)
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                    return data
                else:
                    return "Empty"
            finally:
                win32clipboard.CloseClipboard()
        except ValueError, err:
            raise AssertionError(err)
        
    def clear_data_from_clipboard(self):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
        except ValueError, err:
            raise AssertionError(err)
    
    def add_days_to_current_date(self, time, format, result_format='timestamp', exclude_mills=False, date_format=None):
        try:
            date = Date(datetime.now(), date_format) + Time(time)
            date2 = date.convert(result_format)
            str = utils.get_time(format, utils.parse_time(date2))
            return str
        except ValueError, err:
            raise AssertionError(err)

    def subtract_days_to_current_date(self, time, format, result_format='timestamp', exclude_mills=False, date_format=None):
        try:
            date = Date(datetime.now(), date_format) - Time(time)
            date2 = date.convert(result_format)
            str = utils.get_time(format, utils.parse_time(date2))
            return str
        except ValueError, err:
            raise AssertionError(err)

    def add_days_to_current_date_availability(self, time, format1, format2, result_format='timestamp', exclude_mills=False, date_format=None):
        try:
            date = Date(datetime.now(), date_format) + Time(time)
            date2 = date.convert(result_format)
            str1 = utils.get_time(format1, utils.parse_time(date2))
            str2 = self._get_month_name (utils.get_time(format2, utils.parse_time(date2)))
            return str1 + str2
        except ValueError, err:
            raise AssertionError(err)

    def subtract_days_to_current_date_availability(self, time, format1, format2, result_format='timestamp', exclude_mills=False, date_format=None):
        try:
            date = Date(datetime.now(), date_format) - Time(time)
            date2 = date.convert(result_format)
            str1 = utils.get_time(format1, utils.parse_time(date2))
            str2 = self._get_month_name (utils.get_time(format2, utils.parse_time(date2)))
            return str1 + str2
        except ValueError, err:
            raise AssertionError(err)

    def _get_month_name(self, date):
        try:
            return{
                "01" : "JAN",
                "02" : "FEB",
                "03" : "MAR",
                "04" : "APR",
                "05" : "MAY",
                "06" : "JUN",
                "07" : "JUL",
                "08" : "AUG",
                "09" : "SEP",
                "10" : "OCT",
                "11" : "NOV",
                "12": "DEC"
                }[date]
        except ValueError, err:
            raise AssertionError(err)
        except ValueError, err:
            raise AssertionError(err)

    def remove_leading_and_ending_spaces(self, item):
        try:
            str = item.strip()
            return str
        except ValueError, err:
            raise AssertionError(err)

    def remove_all_spaces(self, item):
        try:
            str = item.replace(" ", "")
            return str
        except ValueError, err:
            raise AssertionError(err)

    def delete_file(self, file):
        try:
            os.remove(file)
        except ValueError, err:
            raise AssertionError(err)

    def convert_string_to_uppercase(self, string):
        try:
            str = string.upper()
            return str
        except ValueError, err:
            raise AssertionError(err)

    def convert_string_to_lowercase(self, string):
        try:
            str = string.lower()
            return str
        except ValueError, err:
            raise AssertionError(err)
    
    def get_line_number(self, file, item):
        try:
            for i, line in enumerate(io.open(file, encoding="utf-8"), 1):
              if item in line:
                return i
        except ValueError, err:
            raise AssertionError(err)
        
    def check_Syex(self,procName):
        cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        try:
            for line in proc.stdout:
                if procName in line:
                    syex = 1
                    return syex
        except ValueError, err:
            raise AssertionError(err)
        
    def get_MonthDate(self,strDate):
        strLength = len(strDate)
        
        print(strLength)
        if strLength == 10:
            strDay = strDate[3:5]
            strMonth = strDate[0:2]
        if strLength == 8:
            strDay = strDate[2:3]
            strMonth = strDate[0:1]
        if strLength == 9:
            strChecker = strDate[2]
            print(strChecker)
            if strChecker != '/':
                strDay = strDate[2:3]
                strMonth = strDate[0:1]
            if strChecker == '/':
                strDay = strDate[3:4]
                strMonth = strDate[0:2]
            strMonthDate = strMonth + strDay
            return strMonthDate

    def get_CompName(self):
        try:
            strComName = win32api.GetComputerName()    
            return strComName
        except ValueError, err:
            raise AssertionError(err)

    def get_UserName(self):
        try:
            strUserName = os.environ['USERNAME']   
            return strUserName
        except ValueError, err:
            raise AssertionError(err)
