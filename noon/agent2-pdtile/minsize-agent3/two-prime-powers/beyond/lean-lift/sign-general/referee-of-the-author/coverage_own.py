"""Referee's own coverage count, written from the text of sign-general-result.md (sections 3, 4) and
sign-lemma-result.md (Theorems 2, 3).  Exact fractions.

 Theorem 2:  n = p^a q^b   (at most two distinct primes)
 Theorem 3:  n = p r q^b   (three distinct primes, at least two of them to the first power)
 Theorem 6:  n = m q^b, q an odd prime not dividing m, b >= 0 (or n = m), with c(m) > 0, where
             c(1) = 1,  c(m) = max over primes p | m with c(m/p) > 0 of
                               min( c(m/p)/2 , c(m/p) - tau(m') 2^(1-p) ),  m' = part of m/p prime to p.
 Also, separately, the definition of Theorem P' itself (families of levels on the digit box) for small m,
 to see that the recursion of section 4 is what the definition gives for the tree levels.
usage: coverage_own.py LIMIT
"""
import sys
from fractions import Fraction as Fr
from functools import lru_cache
from itertools import combinations

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 200000

def factor(n):
    f = {}
    d = 3
    assert n % 2 == 1
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def tau_of(f):
    t = 1
    for e in f.values():
        t *= e + 1
    return t

@lru_cache(maxsize=None)
def c_rec(key):
    """key: sorted tuple of (p, a_p).  The recursion of section 4."""
    if not key:
        return Fr(1)
    best = None
    f = dict(key)
    for p in f:
        g = dict(f)
        g[p] -= 1
        if g[p] == 0:
            del g[p]
        cm = c_rec(tuple(sorted(g.items())))
        if cm <= 0:
            continue
        mprime = {r: a for r, a in f.items() if r != p}
        val = min(cm / 2, cm - Fr(tau_of(mprime) * 2, 2 ** p))
        if best is None or val > best:
            best = val
    return Fr(-1) if best is None else best

def c_of(n):
    return c_rec(tuple(sorted(factor(n).items())))

# ---- the definition in Theorem P' on the digit box, with families of levels as explicit sets ----
@lru_cache(maxsize=None)
def c_family(sides, fam):
    """sides: tuple of (label, size); fam: frozenset of frozensets of labels (subset-closed)."""
    if not sides:
        return Fr(1)
    best = None
    for j, (lab, nj) in enumerate(sides):
        rest = sides[:j] + sides[j + 1:]
        L0 = frozenset(P for P in fam if lab not in P)
        L1 = frozenset(P - {lab} for P in fam if lab in P)
        c0 = c_family(rest, L0)
        if c0 <= 0:
            continue
        val = min(c0 / 2, c0 - Fr(len(L1) * 2, 2 ** nj))
        if best is None or val > best:
            best = val
    return Fr(-1) if best is None else best

def tree_family(f):
    labs = [(p, e) for p in sorted(f) for e in range(1, f[p] + 1)]
    fam = set()
    for r in range(len(labs) + 1):
        for P in combinations(labs, r):
            if len({p for p, _ in P}) == len(P):
                fam.add(frozenset(P))
    sides = tuple(((p, e), p) for (p, e) in labs)
    return sides, frozenset(fam)

def all_family(f):
    labs = [(p, e) for p in sorted(f) for e in range(1, f[p] + 1)]
    fam = set()
    for r in range(len(labs) + 1):
        for P in combinations(labs, r):
            fam.add(frozenset(P))
    return tuple(((p, e), p) for (p, e) in labs), frozenset(fam)

def thm2(f):
    return len(f) <= 2

def thm3(f):
    return len(f) == 3 and sum(1 for e in f.values() if e == 1) >= 2

def thmP_sorted(f):
    """digits of m in increasing order: n_1 >= 3, n_j >= 2j (Theorem P applies to the digit box of m)."""
    digs = sorted(p for p in f for _ in range(f[p]))
    return all(d >= max(3, 2 * (j + 1)) for j, d in enumerate(digs))

