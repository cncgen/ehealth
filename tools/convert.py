## convert.py 
#   
# Convert csv raw data from Arduino (0-1023) to volts values
#
#
# Usage: python convert.py [input file] [output file]
#
# @note Data must be in CSV file in format: time,ecg,gsr

import sys
import csv
import datetime
import re

if len(sys.argv) != 3:
	print "Convert csv raw data from Arduino (0-1023) to Volts\n"
	print "Usage: python " + sys.argv[0] + " [input file] [output file]\n"
	exit(1)

fileinput = open(sys.argv[1],"r")
fileoutput = open(sys.argv[2],"w")
linea = fileinput.readline()
i =0
while (linea!=""):
	row = re.split(r'[;,\s]\s*', linea)
	time = row[0]
	ecg = row[1]
	gsr = row[2]
	fileoutput.write(time + "," + str(float(ecg)*5/1023) + "," + str(float(gsr)*5/1023) + "\n")
	linea = fileinput.readline()
	i=i+1

fileinput.close()
fileoutput.close()

