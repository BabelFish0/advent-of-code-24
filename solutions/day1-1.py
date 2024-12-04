import numpy as np
print(np.sum(np.absolute(np.sort(np.loadtxt('./input/day1-1.txt', dtype=np.int64)[:, 0])-np.sort(np.loadtxt('./input/day1-1.txt', dtype=np.int64)[:, 1]))))