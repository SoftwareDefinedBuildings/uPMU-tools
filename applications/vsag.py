"""
Sublinear algorithm for detecting voltage sags

@author Omid Ardakanian (ardakanian@berkeley.edu)
"""

from btrdbutil.btrdbwrapper import *
from btrdbutil.btrsearch import *
from btrdbutil.plotter import *

threshold = 0.10 # detecting voltage sag

# UTC time -> to get local time -08:00 if PST, -07:00 if PDT
startTime = "2015-08-01T00:00:00"
endTime   = "2015-10-15T21:00:00"

pathStream1 = "/upmu/RPU/Hunter_1224/L1MAG"
pathStream2 = "/upmu/RPU/Hunter_1224/L2MAG"
pathStream3 = "/upmu/RPU/Hunter_1224/L3MAG"

btrdb_wrapper = BTrDBWrapper()
visitor = MinMeanDiffComparator()

searchTree1 = BTrSearch(btrdb_wrapper, pathStream1)
searchTree1.accept(visitor)

baseVoltage = searchTree1.find_mean(startTime, endTime)
print "The estimated nominal voltage is "+str(baseVoltage)+"V"
vsagStartsL1, pw = searchTree1.multi_resolution_search(startTime, endTime, threshold*baseVoltage)

searchTree2 = BTrSearch(btrdb_wrapper, pathStream2)
searchTree2.accept(visitor)
vsagStartsL2, _  = searchTree2.multi_resolution_search(startTime, endTime, threshold*baseVoltage)

searchTree3 = BTrSearch(btrdb_wrapper, pathStream3)
searchTree3.accept(visitor)
vsagStartsL3, _  = searchTree3.multi_resolution_search(startTime, endTime, threshold*baseVoltage)

allcases = list(set(vsagStartsL1) | set(vsagStartsL2) | set(vsagStartsL3))
print len(allcases)

for st in allcases:
    plot_3phase_voltage_rawdata(btrdb_wrapper.get_rawdata(pathStream1, st, pw),btrdb_wrapper.get_rawdata(pathStream2, st, pw),btrdb_wrapper.get_rawdata(pathStream3, st, pw),baseVoltage)
