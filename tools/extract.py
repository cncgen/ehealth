## extract.py 
#   
# Find the ECG heartbeat frequency and GSR average
#
# Plot the ECG in order to verify the result and calibrate the delta value
#
# Usage: python extract.py [file] [delta]
#
# @note Data must be in CSV file in format: time,ecg,gsr

import sys
import numpy
from numpy import NaN, Inf, arange, isscalar, asarray, array
import re

## function [maxtab, mintab]=peakdet(v, delta, x)
#   
#  Finds the local maxima and minima peaks in the vector v
#  The local is defined by delta value
#
#  With x parameter the indices in maxtab and mintab are replaced
#  with the corresponding x-values.
#
#  The out put are to arrays with maximun and minimun values
#  maxtab and mintab consists of two columns, columns 1 contains
#  indices in v and column 2 contains the maximun or minimu value 
#  in that index
#

def peakdet(v, delta, x = None):

    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

if __name__=="__main__":
    from matplotlib.pyplot import plot, scatter, show, legend

    if len(sys.argv) != 3:
	print "Usage: python " + sys.argv[0] + " [file] [delta]\n"
	exit(1)
    
    size = 50000

    signal=numpy.arange(0,size/100 + .01,.01)
    reader = open(sys.argv[1],"r")
    linea = reader.readline()
    i = 0
    sumgsr = 0
    while (linea!="") and (i <=size):
	row = re.split(r'[;,\s]\s*', linea)
	signal[i] = row[1]
	sumgsr = sumgsr + float(row[2])
	i=i+1
	linea = reader.readline()

    maxtab, mintab = peakdet(signal,float(sys.argv[2]))

    time_now = 0
    time_old = 0
    max_diff = 0
    diff = 0
    suma = 0

    for index,row in enumerate(maxtab):

	time_now = row[0]
	if (time_old <> 0 ):
		diff = long(time_now) - long(time_old)
		#print diff
		suma = suma + diff
	
	time_old = time_now

    heartbeat = str(suma/(len(maxtab)-1)*0.065)
    gsravg = str(round((sumgsr/i),4))	

    plot(signal, label="HeartBeat AVG: " + heartbeat + " | GSR AVG: " + gsravg)
    legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

    scatter(array(maxtab)[:,0], array(maxtab)[:,1], color='red')
    scatter(array(mintab)[:,0], array(mintab)[:,1], color='blue')
    #self.savefig("plot_2.png")
    show()
    
    
