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

# # Advent of code 2020: day 12
#
# Problem [here](https://adventofcode.com/2020/day/12)

# +
example_instructions = [ (ln[0], float(ln.strip()[1:])) for ln in  """
F10
N3
F7
R90
F11
""".split("\n") if ln.strip() ]

with open("inputs/day12.txt") as inF:
    puzzle_instructions = [ (ln[0], float(ln.strip()[1:])) for ln in inF if ln.strip() ]

print(example_instructions)
# -

# ## Part 1

# +
def toGeoStr(x, y):
    s_x = (f"east {x:f}" if x > 0 else f"west {-x:f}")
    s_y = (f"north {y:f}" if y > 0 else f"north {-y:f}")
    return ", ".join((s_x, s_y))

import math
class BoatPosition:
    def __init__(self, x, y, q):
        self.x = x
        self.y = y
        self.q = q # note: in degrees, from east up, angle from north: 90-self.q
    def move(self, arg, val):
        if arg == "N":
            self.y += val
        elif arg == "S":
            self.y -= val
        elif arg == "E":
            self.x += val
        elif arg == "W":
            self.x -= val
        elif arg == "L":
            self.q += val
        elif arg == "R":
            self.q -= val
        elif arg == "F":
            theta = math.pi*self.q/180
            self.x += val*math.cos(theta)
            self.y += val*math.sin(theta)
    def __str__(self):
        return f"{toGeoStr(self.x, self.y)} (facing {90-self.q:f})"

example_boat = BoatPosition(0, 0, 0)
for arg, val in example_instructions:
    example_boat.move(arg, val)
print(example_boat)
print(f"Manhattan distance: {abs(example_boat.x)+abs(example_boat.y)}")
# -

puzzle1_boat = BoatPosition(0, 0, 0)
for arg, val in puzzle_instructions:
    puzzle1_boat.move(arg, val)
print(puzzle1_boat)
print(f"Manhattan distance: {round(abs(puzzle1_boat.x)+abs(puzzle1_boat.y))}")
# -

# ## Part 2

# +
class BoatPosition2:
    def __init__(self, x, y, wx, wy):
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy
    def move(self, arg, val):
        if arg == "N":
            self.wy += val
        elif arg == "S":
            self.wy -= val
        elif arg == "E":
            self.wx += val
        elif arg == "W":
            self.wx -= val
        elif arg == "L" or arg == "R":
            if arg == "R":
                val = -val
            vr = val*math.pi/180.
            cq, sq = math.cos(vr), math.sin(vr)
            self.wx, self.wy = (cq*self.wx-sq*self.wy), (cq*self.wy+sq*self.wx)
        elif arg == "F":
            self.x += val*self.wx
            self.y += val*self.wy
    def __str__(self):
        return f"{toGeoStr(self.x, self.y)}, waypoint at {toGeoStr(self.wx, self.wy)}"

example_boat2 = BoatPosition2(0, 0, 10, 1)
for arg, val in example_instructions:
    example_boat2.move(arg, val)
    print(example_boat2)
print(f"Manhattan distance: {abs(example_boat2.x)+abs(example_boat2.y)}")
# -

puzzle2_boat = BoatPosition2(0, 0, 10, 1)
for arg, val in puzzle_instructions:
    puzzle2_boat.move(arg, val)
print(puzzle2_boat)
print(f"Manhattan distance: {abs(puzzle2_boat.x)+abs(puzzle2_boat.y)}")
