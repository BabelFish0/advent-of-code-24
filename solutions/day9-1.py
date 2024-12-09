def convert(lin):
    free_space = -1
    lout = [[int(i/2)]*int(lin[i]*(1-i%2)) + [free_space]*int(lin[i]*(i%2)) for i in range(len(lin))]
    return [x for xs in lout for x in xs]

def rightmost_used(storage):
    free_space = -1
    idx = len(storage)-1
    while storage[idx] == free_space:
        idx -= 1
    return idx

def swap_earliest(storage):
    free_space = -1
    free_loc = storage.index(free_space)
    used_loc = rightmost_used(storage)
    storage[free_loc], storage[used_loc] = storage[used_loc], storage[free_loc]
    return storage

def not_compacted(storage):
    free_space = -1
    return free_space in storage[:rightmost_used(storage)+1]

def compact(storage):
    free_space = -1
    while not_compacted(storage):
        storage = swap_earliest(storage)
    return storage

def checksum(storage):
    return sum([i * e for i, e in enumerate(storage[:rightmost_used(storage)+1])])

def main():
    INPUT = './input/day9-1.txt'
    S = convert([int(a) for a in open(INPUT).read()[:-1]])
    S_comp = compact(S)
    print(checksum(S_comp))

main()
# print(convert([1,2,3,4]))
# print(compact(convert([1, 2, 3, 4, 5])))
# print(checksum(compact(convert([1,2,3,4, 5]))))