import numpy as np
from utils.progress import Printer
import sys
sys.setrecursionlimit(200000)

# express problem as nodes: junctions and edges: scores between junctions?

def load(path):
    with open(path) as INPUT:
        str_input = INPUT.read()[:-1]
    state = np.array([list(row) for row in str_input.split('\n')], dtype=str)
    return state

class Path:
    def __init__(self, position, score, direction, global_ref, walls):
        # global global_best
        self.position = position
        self.score = score
        self.direction = direction
        if self.compare(global_ref):
            return
        self.next(walls, global_ref)

    def find_next(self, walls):
        ahead = self.position + self.direction
        right = self.position + np.matmul(self.direction,np.array([[0,-1],[1,0]]))
        left = 2*self.position - right
        return list(filter(lambda x: tuple(x[0]) not in walls, [[ahead, self.score+1], [right, self.score+1001], [left, self.score+1001]]))
    
    def next(self, walls, global_ref):
        for details in self.find_next(walls):
            # print(f'{self} at {np.array2string(self.position):<9} moving to {np.array2string(details[0]):<9} with score {details[1]:>5.0f} |')#{len(self.cont_ref):>5.0f} active trailheads.')
            Path(details[0], details[1], details[0]-self.position, global_ref, walls)

    def compare(self, global_ref):
        direction_id = {(1,0):0, (0,1):1, (-1,0):2, (0,-1):3}[tuple(self.direction)]
        current = global_ref[direction_id][tuple(self.position)]
        if current <= self.score:
            return True
        global_ref[direction_id][tuple(self.position)] = self.score
        return False

    def ended(self):
        global end
        return np.sum(self.position == end) == 2

state = load('./input/day16-1.txt')
start = np.argwhere(state=='S')[0]
end = np.argwhere(state=='E')[0]
walls = {tuple(id) for id in np.argwhere(state=='#')}
score_log = np.stack([np.where(state=='#', -1e3, 150000)for _ in range(4)]) #((state == '.').astype(np.int64) + (state == 'S').astype(np.int64) + (state == 'E').astype(np.int64)) * 1e6

import time
t0 = time.perf_counter()
Path(start, 0, np.array([0,1]), score_log, walls)
t1 = time.perf_counter()

p = Printer()
p.mapping = {'#':p.colours.Kbg+p.colours.Kfg, '.':p.colours.Bbg+p.colours.Bfg, 'S':p.colours.Gbg+p.colours.Mfg, 'E':p.colours.Rbg}
p.string_arrprint(state, width=1, dsp_vals=False)
p.arrprint(score_log.min(0), False, width=1)
print(f'Best score: \033[45m{score_log.min(0)[tuple(end)]:.0f}\033[0m in {t1-t0:.2f}s.')