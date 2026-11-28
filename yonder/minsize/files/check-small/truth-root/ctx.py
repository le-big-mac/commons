import sys, re
# usage: ctx.py FILE WIDTH pattern [pattern ...]   (plain substrings, case-sensitive)
path = sys.argv[1]
w = int(sys.argv[2])
pats = sys.argv[3:]
lines = open(path, encoding="utf-8").read().split("\n")
for p in pats:
    print("=== %r" % p)
    n = 0
    for i, line in enumerate(lines, 1):
        for m in re.finditer(re.escape(p), line):
            n += 1
            a = max(0, m.start() - w)
            b = min(len(line), m.end() + w)
            print("  L%d c%d: ...%s..." % (i, m.start(), line[a:b]))
    print("  (%d hits)" % n)
