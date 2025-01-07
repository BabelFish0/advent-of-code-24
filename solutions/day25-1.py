import numpy as np
import re

def load(path):
    # find_locks = re.compile(r"#+\n(?:.+\n)+")
    # find_keys = re.compile(r"\n([.]+\n(?:.+\n)+)")
    with open(path) as INPUT:
        str_input = INPUT.read()

    keys, locks = [], []

    for item in str_input.split('\n\n'):
        if item[0] == '.':
            keys.append(convert(item))
        else:
            locks.append(convert(item))
    
    return keys, locks

def convert(str_):
    counter = re.compile('#+')
    diff = lambda tup: tup[1]-tup[0]-1
    return np.array([diff(counter.search(str_[s::6]).span()) for s in range(5)])

def test(key, lock):
    test = key + lock
    # print(test)
    return np.all(test <= 5)

keys, locks = load('./input/day25-1.txt')
passed = 0
for key in keys:
    for lock in locks:
        passed += test(key, lock)
print(passed)