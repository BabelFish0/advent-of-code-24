import numpy as np
import copy
import time

def printer(state):
    BLUE = '\033[44m'
    CYAN = '\033[46m'
    BLANK = '\033[100m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    RESET = '\033[0m'
    for row in state:
        for entry in row:
            if entry == 1: # dish
                print(CYAN + '  ', end='')
            if entry == 0:
                print(BLANK + '  ', end='')
            if entry == 2: # collinear resonance
                print(GREEN + '  ', end='')
            if entry == 3: # dish overlayed with resonance
                print(RED + '  ', end='')
        print(RESET)

def give_dish_coords(grid):
    '''return dict with each dish character and their positions'''
    positions = {}
    for dish_coord in np.transpose(np.nonzero(grid!='.')):
        if grid[dish_coord[0], dish_coord[1]] in positions.keys():
            positions[grid[dish_coord[0], dish_coord[1]]] += [dish_coord]
        else:
            positions[grid[dish_coord[0], dish_coord[1]]] = [dish_coord]
    return positions

def minimum_int_vector(v1, v2):
    '''shortest integer vector between two dishes'''
    direction = (v1-v2).astype(np.int64)
    out = None
    mag = 1
    while mag < np.linalg.norm(direction):
        if not np.sum(direction//mag != direction / mag):
            out = direction//mag
        mag += 1
    return out

def give_antinodes(v1, v2, bounds:tuple):
    '''work forewards then backwards to find integer points on the line'''
    vector = minimum_int_vector(v1, v2)
    out = copy.deepcopy(v1)
    while 0<=out[0]<bounds[0] and 0<=out[1]<bounds[1]:
        yield copy.deepcopy(out)
        out += vector
    out = v1 - vector
    while 0<=out[0]<bounds[0] and 0<=out[1]<bounds[1]:
        yield copy.deepcopy(out)
        out -= vector

def main():
    t0 = time.perf_counter()
    INPUT = './input/day8-1.txt'
    grid = np.array([[e for e in row] for row in np.loadtxt(INPUT, dtype=np.str_, comments=None)])
    antinodes = np.zeros(shape=np.shape(grid))
    positions = give_dish_coords(grid)
    for key in positions:
        for idx, p1 in enumerate(positions[key]):
            for p2 in positions[key][idx+1:]:
                for position in give_antinodes(p1, p2, np.shape(grid)):
                    antinodes[position[0], position[1]] = 1
    print('\033[100m'+'─'*2*len(grid[0])+'\033[0m')
    printer((grid!='.').astype(np.int64) + 2*antinodes)
    print('\033[100m'+'─'*2*len(grid[0])+'\033[0m')
    print(f'total: \033[45m{np.sum(antinodes).astype(np.int64)}\033[0m in {time.perf_counter()-t0:.2}s.')

main()