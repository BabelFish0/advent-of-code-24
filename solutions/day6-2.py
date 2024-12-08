TEST = './input/day6-1.txt'
import numpy as np
import time
import copy

board = np.array([[e for e in s] for s in np.loadtxt(TEST, dtype=np.str_, comments=None)]) #board read in from file
board = np.pad((board=='#').astype(np.int64) - (board=='^').astype(np.int64), 1) #change data representation for convenience
pathlog = {0:np.zeros(shape=np.shape(board)), 1:np.zeros(shape=np.shape(board)), 2:np.zeros(shape=np.shape(board)), 3:np.zeros(shape=np.shape(board))}

def printer(state):
    BLUE = '\033[44m'
    CYAN = '\033[46m'
    BLANK = '\033[100m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    RESET = '\033[0m'
    for row in state:
        for entry in row:
            if entry == -2:
                print(CYAN + ' ', end='')
            if entry == 0:
                print(BLANK + ' ', end='')
            if entry == -3:
                print(GREEN + ' ', end='')
            if entry == 1:
                print(RED + ' ', end='')
            if entry > 1:
                print(BLUE + ' ', end='')
        print(RESET)

def ended(state):
    fence = np.pad(np.zeros(shape=(np.shape(state)[0]-2, np.shape(state)[1]-2), dtype=np.int64), 1, constant_values=1) #outer perimeter of 1s
    return bool(np.sum(state*fence))

def next(state, mode):
    mode_shift = {0:-1, 1:1, 2:1, 3:-1}
    guard = (state==-1).astype(np.int64)
    return state - (np.roll(guard, shift=mode_shift[mode], axis=mode%2)-guard)

def get_obstacle_pos(init_board, pathlog):
    mode = 0
    state_summary = len(np.flatnonzero(init_board))
    nextstate = init_board
    state = nextstate
    while not ended(state):
        collided = False
        while not collided:
            state = nextstate
            nextstate = next(state, mode)
            collided = not len(np.flatnonzero(nextstate)) == state_summary
            if ended(state):
                break
            if not collided:
                yield state, nextstate, copy.deepcopy(pathlog), mode
            pathlog[mode] += (state==-1)
        nextstate = state
        mode = (mode+1)%4

def will_loop(state, mode, pathlog):
    return bool(np.sum(pathlog[mode] * (state==-1)))
    
def run(init_board, pathlog, mode=0):
    state_summary = len(np.flatnonzero(init_board))
    nextstate = init_board
    state = nextstate
    while not ended(state):
        collided = False
        while not collided:
            # printer(state)
            state = nextstate
            if will_loop(state, mode, pathlog):
                return True, pathlog
            pathlog[mode] += (state==-1)
            nextstate = next(state, mode)
            collided = not len(np.flatnonzero(nextstate)) == state_summary
            if ended(state):
                return False, pathlog
        nextstate = state
        mode = (mode+1)%4
    return False, pathlog

c = 0
t0 = time.perf_counter()
persistent_log = {0:np.zeros(shape=np.shape(board)), 1:np.zeros(shape=np.shape(board)), 2:np.zeros(shape=np.shape(board)), 3:np.zeros(shape=np.shape(board))}
for state, nextstate, log, mode in get_obstacle_pos(board, pathlog):
    obstacle = (nextstate==-1)
    persistent_log = {key: (persistent_log[key] + log[key])>0 for key in range(4)}
    loops, route = run(state+obstacle, copy.deepcopy(persistent_log), mode)
    # persistent_log[mode] = np.where((persistent_log[mode]*(state==-1))>0, 0, persistent_log[mode])
    if loops:
        c += 1
        print('\033[2J'+str(c))
        persistent_log = {key: (persistent_log[key] + route[key])>0 for key in range(4)}
#         print('\033[100m'+'─'*len(state[0])+'\033[0m')
#         printer(state + obstacle*2 + (sum(route.values())>0)*-2)
# print('\033[100m'+'─'*len(state[0])+'\033[0m')
print(f'\ntotal: \033[45m{c}\033[0m in {time.perf_counter()-t0}s.')