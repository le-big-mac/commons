"""Print each occurrence of the given phrases in a file, with context.
usage: python3 -I ctx.py FILE WIDTH PHRASE [PHRASE ...]   (case-insensitive, plain substrings)"""
import sys, re
path, width = sys.argv[1], int(sys.argv[2])
phrases = sys.argv[3:]
lines = open(path, encoding='utf-8').read().split('\n')
for ph in phrases:
    n = 0
    for i, line in enumerate(lines, 1):
        for m in re.finditer(re.escape(ph), line, flags=re.I):
            n += 1
            a, b = max(0, m.start() - width), min(len(line), m.end() + width)
            print('[%s] line %d col %d: ...%s>>>%s<<<%s...' % (ph, i, m.start(), line[a:m.start()], line[m.start():m.end()], line[m.end():b]))
    print('[%s] %d occurrence(s)\n' % (ph, n))
