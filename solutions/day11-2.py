from functools import cache
import time
import copy

def split(number):
    s = str(number)
    return int(s[:int(len(s)/2)]), int(s[int(len(s)/2):])

@cache
def blink(number):
    if number == 0:
        return 1,
    if len(str(number)) % 2 == 0:
        return split(number)
    else:
        return number * 2024,

def iterate(arrangement):
    keys = copy.deepcopy(list(arrangement.keys()))
    tmp = copy.deepcopy(arrangement)
    for key in keys:
        if tmp[key] > 0:
            arrangement[key] -= tmp[key] 
            for result in blink(key):
                if result in arrangement:
                    arrangement[result] += tmp[key]
                else:
                    arrangement[result] = tmp[key]
        else:
            del arrangement[key]
    return arrangement

def main():
    with open('./input/day11-1.txt') as INPUT:
        arrangement_raw = INPUT.read()[:-1].split(' ')
        arrangement_raw = [int(e) for e in arrangement_raw]
        arrangement = {key:1 for key in arrangement_raw}

    t0 = time.perf_counter()
    for i in range(75):
        arrangement = iterate(arrangement)
        print(f'{i + 1} blinks')
        # print(arrangement)
    count = sum(arrangement.values())
    t1 = time.perf_counter()-t0

    info = {'largest pebble: ':max(arrangement.keys()), 'highest duplicate pebble count: ':max(arrangement.values()), 'arrangement dict size: ':len(arrangement)}
    print(f'\ntotal: \033[45m{count}\033[0m in {t1:.2}s.')
    for summary in [t[0] + str(t[1]) for t in zip(info.keys(), info.values())]:
        print(summary)

main()