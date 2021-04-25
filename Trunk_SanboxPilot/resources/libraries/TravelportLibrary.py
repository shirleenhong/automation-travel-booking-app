# -*- coding: utf-8 -*-
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.application import Application
from pywinauto import Desktop
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import time
import os
import sys
import pywinauto
import autoit

class TravelportLibrary:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def _connect_to_travelport(self):
        autoit.win_activate("Window 1")
        app = Desktop(backend='uia')
        appwindow = app.window(title_re='Galileo Desktop -', found_index=0)
        travelport_window = appwindow.window(title='Window 1')
        travelport_window.wait('ready', 30, 1)
        travelport_window.set_focus()
        return travelport_window

    def activate_travelport_smart_window(self):
        pnrviewercontrol = self._connect_to_travelport()\
                        .window(auto_id="PnrViewerControl", control_type="Custom")
        pnrviewercontrol.wait('ready', 30, 1)
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

    def click_travelport_popup_ok_button(self):
        """
            To be updated...
        """
        control_popup = self._connect_to_travelport_popup_windows()
        try:
            control_popup.child_window(auto_id="PART_OKButton", control_type="Button").click()
        except pywinauto.findwindows.ElementNotFoundError:
            pass

    def _connect_to_travelport_popup_windows(self):
        app = Desktop(backend='uia')
        appwindow = app.window(title_re='Galileo Desktop -')
        travelport_popup_app = appwindow.window(class_name='Window', control_type='Window', found_index=0)
        return travelport_popup_app