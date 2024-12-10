import numpy as np

def find_zero(grid, position):
    height = grid[position[0], position[1]]
    if height == 0:
        yield position
    safe_grid = np.pad(grid, 1, mode='constant', constant_values=10)
    if safe_grid[1+position[0], 1+position[1]+1] == height - 1:
        yield from find_zero(grid, [position[0], position[1]+1])
    if safe_grid[1+position[0], 1+position[1]-1] == height -1:
        yield from find_zero(grid, [position[0], position[1]-1])
    if safe_grid[1+position[0]+1, 1+position[1]] == height - 1:
        yield from find_zero(grid, [position[0]+1, position[1]])
    if safe_grid[1+position[0]-1, 1+position[1]] == height -1:
        yield from find_zero(grid, [position[0]-1, position[1]])

INPUT = './input/day10-1.txt'
grid = np.array([[int(element) for element in row[:-1] ]for row in open(INPUT).readlines()])
output = np.zeros(shape=np.shape(grid))
print(grid)
for position in [[x, y] for x in range(np.shape(grid)[0]) for y in range(np.shape(grid)[1])]:
    if grid[position[0], position[1]] == 9:
        tmp_output = np.zeros(shape=np.shape(grid))
        for result in find_zero(grid, position):
            tmp_output[result[0], result[1]] = 1 # so that multiple routes between the same 0 and 9 are not double counted
        output += tmp_output
print(output)
print(np.sum(output))