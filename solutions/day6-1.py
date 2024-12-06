TEST = './input/day6-1.txt'
import numpy as np
import time

board = np.array([[e for e in s] for s in np.loadtxt(TEST, dtype=np.str_, comments=None)]) #board read in from file
board = np.pad((board=='#').astype(np.int64) - (board=='^').astype(np.int64), 1) #change data representation for convenience
pathlog = np.zeros(shape=np.shape(board))

def ended(state):
    fence = np.pad(np.zeros(shape=(np.shape(state)[0]-2, np.shape(state)[1]-2), dtype=np.int64), 1, constant_values=1) #outer perimeter of 1s
    return bool(np.sum(state*fence))

def next(state, mode):
    mode_shift = {0:-1, 1:1, 2:1, 3:-1}
    guard = (state==-1).astype(np.int64)
    return state - (np.roll(guard, shift=mode_shift[mode], axis=mode%2)-guard)
    
def main(init_board, pathlog):
    mode = 0
    state_summary = len(np.flatnonzero(init_board))
    nextstate = init_board
    state = nextstate
    while not ended(state):
        collided = False
        while not collided:
            state = nextstate
            pathlog += (state==-1).astype(np.int64)
            # print(pathlog.astype(bool).astype(np.int64)*2 + state)
            nextstate = next(state, mode)
            collided = not len(np.flatnonzero(nextstate)) == state_summary
            if ended(state):
                break
            # time.sleep(0.2)
        nextstate = state
        mode = (mode+1)%4
    
    print(f'Total cell visits: {np.sum(pathlog.astype(bool).astype(np.int64))-1}')

main(board, pathlog)
