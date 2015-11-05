"""
Sublinear algorithm for detecting voltage sags

@author Omid Ardakanian (ardakanian@berkeley.edu)
"""

from btrdbutil.btrdbwrapper import *
from btrdbutil.btrsearch import *
from btrdbutil.plotter import *
import timeit
import matplotlib.pyplot as plt

threshold = 0.10 # detecting voltage sag

# UTC time -> to get local time -08:00 if PST, -07:00 if PDT
startTime = "2014-12-03T00:00:00"
endTime   = "2015-11-01T21:00:00"

pathStream1 = "/clean/switch_a6/L1MAG/CLEAN"
pathStream2 = "/clean/switch_a6/L2MAG/CLEAN"
pathStream3 = "/clean/switch_a6/L3MAG/CLEAN"

btrdb_wrapper = BTrDBWrapper()
#visitor = MinMeanDiffComparator()
visitor = MinMeanRatioComparator()

searchTree1 = BTrSearch(btrdb_wrapper, pathStream1)
searchTree1.accept(visitor)

baseVoltage, count = searchTree1.find_mean(startTime, endTime)
#print "The estimated nominal voltage is "+str(baseVoltage)+"V"
#print "Total points in the time series  "+str(count)
#threshold = threshold*baseVoltage

vsagStartsL1, pw = searchTree1.multi_resolution_search(startTime, endTime, threshold)
# for st in vsagStartsL1:
#     wrapped = decorate(btrdb_wrapper.get_rawdata, pathStream1, st, pw)
#     print "execution time of pw = 23 is " + str(timeit.timeit(wrapped, number=100)/100)

searchTree2 = BTrSearch(btrdb_wrapper, pathStream2)
searchTree2.accept(visitor)
vsagStartsL2, _  = searchTree2.multi_resolution_search(startTime, endTime, threshold)
# for st in vsagStartsL2:
#     wrapped = decorate(btrdb_wrapper.get_rawdata, pathStream2, st, pw)
#     print "execution time of pw = 23 is " + str(timeit.timeit(wrapped, number=100)/100)

searchTree3 = BTrSearch(btrdb_wrapper, pathStream3)
searchTree3.accept(visitor)
vsagStartsL3, _  = searchTree3.multi_resolution_search(startTime, endTime, threshold)
# for st in vsagStartsL3:
#     wrapped = decorate(btrdb_wrapper.get_rawdata, pathStream3, st, pw)
#     print "execution time of pw = 23 is " + str(timeit.timeit(wrapped, number=100)/100)

allcases = list(set(vsagStartsL1) | set(vsagStartsL2) | set(vsagStartsL3))
print len(allcases)

for st in allcases:
    plot_3phase_voltage_rawdata(btrdb_wrapper.get_rawdata(pathStream1, st, pw),btrdb_wrapper.get_rawdata(pathStream2, st, pw),btrdb_wrapper.get_rawdata(pathStream3, st, pw),baseVoltage)


# plt.title('Latency of multi-resolution search')
# plt.ylabel('Chunk size (no. points)', fontsize=16)
# plt.xlabel('Latency (ms)', fontsize=16)
# axes = plt.gca()
# axes.set_xlim([0,200])
# axes.set_ylim([1,10000000000])
#
# nums = [3423082551,2111063,1031]
#
# plt.grid(True)
# plt.semilogy([58.85910988,109.4651222,140.8827519],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,113.5151386,146.9741368],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,113.4209633,148.2705617],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,113.4209633,146.2193441],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,141.2270069,181.1187363],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,116.3892746,150.3114748],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,109.9441051,143.2924843],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,113.4209633,151.0986733],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,108.4291935,145.0168133],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,122.2600937,157.0690131],nums,linestyle=':', marker='o', color='b', markersize=4)
# plt.semilogy([58.85910988,113.4481430,147.1772242],nums,linestyle=':', marker='o', color='b', markersize=4)
#
# plt.show()
