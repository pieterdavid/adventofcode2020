# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Advent of code 2020: day 23
#
# Problem [here](https://adventofcode.com/2020/day/23)

# ## Part 1

# +
def crabCupGame(cups, nRounds, debug=False):
    start = 0
    highest = max(cups)
    lowest = min(cups)
    for i in range(nRounds):
        if debug:
            print(f"-- move {i+1:d} --")
            print(f"cups: {' '.join(str(v) for v in cups[:start])} ({cups[start]:d}) {' '.join(str(v) for v in cups[start+1:])}")
        curVal = cups[start]
        crab = []
        for j in range(1,4): # crab takes away
            pos = start+1
            if pos >= len(cups):
                pos -= len(cups) # could be modulo
                start -= 1       # will remove one before
            crab.append(cups.pop(pos))
        if debug:
            print(f"Pick up: {' '.join(str(v) for v in crab)}")
        assert curVal == cups[start] # check: did start follow?
        destVal = (curVal-1)
        if destVal < lowest:
            destVal = highest
        while destVal in crab:
            destVal -= 1
            if destVal < lowest:
                destVal = highest
        if debug:
            print(f"Destination: {destVal}")
        destPos = cups.index(destVal)+1
        cups[destPos:destPos] = crab
        if destPos <= start:
            start += 3 # inserted before
        assert curVal == cups[start] # check: did start follow?
        start = (start + 1) % len(cups) # move on for the next round
        if debug:
            print()
        if ((i+1) % 100) == 0:
            print(f"Done round {i+1:d}")
    if debug:
        print("-- final --")
        print(f"cups: ({cups[start]:d}) {' '.join(str(v) for v in cups[start+1:]+cups[:start])}")
    return cups

ex10_cups = crabCupGame([int(ch) for ch in "389125467"], 10, debug=True)
ex10_i1 = ex10_cups.index(1)
print("After 10: ", "".join(str(v) for v in ex10_cups[ex10_i1+1:]+ex10_cups[:ex10_i1]))
ex100_cups = crabCupGame([int(ch) for ch in "389125467"], 100, debug=False)
ex100_i1 = ex100_cups.index(1)
print("After 100: ", "".join(str(v) for v in ex100_cups[ex100_i1+1:]+ex100_cups[:ex100_i1]))
# -

p1_cups = crabCupGame([int(ch) for ch in "394618527"], 100, debug=False)
p1_i1 = p1_cups.index(1)
print("After 100: ", "".join(str(v) for v in p1_cups[p1_i1+1:]+p1_cups[:p1_i1]))


# ## Part 2

# +
import numpy as np
def crabCupGame2(firstNums, nRounds, totalLen=None, debug=False):
    if totalLen is None:
        totalLen = len(firstNums)
    iNext = np.zeros((totalLen,), dtype=np.int)
    for i,n in zip(firstNums[:-1], firstNums[1:]):
        iNext[i-1] = n-1
    if totalLen != len(firstNums):
        iNext[firstNums[-1]-1] = len(firstNums)
        for i in range(len(firstNums), iNext.shape[0]-1):
            iNext[i] = i+1
        iNext[-1] = firstNums[0]-1
    else:
        iNext[firstNums[-1]-1] = firstNums[0]-1
    if debug:
        print(iNext)
    iStart = firstNums[0]-1
    for i in range(nRounds):
        if debug:
            print(f"-- move {i+1:d} --")
            cupsFromStart = []
            idx = iNext[iStart]
            while idx != iStart:
                cupsFromStart.append(idx+1)
                idx = iNext[idx]
            print(f"cups: ({iStart+1:d}) {' '.join(str(v) for v in cupsFromStart)}")
        iSlB = iNext[iStart]
        iSlLast = iNext[iNext[iSlB]]
        iSlAfter = iNext[iSlLast]
        iNext[iStart] = iSlAfter
        iCrab = [ iSlB, iNext[iSlB], iSlLast ] # values -1
        if debug:
            print(f"Pick up: {iCrab[0]+1:d} {iCrab[1]+1:d} {iCrab[2]+1:d}")
        iDest = iStart-1
        if iDest < 0:
            iDest = totalLen-1
        while iDest in iCrab:
            iDest -= 1
            if iDest < 0:
                iDest = totalLen-1
        if debug:
            print(f"Destination: {iDest+1}")
        iNext[iSlLast] = iNext[iDest]
        iNext[iDest] = iSlB
        iStart = iSlAfter
    if debug:
        cupsFromStart = []
        idx = iNext[iStart]
        while idx != iStart:
            cupsFromStart.append(idx+1)
            idx = iNext[idx]
        print("-- final --")
        print(f"cups: ({iStart+1:d}) {' '.join(str(v) for v in cupsFromStart)}")
    if totalLen == len(firstNums):
        cupsFrom1 = []
        idx = iNext[0]
        while idx != 0:
            cupsFrom1.append(idx+1)
            idx = iNext[idx]
        return cupsFrom1
    else:
        return iNext[0]+1, iNext[iNext[0]]+1

crabCupGame2([int(ch) for ch in "389125467"], 0)
crabCupGame2([int(ch) for ch in "389125467"], 0, totalLen=12)
# -

ex10_cups = crabCupGame2([int(ch) for ch in "389125467"], 10, debug=True)
print("After 10: ", "".join(str(v) for v in ex10_cups))

ex100_cups = crabCupGame2([int(ch) for ch in "389125467"], 100, debug=False)
print("After 100: ", "".join(str(v) for v in ex100_cups))

ex1M_cups = crabCupGame2([int(ch) for ch in "389125467"], 10000000, totalLen=1000000, debug=False)
print(ex1M_cups, ex1M_cups[0]*ex1M_cups[1])

p1M_cups = crabCupGame2([int(ch) for ch in "394618527"], 10000000, totalLen=1000000, debug=False)
print(p1M_cups, p1M_cups[0]*p1M_cups[1])
