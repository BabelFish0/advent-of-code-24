def split(number):
    s = str(number)
    return [int(s[:int(len(s)/2)]), int(s[int(len(s)/2):])]

def blink(arrangement):
    out = []
    for number in arrangement:
        if number == 0:
            out.append(1)
        elif len(str(number)) % 2 == 0:
            out += split(number)
        else:
            out.append(number * 2024)
    return out

def main():
    with open('./input/day11-1.txt') as INPUT:
        arrangement = INPUT.read()[:-1].split(' ')
        arrangement = [int(e) for e in arrangement]
    print(arrangement)
    for i in range(25):
        arrangement = blink(arrangement)
        print(f'{i + 1} blinks')
        # print(arrangement)
    print(len(arrangement))

main()