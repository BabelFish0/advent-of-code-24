import re
import time

def deconcatenate(target, remove):
    '''
    ## Returns
    `False` if deconcatenation not possible, otherwise left-hand elements of `target` left when clipping `remove` from the right.
    ## Examples
    ```python
    deconcatenate(1234, 34) # -> 12
    deconcatenate(130, 30)  # -> 1
    deconcatenate(1234, 43) # -> False
    deconcatenate(12, 1234) # -> False
    ```
    '''
    if len(str(remove))>=len(str(target)):
        return False
    clipped = int(str(target)[-1*len(str(remove)):])
    left = int(str(target)[:-1*len(str(remove))])
    if clipped != remove:
        return False
    return left

def check(target:int, components:list, i)->bool:
    '''Recursively work right to left and eliminate things that are impossible where applicable.'''
    if target < 0 or components[-1] < 0: # catch negatives (rare)
        print(f'\033[93m\033[41m{i:<3}\033[0m', end='') # end nodes print their recursion depth because it looks cool
        return False
    if len(components) == 1: # base case
        if components[0] == target:
            print(f'\033[92m\033[44m{i:<3}\033[0m', end='')
            return True
        print(f'\033[93m\033[41m{i:<3}\033[0m', end='')
        return False
    rightmost = components[-1]
    if target//rightmost != target/rightmost: # check if multiplication could've been the last op, then test deconcatenation
        if deconcatenate(target, components[-1]):
            return check(target - rightmost, components[:-1], i+1) or check(deconcatenate(target, components[-1]), components[:-1], i+1)
        return check(target - rightmost, components[:-1], i+1)
    if deconcatenate(target, components[-1]):
        return check(target//rightmost, components[:-1], i+1) or check(target - rightmost, components[:-1], i+1) or check(deconcatenate(target, components[-1]), components[:-1], i+1)
    return check(target//rightmost, components[:-1], i+1) or check(target - rightmost, components[:-1], i+1)

with open('./input/day7-1.txt') as INPUT:
    t0 = time.perf_counter()
    c = 0
    for case in re.compile(r"(\d+):((?:[ ](?:\d+))+)").findall(INPUT.read()): # format input using regex
        print('───────────────┼───────────────────────') # pretty table
        print('               │ ', end='')
        target, components = int(case[0]), list(map(int, case[1][1:].split(' '))) # split by whitespace and remove first blank string
        a = check(target, components, 1)
        c += a*target
        print('')
        if a:
            print('\033[42m', end='') # colour based on result
        else:
            print('\033[31m\033[09m', end='')
        print(f'{target:<15}\033[0m│ from {components}')

        

print(f'\ntotal: \033[45m{c}\033[0m in {time.perf_counter()-t0}s.')