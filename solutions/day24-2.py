import sys
sys.setrecursionlimit(30000)
import random
random.seed(0)

# work backwards and forwards?

def load(path):
    wires, rules = {}, {}
    import re
    with open(path) as INPUT:
        str_input = INPUT.read()
    for logic_pair in re.compile(r"(.{3}) ([ANDXOR]{2,3}) (.{3}) -> (.{3})").findall(str_input):
        wires.update({logic_pair[a]:None for a in [0, 2, 3]})
        rules[logic_pair[3]] = (logic_pair[0], logic_pair[2], {'AND':and_, 'OR':or_, 'XOR':xor_}[logic_pair[1]])#(wires[logic_pair[0]], wires[logic_pair[2]], {'AND':and_, 'OR':or_, 'XOR':xor_}[logic_pair[1]])
    for initial_condition in re.compile(r"(.{3}): ([01])").findall(str_input):
        wires[initial_condition[0]] = int(initial_condition[1])
    return wires, rules

and_ = lambda x, y: x and y
or_ = lambda x, y: x or y
xor_ = lambda x, y: x ^ y

table_and = {
    1: [(1,1)],
    0: [(0,0), (0,1), (1,0)]
}
table_or = {
    1: [(1,1), (0,1), (1,0)],
    0: [(0,0)]
}
table_xor = {
    1: [(1,0), (0,1)],
    0: [(1,1), (0,0)]
}

tables = {and_:table_and, or_:table_or, xor_:table_xor}

wires, rules = load('./input/day24-1.txt')

def backtrack(desired_wires, rules, intermediates={}, tables=tables, depth=0):
    '''create input state to arrive at particular state'''
    if depth == 20000:
        return True
    done = {wire:state for wire, state in desired_wires.items() if wire[0] in 'xy'}
    if len(done) == len(desired_wires.keys()):
        return intermediates | desired_wires
    for wire in desired_wires.keys() - done.keys():
        state = desired_wires[wire]
        gate_details = rules[wire]
        gate_func = gate_details[2]
        input_wires = gate_details[:2]
        input_states = tables[gate_func][state]
        for config in input_states:
            required = {input_wires[0]:config[0], input_wires[1]:config[1]}
            mismatched = set(input_wires) & set(intermediates.keys()) - {k for k in input_wires if required[k] == intermediates.get(k)}
            if mismatched:
                print('Rare case: overlap occured in prerequisite gates, trying others.')
                return False
            result = backtrack(required, rules, intermediates | required, tables, depth+1)
            if result:
                return result

def simulate(wires, rules):
    import time
    t0 = time.perf_counter()
    i = 0
    while None in wires.values():
        if i > 10000:
            print('failed')
            return False # circular or fails to reach all
        for output_wire, logic_pair in zip(rules.keys(), rules.values()):
            if wires[logic_pair[0]] != None and wires[logic_pair[1]] != None and wires[output_wire] == None:
                wires[output_wire] = logic_pair[2](wires[logic_pair[0]], wires[logic_pair[1]])
        i += 1
    print(f'Simulated in {time.perf_counter()-t0:.4f}s.')
    return wires

def filter_by_key(dict, condition):
    return {key:value for key, value in dict.items() if condition(key)}

def setall(dict, keys, value):
    dict.update({key:value for key in keys})

def set_random(dict):
    return{key:random.randint(0, 1) for key in dict.keys()}

def from_bin(leading_letter, wires):
    output_states = filter_by_key(wires, lambda x: x[0] == leading_letter)
    binary = [output_states[key] for key in sorted(output_states.keys(), key=lambda x: int(x[1:]), reverse=True)]
    return int("".join(map(str, binary)), base=2)

def test(gate1, gate2, rules, wires):
    '''
    only guarantee correct identification of faulty gates
    '''
    if gate1[2] == gate2[2]:
        return True
    # a xor b -> z is wrong for (1,1)
    # x or y -> c

    # a xor b -> z is right for (0,0)
    # x and y -> c

    # a or b -> z is right for (0,0),(1,1)
    # x and y -> c
    test_case = {
        (or_, xor_):(1, 1, True),
        (and_, xor_):(1, 1, True),
        (and_, or_):(0, 1, True)
    }
    test_case |= {key[::-1]:test_case[key] for key in test_case.keys() }
    test = test_case[(gate1[2], gate2[2])]

    setall(wires, wires.keys(), None)
    wires = wires | set_random(filter_by_key(wires, lambda x: x[0] in 'xy'))
    required_in = backtrack({gate1[0]:test[0], gate1[1]:test[1], gate2[0]:test[1], gate2[1]:test[1]}, rules)
    if required_in == True: # not possible
        return False
    initial_states = wires | required_in

    x = from_bin('x', initial_states)
    y = from_bin('y', initial_states)
    res = simulate(initial_states, rules)
    if res:
        return (x+y == from_bin('z', res)) == test[2]
    return False # not possible

from itertools import combinations
problem_gates = set()
for gate1, gate2 in combinations(rules.keys(), 2):
    # setall(wires, wires.keys(), 0)
    if test(rules[gate1], rules[gate2], rules, wires) == False:
        print('problem detected')
        swap = rules | {gate1: rules[gate2], gate2: rules[gate1]}
        if test(rules[gate1], rules[gate2], swap, wires) == True:
            problem_gates |= {gate1, gate2}
            print(len(problem_gates))

print(len(problem_gates))
print(len(rules))

# print(problem_gates)
print(",".join(sorted(problem_gates)))