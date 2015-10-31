# eHealth #

A set of Python applications to capture, real-time graph and process the data captured by the eHealth platform developed by Cooking-Hacks.

The current development only consider the ECG and GSR signals and is based on the [RTGraph library](https://github.com/ssepulveda/RTGraph).

The applications include tools for post processing the data.

## Main features ##
* Serial port reading
* Fast Fourier Transform (FFT) and Low Pass filters in real time
* CSV data generation
* Heartbeat detector
* GSR average
* FFT graphics

## Dependencies ##

* Python (2.7.x)
* PySerial
* Numpy
* PyQt4
* PyQtGraph


## Ubuntu / Debian Installation ##

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
* You probably need to install missing libraries with

```
#!shell

pip install pyserial pyqtgraph
```
## Collecting Data ##

To collect data is used the application eHealth. The application capture the data trough the serial port. To execute the application use the command


```
#!python

./run
```


or 

```
#!python


python ./app/main.py
```

The application running show this interface

![eHealth.png](https://bitbucket.org/repo/LLq89d/images/2219354141-eHealth.png)

The buttons Star and Stop control the process of collecting data. To store the data the check box "Export to CSV" must be on. If required, the data can be tagged using the parameter "Session Name".

All the data collected is saved in the folder data.

## Post Processing ##

### Convert ###
This program allow to convert the raw data from the Arduino board to volts. 

Usage: python ./tools/convert.py [input file] [output file]

### Correlation ###
This program allow to compare two signals in order to see if are correlated

An example can be executed whit the command


```
#!python

./correlation_example
```

The example will show several graph with the process and with the correlation index

![correlation_example.png](https://bitbucket.org/repo/LLq89d/images/906864467-correlation_example.png)

### Extract features ###

The program extract.py allow to extract the features of the signal.

To execute the example use the commnad


```
#!python

./extract_sample
```

The example will show the heartbeat and the gsr average, also show a graph with red points to show how the feature was calculated.

![extract.png](https://bitbucket.org/repo/LLq89d/images/90539312-extract.png)


### Noise Filter Examples ###

The program fft_graph.py allow to calculate the cut frequency to apply a low-pass filter. 

To execute the examples use

```
#!python


./gsr_filter_example
```

![gsr_filter_example.png](https://bitbucket.org/repo/LLq89d/images/4139244647-gsr_filter_example.png)


```
#!python

./ecg_noise_filter_example
```
![ecg_noise_filter_example.png](https://bitbucket.org/repo/LLq89d/images/3670828227-ecg_noise_filter_example.png)


### Noise Filter Process ###

The program fft_process.py  allow to process a signal applying the low-pass filter. 

```
#!python


Usage: python ./tools/fft_process.py [input_file] [output_file] [cut_frequency]
```


Where

   input_file:    Input data file in CSV format

   output_file:   Output data file in CSV format

   cut_frequency: Cut frequency for low-pass filter