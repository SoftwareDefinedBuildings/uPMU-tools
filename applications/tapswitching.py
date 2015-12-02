"""
Sublinear algorithm for detecting tap switching events

@author Omid Ardakanian (ardakanian@berkeley.edu)
"""

from btrdbutil.btrdbwrapper import *
from btrdbutil.btrsearch import *
from btrdbutil.plotter import *

threshold = 0.005 # detecting voltage sag

startTime = "2015-01-01T00:00:00"
endTime   = "2015-08-01T00:00:00"

distillate1 = "/Production/psl_alameda/L1MAG-MA"
distillate2 = "/Production/psl_alameda/L2MAG-MA"
distillate3 = "/Production/psl_alameda/L3MAG-MA"

pathStream1 = "/upmu/psl_alameda/L1MAG"
pathStream2 = "/upmu/psl_alameda/L2MAG"
pathStream3 = "/upmu/psl_alameda/L3MAG"

btrdb_wrapper = BTrDBWrapper()
visitor = MinMeanMaxMeanRatioComparator()

searchTree1 = BTrSearch(btrdb_wrapper, distillate1)
baseVoltage = searchTree1.find_mean(startTime, endTime)
searchTree1.accept(visitor)
vchangeStarts1, pw = searchTree1.multi_resolution_search(startTime, endTime, 'Voltage', threshold)

searchTree2 = BTrSearch(btrdb_wrapper, distillate2)
searchTree2.accept(visitor)
vchangeStarts2, _  = searchTree2.multi_resolution_search(startTime, endTime, 'Voltage', threshold)

searchTree3 = BTrSearch(btrdb_wrapper, distillate3)
searchTree3.accept(visitor)
vchangeStarts3, _  = searchTree3.multi_resolution_search(startTime, endTime, 'Voltage', threshold)

allcases = list(set(vchangeStarts1) | set(vchangeStarts2) | set(vchangeStarts3))
print len(allcases)

for st in allcases:
    plot_3phase_voltage_rawdata(btrdb_wrapper.get_rawdata(pathStream1, st, pw),btrdb_wrapper.get_rawdata(pathStream2, st, pw),btrdb_wrapper.get_rawdata(pathStream3, st, pw),baseVoltage)