def thm6_ways(n, f):
    """list of (q or None, kind) for which Theorem 6 applies to n = m q^b."""
    ways = []
    if c_rec(tuple(sorted(f.items()))) > 0:
        ways.append((None, 'P' if thmP_sorted(f) else "P'"))
    for q in f:
        g = {r: a for r, a in f.items() if r != q}
        if c_rec(tuple(sorted(g.items()))) > 0:
            ways.append((q, 'P' if (not g or thmP_sorted(g)) else "P'"))
    return ways

def squarefree(f):
    return all(e == 1 for e in f.values())

def one_repeated(f):
    return sum(1 for e in f.values() if e >= 2) <= 1

if __name__ == '__main__':
    # 1. recursion of section 4 against the definition of Theorem P' (tree levels), small m
    bad = 0; tested = 0
    for m in range(1, 6000, 2):
        f = factor(m)
        if sum(f.values()) > 6:
            continue
        sides, fam = tree_family(f)
        a = c_family(sides, fam); b = c_rec(tuple(sorted(f.items())))
        tested += 1
        # only the sign and, where positive, the value are compared
        if (a > 0) != (b > 0) or (a > 0 and a != b):
            bad += 1
            print('DIFFERENCE recursion/definition at m =', m, a, b)
    print(f'recursion of section 4 against the definition in Theorem P\' (tree levels of the digit box): '
          f'{tested} odd m < 6000 with at most 6 digits, differences: {bad}')
    # values quoted in the text
    for m, name in [(175, '5^2*7'), (63, '3^2*7'), (441, '3^2*7^2'), (27, '3^3'), (3125, '5^5'), (875, '5^3*7'),
                    (4375, '5^4*7'), (189, '3^3*7'), (6125, '5^3*7^2'), (1225, '5^2*7^2'), (225, '3^2*5^2')]:
        print(f'   c({m} = {name}) = {c_of(m)}')
    # 2. coverage
    unc = []; by6only = []; by6 = 0; n_odd = 0
    by_ab_only = 0; need_rec = []
    sqf_or_one = 0; sqf_or_one_not23 = 0
    for n in range(1, LIMIT, 2):
        f = factor(n); n_odd += 1
        t2, t3 = thm2(f), thm3(f)
        ways = thm6_ways(n, f)
        t6 = bool(ways)
        if t6: by6 += 1
        if not (t2 or t3 or t6):
            unc.append((n, f))
        if t6 and not (t2 or t3):
            by6only.append(n)
        ab = one_repeated(f)          # (a) or (b): at most one prime with exponent >= 2
        if ab:
            sqf_or_one += 1
            assert t6, n               # (a), (b) must be inside Theorem 6
            if not (t2 or t3): sqf_or_one_not23 += 1
        if t6 and not ab and not (t2 or t3):
            need_rec.append((n, ways))
    print(f'odd n < {LIMIT}: {n_odd}')
    print(f'covered by nothing: {len(unc)}: {unc[:10]}')
    print(f'covered by Theorem 6 and not by Theorems 2, 3: {len(by6only)}; first: {by6only[:12]}')
    print(f'covered by Theorem 6 at all: {by6}')
    print(f'n with at most one repeated prime ((a) or (b)): {sqf_or_one}, all inside Theorem 6 (asserted); '
          f'of them not in Theorems 2, 3: {sqf_or_one_not23}')
    print(f'covered only through "further cases" (two or more repeated primes, not Theorems 2, 3): {len(need_rec)}; '
          f'first: {need_rec[:6]}')
    # of the further cases: those where Theorem P itself (sorted digits n_j >= 2j) suffices for some q,
    # and those that need the recursion P' (tree levels)
    onlyPprime = [n for n, ways in need_rec if all(k == "P'" for _, k in ways)]
    print(f'   of these, those for which no choice of q lets Theorem P itself apply (the recursion is needed): '
          f'{len(onlyPprime)}; first: {onlyPprime[:10]}')
    below = [n for n in onlyPprime if n < 118125]
    print(f'   of those, below 118125: {len(below)}; first {below[:10]}')
    for n in [1155, 1365, 1575, 3465, 5005, 11025, 7875, 15015, 23625, 33075, 84375, 118125, 165375, 1157625]:
        f = factor(n)
        print(f'   {n} {f}: Thm2 {thm2(f)} Thm3 {thm3(f)} Thm6 {thm6_ways(n, f)}')
