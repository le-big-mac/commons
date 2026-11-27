"""Exhaustive test (all signings) of the level bound and of the union bound on small groups.

For a multiset B of m elements on Z_n:
  B_flat, n_flat = canonical contraction (every level of every tree of B_flat has a full group).
  (a) Lemma 2 / Proposition 3 of the note: a signing good for B_flat is good for B.
  (b) Level bound: for every d | n_flat, d > 1:  #(signings with Phi_d | S) <= 2^(m - mu(d)).
      Finer form: for every prime p | d, with p^i || d:  fraction <= prod over the occupied groups D at level i
      of the p-tree of 2^(-min(k_D, p-1)), k_D = number of occupied subclasses of D.
  (c) Union bound: fraction of bad signings of B_flat <= c_m + sum over d | n_flat, d > 1 of 2^(-mu(d)).
  (d) Control: the level bound (b) applied to B itself on Z_n, WITHOUT contracting (expected to fail sometimes).

usage: test_levels.py n mmin mmax count seed kind   (kind: random | full | coset | mixed)
"""
import sys
import random
from fractions import Fraction as Fr
import numpy as np
from lib4 import (factor, divisors, mu, all_signs, bad_table, all_full, contract, crt, c_even, digits)


def gen_random(n, m, rng):
    return [rng.randrange(n) for _ in range(m)]


def gen_full(n, m, rng):
    """every level of every tree has a full group (needs m >= 1 + a(p-1) for every p^a || n)"""
    f = factor(n)
    cols = []
    for p, a in f.items():
        q = p ** a
        spine = rng.randrange(q)
        req = [spine]
        for t in range(1, a + 1):
            for j in range(1, p):
                r = (spine % p ** (t - 1)) + ((digits(spine, p, a)[t - 1] + j) % p) * p ** (t - 1)
                r += p ** t * rng.randrange(p ** (a - t))
                req.append(r % q)
        if len(req) > m:
            return None
        rest = []
        for _ in range(m - len(req)):
            u = rng.random()
            if u < 0.4:
                rest.append(rng.randrange(q))
            elif u < 0.8:
                base = rng.choice(req + rest)
                t = rng.randrange(a + 1)
                rest.append((base % p ** t) + p ** t * rng.randrange(p ** (a - t)))
            else:
                rest.append(rng.choice(req + rest))
        col = req + rest
        rng.shuffle(col)
        cols.append((col, q))
    return [crt([(col[k], q) for col, q in cols])[0] for k in range(m)]


