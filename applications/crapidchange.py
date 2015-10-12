"""
Sublinear algorithm for detecting rapid changes in current magnitude

@author Omid Ardakanian (ardakanian@berkeley.edu)
"""

from btrdbutil.btrdbwrapper import *
from btrdbutil.btrsearch import *
from btrdbutil.plotter import *

threshold = 200 # detecting voltage sag

startTime = "2015-07-01T00:00:00"
endTime   = "2015-10-01T00:00:00"

distillate1 = "/Production/RPU/Building_1086/CurrentDiff/Currentdiff_1/currentdifference"
distillate2 = "/Production/RPU/Building_1086/CurrentDiff/Currentdiff_2/currentdifference"
distillate3 = "/Production/RPU/Building_1086/CurrentDiff/Currentdiff_3/currentdifference"

pathStream1 = "/upmu/RPU/building_1086/C1MAG"
pathStream2 = "/upmu/RPU/building_1086/C2MAG"
pathStream3 = "/upmu/RPU/building_1086/C3MAG"

btrdb_wrapper = BTrDBWrapper()
visitor = MaxAboveThreshold()

searchTree1 = BTrSearch(btrdb_wrapper, distillate1)
searchTree1.accept(visitor)
cvarStarts1, pw = searchTree1.multi_resolution_search(startTime, endTime, threshold)

searchTree2 = BTrSearch(btrdb_wrapper, distillate2)
searchTree2.accept(visitor)
cvarStarts2, _  = searchTree2.multi_resolution_search(startTime, endTime, threshold)

searchTree3 = BTrSearch(btrdb_wrapper, distillate3)
searchTree3.accept(visitor)
cvarStarts3, _  = searchTree3.multi_resolution_search(startTime, endTime, threshold)

allcases = list(set(cvarStarts1) | set(cvarStarts2) | set(cvarStarts3))
print len(allcases)

for st in allcases:
    plot_3phase_current_rawdata(btrdb_wrapper.get_rawdata(pathStream1, st, pw),btrdb_wrapper.get_rawdata(pathStream2, st, pw),btrdb_wrapper.get_rawdata(pathStream3, st, pw))
