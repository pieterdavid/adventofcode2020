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

# # Advent of code 2020: day 16
#
# Problem [here](https://adventofcode.com/2020/day/16)

# ## Part 1

# +
ex_input = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

class Field:
    def __init__(self, validRanges):
        self.validRanges = validRanges
    def maybeValid(self, num):
        return any(lw <= num and num <= up for lw, up in self.validRanges)
    @staticmethod
    def parse(spec):
        return Field([ tuple(int(vl) for vl in tok.split("-")) for tok in spec.split(" or ") ])
    def __str__(self):
        return " or ".join("-".join(rng) for rng in self.validRanges)

def parseNotes(lines):
    iLines = iter(lines)
    fields, mine, nearby = {}, None, []
    while ln := next(iLines): ## read fields
        fNm, opts = ln.split(": ")
        fields[fNm] = Field.parse(opts)
    assert next(iLines) == "your ticket:"
    mine = [ int(val) for val in next(iLines).split(",") ]
    assert not next(iLines) ## skip empty
    assert next(iLines) == "nearby tickets:"
    try:
        while ln := next(iLines): ## read nearby
            nearby.append([ int(val) for val in ln.split(",") ])
    except StopIteration:
        pass
    return fields, mine, nearby

ex_fields, ex_mine, ex_nearby = parseNotes(ex_input.split("\n"))
print(ex_fields)
print(ex_mine)
print(ex_nearby)
ex_errRate = 0
for nbTk in ex_nearby:
    for val in nbTk:
        if not any(field.maybeValid(val) for field in ex_fields.values()):
            print(f"Value {val:d} in nearby ticket {nbTk!r} is invalid")
            ex_errRate += val
print(f"Example scanning error rate: {ex_errRate:d}")

# +
with open("inputs/day16.txt") as inF:
    p1_fields, p1_mine, p1_nearby = parseNotes(( ln.strip() for ln in inF ))
    
p1_errRate = 0
valid_nearby = []
for nbTk in p1_nearby:
    isValid = True
    for val in nbTk:
        if not any(field.maybeValid(val) for field in p1_fields.values()):
            p1_errRate += val
            isValid = False
    if isValid:
        valid_nearby.append(nbTk)
print(f"Puzzle scanning error rate: {p1_errRate:d}")
# -

# ## Part 2

compat_fields_per_col = [
    [ fNm for fNm,f in p1_fields.items() if all(f.maybeValid(nbTk[iCol]) for nbTk in valid_nearby ) ]
    for iCol in range(len(p1_fields)) ]
print([len(compat) for compat in compat_fields_per_col])
colNames = [ None for f in p1_fields ]
while any(cn is None for cn in colNames):
    assigned = []
    for iCol, compat in enumerate(compat_fields_per_col):
        if len(compat) == 1:
            name = compat[0]
            colNames[iCol] = name
            assigned.append(name)
    if not assigned:
        print("I'm stuck :-(")
        break
    assert len(assigned) == len(set(assigned))
    for compat in compat_fields_per_col:
        for name in assigned:
            if name in compat:
                del compat[compat.index(name)]
print(colNames)
depVals = [ mnVal for mnVal,colNm in zip(p1_mine, colNames) if colNm.startswith("departure") ]
print(depVals)
prod = 1
for v in depVals:
    prod *= v
print(prod)
