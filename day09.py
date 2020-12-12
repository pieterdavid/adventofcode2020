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

# # Advent of code 2020: day 9
#
# Problem [here](https://adventofcode.com/2020/day/9)
#
# ## Part 1

# +
example_input = [int(ln.strip()) for ln in """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split("\n") ]

from itertools import combinations

def run_while_valid(inputs, preambleSize):
    buffer = inputs[:preambleSize]
    iB = 0
    for i,num in enumerate(inputs[preambleSize:], start=preambleSize):
        if not any(a+b == num for a,b in combinations(buffer, 2)):
            print(f"Invalid for element {i:d}: {num:d}")
            return num
        buffer[iB] = num
        iB = (iB + 1) % preambleSize

example_invalid = run_while_valid(example_input, 5)
# -

# +
with open("inputs/day09.txt") as inF:
    puzzle_input = [ int(ln.strip()) for ln in inF if ln.strip() ]

puzzle_invalid = run_while_valid(puzzle_input, 25)
# -

# ## Part 2

# +
def find_weakness(inputs, invalid):
    iB,iE = 0,0
    rngSum = 0
    while iE < len(inputs):
        while rngSum < invalid and iE < len(inputs):
            rngSum += inputs[iE]
            iE += 1
        if rngSum == invalid:
            weakness = inputs[iB:iE]
            print(f"Found weakness: {weakness!r}")
            mn = min(weakness)
            mx = max(weakness)
            print(f"Weakness min and max: {mn!r}, {mx!r}; sum={mn+mx!r}")
            break
        else:
            rngSum -= inputs[iB]
            iB += 1
            while rngSum > invalid:
                iE -= 1
                rngSum -= inputs[iE]

find_weakness(example_input, example_invalid)
# -

find_weakness(puzzle_input, puzzle_invalid)
