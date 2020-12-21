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

# # Advent of code 2020: day 20
#
# Problem [here](https://adventofcode.com/2020/day/20)

# ## Part 1

# +
def boolsToInt(values):
    return sum(1<<i for i,v in enumerate(reversed(values)) if v)

class Tile:
    """
    Tile, storing id and edges converted to integer (normal and reversed, so 8 possibilities)
    """
    def __init__(self, uid, values):
        self.uid = uid
        self.edges = Tile.makeEdges(values)
        self.values = values
    @staticmethod
    def makeEdges(values):
        return tuple([
            boolsToInt(values[0,:]),     ## N: top row, L->R
            boolsToInt(values[:,-1]),    ## E: rightmost column, T->B
            boolsToInt(values[-1,:]),    ## S: bottom row, L->R
            boolsToInt(values[:,0]),     ## W: leftmost column, T->B
            boolsToInt(values[0,::-1]),  ## -N
            boolsToInt(values[::-1,-1]), ## -E
            boolsToInt(values[-1,::-1]), ## -S
            boolsToInt(values[::-1,0])   ## -W
        ])

import numpy as np
def readTiles(iLines):
    tiles = {}
    try:
        while True:
            hdr = next(iLines)
            assert hdr.startswith("Tile ") and hdr.endswith(":")
            tileId = int(hdr[5:-1])
            tileVals = []
            while ln := next(iLines):
                tileVals.append([ (ch == "#") for ch in ln ])
            tiles[tileId] = Tile(tileId, np.array(tileVals))
    except StopIteration:
        tiles[tileId] = Tile(tileId, np.array(tileVals))
    return tiles

with open("inputs/day20_ex1.txt") as exInF:
    ex1_tiles = readTiles((ln.strip() for ln in exInF))

# +
from collections import defaultdict

def getTilesStats(tiles):
    tilesPerEdge = defaultdict(list)
    for tl in tiles:
        for ed in tl.edges:
            tilesPerEdge[ed].append(tl.uid)
    h_edgesPerTile = defaultdict(int)
    for ed,edTiles in tilesPerEdge.items():
        h_edgesPerTile[len(edTiles)] += 1
    return tilesPerEdge, h_edgesPerTile

ex1_tPerEdge, ex1_hEdgesPerTile = getTilesStats(ex1_tiles.values())
for nTiles in sorted(ex1_hEdgesPerTile.keys()):
    print(f"Number of edges present in {nTiles:d} tiles: {ex1_hEdgesPerTile[nTiles]:d}")

# +
tileOrientations = [
    (0, 1, 2, 3), #  N E S W = leave
    (1, 6, 3, 4), #  E-S W-N = np.rot90
    (6, 7, 4, 5), # -S-W-N-E = np.rot90(, k=2)
    (7, 0, 5, 2), # -W N-E S = np.rot90(, k=-1)
    (4, 3, 6, 1), # -N W-S E = fliplr
    (5, 4, 7, 6), # -E-N-W-S = np.rot90(fliplr, k=-1)
    (2, 5, 0, 7), #  S-E N-W = flipud
    (3, 2, 1, 0)] #  W S E N = transpose
edgeOfOther = (2, 3, 0, 1) # N<->S, E<->W

def getCorners(tiles, perEdge):
    corners = []
    for tl in tiles:
        unMatched = []
        for i,ed in enumerate(tl.edges):
            tlForEd = perEdge[ed]
            if len(tlForEd) == 1:
                unMatched.append(i)
        if min(sum(1 for ie in ori if ie in unMatched) for ori in tileOrientations) == 2:
            corners.append(tl)
    return corners

ex1_corners = getCorners(ex1_tiles.values(), ex1_tPerEdge)
print(f"Corner tile(s): {', '.join(str(tl.uid) for tl in ex1_corners)}")

if len(ex1_corners) == 4:
    p = 1
    for tl in ex1_corners:
        p *= tl.uid
    print(f"Product of corner tile IDs: {p:d}")
# -

with open("inputs/day20.txt") as inF:
    p_tiles = readTiles((ln.strip() for ln in inF))
print(len(p_tiles))
p_tPerEdge, p_hEdgesPerTile = getTilesStats(p_tiles.values())
p_corners = getCorners(p_tiles.values(), p_tPerEdge)
print(f"Corner tile(s): {', '.join(str(tl.uid) for tl in p_corners)}")
if len(p_corners) == 4:
    p = 1
    for tl in p_corners:
        p *= tl.uid
    print(f"Product of corner tile IDs: {p:d}")


# ## Part 2

