#!/usr/bin/env python

## Class to Export data in CSV format
#
# Export data using date and time as name for the file, avoiding overwriting
# data in differents adquisitions.
#
# It also registers in the first colummn the elapsed since the first
# adquisition
#
# @note The data is stored in a "data" folder

from time import strftime, gmtime
from datetime import datetime
import csv
from gui import *

class CSVExport:
    ##
    # @brief Constructor
    # Gets a tag and create the filename and open the file for data adquisition
    #
    # @param txt A tag to identify the file for post processing
    # @note The filename format is Year-Moth-Day_Hours-minutes-seconds.csv
    def __init__(self,txt):
        self.name = strftime("data/%Y-%m-%d_%H-%M-%S_" + str(txt) + ".csv", gmtime())
        FILE = open(self.name, "wb")
        self.CSV = csv.writer(FILE)

    ## Writes a new line of data
    #
    # @param self The object pointer
    # @param txt The data to export
    def csvWrite(self, txt):
        self.CSV.writerow(txt)
