import re;INPUT = open('./input/day5-1.txt').read();fix = lambda update: update if not sum([([match.start() for match in re.compile(pages[0]).finditer(update)] > [match.start() for match in re.compile(pages[1]).finditer(update)] and (len(re.compile(pages[0]).findall(update)) > 0) and (len(re.compile(pages[1]).findall(update)) > 0)) for pages in re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)]) else fix(update.replace(re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)[[([match.start() for match in re.compile(pages[0]).finditer(update)] > [match.start() for match in re.compile(pages[1]).finditer(update)] and (len(re.compile(pages[0]).findall(update)) > 0) and (len(re.compile(pages[1]).findall(update)) > 0)) for pages in re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)].index(1)][1], 'X').replace(re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)[[([match.start() for match in re.compile(pages[0]).finditer(update)] > [match.start() for match in re.compile(pages[1]).finditer(update)] and (len(re.compile(pages[0]).findall(update)) > 0) and (len(re.compile(pages[1]).findall(update)) > 0)) for pages in re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)].index(1)][0], re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)[[([match.start() for match in re.compile(pages[0]).finditer(update)] > [match.start() for match in re.compile(pages[1]).finditer(update)] and (len(re.compile(pages[0]).findall(update)) > 0) and (len(re.compile(pages[1]).findall(update)) > 0)) for pages in re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)].index(1)][1]).replace('X', re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)[[([match.start() for match in re.compile(pages[0]).finditer(update)] > [match.start() for match in re.compile(pages[1]).finditer(update)] and (len(re.compile(pages[0]).findall(update)) > 0) and (len(re.compile(pages[1]).findall(update)) > 0)) for pages in re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)].index(1)][0]));print(sum([bool(sum([([match.start() for match in re.compile(pages[0]).finditer(line)] > [match.start() for match in re.compile(pages[1]).finditer(line)] and (len(re.compile(pages[0]).findall(line)) > 0) and (len(re.compile(pages[1]).findall(line)) > 0)) for pages in re.compile(r'(\d{2})\|(\d{2})').findall(INPUT)]))*int(fix(line)[int(len(line)/2-1):int(len(line)/2+1)]) for line in re.compile(r'((?:\d{2},*){2,100})').findall(INPUT)]))

#the `fix` lambda recursively swaps pages that cause the first rule vilation for that line until it is fixed