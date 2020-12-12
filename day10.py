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

# # Advent of code 2020: day 10
#
# Problem [here](https://adventofcode.com/2020/day/10)
#
# ## Part 1

# +
ex1_input = [ int(ln.strip()) for ln in """
16
10
15
5
1
11
7
19
6
12
4
""".split() if ln.strip() ]

ex2_input = [ int(ln.strip()) for ln in """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
""".split() if ln.strip() ]

# +
import numpy as np

def count_steps(inputs):
    inputs = np.array(sorted(inputs))
    steps = inputs[1:]-inputs[:-1]
    counts = [ np.count_nonzero(steps == i+1) for i in range(3) ]
    counts[0] += 1 ## initial, from 0
    counts[2] += 1 ## final, to max+3
    return counts

print(count_steps(ex1_input))
# -

print(count_steps(ex2_input))

# +
with open("inputs/day10.txt") as inF:
    puzzle_inputs = [ int(ln.strip()) for ln in inF if ln.strip() ]

nSteps_puzzle = count_steps(puzzle_inputs)
print(nSteps_puzzle, nSteps_puzzle[0]*nSteps_puzzle[2])
# -

# ## Part 2

# Since the largest difference is 3, the number of ways to reach N is
# the sum of the number of ways to get to N-1, N-2 and N-3.
# Therefore it is sufficient to loop over the range of voltages once,
# keeping track of three adaptors at a time, to count the number of
# ways to bridge the whole interval.

# +
def count_ways(inputs):
    input_s = set(inputs)
    assert len(input_s) == len(inputs)
    target = max(inputs)
    n = 0
    nWaysTo = [None]*3
    for n in range(3):         # initialize the first 3
        nWaysTo[n] = (1+sum(nWaysTo[:n]) if n+1 in input_s else 0)
    for n in range(3, target): # then count the rest
        nWaysTo[n%3] = (sum(nWaysTo) if n+1 in input_s else 0)
    return nWaysTo[(target-1)%3]

print(count_ways(ex1_input))
# -

print(count_ways(ex2_input))

print(count_ways(puzzle_inputs))
