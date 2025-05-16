import numpy as np
from utils.progress import Printer

def simulate(pos:np.ndarray, vels:np.ndarray, s:int=1) -> np.ndarray:
    width, height = 101, 103
    offset = pos + vels*s
    offset = np.column_stack((offset[:,0] % width, offset[:,1] % height))
    return offset

def display(pos, p=Printer()):
        grid = np.zeros(shape=(103,101))
        for idx in pos:
            grid[idx[1], idx[0]] = 1
        p.arrprint(grid, width=1)

def suspicious(pos, threshold=100):
    n_adjacent = 0
    for coord in pos:
        dists = np.abs(pos-coord)
        mask = (dists==1).astype(np.int64)
        adjacent = (mask[:,0]*mask[:,1]).astype(bool)
        n_adjacent+=np.sum(adjacent)
    return n_adjacent

def main():
    import re
    with open('./input/day14-1.txt') as INPUT:
        pos, vel = [], []
        for line in INPUT.readlines():
            res = re.compile('p=(\d+),(\d+) v=([+-]*\d+),([+-]*\d+)').search(line).groups()
            pos += [[int(res[0]), int(res[1])]]
            vel += [[int(res[2]), int(res[3])]]
    pos = np.array(pos)
    vel = np.array(vel)

    ended = False
    time = 0
    max_adjacent = 20
    while not ended:
        while not suspicious(pos)>max_adjacent:
            pos = simulate(pos, vel)
            print(f'elapsed: {time}s.')
            time+=1
        display(pos)
        max_adjacent = suspicious(pos)
        ended = input(f'elapsed: \033[45m{time}\033[0ms. Total neighbours: \033[44m{max_adjacent}\033[0m. Press \033[41me\033[0m to end.')=='e'

main()