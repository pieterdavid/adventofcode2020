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

# # Advent of code 2020: day 14
#
# Problem [here](https://adventofcode.com/2020/day/14)

print(bin(0xfa), 0xfa)
print(int("11111010", 2))
print(bin((0x1<<36)-1))

# ## Part 1

# +
class BitMask:
    def __init__(self, strRepr):
        self.mask = int("".join(("0" if ch == "X" else "1") for ch in strRepr), 2)
        self.val  = int("".join(("0" if ch == "X" else ch) for ch in strRepr), 2)
    def mod1(self, num):
        return (num&(~self.mask)) + (self.val&self.mask)
    def __str__(self):
        msk_s = f"{self.mask:036b}"
        val_s = f"{self.val:036b}"
        return "".join(("X" if mc == "0" else vc) for mc,vc in zip(msk_s, val_s))

ex_mask = BitMask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
print(str(ex_mask))
# -

for ex_val in (11, 101, 0):
    print(f"value:  {ex_val:036b} (decimal {ex_val})")
    print(f"mask:   {ex_mask!s}")
    res = ex_mask.mod1(ex_val)
    print(f"result: {res:036b} (decimal {res})")


def init(mem, lines, msk=None):
    if not msk:
        msk = BitMask("X"*36)
    for ln in lines:
        cmd, val = ln.split(" = ")
        if cmd == "mask":
            msk = BitMask(val)
        elif cmd.startswith("mem[") and cmd.endswith("]"):
            ky = int(cmd[4:-1])
            mem[ky] = msk.mod1(int(val))
        else:
            raise RuntimeError()
    return msk


# +
ex_in = list("""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".split("\n"))

from collections import defaultdict
ex_mem = defaultdict(int)
msk = init(ex_mem, ex_in)
print(sum(ex_mem.values()), str(msk), ex_mem)

# +
with open("inputs/day14.txt") as inF:
    puz_lines = [ ln.strip() for ln in inF if ln.strip() ]

mem = defaultdict(int)
msk = init(mem, puz_lines)
print(msk, sum(mem.values()))
# -

# ## Part 2

ex_mask = BitMask("000000000000000000000000000000X1001X")
adr = 0b000000000000000000000000000000101010
print(f"address:  {adr:036b} (decimal {adr})")
print(f"mask:     {ex_mask!s}")
print(f"result:   {adr|ex_mask.val:036b}")
print(f"result-m: {(adr|ex_mask.val)&ex_mask.mask:036b}")


# +
def adrFor(adr, aMask):
    toCh = []
    for i in range(36):
        test = 0x1<<i
        if (~aMask) & test: ## is an X
            toCh.append(test)
    vals = []
    for i in range(2**len(toCh)):
        yield (adr&aMask) + sum((ch if i&(0x1<<j) else 0) for j,ch in enumerate(toCh))

ex_adr = 0b000000000000000000000000000000101010
ex_msk = BitMask("000000000000000000000000000000X1001X")
print("\n".join(f"{v:036b}" for v in adrFor(ex_adr|ex_mask.val, ex_msk.mask)))
# -

ex_adr2 = 0b000000000000000000000000000000011010
ex_msk2 = BitMask("00000000000000000000000000000000X0XX")
print("\n".join(f"{v:036b}" for v in adrFor(ex_adr2|ex_msk2.val, ex_msk2.mask)))


# +
def sumMemory(inLines):
    initInstr = []
    i = 0
    mem = dict()
    msk = None
    while i != len(inLines):
        cmd, val = inLines[i].split(" = ")
        if cmd == "mask":
            msk = BitMask(inLines[i].split(" = ")[1])
        elif cmd.startswith("mem[") and cmd.endswith("]"):
            ky = int(cmd[4:-1])
            val = int(val)
            for adr in adrFor(ky|msk.val, msk.mask):
                mem[adr] = val
        else:
            raise RuntimeError("Unknown command")
        i += 1
    return sum(mem.values())

ex2_in = list("""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".split("\n"))


print(sumMemory(ex2_in))
# -

print(sumMemory(puz_lines))
