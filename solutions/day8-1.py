import numpy as np

def printer(state):
    BLUE = '\033[44m'
    CYAN = '\033[46m'
    BLANK = '\033[100m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    RESET = '\033[0m'
    for row in state:
        for entry in row:
            if entry == 1:
                print(CYAN + '  ', end='')
            if entry == 0:
                print(BLANK + '  ', end='')
            if entry == 2:
                print(GREEN + '  ', end='')
            if entry == 3:
                print(RED + '  ', end='')
            # if entry > 1:
            #     print(BLUE + ' ', end='')
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

def give_antinode(v1, v2):
    return 2*v1-v2

def main():
    INPUT = './input/day8-1.txt'
    grid = np.array([[e for e in row] for row in np.loadtxt(INPUT, dtype=np.str_, comments=None)])
    antinodes = np.zeros(shape=np.shape(grid))
    positions = give_dish_coords(grid)
    for key in positions:
        for p1 in positions[key]:
            for p2 in positions[key]:
                if np.sum(p1!=p2) > 0:
                    position = give_antinode(p1, p2)
                    if 0<=position[0]<= np.shape(grid)[0]-1 and 0<=position[1]<= np.shape(grid)[1]-1:
                        antinodes[position[0], position[1]] = 1
    printer((grid!='.').astype(np.int64) + 2*antinodes)
    print(np.sum(antinodes))
main()