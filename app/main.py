#!/usr/bin/env python

## eHealth - Main program to control the gui and the data adquisition
#
# Python application to capture data from Cooking-Hacks eHealth Platform 
# https://www.cooking-hacks.com/documentation/tutorials/ehealth-biometric-sensor-platform-arduino-raspberry-pi-medical
#
# Modified by Jose Zorrilla <jzorrilla@x-red.com> to graph in realtime and process the data using FFT and LowPass Filters
#
# Based on the Open Source RTGraph library by Sebastian Sepulveda https://github.com/ssepulveda/RTGraph
#
# @note To execute: # python main.py
#

import sys
from gui import *
from serialProcess import SerialProcess
from multiprocessing import Queue
from collections import deque
from csvExport import CSVExport
from serialPorts import getSerialPorts
from log import Log

import numpy, scipy, pylab, random



##
# @brief Buffer size for the data (number of points in the plot)
N_SAMPLES = 4096
##
# @brief Update time of the plot, in ms
PLOT_UPDATE_TIME = 30
##
# @brief Point to update in each redraw
PLOT_UPDATE_POINTS = -256


##
# @brief Managing and plotting acquired data
# @param QtGui.QMainWindow Qt4 Main Window reference
class MainWindow(QtGui.QMainWindow):
    ##
    # @brief Configures initial settings of the window.
    # Initialize data, plots, imported functions and timers
    # @param self Object handler
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initializes plots
        self.ui.plt.setBackground(background=None)
        self.ui.plt.setAntialiasing(True)
        self.plt1 = self.ui.plt.addPlot(row=1, col=1)
	self.plt2 = self.ui.plt.addPlot(row=2, col=1)

        # Variables
        self.queue = Queue(N_SAMPLES)
        self.data = None
        self.csv = None
        self.DATA0 = deque([], maxlen=N_SAMPLES)
	self.DATA1 = deque([], maxlen=N_SAMPLES)
        self.TIME = deque([], maxlen=N_SAMPLES)
        self.reset_buffers()

        ##
        # @brief Reference update plot timer
        # Qt4 timer to trigger the @updatePlot function
        self.timer_plot_update = QtCore.QTimer(self)

        self.timer_freq_update = QtCore.QTimer(self)

        # Qt signals and slots
        QtCore.QObject.connect(self.ui.pButton_Start,
                               QtCore.SIGNAL('clicked()'), self.start)
        QtCore.QObject.connect(self.ui.pButton_Stop,
                               QtCore.SIGNAL('clicked()'), self.stop)
        QtCore.QObject.connect(self.timer_plot_update,
                               QtCore.SIGNAL('timeout()'), self.update_plot)
        QtCore.QObject.connect(self.timer_freq_update,
                               QtCore.SIGNAL('timeout()'), self.update_freq)

        # Configure UI
        ports = getSerialPorts()
        if len(ports) <= 0:
            ans = QtGui.QMessageBox.question(self,
                                             "No device detected",
                                             "Connect a serial device.\n" +
                                             "Scan again?",
                                             QtGui.QMessageBox.Yes,
                                             QtGui.QMessageBox.No)
            if ans == QtGui.QMessageBox.Yes:
                ports = getSerialPorts()
        self.ui.cBox_Port.addItems(ports)
        self.ui.cBox_Speed.addItems(["9600", "57600", "115200"])
        self.ui.cBox_Speed.setCurrentIndex(2)
        self.set_ui_locked(False)
	
        # Configure two plots: ECG and GSR
        self.configure_plot(self.plt1, "ECG", "")
	self.configure_plot(self.plt2, "GSR", "")

    ##
    # @brief Start SerialProcess for data acquisition
    # @param self Object handler
    def start(self):
        self.data = SerialProcess(self.queue)
        # Select serial port configuration form ui
        self.data.openPort(str(self.ui.cBox_Port.currentText()),
                           int(self.ui.cBox_Speed.currentText()))

        if self.data.start() is False:
            QtGui.QMessageBox.question(self,
                                       "Can't open Serial Port",
                                       "Serial port is already opened.",
                                       QtGui.QMessageBox.Ok)
        else:
            # start CSV data export if enabled
            if self.ui.chBox_export.isChecked():
                # export data
                self.csv = CSVExport(self.ui.file_export.text())
                self.ui.statusbar.showMessage("Exporting data to session " + self.ui.file_export.text())
            else:
                self.ui.statusbar.showMessage("Acquiring data")
            # start data process, lock the ui and set plot update time
            self.set_ui_locked(True)
            self.timer_plot_update.start(PLOT_UPDATE_TIME)
            self.timer_freq_update.start(PLOT_UPDATE_TIME*10)

    ##
    # @brief Updates graphs and writes to CSV files if enabled
    # @param self Object handler
    def update_plot(self):
        # Get data from buffer
        while self.queue.qsize() != 0:
            data = self.queue.get(True, 1)
            self.TIME.append(data[0])
            self.DATA0.append((float(data[1]*5/1023)))
	    self.DATA1.append((float(data[2]*5/1023)))
            # If enabled, write to log file
            if self.ui.chBox_export.isChecked():
                self.csv.csvWrite(data)
	
	# Apply the filter to ECG signal to reduce the noise
	# Cut frequency is 110
	fft=scipy.fft(self.DATA0)   
	pecg=fft[:]  
	for i in range(len(pecg)):
		if i>=110:pecg[i]=0
		
	ecg=scipy.ifft(pecg)

	# Apply the filter to GSR signal to reduce the noise
	# Cut frequency is 110
	fft2=scipy.fft(self.DATA1)   
	pgsr=fft2[:]  
	for i in range(len(pgsr)):
		if i>=110:pgsr[i]=0
		
	gsr=scipy.ifft(pgsr)

        # Draw new data
        self.plt1.clear()
        self.plt1.plot(x=list(self.TIME)[-PLOT_UPDATE_POINTS:], y=list(abs(ecg))[-PLOT_UPDATE_POINTS:], pen='#2196F3')
	self.plt2.clear()
        self.plt2.plot(x=list(self.TIME)[-PLOT_UPDATE_POINTS:], y=list(abs(gsr))[-PLOT_UPDATE_POINTS:], pen='#2196F3')

    def update_freq(self):
        # Show adquisition frequency
        self.ui.statusbar.showMessage("Sampling at " + str(1/(self.TIME[-1] - self.TIME[-2])) + " Hz : T = " + str(self.TIME[-1] - self.TIME[-2]))

    ##
    # @brief Stops SerialProcess for data acquisition
    # @param self Object handler
    def stop(self):
        self.data.closePort()
        self.data.join()
        self.timer_plot_update.stop()
        self.timer_freq_update.stop()
        self.set_ui_locked(False)
        self.reset_buffers()
        self.ui.statusbar.showMessage("Stopped data acquisition")

    ##
    # @brief Basic configurations for a plot
    # @param self Object handler
    # @param plot Plot to be customized
    # @param title Title for the plot
    # @param unit Unit for the plot
    # @param plot_range List with min and max values to show in the plot
    @staticmethod
    def configure_plot(plot, title, unit, y_min=0, y_max=0,
                       label_color='#219600', label_size='11pt'):
        label_style = {'color': label_color, 'font-size': label_size}
        plot.setLabel('left', title, unit, **label_style)
        plot.setLabel('bottom', 'Time', 's', **label_style)
        plot.showGrid(x=False, y=True)
        if y_min != y_max:
            plot.setYRange(y_min, y_max)
        else:
            plot.enableAutoRange(axis=None, enable=True)
        plot.setMouseEnabled(x=False, y=False)

    ##
    # @brief Basic configurations for a plot
    # @param self Object handler
    # @param enabled Sets the ui locked
    def set_ui_locked(self, enabled):
        self.ui.pButton_Stop.setEnabled(enabled)
        self.ui.pButton_Start.setEnabled(not enabled)
        self.ui.cBox_Port.setEnabled(not enabled)
        self.ui.cBox_Speed.setEnabled(not enabled)
        self.ui.chBox_export.setEnabled(not enabled)

    ##
    # @brief Clears the buffers
    # @param self Object handler
    def reset_buffers(self):
        self.DATA0.clear()
	self.DATA1.clear()
        self.TIME.clear()

    ##
    # @brief Function to be executed while closing the main window
    # @param self Object handler
    # @param event Event who calls the exit
    def closeEvent(self, event):
        log.i('Starting close')
        try:
            if self.data.is_alive():
                log.w('SerialProcess running, stopping it')
                self.stop()
        except:
            pass
        app.exit()
        sys.exit()

if __name__ == "__main__":
    # configuring log
    log = Log('main')
    if '-v' in sys.argv:
        log.level('INFO')
    elif '-vv' in sys.argv:
        log.level('DEBUG')
    else:
        log.level('ERROR')

    log.i('Starting Application')
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    app.exec_()
