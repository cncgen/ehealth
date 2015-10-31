## fft_graph.py 
#   
# Graph data and apply the FFT in order to analize and find the cut frequency 
# for the low-pass filter.
#
# This filter is used to eliminate electrical noise and static from signal data
#
# Usage: python fft_graph.py [input_file] [data] [cut_frequency]
# 
# @param input_file The file to be analysed
# @param data The data column from the file
# @param cut_frequency Frequency to apply the low-pass filter
# @param data The number of samples to be analysed
#
# @note Data must be in CSV file in format: time,ecg,gsr

import sys
import csv
import numpy, scipy, pylab, random  
import re

if len(sys.argv) != 4 and len(sys.argv) != 5:
	print "Graph data and apply the FFT and Low-Pass filter\n"
	print "Usage: python " + sys.argv[0] + " [input_file] [data] [cut_frequency] [samples]\n"
	print ("Where\n   input_file:    Input data in CSV format\n" +
		"   data:          Data column to be analyzed\n" +
		"   cut_frequency: Cut frequency for low-pass filter\n"
		"   samples:        Number of samples to be analysed (default = 4000)\n")
	print "Example: python " + sys.argv[0] + " ../data/sample.csv 1 110\n"
	exit(1)


# Default buffer size or sample parameter 
if len(sys.argv) == 5:
	size = int(sys.argv[4])
else:
	size = 4000

signal=numpy.arange(0,size/100 + .01,.01)


# Read the input data
reader = open(sys.argv[1],"r")
linea = reader.readline()
i =0
while (linea!="") and (i <=size):
	row = re.split(r'[;,\s]\s*', linea)
	signal[i] = row[int(sys.argv[2])]
	i=i+1
	linea = reader.readline()


# Define the cut frequency
cut_frequency=int(sys.argv[3])

# Calculate the FFT
fft=scipy.fft(signal)   
bp=fft[:] 

# Apply the Low-Pass filter 
for i in range(len(bp)):  
	if i>=cut_frequency:
		bp[i]=0		

#Calculate the inverse FFT 
ibp=scipy.ifft(bp)   
 
# Generate the graphs

h,w=3,2  
pylab.figure(figsize=(12,6))  
pylab.subplots_adjust(hspace=.9)  

  
pylab.subplot(h,w,1);pylab.title("(A) Raw Signal")  
pylab.plot(signal)   

pylab.subplot(h,w,2);pylab.title("(B) FFT")  
fft=scipy.fft(signal)  
pylab.plot(abs(fft))  
pylab.axis([0,500,0,100]) 
  
pylab.subplot(h,w,3);pylab.title("(C) Low-Pass FFT")  
pylab.plot(abs(fft))   
pylab.axvspan(cut_frequency,10000,fc='r',alpha=0.5)  
pylab.axis([0,500,0,100])  
  
pylab.subplot(h,w,4);pylab.title("(D) Inverse FFT")  
pylab.plot(ibp)  
  
pylab.subplot(h,w,5);pylab.title("(E) Signal vs. iFFT")  
pylab.plot(signal,'k',label="signal",alpha=0.5)  
pylab.plot(ibp,'b',label="ifft",alpha=0.5)  
  
pylab.subplot(h,w,6);pylab.title("(F) Normalized Signal vs. iFFT")  
pylab.plot(signal/max(signal),'k',label="signal",alpha=0.5)  
pylab.plot(ibp/max(ibp),'b',label="ifft",alpha=0.5)   

# Save the graph to a png file  
pylab.savefig("fft_graph.png",dpi=200)  
pylab.show()  
