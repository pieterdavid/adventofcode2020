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

# # Advent of code 2020: day 8
#
# Problem [here](https://adventofcode.com/2020/day/8)
#
# ## Part 1

# +
example_input = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

def parse_instructions(lines):
    instructions = []
    for ln in lines:
        instr,arg = ln.split()
        instructions.append((instr, int(arg)))
    return instructions

def execute_break_loop(instructions, debug=False, silent=False, tryFix=False, pos=0, acc=0, stack=None):
    executed = stack if stack else []
    while pos not in executed and pos < len(instructions):
        instr, arg = instructions[pos]
        if debug:
            print(f"DEBUG: Executing #{pos:d}: {instr} {arg:d}")
        if instr == "nop":
            nPos = pos+1
        elif instr == "acc":
            acc += arg
            nPos = pos+1
        elif instr == "jmp":
            nPos = pos+arg
        executed.append(pos)
        pos = nPos
    if pos in executed and tryFix: ## This part added for part 2
        if not silent:
            print("Detected loop, stepping back and trying to fix")
        rAcc = acc
        for i,rPos in enumerate(reversed(executed)):
            rInstr, rArg = instructions[rPos]
            if rInstr == "nop":
                tryInstr = list(instructions)
                tryInstr[rPos] = ("jmp", rArg)
                if debug:
                    print(f"Trying to fix by changing line {rPos:d} from '{rInstr} {rArg:d}' to 'jmp {rArg:d}'")
                tPos, tAcc = execute_break_loop(tryInstr, silent=(not debug), tryFix=False,
                                                pos=rPos, acc=rAcc, stack=executed[:-1-i])
                if tPos == len(instructions):
                    pos, acc = tPos, tAcc
                    break
            elif rInstr == "jmp":
                tryInstr = list(instructions)
                tryInstr[rPos] = ("nop", rArg)
                if debug:
                    print(f"Trying to fix by changing line {rPos:d} from '{rInstr} {rArg:d}' to 'nop {rArg:d}'")
                tPos, tAcc = execute_break_loop(tryInstr, silent=(not debug), tryFix=False,
                                                pos=rPos, acc=rAcc, stack=executed[:-1-i])                    
                if tPos == len(instructions):
                    pos, acc = tPos, tAcc
                    break
            elif rInstr == "acc":
                rAcc -= rArg
    if not silent:
        if pos in executed:
            print(f"Executing instruction {pos:d} for a second time. Accumulator value is {acc:d}")
        elif pos == len(instructions):
            print(f"Terminated successfully! Accumulator is {acc:d}")
    return pos, acc

example_instructions = parse_instructions((ln.strip() for ln in example_input.split("\n") if ln.strip()))
execute_break_loop(example_instructions, debug=True)
# -

with open("inputs/day08.txt") as inF:
    puzzle_instructions = parse_instructions((ln.strip() for ln in inF if ln.strip()))
execute_break_loop(puzzle_instructions)

# ## Part 2

example_input_fixed = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
nop -4
acc +6
"""
example_instructions_fixed = parse_instructions((ln.strip() for ln in example_input_fixed.split("\n") if ln.strip()))
execute_break_loop(example_instructions_fixed, debug=True)
execute_break_loop(example_instructions, debug=True, tryFix=True)

execute_break_loop(puzzle_instructions, debug=False, tryFix=True)
