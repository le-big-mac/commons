"""Exact test of the contraction lemma (27 Nov 2026, agent3).
n = p^a n'', p not dividing n''.  Level t (1 <= t <= a) of the p-tree is CONTRACTIBLE for a multiset B on Z_n if every class
mod p^(t-1) that holds elements of B has a class mod p^t inside it that holds none.  Deleting the p-adic digit of index t-1
of every element gives a multiset on Z_(n/p).  Claim: every signing that is good for the contracted multiset (its signed mask
has no cyclotomic divisor Phi_d, d | n/p) is good for B (no Phi_d, d | n).  The converse is not claimed; the test counts how
often it fails.          usage: test_contract.py SEED COUNT"""
import sys, random, itertools
sys.path.insert(0, '/home/agent3/lean/lift-check/mod4')
from star import exact_ok

def crt(r1, m1, r2, m2):
    for k in range(m2):
        x = r1 + m1 * k
        if x % m2 == r2: return x % (m1 * m2)
def digits(x, p, a): return [(x // p ** i) % p for i in range(a)]
def undig(d, p): return sum(v * p ** i for i, v in enumerate(d))
def signings(m):
    for k in range(m):
        for M in itertools.combinations(range(1, m), k): yield M
def good(n, B, M): return exact_ok(n, tuple(B), tuple(B[i] for i in M))

rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
shapes = [(3, 2, 1), (3, 2, 5), (3, 3, 1), (5, 2, 1), (5, 2, 3), (3, 2, 7), (5, 1, 9), (3, 3, 5), (5, 1, 3), (7, 1, 3), (5, 2, 9), (3, 1, 5), (3, 2, 25), (7, 1, 9), (5, 1, 21)]
cases = 0; signs = 0; both = 0; onlyB = 0; neither = 0; branching_cases = 0
while cases < count:
    p, a, n2 = rng.choice(shapes); n = p ** a * n2; t = rng.randint(1, a); m = rng.randint(2, 7)
    els = []
    for _ in range(m):
        d = [rng.randrange(p) for _ in range(a)]
        if els and rng.random() < 0.7:
            e = els[rng.randrange(len(els))][0]; k = rng.randint(0, a); d[:k] = e[:k]
        els.append((d, rng.randrange(n2)))
    # is level t contractible?  every group (prefix of length t-1) must miss at least one value of the digit of index t-1
    groups = {}
    for d, r in els: groups.setdefault(tuple(d[:t - 1]), set()).add(d[t - 1])
    if any(len(v) == p for v in groups.values()): continue
    if any(len(v) >= 2 for v in groups.values()): branching_cases += 1
    B = [(crt(undig(d, p), p ** a, r, n2) if n2 > 1 else undig(d, p)) for d, r in els]
    Bt = []
    for d, r in els:
        dt = d[:t - 1] + d[t:]
        Bt.append((crt(undig(dt, p), p ** (a - 1), r, n2) if n2 > 1 else undig(dt, p)) if a > 1 else r)
    for M in signings(m):
        x = good(n, B, M); y = good(n // p, Bt, M); signs += 1
        assert x or not y, ('CONTRACTION FAILS', p, a, n2, t, B, Bt, M)
        both += x and y; onlyB += x and not y; neither += (not x) and (not y)
    cases += 1
print(f'contraction: {cases} multisets ({branching_cases} of them with a level that branches), {signs} signings: good for both {both}, good for the original only {onlyB}, good for neither {neither}; good for the contracted one and not for the original: 0 (asserted)')
