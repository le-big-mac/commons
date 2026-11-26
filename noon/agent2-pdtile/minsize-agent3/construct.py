"""The construction that attains the minimum when Phi_q does not divide A (from the prior-art reader's hand derivation, section 3),
checked for EVERY pattern with 0 not in F: build it, find its exact pattern by complex values and by exact integer division, compare sizes.
usage: construct.py NMAX p q [p q ...]"""
import sys, itertools, cmath, math
sys.path.insert(0, '/home/agent3/minsize')
from minsize import exact_pattern, cyclotomic
def build(p, q, n, E, F):
    """multiset on Z_M as a list of weights; level l is the base-p digit number l-1 of u (u mod p^l decides the class of depth l)"""
    M = p ** n * q; D = set(E) | set(F); EF = [l for l in E if l not in F]
    x = [0] * M
    inv = pow(p ** n, -1, q); invq = pow(q, -1, p ** n)
    def crt(u, w): return (u * q * invq + w * p ** n * inv) % M
    def members(free):
        for digs in itertools.product(*[(range(p) if l in free else (0,)) for l in range(1, n + 1)]):
            yield sum(d * p ** (l - 1) for l, d in zip(range(1, n + 1), digs)), digs
    for u, digs in members(D):                                   # A1
        tau = 1 if (EF and all(digs[l - 1] != 0 for l in EF)) else 0
        x[crt(u, tau)] += 1
    if any(l not in E for l in F):                               # A2, only when F is not inside E
        for u, digs in members(set(E)):
            for w in range(q): x[crt(u, w)] += 1
    return x
def exact_by_division(p, q, n, x):
    def divides(d):
        phi = cyclotomic(d); r = list(x)
        for k in range(len(r) - len(phi), -1, -1):
            c = r[k + len(phi) - 1]
            if c:
                for t, dc in enumerate(phi): r[k + t] -= c * dc
        return not any(r[:len(phi) - 1])
    return tuple(a for a in range(1, n + 1) if divides(p ** a)), tuple(a for a in range(0, n + 1) if divides(p ** a * q))
nmax = int(sys.argv[1]); pairs = [(int(sys.argv[i]), int(sys.argv[i + 1])) for i in range(2, len(sys.argv), 2)]
for p, q in pairs:
    for n in range(1, nmax + 1):
        ok = bad = sets = 0; M = p ** n * q
        for ke in range(n + 1):
            for E in itertools.combinations(range(1, n + 1), ke):
                for kf in range(n + 1):
                    for F in itertools.combinations(range(1, n + 1), kf):
                        x = build(p, q, n, E, F)
                        k = len([a for a in F if a not in E]); want = p ** len(E) * (p ** k + q) if k else p ** len(E)
                        pat = exact_pattern(p, q, n, x)
                        good = (pat == (E, F)) and sum(x) == want
                        if good and M <= 400: good = exact_by_division(p, q, n, x) == (E, F)
                        ok += good; bad += (not good); sets += (max(x) <= 1)
                        if not good and bad <= 3: print('   NOT AS WANTED', p, q, n, E, F, 'pattern', pat, 'size', sum(x), 'want', want)
        print(f'p={p} q={q} n={n} order {M}: {ok} patterns with the wanted pattern and size, {bad} not; the construction is a set in {sets}' + ('' if M <= 400 else ' (pattern by complex values only)'))
