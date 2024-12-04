import numpy as np

with open('./input/day2-1.txt') as INPUT:
    print(sum([(np.min(np.fromstring(line, sep=' ')[1:]-np.fromstring(line, sep=' ')[:-1]) >= 1 and np.max(np.fromstring(line, sep=' ')[1:]-np.fromstring(line, sep=' ')[:-1]) <= 3) or (np.min(np.fromstring(line, sep=' ')[1:]-np.fromstring(line, sep=' ')[:-1]) >= -3 and np.max(np.fromstring(line, sep=' ')[1:]-np.fromstring(line, sep=' ')[:-1]) <= -1) for line in INPUT.readlines()]))