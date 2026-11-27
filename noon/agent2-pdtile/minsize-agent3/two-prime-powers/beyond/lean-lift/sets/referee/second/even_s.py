"""Second pass, the step from one doubling to 'every even s' (the paper: 'So Corollary 21 also holds for every even s when
some least multiset has multiplicities at most 2').  The route, as I read it: take a least multiset on Z_M, M = p^n q,
with multiplicities at most 2 (not every element 2, being least); FIRST lift along one factor 2 by the paragraph's step
(two.step_two), which gives a set; then along the other factors 2 by Lemma 18 (sign every element of one class by
Lemma 17; + low, - high; the other classes low); then along the odd prime factors by Lemma 16 (every element to its lift
with t = 0, one element to its lift with t = 1).  Checked at the end: a set of m elements on Z_{M s} whose pattern among
the divisors > 1 of M s is exactly D.

The least multisets: for p odd, those of ../cap-witnesses.jsonl (multiplicities at most 2); for p = 2, found here by my
model (../sets_cpsat.solve) with the cap 2, where one exists.
usage: even_s.py TLIM"""
import sys, os, json, random, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cyc import pattern, divisors
from thm import theorem_m, D_of, all_patterns
from sets_cpsat import solve
from two import step_two, signs17, roles, factor
rnd = random.Random(9)
tlim = float(sys.argv[1])


def lift18(S, N):
    """Lemma 18 for a set S on Z_N (dict y -> 1): returns a set on Z_{2N}"""
    k = 0
    while N % 2 ** (k + 1) == 0: k += 1
    Np = N // 2 ** k
    P, a, Q = rnd.choice(roles(Np))
    cls = rnd.choice(sorted(set(x % 2 ** k for x in S)))
    inc = [x for x in sorted(S) if x % 2 ** k == cls]
    sg = dict(zip(inc, signs17([x % Np for x in inc], P, a, Q, rnd)))
    out = {}
    for x in S:
        lo = [y for y in (x, x + N) if y % 2 ** (k + 1) < 2 ** k][0]
        hi = [y for y in (x, x + N) if y % 2 ** (k + 1) >= 2 ** k][0]
        out[hi if sg.get(x, 1) == -1 else lo] = 1
    return out


def lift16(S, N, r):
    """Lemma 16 for a set S on Z_N, r an odd prime: returns a set on Z_{Nr}"""
    k = 0
    while N % r ** (k + 1) == 0: k += 1
    x0 = rnd.choice(sorted(S))
    out = {}
    for x in S:
        want = 1 if x == x0 else 0
        for u in range(r):
            y = x + N * u
            if (y % r ** (k + 1) - x % r ** k) // r ** k == want:
                out[y] = 1
    return out


def route(mult, M, s):
    f = factor(s)
    assert f.get(2, 0) >= 1
    cur = step_two(mult, M, rnd)
    N = 2 * M
    for _ in range(f[2] - 1):
        cur = lift18(cur, N); N *= 2
    for r in sorted(f):
        if r == 2: continue
        for _ in range(f[r]):
            cur = lift16(cur, N, r); N *= r
    assert N == M * s
    return cur


wit = {}
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cap-witnesses.jsonl')):
    o = json.loads(line)
    mult = {int(x): w for x, w in o['multiset'].items()}
    if max(mult.values()) <= 2:
        wit[(o['p'], o['q'], o['n'], tuple(o['E']), tuple(o['F']), o['balanced'])] = mult

for (p, q, n) in [(3, 2, 2), (3, 5, 2), (5, 2, 2), (5, 3, 2), (3, 2, 3), (2, 3, 2), (2, 5, 2), (2, 3, 3), (2, 5, 3), (2, 3, 4)]:
    M = p ** n * q
    have = none = und = 0
    runs = ok = 0
    ss = [s for s in (2, 4, 6, 8, 10, 12, 20, 36) if M * s <= 600]
    per_s = collections.Counter()
    for E, F, bal in all_patterns(p, q, n):
        m = theorem_m(p, q, n, E, F, bal); D = D_of(p, q, n, E, F, bal)
        key = (p, q, n, tuple(E), tuple(F), bal)
        mult = wit.get(key)
        if mult is None:
            st, mult = solve(M, D, 2, size=m, tlim=tlim)
            if mult is None:
                if st == 'INFEASIBLE': none += 1
                else: und += 1
                continue
        assert max(mult.values()) <= 2 and sum(mult.values()) == m and pattern(mult, M) == D
        assert not all(w == 2 for w in mult.values())
        have += 1
        for s in ss:
            S = route(mult, M, s)
            runs += 1
            good = (all(w == 1 for w in S.values()) and len(S) == m and pattern(S, M * s) == D)
            ok += good; per_s[s] += good
            if not good:
                print('FAIL', p, q, n, E, F, bal, s)
    print(f'Z_{M} (p={p}, q={q}, n={n}): patterns {2 ** (2 * n + 1)}; with a least multiset of multiplicities <= 2: {have}; none exists (solver: infeasible): {none}; '
          f'undecided in {tlim:.0f} s: {und}; routes for s in {ss}: {runs}; a set of m elements with exactly the pattern on Z_(M s): {ok}', flush=True)
