"""Larger numbers of elements (14 to 20) with ALL signings (in chunks): exact fraction of good signings, and the
level bound at every d | n_flat.

kind 'full':     every level of every tree of Z_n has a full group (caterpillar with random spine, as in test_levels.py)
kind 'interval': the k-th element is pi_p(k) modulo p^a for every p^a || n, pi_p a random permutation of 0..m-1
                 (the first multiset has all pi_p = identity: it is the interval {0, .., m-1}); the classes are
                 as balanced as can be, so many classes at many levels hold several elements
The multiset is contracted first (my routine); the counts are for (B_flat, n_flat).

usage: even_exact.py n m count seed kind
"""
import sys
import random
from fractions import Fraction as Fr
import numpy as np
from lib4 import divisors, mu, powers_mod_phi, all_full, contract, c_even, factor, crt
from test_levels import gen_full


_cf = {}


def cyc_fast(d):
    """Phi_d as an int64 array, lowest coefficient first, by Phi_{dp}(X) = Phi_d(X^p) / Phi_d(X) (p not dividing d)
    and Phi_{dp}(X) = Phi_d(X^p) (p | d); exact integer division. (lib4.cyclotomic is too slow for d = 45045;
    the two are compared for the divisors of 315 and 675 at the start.)"""
    if d in _cf:
        return _cf[d]
    if d == 1:
        r = np.array([-1, 1], dtype=np.int64)
    else:
        p = max(factor(d))
        e = d // p
        base = cyc_fast(e)
        up = np.zeros((len(base) - 1) * p + 1, dtype=np.int64)
        up[::p] = base
        if e % p == 0:
            r = up
        else:
            num = up.copy()
            den = base
            q = np.zeros(len(num) - len(den) + 1, dtype=np.int64)
            for i in range(len(q) - 1, -1, -1):
                c = num[i + len(den) - 1]
                q[i] = c
                if c:
                    num[i:i + len(den)] -= c * den
            assert not num.any()
            r = q
    _cf[d] = r
    return r


def rows_mod_phi(d, xs):
    """array (len(xs), phi(d)): row j = X^(xs[j]) mod Phi_d, without storing the whole table"""
    phi = cyc_fast(d)
    deg = len(phi) - 1
    low = phi[:-1]
    want = {}
    for j, x in enumerate(xs):
        want.setdefault(int(x) % d, []).append(j)
    out = np.zeros((len(xs), deg), dtype=np.int64)
    r = np.zeros(deg, dtype=np.int64)
    r[0] = 1
    for x in range(max(want) + 1):
        if x in want:
            out[want[x]] = r
        top = r[-1]
        r = np.roll(r, 1)
        r[0] = 0
        if top:
            r = r - top * low
    return out


def main():
    from lib4 import cyclotomic
    for d in divisors(315) + divisors(675):
        assert list(cyc_fast(d)) == cyclotomic(d)
        assert (rows_mod_phi(d, list(range(d))) == powers_mod_phi(d)).all()
    n0 = int(sys.argv[1]); m = int(sys.argv[2]); count = int(sys.argv[3]); seed = int(sys.argv[4]); kind = sys.argv[5]
    rng = random.Random(seed)
    k = m - 1
    CH = 1 << 11
    least = Fr(1)
    for it in range(count):
        if kind == 'full':
            B = gen_full(n0, m, rng)
            assert B is not None
        else:
            cols = []
            for p, a in factor(n0).items():
                perm = list(range(m))
                if it > 0:
                    rng.shuffle(perm)
                cols.append(([v % p ** a for v in perm], p ** a))
            B = [crt([(col[j], q) for col, q in cols])[0] for j in range(m)]
        B, n = contract(B, n0)
        assert all_full(B, n)
        ds = divisors(n)
        Barr = np.array(B, dtype=np.int64)
        Ms = {d: rows_mod_phi(d, B) for d in ds if d > 1}
        badcount = {d: 0 for d in ds}
        good = 0
        for start in range(0, 1 << k, CH):
            idx = np.arange(start, min(start + CH, 1 << k), dtype=np.int64)
            E = np.ones((len(idx), m), dtype=np.int64)
            for j in range(k):
                E[:, j + 1] = 1 - 2 * ((idx >> j) & 1)
            bad = (E.sum(axis=1) == 0)
            badcount[1] += int(bad.sum())
            for d in ds:
                if d == 1:
                    continue
                b = ~(E @ Ms[d]).any(axis=1)
                badcount[d] += int(b.sum())
                bad |= b
            good += int((~bad).sum())
        tot = 1 << k
        viol = [d for d in ds if d > 1 and badcount[d] * 2 ** mu(d) > tot]
        plain = c_even(m) + sum(Fr(1, 2 ** mu(d)) for d in ds if d > 1)
        g = Fr(good, tot)
        least = min(least, g)
        print(f"n={n0} kind={kind} m={m} set {it}: n_flat={n}; fraction of good signings {g} = {float(g):.4f}; bad at 1: {float(Fr(badcount[1], tot)):.4f}; "
              f"bad at 3: {float(Fr(badcount.get(3, 0), tot)):.4f}; level bound violated at {viol}; "
              f"c_m + sum over d | n of 2^-mu(d) = {float(plain):.4f}", flush=True)
    print(f"n={n0} kind={kind} m={m}: least fraction of good signings over {count} multisets: {float(least):.4f}")


main()
