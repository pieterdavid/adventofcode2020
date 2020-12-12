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

# # Advent of code 2020: day 5
#
# Problem [here](https://adventofcode.com/2020/day/5)
#
# Actually these boarding passes are numbers in binary format,
# so a simple translation to 0 and 1, and a conversion to integers,
# gets them into a very convenient format.

# +
with open("inputs/day05.txt") as inF:
    boardingPasses = [ ln.strip() for ln in inF ]

trans_rows = str.maketrans({"F":"0","B":"1"})
trans_cols = str.maketrans({"L":"0","R":"1"})

def getRowAndSeat(bPass):
    return (int(bPass[:7].translate(trans_rows), base=2),
            int(bPass[7:].translate(trans_cols), base=2))
# -

# Check the first example

print(getRowAndSeat("FBFBBFFRLR"))

# Check the other three examples, and the unique seat IDs (the full number)

for bPass in ("BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL"):
    row,seat = getRowAndSeat(bPass)
    print(bPass, row, seat, 8*row+seat)

# ## Part 1: the highest seatID.
#
# We will need them for the next part, so it is convenient to keep the whole list around.

takenRowsAndSeats = [ getRowAndSeat(bPass) for bPass in boardingPasses ]
bPassIDs = [ 8*row+seat for row,seat in takenRowsAndSeats ]
highestID = max(bPassIDs)
print(highestID)

# ## Part 2: find the one empty seat between two that are taken.
#
# An efficient way (in python) to do this is by comparing
# the "previous ID" and "next ID" lists (sorted),
# the difference should be two.

import numpy as np
sortedIDs = np.array(sorted(bPassIDs))
mask_beforeMySeat = sortedIDs[:-1]+2 == sortedIDs[1:]
mySeatCandidates = sortedIDs[:-1][mask_beforeMySeat]+1
print(mySeatCandidates)
