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

# # Advent of code 2020: day 22
#
# Problem [here](https://adventofcode.com/2020/day/22)

# ## Part 1

# +
ex_a = [ 9, 2, 6, 3, 1 ]
ex_b = [ 5, 8, 4, 7, 10 ]

def playGame1(deckA, deckB):
    while deckA and deckB:
        if len(deckA) > len(deckB):
            newA = deckA[len(deckB):]
            newB = []
        else:
            newB = deckB[len(deckA):]
            newA = []
        for i,(a,b) in enumerate(zip(deckA, deckB)): # shortest
            if a > b:
                newA.append(a)
                newA.append(b)
            else:
                newB.append(b)
                newB.append(a)
        deckA = newA
        deckB = newB
    score = 0
    if deckA:
        for i,a in enumerate(reversed(deckA), 1):
            score += i*a
    else:
        for i,b in enumerate(reversed(deckB), 1):
            score += i*b
    return deckA, deckB, score

print(playGame1(ex_a, ex_b))

# +
puz_a, puz_b = [], []
with open("inputs/day22.txt") as inF:
    assert next(inF).strip() == "Player 1:"
    while ln := next(inF).strip():
        puz_a.append(int(ln))
    assert next(inF).strip() == "Player 2:"
    try:
        while ln := next(inF).strip():
            puz_b.append(int(ln))
    except StopIteration:
        pass
print(len(puz_a), len(puz_b), puz_a, puz_b)

f_a, f_b, p_score = playGame1(puz_a, puz_b)
print(p_score)


# -

# ## Part 2

# +
def playGame2(deckA, deckB, debug=False, iGame=1):
    if debug:
        print(f"\n== Game {iGame:d} ==")
    history = set()
    infinite = False
    rnd = 1
    while deckA and deckB and not infinite:
        if debug:
            print(f"\n-- Round {rnd:d} (Game {iGame:d}) --")
            print(f"Player 1's deck: {', '.join(str(n) for n in deckA)}")
            print(f"Player 2's deck: {', '.join(str(n) for n in deckB)}")
            print(f"Player 1 plays: {deckA[0]:d}")
            print(f"Player 2 plays: {deckB[0]:d}")
        a = deckA[0]
        b = deckB[0]
        if a < len(deckA) and b < len(deckB):
            if debug:
                print(f"Playing subgame with {deckA[1:a+1]!r} and {deckB[1:b+1]!r}")
            subA, subB, _ = playGame2(deckA[1:a+1], deckB[1:b+1], debug=debug, iGame=iGame+1)
            aWon = len(subA) != 0
        else:
            aWon = a > b
        if aWon:
            if debug:
                print(f"Player 1 wins round {rnd} of game {iGame:d}!")
            deckA = deckA[1:] + [ a, b ]
            deckB = deckB[1:]
        else:
            if debug:
                print(f"Player 2 wins round {rnd} of game {iGame:d}!")
            deckA = deckA[1:]
            deckB = deckB[1:] + [ b, a ]
        hsh = hash((tuple(deckA), tuple(deckB)))
        infinite = hsh in history
        history.add(hsh)
        rnd += 1
    if infinite and debug:
        print("Infinite recursion break, player 1 wins")
    score = 0
    if infinite or deckA:
        for i,a in enumerate(reversed(deckA), 1):
            score += i*a
    else:
        for i,b in enumerate(reversed(deckB), 1):
            score += i*b
    return deckA, deckB, score

playGame2([43, 19], [2, 29, 14], debug=True)
# -

playGame2(ex_a, ex_b, debug=True)

f_a, f_b, p_score = playGame2(puz_a, puz_b, debug=False)
print(p_score)
