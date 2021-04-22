import sys
import json
import requests
from datetime import datetime
import threading
import time
import socket

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from window import Ui_MainWindow

# Create the json currencies dataframe
with open('currencies.json', encoding="utf8") as f:
    curr_json = json.load(f)

# Create the json save dataframe
with open('save.json', encoding='utf8') as f:
    save_json = json.load(f)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # - - - - - - - - Variable initialisation - - - - - - - -
        self.app_run = True
        self.graph_run = False
        self.connection_lost = False
        self.api_name = ""
        self.api_key = ""
        self.api_def_key = ""
        self.time_format = "24"
        self.date_format = "dd/mm/yyyy"
        self.refresh = 60 # Seconds
        self.tested = (False, None) # (Tested ?, if so : test result)

        self.rate_list = []
        self.time_list = []

        # - - - - - - - - Widget/function connection - - - - - - - - 
        # --- Tab hub
        self.tab_hub.currentChanged.connect(self.tab_switch)
        # --- Option tab
        self.opt_combo_api.currentIndexChanged.connect(self.api_switch)
        self.opt_lineEdit_apiKey.textChanged.connect(self.check_api)
        self.opt_combo_unit.currentIndexChanged.connect(self.refresh_minimum)
        self.opt_button_save.clicked.connect(self.saveAll)
        self.opt_button_test.clicked.connect(self.test_button)
        self.opt_spinBox_time.valueChanged.connect(self.refresh_minimum)
        # --- Converter tab
        self.tab_conv_input.textChanged.connect(self.input_check)
        self.tab_conv_button_convert.clicked.connect(self.convert)
        self.tab_conv_button_swipe.clicked.connect(lambda: self.swipe(tab="conv"))
        self.tab_conv_button_clear.clicked.connect(self.clear)
        # --- Chart tab
        self.tab_chart_button_swipe.clicked.connect(lambda: self.swipe(tab="chart"))
        self.tab_chart_button_run.clicked.connect(self.run_button)
        self.tab_chart_button_stop.clicked.connect(self.graph_stop)

        # - - - - - - - - Widgets initialisation - - - - - - - - 
        self.tab_conv_button_convert.setEnabled(False)
        self.tab_chart_button_stop.setEnabled(False)
        self.tab_chart_button_save.setEnabled(False)
        self.tab_chart_button_copy.setEnabled(False)
        #self.tab_chart_frame_graph.setHidden(True)

        # - - - - - - - - ComboBoxes filling - - - - - - - - 
        # ---- API comboBox 
        # Filling from json dataframe
        api_list = []
        for api in save_json['API']:
            api_list.append(api['name'])
        self.opt_combo_api.addItems(api_list)

        # ---- Currencies Combobox 
        # All currency names in a list
        curr_list = []
        for curr in curr_json:
            curr_list.append(curr_json[curr]['name'])
        curr_list = sorted(curr_list)

        # ComboBoxes filling with currency names
        # Converter tab comboBox     
        self.tab_conv_curr1.addItems(curr_list)
        self.tab_conv_curr2.addItems(curr_list)
        # Chart tab comboBox
        self.tab_chart_curr1.addItems(curr_list)
        self.tab_chart_curr2.addItems(curr_list)

        # - - - - - - - - ComboBoxes index setting - - - - - - - -
        # Set default indexes in comboBoxes
        # Converter tab
        self.tab_conv_curr1.setCurrentIndex(39) # Euro
        self.tab_conv_curr2.setCurrentIndex(108) # US Dollar
        # Chart tab
        self.tab_chart_curr1.setCurrentIndex(39)
        self.tab_chart_curr2.setCurrentIndex(108)

        # - - - - - - - - Loading save - - - - - - - -
        self.load_save()

        # - - - - - - - Threads creation/start - - - - - - -
        # Current date/time thread
        self.thd_curr_time = threading.Thread(target=self.current_time)
        self.thd_curr_time.start()

        # Connection check thread
        self.thd_conn_check = threading.Thread(target=self.checkConnection)
        self.thd_conn_check.start()

        self.thd_graph = threading.Thread(target=self.graph_update)

    def tab_switch(self):
        """ Changes the app title according to the active tab """

        if self.tab_hub.currentIndex() == 0: # Tab option
            self.main_title.setText("Options")
        elif self.tab_hub.currentIndex() == 1: # Tab converter
            self.main_title.setText("Currency Converter")
        else: # Tab chart
            self.main_title.setText("Currency Chart")

    def time_master(self):
        """ Retruns the current week-day, date and time in 
        different formats """

        time_form = self.time_format
        date_form = self.date_format

        today = datetime.now()
        hour = today.strftime("%H:%M:%S")

        # Day
        day = today.weekday()
        if day == 0:
            day = "Monday"
        elif day == 1:
            day = "Tuesday"
        elif day == 2:
            day = "Wednesday"
        elif day == 3:
            day = "Thursday"
        elif day == 4:
            day = "Friday"
        elif day == 5:
            day = "Saturday"
        else:
            day = "Sunday"

        # Date
        if date_form == "dd/mm/yyyy":
            date = today.strftime("%d/%m/%Y")
        elif date_form == "mm/dd/yyyy":
            date = today.strftime("%m/%d/%Y")
        else: # yyyy/mm/dd
            date = today.strftime("%Y/%m/%d")

        # Time
        if time_form == "24":
            pass # Already in 24 format
        else:
            hour = today.strptime(hour, "%H:%M:%S")
            hour = hour.strftime("%I:%M:%S %p")

        return (day, date, hour)
        
    def current_time(self):
        """ Displays the current date/time while app's running """

        while self.app_run:
            now = self.time_master()
            weekday = now[0]
            date = now[1]
            hour = now[2]

            text = f"{weekday}, {date} - {hour}"
            self.main_time.setText(text)

            time.sleep(0.3)

    def load_save(self):

        # --- Retrieving the options saved in the Json dataframe
        # API
        apiName = save_json['choosen_api']
        for api in save_json['API']: # Search apiName in API list
            if api['name'] == apiName: # Match
                key = api['key']
                defaultKey = api['default']
        
        # Retrieving other options
        refresh_value = save_json['refresh_time'][0]
        refresh_unit = save_json['refresh_time'][1]
        time_format = save_json['time_format']
        date_format = save_json['date_format']

        # --- Applying the retrieved parameters
        self.api_name = apiName
        self.api_key = key
        self.api_def_key = defaultKey
        self.opt_combo_api.setCurrentText(apiName)

        self.opt_lineEdit_apiKey.setText(key)
        self.opt_spinBox_time.setValue(refresh_value)
        self.opt_combo_unit.setCurrentText(refresh_unit)

        self.time_format = time_format
        if time_format == "24":
            self.opt_radio_24.setChecked(True)
        else:
            self.opt_radio_12.setChecked(True)

        self.date_format = date_format
        if date_format == "dd/mm/yyyy":
            self.opt_radio_dmy.setChecked(True)
        elif date_format == "mm/dd/yyyy":
            self.opt_radio_mdy.setChecked(True)
        else:
            self.opt_radio_ymd.setChecked(True) 

        if refresh_unit == "Sec.":
            self.refresh = refresh_value
        else:
            self.refresh = refresh_value * 60
        
        self.refresh_reminder()

    def saveAll(self):
        """ Apply user's preferences and save them to a file """

        # --- Apply changes
        # API
        apiName = self.opt_combo_api.currentText()
        apiKey = self.opt_lineEdit_apiKey.text()
        self.api_name = apiName
        self.api_key = apiKey

        # Date format
        if self.opt_radio_dmy.isChecked():
            date_form = "dd/mm/yyyy"
            self.date_format = date_form
        if self.opt_radio_mdy.isChecked():
            date_form = "mm/dd/yyyy"
            self.date_format = date_form
        if self.opt_radio_ymd.isChecked():
            date_form = "yyyy/mm/dd"
            self.date_format = date_form
        
        # Hour format
        if self.opt_radio_24.isChecked():
            time_form = "24"
            self.time_format = time_form
        if self.opt_radio_12.isChecked():
            time_form = "12"
            self.time_format = time_form
        
        # Refresh
        refresh_value = self.opt_spinBox_time.value()
        refresh_unit = self.opt_combo_unit.currentText()
        refresh_time = [refresh_value, refresh_unit]

        if refresh_unit == "Sec.":
            self.refresh = refresh_value
        else:
            self.refresh = refresh_value * 60
        
        self.refresh_reminder()

        # --- Save preferences in file
        save_json['choosen_api'] = apiName
        for api in save_json['API']:
            if api['name'] == apiName:
                if api['key'] != apiKey:
                    api['key'] = apiKey
                else:
                    pass

        save_json['refresh_time'] = refresh_time
        save_json['time_format'] = time_form
        save_json['date_format'] = date_form

        with open('save.json', 'w') as outsave:
            json.dump(save_json, outsave)
            #json.dump(json.dumps(save_json, indent=4), outsave)
        
        # --- 

    def check_api(self):
        current_api = self.opt_combo_api.currentText()
        current_key = self.opt_lineEdit_apiKey.text()

        for api in save_json['API']:
            if api['name'] == current_api:
                saved_key = api['key']
        
        if current_key != saved_key:
            self.opt_button_save.setEnabled(False)
            text = 'Please test the new API key before saving'
            self.opt_label_api_check.setText(text)
        else:
            self.opt_button_save.setEnabled(True)
            self.opt_label_api_check.setText("")
    
    def test_button(self):
        current_api = self.opt_combo_api.currentText()
        current_key = self.opt_lineEdit_apiKey.text()

        for api in save_json['API']:
            if api['name'] == current_api:
                saved_key = api['key']

        test = self.convert_API('EUR', 'USD', test=(True, current_api, current_key))
        
        if test:
            self.opt_label_api_check.setText("API OK")
            self.opt_button_save.setEnabled(True)
        else:
            self.opt_label_api_check.setText("Wrong API")

            text = f"The inserted API key seems wrong.\nRestore the previous one ?\n({saved_key})"
            reply = QMessageBox.question(self, 'Wrong API', text,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.opt_lineEdit_apiKey.setText(saved_key)
                self.opt_button_save.setEnabled(True)
            else:
                pass

        self.tested = (True, test)

        return test

    def api_switch(self):
        current = self.opt_combo_api.currentText()
        for api in save_json['API']:
            if api['name'] == current:
                self.opt_lineEdit_apiKey.setText(api['key'])
        self.refresh_minimum()

    def refresh_minimum(self):
        """ When user changes the time refresh unit to second, the 
        the spinBox minimum value is 30 """

        if self.opt_combo_api.currentText() == 'free.currconv':
            if self.opt_combo_unit.currentText() == 'Min.': # Unit = Minute
                self.opt_spinBox_time.setMinimum(1)
            else : # Unit = Second
                self.opt_spinBox_time.setMinimum(30)
        
        if self.opt_combo_api.currentText() == 'finnhub.io':
            if self.opt_combo_unit.currentText() == 'Min': # Unit = Minute
                self.opt_spinBox_time.setMinimum(1)
            else : # Unit = Second
                self.opt_spinBox_time.setMinimum(2)

    def input_check(self):
        """ Checks the value entered by the user at each key pressed, 
        if it's not valid, the "Convert" button is disabled """

        user_input = self.tab_conv_input.text()

        try: # A number
            user_input = float(user_input)
            self.tab_conv_button_convert.setEnabled(True)
            self.main_status.setText("")

        except ValueError: # Not a number
            self.tab_conv_button_convert.setEnabled(False)
            errText = "Please enter a valid value"
            self.main_status.setText(errText)
    
    def swipe(self, tab="conv"):
        """ Invert the 2 comboBox current indexes """

        if tab == "conv":
            idx1 = self.tab_conv_curr1.currentIndex()
            idx2 = self.tab_conv_curr2.currentIndex()
            self.tab_conv_curr1.setCurrentIndex(idx2)
            self.tab_conv_curr2.setCurrentIndex(idx1)
        else:
            idx1 = self.tab_chart_curr1.currentIndex()
            idx2 = self.tab_chart_curr2.currentIndex()
            self.tab_chart_curr1.setCurrentIndex(idx2)
            self.tab_chart_curr2.setCurrentIndex(idx1)
    
    def convert(self):
        """ Convert the 2 currencies choosen in the converter tab
        1 - Get the user input
        2 - Get the code of the 2 currencies choosen by the user
        3 - Get the currency rate from the choosen API 
        4 - Convertion calculation
        5 - Display
        """
        #print(self.tab_conv_curr1.currentIndex(), self.tab_conv_curr2.currentIndex())
        # 1
        user_value = float(self.tab_conv_input.text())

        # 2
        # Search currency abreviation by currency name for curr1
        for key, value in curr_json.items():
            if value["name"] == self.tab_conv_curr1.currentText():
                curr_1 = key
        # Search currency abreviation by currency name for curr2
        for key, value in curr_json.items():
            if value["name"] == self.tab_conv_curr2.currentText():
                curr_2 = key

        # 3
        # Get rate from free.currconv API
        """ url = (f"https://free.currconv.com/api/v7/convert?q={curr_1}_{curr_2}&compact=ultra&apiKey={self.api_key}")
        response = requests.get(url)
        data = json.loads(response.text)
        rate = float(list(data.values())[0]) # Get rate """

        #rate = self.freeconv_API(curr_1, curr_2)

        rate = self.convert_API(curr_1, curr_2)

        if rate == None:
            text = "API does not respond"
            self.main_status.setText(text)
            return None

        if rate == False:
            text = "Invalid API"
            self.main_status.setText(text)
            return None

        # 4
        # Calculation and display
        dec_digits = curr_json[curr_2]["decimal_digits"]
        res = round(user_value * rate, dec_digits)
        #res = user_value * rate

        # 5
        self.tab_conv_output.setText(str(res)) # Result display

        # Info display
        curr1_name = self.tab_conv_curr1.currentText()
        curr1_native = curr_json[curr_1]["symbol_native"]
        curr2_name = self.tab_conv_curr2.currentText()
        curr2_native = curr_json[curr_2]["symbol_native"]

        day, date, hour = self.time_master()
        text_rate = f"1 {curr1_name} ({curr1_native}) = {round(rate, dec_digits)} {curr2_name} ({curr2_native})"
        text_up = f"Last update : {day}, {date} at {hour}"
        self.tab_conv_label_info.setText(text_rate+"\n"+text_up)

    def clear(self):
        """ Clear the input/output section and the info text 
        in converter tab """

        self.tab_conv_input.clear()
        self.tab_conv_output.clear()
        self.tab_conv_label_info.setText("")
        self.tab_conv_button_convert.setEnabled(False)
    
    def convert_API(self, curr1, curr2, test=(False, "", "")):
        """ test=(True/False, api_name, api_key) """

        if test[0] == False: # Test mode OFF
            api = self.api_name
            key = self.api_key
        else: # Test mode ON
            api = test[1]
            key = test[2]

        if api == "free.currconv":
            try:
                url = (f"https://free.currconv.com/api/v7/convert?q={curr1}_{curr2}&compact=ultra&apiKey={key}")
                response = requests.get(url)
            except requests.exceptions.ConnectionError: # Not resp.
                return None

            data = json.loads(response.text)
            #print(data)

            if len(list(data.values())) != 1: # Wrong API key
                #print(url)
                return False

            rate = float(list(data.values())[0])

            if test[0] == False:
                #print(url)
                return rate

            else: # Test mode ON
                if len(list(data.values())) != 1:
                    return False
                else:
                    return True
            
        if api == "fixer.io":
            try:
                url = f"http://data.fixer.io/api/latest?access_key={key}&base={curr1}&symbols={curr2}"
                response = requests.get(url)
            except requests.exceptions.ConnectionError: # Wrong URL
                return None
            
            data = json.loads(response.text)
            #print(data)

            if data['success'] == False: # Wrong API key
                #print(url)
                return False

            iterator = iter(data['rates'].values())
            rate = next(iterator)

            if test[0] == False:
                print(url)
                return rate

            else: # Test mode ON
                if data['success'] == False:
                    return False
                else:
                    return True
            
            print(url)
        
        if api == "finnhub.io":
            try:
                url = f'https://finnhub.io/api/v1/forex/rates?base={curr1}&token={key}'
                response = requests.get(url)
            except requests.exceptions.ConnectionError: # Wrong URL
                return None
            
            data = json.loads(response.text)
            #print(data)

            check = iter(data.keys())
            check = next(check)
            if check == 'error':
                return False
            
            rate = data['quote'][curr2]

            if test[0] == False:
                #print(url)
                return rate

            else: # Test mode ON
                check = iter(data.keys())
                check = next(check)
                if check == 'error':
                    return False
                else:
                    return True
    
    def run_button(self):
        self.graph_run = True

        self.thd_graph = threading.Thread(target=self.graph_update)
        self.thd_graph.start()

    def graph_update(self):
        self.tab_chart_button_stop.setEnabled(True)

        for key, value in curr_json.items():
            if value['name'] == self.tab_chart_curr1.currentText():
                curr_1 = key
        
        for key, value in curr_json.items():
            if value['name'] == self.tab_chart_curr2.currentText():
                curr_2 = key
        
        self.tab_chart_button_run.setEnabled(False)

        while self.graph_run:
            rate = self.convert_API(curr_1, curr_2)
            self.time_list.append(self.time_master()[2])
            self.rate_list.append(rate)

            print(self.time_list)
            print(self.rate_list)

            t = self.refresh
            while t > 0 and self.graph_run:
                print(t)
                time.sleep(1)
                t-=1
    
    def graph_stop(self):
        if self.tab_chart_button_stop.text() == "STOP":
            self.graph_run = False
            self.tab_chart_button_stop.setText("CLEAR")
            self.tab_chart_button_run.setEnabled(True)

        if self.tab_chart_button_stop.text() == "CLEAR":
            self.rate_list = []
            self.time_list = []
            self.graph.clear()
            self.tab_chart_button_stop.setText("STOP")
            self.tab_chart_button_stop.setEnabled(False)

    def checkConnection(self, host ="8.8.8.8", port=53, timeout=3):
        """ Regularly check the connection status.
		To do this, a regular connection is established 
		with the Google DNS (8.8.8.8) """

        backOnline = False

        while self.app_run:
            try:
                socket.setdefaulttimeout(timeout)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))

                if backOnline:
                    self.connection_lost = False
                    self.main_status.setText("Back online")
                    self.opt_button_test.setEnabled(True)
                    self.tab_conv_button_convert.setEnabled(True)
                    self.tab_chart_button_run.setEnabled(True)

                    backOnline = False
                
            except socket.error as ex: # Connection lost
                """ A connection lost has the effect of deactivating 
                certain buttons in order to prevent the user from 
                launching processes requiring an internet connection. """

                print(ex)
                self.connection_lost = True
                self.main_status.setText("NO CONNECTION")

                self.opt_button_test.setEnabled(False)
                self.tab_conv_button_convert.setEnabled(False)
                self.tab_chart_button_run.setEnabled(False)

                backOnline = True
            
            t= 9
            while t > 0 and self.app_run:
                time.sleep(1)
                t -= 1

    def refresh_reminder(self):
        value = self.opt_spinBox_time.value()

        if self.opt_combo_unit.currentText() == "Sec.":
            text = f"Chart will update every {value} seconds"
        else:
            text = f"Chart will update every {value} minutes"
        
        self.opt_label_refresh_remind.setText(text)

    def closeEvent(self, event):
        event.accept()
        self.app_run = False
        self.graph_run = False
        if self.thd_graph.is_alive():
            self.graph_run = False
            self.thd_graph.join()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())