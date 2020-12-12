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

# # Advent of code 2020: day 4
#
# Problem [here](https://adventofcode.com/2020/day/4)

# +
from itertools import groupby
with open("inputs/day04.txt") as inF:
    inLines = [ ln.strip() for ln in inF ]

passports_unparsed = [" ".join(ln.strip() for ln in passLines) for isNotSep,passLines in groupby(inLines, bool) if isNotSep]
passports_parsed = [ dict(word.split(":") for word in unp.split()) for unp in passports_unparsed ]
# -

# # Part 1

print(sum(1 for p in passports_parsed if all(ky in p for ky in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"))))


# # Part 2

# +
def isValid2(passport):
    if not all(ky in passport for ky in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")):
        return False
    byr = int(passport["byr"])
    if byr < 1920 or byr > 2002:
        return False
    iyr = int(passport["iyr"])
    if iyr < 2010 or iyr > 2020:
        return False
    eyr = int(passport["eyr"])
    if eyr < 2020 or eyr > 2030:
        return False
    if ( not passport["hgt"].endswith("cm") ) and ( not passport["hgt"].endswith("in") ):
        return False
    hgt = int(passport["hgt"][:-2])
    hgtU = passport["hgt"][-2:]
    if hgtU == "cm":
        if hgt < 150 or hgt > 193:
            return False
    elif hgtU == "in":
        if hgt < 59 or hgt > 76:
            return False
    else:
        return False
    if not ( len(passport["hcl"]) == 7 and passport["hcl"][0] == "#" and all(c.isnumeric() or c in "abcdef" for c in passport["hcl"][1:]) ):
        return False
    if passport["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        return False
    if not ( passport["pid"].isnumeric() and len(passport["pid"]) == 9 ):
        return False
    return True

print(sum(1 for p in passports_parsed if isValid2(p)))
# -
