import sys
import json
import requests
from datetime import datetime
import threading
import time
import socket
from statistics import mean

import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
from pyqtgraph import exporters
import pyperclip

from window import Ui_MainWindow

__version__ = '1.0'
__author__ = 'Kartmaan'

# - - - - - - - - Dataframes creation - - - - - - - -
# Create the json currencies dataframe
# Contains all currency names along with their code and 
# other additional information
with open('currencies.json', encoding="utf8") as f:
    curr_json = json.load(f)

# Create the json save dataframe
# Contains user preferences :
# - API names and their key
# - The last choosen API
# - Theme choice
# - Grid choice
# - The time and date format
with open('save.json', encoding='utf8') as f:
    save_json = json.load(f)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # - - - - - - - - Variable initialisation - - - - - - - -
        self.connection_lost = False
        self.backOnline = False
        self.api_name = ""
        self.api_key = ""
        self.api_def_key = ""
        self.time_format = "24"
        self.date_format = "dd/mm/yyyy"
        self.grid = True
        self.theme = "Light"
        self.range = 7
        self.pen = self.red_pen

        self.currs_graph = ("","")
        self.rate_list = []
        self.time_list = []

        # - - - - - - - - Widget/function connection - - - - - - - - 
        # --- Tab hub
        self.tab_hub.currentChanged.connect(self.tab_switch)

        # --- Option tab
        self.opt_combo_api.currentIndexChanged.connect(self.api_switch)
        self.opt_lineEdit_apiKey.textChanged.connect(self.check_api_key_change)
        self.opt_button_save.clicked.connect(self.saveAll)
        self.opt_button_test.clicked.connect(self.test_button)

        # --- Converter tab
        self.tab_conv_input.textChanged.connect(self.input_check)
        self.tab_conv_button_convert.clicked.connect(self.convert)
        self.tab_conv_button_swipe.clicked.connect(lambda: self.swipe(tab="conv"))
        self.tab_conv_button_clear.clicked.connect(self.clear)
        self.tab_conv_button_copy.clicked.connect(self.copy_conv)

        # --- Chart tab
        self.tab_chart_button_swipe.clicked.connect(lambda: self.swipe(tab="chart"))
        self.tab_chart_button_view.clicked.connect(self.get_historical)
        self.tab_chart_button_copy.clicked.connect(self.copy_graph)
        self.tab_chart_button_save.clicked.connect(self.save_graph)

        # - - - - - - - - Widgets initialisation - - - - - - - - 
        self.tab_conv_button_convert.setEnabled(False)
        self.tab_chart_button_save.setEnabled(False)
        self.tab_chart_button_copy.setEnabled(False)

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
        self.timer_currTime = QtCore.QTimer()
        self.timer_currTime.setInterval(300)
        self.timer_currTime.timeout.connect(self.current_time)
        self.timer_currTime.start()

        # Connection check thread
        self.timer_connCheck = QtCore.QTimer()
        self.timer_connCheck.setInterval(6000)
        self.timer_connCheck.timeout.connect(self.checkConnection)
        self.timer_connCheck.start()

    def tab_switch(self):
        """ Changes the app title according to the active tab """

        if self.tab_hub.currentIndex() == 0: # Tab option
            self.main_title.setText("Options")
        elif self.tab_hub.currentIndex() == 1: # Tab converter
            self.main_title.setText("Currency Converter")
        else: # Tab chart
            self.main_title.setText("Historical graph")
        
        self.opt_label_save_remind.setText('')
        self.main_status.setText('')

    def time_master(self):
        """ Retruns the current week-day, date and time in 
        different formats according to 'self.time_format' and
        'self.date_format' """

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
        """ Displays the current date/time while app's running.
        Runs from thread : self.thd_curr_time """

        now = self.time_master()
        weekday = now[0]
        date = now[1]
        hour = now[2]

        text = f"{weekday}, {date} - {hour}"
        self.main_time.setText(text)

        #time.sleep(0.3)

    def load_save(self):
        """ Load save.json backup and apply preferences.
        Starts each time the program is started """

        # --- Retrieving the options saved in the Json dataframe
        # API
        apiName = save_json['choosen_api']
        for api in save_json['API']: # Search apiName in API list
            if api['name'] == apiName: # Match
                key = api['key']
                defaultKey = api['default']
        
        # Retrieving other options
        choosen_theme = save_json['theme']
        grid_display = save_json['grid']
        choosen_range = save_json['range']
        time_format = save_json['time_format']
        date_format = save_json['date_format']

        # --- Applying the retrieved parameters
        self.api_name = apiName
        self.api_key = key
        self.api_def_key = defaultKey
        self.opt_combo_api.setCurrentText(apiName)

        self.opt_lineEdit_apiKey.setText(key)

        # Theme
        self.opt_combo_theme.setCurrentText(choosen_theme)
        self.theme = choosen_theme
        if self.theme == "Light":
            self.graph.setBackground('w')
            self.pen = self.red_pen
        if self.theme == "Dark":
            self.graph.setBackground((0,0,0))
            self.pen = self.white_pen

        # Grid
        if grid_display == 'Yes':
            self.opt_radio_YES.setChecked(True)
            self.grid = True
            self.graph.showGrid(x=True, y=True)
        else:
            self.opt_radio_NO.setChecked(True)
            self.grid = False
            self.graph.showGrid(x=False, y=False)
        
        self.range = choosen_range
        self.tab_chart_range.setCurrentText(f'{str(choosen_range)} days')

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

    def saveAll(self):
        """ Apply user's preferences and save them to save.json.
        Starts by clicking on the 'Save all' button """

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
        
        choosen_theme = self.opt_combo_theme.currentText()
        self.theme = choosen_theme

        range_val = self.tab_chart_range.currentText()
        range_val = [int(s) for s in range_val.split() if s.isdigit()]
        range_val = range_val[0]
        self.range = range_val

        if self.opt_radio_YES.isChecked():
            self.grid = True
            grid_display = 'Yes'
        if self.opt_radio_NO.isChecked():
            self.grid = False
            grid_display = 'No'

        # --- Save preferences in file
        save_json['choosen_api'] = apiName
        for api in save_json['API']:
            if api['name'] == apiName:
                if api['key'] != apiKey:
                    api['key'] = apiKey
                else:
                    pass

        save_json['theme'] = choosen_theme
        save_json['grid'] = grid_display
        save_json['range'] = range_val
        save_json['time_format'] = time_form
        save_json['date_format'] = date_form

        with open('save.json', 'w') as outsave:
            json.dump(save_json, outsave)
        
        # --- 
        text = 'All preferences have been applied and saved'
        self.opt_label_save_remind.setText(text)

    def check_api_key_change(self):
        """ When the user inserts an API key different from 
        the one saved in the backup file, the user is invited 
        to test it by clicking on the 'TEST' button. The 'Save all' 
        button is disabled as long as the check result is not
        positive. """

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
        """ Launches an API key validation test to the 
        'self.convert_API (test = True)' function, if the 
        API key is invalid, a window is displayed offering 
        the user to restore the API key saved in the backup file.
        Connect to 'TEST' button in option tab."""

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

        return test

    def api_switch(self):
        """ The API key displayed changes depending on 
        the API chosen on the comboBox """

        current = self.opt_combo_api.currentText()
        for api in save_json['API']:
            if api['name'] == current:
                self.opt_lineEdit_apiKey.setText(api['key'])

    def input_check(self):
        """ In the convert tab, checks the value entered by 
        the user at each key pressed, if it's not valid, 
        the "Convert" button is disabled """

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
        """ Invert the 2 comboBox current indexes in the 
        converter tab or the graph tab """

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
        The rates are acquired by calling the function 
        'self.convert_API (curr1, curr2)'
        """
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
        rate = self.convert_API(curr_1, curr_2)

        if rate == None:
            text = "API does not respond"
            self.main_status.setText(text)
            return None

        elif rate == False:
            text = "Invalid API"
            self.main_status.setText(text)
            return None
        
        else :
            self.main_status.setText('')

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
    
    def copy_conv(self):
        """ Copy the converter output value in clipboard """
        value = self.tab_conv_output.text()

        if len(value) != 0:
            pyperclip.copy(value)
            text = 'Value copied to clipboard'
            self.main_status.setText(text)
        else:
            text = 'No value to copy'
            self.main_status.setText(text)

    def convert_API(self, curr1, curr2, test=(False, "", "")):
        """Acquires the rate from the API chosen by the user and 
        its key (self.api_name and self.api_key). The function 
        returns 'None' if the URL does not respond, 'False' if 
        the API key is incorrect, the rate otherwise. 
        The function also has a test mode which allows to 
        check the validity of the API key, if it's correct the 
        function does not return the rate but only 'True', 
        'False' otherwise. 
        test=(True/False, api_name, api_key) """

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
    
    def time_range(self):
        t_range = self.tab_chart_range.currentText()
        t_range = [int(s) for s in t_range.split() if s.isdigit()]
        t_range = t_range[0]
        
        day = 86400
        ts_list = []
        now = int(time.time())
        ts_start = now - (day * t_range)
        ts_list.append(ts_start)

        i = 0
        while now not in ts_list:
            add = ts_list[i] + day
            ts_list.append(add)
            i+=1

        start_api = datetime.fromtimestamp(ts_list[0])
        start_api = start_api.strftime('%Y-%m-%d')
        now_api = datetime.fromtimestamp(ts_list[-1])
        now_api = now_api.strftime('%Y-%m-%d')

        return [(start_api, now_api), ts_list]


    def get_historical(self):
        """ Get historical data of choosen currency pair """
        
        # Get the currency codes
        for key, value in curr_json.items():
            if value['name'] == self.tab_chart_curr1.currentText():
                curr1 = key
        
        for key, value in curr_json.items():
            if value['name'] == self.tab_chart_curr2.currentText():
                curr2 = key

        self.currs_graph = (curr1, curr2)

        # Get free.currconv API key
        api_hist = 'free.currconv'
        for api in save_json['API']:
            if api['name'] == api_hist:
                key = api['key']
        
        # Set time range
        t_range = self.time_range()

        # Range date for API syntax
        api_range = t_range[0]
        api_start = api_range[0] # From
        api_now = api_range[1] # To

        # List of timestamps in range
        ts_list = t_range[1]
        self.time_list = ts_list

        # Get JSON
        url = f"https://free.currconv.com/api/v7/convert?q={curr1}_{curr2}&compact=ultra&date={api_start}&endDate={api_now}&apiKey={key}"
        response = requests.get(url)
        data = json.loads(response.text)
        #print(data)

        # Generation of str dates list
        dte_list = []
        if self.date_format == "dd/mm/yyyy":
            dte_form = "%d/%m/%Y"
        elif self.date_format == "mm/dd/yyyy":
            dte_form = "%m/%d/%Y"
        else: # yyyy/mm/dd
            dte_form = "%Y/%m/%d"

        for ts in ts_list:
            dte = datetime.fromtimestamp(ts)
            dte = dte.strftime(dte_form)
            dte_list.append(dte)
        
        # Rates extraction
        rate_list = []
        for r in data[f'{curr1}_{curr2}'].items():
            rate_list.append(r[1])
        
        self.rate_list = rate_list
        
        # GRAPH DRAW
        self.graph_draw(dte_list, rate_list)

        # GRAPH STATS
        self.graph_stats(dte_list, rate_list)

        # Set graph title
        txt = f"{dte_list[0]} to {dte_list[-1]}"
        self.graph.setTitle(f"{curr1}/{curr2} - {txt}")
        
        #print(dte_list)
        #print(rate_list)
    
    def graph_draw(self, d_list, r_list):
        """ Draw the graph
        x = dates, y = rates """

        if self.grid:
            self.graph.showGrid(x=True, y=True)
        else :
            self.graph.showGrid(x=False, y=False)
        
        if self.theme == "Light":
            self.graph.setBackground('w')
            self.pen = self.red_pen
        if self.theme == "Dark":
            self.graph.setBackground((0,0,0))
            self.pen = self.white_pen

        self.graph.clear()

        y_axis = np.array(r_list)

        x_dict = dict(enumerate(d_list))
        stringAxis = pg.AxisItem(orientation='bottom')
        stringAxis.setTicks([x_dict.items()])

        self.graph.setAxisItems(axisItems={'bottom' : stringAxis})

        self.graph.plot(list(x_dict.keys()), y_axis, pen= self.pen)

        self.tab_chart_button_copy.setEnabled(True)
        self.tab_chart_button_save.setEnabled(True)

    def graph_stats(self, d_list, r_list):
        """ Displays statistics from dates list and rates list
        Right column in graph tab """

        # Time range
        dte_from = d_list[0]
        dte_to = d_list[-1]
        range_days = f"{self.range} days"

        self.tab_chart_label_from.setText(f"From\n {dte_from}")
        self.tab_chart_label_to.setText(f"To\n {dte_to}")
        self.tab_chart_label_range.setText(f"Range\n {range_days}")

        # Last rate
        last_rate = r_list[-1]
        self.tab_chart_last_rate.setText(str(last_rate))

        # Last variation
        perc_round = 4
        abs_round = 6

        b_last_rate = r_list[-2]
        perc_var = (last_rate-b_last_rate)/b_last_rate*100
        perc_var = round(perc_var, perc_round)
        self.tab_chart_last_var_perc.setText(f"{str(perc_var)}%")

        if last_rate > b_last_rate:
            var_abs = last_rate - b_last_rate
            var_abs = round(var_abs, abs_round)
            self.tab_chart_last_var_abs.setText(f"+{var_abs}")
        else:
            var_abs = last_rate - b_last_rate
            var_abs = round(var_abs, abs_round)
            self.tab_chart_last_var_abs.setText(f"{var_abs}")
        
        # Total variation
        first_rate = r_list[0]
        perc_var = (last_rate-first_rate)/first_rate*100
        perc_var = round(perc_var, perc_round)
        self.tab_chart_var_total_perc.setText(f"{str(perc_var)}%")

        if last_rate > first_rate:
            var_abs = last_rate - first_rate
            var_abs = round(var_abs, abs_round)
            self.tab_chart_var_total_abs.setText(f"+{var_abs}")
        else:
            var_abs = last_rate - first_rate
            var_abs = round(var_abs, abs_round)
            self.tab_chart_var_total_abs.setText(f"{var_abs}")
        
        # Min/Max/Min
        min_rate = min(r_list)
        max_rate = max(r_list)
        mean_rate = round(mean(r_list),abs_round)

        self.tab_chart_min.setText(f"{str(min_rate)}")
        self.tab_chart_max.setText(f"{str(max_rate)}")
        self.tab_chart_mean.setText(f"{str(mean_rate)}")
    
    def save_graph(self):
        title = f"{self.currs_graph[0]}_{self.currs_graph[1]}"
        export = exporters.ImageExporter(self.graph.plotItem)

        #name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        export.export(f'{title}.png')

        self.main_status.setText("Graph saved successfully")
    
    def copy_graph(self):
        """ Copy the data from the graph as a dictionary
        - Currency pair
        - Timestamps
        - Rates """

        if len(self.rate_list) >= 2:
            copy = {}

            copy['pair'] = [self.currs_graph[0], self.currs_graph[1]]

            rates_dict = {}
            i = 0 
            while len(rates_dict) < len(self.rate_list):
                rates_dict[f'{int(self.time_list[i])}'] = f'{float(self.rate_list[i])}'
                i+=1
            
            copy['rates'] = rates_dict

            pyperclip.copy(str(copy))
            txt = 'Values copied to clipboard'
            self.main_status.setText(txt)
        
        else:
            txt = 'No value to copy'
            self.main_status.setText(txt)

    def checkConnection(self, host ="8.8.8.8", port=53, timeout=3):
        """ Regularly check the connection status.
		To do this, a regular connection is established 
		with the Google DNS (8.8.8.8) """
        
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))

            if self.backOnline:
                self.connection_lost = False
                self.main_status.setText("Back online")
                print('BACK ONLINE')
                self.opt_button_test.setEnabled(True)
                self.tab_conv_button_convert.setEnabled(True)
                self.tab_chart_button_view.setEnabled(True)

                self.backOnline = False
            
        except socket.error as ex: # Connection lost
            """ A connection lost has the effect of deactivating 
            certain buttons in order to prevent the user from 
            launching processes requiring an internet connection. """

            print("CONNECTION LOST")
            self.connection_lost = True
            self.main_status.setText("CONNECTION LOST")

            self.opt_button_test.setEnabled(False)
            self.tab_conv_button_convert.setEnabled(False)
            self.tab_chart_button_view.setEnabled(False)

            self.backOnline = True

    def closeEvent(self, event):
        """ End threads when closing programs """

        event.accept()
        self.timer_connCheck.stop()
        self.timer_currTime.stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())