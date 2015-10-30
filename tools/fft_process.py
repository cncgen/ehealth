## fft_process.py 
#   
# Process a CSV file applying the FFT and a Low-Pass filter 
#
# This filter is used to eliminate electrical noise and static from signal data
#
# Usage: python fft_process.py [input_file] [output_file] [cut_frequency]
# 
# @param input_file The file in CSV format to be processed
# @param output_file The file in CSV format processed
# @param cut_frequency Frequency to apply the low-pass filter
#
# @note Data must be in CSV file in format: time,ecg,gsr

import sys
import numpy, scipy, pylab, random  
import re

if len(sys.argv) != 4:
	print "Process a CSV file applying the FFT and a Low-Pass filter\n"
	print "Usage: python " + sys.argv[0] + " [input_file] [output_file] [cut_frequency]\n"
	print ("Where\n   input_file:    Input data file in CSV format\n" +
		"   output_file:   Output data file in CSV format\n" +
		"   cut_frequency: Cut frequency for low-pass filter\n")
	print "Example: python " + sys.argv[0] + " ../data/sample.csv ../data/output.csv 110\n"
	exit(1)

time = []
signal1 = []
signal2 = []

try:

	reader = open(sys.argv[1],"r")
	arch = open(sys.argv[2],"w")
	cut_frequency = int(sys.argv[3])
	c = 0
	print "Processing file: " + sys.argv[1] 
	print "Cut frequency: " + str(cut_frequency)
	print "Output file: " + sys.argv[2]

	linear = reader.readline()
	while linear!="":
		row = re.split(r'[;,\s]\s*', linear)
		data0 = row[0]
		data1 = row[1]
		data2 = row[2]

		if (data0 <> "" and data1 <> "" and data2<> ""):
			time.append(data0)
			signal1.append(float(data1.rstrip()))	
			signal2.append(float(data2.rstrip()))
			c = c + 1
			if (c == 300000):
				# Process the ecg data
				fft1=scipy.fft(signal1)
				pecg=fft1[:]  
				for i in range(len(pecg)):  
					if i>=cut_frequency:
						pecg[i]=0
  
				ecg=scipy.ifft(pecg)

				# Process the gsr data
				fft2=scipy.fft(signal2)
				pgsr=fft2[:]  
				for i in range(len(pgsr)):  
					if i>=cut_frequency:
						pgsr[i]=0
  
				gsr=scipy.ifft(pgsr)
				
				# Generate the output file
				for i in range(len(time)):
					linea = str(time[i]) + "," + str(float(ecg[i])) + "," + str(float(gsr[i]))
					#linea = str(time[i]) + "," + str(float(ecg[i])) + ", 0.3"
					arch.write(linea + "\n")
		
				del time[:]
				del signal1[:]
				del signal2[:]
				del pecg
				del ecg
				del pgsr
				del gsr
				c = 0
		else:
			print("Error processing the file: data0: " + data0 + " | data1: " + data1)
		linear = reader.readline()
	arch.close()
except Exception,e:
	print(e)
	print("Error processing the file: data0: " + data0 + " | data1: " + data1)
