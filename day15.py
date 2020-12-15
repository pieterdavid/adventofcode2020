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

# # Advent of code 2020: day 15
#
# Problem [here](https://adventofcode.com/2020/day/15)

# ## Part 1

# +
class MemoryGame:
    def __init__(self):
        self.mem = dict()
        self.count = 0
        self.last = None
    def add(self, nb, debug=False):
        prev,_ = self.mem.get(nb, (None, None))
        intv = ((self.count-prev) if prev is not None else 0)
        if debug:
            print(f"Adding {nb:d} as number {self.count:d}, past {intv}")
        self.mem[nb] = (self.count, intv)
        self.last = nb
        self.count += 1
    def runUntil(self, mx, debug=False):
        while self.count != mx:
            _,intv = self.mem[self.last]
            self.add(intv, debug=debug)
        return self.last

ex_game = MemoryGame()
for nb in [0, 3, 6]:
    ex_game.add(nb, debug=True)
ex_game.runUntil(10, debug=True)
print(ex_game.runUntil(2020))
# -

for ex_init in [ [1,3,2], [2,1,3], [1,2,3], [2,3,1], [3,2,1], [3,1,2] ]:
    gm = MemoryGame()
    for nb in ex_init:
        gm.add(nb)
    print(ex_init, gm.runUntil(2020))

p1_gm = MemoryGame()
for inb in [0,13,1,16,6,17]:
    p1_gm.add(inb)
print(p1_gm.runUntil(2020))

# ## Part 2

print(ex_game.runUntil(30000000))

print(p1_gm.runUntil(30000000))
