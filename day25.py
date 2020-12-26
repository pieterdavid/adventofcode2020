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

# # Advent of code 2020: day 25
#
# Problem [here](https://adventofcode.com/2020/day/25)

# +
def cryptTransform1(subject, loopSize=1):
    value = 1
    for i in range(loopSize):
        value = (value*subject) % 20201227
    return value

print(cryptTransform1(7, 8), cryptTransform1(7, 11))
print(cryptTransform1(17807724, 8), cryptTransform1(5764801, 11))


# +
def findLoopSizes(subject, values, findAny=False):
    sizes = dict()
    value = 1
    i = 0
    while len(sizes) != len(values):
        if value in values:
            sizes[value] = i
            if findAny:
                return sizes
        value = (value*subject) % 20201227
        i += 1
    return sizes

print(findLoopSizes(7, [17807724, 5764801]))
print(findLoopSizes(7, [17807724, 5764801], findAny=True))
# -

print(findLoopSizes(7, [1965712, 19072108], findAny=True))

print(cryptTransform1(1965712, 7177897))
