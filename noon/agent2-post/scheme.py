"""Write out, as a strategy that verify.py can replay, the scheme of the second sheet: j blind questions, then blind letters that each
name a code the tree will leave over, then j letters that each name a code knowing the first 1, 2, ..., j answers.
usage: python -I scheme.py n k d  g1 g2 ... gj  > strategy.out      (codes as digits, e.g. 1123). Letters in all: d + 1 + j.
It fails loudly if the lag is too short for the codes left over."""
import sys, itertools
n, k, d = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); qs = sys.argv[4:]; j = len(qs)
def answer(g, s):
    b = sum(x == y for x, y in zip(g, s)); return f"{b}{sum(min(g.count(c), s.count(c)) for c in set(g)) - b}"
codes = ["".join(p) for p in itertools.product("123456"[:k], repeat=n) if "".join(p) not in qs]
# the tree: a node is the set of codes sharing the first `level` answers; it names one code; returns (codes left over, the names chosen)
names = {}                                             # (answers known as a tuple) -> code named there
def walk(cell, hist):
    level = len(hist)
    if level == j: left = list(cell)
    else:
        parts = {}
        for s in cell: parts.setdefault(answer(qs[level], s), []).append(s)
        left = [s for a in sorted(parts) for s in walk(parts[a], hist + (a,))]
    if left: names[hist] = left[0]; left = left[1:]    # name one of those still unnamed below
    return left
parts = {}
for s in codes: parts.setdefault(answer(qs[0], s), []).append(s)
over = [s for a in sorted(parts) for s in walk(parts[a], (a,))]
room = d + 1 - j
assert room >= len(over), f"{len(over)} codes are left over and only {room} blind letters are free at a lag of {d}"
blind = qs + over + [qs[0]] * (room - len(over))       # the questions, the codes left over, then anything
for t, g in enumerate(blind, 1): print(f"S {t} -:{g}")
def emit(hist):                                        # the letter sent knowing these answers
    t = d + 1 + len(hist)
    print(f"S {t} {','.join(hist)}:{names.get(hist, qs[0])}")
seen = set()
for s in codes:
    full = tuple(answer(q, s) for q in qs)
    for L in range(1, j + 1):
        if full[:L] not in seen: seen.add(full[:L]); emit(full[:L])
print(f"# {j} questions {' '.join(qs)}; {len(over)} codes left over; lag {d}; {d + 1 + j} letters", file=sys.stderr)
