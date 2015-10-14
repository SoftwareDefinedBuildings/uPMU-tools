import math
import btrdb

class BTrSearch(object):
    def __init__(self, wrapper, path):
        self.connection = wrapper.connection
        self.uuid = wrapper.get_uuid(path)

    def accept(self, visitor):
        self.visitor = visitor

    def multi_resolution_search(self, startStr, endStr, threshold=0.1):
        startTime = btrdb.date(startStr)
        endTime   = btrdb.date(endStr)
        return self.visitor.traverse(self.uuid, self.connection, startTime, endTime, threshold)

    def find_mean(self, startStr, endStr):
        startTime = btrdb.date(startStr)
        endTime   = btrdb.date(endStr)
        summation = 0
        count = 0
        pw = int(math.ceil(math.log(endTime-startTime, 2)))-11
        overview = self.connection.get_stat(self.uuid, startTime, endTime, pw)
        for x in overview:
            summation += x[2]*x[4]
            count += x[4]
        return summation/count

class Visitor:
    def visit(self, points, threshold): pass

    def traverse(self, uuid, cn, start, end, threshold, finalresolution=23):
        pw = int(math.ceil(math.log(end-start, 2)))-11
        startsL1 = self.visit(cn.get_stat(uuid, start, end, pw), threshold)
        while pw > finalresolution + 11:
            pwnew = pw - 11;
            startsL2 = []
            for st in startsL1:
                startsL2.extend(self.visit(cn.get_stat(uuid, st, st + (1<<pw), pwnew), threshold))
            startsL1 = startsL2
            pw = pwnew
        return startsL1, pw

    def __str__(self):
        return self.__class__.__name__

class MaxComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if x[3] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MeanComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if x[2] < threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MinComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if x[1] < threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MinMeanDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if x[2]-x[1] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MaxMeanDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if x[3]-x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MaxMinDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if x[3]-x[1] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MinMeanMaxMeanDiffComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if x[2]-x[1] > threshold or x[3]-x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MinMeanRatioComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if (x[2]-x[1])/x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MaxMeanRatioComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if (x[3]-x[2])/x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts

class MinMeanMaxMeanRatioComparator(Visitor):
    def visit(self, points, threshold):
        starts = []
        for x in points:
            if (x[2]-x[1])/x[2] > threshold or (x[3]-x[2])/x[2] > threshold:
                starts.append(x[0]) # append start time of this partition
        return starts
