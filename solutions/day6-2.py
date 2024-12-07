TEST = './test/day6-1.txt'
import numpy as np

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

def get_obstacle_pos(init_board, pathlog):
    mode = 0
    state_summary = len(np.flatnonzero(init_board))
    nextstate = init_board
    state = nextstate
    while not ended(state):
        collided = False
        while not collided:
            state = nextstate
            pathlog += (state==-1).astype(np.int64)
            nextstate = next(state, mode)
            collided = not len(np.flatnonzero(nextstate)) == state_summary
            if ended(state):
                break
        nextstate = state
        mode = (mode+1)%4
    return pathlog
obstacle_pos = np.transpose(get_obstacle_pos(board, pathlog).nonzero())

# -----------

board = np.array([[e for e in s] for s in np.loadtxt(TEST, dtype=np.str_, comments=None)]) #board read in from file
board = np.pad((board=='#').astype(np.int64) - (board=='^').astype(np.int64), 1) #change data representation for convenience
pathlog = {0:np.zeros(shape=np.shape(board)), 1:np.zeros(shape=np.shape(board)), 2:np.zeros(shape=np.shape(board)), 3:np.zeros(shape=np.shape(board))}

def will_loop(state, mode, pathlog=pathlog):
    return bool(np.sum(pathlog[mode] * (state==-1)))
    
def run(init_board, pathlog):
    mode = 0
    state_summary = len(np.flatnonzero(init_board))
    nextstate = init_board
    state = nextstate
    while not ended(state):
        collided = False
        while not collided:
            state = nextstate
            if will_loop(state, mode):
                return True
            pathlog[mode] += (state==-1)
            nextstate = next(state, mode)
            collided = not len(np.flatnonzero(nextstate)) == state_summary
            if ended(state):
                return False
        nextstate = state
        mode = (mode+1)%4
    return False

count = 0
for index in obstacle_pos:
    board = np.array([[e for e in s] for s in np.loadtxt(TEST, dtype=np.str_, comments=None)]) #board read in from file
    board = np.pad((board=='#').astype(np.int64) - (board=='^').astype(np.int64), 1) #change data representation for convenience
    board[index[0], index[1]] = 1
    print(board)
    pathlog = {0:np.zeros(shape=np.shape(board)), 1:np.zeros(shape=np.shape(board)), 2:np.zeros(shape=np.shape(board)), 3:np.zeros(shape=np.shape(board))}
    count += run(board, pathlog)
print(count)

