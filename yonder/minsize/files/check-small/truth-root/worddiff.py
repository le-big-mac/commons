import sys, difflib
# usage: worddiff.py OLD NEW oldline newline   (1-based line numbers); prints changed word runs with context
old = open(sys.argv[1], encoding="utf-8").read().split("\n")
new = open(sys.argv[2], encoding="utf-8").read().split("\n")
a = old[int(sys.argv[3]) - 1].split()
b = new[int(sys.argv[4]) - 1].split()
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    print("---", tag, "after: ...", " ".join(a[max(0, i1 - 8):i1]))
    print("   OLD:", " ".join(a[i1:i2]))
    print("   NEW:", " ".join(b[j1:j2]))
    print("   before: ", " ".join(a[i2:i2 + 6]), "...")
