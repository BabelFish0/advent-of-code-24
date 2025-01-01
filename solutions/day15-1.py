import numpy as np
from utils.progress import Printer

def display(state, p=Printer()):
    p.mapping = {'#':p.colours.Kbg, '.':p.colours.Bbg, '@':p.colours.Gbg, 'O':p.colours.Rbg}
    # converted = np.vectorize(mapping.get)(state)
    p.string_arrprint(state)

def load(path):
    import re
    find_board = re.compile(r"(?:((?:.*\n)+.*)\n\n)")
    find_instructions = re.compile(r"\n\n((?:.*\n)*)")
    with open(path) as INPUT:
        str_input = INPUT.read()
    state = np.array([list(row) for row in find_board.search(str_input).group(1).split('\n')], dtype=str)
    instructions = find_instructions.search(str_input).group(1).replace('\n','')
    return state, instructions

def find_pushable(state, move):
    import copy
    pos = np.argwhere(state=='@')[0]
    delta = {'^':np.array([-1,0]),'v':np.array([1,0]),'>':np.array([0,1]),'<':np.array([0,-1])}
    current = pos + delta[move]
    pushable = [pos]
    while state[tuple(current)] == 'O':
        pushable += [copy.deepcopy(current)]
        current += delta[move]
    if state[tuple(current)] == '#':
        return None
    pushable += [copy.deepcopy(current)]
    return pushable

def move(active_state, move):
    pushable = find_pushable(active_state, move)
    if pushable: # @OOO. -> .@OOO ; @. -> .@
        active_state[tuple(pushable[0])] = '.'
        active_state[tuple(pushable[-1])] = 'O'
        active_state[tuple(pushable[1])] = '@' # if no obstruction the 'O' above just gets overwritten

def get_gps(state):
    coords = np.argwhere(state=='O')
    return np.sum(100*coords[:,0]+coords[:,1])

def main():
    import time
    state, instructions = load('./input/day15-1.txt')
    display(state)
    c = 0
    for mv in instructions:
        c+=1
        time.sleep(0.05)
        print(f'Move: \033[045m{mv}\033[0m {100*c/len(instructions):>7.0f}%')
        move(state, mv)
        display(state)
    print(f'GPS sum: \033[045m{get_gps(state)}\033[0m')

main()