"""Second look: the author's test squarefree_own.py, replayed with the same random stream (same seed, same calls in the
same order) but with the referee's own exact long division (thm6_own.cyc_divisors) in place of the sympy remainder.
If the two division routines agree, the counts of the author's output must come out the same.
usage: replicate_squarefree.py n COUNT [seed]"""
import sys, random
sys.path.insert(0, '/home/agent3/paper/referee-signs')
from thm6_own import cyc_divisors, cyclotomic, factor
n = int(sys.argv[1]); cnt = int(sys.argv[2]); random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
fn = factor(n); ps = sorted(fn); assert all(e == 1 for e in fn.values()) and n % 2
divs = [d for d in range(1, n + 1) if n % d == 0]
for d in divs: cyclotomic(d)
def zeros(sg):
    return cyc_divisors({x: c for x, c in sg.items() if c}, n, divs)
tried_tot = 0; worst = 0; allplus_bad = 0; found = 0
for _ in range(cnt):
    B = set()
    for _c in range(random.randint(1, 3)):
        d = random.choice([d for d in divs if 1 < d < n]); x0 = random.randrange(n); B |= {(x0 + d * j) % n for j in range(n // d)}
    for _c in range(random.randint(0, 3)): B ^= {random.randrange(n)}
    if not B: continue
    if zeros({x: 1 for x in B}): allplus_bad += 1
    for t in range(1, 400):
        sig = {p: [random.choice((1, -1)) for _ in range(p)] for p in ps}
        sg = {}
        for x in B:
            s = 1
            for p in ps: s *= sig[p][x % p]
            sg[x] = s
        if not zeros(sg): found += 1; tried_tot += t; worst = max(worst, t); break
print(f'n = {n}: {cnt} sets; all + has a cyclotomic divisor for {allplus_bad}; a good signing of product form found for {found}; '
      f'random patterns tried: {tried_tot / max(found, 1):.2f} on average, at most {worst}')
