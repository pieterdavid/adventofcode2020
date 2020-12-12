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

# # Advent of code 2020: day 1
#
# Problem [here](https://adventofcode.com/2020/day/1)

with open("inputs/day01.txt") as inF:
    numbers = [ int(ln.strip()) for ln in inF ]

# ## Part 1

from itertools import combinations
a,b = next((ia, ib) for ia,ib in combinations(numbers, 2) if ia+ib == 2020)
print((a,b), a*b)

# ## Part 2

a,b,c = next((ia, ib, ic) for ia,ib,ic in combinations(numbers, 3) if ia+ib+ic == 2020)
print((a,b,c), a*b*c)
