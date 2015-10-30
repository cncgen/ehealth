## correlation.py 
#   
# Process and graph two signals and calculate the correlation factor between them 
#
#
# Usage: python correlation.py [input_file_1] [input_file_2]
# 
# @param input_file_1 The file with low sample frequency 
# @param input_file_2 The file with high sample frequency
#


import sys
import csv
import re
import numpy, scipy, pylab, random 

from scipy.stats.stats import pearsonr 

import numpy as np

from scipy.signal import resample

if len(sys.argv) != 3:
	print "Calculate the correlation factor between two data files\n"
	print "Usage: python " + sys.argv[0] + " [input_file_1] [input_file_2]\n"
	print ("Where\n   input_file_1: The file with low sample frequency\n" +
		"   input_file_2: The file with high sample frequency\n")
	print "Example: python " + sys.argv[0] + " ../data/biopac.csv ../data/ehealth.csv\n"
	exit(1)

# Create the list for store the signals

signal1 = []
signal2 = []

try:
	# Read the singal 1

	reader = open(sys.argv[1],"r")
	linea = reader.readline()
	s1=0
	while (linea!=""):
		row = re.split(r'[;,\s]\s*', linea)
		signal1.append(float(row[1].rstrip()))
		s1=s1+1
		linea = reader.readline()
	reader.close()

	# Read  the signal 2
	reader = open(sys.argv[2],"r")
	linea = reader.readline()
	s2=0
	while (linea!=""):
		row = re.split(r'[;,\s]\s*', linea)
		signal2.append(float(row[2].rstrip()))
		s2=s2+1
		linea = reader.readline()
	reader.close()
	
	# Generate the graphs
	h,w=2,2  
	pylab.figure(figsize=(12,6))  
	pylab.subplots_adjust(hspace=.9)  

  
	pylab.subplot(h,w,1);pylab.title("(A) GSR Biopac")  
	pylab.plot(signal1)   

	pylab.subplot(h,w,2);pylab.title("(B) GSR eHealth")  
	pylab.plot(signal2) 

	# Create the temp signals to apply the correlation using the function pearsonr
	# Signal 2 is interpolated
	signal2_tmp = numpy.interp(np.arange(0, len(signal2), round((s2/s1),4)), np.arange(0, len(signal2)), signal2)
	# Signal 1 is resampled
	signal1_tmp = resample(signal1,len(signal2_tmp))
	# Calculate the correlation
	corr = round(pearsonr(signal1_tmp,signal2_tmp)[0],4)

	# Graph the data resampled
	pylab.subplot(h,w,3);pylab.title("(C) GSR Biopac Interpolation")  
	pylab.plot(signal1_tmp)  

	# Graph the data interpolated and the correlation factor
	pylab.subplot(h,w,4);pylab.title("(D) GSR eHealth - Correlation : " + str(corr))  
	pylab.plot(signal2_tmp)   

	pylab.show()

except Exception,e:
	print(e)
