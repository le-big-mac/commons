"""Least number of marks (repeats allowed) on the 12-hour clock for every pattern, by plain search with whole numbers.
A marking is a vector a[0..11] of non-negative counts.  It balances at d (d = 2, 3, 4, 6, 12) iff the cyclotomic polynomial
Phi_d divides sum a[x] X^x; tested by reducing modulo Phi_d with integer arithmetic.  Markings are tried in order of size,
and within a size in lexicographic order of the sorted list of marks, so the first marking found for a pattern is a least one.
usage: table12.py [MAXSIZE]   (default 12)"""
import sys, itertools
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
def bal(a):
    c2 = [sum(a[x] for x in range(12) if x % 2 == r) for r in range(2)]
    c3 = [sum(a[x] for x in range(12) if x % 3 == r) for r in range(3)]
    c4 = [sum(a[x] for x in range(12) if x % 4 == r) for r in range(4)]
    b = [sum(a[x] for x in range(12) if x % 6 == r) for r in range(6)]
    out = []
    if c2[0] == c2[1]: out.append(2)
    if c3[0] == c3[1] == c3[2]: out.append(3)
    if c4[0] == c4[2] and c4[1] == c4[3]: out.append(4)                    # Phi_4 = X^2 + 1
    if b[0] - b[2] - b[3] + b[5] == 0 and b[1] + b[2] - b[4] - b[5] == 0: out.append(6)     # Phi_6 = X^2 - X + 1
    if (a[0] - a[4] - a[6] + a[10] == 0 and a[1] - a[5] - a[7] + a[11] == 0 and
        a[2] + a[4] - a[8] - a[10] == 0 and a[3] + a[5] - a[9] - a[11] == 0): out.append(12)   # Phi_12 = X^4 - X^2 + 1
    return tuple(out)
best = {}
for m in range(1, MAX + 1):
    for marks in itertools.combinations_with_replacement(range(12), m):
        if marks[0] != 0: break                    # turning a marking does not change where it balances: start at hour 0
        a = [0] * 12
        for x in marks: a[x] += 1
        p = bal(a)
        if p not in best: best[p] = (m, marks)
    print(f'size {m}: {len(best)} of 32 patterns found so far', flush=True)
    if len(best) == 32: break
print()
for p in sorted(best, key=lambda p: (len(p), p)):
    m, marks = best[p]
    rep = 'an hour marked more than once' if len(set(marks)) < m else 'all hours different'
    print(f'balance at exactly {list(p) if p else "nothing"}: least {m} marks, for instance {list(marks)} ({rep})')
