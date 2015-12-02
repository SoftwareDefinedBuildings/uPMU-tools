import math
import btrdb
import timeit
from plotter import *

def decorate(func, *args, **kwargs):
    def func_wrapper():
        return func(*args, **kwargs)
    return func_wrapper

class BTrSearch(object):
    def __init__(self, wrapper, path):
        self.connection = wrapper.connection
        self.uuid = wrapper.get_uuid(path)

    def accept(self, visitor):
        self.visitor = visitor

    def multi_resolution_search(self, startUTCTimeStr, endUTCTimeStr, threshold=0.1, plotFlag=False, benchmarkFlag=False, ylabel):
        startTime = btrdb.date(startUTCTimeStr)     # returns nanoseconds since the epoch
        endTime   = btrdb.date(endUTCTimeStr)       # returns nanoseconds since the epoch
        return self.visitor.traverse(self.uuid, self.connection, startTime, endTime, threshold, ylabel, plotFlag=plotFlag, benchmarkFlag=benchmarkFlag)

    def multi_resolution_search_fw(self, startUTCTimeStr, endUTCTimeStr, threshold=0.1, final_res=26, plotFlag=False, benchmarkFlag=False, ylabel):
        startTime = btrdb.date(startUTCTimeStr)     # returns nanoseconds since the epoch
        endTime   = btrdb.date(endUTCTimeStr)       # returns nanoseconds since the epoch
        return self.visitor.traverse(self.uuid, self.connection, startTime, endTime, threshold, ylabel, final_res, plotFlag=plotFlag, benchmarkFlag=benchmarkFlag)

    def find_mean(self, startUTCTimeStr, endUTCTimeStr):
        startTime = btrdb.date(startUTCTimeStr)     # returns nanoseconds since the epoch
        endTime   = btrdb.date(endUTCTimeStr)       # returns nanoseconds since the epoch
        summation = 0
        count = 0
        pw = int(math.ceil(math.log(endTime-startTime, 2)))-11
        overview = self.connection.get_stat(self.uuid, startTime, endTime, pw)
        for x in overview:
            summation += x[2]*x[4]
            count += x[4]
        return summation/count, count

class Visitor:
    def visit(self, points, threshold): pass

    def traverse(self, uuid, cn, start, end, threshold, ylabel, finalresolution=23, plotFlag=False, benchmarkFlag=False):
        pw = int(math.ceil(math.log(end-start, 2)))-11

        start_time = timeit.default_timer()
        overview = cn.get_stat(uuid, start, end, pw)
        startsL1, operands = self.visit(overview, threshold)

        if benchmarkFlag:
            elapsed = timeit.default_timer() - start_time
            print "the search completes in " + str(1000*elapsed) + "ms at depth 1"

        if plotFlag:
            visualize_tree_traversal([x[0] for x in overview], operands, threshold)

        depth = 1
        while pw > finalresolution + 11:
            depth = depth + 1
            pw = pw - 11;
            startsL2 = []
            for st in startsL1:
                start_time = timeit.default_timer()
                coarse = cn.get_stat(uuid, st, st + (1<<(pw+11)), pw)
                startsTemp, operandsTemp = self.visit(coarse, threshold)
                startsL2.extend(startsTemp)
                
                if len(startsTemp) > 0:
                    if benchmarkFlag:
                        elapsed = timeit.default_timer() - start_time
                        print "the search completes in " + str(1000*elapsed) + "ms at depth " + str(depth)
                    if plotFlag:
                        visualize_tree_traversal([x[0] for x in coarse], operandsTemp, threshold)
                        if pw <= finalresolution + 11:
                            for sts in startsTemp:
                                start_time = timeit.default_timer()
                                raw = cn.get_stat(uuid, sts, sts + (1<<pw), 23)
                                elapsed = timeit.default_timer() - start_time
                                plot_rawdata([(x[0],x[2]) for x in raw], ylabel)
                                if benchmarkFlag:
                                    print "raw data query completes in " + str(1000*elapsed) + "ms"
                elif len(startsTemp) == 0:
                    #print 'Warning!'
                    pass

            startsL1 = startsL2

        return startsL1, pw

    def __str__(self):
        return self.__class__.__name__

class MaxComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if x[3] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(x[3])
        return starts, operands

class MeanComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if x[2] < threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(x[2])
        return starts, operands

class MinComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if x[1] < threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(x[1])
        return starts, operands

class MinMeanDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if x[2]-x[1] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(x[2]-x[1])
        return starts, operands

class MaxMeanDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if x[3]-x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(x[3]-x[2])
        return starts, operands

class MaxMinDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if x[3]-x[1] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(x[3]-x[1])
        return starts, operands

class MinMeanMaxMeanDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if x[2]-x[1] > threshold or x[3]-x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(max(x[3]-x[2],x[2]-x[1]))
        return starts, operands

class MinMeanRatioComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if (x[2]-x[1])/x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append((x[2]-x[1])/x[2])
        return starts, operands

class MaxMeanRatioComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if (x[3]-x[2])/x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append((x[3]-x[2])/x[2])
        return starts, operands

class MinMeanMaxMeanRatioComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        operands = []
        for x in points:
            if (x[2]-x[1])/x[2] > threshold or (x[3]-x[2])/x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
            operands.append(max((x[2]-x[1])/x[2],(x[3]-x[2])/x[2]))
        return starts, operands
