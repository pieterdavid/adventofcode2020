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

# # Advent of code 2020: day 17
#
# Problem [here](https://adventofcode.com/2020/day/17)

# ## Part 1

# +
import numpy as np
example_input = """
.#.
..#
###
"""

def printState(state):
    for iz,stateSlice in enumerate(state):
        print(f"z={iz:d}")
        print("\n".join("".join(("#" if st else ".") for st in stLn) for stLn in stateSlice))

example_init = np.array([ [ (ch == "#") for ch in ln.strip() ] for ln in example_input.split("\n") if ln.strip() ])
example_init = np.reshape(example_init, (1, example_init.shape[0], example_init.shape[1]))
print(example_init.shape)
printState(example_init)

# +
from itertools import product, repeat
def boot_cycle(state):
    nNeighboursOn = np.zeros(tuple(dim+2 for dim in state.shape), dtype=np.intc)
    slices = (slice(None, -2), slice(1, -1), slice(2, None))
    state_int = np.where(state, np.ones(state.shape, dtype=np.intc), np.zeros(state.shape, dtype=np.intc))
    for (i1,sl1), (i2,sl2), (i3,sl3) in product(enumerate(slices, -1), repeat=3):
        if not (i1 == 0 and i2 == 0 and i3 == 0):
            nNeighboursOn[sl1,sl2,sl3] += state_int
    newState = (nNeighboursOn == 3) # turn on or stay
    newState[1:-1,1:-1,1:-1] = np.logical_or(newState[1:-1,1:-1,1:-1],
                               np.logical_and(state, (nNeighboursOn[1:-1,1:-1,1:-1] == 2)))
    slAll = [ slice(None), slice(None), slice(None) ]
    for iD in range(len(newState.shape)):
        forDim = list(slAll)
        forDim[iD] = slice(1, None)
        dropFirst = tuple(forDim)
        forDim[iD] = 0
        first = tuple(forDim)
        while np.all(np.logical_not(newState[first])):
            newState = newState[dropFirst]
        forDim[iD] = slice(None, -1)
        dropLast = tuple(forDim)
        forDim[iD] = -1
        last = tuple(forDim)
        while np.all(np.logical_not(newState[last])):
            newState = newState[dropLast]
    return newState

example_state = np.array(example_init)
print("Before cycling")
printState(example_state)
for i in range(6):
    example_state = boot_cycle(example_state)
    if i < 2:
        print(f"After cycle {i+1:d}")
    printState(example_state)
print(np.sum(np.where(example_state, np.ones(example_state.shape), np.zeros(example_state.shape))))
# -

puzzle_input = """
######.#
##.###.#
#.###.##
..#..###
##.#.#.#
##...##.
#.#.##.#
.###.###"""
puzzle_init = np.array([ [ (ch == "#") for ch in ln.strip() ] for ln in puzzle_input.split("\n") if ln.strip() ])
puzzle_init = np.reshape(puzzle_init, (1, puzzle_init.shape[0], puzzle_init.shape[1]))
puzzle_state = np.array(puzzle_init)
for i in range(6):
    puzzle_state = boot_cycle(puzzle_state)
print(np.sum(np.where(puzzle_state, np.ones(puzzle_state.shape), np.zeros(puzzle_state.shape))))


# ## Part 2

# +
def boot_cycle_n(state):
    dim = len(state.shape)
    nNeighboursOn = np.zeros(tuple(dim+2 for dim in state.shape), dtype=np.intc)
    slices = (slice(None, -2), slice(1, -1), slice(2, None))
    state_int = np.where(state, np.ones(state.shape, dtype=np.intc), np.zeros(state.shape, dtype=np.intc))
    for iAndSl in product(enumerate(slices, -1), repeat=dim):
        if not all(i == 0 for i,_ in iAndSl):
            nNeighboursOn[tuple(sl for _,sl in iAndSl)] += state_int
    newState = (nNeighboursOn == 3) # turn on or stay
    dropAllOuter = tuple(repeat(slice(1, -1), dim))
    newState[dropAllOuter] = np.logical_or(newState[dropAllOuter],
                                np.logical_and(state, (nNeighboursOn[dropAllOuter] == 2)))
    slAll = [ slice(None) ]*dim
    for iD in range(dim):
        forDim = list(slAll)
        forDim[iD] = slice(1, None)
        dropFirst = tuple(forDim)
        forDim[iD] = 0
        first = tuple(forDim)
        while np.all(np.logical_not(newState[first])):
            newState = newState[dropFirst]
        forDim[iD] = slice(None, -1)
        dropLast = tuple(forDim)
        forDim[iD] = -1
        last = tuple(forDim)
        while np.all(np.logical_not(newState[last])):
            newState = newState[dropLast]
    return newState

def printState2(state):
    for iu,stateSliceU in enumerate(state):
        for iz,stateSlice in enumerate(stateSliceU):
            print(f"u={iu:d}, z={iz:d}")
            print("\n".join("".join(("#" if st else ".") for st in stLn) for stLn in stateSlice))

example_init2 = np.reshape(example_init, tuple([1]+list(example_init.shape)))
print(example_init2.shape)
example_state2 = np.array(example_init2)
print("Before cycling")
printState2(example_state2)
for i in range(6):
    example_state2 = boot_cycle_n(example_state2)
    if i < 2:
        print(f"After cycle {i+1:d}")
    printState2(example_state2)
print(np.sum(np.where(example_state2, np.ones(example_state2.shape), np.zeros(example_state2.shape))))
# -

puzzle_init2 = np.reshape(puzzle_init, tuple([1]+list(puzzle_init.shape)))
puzzle_state2 = np.array(puzzle_init2)
for i in range(6):
    puzzle_state2 = boot_cycle_n(puzzle_state2)
print(np.sum(np.where(puzzle_state2, np.ones(puzzle_state2.shape), np.zeros(puzzle_state2.shape))))