# +
def getNeighboursFilled(solution):
    nFilled = np.zeros(tuple(list(solution.shape)[:2]), dtype=np.int)
    ones = np.ones(nFilled.shape, dtype=np.int)
    zeros = np.zeros(nFilled.shape, dtype=np.int)
    nFilled[1: , : ] += np.where(solution[:-1, : ,0] != 0, ones[1:,:], zeros[1:,:])
    nFilled[:-1, : ] += np.where(solution[1: , : ,0] != 0, ones[1:,:], zeros[1:,:])
    nFilled[ : ,1: ] += np.where(solution[ : ,:-1,0] != 0, ones[:,1:], zeros[:,1:])
    nFilled[ : ,:-1] += np.where(solution[ : ,1: ,0] != 0, ones[:,1:], zeros[:,1:])
    return nFilled

def positionRequires(solution, pos, allTiles):
    i,j = pos
    requires = [None]*4
    if i != 0 and solution[i-1,j,0]: # above
        oId, oOri = solution[i-1,j]
        requires[0] = allTiles[oId].edges[tileOrientations[oOri][edgeOfOther[0]]]
    if j+1 != solution.shape[1] and solution[i,j+1,0]: # right
        oId, oOri = solution[i,j+1]
        requires[1] = allTiles[oId].edges[tileOrientations[oOri][edgeOfOther[1]]]
    if i+1 != solution.shape[0] and solution[i+1,j,0]: # above
        oId, oOri = solution[i+1,j]
        requires[2] = allTiles[oId].edges[tileOrientations[oOri][edgeOfOther[2]]]
    if j != 0 and solution[i,j-1,0]: # left
        oId, oOri = solution[i,j-1]
        requires[3] = allTiles[oId].edges[tileOrientations[oOri][edgeOfOther[3]]]
    return requires

from itertools import product

def makePuzzle(n, tiles, perEdge):
    corners = getCorners(tiles.values(), perEdge)
    startTile = corners[0]
    startTile_ors = [ i for i,ori in enumerate(tileOrientations)
                     if len(perEdge[startTile.edges[ori[0]]]) == 1
                     and len(perEdge[startTile.edges[ori[3]]]) == 1 ]
    print(f"Starting with {startTile.uid} at (0,0) in orientation {startTile_ors[0]:d}")
    solution = np.stack((np.zeros((n,n), dtype=np.int), -1*np.ones((n,n), dtype=np.int)), axis=2)
    solution[0,0] = [ startTile.uid, startTile_ors[0]]
    sol_history = [((0, 0), startTile_ors[1:])]
    usedTiles = set()
    usedTiles.add(startTile.uid)
    trialIsValid = True
    while np.any(solution[:,:,0] == 0):
        if not trialIsValid:
            while sol_history and not sol_history[-1][1]:
                (i,j), _ = sol_history[-1]
                del sol_history[-1]
                tlId = solution[i,j,0]
                solution[i,j] = [0, -1]
                usedTiles.discard(tlId)
            if not sol_history:
                raise RuntimeError("Stuck and cannot roll back")
            (i,j), otherOptions = sol_history[-1]
            solution[i,j,1] = otherOptions[0]
            sol_history[-1] = ((i,j), otherOptions[1:])
            print(f"Rolled back until position ({i:d}, {j:d}), now taking orientation {otherOptions[0]:d}")
            trialIsValid = True
        else:
            nReq = 4
            while nReq and trialIsValid:
                neighFilled = getNeighboursFilled(solution)
                if np.any(np.logical_and(neighFilled == nReq, solution[:,:,0] == 0)):
                    nFilled = 0
                    with np.nditer(neighFilled, flags=['multi_index']) as it:
                        for nN in it:
                            i,j = it.multi_index
                            if nN == nReq and solution[i,j,0] == 0:
                                req = positionRequires(solution, (i,j), tiles)
                                print(f"Checking for ({i:d},{j:d}), needs {req!r}")
                                options = []
                                for tl, (k,ori) in product(tiles.values(), enumerate(tileOrientations)):
                                    if tl.uid not in usedTiles:
                                        if all(tl.edges[i] == rq for i,rq in zip(ori,req) if rq is not None):
                                            options.append((tl.uid, k))
                                if not options:
                                    trialIsValid = False
                                    print(solution[:,:,0])
                                    print("No options, we're stuck")
                                    for tl, (k,ori) in product(tiles.values(), enumerate(tileOrientations)):
                                        if tl.uid not in usedTiles:
                                            print(f"{tl.uid:d} ori {k:d}: ({', '.join(str(tl.edges[i]) for i in ori)})")
                                    break ## a problem
                                else:
                                    nFilled += 1
                                    tlid, kO = options[0]
                                    print(f"Putting tile {tlid:d} at ({i:d},{j:d}) with orientation {kO:d} ({', '.join(str(tiles[tlid].edges[i]) for i in tileOrientations[kO])})")
                                    solution[i,j] = [ tlid, kO ]
                                    sol_history.append(((i,j), options[1:]))
                                    usedTiles.add(tlid)
                    if nFilled:
                        break # try again with more
                else:
                    nReq -= 1
    if trialIsValid:
        print(solution[:,:,0])
        return solution

