# eHealth #

A set of Python applications to capture, real-time graph and process the data captured by the eHealth platform developed by Cooking-Hacks.

The current development only consider the ECG and GSR signals.

The applications include tools for post processing the data.

### Main features ###
* Serial port reading
* Fast Fourier Transform (FFT) and Low Pass filters in real time
* CSV data generation
* Heartbeat detector
* GSR average
* FFT graphics

### Dependencies ###

* Python (2.7.x)
* PySerial
* Numpy
* PyQt4
* PyQtGraph


### Ubuntu / Debian Installation ###

* Install the basic dependences using 

```
#!shell

sudo apt-get install python python-pip python-serial numpy python-qt4
```
* Install PyQtGraph library with

```
#!shell

sudo pip install pyqtgraph
```
* To develop the GUI you myust to install qt4-Designer

```
#!shell

sudo apt-get install pyqt4-dev-tools qt4-designer
```

### Mac OS X Installation ###
* Install [Anaconda Scientific Python Distribution](https://store.continuum.io/cshop/anaconda/) that comes with all the libraries
* You probably needs to install missing libraries with

```
#!shell

pip install pyserial pyqtgraph
```