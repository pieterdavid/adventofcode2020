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

# # Advent of code 2020: day 6
#
# Problem [here](https://adventofcode.com/2020/day/6)
#
# ## Part 1

# +
example_input = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""
from itertools import groupby

def readGroups(lines):
    for bV,lnGrp in groupby((ln.strip() for ln in lines), bool):
        if bV:
            yield lnGrp

def collect_questions(inputLines):
    questions_per_group = []
    for grp in readGroups(inputLines):
        sGrp = set()
        for ln in grp:
            for c in ln:
                sGrp.add(c)
        questions_per_group.append(sGrp)
    return questions_per_group

ex_qs = collect_questions(example_input.split("\n"))
print(ex_qs, sum(len(st) for st in ex_qs))
# -

with open("inputs/day06.txt") as puzzleInput:
    puzzle_questions_per_group = collect_questions(puzzleInput)
print(sum(len(grp) for grp in puzzle_questions_per_group))

# ## Part 2

# +
def collect_questions_2(inputLines):
    questions_per_group = []
    for grp in readGroups(inputLines):
        allAnswered = None
        for ln in grp:
            if allAnswered is None:
                allAnswered = ln
            else:
                allAnswered = "".join(c for c in allAnswered if c in ln)
        questions_per_group.append(allAnswered)
    return questions_per_group

ex_qs_2 = collect_questions_2(example_input.split("\n"))
print(ex_qs_2, sum(len(st) for st in ex_qs_2))
# -

with open("inputs/day06.txt") as puzzleInput:
    puzzle_questions_per_group_2 = collect_questions_2(puzzleInput)
print(sum(len(grp) for grp in puzzle_questions_per_group_2))
