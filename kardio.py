# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kardio.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph.ptime import time
import sys, serial, glob, os, datetime
import numpy as np
import peakutils

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class Ui_Kardio(object):
    def __init__(self):
        self.CONNECTED = False
        self.SERIAL = False
        self.READING = False
        self.RECORD = False
        self.MAX_VOLTAGE = 5.0
        self.indices = []
        self.recorded_data = []
        
    def setupUi(self, Kardio):
        Kardio.setObjectName("Kardio")
        Kardio.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Kardio.sizePolicy().hasHeightForWidth())
        Kardio.setSizePolicy(sizePolicy)
        Kardio.setMinimumSize(QtCore.QSize(800, 600))
        Kardio.setMaximumSize(QtCore.QSize(800, 600))
#        Kardio.setStyleSheet("QMainWindow {background: 'gray';}")
        self.centralwidget = QtWidgets.QWidget(Kardio)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(510, 0, 281, 51))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(0, 20, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('color: green;}')
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(110, 20, 168, 32))
        self.comboBox.setObjectName("comboBox")
#        pg.setConfigOption('background', 'w')
        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(15, 71, 771, 471))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setLabel('bottom', 'Time', units='s')
        self.graphicsView.setLabel('left', 'Voltage', units='V')
        self.graphicsView.setBackground('w')
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(599, 69, 181, 91))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(20, 30, 60, 16))
        self.label.setText("")
        self.label.setObjectName("label")
        self.BPM_counter = QtWidgets.QLabel(self.groupBox_2)
        self.BPM_counter.setGeometry(QtCore.QRect(10, 30, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(60)
        self.BPM_counter.setFont(font)
        self.BPM_counter.setObjectName("BPM_counter")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(120, 65, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 0, 471, 51))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet('color: green;}')
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_3)
        self.plainTextEdit.setGeometry(QtCore.QRect(240, 22, 221, 25))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.overwriteMode()
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(120, 20, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet('color: green;}')    
        Kardio.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Kardio)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        Kardio.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Kardio)
        self.statusbar.setObjectName("statusbar")
        Kardio.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(Kardio)
        QtCore.QMetaObject.connectSlotsByName(Kardio)
        
        self.pushButton.clicked.connect(self.serialConnect)
        self.comboBox.activated.connect(self.serialFind)
        self.pushButton_2.clicked.connect(self.readData)
        
        self.pushButton_3.clicked.connect(self.recordData)
        
        savefilepath = self.getNextFile()
        self.plainTextEdit.insertPlainText(savefilepath)
        
        
        self.SAMPLING_RATE = 100 # Sampling rate of serial data (100 Hz)

    def getNextFile(self):
        files = glob.glob(os.curdir + '/rawData_%s_[^0-9]*.dat'%datetime.date.today())
        if len(files) == 0:
            N = 1
        else:
            N = np.max([int(i.split('.dat')[0].split('_')[-1]) for i in files]) + 1
        return os.curdir + '/rawData_%s_%s.dat'%(datetime.date.today(), N)

    def retranslateUi(self, Kardio):
        _translate = QtCore.QCoreApplication.translate
        Kardio.setWindowTitle(_translate("Kardio", "MainWindow"))
        self.groupBox.setTitle(_translate("Kardio", "Serial Connection"))
        self.pushButton.setText(_translate("Kardio", "Connect"))
        self.groupBox_2.setTitle(_translate("Kardio", "Heart Rate"))
        self.label_3.setText(_translate("Kardio", "BPM"))
        self.groupBox_3.setTitle(_translate("Kardio", "Data Streaming"))
        self.pushButton_2.setText(_translate("Kardio", "Start"))
        self.pushButton_3.setText(_translate("Kardio", "Record"))
        self.menuSettings.setTitle(_translate("Kardio", "Settings"))
        if self.CONNECTED == False:
            self.serialFind()
        
    def serialFind(self):
        # Delete all items in ports list
        items = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]
        for i in range(len(items)):
            
            self.comboBox.removeItem(i)
        # Add back available items to ports list
        ports = serial_ports()
        self.comboBox.addItems(ports)
        return False
    
    def serialConnect(self, baud=9600):
        _translate = QtCore.QCoreApplication.translate
        if self.CONNECTED == False:
            # Open serial port
            port = self.comboBox.currentText()
            self.SERIAL = serial.Serial(port, baud)
            self.CONNECTED = True
            self.comboBox.setEnabled(False)
            self.pushButton.setText(_translate("MainWindow", 'Disconnect'))
            self.pushButton.setStyleSheet('color: red;}')
        else:
            # Close serial port
            self.SERIAL.close()
            self.pushButton.setText(_translate("MainWindow", 'Connect'))
            self.pushButton.setStyleSheet('color: green;}')
            self.CONNECTED = False
            self.comboBox.setEnabled(True)
        return False
    
    def recordData(self):
        _translate = QtCore.QCoreApplication.translate
        if len(self.recorded_data) != 0 and self.RECORD == True:
            self.pushButton_3.setText(_translate("Kardio", "Recording..."))
            self.pushButton_3.setStyleSheet('color: red;}')
            self.writeData()
            self.RECORD = False
            savefilepath = self.getNextFile()
            self.plainTextEdit.clear()
            self.plainTextEdit.insertPlainText(savefilepath)
          
        elif self.READING == True:
            self.pushButton_3.setText(_translate("Kardio", "Record"))
            self.pushButton_3.setStyleSheet('color: green;}')
            self.RECORD = True
            
        # Clear recording buffer
        self.recorded_data = []
        return False
    
    def writeData(self):
        with open(self.plainTextEdit.toPlainText(), 'w') as datafile:
            # Write header w/ settings
            datafile.write('###\n')
            datafile.write('# OLIMEX SHIELD-EKG-EMG Data Recording\n')
            datafile.write('# Writtent by: Daniel C. Sweeney (v0.1)\n')
            datafile.write('# Filename: %s\n'%self.plainTextEdit.toPlainText()) 
            datafile.write('# Sampling Rate: %s Hz\n'%self.SAMPLING_RATE) 
            datafile.write('# No. Samples: %s\n'%len(self.recorded_data))
            datafile.write('# Date: %s\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            datafile.write('###\n')
            
            # Write data
            for i in self.recorded_data:
                datafile.write('%s\n'%i)
        return False

    def update(self, BUFFERLEN = 250):
        line = self.SERIAL.readline()
        self.data.append(int(line)/1024.*self.MAX_VOLTAGE)
        if len(self.data) > BUFFERLEN:
            if self.RECORD == True:
                self.recorded_data.append(self.data[-1])
            self.data.pop(0)
        times = np.linspace(0, 
                            len(self.data)/self.SAMPLING_RATE, 
                            len(self.data))
        xdata = np.array(self.data, dtype='float64')
        self.curve.setData(times, xdata)
        app.processEvents()
        if self.READING == True:
            self.peakDetection()
        return False
    
    def readData(self):
        _translate = QtCore.QCoreApplication.translate
        if self.READING == False:
            self.graphicsView.clear()
            self.curve = self.graphicsView.plot(pen = pg.mkPen('r', width=3))
            self.data = [0]
            self.SERIAL.close()
            self.SERIAL.open()
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(0)
            self.READING = True
            self.pushButton_2.setText(_translate("Kardio", "Stop"))
            self.pushButton_2.setStyleSheet('color: red;}')
            self.plainTextEdit.setEnabled(False)
            
        else:
            self.timer.stop()
            self.READING = False
            self.pushButton_2.setText(_translate("Kardio", "Start"))
            self.pushButton_2.setStyleSheet('color: green;}')
            self.plainTextEdit.setEnabled(False)
        return False
    
    def peakDetection(self):
        _translate = QtCore.QCoreApplication.translate
        offset = np.mean(self.data)
        data_norm = np.divide(self.data, self.MAX_VOLTAGE)
        self.indices.append(len(peakutils.indexes(data_norm, 
                                              thres=0.75, 
                                              min_dist=0.01)))
        if len(self.indices) > 500:
            self.indices.pop(0)
        bpm = np.mean(self.indices)*self.SAMPLING_RATE/(len(self.data)/60.0)
        print(bpm)
        self.BPM_counter.setText(_translate("Kardio", '%3.0f'%bpm))
        return False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Kardio = QtWidgets.QMainWindow()
    ui = Ui_Kardio()
    ui.setupUi(Kardio)
    Kardio.show()
    sys.exit(app.exec_())

