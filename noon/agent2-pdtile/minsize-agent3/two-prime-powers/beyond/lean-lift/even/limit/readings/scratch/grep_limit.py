import re, sys
p = sys.argv[1]; word = sys.argv[2]
for n, line in enumerate(open(p, encoding='utf-8'), 1):
    for m in re.finditer(word, line, flags=re.I):
        a = max(0, m.start() - 90); b = min(len(line), m.end() + 110)
        print(n, ':', line[a:b].replace('\n', ' '))
