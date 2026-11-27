"""Fourth look: print contexts of a pattern in a file.  usage: ctx.py FILE REGEX [before after]"""
import re, sys
f, pat = sys.argv[1], re.compile(sys.argv[2])
bef = int(sys.argv[3]) if len(sys.argv) > 3 else 200; aft = int(sys.argv[4]) if len(sys.argv) > 4 else 260
for i, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
    last = -10 ** 9
    for m in pat.finditer(line):
        if m.start() - last < bef + aft: continue
        last = m.start()
        print(f'{i}: ...{line[max(0, m.start() - bef):m.end() + aft]}...')
