import numpy as np
from utils.progress import Printer

def display(state, p=Printer()):
    p.mapping = {'#':p.colours.Kbg+p.colours.Kfg, '.':p.colours.Bbg+p.colours.Bfg, '@':p.colours.Gbg+p.colours.Mfg, 'O':p.colours.Rbg, '[':p.colours.Rbg+p.colours.Yfg, ']':p.colours.Rbg+p.colours.Yfg}
    # converted = np.vectorize(mapping.get)(state)
    p.string_arrprint(state, dsp_vals=True)

def load(path):
    import re
    find_board = re.compile(r"(?:((?:.*\n)+.*)\n\n)")
    find_instructions = re.compile(r"\n\n((?:.*\n)*)")
    with open(path) as INPUT:
        str_input = INPUT.read()
    state = np.array([list(row) for row in find_board.search(str_input).group(1).split('\n')], dtype=str)
    instructions = find_instructions.search(str_input).group(1).replace('\n','')
    return state, instructions

def convert(state):
    from itertools import chain
    replace = {'#':['#', '#'], '.':['.','.'], '@':['@','.'], 'O':['[',']']}
    transformed = np.array([list(chain(*[replace[i] for i in row])) for row in state])
    return transformed

def recursive_push_ud(state, position, delta):
    next = position + delta
    s_next = state[tuple(next)]
    if s_next == '#':
        return [np.array([-1,-1])]
    if s_next == '.':
        return [position]
    if s_next == ']':
        return [position] + recursive_push_ud(state, next, delta) + recursive_push_ud(state, next+np.array([0,-1]), delta)
    return [position] + recursive_push_ud(state, next, delta) + recursive_push_ud(state, next+np.array([0,1]), delta)

def recursive_push_lr(state, position, delta):
    next = position + delta
    s_next = state[tuple(next)]
    if s_next == '#':
        return [np.array([-1,-1])]
    if s_next == '.':
        return [position]
    return [position] + recursive_push_lr(state, next, delta)

# class Box:
#     def __init__(self, pos):
#         self.pos = pos
#     def move(self, walls, box_ids, box_objs, delta):
#         next = self.pos + delta
#         if next in walls:
#             return False
#         if next in box_ids:
#             if move(walls, box_ids, box_objs[box_ids.index(next)], delta):
#                 self.pos += delta
#                 return True
#         self.pos += delta
#         return True

def move(active_state, mv):
    import copy
    delta = {
        '^':(np.array([-1,0]), recursive_push_ud),
        'v':(np.array([1,0]), recursive_push_ud),
        '>':(np.array([0,1]), recursive_push_lr),
        '<':(np.array([0,-1]), recursive_push_lr)}
    position = np.argwhere(active_state=='@')[0]
    pushable = delta[mv][1](active_state, position, delta[mv][0])
    pushable = np.array(list(set([tuple(idx) for idx in pushable]))) # remove duplicates by turning into hashable dtype
    if not np.array([-1,-1]) in pushable:
        ordered_chars = []
        for idx in pushable:
            ordered_chars += [copy.deepcopy(active_state[tuple(idx)])]
            active_state[tuple(idx)] = '.'
        for i, idx in enumerate(np.array(pushable) + delta[mv][0]):
            active_state[tuple(idx)] = ordered_chars[i]

def get_gps(state):
    coords = np.argwhere(state=='[')
    return np.sum(100*coords[:,0]+coords[:,1])

def main():
    import time
    state, instructions = load('./input/day15-1.txt')
    display(state)
    state=convert(state)
    print('converting...')
    display(state)
    print(instructions)
    # while True:
    #     mv = input()
    #     move(state, mv)
    #     display(state)
    c = 0
    for mv in instructions:
        c+=1
        time.sleep(0.2)
        print(f'Move: \033[045m{mv}\033[0m {100*c/len(instructions):>7.0f}%')
        move(state, mv)
        display(state)
    print(f'GPS sum: \033[045m{get_gps(state)}\033[0m')

main()