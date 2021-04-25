# -*- coding: utf-8 -*-
from collections import Counter, OrderedDict
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.application import Application
from pywinauto import Desktop
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from Constant import CurrencyConstant
from Constant import CountryConstant
from robot.api import logger
import itertools
import datetime
import time
import calendar
import os
import sys
import pywinauto
import autoit
import getpass
import re
import random
import math
from RailLibrary import RailLibrary
from pywinauto import keyboard
# from ImageHorizonLibrary import ImageHorizonLibrary
reload(sys)
sys.setdefaultencoding('Cp1252')

class ExtendedCustomSyExLibrary:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def launch_power_express(self, version, syex_env, username):

        autoit.process_close('PowerExpress.exe')
        express_path = self.get_power_express_path(version)
        autoit.run(express_path + ' ENV:' + syex_env +' testuser:' + username + '')
        autoit.win_wait(title='Power Express')
        BuiltIn().set_test_variable('${username}', username)
        BuiltIn().set_suite_variable('${syex_env}', syex_env)

    def get_power_express_path(self, version):
        express_path = "C:\\Program Files (x86)\\Carlson Wagonlit Travel\\Power Express " + version + "\\PowerExpress.exe"
        if os.path.exists(express_path):
            return express_path
        else:
            BuiltIn().fail('Path not found. Change your Express installation to default location')

    def get_log_path(self, test_environment, version):
        local_log_path = "C:\\Users\\"+ self.get_local_username() +"\\AppData\\Local\\Carlson Wagonlit Travel\\Power Express\\"+ version +"\\"
        citrix_log_path = "D:\\Syex_Logs\\"

        if test_environment == 'citrix':
            return citrix_log_path
        else:
            return local_log_path

    def get_local_username(self):
        return getpass.getuser()

    def select_profile(self, user_profile):
        autoit.win_wait('[REGEXPTITLE:rofil]')
        autoit.win_activate('[REGEXPTITLE:rofil]')
        select_profile_app = Application().Connect(path='PowerExpress.exe')
        select_profile_window = select_profile_app.window_(title_re=u'.*rofil')
        # select_profile_window = select_profile_app.top_window_()
        select_profile_window_list_box = select_profile_window.ListBox
        select_profile_window_list_box.Select(user_profile)
        select_profile_ok_button = select_profile_window.OK
        select_profile_ok_button.Click()
        BuiltIn().set_suite_variable('${user_profile}', user_profile)
        time.sleep(2)
        try:
            if autoit.control_command('Power Express', '[NAME:YesBtn]', 'IsVisible'):
                autoit.control_click('Power Express', '[NAME:YesBtn]')
        except Exception:
            pass

    def select_team_name(self, team_name, window_title):
        logger.info("Selecting team '{}'".format(team_name))
        app = Application().Connect(path='PowerExpress.exe')
        # power_express_app_instance = app[u'WindowsForms10.Window.8.app.0.3309ded_r17_ad1']
        # power_express_app_instance.Wait('ready', 90, 3)
        team_selection_window = app.window(title=window_title)
        team_selection_window.Wait('ready', 60, 3)
        team_selection_window.SetFocus()
        try:
            team_list = team_selection_window.ListBox
            # team_list.Wait('ready', 30, 3)
            # team_list.SetFocus()
            # time.sleep(2) 
            team_name_index = team_list.ItemTexts().index(team_name)
            team_list.TypeKeys("{HOME}")
            time.sleep(1)
            team_list.TypeKeys("{DOWN}" * team_name_index)
            time.sleep(1) 
            team_list.TypeKeys("{SPACE}")
        except Exception:
            BuiltIn().fail("Team '{}' is not found on team list".format(team_name))
        time.sleep(2)

    def get_team_index_value(self, team, window_title):
        app = Application().Connect(path='PowerExpress.exe')
        team_selection_window = app.window(title=window_title)
        team_selection_window.Wait('ready', 60, 3)
        # team_selection_window.SetFocus()
        # team_selection_window.ListBox.SetFocus()
        team_list = team_selection_window.ListBox.ItemTexts()
        if team in team_list:
            return team_list.index(team)
        else:
            BuiltIn().fail("Team '{}' is not found on team list".format(team))

    def set_departure_date_x_months_from_now_in_gds_format(self, number_of_months, number_of_days=0):
        future_date = self._set_future_date(number_of_months, number_of_days)
        return self._set_gds_date_format(future_date)

    def set_departure_date_x_months_from_now_in_syex_format(self, number_of_months, number_of_days=0):
        future_date = self._set_future_date(number_of_months, number_of_days)
        adjusted_date = self._adjust_weekend_to_weekday(future_date)
        return self._set_syex_date_format(adjusted_date)

    def add_days_to_current_date_in_syex_format(self, day_to_add):
        future_date = self._add_days_to_current_day(day_to_add)
        adjusted_date = self._adjust_weekend_to_weekday(future_date, 'add')
        return self._set_syex_date_format(adjusted_date)

    def set_rail_trip_date_x_months_from_now(self, number_of_months, number_of_days=0):
        return str(self.generate_date_x_months_from_now(number_of_months, number_of_days, '%d %B %Y'))

    def generate_date_x_months_from_now(self, number_of_months, number_of_days=0, date_format='%d/%m/%Y'):
        """
        Description:
        Generates date given the number of months, days and date format. If date format is not
        given, will use this format "%d %B %Y"

        Usage:
        | ${generated_date} = | Generate Date X Months From Now | 2 | 1 | "%m-%d-%Y"
        | ${generated_date} = | Generate Date X Months From Now | 2 | 1 | "%d %b %Y"
        | ${generated_date} = | Generate Date X Months From Now | 2 | 1 |
        =>
        | ${generated_date} = | 08-20-2017  |
        | ${generated_date} = | 20 Aug 2017 |
        | ${generated_date} = | 20/08/2017  |

        """        
        date_formatted = self._set_future_date(number_of_months, number_of_days)
        return str(date_formatted.strftime(date_format))

    def get_current_date(self):
        date_today = '{dt.month}/{dt.day}/{dt.year}'.format(dt=datetime.datetime.now())
        return str(date_today)

    def get_gds_current_date(self, remove_leading_zero='true'):
        """ 
        Returns gds current date. If you want to remove leading zero in days, set remove
        leading zero to 'true'

        | ${gds_date} = | Get Gds Current Date | remove_leading_zero=true |
        """
        time_now = datetime.datetime.now().time()
        today_2pm = time_now.replace(hour=14, minute=31, second=0, microsecond=0)
        if time_now < today_2pm:
            gds_date = datetime.datetime.now() - datetime.timedelta(days=int(1))
        else:
            gds_date = datetime.datetime.now()

        if remove_leading_zero.lower() == 'true':
            return str('{dt.day}{dt:%b}'.format(dt=gds_date).upper())
        else:
            return self._set_gds_date_format(gds_date)

    def convert_date_to_gds_format(self, date, actual_date_format):
        """ 
        Example:
        | ${date} = | Convert Date To Gds Format | 11/5/2016  | %m/%d/%Y |
        | ${date} = | Convert Date To Gds Format | 2016/11/09 | %Y/%m/%d |
        
        =>
        | ${date} = | 05NOV |        
        """
        converted_date = datetime.datetime.strptime(date, actual_date_format)
        return self._set_gds_date_format(converted_date)

    def convert_date_to_syex_format(self, date, actual_date_format):
        """ 
        Example:
        | ${date} = | Convert Date To Syex Format | 11/5/2016  | %m/%d/%Y
        | ${date} = | Convert Date To Syex Format | 2016/11/09 | %Y/%m/%d

        """
        converted_date = datetime.datetime.strptime(date, actual_date_format)
        return self._set_syex_date_format(converted_date)
		
    def convert_date_to_timestamp_format(self, date, actual_date_format):
        """ 
        Example:
        | ${date} = | Convert Date To Timestamp Format | 11/5/2016  | %m/%d/%Y |
        | ${date} = | Convert Date To Timestamp Format | 2016/11/09 | %Y/%m/%d |
        """
        converted_date = datetime.datetime.strptime(date, actual_date_format)
        return self._set_timestamp_format(converted_date)

    def add_days_in_gds_format(self, date, day_to_add):
        """ 
        Description:

        Add days using GDS format which is %d%b or 09SEP
        Example:
        | ${adjusted_date} = | Add days In GDS Format | 09SEP  | 1 |

        =>
        ${adjusted_date} = 10SEP
        """
        converted_date = datetime.datetime.strptime(date, '%d%b')
        added_date = converted_date + datetime.timedelta(days=int(day_to_add))
        actual_date = self._adjust_weekend_to_weekday(added_date)
        return self._set_gds_date_format(actual_date)

    def add_days_in_syex_format(self, date, day_to_add):
        """ 
        Description:

        Add days using Syex format which is %m/%d/%Y or 12302017
        Example:
        | ${adjusted_date} = | Add days In Syex Format | 12302017  | 1 |

        =>
        ${adjusted_date} = 12312017
        """        
        converted_date = datetime.datetime.strptime(date, '%m/%d/%Y')
        added_date = converted_date + datetime.timedelta(days=int(day_to_add))
        actual_date = self._adjust_weekend_to_weekday(added_date, 'add')
        return self._set_syex_date_format(actual_date)

    def subtract_days_in_gds_format(self, date, day_to_subtract, adjust_weekend_to_weekday='True'):
        converted_date = datetime.datetime.strptime(date, '%d%b')
        subtracted_date = converted_date - datetime.timedelta(days=int(day_to_subtract))
        if adjust_weekend_to_weekday == 'True':
            actual_date = self._adjust_weekend_to_weekday(subtracted_date)
            return str('{dt:%d}{dt:%b}'.format(dt=actual_date).upper())
        else:
            return str('{dt:%d}{dt:%b}'.format(dt=subtracted_date).upper())

    def subtract_days_in_syex_format(self, date, day_to_subtract, adjust_weekend_to_weekday='True'):
        converted_date = datetime.datetime.strptime(date, '%m/%d/%Y')
        subtracted_date = converted_date - datetime.timedelta(days=int(day_to_subtract))
        if adjust_weekend_to_weekday == 'True':
            actual_date = self._adjust_weekend_to_weekday(subtracted_date)
            return self._set_syex_date_format(actual_date)
        else:
            return self._set_syex_date_format(subtracted_date)

    def _set_gds_date_format(self, date):
        return str('{dt:%d}{dt:%b}'.format(dt=date).upper())
		
    def _set_syex_date_format(self, date):
        return str('{dt.month}/{dt.day}/{dt.year}'.format(dt=date))
    
    def _set_timestamp_format(self, date):
        return str('{dt:%Y}-{dt:%m}-{dt:%d}'.format(dt=date))	

    def _adjust_weekend_to_weekday(self, adjusted_date, operation='subtract'):
        if str(adjusted_date.weekday()) == '5':
			if operation != 'subtract':
				return adjusted_date + datetime.timedelta(days=int(2))
			else:
				return adjusted_date - datetime.timedelta(days=int(1))
        elif str(adjusted_date.weekday()) == '6':
			if operation != 'subtract':
				return adjusted_date + datetime.timedelta(days=int(1))
			else:
				return adjusted_date - datetime.timedelta(days=int(2))
        else:
            return adjusted_date

    def _add_days_to_current_day(self, day_to_add):
        return datetime.datetime.now() + datetime.timedelta(days=int(day_to_add))

    def _set_future_date(self, number_of_months, number_of_days):
        if number_of_days > 0:
            return self._add_month_to_current_date(int(number_of_months)) + datetime.timedelta(days=int(number_of_days))
        else:
            return self._add_month_to_current_date(int(number_of_months))

    def _add_month_to_current_date(self, month_to_add):
        today = datetime.date.today()
        month = today.month - 1 + month_to_add
        year = int(today.year + month / 12)
        month = month % 12 + 1
        day = min(today.day, calendar.monthrange(year, month)[1])
        future_date = datetime.date(year, month, day)
        return future_date

    def are_there_duplicate_remarks(self, pnr_details, gds):
        # TODO
        # implement check for other gds
        """ 
        Notes:
        Amadeus - Remarks that starts with 'RM' will be checked

        """
        remarks_list = []
        pnr_log = Counter(pnr_log.strip().lower() for pnr_log in pnr_details.split('\n') if pnr_log.strip())
        for line in pnr_log:
            if pnr_log[line] > 1:
                if gds.lower() == 'amadeus' and line != 'rir *' and line.startswith("rm"):
                    print 'duplicate remarks found: ' + line
                    remarks_list.append(line)
        return True if len(remarks_list) > 0 else False

    def sort_pnr_details(self, pnr_details):
        """ 
        Description:
        Sorts PNR Details and removes duplicate line

        Example:
        | ${sorted_pnr_details} = | Sort Pnr Details | ${pnr_details}
        """
        remark_list = [line for line in pnr_details.splitlines()]
        for index, remark in enumerate(remark_list):
            if re.match(r'\s{1,4}\d', remark):
                remark_list[index] = remark.lstrip()
        seen = set()
        seen_add = seen.add
        sorted_pnr_details = [remark for remark in remark_list \
                            if not (remark in seen or seen_add(remark)) \
                            or re.match(r'[ \t\t]', remark)]
        return "\n".join(sorted_pnr_details)

    def select_value_from_dropdown_list(self, control_id, value_to_select, window_title='Power Express', by_index=False):
        """ 
        Selects dropdown value using text or index.  If using index, use by_index=True
        
        Example:
        | Select Value From Dropdown List | [NAME:ccboClass_1] | Class Code Sample |
        """
        logger.info("Selecting dropdown value '{}'".format(value_to_select))
        autoit.win_activate(window_title)
        try:
            autoit.control_click(window_title, control_id)
        except AutoItError:
            BuiltIn().fail("Control '{}' not found".format(control_id))
        autoit.send('{PAGEUP}')
        autoit.send('{BACKSPACE}')
        autoit.send('{HOME}')
        if by_index == "True":
            autoit.control_focus(window_title, control_id)
            if value_to_select == "0":
                autoit.send('{ENTER}')
                autoit.send('{TAB}')
            else:
                autoit.send("{DOWN}" * int(value_to_select))
                autoit.send('{ENTER}')
                autoit.send('{TAB}')              
        else:
            while 1:
                item_combo_value = autoit.control_get_text(window_title, control_id)
                if item_combo_value == value_to_select:
                    autoit.control_focus(window_title, control_id)
                    autoit.send('{ENTER}')
                    autoit.send('{TAB}')
                    break
                else:
                    autoit.control_focus(window_title, control_id)
                    autoit.send('{DOWN}')
                if autoit.control_get_text(window_title, control_id) == item_combo_value:
                    BuiltIn().fail("Dropdown '{}' value is not found".format(value_to_select))
                    break

    def get_value_from_dropdown_list(self, control_id, window_title='Power Express'):
        """ 
        Returns a list containing all values of the specified dropdown.
        The default dropdown value is retained.
        """
        dropdown_list = []
        autoit.win_activate(window_title)
        autoit.control_focus(window_title, control_id)
        original_value = autoit.control_get_text(window_title, control_id)
        # autoit.send('{PAGEUP}')
        autoit.send('{BACKSPACE}')
        autoit.send('{HOME}')
        while 1:
            item_combo_value = autoit.control_get_text(window_title, control_id)
            dropdown_list.append(item_combo_value)
            autoit.send('{DOWN}')
            if autoit.control_get_text(window_title, control_id) == item_combo_value:
                break
        autoit.send('{BACKSPACE}')
        autoit.send('{HOME}')
        for item in dropdown_list:
            if original_value == autoit.control_get_text(window_title, control_id):
                break
            else:
                autoit.send('{DOWN}')
        return filter(None, dropdown_list)

    def _create_power_express_app_instance(self):
        app = Application().Connect(path='PowerExpress.exe')
        power_express_app_instance = app[u'WindowsForms10.Window.8.app.0.3309ded_r17_ad1']
        power_express_app_instance.Wait('ready')
        return power_express_app_instance

    def select_tab_control(self, tab_control_value):
        """ 
        Description:
        Select Tab using given EXACT value
        Example:
        | Select Tab Control | Fare 1 |
        """
        logger.info("Selecting '{}' tab".format(tab_control_value))
        tab_control = self._create_power_express_app_instance().TabControl
        try:
            tab_control.Select(tab_control_value)
        except Exception:
            BuiltIn().fail("Tab '{}' is not visible".format(tab_control_value))

    def select_tab_item(self, tab_item):
        """
        Selects tab item. Use this if select tab control is not working

        Example:
        | Select Tab Item | EMD |
        """
        logger.info("Selecting '{}' tab".format(tab_item))        
        app = self._create_power_express_backend_app()
        try:
            app.child_window(title=tab_item, control_type="TabItem").select()            
        except Exception:
            BuiltIn().fail("Tab '{}' is not visible".format(tab_item))

    def select_value_from_combobox(self, combobox_field, combobox_value):
        """ 
        Description:
        Selects value from dropdown using dropdown name or control id as argument
        Usage:
        | Select Value From Comnbobox | Bundled Fee | Apply Bundled Fee |
        """
        if bool(re.search(r"(\[.*:)|(\])", combobox_field)):
            self.select_dropdown_value(combobox_field, combobox_value)
        else:
            self._select_combobox_using_combobox_name(combobox_field, combobox_value)

    def _select_combobox_using_combobox_name(self, combobox_name, combobox_value):
        app = Application().Connect(path='PowerExpress.exe')
        appwindow = app[u'WindowsForms10.Window.8.app.0.bce5ad_r17_ad1']
        try:
            logger.info("Selecting '{}' from '{}' combobox".format(combobox_value, combobox_name))            
            appwindow[u''.join(combobox_name)+'ComboBox'].Select(u''.join(combobox_value))
        except (ValueError):
            BuiltIn().fail("Combobox value '{}' is not found".format(combobox_value))

    def select_tst_fare(self, fare_number):
        """ 
        Description:
        For Rail Panel
        Select Tab using given EXACT value
        """        
        listbox = self._create_power_express_app_instance().ListBox
        listbox.Select(u'  %s' % fare_number)

    def select_value_from_listbox(self, listbox_value):
        listbox = self._create_power_express_app_instance().ListBox
        listbox.Select(u''.join(listbox_value))

    def get_value_from_combobox(self, combobox_name):
        """ 
        Description:
        Gets all dropdown values/items using dropdown name as argument

        Usage:
        | Get Value From Combobox | Bundled Fee |
        
        =>
        [u'Apply Bundled Fee', u'No Bundled Fee']
        """        
        app = Application().Connect(path='PowerExpress.exe')
        appwindow = app[u'WindowsForms10.Window.8.app.0.bce5ad_r17_ad1']
        return appwindow[u''.join(combobox_name)+'ComboBox'].ItemTexts()

    def _is_control_enabled(self, control):
        return True if control.IsEnabled() else False

    def is_tab_visible(self, tab_value):
        tab_control_texts = self._create_power_express_app_instance().TabControl.Texts()
        return True if tab_value in tab_control_texts else False

    def get_currency(self, country_code):
        return getattr(CurrencyConstant, country_code.lower())

    def get_percentage_value(self, number):
        percentage = (float(number) / float(100))
        return percentage

    def convert_to_float(self, value, precision=2):
        """ 
        Converts value to float. By default precision used is 2.

        Example:
        | ${convered_value} = | Convert To Float | 15.0909 | precision=5 |

        """
        try:
            return "{:.{prec}f}".format(float(value), prec=precision)
        except Exception as error:
            raise ValueError(repr(error))

    def get_visible_tab(self):
        """ 
        Returns tabs in list data type

        """
        tab_control = self._create_power_express_app_instance().TabControl
        tab_list = []
        tab = tab_control.WrapperObject()
        for tab_item in range(0, tab.TabCount()):
            tab_list.append(tab.GetTabText(tab_item).strip())
        return tab_list

    def get_string_matching_regexp(self, reg_exp, data):
        """ 
        Get string matching Reg Expression.

        Example:
        | ${string} = | Get String Matching Regexp | TAX [0-9]+\.[0-9][0-9] | NZD120.00 TAX12.00 |
        
        Output:
        ${string} = TAX12.00
        
        """
        try:
            m = re.search(reg_exp, data)
            return m.group(0)
        except Exception:
            return 0

    def get_string_using_marker(self, whole_string, first_marker, end_marker=None):
        """ 
        Description:
        Returns substring or in between string of first marker and end marker.
        Leading and trailing spaces will be stripped.

        Usage:
        | ${summary_texts} = | Get String Using Marker | HP*BIRTHDATE-20JUN84 98| - | ${SPACE} |

        =>
        ${summary_texts} = 20JUN84
        """
        BuiltIn().log("Getting string from {} between {} and {}".format(whole_string, first_marker, end_marker))
        start = str(whole_string).find(first_marker) + len(first_marker)
        end = whole_string.find(end_marker, start)
        if end == -1:
            end = len(whole_string)
            return whole_string[start:end].strip()
        else:
            return whole_string[start:end].strip()      

    def get_minimum_value_from_list(self, list_):
        """ 
        Description:
        Returns the least / minimum value of list item

        Usage:
        | @{fare_list}          = | Create List                 | 12.3 | 21.2 | 35.3 | 10.8 |
        | ${minimum_fare_value} = | Get Minimum Value From List | ${fare_list}              | 

        Result:
        | ${minimum_fare_value} = | 10.8 |

        """
        try:
            return min(float(value) for value in list_)
        except (ValueError):
            BuiltIn().fail("List does not contain any value")

    def get_required_flight_details(self, raw_flight_details, city_pair_marker):
        raw_flight_details = raw_flight_details.strip()
        flight_details_line = raw_flight_details.find(city_pair_marker)
        fare_line_length = flight_details_line + len(city_pair_marker)
        raw_flight_details = raw_flight_details[:fare_line_length]
        flight_details_list = raw_flight_details.split(" ")
        flight_details_list = [x for x in flight_details_list if x]
        del flight_details_list[0]
        return flight_details_list

    def round_up_hk(self, number):
        """
        Description:
        Returns round up value in integer if decimal is found otherwise no roundup 
        """
        number_decimal = str(number-int(number))[2:]
        if float(number_decimal) == 0:
            return int(number)
        else:
            return int(number) + 1

    def round_off(self, number, precision=2):
        """
        Description:
        Returns round off to 2 decimal places. By default the precision is two (2)

        Usage:
        | ${number} | Round Off | 12.8998 |

        Output:
        ${number} = 12.90
        """
        try:
            number_decimal = round(float(number), int(precision))
            return str(number_decimal)
        except (ValueError):
            BuiltIn().fail("'{}' is an invalid input.".format(number))
            
            
    def click_button_in_air_fare(self, fare_tab, button_action):
        """ 
        Description:
        Currently supports Add Manual, Add Alternate, and Remove Fare
        Needs to provide current active fare tab where the Manual, Alternate and Remove button is located

        Usage:
        | Click Button In Air Fare | Alternate Fare 1 | Remove Fare |

        """    
        autoit.win_activate("Power Express")
        app_instance = self._create_power_express_app_instance()
        if "alternate" not in fare_tab.lower():
            if "manual" in button_action.lower():
                button = app_instance.Button6
            elif "alternate" in button_action.lower():
                button = app_instance.Button5
            elif "remove" in button_action.lower():
                button = app_instance.Button7
        elif "alternate" in fare_tab.lower():
            if "manual" in button_action.lower():
                button = app_instance.Button4
            elif "alternate" in button_action.lower():
                button = app_instance.Button3
            elif "remove" in button_action.lower():
                button = app_instance.Button5
        else:
            BuiltIn().fail("Button does not exist")
        button.Click()

    def get_tst_list(self):
        """ 
        Description:
        Get all TST item and save it to list type

        Usage:
        | @{tst_list} = | get_tst_list |

        Result:
        | @{list} =     | 1 | 2 |
        """    
        tst_listbox = self._create_power_express_app_instance().ListBox
        tst_list =  tst_listbox.ItemTexts()
        tst_list = [item.strip() for item in tst_list]
        return tst_list

    def remove_duplicate_from_list(self, list_):
        """ 
        Description:
        Remove all duplicate item from list

        Usage:
        | @{sample_list} = | Create List                | 1  | 2 | 3 | 1 |
        | @{sample_list} = | Remove Duplicate From List | ${sample_list} | 

        Result:
        | @{sample_list} = | [ 1, 2, 3 ] |
        """   
        seen = set()
        seen_add = seen.add
        return [value for value in list_ if not (value in seen or seen_add(value))]

    def get_checkbox_state(self, control_id, window="Power Express"):
        """ 
        Description:
        Return Checkbox Status. True if checked and False if unchecked

        Usage:
        | ${is_checked} = | Get Checkbox State | [NAME:cchkMySubUnit] | Power Express |

        Result:
        | ${is_checked} = | True |
        """   
        app = Application(backend='uia').connect(path='PowerExpress.exe')
        dlg = app.window(title_re=window)
        control_id = re.sub(r"(\[.*:)|(\])", "", control_id)
        toggle_state = app.dlg.window(auto_id=control_id).get_toggle_state()
        logger.info("Checkbox status is '{}'".format(toggle_state))
        return True if toggle_state == 1 else False

    def click_menu_item(self, menu_title, window="Power Express"):
        """ 
        Description:
        Selects Menu item such as "Change Team", "Manual Contact", etc.
        
        Usage:
        | Click Menu Item | Change Team |

        """
        app_dlg = self._create_power_express_backend_app()
        app_dlg.child_window(title=menu_title, control_type="Button").click_input()

    def select_panel(self, panel_name):
        """ 
        Selects Panel item
        
        Example:
        | Select Panel | Cust Refs |
        """
        logger.info("Selecting panel : {}".format(panel_name))
        app_dlg = self._create_power_express_backend_app()
        try:
            panel = app_dlg.child_window(title=panel_name, control_type="TabItem")
            panel.select()
        except ElementNotFoundError:
            BuiltIn().fail("'{}' panel is not found".format(panel_name))

    def get_all_panels(self):
        """ 
        Returns all active / current panels

        Example:
        | @{current_panels} = | Get All Panels |

        =>
        @{current_panels} =  [ Client Info | Client Fees ]
        """
        app_dlg = self._create_power_express_backend_app()
        return app_dlg.TabControl.children_texts()

    def _create_power_express_backend_app(self):
        app = Application(backend='uia')
        appconnect = app.connect(path='PowerExpress.exe')
        appwindow = appconnect.window(auto_id="frmMain", control_type="Window")
        return appwindow

    def get_lines_using_regexp(self, string, regex_pattern):
        """ 
        Description:
        Returns lines matching regex or pattern

        Usage:
        | Get Lines Using Regexp | ${pnr_details} | (QU|QA)/QE/PARWL24CA/70C4 |
        """
        regex_pattern = re.compile(regex_pattern)
        logger.info("Searching pattern: '{}'".format(regex_pattern.pattern))
        line_match = [line.strip() for line in string.splitlines() if re.search(regex_pattern, line)]
        return '\n'.join(line_match)

    def flatten_string(self, string_to_flatten):
        """ 
        Description:
        Converts multiple lines into one line 

        Usage:
        | ${sample} | Flatten String | ${string_to_flatten} |
        
        """
        string_to_flatten = re.sub(r"([\n ])\1*", r"\1", string_to_flatten)
        flattened_string = [line.rstrip() for line in string_to_flatten.splitlines()]
        return "".join(flattened_string)

    def verify_list_values_are_identical(self, list_):
        """ 
        Description:
        Returns Boolean value if list contains similar value

        Usage:
        | ${is_similar_value} | Verify List Values Are Identical  | ${list_sample} |
        
        """
        if list_: 
            return len(set(list_)) <= 1
        else:
            BuiltIn().fail("List does not contain any value")

    def get_summary_texts(self):
        """ 
        Description:
        Returns summary text in list data type

        Usage:
        | ${summary_texts} = | Get Summary Texts  |
        
        """        
        appwindow = self._create_power_express_backend_app()        
        summary_field = appwindow.child_window(auto_id="lvwSummary", control_type="List")
        summary_texts = [item for sublist in summary_field.texts() for item in sublist]
        return summary_texts

    def generate_random_date(self, year, date_format, strip_leading_zero_in_day=False):
        """ 
        Description:
        Generate random date using gien start, end and date format

        Usage:
        | ${new_date} = | Generate Random Date | 1980 | %m/%d/%Y |
        
        =>
        ${new_date} = 12/24/1980
        """              
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = datetime.date(int(year),month,int(day))
        generated_date = str(date.strftime(date_format).upper())
        return generated_date if strip_leading_zero_in_day == False else generated_date.lstrip('0')

    def tick_checkbox_via_text(self, checkbox_description, ctrl_index=0):
        """ 
        Description:
        Tick checkbox using checkbox description
        Change ctrl_index value if checkbox is visible in other panels

        Usage:
        | Tick Checkbox Via Text | Awaiting Approval | ctrl_index=1 |
        | Tick Checkbox Via Text | Auto Invoice      |   
        """
        appwindow = self._create_power_express_backend_app()
        checkbox = appwindow.child_window(title=u''.join(checkbox_description), control_type="CheckBox", ctrl_index=0)
        try:
            checkbox_state = checkbox.get_toggle_state()
        except (IndexError):
            BuiltIn().fail("Checkbox description '{}' is not found".format(checkbox_description))             
        if checkbox_state == 0:
            checkbox.click_input()
        else:
            logger.info("Checkbox '{}' already ticked".format(checkbox_description))
			
    def untick_checkbox_via_text(self, checkbox_description, ctrl_index=0):
        """ 
        Description:
        Untick checkbox using checkbox description
        Change ctrl_index value if checkbox is visible in other panels

        Usage:
        | Untick Checkbox Via Text | Awaiting Approval | ctrl_index=1 |
        | Untick Checkbox Via Text | Auto Invoice      |   
        """
        appwindow = self._create_power_express_backend_app()
        checkbox = appwindow.child_window(title=u''.join(checkbox_description), control_type="CheckBox", ctrl_index=0)
        try:
            checkbox_state = checkbox.get_toggle_state()
        except (IndexError):
            BuiltIn().fail("Checkbox description '{}' is not found".format(checkbox_description))             
        if checkbox_state == 1:
            checkbox.click_input()
        else:
            logger.info("Checkbox '{}' already unticked".format(checkbox_description))

    def get_document_items(self):
        """ 
        Description:
        Retrieve all information from Unused Document tab

        Usage:
        | ${actual_document_items} = | Get Document Items |
        """    
        treeview_dlg = self._create_power_express_app_instance().TreeView
        return treeview_dlg.print_items().strip()

    def click_document_item(self, document_item, double_click=False):
        """ 
        Description:
        Clicks item from Unused Document

        Usage:
        | Click Document Item | PA S 56TGHY  079 1212121212                  USD3434     20180606  FULL | double_click=False |
        """
        treeview_dlg = self._create_power_express_app_instance().TreeView
        try:
            tree_item = treeview_dlg.GetItem([u''.join(document_item)])
            logger.info("selecting '{}'".format(document_item))
            if double_click == "True":
                tree_item.ClickInput(double=True)
            else:
                tree_item.ClickInput()
        except (IndexError):
            BuiltIn().fail("Document item '{}' is not found and cannot be selected".format(document_item))

    def get_service_option_items(self):
        """ 
        Description:
        Gets all values of service option delimited by Tab and every item is splitted into lines

        Usage:
        | ${service_option_values}= | Get Service Option Items |

        =>
        High Fare Calculation   WPNC‡XR¦1S  High Fare
        Low Fare International Calculation  WPNIN/T2¦1S Low Fare
        """
        list_view = self._create_power_express_app_instance().ListView
        list_items = list_view.texts()
        so_list = list_items[1:]
        so_items = [u'\t'.join(so_list[index: index+3])\
                    for index, item in enumerate(so_list) if index % 3 == 0]
        return '\n'.join(so_items)

    def _connect_to_travelport(self):
        app = Desktop(backend='uia')
        # appwindow = app.window(title_re='Galileo Desktop -', class_name='FrameWndClass', found_index=0)
        appwindow = app.window(title_re='Galileo Desktop -', found_index=0)
        travelport_window = appwindow.window(title='Window 1', found_index=0)
        travelport_window.wait('ready', 60, 3)
        travelport_window.set_focus()
        return travelport_window

    def activate_travelport_smart_window(self):
        pnrviewercontrol = self._connect_to_travelport()\
                        .window(auto_id="PnrViewerControl", control_type="Custom")
        pnrviewercontrol.wait('ready', 60, 1)
        pnrviewercontrol.set_focus()
        return pnrviewercontrol

    def activate_travelport_terminal_window(self):
        terminal_window = self._connect_to_travelport()\
                        .window(class_name="RichTextBox", control_type="Document", found_index=0)
        terminal_window.wait('ready', 30, 1)
        terminal_window.set_focus()
        return terminal_window

    def click_travelport_smart_button(self, button_name):
        """ 
        Description:
        Clicks Travelport Smart button such as "*ALL", "*FOP", "*NP"
        
        Usage:
        | Click Travelport Smart Button | *FOP |
        """
        allbutton = self.activate_travelport_smart_window()\
                    .child_window(title=button_name, control_type="Button", found_index=0) 
        allbutton.set_focus()
        allbutton.click()

    def get_travelport_smart_window_details(self, command="*ALL"):
        """ 
        Description:
        Get details from clicking button from smart window such as "*ALL", "*FOP", "*NP". 
        By default, command used is *ALL
        
        Usage:
        | Get Travelport Smart Window Details | *FOP |
        | Get Travelport Smart Window Details |      |
        """
        self.click_travelport_smart_button(command)
        smart_window = self.activate_travelport_smart_window()
        data =  u''.join(smart_window.child_window\
            (auto_id="PART_PNRContainer", control_type="Document").texts())
        return data.strip()

    # def get_travelport_terminal_window_details(self):
    #     terminal_window = self.activate_travelport_terminal_window()
    #     return u''.join(terminal_window.texts()).strip()

    def copy_content_from_sabre(self):
        sabre_window = RailLibrary()._connect_to_sabre_instance()
        sabre_menu_item_select = sabre_window.MenuItem(u'&Edit->Select &All')
        sabre_menu_item_select.Select()
        # sabre_menu_item_copy = sabre_window.MenuItem(u'&Edit->&Copy\tCtrl+C')
        # sabre_menu_item_copy.Select()
        sunawtcanvas = sabre_window[u'SunAwtCanvas']
        sunawtcanvas.SetFocus()
        time.sleep(1)
        sunawtcanvas.TypeKeys("^c")
        sunawtcanvas.TypeKeys("{ESC}")
        time.sleep(1)

    def send_sabre_command(self, *command_list):
        sabre_window = RailLibrary()._connect_to_sabre_instance()
        sunawtcanvas = sabre_window[u'SunAwtCanvas6']
        sunawtcanvas.Wait('ready', 30, 1)
        kbdlocked = sabre_window.child_window(title="KbdLocked", control_type="Text")
        kbdlocked.wait_not('exists', 30, 1)
        try:
            sunawtcanvas.Wait('ready', 30, 1)
            sunawtcanvas.SetFocus()
        except pywinauto.findbestmatch.MatchError:
            BuiltIn().fail("Sabre window is not activated")
        for command in command_list:
            autoit.send("+{BACKSPACE}")
            autoit.send("+{HOME}")
            sunawtcanvas.SetFocus()
            autoit.send(command)
            time.sleep(1)
            autoit.send('{ENTER}')
            kbdlocked = sabre_window.child_window(title="KbdLocked", control_type="Text")
            kbdlocked.wait_not('exists', 30, 1)

    def get_radio_button_state(self, control_id):
        app = Application(backend='uia').connect(path='PowerExpress.exe')
        dlg = app.window(title_re='Power Express V')
        control_id = re.sub(r"(\[.*:)|(\])", "", control_id)
        radio_button_state = dlg.window(auto_id=control_id,  control_type="RadioButton").is_selected()
        if radio_button_state == 1:
            radio_button_state = "Selected"
        else:
            radio_button_state = "Not Selected"
        logger.info("Radio Button status is '{}'".format(radio_button_state))
        return True if radio_button_state == "Selected" else False

    def _convert_control_id_to_uia_format(self, control_id):
        return re.sub(r"(\[.*:)|(\])", "", control_id)

    def get_radio_button_state_using_label(self, label):
        """ 
        Description:
        Gets Radio Button Status and returns True if Selected and False if Not Selected using field label or text
        
        Usage:
        | ${radio_button_status} | Get Radio Button Status Using Label | modifiable |
        """
        app = Application(backend='uia').connect(path='PowerExpress.exe')
        dlg = app.window(title_re='Power Express V')
        label = re.sub(r"(\[.*:)|(\])", "", label)
        radio_button_state = dlg.window(title=label,  control_type="RadioButton").is_selected()
        if radio_button_state == 1:
            radio_button_state = "Selected"
        else:
            radio_button_state = "Not Selected"
        logger.info("Radio Button status is '{}'".format(radio_button_state))
        return True if radio_button_state == "Selected" else False

    def get_fare_restiction_selected_radio_button(self, translate_to_english=True):
        """ 
        Description:
        Gets the Fare Rectrion name currently selected radio button
        Add argument True if translation to English is needed otherwise will return current language

        Usage:
        | ${currently_selected_fare_restriction} | Get Fare Restiction Selected Radio Button |
        | ${currently_selected_fare_restriction} | Get Fare Restiction Selected Radio Button | True |

        """        
        app = Application(backend='uia').connect(path='PowerExpress.exe')
        dlg = app.window(title_re='Power Express')
        restriction_value = ""
        for restriction in dlg.child_window(auto_id="Panel1", control_type="Pane", found_index=0).children_texts():
            radio_button_state = dlg.window(title=restriction,  control_type="RadioButton").is_selected()
            if radio_button_state == 1:
                restriction_value += restriction
                break
        return self._translate_fare_restriction(restriction_value, translate_to_english)    

    def _translate_fare_restriction(self, restriction_value, translate_to_english):
        new_restriction_value = ""
        if translate_to_english == "True":
            if restriction_value == "Modifiable":
                new_restriction_value += "Fully Flexible"
            elif restriction_value == "Partiellement modifiable":
                new_restriction_value += "Semi Flexible"
            elif restriction_value == "Non modifiable":
                new_restriction_value += "Non Flexible"
        else:
            new_restriction_value += restriction_value
        return new_restriction_value

    def click_travelport_popup_ok_button(self):
        """
            To be updated...
        """
        control_popup = self._connect_to_travelport_popup_windows()
        try:
            control_popup.child_window(auto_id="PART_OKButton", control_type="Button").click()
        except pywinauto.findwindows.ElementNotFoundError:
            pass

    def get_control_text(self, control_id, window="Power Express"):
        app = Application(backend='uia').connect(path='PowerExpress.exe')
        dlg = app.window(title_re=window)
        control_id = re.sub(r"(\[.*:)|(\])", "", control_id)
        return app.dlg.window(auto_id=control_id).texts()

    def get_control_text_current_value(self, control_id):
        """
        Gets text value of current control. Use this for multiple control instances
        """        
        control_id_object = self._convert_control_id_to_uia_format(control_id)
        app = Application(backend='uia')
        appconnect = app.connect(path='PowerExpress.exe')
        appwindow = appconnect.window(auto_id="frmMain", control_type="Window")
        current_field = appwindow.child_window(auto_id=control_id_object)
        return current_field.iface_value.CurrentValue

    def truncate(self, value, precision=2):
        """
        Truncate the value without rounding up. By default precision used is 2.

        Example:
        ${truncated_value} = | Truncate | 15.0909 | precision=2

        Output:
        ${truncated_value} = 15.09
        """
        try:
            s = '{}'.format(value)
            if 'e' in s or 'E' in s:
                return '{0:.{1}value}'.format(value, precision)
            i, p, d = s.partition('.')
            return '.'.join([i, (d+'0'*precision)[:precision]])
        except Exception as error:
            raise ValueError(repr(error))

    def _connect_to_travelport_popup_windows(self):
        app = Desktop(backend='uia')
        appwindow = app.window(title_re='Galileo Desktop -')
        travelport_popup_app = appwindow.window(class_name='Window', control_type='Window', found_index=0)
        return travelport_popup_app
	
    def get_country_code_based_on_currency(self, currency):
        return getattr(CountryConstant, currency.lower())

    def select_gds_value(self, gds):
        logger.info("Selecting '{}' from gds toolstrip".format(gds))            
        app = Application(backend='uia').connect(path='PowerExpress.exe')
        gds_win = app.window(auto_id="frmMain", control_type="Window")
        gds_win.wait('ready', 60, 3)
        gds_win.set_focus()
        try:
            gds_win.click_input(coords=(557, 104))
            toolstrip = gds_win.child_window(control_type="Menu")
            toolstrip.wait('ready', 60, 3)
            keyboard.SendKeys("{TAB}")
            if gds == 'apollo':
                keyboard.SendKeys("p")
            elif gds == 'amadeus':
                keyboard.SendKeys("a")
            elif gds == 'galileo':
                keyboard.SendKeys("g")
            elif gds == 'sabre':
                keyboard.SendKeys("s")
        except Exception:
            pass

    def convert_list_to_lines(self, list_):
        return "\n".join(list_)

    def get_status_strip_text(self):
        """
        Gets the status strip text.

        Example:
        ${status_strip_text} = | Get Status Strip Text |

        Output:
        ${status_strip_text} = Form of Payment Update Failed
        """
        app = self._create_power_express_backend_app()
        status_strip = app.window(title="StatusStrip")
        return "".join(status_strip.children_texts()).strip()

    def select_dropdown_value(self, control_id, dropdown_value):
        """
        Selects dropdown value

        Example:
        | Select Dropdown Value | [NAME:ccboTouchLevel] |
        """
        logger.info("Selecting dropdown value '{}'".format(dropdown_value))
        control_id_object = self._convert_control_id_to_uia_format(control_id)
        autoit.win_activate('Power Express')
        app = self._create_power_express_backend_app()
        try:
            combo = app.child_window(auto_id=control_id_object, control_type="ComboBox")
            combo.Button.click_input()
        except ElementNotFoundError:
            BuiltIn().fail("Field with control id '{}' is not found".format(control_id))    
        try:
            combo.child_window(title=dropdown_value, control_type="ListItem").click_input()
        except ElementNotFoundError:
            BuiltIn().fail("Dropdown '{}' value is not found".format(dropdown_value))

    def get_dropdown_values(self, control_id):
        """
        Gets all dropdown values. Returns values in List

        Example:
        | ${sdropdown_values} = | Get Dropdown Values | [NAME:ccboTouchLevel] |
        """
        control_id_object = self._convert_control_id_to_uia_format(control_id)
        autoit.win_activate('Power Express')
        app = self._create_power_express_backend_app()
        try:
            combo = app.child_window(auto_id=control_id_object, control_type="ComboBox")
            combo.Button.click_input()
            combo_values = app.child_window(control_type="List", visible_only=False, found_index=0).texts()
            combo_values = list(itertools.chain(*combo_values))
            autoit.send("{ESC}")
            return combo_values
        except ElementNotFoundError:
            BuiltIn().fail("Field with control id '{}' is not found".format(control_id))

    def get_tooltip_text(self, xpos, ypos):
        """
        Returns tooltip text.
        Use KW "Get Control Object Coordinates" as pre-requisite

        """
        app = self._create_power_express_backend_app()
        autoit.win_activate("Power Express")
        autoit.win_wait_active("Power Express")
        autoit.auto_it_set_option("MouseCoordMode", 2)
        autoit.mouse_move(int(xpos), int(ypos))
        autoit.auto_it_set_option("MouseCoordMode", 0)
        try:
            actual_tooltip = "".join(app.child_window(control_type="ToolTip").texts())
            return actual_tooltip            
        except ElementNotFoundError:
            BuiltIn().fail("Tooltip text is not found")
