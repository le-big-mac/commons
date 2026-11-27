"""Third pass: the table for the clock of 12 hours, by a search of my own.
Every marking (repeats allowed) of 1 to 18 marks on the 12 hours is counted by the exact set of divisors at which it balances.
A marking is a vector a[0..11] of counts; it balances at d iff the remainder of sum a[x] X^x on division by the cyclotomic
polynomial Phi_d is zero (whole numbers).  The remainder is linear in a, so the 12 hours are split into two halves, the
remainders of every half-marking are computed once, and the halves are joined: Phi_d divides iff the remainder of one half is
minus that of the other.  Nothing is taken from the author's program.  The least numbers are then set beside (1) the page's
table and sentence, (2) the author's table12.out, (3) Theorem 1 of the paper for p = 2, q = 3, n = 2.
usage: table12check.py [MAXSIZE]   (default 18)"""
import sys, itertools, re
import numpy as np
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
M = 12; DIVS = (2, 3, 4, 6, 12)

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def polydivexact(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1] // b[-1]; q[i] = c
        for j, y in enumerate(b): a[i + j] -= c * y
    assert not any(a)
    return q
_phi = {}
def phi(n):
    if n in _phi: return _phi[n]
    p = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n):
        if d < n: p = polydivexact(p, phi(d))
    _phi[n] = p; return p
def rem(a, b):
    a = a[:]
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        if c:
            for j, y in enumerate(b): a[i + j] -= c * y
    return a[:len(b) - 1]
def pattern_slow(marks):                       # the plain test, used to check the fast one and the page's instances
    a = [0] * M
    for x in marks: a[x % M] += 1
    return tuple(d for d in DIVS if not any(rem(a, phi(d))))

# remainder of X^x by each Phi_d, as rows of whole numbers: R[x] is the concatenation over d
blocks = []; R = []
for x in range(M):
    row = []
    for d in DIVS:
        mono = [0] * M; mono[x] = 1
        row += rem(mono, phi(d))
    R.append(row)
R = np.array(R, dtype=np.int64)
off = 0; cols = {}
for d in DIVS:
    k = len(phi(d)) - 1; cols[d] = (off, off + k); off += k
print('remainders of X^x by Phi_2, Phi_3, Phi_4, Phi_6, Phi_12 take', off, 'whole numbers; columns', cols)

# all half-markings (6 hours) by number of marks
half = {}
for m in range(0, MAX + 1):
    rows = []
    for c in itertools.combinations_with_replacement(range(6), m):
        v = [0] * 6
        for x in c: v[x] += 1
        rows.append(v)
    half[m] = np.array(rows, dtype=np.int64).reshape(len(rows), 6)
print('half-markings of 0..%d marks: %d' % (MAX, sum(len(v) for v in half.values())))
BASE = 2 * MAX + 3
def keys(U, sign):                             # one whole number for each block of a remainder vector
    out = []
    for d in DIVS:
        a, b = cols[d]; k = np.zeros(len(U), dtype=np.int64)
        for c in range(a, b): k = k * BASE + (sign * U[:, c] + MAX + 1)
        out.append(k)
    return out
