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

# # Advent of code 2020: day 7
#
# Problem [here](https://adventofcode.com/2020/day/7)
#
# ## Part 1

example_input = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


# +
def parseRule(line):
    ## parse a rule to { colour: [ (number, colour) ] }
    colour, contPart = line.split(" bags contain ")
    contents = []
    if contPart != "no other bags.":
        contTokens = contPart.rstrip(".").split(", ")
        for contTk in contTokens:
            nr,c1,c2,_ = contTk.split()
            contents.append((int(nr), " ".join((c1,c2))))
    return colour, contents

def _check_contains(testColour, rules, colour, memo):
    ## recursive part of find_that_contains: fill up the cache up until colour
    doesContain = False
    for _,cl in rules[colour]:
        if cl == testColour:
            doesContain = True
        else:
            if cl not in memo:
                _check_contains(testColour, rules, cl, memo)
            if memo[cl]:
                doesContain = True
    memo[colour] = doesContain

def find_that_contain(testColour, rules):
    ## find colours (in rules) that (recursively) contain at least one of testColour
    memo = dict()
    goodColours = []
    for aCol in rules:
        if aCol not in memo:
            _check_contains(testColour, rules, aCol, memo)
        if memo[aCol]:
            goodColours.append(aCol)
    return goodColours

example_rules = dict(parseRule(ln.strip()) for ln in example_input.split("\n") if ln.strip())
example_contain_shinygold = find_that_contain("shiny gold", example_rules)
print(len(example_contain_shinygold), example_contain_shinygold)
# -

with open("inputs/day07.txt") as inF:
    puzzle_rules = dict(parseRule(ln.strip()) for ln in inF if ln.strip())
print(len(find_that_contain("shiny gold", puzzle_rules)))

# ## Part 2

# +
example2_input = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

def number_inside(colour, rules):
    return sum(n*(1+number_inside(aCol, rules)) for n, aCol in rules[colour])

example2_rules = dict(parseRule(ln.strip()) for ln in example2_input.split("\n") if ln.strip())
print(number_inside("shiny gold", example2_rules))
# -

print(number_inside("shiny gold", puzzle_rules))
