"""
Sublinear algorithm for detecting rapid changes in current magnitude

@author Omid Ardakanian (ardakanian@berkeley.edu)
"""

from btrdb-util import *

threshold = 525 # detecting voltage sag

startTime = "2015-07-01T00:00:00"
endTime   = "2015-10-01T00:00:00"

distillate1 = "/prod/RPU/building_1086/C1MAG-Delta"
distillate2 = "/prod/RPU/building_1086/C2MAG-Delta"
distillate3 = "/prod/RPU/building_1086/C3MAG-Delta"

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
cvarStarts2, _  = searchTree1.multi_resolution_search(startTime, endTime, threshold)

searchTree3 = BTrSearch(btrdb_wrapper, distillate3)
searchTree3.accept(visitor)
cvarStarts3, _  = searchTree1.multi_resolution_search(startTime, endTime, threshold)

allcases = list(set(cvarStarts1) | set(cvarStarts2) | set(cvarStarts3))
print len(allcases)

for st in allcases:
    plot_3phase_current_rawdata(btrdb_wrapper.get_rawdata(pathStream1, st, pw),btrdb_wrapper.get_rawdata(pathStream2, st, pw),btrdb_wrapper.get_rawdata(pathStream3, st, pw))
