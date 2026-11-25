"""Independent check (Python, from the definition) of the witnesses q2.c printed for K(3)<=5."""
import itertools, sys
codes = list(itertools.product(range(6), repeat=4))
def ans(g, c):
    b = sum(x == y for x, y in zip(g, c))
    return (b, sum(min(g.count(q), c.count(q)) for q in range(6)) - b)
amap = [(b, w) for b in range(5) for w in range(5 - b) if (b, w) != (3, 1)]
def show(i): return ''.join(str(x + 1) for x in codes[i])
for f in sys.argv[1:]:
    line = [l for l in open(f) if l.startswith('WITNESS')][0]
    left, right = line.split(';')
    g = [int(x) for x in left.split('=')[1].split()]
    g5 = [int(x) for x in right.split(':')[1].split()]
    seen = {}
    for c in codes:
        a1 = ans(codes[g[0]], c)
        fifth = g5[amap.index(a1)]          # guess 5 uses answer 1 only
        key = (a1,) + tuple(ans(codes[x], c) for x in g[1:]) + (ans(codes[fifth], c),)
        seen.setdefault(key, []).append(c)
    worst = max(len(v) for v in seen.values())
    print(f, 'blind:', ' '.join(show(x) for x in g), '| distinct answer rows', len(seen), 'of 1296, largest class', worst,
          '=> five guesses at lag 3 determine every code' if worst == 1 else '=> FAILS')
