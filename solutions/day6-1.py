TEST = './test/day6-1.txt'
import numpy as np

mapping = lambda x: x=='.'-x=='^'

print(np.loadtxt(TEST, dtype=np.str_, comments=None, converters=mapping))