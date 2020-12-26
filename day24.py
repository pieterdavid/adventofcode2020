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

# # Advent of code 2020: day 24
#
# Problem [here](https://adventofcode.com/2020/day/24)

# +
ex_in = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

def parseInstructions(lines):
    out = []
    for ln in lines:
        lnOut = []
        chars = iter(ln)
        ch = next(chars)
        try:
            prev = None
            while True:
                if ch in ("e", "w"):
                    if prev:
                        lnOut.append("".join((prev, ch)))
                    else:
                        lnOut.append(ch)
                    prev = None
                else:
                    prev = ch
                ch = next(chars)
        except StopIteration:
            pass
        out.append(lnOut)
    return out

ex_instructions = parseInstructions(ex_in.split("\n"))

# +
import numpy as np

def tileRoom1(instructions, debug=False):
    center = 1,1
    roomTiles = np.full((3,3), False, dtype=np.bool)
    for inLn in instructions:
        i,j = center
        for step in inLn:
            if step == "e":
                j += 1
            elif step == "w":
                j -= 1
            elif step == "ne":
                i -= 1
            elif step == "sw":
                i += 1
            elif step == "nw":
                i -= 1
                j -= 1
            elif step == "se":
                i += 1
                j += 1
            if i < 0:
                nExt = roomTiles.shape[0]
                roomTiles = np.vstack((np.full(roomTiles.shape, False, dtype=np.bool), roomTiles))
                i += nExt
                center = center[0]+nExt, center[1]
            elif i == roomTiles.shape[0]:
                roomTiles = np.vstack((roomTiles, np.full(roomTiles.shape, False, dtype=np.bool)))
            if j < 0:
                nExt = roomTiles.shape[1]
                roomTiles = np.hstack((np.full(roomTiles.shape, False, dtype=np.bool), roomTiles))
                j += nExt
                center = center[0], center[1]+nExt
            elif j == roomTiles.shape[1]:
                roomTiles = np.hstack((roomTiles, np.full(roomTiles.shape, False, dtype=np.bool)))
        if debug:
            if roomTiles[i,j]:
                print(f"Flipping {i:d},{j:d} back to white")
            else:
                print(f"Flipping {i:d},{j:d} to black")
        roomTiles[i,j] = not roomTiles[i,j]
    return roomTiles

ex_tiled = tileRoom1(ex_instructions, debug=True)
print(np.sum(ex_tiled))

# +
with open("inputs/day24.txt") as inF:
    p_instructions = parseInstructions((ln.strip() for ln in inF if ln.strip()))

p_tiled = tileRoom1(p_instructions)
print(np.sum(p_tiled))


# -

# ## Part 2

# +
def evolveTiles(tiles, nDays):
    for i in range(nDays):
        extShp = tuple(dm+2 for dm in tiles.shape)
        nBN = np.zeros(extShp, dtype=np.int)
        nBN[:-2,1:-1]   += tiles # E
        nBN[2: ,1:-1]   += tiles # W
        nBN[1:-1,:-2]   += tiles # SW
        nBN[1:-1,2: ]   += tiles # NE
        nBN[:-2,:-2]    += tiles # SE
        nBN[2:,2:]      += tiles # NW
        if np.any(nBN[0,:] == 2):
            tiles = np.vstack((np.full((1, tiles.shape[1]), False, dtype=np.bool), tiles))
        else:
            nBN = nBN[1:,:]
        if np.any(nBN[-1,:] == 2):
            tiles = np.vstack((tiles, np.full((1, tiles.shape[1]), False, dtype=np.bool)))
        else:
            nBN = nBN[:-1,:]
        if np.any(nBN[:,0] == 2):
            tiles = np.hstack((np.full((tiles.shape[0], 1), False, dtype=np.bool), tiles))
        else:
            nBN = nBN[:,1:]
        if np.any(nBN[:,-1] == 2):
            tiles = np.hstack((tiles, np.full((tiles.shape[0], 1), False, dtype=np.bool)))
        else:
            nBN = nBN[:,:-1]
        assert nBN.shape == tiles.shape
        msk_toFlip = np.logical_or(
            np.logical_and(tiles, # black and 0 or >2 black -> white
                           np.logical_or(nBN == 0, nBN > 2)),
            np.logical_and(np.logical_not(tiles), # white and 2 black neighbours -> black
                           nBN == 2)
        )
        tiles[msk_toFlip] = np.logical_not(tiles[msk_toFlip])
    return tiles

ex_tiled2 = tileRoom1(ex_instructions, debug=False)
for i in range(10):
    ex_tiled2 = evolveTiles(ex_tiled2, 1)
    print(f"Day {i+1:d}: {np.sum(ex_tiled2):d}")
for i in range(20, 101, 10):
    ex_tiled2 = evolveTiles(ex_tiled2, 10)
    print(f"Day {i:d}: {np.sum(ex_tiled2):d}")
# -

p_tiled = tileRoom1(p_instructions)
p_tiled = evolveTiles(p_tiled, 100)
print(np.sum(p_tiled))
