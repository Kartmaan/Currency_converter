from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import QLocale
import pyqtgraph as pg 
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1051, 711)
        MainWindow.setMinimumSize(QtCore.QSize(1051, 711))
        MainWindow.setMaximumSize(QtCore.QSize(1051, 711))
        font = QtGui.QFont()
        font.setPointSize(18)
        MainWindow.setFont(font)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setWindowIcon(QtGui.QIcon('favicon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        
        # ToolBox hub
        self.tab_hub = QtWidgets.QToolBox(self.centralwidget)
        self.tab_hub.setGeometry(QtCore.QRect(10, 60, 1031, 621))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tab_hub.setFont(font)
        self.tab_hub.setFrameShape(QtWidgets.QFrame.Box)
        self.tab_hub.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_hub.setObjectName("tab_hub")

        # --------------------------------------------------------
        # - - - - - Tab option - - - - -
        self.tab_option = QtWidgets.QWidget()
        self.tab_option.setGeometry(QtCore.QRect(0, 0, 1027, 518))
        self.tab_option.setObjectName("tab_option")

        # - - - - GroupBox API
        self.opt_groupBox_api = QtWidgets.QGroupBox(self.tab_option)
        self.opt_groupBox_api.setGeometry(QtCore.QRect(10, 0, 1001, 131))
        self.opt_groupBox_api.setObjectName("opt_groupBox_api")

        # ComboBox API choice
        self.opt_combo_api = QtWidgets.QComboBox(self.opt_groupBox_api)
        self.opt_combo_api.setGeometry(QtCore.QRect(10, 40, 261, 51))
        self.opt_combo_api.setObjectName("opt_combo_api")
        #self.opt_combo_api.addItems(["free.currconv", "xe.com"])

        # LineEdit API key
        self.opt_lineEdit_apiKey = QtWidgets.QLineEdit(self.opt_groupBox_api)
        self.opt_lineEdit_apiKey.setGeometry(QtCore.QRect(290, 40, 521, 51))
        self.opt_lineEdit_apiKey.setObjectName("opt_lineEdit_apiKey")

        # Button test
        self.opt_button_test = QtWidgets.QPushButton(self.opt_groupBox_api)
        self.opt_button_test.setGeometry(QtCore.QRect(830, 42, 151, 51))
        self.opt_button_test.setObjectName("opt_button_test")

        # Label API check
        self.opt_label_api_check = QtWidgets.QLabel(self.opt_groupBox_api)
        self.opt_label_api_check.setGeometry(QtCore.QRect(280, 95, 441, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.opt_label_api_check.setFont(font)
        self.opt_label_api_check.setAlignment(QtCore.Qt.AlignCenter)
        self.opt_label_api_check.setObjectName("opt_label_api_check")

        # - - - - GroupBox refresh
        self.opt_groupBox_refresh = QtWidgets.QGroupBox(self.tab_option)
        self.opt_groupBox_refresh.setGeometry(QtCore.QRect(10, 140, 481, 241))
        self.opt_groupBox_refresh.setObjectName("opt_groupBox_refresh")
        self.opt_groupBox_refresh.setEnabled(False) 

        # Label instruction
        self.opt_label_refresh_inst = QtWidgets.QLabel(self.opt_groupBox_refresh)
        self.opt_label_refresh_inst.setGeometry(QtCore.QRect(10, 30, 441, 31))
        font = QtGui.QFont()
        font.setItalic(True)
        self.opt_label_refresh_inst.setFont(font)
        self.opt_label_refresh_inst.setAlignment(QtCore.Qt.AlignCenter)
        self.opt_label_refresh_inst.setObjectName("opt_label_refresh_inst")
        self.opt_label_refresh_inst.setHidden(True)

        self.opt_label_refresh_info = QtWidgets.QLabel(self.opt_groupBox_refresh)
        self.opt_label_refresh_info.setGeometry(QtCore.QRect(10, 30, 441, 31))
        self.opt_label_refresh_info.setFont(font)
        self.opt_label_refresh_info.setAlignment(QtCore.Qt.AlignCenter)
        self.opt_label_refresh_info.setText("- - - Graph functionality in a future version - - -")


        # SpinBox time
        self.opt_spinBox_time = QtWidgets.QSpinBox(self.opt_groupBox_refresh)
        self.opt_spinBox_time.setGeometry(QtCore.QRect(150, 110, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.opt_spinBox_time.setFont(font)
        self.opt_spinBox_time.setAlignment(QtCore.Qt.AlignCenter)
        self.opt_spinBox_time.setMinimum(1)
        self.opt_spinBox_time.setMaximum(180)
        self.opt_spinBox_time.setObjectName("opt_spinBox_time")

        # ComboBox time unit
        self.opt_combo_unit = QtWidgets.QComboBox(self.opt_groupBox_refresh)
        self.opt_combo_unit.setGeometry(QtCore.QRect(250, 110, 61, 41))
        self.opt_combo_unit.setFrame(True)
        self.opt_combo_unit.setObjectName("opt_combo_unit")
        self.opt_combo_unit.addItems(["Min.","Sec."])

        # Label refresh reminder
        self.opt_label_refresh_remind = QtWidgets.QLabel(self.opt_groupBox_refresh)
        self.opt_label_refresh_remind.setGeometry(QtCore.QRect(16, 168, 431, 71))
        self.opt_label_refresh_remind.setAlignment(QtCore.Qt.AlignCenter)
        self.opt_label_refresh_remind.setObjectName("opt_label_refresh_remind")

        # - - - - GroupBox time and date
        self.opt_groupBox_time = QtWidgets.QGroupBox(self.tab_option)
        self.opt_groupBox_time.setGeometry(QtCore.QRect(530, 140, 481, 241))
        self.opt_groupBox_time.setObjectName("opt_groupBox_time")

        # Label time and date instruction
        self.opt_label_time_inst = QtWidgets.QLabel(self.opt_groupBox_time)
        self.opt_label_time_inst.setGeometry(QtCore.QRect(10, 30, 441, 31))
        font = QtGui.QFont()
        font.setItalic(True)
        self.opt_label_time_inst.setFont(font)
        self.opt_label_time_inst.setAlignment(QtCore.Qt.AlignCenter)
        self.opt_label_time_inst.setObjectName("opt_label_time_inst")

        # Frame date option display
        self.opt_frame_date = QtWidgets.QFrame(self.opt_groupBox_time)
        self.opt_frame_date.setGeometry(QtCore.QRect(10, 60, 461, 80))
        self.opt_frame_date.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.opt_frame_date.setFrameShadow(QtWidgets.QFrame.Raised)
        self.opt_frame_date.setObjectName("opt_frame_date")

        # Label date
        self.opt_label_date = QtWidgets.QLabel(self.opt_frame_date)
        self.opt_label_date.setGeometry(QtCore.QRect(10, 20, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.opt_label_date.setFont(font)
        self.opt_label_date.setObjectName("opt_label_date")

        # Radio dd/mm/yyyy
        self.opt_radio_dmy = QtWidgets.QRadioButton(self.opt_frame_date)
        self.opt_radio_dmy.setGeometry(QtCore.QRect(10, 40, 141, 31))
        self.opt_radio_dmy.setChecked(True)
        self.opt_radio_dmy.setObjectName("opt_radio_dmy")

        # Radio mm/dd/yyyy
        self.opt_radio_mdy = QtWidgets.QRadioButton(self.opt_frame_date)
        self.opt_radio_mdy.setGeometry(QtCore.QRect(160, 40, 141, 31))
        self.opt_radio_mdy.setObjectName("opt_radio_mdy")

        # Radio yyyy/mm/dd
        self.opt_radio_ymd = QtWidgets.QRadioButton(self.opt_frame_date)
        self.opt_radio_ymd.setGeometry(QtCore.QRect(310, 40, 141, 31))
        self.opt_radio_ymd.setObjectName("opt_radio_ymd")

        # Frame hour option display
        self.opt_frame_hour = QtWidgets.QFrame(self.opt_groupBox_time)
        self.opt_frame_hour.setGeometry(QtCore.QRect(10, 150, 461, 80))
        self.opt_frame_hour.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.opt_frame_hour.setFrameShadow(QtWidgets.QFrame.Raised)
        self.opt_frame_hour.setObjectName("opt_frame_hour")

        # Label hour 
        self.opt_label_hour = QtWidgets.QLabel(self.opt_frame_hour)
        self.opt_label_hour.setGeometry(QtCore.QRect(10, 20, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.opt_label_hour.setFont(font)
        self.opt_label_hour.setObjectName("opt_label_hour")

        # Radio format 24h
        self.opt_radio_24 = QtWidgets.QRadioButton(self.opt_frame_hour)
        self.opt_radio_24.setGeometry(QtCore.QRect(10, 40, 141, 31))
        self.opt_radio_24.setChecked(True)
        self.opt_radio_24.setObjectName("opt_radio_24")

        # Radio format 12h
        self.opt_radio_12 = QtWidgets.QRadioButton(self.opt_frame_hour)
        self.opt_radio_12.setGeometry(QtCore.QRect(160, 40, 141, 31))
        self.opt_radio_12.setObjectName("opt_radio_12")

        # - - - - GroupBox save
        self.opt_groupBox_save = QtWidgets.QGroupBox(self.tab_option)
        self.opt_groupBox_save.setGeometry(QtCore.QRect(9, 389, 1001, 121))
        self.opt_groupBox_save.setObjectName("opt_groupBox_save")

        # Button save all
        self.opt_button_save = QtWidgets.QPushButton(self.opt_groupBox_save)
        self.opt_button_save.setGeometry(QtCore.QRect(450, 44, 101, 51))
        self.opt_button_save.setObjectName("opt_button_save")

        # Label save reminder
        self.opt_label_save_remind = QtWidgets.QLabel(self.opt_groupBox_save)
        self.opt_label_save_remind.setGeometry(QtCore.QRect(570, 34, 431, 71))
        font = QtGui.QFont()
        font.setItalic(True)
        self.opt_label_save_remind.setFont(font)
        self.opt_label_save_remind.setAlignment(QtCore.Qt.AlignCenter)
        self.opt_label_save_remind.setObjectName("opt_label_save_remind")

        # --------------------------------------------------------
        # - - - - -  Tab converter - - - - -
        self.tab_hub.addItem(self.tab_option, "")
        self.tab_conv = QtWidgets.QWidget()
        self.tab_conv.setGeometry(QtCore.QRect(0, 0, 1027, 518))
        self.tab_conv.setObjectName("tab_conv")

        # ComboBox currency 1
        self.tab_conv_curr1 = QtWidgets.QComboBox(self.tab_conv)
        self.tab_conv_curr1.setGeometry(QtCore.QRect(280, 110, 240, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tab_conv_curr1.setFont(font)
        self.tab_conv_curr1.setObjectName("tab_conv_curr1")

        # ComboBox currency 2
        self.tab_conv_curr2 = QtWidgets.QComboBox(self.tab_conv)
        self.tab_conv_curr2.setGeometry(QtCore.QRect(590, 110, 240, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tab_conv_curr2.setFont(font)
        self.tab_conv_curr2.setObjectName("tab_conv_curr2")

        # Button convert
        self.tab_conv_button_convert = QtWidgets.QPushButton(self.tab_conv)
        self.tab_conv_button_convert.setGeometry(QtCore.QRect(858, 115, 151, 51))
        self.tab_conv_button_convert.setObjectName("tab_conv_button_convert")

        # Input
        self.tab_conv_input = QtWidgets.QLineEdit(self.tab_conv)
        self.tab_conv_input.setGeometry(QtCore.QRect(20, 110, 241, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.tab_conv_input.setFont(font)
        self.tab_conv_input.setAcceptDrops(False)
        self.tab_conv_input.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_conv_input.setObjectName("tab_conv_input")

        # Output
        self.tab_conv_output = QtWidgets.QLineEdit(self.tab_conv)
        self.tab_conv_output.setGeometry(QtCore.QRect(110, 210, 781, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(25)
        font.setItalic(False)
        self.tab_conv_output.setFont(font)
        self.tab_conv_output.setAcceptDrops(False)
        self.tab_conv_output.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_conv_output.setReadOnly(True)
        self.tab_conv_output.setObjectName("tab_conv_output")

        # Button clear
        self.tab_conv_button_clear = QtWidgets.QPushButton(self.tab_conv)
        self.tab_conv_button_clear.setGeometry(QtCore.QRect(390, 290, 81, 31))
        self.tab_conv_button_clear.setObjectName("tab_conv_button_clear")

        # Frame info
        self.tab_conv_frame_info = QtWidgets.QFrame(self.tab_conv)
        self.tab_conv_frame_info.setGeometry(QtCore.QRect(9, 410, 1011, 101))
        self.tab_conv_frame_info.setFrameShape(QtWidgets.QFrame.Box)
        self.tab_conv_frame_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_conv_frame_info.setObjectName("tab_conv_frame_info")

        # Label info
        self.tab_conv_label_info = QtWidgets.QLabel(self.tab_conv_frame_info)
        self.tab_conv_label_info.setGeometry(QtCore.QRect(40, 20, 921, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tab_conv_label_info.setFont(font)
        self.tab_conv_label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_conv_label_info.setObjectName("tab_conv_label_info")

        # Label amount
        self.tab_conv_label_amount = QtWidgets.QLabel(self.tab_conv)
        self.tab_conv_label_amount.setGeometry(QtCore.QRect(20, 80, 101, 19))
        self.tab_conv_label_amount.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tab_conv_label_amount.setObjectName("tab_conv_label_amount")

        # Label from
        self.tab_conv_label_from = QtWidgets.QLabel(self.tab_conv)
        self.tab_conv_label_from.setGeometry(QtCore.QRect(280, 80, 101, 19))
        self.tab_conv_label_from.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tab_conv_label_from.setObjectName("tab_conv_label_from")

        # Label to
        self.tab_conv_label_to = QtWidgets.QLabel(self.tab_conv)
        self.tab_conv_label_to.setGeometry(QtCore.QRect(590, 80, 101, 19))
        self.tab_conv_label_to.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tab_conv_label_to.setObjectName("tab_conv_label_to")

        # Button copy
        self.tab_conv_button_copy = QtWidgets.QPushButton(self.tab_conv)
        self.tab_conv_button_copy.setGeometry(QtCore.QRect(530, 290, 81, 31))
        self.tab_conv_button_copy.setObjectName("tab_conv_button_copy")

        # Button swipe
        self.tab_conv_button_swipe = QtWidgets.QPushButton(self.tab_conv)
        self.tab_conv_button_swipe.setGeometry(QtCore.QRect(535, 120, 41, 41))
        self.tab_conv_button_swipe.setCheckable(False)
        self.tab_conv_button_swipe.setAutoRepeat(False)
        self.tab_conv_button_swipe.setObjectName("tab_conv_button_swipe")

        # --------------------------------------------------------
        # - - - - - Tab chart - - - - -
        self.tab_hub.addItem(self.tab_conv, "")
        self.tab_chart = QtWidgets.QWidget()
        self.tab_chart.setGeometry(QtCore.QRect(0, 0, 1027, 518))
        self.tab_chart.setObjectName("tab_chart")

        # ComboBox curr 1
        self.tab_chart_curr1 = QtWidgets.QComboBox(self.tab_chart)
        self.tab_chart_curr1.setGeometry(QtCore.QRect(10, 10, 311, 41))
        self.tab_chart_curr1.setEditable(False)
        self.tab_chart_curr1.setObjectName("tab_chart_curr1")

        # ComboBox curr2
        self.tab_chart_curr2 = QtWidgets.QComboBox(self.tab_chart)
        self.tab_chart_curr2.setGeometry(QtCore.QRect(410, 10, 321, 41))
        self.tab_chart_curr2.setObjectName("tab_chart_curr2")

        # Button view
        self.tab_chart_button_run = QtWidgets.QPushButton(self.tab_chart)
        self.tab_chart_button_run.setGeometry(QtCore.QRect(743, 10, 271, 41))
        self.tab_chart_button_run.setObjectName("tab_chart_button_view")

        # Frame graph
        self.tab_chart_frame_graph = QtWidgets.QFrame(self.tab_chart)
        self.tab_chart_frame_graph.setGeometry(QtCore.QRect(9, 69, 721, 401))
        self.tab_chart_frame_graph.setFrameShape(QtWidgets.QFrame.Box)
        self.tab_chart_frame_graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_chart_frame_graph.setObjectName("tab_chart_frame_graph")

        # Graph
        self.graph = pg.PlotWidget(self.tab_chart_frame_graph)
        self.graph.setGeometry(QtCore.QRect(0,0,721, 401))
        self.graph.setBackground('w')
        self.graph.showGrid(x=True, y=True)
        self.graph.setTitle("", bold=True)
        self.graph.setLabel('left', 'Rate')
        self.graph.setLabel('bottom', 'Time')

        # Pens graph
        self.red_pen = pg.mkPen(color=(255,0,0), width = 2)
        self.blue_pen = pg.mkPen(color=(0,0,255), width = 2)

        """ 
        x1 = [1, 2, 3, 4, 5]
        x1 = np.array(x1)

        y1 = [3.1454, 3.1484, 3.1424, 3.1452, 3.1462]
        y1 = np.array(y1)

        self.graph.plot(x1, y1, pen = self.red_pen) """

        # Frame info chart
        self.tab_chart_frame_info = QtWidgets.QFrame(self.tab_chart)
        self.tab_chart_frame_info.setGeometry(QtCore.QRect(737, 69, 281, 441))
        self.tab_chart_frame_info.setFrameShape(QtWidgets.QFrame.Box)
        self.tab_chart_frame_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_chart_frame_info.setObjectName("tab_chart_frame_info")

        # Label time info
        self.tab_chart_label_time_info = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_time_info.setGeometry(QtCore.QRect(50, 5, 171, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.tab_chart_label_time_info.setFont(font)
        self.tab_chart_label_time_info.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_label_time_info.setObjectName("tab_chart_label_time_info")

        # Label started at
        self.tab_chart_label_started_at = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_started_at.setGeometry(QtCore.QRect(40, 30, 91, 41))
        self.tab_chart_label_started_at.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tab_chart_label_started_at.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.tab_chart_label_started_at.setWordWrap(True)
        self.tab_chart_label_started_at.setObjectName("tab_chart_label_started_at")

        # Label last update
        self.tab_chart_label_last_up = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_last_up.setGeometry(QtCore.QRect(140, 30, 101, 41))
        self.tab_chart_label_last_up.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tab_chart_label_last_up.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.tab_chart_label_last_up.setWordWrap(True)
        self.tab_chart_label_last_up.setObjectName("tab_chart_label_last_up")

        # Label next update
        self.tab_chart_label_next_up = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_next_up.setGeometry(QtCore.QRect(85, 80, 111, 41))
        self.tab_chart_label_next_up.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tab_chart_label_next_up.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.tab_chart_label_next_up.setWordWrap(True)
        self.tab_chart_label_next_up.setObjectName("tab_chart_label_next_up")

        # Line 1
        self.tab_chart_line_1 = QtWidgets.QFrame(self.tab_chart_frame_info)
        self.tab_chart_line_1.setGeometry(QtCore.QRect(2, 120, 279, 20))
        self.tab_chart_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.tab_chart_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tab_chart_line_1.setObjectName("tab_chart_line_1")

        # Label last variation
        self.tab_chart_label_last_var = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_last_var.setGeometry(QtCore.QRect(60, 192, 161, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.tab_chart_label_last_var.setFont(font)
        self.tab_chart_label_last_var.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_label_last_var.setObjectName("tab_chart_label_last_var")

        # Last variation value (percent)
        self.tab_chart_last_var_perc = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_last_var_perc.setGeometry(QtCore.QRect(5, 211, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.tab_chart_last_var_perc.setFont(font)
        self.tab_chart_last_var_perc.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_last_var_perc.setObjectName("tab_chart_last_var_perc")

        # Last variation value (abs)
        self.tab_chart_last_var_abs = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_last_var_abs.setGeometry(QtCore.QRect(140, 211, 133, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tab_chart_last_var_abs.setFont(font)
        self.tab_chart_last_var_abs.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_last_var_abs.setObjectName("tab_chart_last_var_abs")

        # Label total variation
        self.tab_chart_label_var_total = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_var_total.setGeometry(QtCore.QRect(60, 249, 161, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.tab_chart_label_var_total.setFont(font)
        self.tab_chart_label_var_total.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_label_var_total.setObjectName("tab_chart_label_var_fstart")

        # Total variation value (percent)
        self.tab_chart_var_total_perc = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_var_total_perc.setGeometry(QtCore.QRect(5, 269, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.tab_chart_var_total_perc.setFont(font)
        self.tab_chart_var_total_perc.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_var_total_perc.setObjectName("tab_chart_var_fstart_perc")

        # Total variation value (abs)
        self.tab_chart_var_total_abs = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_var_total_abs.setGeometry(QtCore.QRect(140, 269, 133, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tab_chart_var_total_abs.setFont(font)
        self.tab_chart_var_total_abs.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_var_total_abs.setObjectName("tab_chart_var_fstart_abs")

        # Min value
        self.tab_chart_min = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_min.setGeometry(QtCore.QRect(40, 320, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tab_chart_min.setFont(font)
        self.tab_chart_min.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_min.setObjectName("tab_chart_min")

        # Mean value
        self.tab_chart_mean = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_mean.setGeometry(QtCore.QRect(40, 366, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tab_chart_mean.setFont(font)
        self.tab_chart_mean.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_mean.setObjectName("tab_chart_mean")

        # Max value
        self.tab_chart_max = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_max.setGeometry(QtCore.QRect(40, 410, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tab_chart_max.setFont(font)
        self.tab_chart_max.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_max.setObjectName("tab_chart_max")

        # Label min
        self.tab_chart_label_min = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_min.setGeometry(QtCore.QRect(114, 300, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tab_chart_label_min.setFont(font)
        self.tab_chart_label_min.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_label_min.setObjectName("tab_chart_label_min")

        # Label mean
        self.tab_chart_label_mean = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_mean.setGeometry(QtCore.QRect(114, 345, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tab_chart_label_mean.setFont(font)
        self.tab_chart_label_mean.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_label_mean.setObjectName("tab_chart_label_mean")

        # Label max
        self.tab_chart_label_max = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_max.setGeometry(QtCore.QRect(114, 390, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tab_chart_label_max.setFont(font)
        self.tab_chart_label_max.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_label_max.setObjectName("tab_chart_label_max")

        # Label last rate
        self.tab_chart_label_last_rate = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_label_last_rate.setGeometry(QtCore.QRect(60, 135, 161, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.tab_chart_label_last_rate.setFont(font)
        self.tab_chart_label_last_rate.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_label_last_rate.setObjectName("tab_chart_label_last_rate")

        # Last rate value
        self.tab_chart_last_rate = QtWidgets.QLabel(self.tab_chart_frame_info)
        self.tab_chart_last_rate.setGeometry(QtCore.QRect(30, 154, 220, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tab_chart_last_rate.setFont(font)
        self.tab_chart_last_rate.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_chart_last_rate.setObjectName("tab_chart_last_rate")

        # Line 2
        self.tab_chart_line_2 = QtWidgets.QFrame(self.tab_chart_frame_info)
        self.tab_chart_line_2.setGeometry(QtCore.QRect(2, 180, 279, 20))
        self.tab_chart_line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.tab_chart_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tab_chart_line_2.setObjectName("tab_chart_line_2")

        # Line 3
        self.tab_chart_line_3 = QtWidgets.QFrame(self.tab_chart_frame_info)
        self.tab_chart_line_3.setGeometry(QtCore.QRect(2, 237, 279, 20))
        self.tab_chart_line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.tab_chart_line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tab_chart_line_3.setObjectName("tab_chart_line_3")

        # Line 4
        self.tab_chart_line_4 = QtWidgets.QFrame(self.tab_chart_frame_info)
        self.tab_chart_line_4.setGeometry(QtCore.QRect(2, 293, 279, 20))
        self.tab_chart_line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.tab_chart_line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tab_chart_line_4.setObjectName("tab_chart_line_4")

        # Button STOP
        self.tab_chart_button_stop = QtWidgets.QPushButton(self.tab_chart)
        self.tab_chart_button_stop.setGeometry(QtCore.QRect(10, 480, 201, 31))
        self.tab_chart_button_stop.setObjectName("tab_chart_button_stop")

        # Button save
        self.tab_chart_button_save = QtWidgets.QPushButton(self.tab_chart)
        self.tab_chart_button_save.setGeometry(QtCore.QRect(270, 480, 201, 31))
        self.tab_chart_button_save.setObjectName("tab_chart_button_save")

        # Button "copy rate values"
        self.tab_chart_button_copy = QtWidgets.QPushButton(self.tab_chart)
        self.tab_chart_button_copy.setGeometry(QtCore.QRect(530, 480, 201, 31))
        self.tab_chart_button_copy.setObjectName("tab_chart_copy")

        # Button swipe
        self.tab_chart_button_swipe = QtWidgets.QPushButton(self.tab_chart)
        self.tab_chart_button_swipe.setGeometry(QtCore.QRect(345, 10, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tab_chart_button_swipe.setFont(font)
        self.tab_chart_button_swipe.setObjectName("tab_chart_button_swipe")

        #self.tab_hub.addItem(self.tab_chart, "")

        # --------------------------------------------------------
        # - - - - - Main window - - - - -

        # Label Title
        self.main_title = QtWidgets.QLabel(self.centralwidget)
        self.main_title.setGeometry(QtCore.QRect(400, 10, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.main_title.setFont(font)
        self.main_title.setAlignment(QtCore.Qt.AlignCenter)
        self.main_title.setObjectName("main_title")

        # Label status message
        self.main_status = QtWidgets.QLabel(self.centralwidget)
        self.main_status.setGeometry(QtCore.QRect(16, 680, 1021, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        font.setUnderline(False)
        self.main_status.setFont(font)
        self.main_status.setAlignment(QtCore.Qt.AlignCenter)
        self.main_status.setObjectName("main_status")

        # Label time and date
        self.main_time = QtWidgets.QLabel(self.centralwidget)
        self.main_time.setGeometry(QtCore.QRect(12, 10, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.main_time.setFont(font)
        self.main_time.setFrameShape(QtWidgets.QFrame.Panel)
        self.main_time.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_time.setAlignment(QtCore.Qt.AlignCenter)
        self.main_time.setObjectName("main_time")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tab_hub.setCurrentIndex(1)
        self.tab_hub.layout().setSpacing(6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.opt_groupBox_api.setTitle(_translate("MainWindow", "API key"))
        #self.opt_combo_api.setItemText(0, _translate("MainWindow", "free.currconv.com"))
        #self.opt_combo_api.setItemText(1, _translate("MainWindow", "xe.com"))
        self.opt_lineEdit_apiKey.setText(_translate("MainWindow", "23a2ea907e3df0c23fb8"))
        self.opt_button_test.setText(_translate("MainWindow", "TEST"))
        self.opt_label_api_check.setText(_translate("MainWindow", ""))
        self.opt_groupBox_refresh.setTitle(_translate("MainWindow", "Chart refresh"))
        self.opt_label_refresh_inst.setText(_translate("MainWindow", "Define the graph refresh interval"))
        #self.opt_combo_unit.setItemText(0, _translate("MainWindow", "Min."))
        #self.opt_combo_unit.setItemText(1, _translate("MainWindow", "Sec."))
        self.opt_label_refresh_remind.setText(_translate("MainWindow", ""))
        self.opt_groupBox_time.setTitle(_translate("MainWindow", "Time and date format"))
        self.opt_label_time_inst.setText(_translate("MainWindow", "Choose the time and date format to display"))
        self.opt_radio_ymd.setText(_translate("MainWindow", "yyyy/mm/dd"))
        self.opt_label_date.setText(_translate("MainWindow", "Date"))
        self.opt_radio_mdy.setText(_translate("MainWindow", "mm/dd/yyyy"))
        self.opt_radio_dmy.setText(_translate("MainWindow", "dd/mm/yyyy"))
        self.opt_radio_12.setText(_translate("MainWindow", "12h AM/PM"))
        self.opt_radio_24.setText(_translate("MainWindow", "24h"))
        self.opt_label_hour.setText(_translate("MainWindow", "Hour"))
        self.opt_groupBox_save.setTitle(_translate("MainWindow", "Save the preferences"))
        self.opt_button_save.setText(_translate("MainWindow", "Save all"))
        self.opt_label_save_remind.setText(_translate("MainWindow", ""))


        self.tab_hub.setItemText(self.tab_hub.indexOf(self.tab_option), _translate("MainWindow", "Options"))
        self.tab_conv_button_convert.setText(_translate("MainWindow", "CONVERT"))
        self.tab_conv_output.setText(_translate("MainWindow", ""))
        self.tab_conv_button_clear.setText(_translate("MainWindow", "Clear"))
        self.tab_conv_label_info.setText(_translate("MainWindow", ""))
        self.tab_conv_label_amount.setText(_translate("MainWindow", "Amount"))
        self.tab_conv_label_from.setText(_translate("MainWindow", "From"))
        self.tab_conv_label_to.setText(_translate("MainWindow", "To"))
        self.tab_conv_button_copy.setText(_translate("MainWindow", "Copy"))
        self.tab_conv_button_swipe.setText(_translate("MainWindow", "< >"))
        self.tab_hub.setItemText(self.tab_hub.indexOf(self.tab_conv), _translate("MainWindow", "Currency Converter"))


        self.tab_chart_button_run.setText(_translate("MainWindow", "RUN"))
        self.tab_chart_label_time_info.setText(_translate("MainWindow", "Time infos"))
        self.tab_chart_label_started_at.setText(_translate("MainWindow", "Started at \n"
"..."))
        self.tab_chart_label_last_up.setText(_translate("MainWindow", "Last update \n"
"..."))
        self.tab_chart_label_next_up.setText(_translate("MainWindow", "Next update in\n"
"..."))
        self.tab_chart_label_last_var.setText(_translate("MainWindow", "Last variation"))
        self.tab_chart_last_var_perc.setText(_translate("MainWindow", "... %"))
        self.tab_chart_last_var_abs.setText(_translate("MainWindow", "..."))
        self.tab_chart_label_var_total.setText(_translate("MainWindow", "Total variation"))
        self.tab_chart_var_total_perc.setText(_translate("MainWindow", "... %"))
        self.tab_chart_var_total_abs.setText(_translate("MainWindow", "..."))
        self.tab_chart_min.setText(_translate("MainWindow", "..."))
        self.tab_chart_mean.setText(_translate("MainWindow", "..."))
        self.tab_chart_max.setText(_translate("MainWindow", "..."))
        self.tab_chart_label_min.setText(_translate("MainWindow", "Min"))
        self.tab_chart_label_mean.setText(_translate("MainWindow", "Mean"))
        self.tab_chart_label_max.setText(_translate("MainWindow", "Max"))
        self.tab_chart_label_last_rate.setText(_translate("MainWindow", "Last rate"))
        self.tab_chart_last_rate.setText(_translate("MainWindow", "..."))
        self.tab_chart_button_stop.setText(_translate("MainWindow", "STOP"))
        self.tab_chart_button_save.setText(_translate("MainWindow", "Save the graph"))
        self.tab_chart_button_copy.setText(_translate("MainWindow", "Copy rate values"))
        self.tab_chart_button_swipe.setText(_translate("MainWindow", "< >"))

        self.tab_hub.setItemText(self.tab_hub.indexOf(self.tab_chart), _translate("MainWindow", "Currency Chart"))
        self.main_title.setText(_translate("MainWindow", "Currency Converter"))
        self.main_status.setText(_translate("MainWindow", ""))
        self.main_time.setText(_translate("MainWindow", "Wednesday, 05/04/2021 - 12:25:14 AM"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())