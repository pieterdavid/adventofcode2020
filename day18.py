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

# # Advent of code 2020: day 18
#
# Problem [here](https://adventofcode.com/2020/day/18)

# ## Part 1

# +
ex_in = "1 + 2 * 3 + 4 * 5 + 6"

def execute_noParen(expr):
    tokens = iter(expr.split())
    result = int(next(tokens))
    try:
        while True:
            op = next(tokens)
            val = next(tokens)
            if op == "+":
                result += int(val)
            elif op == "*":
                result *= int(val)
    except StopIteration:
        pass
    return result

print(execute_noParen(ex_in))

# +
import re
patSub = re.compile("\([0-9\+\* ]+\)")
def execute_with_subexpr(expr, execNoParen=execute_noParen):
    while m := patSub.search(expr):
        subRes = execNoParen(expr[m.start()+1:m.end()-1])
        expr = "".join((expr[:m.start()], str(subRes), expr[m.end():]))
    return execNoParen(expr)

examples = [
    "2 * 3 + (4 * 5)",
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
]
for ex_in in examples:
    print(ex_in, execute_with_subexpr(ex_in))

# +
with open("inputs/day18.txt") as inF:
    puzzle_expressions = [ ln.strip() for ln in inF if ln.strip() ]

print(sum(execute_with_subexpr(expr) for expr in puzzle_expressions))


# -

# ## Part 2

# +
def execute_noParen_2(expr):
    res = 1
    for factor in expr.split(" * "):
        res *= sum(int(tk) for tk in factor.split(" + "))
    return res

print(execute_noParen_2("1 + 2 * 3 + 4 * 5 + 6"))
print(execute_with_subexpr("1 + (2 * 3) + (4 * (5 + 6))", execNoParen=execute_noParen_2))
for ex_in in examples:
    print(ex_in, execute_with_subexpr(ex_in, execNoParen=execute_noParen_2))
# -

print(sum(execute_with_subexpr(expr, execNoParen=execute_noParen_2) for expr in puzzle_expressions))