ex_solution = makePuzzle(3, ex1_tiles, ex1_tPerEdge)
# -

p_solution = makePuzzle(12, p_tiles, p_tPerEdge)

# +
oriTransforms = [
    lambda a : a,                            #  N E S W = leave
    lambda a : np.rot90(a),                  #  E-S W-N = np.rot90
    lambda a : np.rot90(a, k=2),             # -S-W-N-E = np.rot90(, k=2)
    lambda a : np.rot90(a, k=-1),            # -W N-E S = np.rot90(, k=-1)
    lambda a : np.fliplr(a),                 # -N W-S E = fliplr
    lambda a : np.rot90(np.fliplr(a), k=-1), # -E-N-W-S = np.rot90(fliplr, k=-1)
    lambda a : np.flipud(a),                 #  S-E N-W = flipud
    lambda a : np.transpose(a)]              #  W S E N = transpose

m = np.array([ [ 1., 2., 3. ], [ 4., 5., 6. ], [ 7., 8., 9. ] ])
for i,t in enumerate(oriTransforms):
    print(i, t(m))
# -

ex1_full = [ [ oriTransforms[ori](ex1_tiles[uid].values) for uid,ori in row ] for row in ex_solution ]
p_full = [ [ oriTransforms[ori](p_tiles[uid].values) for uid,ori in row ] for row in p_solution ]


# +
def getLineStr(arr):
    return [ "".join(("#" if ch else ".") for ch in row) for row in arr ]

for i,row in enumerate(ex1_full):
    for linePerBlock in zip(*(getLineStr(tile) for tile in row)):
        print(" ".join(linePerBlock))
    print("")
# -

ex_merged = np.vstack((np.hstack((vals[1:-1,1:-1] for vals in row)) for row in ex1_full)).T
print("\n".join("".join(("#" if ch else ".") for ch in row) for row in ex_merged))

p_merged = np.vstack((np.hstack((vals[1:-1,1:-1] for vals in row)) for row in p_full)).T

monster_pat = np.array([ [(True if ch == "#" else False) for ch in row] for row in """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.split("\n") ], dtype=np.bool)

ex_nMonsters = 0
ex_monsters = []
for k,tr in enumerate(oriTransforms):
    t_m = tr(monster_pat)
    for i in range(ex_merged.shape[0]-t_m.shape[0]):
        for j in range(ex_merged.shape[1]-t_m.shape[1]):
            if np.all(t_m == np.logical_and(ex_merged[i:i+t_m.shape[0], j:j+t_m.shape[1]], t_m)):
                ex_monsters.append(((i,j), k))
                ex_nMonsters += 1
print(f"Example monsters: {ex_nMonsters:d}, {ex_monsters!r}")
ex_forRough = np.array(ex_merged)
for (i,j), k in ex_monsters:
    t_m = oriTransforms[k](monster_pat)
    ex_forRough[i:i+t_m.shape[0], j:j+t_m.shape[1]] = np.where(
        np.logical_and(ex_forRough[i:i+t_m.shape[0], j:j+t_m.shape[1]], t_m),
        np.full(t_m.shape, False), ex_forRough[i:i+t_m.shape[0], j:j+t_m.shape[1]])
print(f"Example roughness: {np.sum(ex_forRough):d}")

p_nMonsters = 0
p_monsters = []
for k,tr in enumerate(oriTransforms):
    t_m = tr(monster_pat)
    for i in range(p_merged.shape[0]-t_m.shape[0]):
        for j in range(p_merged.shape[1]-t_m.shape[1]):
            if np.all(t_m == np.logical_and(p_merged[i:i+t_m.shape[0], j:j+t_m.shape[1]], t_m)):
                p_monsters.append(((i,j), k))
                p_nMonsters += 1
print(f"Puzzle monsters: {p_nMonsters:d}, {p_monsters!r}")
p_forRough = np.array(p_merged)
for (i,j), k in p_monsters:
    t_m = oriTransforms[k](monster_pat)
    p_forRough[i:i+t_m.shape[0], j:j+t_m.shape[1]] = np.where(
        np.logical_and(p_forRough[i:i+t_m.shape[0], j:j+t_m.shape[1]], t_m),
        np.full(t_m.shape, False), p_forRough[i:i+t_m.shape[0], j:j+t_m.shape[1]])
print(f"Puzzle roughness: {np.sum(p_forRough):d}")
