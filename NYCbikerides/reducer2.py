#!/usr/bin/python

import sys

tagCountList = []
tagCount = 0
oldKey = None

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisVal = data_mapped

    if oldKey and oldKey != thisKey:
        tagCountList.append((oldKey, tagCount))
        tagCount = 0

    oldKey = thisKey
    tagCount += int(thisVal)

if oldKey != None:
    tagCountList.append((oldKey, tagCount))

sorted_tagCountList = sorted(tagCountList, key = lambda x: x[1], reverse = True)

for i in range(10):
    print "{0}\t{1}".format(sorted_tagCountList[i][0], sorted_tagCountList[i][1])