import re

def check(target:int, components:list)->bool:
    if len(components) == 1:
        return components[0] == target
    rightmost = components[-1]
    if target//rightmost != target/rightmost:
        return check(target - rightmost, components[:-1])
    return check(target//rightmost, components[:-1]) or check(target - rightmost, components[:-1])

with open('./input/day7-1.txt') as INPUT:
    print('')
    c = 0
    for case in re.compile(r"(\d+):((?:[ ](?:\d+))+)").findall(INPUT.read()):
        target, components = int(case[0]), list(map(int, case[1][1:].split(' ')))
        a = check(target, components)
        c += a*target
        print(f'{a:<2}| {target:<15} from {components}')

print(c)

