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

# # Advent of code 2020: day 3
#
# Problem [here](https://adventofcode.com/2020/day/3)

with open("inputs/day03.txt") as inF:
    inStr = inF.read()

# # Part 1

import numpy as np
inArr = np.array([ [ (True if c == "#" else False) for c in ln ]
    for ln in inStr.strip().split("\n") ], dtype=np.bool)
nTrees = sum((1 if inArr[i,(3*i)%inArr.shape[1]] else 0 ) for i in range(inArr.shape[0]))
print(nTrees)

# # Part 2

nTrees_11 = sum((1 if inArr[i,i%inArr.shape[1]] else 0 ) for i in range(inArr.shape[0]))
nTrees_31 = sum((1 if inArr[i,(3*i)%inArr.shape[1]] else 0 ) for i in range(inArr.shape[0]))
nTrees_51 = sum((1 if inArr[i,(5*i)%inArr.shape[1]] else 0 ) for i in range(inArr.shape[0]))
nTrees_71 = sum((1 if inArr[i,(7*i)%inArr.shape[1]] else 0 ) for i in range(inArr.shape[0]))
nTrees_12 = sum((1 if inArr[i,(i//2)%inArr.shape[1]] else 0 ) for i in range(0, inArr.shape[0], 2))
print(nTrees_11*nTrees_31*nTrees_51*nTrees_71*nTrees_12)
