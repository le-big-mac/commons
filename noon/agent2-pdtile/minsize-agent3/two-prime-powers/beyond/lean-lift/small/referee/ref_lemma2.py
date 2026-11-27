"""Referee's test of the contraction lemma (Lemma 2 of small-multisets.md), written from its statement.

Statement tested.  n odd, p^a || n, 1 <= t <= a.  Level t of the p-tree is contractible for a multiset B on Z_n if every
class modulo p^(t-1) that holds an element of B has a class modulo p^t inside it that holds none.  B-flat on Z_(n/p):
delete the base-p digit of index t-1 of (x mod p^a), keep x mod n/p^a.  Claim: every signing that is good for B-flat on
Z_(n/p) is good for B on Z_n.  (good: the signed mask is divisible by no Phi_d, d | group order; exact arithmetic.)

modes
  exh N K        every multiset of 1..K elements on Z_N, every prime p | N, every level t: all signings.
                 For the levels that are NOT contractible the same implication is counted too (it is not claimed; the
                 count shows that the test can fail).
  rnd SEED COUNT random and structured multisets of 2..10 elements on larger groups; all signings; tallied by case.
"""
import sys, random
from itertools import combinations_with_replacement
import numpy as np
from reflib import *


def check(n, el, p, a, t, tally, key):
    """returns number of violations of 'good for the contracted multiset => good for the original'."""
    fl = contract(el, n, p, a, t)
    g = good_all(n, el)
    gf = good_all(n // p, fl)
    viol = int((gf & ~g).sum())
    T = tally.setdefault(key, [0, 0, 0, 0, 0, 0])
    T[0] += 1                       # multisets
    T[1] += len(g)                  # signings
    T[2] += int((~g).sum())         # bad for the original
    T[3] += int(gf.sum())           # good for the contracted one (instances of the implication)
    T[4] += viol                    # violations
    T[5] += int((g & ~gf).sum())    # converse fails
    return viol, fl


def show(tally, title):
    print(title)
    print('   case: multisets, signings, bad for B, good for B-flat (instances), VIOLATIONS, converse fails')
    for k in sorted(tally, key=str):
        print('   ', k, ':', ', '.join(str(v) for v in tally[k]))


def run_exh(N, K):
    f = factor(N)
    tally = {}; tally_non = {}
    first_viol_non = None
    for k in range(1, K + 1):
        for el in combinations_with_replacement(range(N), k):
            el = list(el)
            for p, a in f.items():
                for t in range(1, a + 1):
                    if contractible(el, p, a, t):
                        key = (f'p={p}', f'a={a}', f't={t}', 'branching' if branches(el, p, a, t) else 'no branching')
                        v, fl = check(N, el, p, a, t, tally, key)
                        if v:
                            print('VIOLATION of Lemma 2:', N, el, p, a, t, fl); sys.exit(1)
                    else:
                        key = (f'p={p}', f'a={a}', f't={t}', 'NOT contractible')
                        v, fl = check(N, el, p, a, t, tally_non, key)
                        if v and first_viol_non is None:
                            first_viol_non = (el, p, a, t, fl)
    show(tally, f'Z_{N}, every multiset of 1..{K} elements, contractible levels (Lemma 2 claims 0 violations):')
    show(tally_non, f'Z_{N}, the same multisets, levels that are not contractible (nothing claimed):')
    if first_viol_non:
        el, p, a, t, fl = first_viol_non
        print(f'   first failure without the hypothesis: B = {el}, p = {p}, t = {t}, contracted to {fl} on Z_{N // p}')


def gen(rng, n, f, m):
    kind = rng.randrange(6)
    ps = list(f)
    if kind == 0:
        return [rng.randrange(n) for _ in range(m)]
    if kind == 1:                                   # points of one coset of a subgroup, with repeats
        d = rng.choice([x for x in divisors(n) if x > 1]); c = rng.randrange(n)
        return [(c + (n // d) * rng.randrange(d)) % n for _ in range(m)]
    if kind == 2:                                   # whole cosets of subgroups of prime order, then random points
        el = []
        while len(el) < m:
            q = rng.choice(ps); c = rng.randrange(n)
            if len(el) + q <= m and rng.random() < 0.8:
                el += [(c + (n // q) * j) % n for j in range(q)]
            else:
                el.append(rng.randrange(n))
        return el
    if kind == 3:                                   # full groups at lower levels: c + j * q^i * unit
        el = []
        while len(el) < m:
            q = rng.choice(ps); i = rng.randrange(f[q]); c = rng.randrange(n)
            step = q ** i * (n // q ** f[q])
            if len(el) + q <= m and rng.random() < 0.8:
                el += [(c + step * j) % n for j in range(q)]
            else:
                el.append(rng.choice(el) if el and rng.random() < 0.4 else rng.randrange(n))
        return el
    if kind == 4:                                   # a small pool with repeats
        pool = [rng.randrange(n) for _ in range(rng.randint(1, 4))]
        return [rng.choice(pool) for _ in range(m)]
    # kind 5: cosets with one point moved or removed
    el = gen(rng, n, f, m)
    j = rng.randrange(len(el)); el[j] = rng.randrange(n)
    return el


def run_rnd(seed, count):
    rng = random.Random(seed)
    shapes = [27, 81, 243, 45, 135, 405, 63, 189, 75, 225, 375, 125, 147, 441, 105, 315, 525, 99, 117, 175, 245, 495, 675, 729, 343, 1125]
    tally = {}
    done = 0; tries = 0
    while done < count:
        tries += 1
        n = rng.choice(shapes); f = factor(n)
        m = rng.randint(2, 10)
        el = gen(rng, n, f, m)[:m]
        p = rng.choice(list(f)); a = f[p]; t = rng.randint(1, a)
        if not contractible(el, p, a, t):
            # try to repair: remove from each full group the elements of one subclass
            occ = {}
            for x in el:
                u = x % p ** a
                occ.setdefault(u % p ** (t - 1), set()).add((u // p ** (t - 1)) % p)
            kill = {k: rng.choice(sorted(v)) for k, v in occ.items() if len(v) == p}
            el = [x for x in el if not ((x % p ** a) % p ** (t - 1) in kill and ((x % p ** a) // p ** (t - 1)) % p == kill[(x % p ** a) % p ** (t - 1)])]
            if len(el) < 2 or not contractible(el, p, a, t):
                continue
        key = (f'p={p}', 'a=1' if a == 1 else 'a>1', 't=1' if t == 1 else ('t=a' if t == a else '1<t<a'),
               'branching' if branches(el, p, a, t) else 'no branching')
        v, fl = check(n, el, p, a, t, tally, key)
        if v:
            print('VIOLATION of Lemma 2:', n, el, p, a, t, fl); sys.exit(1)
        done += 1
    show(tally, f'random and structured multisets of 2..10 elements (seed {seed}, {count} multisets with a contractible level; groups {shapes}):')
    tot = [sum(v[i] for v in tally.values()) for i in range(6)]
    print('   total:', ', '.join(str(x) for x in tot))


if __name__ == '__main__':
    if sys.argv[1] == 'exh':
        run_exh(int(sys.argv[2]), int(sys.argv[3]))
    else:
        run_rnd(int(sys.argv[2]), int(sys.argv[3]))