K1 = {m: keys(half[m] @ R[:6], +1) for m in half}       # first half: hours 0..5
K2 = {m: keys(half[m] @ R[6:], -1) for m in half}       # second half: hours 6..11, sign turned
count = np.zeros((MAX + 1, 32), dtype=np.int64)         # count[m][code]: markings of m marks with pattern code
example = {}
for m in range(1, MAX + 1):
    for m1 in range(0, m + 1):
        m2 = m - m1; n1, n2 = len(half[m1]), len(half[m2])
        step = max(1, 3_000_000 // max(n2, 1))
        for i0 in range(0, n1, step):
            code = np.zeros((min(step, n1 - i0), n2), dtype=np.int8)
            for bit, d in enumerate(DIVS):
                code |= ((K1[m1][bit][i0:i0 + step, None] == K2[m2][bit][None, :]).astype(np.int8) << bit)
            bc = np.bincount(code.ravel(), minlength=32)
            for c in np.nonzero(bc)[0]:
                if int(c) not in example:
                    i, j = np.argwhere(code == c)[0]
                    a = list(half[m1][i0 + i]) + list(half[m2][j])
                    example[int(c)] = (m, [x for x in range(12) for _ in range(int(a[x]))])
            count[m] += bc
    print(f'{m} marks: {int(count[m].sum())} markings; patterns reached so far: {len(example)} of 32', flush=True)
import math
assert all(int(count[m].sum()) == math.comb(m + 11, 11) for m in range(1, MAX + 1)), 'not every marking counted'
print('every marking of 1 to %d marks counted once: %d in all' % (MAX, int(count[1:].sum())))

def pat(code): return tuple(d for bit, d in enumerate(DIVS) if code >> bit & 1)
least = {pat(c): m for c, (m, ex) in example.items()}
for c, (m, ex) in example.items(): assert pattern_slow(ex) == pat(c), (ex, pat(c))     # the fast test against the plain one
print('\nleast number of marks for each of the 32 patterns (repeats allowed), with an instance and the number of least markings:')
for p in sorted(least, key=lambda p: (len(p), p)):
    c = sum(1 << DIVS.index(d) for d in p); m, ex = example[c]
    rep = 'all hours different' if len(set(ex)) == len(ex) else 'an hour marked more than once'
    print(f'   balance at exactly {list(p) if p else "nothing"}: least {m}; e.g. {ex} ({rep}); least markings: {int(count[m][c])}')
print('patterns reached:', len(least), 'of 32;  patterns whose least number is more than 12:', {p: m for p, m in least.items() if m > 12})
print('the largest least number:', max(least.values()), 'for', [p for p, m in least.items() if m == max(least.values())])

print('\n--- (1) the page\'s table')
rows = [((12,), 5, [0, 6, 1, 5, 9]), ((4, 12), 2, [0, 6]), ((3,), 3, [0, 1, 2]), ((2, 6), 2, [0, 3]), ((2, 3, 4, 6, 12), 12, list(range(12)))]
for p, n, inst in rows:
    print(f'   to balance at {p}: page says {n}, search says {least.get(p)}; the instance {inst} has {len(inst)} marks and balances exactly at {pattern_slow(inst)}:',
          'RIGHT' if least.get(p) == n and pattern_slow(inst) == p and len(inst) == n else 'WRONG')
print('   "32 patterns, with the one that asks for no balance at all (one mark does that)":', len(least) == 32 and least.get(()) == 1)
print('   "for none of them is the least number more than 12":', all(m <= 12 for m in least.values()) and len(least) == 32)

print('\n--- (2) the author\'s table12.out')
t = open('/home/agent3/door/table12/table12.out').read()
theirs = {}
for mm in re.finditer(r'balance at exactly (\[[^\]]*\]|nothing): least (\d+) marks', t):
    p = () if mm.group(1) == 'nothing' else tuple(int(x) for x in mm.group(1).strip('[]').split(','))
    theirs[p] = int(mm.group(2))
print('   patterns in it:', len(theirs), '; its last progress line:', [l for l in t.split('\n') if l.startswith('size')][-1])
print('   patterns missing from it:', sorted(set(least) - set(theirs)))
print('   values that differ from mine:', {p: (theirs[p], least[p]) for p in theirs if theirs[p] != least.get(p)})

print('\n--- (3) Theorem 1 of the paper for p = 2, q = 3, n = 2 (levels 1, 2 are the divisors 2, 4; with q: 6, 12)')
p_, q_, n_ = 2, 3, 2
def theorem(E, F, balanced):
    e = len(E)
    if not balanced:
        return p_ ** e if F <= E else p_ ** e * (p_ ** len(F - E) + q_)
    if F == set(range(1, n_ + 1)): return q_ * p_ ** e
    a0 = min(a for a in range(1, n_ + 1) if a not in F)
    G = {a for a in F - E if a > a0}; k = len(G)
    x = 0 if (k == 0 or any(a in E for a in range(1, a0)) or (a0 in E and p_ >= 3) or
              (k >= 1 and a0 in E and p_ == 2 and any(a0 < a < min(G) for a in E - F))) else 1
    return q_ * p_ ** e * (p_ ** k + x)
bad = 0
for p in sorted(least, key=lambda p: (len(p), p)):
    E = {a for a in (1, 2) if p_ ** a in p}; F = {a for a in (1, 2) if p_ ** a * q_ in p}; bal = q_ in p
    th = theorem(E, F, bal)
    if th != least[p]: bad += 1; print('   DIFFERS:', p, 'theorem', th, 'search', least[p])
print('   patterns on which the theorem\'s number and the search differ:', bad, 'of', len(least))
