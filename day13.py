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

# # Advent of code 2020: day 13
#
# Problem [here](https://adventofcode.com/2020/day/13)

# ## Part 1

# +
example_input = """939
7,13,x,x,59,x,31,19"""

def parse_input1(l1, l2):
    return int(l1), [ int(tk) for tk in l2.split(",") if tk != "x" ]

example_dep, example_buses = parse_input1(*example_input.split("\n"))
print(example_dep, example_buses)
# -

example_time_until_bus = [ (bus, bus - (example_dep % bus)) for bus in example_buses ]
print(example_time_until_bus)


# +
def earliest_bus(dep, buses):
    return min(((bus, bus - (dep%bus)) for bus in buses), key=(lambda elm : elm[1]))

ex_firstbus, ex_wait = earliest_bus(example_dep, example_buses)
print(ex_firstbus*ex_wait)
# -

with open("inputs/day13.txt") as inF:
    puzzle_dep, puzzle_buses = parse_input1(*(ln.strip() for ln in inF if ln.strip()))
p1_firstbus, p1_wait = earliest_bus(puzzle_dep, puzzle_buses)
print(p1_firstbus*p1_wait)

# ## Part 2

example_buses2 = [ (i, int(tk)) for i,tk in enumerate(example_input.split("\n")[1].split(",")) if tk != "x" ]
print(example_buses2)

import math
i = 0
while ((i*7) % 13) != 12:
    i += 1
print(f"Common for 7 and 13: t={i*7:d}")


# +
def find_leave_in_sequence(buses):
    inc = 1
    t = 0
    for bI,bus in buses:
        targ = (bus-bI)%bus
        while (t%bus) != targ:
            t += inc
        inc = math.lcm(inc, bus) # time until this happens next
        pbI = bI
        print(f"Common up until bus {bus:d}#{bI:d}: {t:d}, new increment: {inc:d}")
    return t

find_leave_in_sequence([ (0,7), (1,13), (4,59), (6,31), (7,19) ])
# -

with open("inputs/day13.txt") as inF:
    inLines = [ ln.strip() for ln in inF if ln.strip() ]
    puzzle_buses2 = [ (i, int(tk)) for i,tk in enumerate(inLines[1].split(",")) if tk != "x" ]
print(puzzle_buses2)

find_leave_in_sequence(puzzle_buses2)
