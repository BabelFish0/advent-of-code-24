import re;print(sum([sum([int(m[0])*int(m[1]) for m in re.compile(r'mul\((\d{1,3}),(\d{1,3})\)').findall(s)]) for s in re.compile(r"do\(\)(.*?)don't\(\)", re.DOTALL).findall("do()"+open('./input/day3-1.txt').read()+"don't()")]))