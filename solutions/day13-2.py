def test_integer_combination(v1, v2, vt):
    '''av_1+bv_2=v_t'''
    x1, y1 = v1
    x2, y2 = v2
    xt, yt = vt
    b = (x1*yt-y1*xt)/(x1*y2-y1*x2)
    a = (xt-b*x2)/x1
    if (a, b) == (int(a), int(b)):
        return int(a), int(b)
    return False

def parse(path): # efficient because generator objects save memory
    import re
    get_signedxy = re.compile(r"([+-]*\d+)(?:[^\d]+?)([+-]*\d+)")
    with open(path) as file:
        l_idx = 0
        out = [[]]*3
        for line in file.readlines():
            matches = get_signedxy.search(line)
            if matches:
                out[l_idx%3] = [int(matches.groups()[0]), int(matches.groups()[1])]
                if l_idx%3 == 2:
                    yield out
                l_idx+=1

def main():
    import time
    total = 0
    t0 = time.perf_counter()
    for xylist in parse('./input/day13-1.txt'):
        coeffs = test_integer_combination(xylist[0], xylist[1], [xylist[2][0]+10000000000000, xylist[2][1]+10000000000000])
        if coeffs:
            total += 3*coeffs[0] + coeffs[1]
    print(f'\ntotal: \033[45m{total}\033[0m in {time.perf_counter()-t0:.2}s.')

main()