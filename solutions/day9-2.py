import sys
from utils.progress import Colour, Printer
sys.setrecursionlimit(20000)

def convert(lin):
    free_space = -1
    lout = [[int(i/2)]*int(lin[i]*(1-i%2)) + [free_space]*int(lin[i]*(i%2)) for i in range(len(lin))]
    return lout

def checksum(storage):
    flattened = [x for xs in storage for x in xs]
    # print(flattened)
    return sum([i*e*(e!=-1) for i, e in enumerate(flattened)])

def get_latest_file(storage):
    for idx, file in enumerate(storage[::-1]):
        if file[0] != -1:
            return len(storage)-1-idx, file

def pop_empty(storage):
    remove_ids = []
    for idx, element in enumerate(storage):
        if len(element) == 0:
            remove_ids += [idx]
    for idx in remove_ids[::-1]:
        storage.pop(idx)
    return storage

def get_free_spaces(storage):
    for idx, file in enumerate(storage):
        if file[0] == -1:
            yield idx, file

def swap_latest_file(storage):
    # print(storage)
    idx, latest_file = get_latest_file(storage)
    for idf, free_space in get_free_spaces(storage):
        # print(free_space, idf)
        # print(latest_file, idx)
        if len(free_space) > len(latest_file) and idf<idx:
            # print('mode 1')
            storage = storage[:idf] + [latest_file] + [[-1]*(len(free_space)-len(latest_file))] + storage[idf+1:idx] + [[-1]*len(latest_file)] + storage[idx+1:]
            return storage, latest_file[0]
        if len(free_space) == len(latest_file) and idf<idx:
            # print('mode 2')
            storage = storage[:idf] + [latest_file] + storage[idf+1:idx] + [[-1]*len(latest_file)] + storage[idx+1:]
            return storage, latest_file[0]
    return storage, latest_file[0]
    
def swap_possible(S, avoid=[]):
    if len(S) == 0:
        return []
    S_comp, id = swap_latest_file(S)
    S_comp = pop_empty(S_comp)
    avoid.append(id)
    # print(len(avoid))
    while S!=S_comp:
        S = S_comp
        if S[-1] in avoid:
            break
        S_comp = remerge(pop_empty(swap_latest_file(S)[0]))
        # print('popped', S_comp)
    return swap_possible(S_comp[:-1], avoid) + [S_comp[-1]]

def remerge(S):
    for idx in range(len(S))[::-1]:
        # print(idx)
        if S[idx][0] == S[idx-1][0]:
            S[idx-1] += S[idx]
            S = S[:idx] + S[idx+1:]
    return S

def main():
    INPUT = './input/day9-1.txt'
    class vis(Printer):
        def __init__(self):
            super().__init__()
        def mprint(self, storage):
            flattened = [int((x%6)*(x!=-1)-(x==-1)) for xs in storage for x in xs]
            self.iprint(self, flattened)
    v = vis
    v.mapping = {-1:Colour.Kbg, 0:Colour.Rbg, 1:Colour.Mbg, 2:Colour.Bbg, 3:Colour.Cbg, 4:Colour.Gbg, 5:Colour.Ybg}
    S = pop_empty(convert([int(a) for a in open(INPUT).read()[:-1]]))
    S = swap_possible(S)
    v.clear(v)
    v.mprint(v, S)
    print('\n' + str(checksum(S)))

main()