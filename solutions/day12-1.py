import numpy as np
from functools import cache

@cache
def recursive_flood_fill(target, index, tmp_arr):
    tmp_arr[index[0], index[1]] = 1
    neighbours = lambda x, y: [[x+(i%2)*(-1)**i, y+i] for i in range(4)]