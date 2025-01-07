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
wires, rules = load('./input/day24-1.txt')

def simulate(wires, rules):
    while None in wires.values():
        for output_wire, logic_pair in zip(rules.keys(), rules.values()):
            if wires[logic_pair[0]] != None and wires[logic_pair[1]] != None and wires[output_wire] == None:
                wires[output_wire] = logic_pair[2](wires[logic_pair[0]], wires[logic_pair[1]])
    return wires

def filter_by_key(dict, condition):
    return {key:value for key, value in dict.items() if condition(key)}

output_states = filter_by_key(simulate(wires, rules), lambda x: x[0] == 'z')
binary = [output_states[key] for key in sorted(output_states.keys(), key=lambda x: int(x[1:]), reverse=True)]
print(int("".join(map(str, binary)), base=2))