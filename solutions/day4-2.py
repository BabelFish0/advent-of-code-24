import re; print(len(re.compile('(?=M[^\n]M.{139}A.{139}S[^\n]S)', re.DOTALL).findall(open('./input/day4-1.txt').read()))+len(re.compile('(?=M[^\n]S.{139}A.{139}M[^\n]S)', re.DOTALL).findall(open('./input/day4-1.txt').read()))+len(re.compile('(?=S[^\n]S.{139}A.{139}M[^\n]M)', re.DOTALL).findall(open('./input/day4-1.txt').read()))+len(re.compile('(?=S[^\n]M.{139}A.{139}S[^\n]M)', re.DOTALL).findall(open('./input/day4-1.txt').read())))