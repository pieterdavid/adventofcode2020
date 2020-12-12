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

# # Advent of code 2020: day 2
#
# Problem [here](https://adventofcode.com/2020/day/2)

with open("inputs/day02.txt") as inF:
    passLines = [ ln.strip() for ln in inF ]

# ## Part 1

invalidPasswords = []
for aLine in passLines:
    policy, passWord = aLine.split(": ")
    counts, mandLetter = policy.split()
    nMin, nMax = tuple(int(tk) for tk in counts.split("-"))
    nFound = passWord.count(mandLetter)
    if nFound < nMin or nFound > nMax:
        invalidPasswords.append(aLine)
print(len(passLines)-len(invalidPasswords))

# ## Part 2

invalidPasswords_policy2 = []
for aLine in passLines:
    policy, passWord = aLine.split(": ")
    positions, mandLetter = policy.split()
    positions = tuple(int(tk)-1 for tk in positions.split("-"))
    nInPos = sum((1 if passWord[iPos] == mandLetter else 0) for iPos in positions)
    if nInPos != 1:
        invalidPasswords_policy2.append(aLine)
print(len(passLines)-len(invalidPasswords_policy2))
