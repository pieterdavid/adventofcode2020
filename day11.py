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

# # Advent of code 2020: day 11
#
# Problem [here](https://adventofcode.com/2020/day/11)
#
# ## Part 1

import numpy as np
example_layout = np.array([ [ elm == "L" for elm in ln.strip() ] for ln in
"""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n") if ln.strip() ] )


# +
def seatOneStep(seating, layout, debug=False):
    ## seating (changed in place) should be integer, layout boolean
    def _getSlices(d):
        if d > 0:
            return slice(d, None), slice(-d)
        elif d < 0:
            return slice(d), slice(-d, None)
        else:
            return slice(None), slice(None)
    ## calculate number of adjacent occupied
    nAdj = np.zeros(layout.shape, dtype=np.int)
    for dx in range(-1, 2):
        x_from, x_to = _getSlices(dx)
        for dy in range(-1, 2):
            y_from, y_to = _getSlices(dy)
            if dx != 0 or dy != 0:
                nAdj[x_to,y_to] += seating[x_from,y_from]
    ## apply the seating rules
    s_ones = np.ones(seating.shape, dtype=seating.dtype)
    s_zeros = np.zeros(seating.shape, dtype=seating.dtype)
    nextSeating = np.array(seating)
    ## empty and empty around -> occupy
    msk_fill = np.logical_and(seating == 0, nAdj == 0)
    nextSeating += np.where(layout, np.where(msk_fill, s_ones, s_zeros), s_zeros)
    ## taken and >= 4 -> empty
    msk_empty = np.logical_and(seating == 1, nAdj >= 4)
    nextSeating -= np.where(layout, np.where(msk_empty, s_ones, s_zeros), s_zeros)

    return nextSeating

def printSeating(seating, layout):
    print("\n".join("".join(
        ("." if not iL else ("#" if iS else "L")) for iS, iL in zip(sRow, lRow))
        for sRow,lRow in zip(seating, layout)))

def run_until_stable(layout, debug=True, oneStep=None):
    prevSeating = np.ones(layout.shape, dtype=np.int) # placeholder, irrelevant
    seating = np.zeros(layout.shape, dtype=np.int)
    i = 0
    while not np.array_equal(prevSeating, seating):
        prevSeating, seating = seating, oneStep(seating, layout)
        if debug:
            print(f"Seating step {i+1:d} went from {np.sum(prevSeating):d} to {np.sum(seating):d} occupied seats")
            printSeating(seating, layout)
        i += 1
    return i-1, seating

example_steps, example_stable = run_until_stable(example_layout, debug=True, oneStep=seatOneStep)
print(f"Example input: {np.sum(example_stable):d} seats taken when stable, after {example_steps:d} steps")

# +
with open("inputs/day11.txt") as inF:
    puzzle_layout = np.array([ [ char != "." for char in ln.strip() ] for ln in inF if ln.strip() ])
    
puzzle_steps, puzzle_stable = run_until_stable(puzzle_layout, debug=False, oneStep=seatOneStep)
print(f"Puzzle input: {np.sum(puzzle_stable):d} seats taken when stable, after {puzzle_steps:d} steps")
# -

# ## Part 2

# +
def seatOneStep2(seating, layout, debug=False):
    ## seating (changed in place) should be integer, layout boolean
    ## calculate number of adjacent occupied
    nVis = np.zeros(layout.shape, dtype=np.int)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                with np.nditer(seating, flags=['multi_index']) as itSeat:
                    for elm in itSeat:
                        idx = itSeat.multi_index
                        visInDir = None
                        i,j = idx[0]+dx, idx[1]+dy
                        while i >= 0 and i < layout.shape[0] and j >= 0 and j < layout.shape[1]:
                            if layout[i,j]: # first seat in that direction
                                visInDir = seating[i,j]
                                break
                            else:
                                i += dx
                                j += dy
                        if visInDir == 1:
                            nVis[idx] += 1
    ## apply the seating rules
    s_ones = np.ones(seating.shape, dtype=seating.dtype)
    s_zeros = np.zeros(seating.shape, dtype=seating.dtype)
    nextSeating = np.array(seating)
    ## empty and empty around -> occupy
    msk_fill = np.logical_and(seating == 0, nVis == 0)
    nextSeating += np.where(layout, np.where(msk_fill, s_ones, s_zeros), s_zeros)
    ## taken and >= 5 -> empty
    msk_empty = np.logical_and(seating == 1, nVis >= 5)
    nextSeating -= np.where(layout, np.where(msk_empty, s_ones, s_zeros), s_zeros)

    return nextSeating

example_steps2, example_stable2 = run_until_stable(example_layout, debug=True, oneStep=seatOneStep2)
print(f"Example input: {np.sum(example_stable2):d} seats taken when stable, after {example_steps2:d} steps")
# -

puzzle_steps2, puzzle_stable2 = run_until_stable(puzzle_layout, debug=False, oneStep=seatOneStep2)
print(f"Puzzle input with rules v2: {np.sum(puzzle_stable2):d} seats taken when stable, after {puzzle_steps2:d} steps")
