"""
Sublinear algorithm for detecting voltage sags

@author Omid Ardakanian (ardakanian@berkeley.edu)
"""

from btrdbutil import *

threshold = 0.10 # detecting voltage sag

startTime = "2015-01-01T00:00:00"
endTime   = "2015-08-01T00:00:00"

pathStream1 = "/upmu/psl_alameda/L1MAG"
pathStream2 = "/upmu/psl_alameda/L2MAG"
pathStream3 = "/upmu/psl_alameda/L3MAG"

btrdb_wrapper = BTrDBWrapper()
visitor = MinMeanAbsDiffAboveThreshold()

searchTree1 = BTrSearch(btrdb_wrapper, pathStream1)
baseVoltage = searchTree1.find_mean(startTime, endTime)
searchTree1.accept(visitor)
vsagStartsL1, pw = searchTree1.multi_resolution_search(startTime, endTime, threshold*baseVoltage)

searchTree2 = BTrSearch(btrdb_wrapper, pathStream2)
searchTree2.accept(visitor)
vsagStartsL2, _  = searchTree1.multi_resolution_search(startTime, endTime, threshold*baseVoltage)

searchTree3 = BTrSearch(btrdb_wrapper, pathStream3)
searchTree3.accept(visitor)
vsagStartsL3, _  = searchTree1.multi_resolution_search(startTime, endTime, threshold*baseVoltage)

allcases = list(set(vsagStartsL1) | set(vsagStartsL2) | set(vsagStartsL3))
print len(allcases)

for st in allcases:
    plot_3phase_voltage_rawdata(btrdb_wrapper.get_rawdata(pathStream1, st, pw),btrdb_wrapper.get_rawdata(pathStream2, st, pw),btrdb_wrapper.get_rawdata(pathStream3, st, pw),baseVoltage)
