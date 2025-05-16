import numpy as np

def simulate(pos:np.ndarray, vels:np.ndarray, s:int) -> np.ndarray:
    width, height = 101, 103
    offset = pos + vels*s
    # print(offset)
    offset = np.column_stack((offset[:,0] % width, offset[:,1] % height))
    # print(offset)
    return offset

def safety_score(pos):
    # print(pos)
    width, height = 101, 103
    right = pos[:,0]>(width-1)/2
    left = pos[:,0]<(width-1)/2
    up = pos[:,1]>(height-1)/2
    down = pos[:,1]<(height-1)/2
    # print(up, left, down, right)
    return np.sum(right*up)*np.sum(right*down)*np.sum(left*up)*np.sum(left*down)

def main():
    import re
    with open('./input/day14-1.txt') as INPUT:
        pos, vel = [], []
        for line in INPUT.readlines():
            res = re.compile('p=(\d+),(\d+) v=([+-]*\d+),([+-]*\d+)').search(line).groups()
            pos += [[int(res[0]), int(res[1])]]
            vel += [[int(res[2]), int(res[3])]]
    grid = np.zeros(shape=(103,101))
    for idx in pos:
        grid[idx[1], idx[0]] += 1
    print(grid.astype(np.int64))
    end = simulate(np.array(pos), np.array(vel), 100)
    grid = np.zeros(shape=(103,101))
    for idx in end:
        grid[idx[1], idx[0]] += 1
    print(grid.astype(np.int64))
    return safety_score(end)



print(main())
