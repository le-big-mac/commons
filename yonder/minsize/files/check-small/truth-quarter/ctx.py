import sys, re
path = sys.argv[1]
pats = sys.argv[2:]
text = open(path, encoding="utf-8").read()
lines = text.split("\n")
for p in pats:
    print("=== %r" % p)
    for i, line in enumerate(lines, 1):
        for m in re.finditer(re.escape(p), line):
            a = max(0, m.start() - 170)
            b = min(len(line), m.end() + 170)
            print("  L%d @%d: ...%s..." % (i, m.start(), line[a:b]))
