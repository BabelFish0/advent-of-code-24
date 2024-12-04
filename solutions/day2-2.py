import numpy as np
import time


def check_safe(report:np.ndarray)->bool:
    diffs = report[1:] - report[:-1]
    return (np.min(diffs) >= 1 and np.max(diffs) <= 3) or (np.min(diffs) >= -3 and np.max(diffs) <= -1)

def check_tolerant_safe(report):
    if check_safe(report):
        return True
    else:
        return bool(sum(check_safe(np.concatenate([report[:i], report[i+1:]])) for i in range(len(report))))

t0 = time.perf_counter()
with open('./input/day2-1.txt') as INPUT:
    print(sum([check_tolerant_safe(np.fromstring(line, sep=' ')) for line in INPUT.readlines()]))

print(f'Completed in {time.perf_counter()-t0}s.')