import numpy as np
from utils.progress import Printer
import sys
sys.setrecursionlimit(20000)

# express problem as nodes: junctions and edges: scores between junctions?

def load(path):
    with open(path) as INPUT:
        str_input = INPUT.read()[:-1]
    state = np.array([list(row) for row in str_input.split('\n')], dtype=str)
    return state

# def display(state, p=Printer()):
#     p.mapping = {'#':p.colours.Kbg+p.colours.Kfg, '.':p.colours.Bbg+p.colours.Bfg, 'S':p.colours.Gbg+p.colours.Mfg, 'E':p.colours.Rbg}
#     p.string_arrprint(state, dsp_vals=False, width=2)

# def display_numeric(state, p=Printer()):
#     p.arrprint(state)

class Path:
    def __init__(self, position, score, direction, container, global_ref, walls):
        self.position = position
        self.score = score
        self.direction = direction
        # self.history = history
        self.cont_ref = container
        container.append(self)
        # if self.looped():
        #     self.cull()
        #     return
        if self.compare(global_ref):
            self.cull()
            return
        if self.ended():
            print(f'{self} reached end with score: {self.score:.0f}\033[42m\n\033[0m')
            # self.cull()
            # return
        self.next(walls, global_ref)

    def find_next(self, walls):
        ahead = self.position + self.direction
        right = self.position + np.matmul(self.direction,np.array([[0,-1],[1,0]]))
        left = 2*self.position - right
        return list(filter(lambda x: tuple(x[0]) not in walls, [[ahead, self.score+1], [right, self.score+1001], [left, self.score+1001]]))
    
    def next(self, walls, global_ref):
        for details in self.find_next(walls):
            print(f'{self} at {np.array2string(self.position):<9} moving to {np.array2string(details[0]):<9} with score {details[1]:>5.0f} | {len(self.cont_ref):>5.0f} active trailheads.')
            # p = Printer()
            # p.arrprint(np.where(np.isnan(global_ref), -100, global_ref), False)
            Path(details[0], details[1], details[0]-self.position, self.cont_ref, global_ref, walls)
            # self.history.union({tuple(self.position)})
        self.cull()

    def compare(self, global_ref):
        current = global_ref[tuple(self.position)]
        if current < self.score:
            return True
        global_ref[tuple(self.position)] = self.score
        return False

    # def looped(self):
    #     return tuple(self.position) in self.history # not needed, remove history

    def ended(self):
        global end
        return np.sum(self.position == end) == 2

    def cull(self):
        print(f'Killed {self} at {np.array2string(self.position):<9}')
        self.cont_ref.remove(self) # garbage collector frees memory when no other refs to obj exist

state = load('./input/day16-1.txt')
start = np.argwhere(state=='S')[0]
end = np.argwhere(state=='E')[0]
walls = {tuple(id) for id in np.argwhere(state=='#')}
score_log = ((state == '.').astype(np.int64) + (state == 'S').astype(np.int64) + (state == 'E').astype(np.int64)) * np.inf
paths = []

import time
t0 = time.perf_counter()
Path(start, 0, np.array([0,1]), paths, score_log, walls)
t1 = time.perf_counter()

p = Printer()
p.mapping = {'#':p.colours.Kbg+p.colours.Kfg, '.':p.colours.Bbg+p.colours.Bfg, 'S':p.colours.Gbg+p.colours.Mfg, 'E':p.colours.Rbg}
p.string_arrprint(state, width=1, dsp_vals=False)
p.arrprint(np.where(np.isnan(score_log), -100, score_log), False, width=1)
print(f'Best score: \033[45m{score_log[tuple(end)]:.0f}\033[0m in {t1-t0:.2f}s.')