def gen_coset(n, m, rng):
    """union of cosets of subgroups, then points added or removed to reach m elements"""
    B = []
    ds = [d for d in divisors(n) if 1 < d <= m]
    tries = 0
    while len(B) < m and tries < 20:
        tries += 1
        if not ds:
            break
        d = rng.choice(ds)
        if len(B) + d > m + 2:
            continue
        s = rng.randrange(n)
        B += [(s + k * (n // d)) % n for k in range(d)]
    while len(B) < m:
        B.append(rng.randrange(n) if rng.random() < 0.5 else rng.choice(B) if B else 0)
    rng.shuffle(B)
    return B[:m]


def main():
    n = int(sys.argv[1]); mmin = int(sys.argv[2]); mmax = int(sys.argv[3])
    count = int(sys.argv[4]); seed = int(sys.argv[5]); kind = sys.argv[6]
    rng = random.Random(seed)
    stats = dict(tested=0, signings=0, lemma2_viol=0, level_viol=0, fine_viol=0, union_viol=0,
                 control_tested=0, control_viol=0, nflat={}, )
    tight = Fr(0)          # max of fraction_bad(d) * 2^mu(d)
    tight_at = None
    worst_union = Fr(0)    # max of (bad fraction) / (union bound)
    worst_union_at = None
    least_good = Fr(1)
    least_good_at = None
    for it in range(count):
        m = rng.randint(mmin, mmax)
        k = kind if kind != 'mixed' else rng.choice(['random', 'full', 'full', 'coset'])
        B = {'random': gen_random, 'full': gen_full, 'coset': gen_coset}[k](n, m, rng)
        if B is None:
            continue
        Bf, nf = contract(B, n)
        assert all_full(Bf, nf)
        if k == 'full':
            assert nf == n, (B, n, nf)
        E = all_signs(m)
        tot = E.shape[0]
        tabF = bad_table(Bf, nf, E)
        badF = np.zeros(tot, dtype=bool)
        for d, b in tabF.items():
            badF |= b
        stats['tested'] += 1
        stats['signings'] += tot
        stats['nflat'][nf] = stats['nflat'].get(nf, 0) + 1
        # (a)
        if nf != n:
            tabB = bad_table(B, n, E)
            badB = np.zeros(tot, dtype=bool)
            for d, b in tabB.items():
                badB |= b
            if (badB & ~badF).any():
                stats['lemma2_viol'] += 1
                print("LEMMA 2 VIOLATED", n, B)
            # (d) control
            stats['control_tested'] += 1
            if any(Fr(int(b.sum()), tot) > Fr(1, 2 ** mu(d)) for d, b in tabB.items() if d > 1):
                stats['control_viol'] += 1
        # (b)
        ff = factor(nf)
        bound_sum = c_even(m)
        for d, b in tabF.items():
            if d == 1:
                assert Fr(int(b.sum()), tot) == c_even(m)
                continue
            frac = Fr(int(b.sum()), tot)
            bound_sum += Fr(1, 2 ** mu(d))
            if frac > Fr(1, 2 ** mu(d)):
                stats['level_viol'] += 1
                print("LEVEL BOUND VIOLATED", nf, Bf, d)
            if frac * 2 ** mu(d) > tight:
                tight = frac * 2 ** mu(d); tight_at = (nf, d, list(Bf))
            for p, i in factor(d).items():
                groups = {}
                for x in Bf:
                    groups.setdefault(x % p ** (i - 1), set()).add((x // p ** (i - 1)) % p)
                ex = sum(min(len(s), p - 1) for s in groups.values())
                if frac > Fr(1, 2 ** ex):
                    stats['fine_viol'] += 1
                    print("FINER BOUND VIOLATED", nf, Bf, d, p)
        # (c)
        fb = Fr(int(badF.sum()), tot)
        if fb > bound_sum:
            stats['union_viol'] += 1
            print("UNION BOUND VIOLATED", nf, Bf)
        if bound_sum > 0 and fb / bound_sum > worst_union:
            worst_union = fb / bound_sum; worst_union_at = (nf, m, float(fb), float(bound_sum))
        if 1 - fb < least_good:
            least_good = 1 - fb; least_good_at = (nf, m, list(Bf))
    print(f"n={n} m={mmin}..{mmax} kind={kind} seed={seed}: multisets {stats['tested']}, signings {stats['signings']}")
    print(f"  contracted groups n_flat (count): {dict(sorted(stats['nflat'].items()))}")
    print(f"  (a) good for B_flat but bad for B: {stats['lemma2_viol']}")
    print(f"  (b) level bound violated: {stats['level_viol']}; finer bound violated: {stats['fine_viol']}")
    print(f"      largest fraction_bad(d) * 2^mu(d) = {tight} = {float(tight):.4f} at (n_flat, d, B_flat) = {tight_at}")
    print(f"  (c) union bound violated: {stats['union_viol']}; largest (bad fraction)/(bound) = {float(worst_union):.4f} at (n_flat, m, bad, bound) = {worst_union_at}")
    print(f"      least fraction of good signings = {least_good} = {float(least_good):.4f} at (n_flat, m, B_flat) = {least_good_at}")
    print(f"  (d) control, level bound on B without contraction: violated for {stats['control_viol']} of {stats['control_tested']} multisets with n_flat != n")


if __name__ == '__main__':
    main()
