"""Referee's small-M numerical check of Section 2 (Props 1, 2, 3 and the two 'further consequences').

Independent of the author's code: D+ is a small LP over step functions; 'A pd-tiles Z_M' is tested by a
separate LP over ALL real functions f on Z_M straight from the definition (no step functions, no
averaging); proper tiling is tested by exact-cover backtracking; (T1),(T2) are tested in the
Coven-Meyerowitz sense for the integer set A in {0..M-1}, i.e. with S_A = ALL prime powers s with
Phi_s | A(X), not only those dividing M.
"""
import itertools
import math
import random
import sys

import numpy as np
from scipy.optimize import linprog

from cyclo import divisors, phi, xpow_table, cyclotomic

TOL = 1e-6


class Group:
    def __init__(self, M):
        self.M = M
        self.divs = divisors(M)
        self.ordx = [M // math.gcd(x, M) for x in range(M)]
        n = len(self.divs)
        # R[e][d] = sum over x of order d of cos(2 pi x (M/e) / M)
        R = np.zeros((n, n))
        for ei, e in enumerate(self.divs):
            xi = M // e
            for x in range(M):
                R[ei, self.divs.index(self.ordx[x])] += math.cos(2 * math.pi * x * xi / M)
        assert np.abs(R - np.round(R)).max() < 1e-8
        self.R = np.round(R)
        self.size = np.array([phi(d) for d in self.divs], dtype=float)

    def dplus(self, Z):
        n = len(self.divs)
        bounds = []
        for d in self.divs:
            if d == 1:
                bounds.append((1, 1))
            elif d in Z:
                bounds.append((0, None))
            else:
                bounds.append((0, 0))
        res = linprog(-self.size, A_ub=-self.R, b_ub=np.zeros(n), bounds=bounds, method="highs")
        assert res.status == 0, res.message
        return -res.fun, res.x


_groups = {}


def group(M):
    if M not in _groups:
        _groups[M] = Group(M)
    return _groups[M]


def zero_set(A, M):
    out = []
    for d in divisors(M):
        if d > 1 and not np.any(xpow_table(M, d)[A].sum(axis=0)):
            out.append(d)
    return out


def pd_tiles_direct(A, M):
    """LP straight from the definition: f>=0, f(0)=1, f^ real and >=0, 1_A * f = 1."""
    x = np.arange(M)
    C = np.cos(2 * np.pi * np.outer(x, x) / M)
    S = np.sin(2 * np.pi * np.outer(x, x) / M)
    conv = np.zeros((M, M))
    for z in range(M):
        for a in A:
            conv[z, (z - a) % M] += 1
    e0 = np.zeros((1, M))
    e0[0, 0] = 1
    Aeq = np.vstack([conv, S, e0])
    beq = np.concatenate([np.ones(M), np.zeros(M), [1]])
    res = linprog(np.zeros(M), A_ub=-C, b_ub=np.zeros(M), A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * M, method="highs")
    return res.status == 0


def prime_power(s):
    for p in range(2, s + 1):
        if s % p == 0:
            while s % p == 0:
                s //= p
            return p if s == 1 else None
    return None


def cm_data(A, M):
    """S_A in the Coven-Meyerowitz sense (all prime powers), T1, T2 for the integer set A."""
    S = []
    for s in range(2, 4 * M):
        p = prime_power(s)
        if p is None or phi(s) > max(A):
            continue
        if not np.any(xpow_table(max(A) + 1, s)[A].sum(axis=0)):
            S.append((s, p))
    t1 = math.prod(p for _, p in S) == len(A)
    t2 = True
    byp = {}
    for s, p in S:
        byp.setdefault(p, []).append(s)
    primes = sorted(byp)
    for k in range(2, len(primes) + 1):
        for ps in itertools.combinations(primes, k):
            for combo in itertools.product(*[byp[p] for p in ps]):
                d = math.prod(combo)
                if np.any(xpow_table(max(A) + 1, d)[A].sum(axis=0)):
                    t2 = False
    return [s for s, _ in S], t1, t2


def tiles(A, M):
    if M % len(A):
        return False
    A = sorted(A)
    covered = [False] * M

    def rec(z, left):
        if left == 0:
            return True
        while covered[z]:
            z += 1
        # some translate t + A must cover z
        for a in A:
            t = (z - a) % M
            cells = [(t + b) % M for b in A]
            if any(covered[c] for c in cells):
                continue
            for c in cells:
                covered[c] = True
            if rec(z, left - 1):
                return True
            for c in cells:
                covered[c] = False
        return False

    return rec(0, M // len(A))


def check_set(A, M, stats):
    G = group(M)
    n = len(A)
    Z = zero_set(A, M)
    dp, h = G.dplus(Z)
    # Prop 1(i)
    if dp > n + TOL:
        stats["viol_1i"] += 1
        print("VIOLATION Prop 1(i):", M, A, dp)
    # Prop 1(iii)
    k = math.prod(prime_power(d) for d in Z if prime_power(d))
    if n % k:
        stats["viol_1iii"] += 1
        print("VIOLATION Prop 1(iii):", M, A, k)
    crit = abs(dp - n) < TOL
    direct = pd_tiles_direct(A, M)
    stats["sets"] += 1
    if crit != direct:
        stats["viol_1ii"] += 1
        print("VIOLATION Prop 1(ii):", M, A, dp, direct)
    if not direct:
        return
    stats["pd"] += 1
    # conclusion of Prop 2 on this set: T1, T2 (CM sense), tiles; and S_A has only divisors of M
    S, t1, t2 = cm_data(A, M)
    tl = tiles(A, M)
    if not (t1 and t2 and tl and all(M % s == 0 for s in S)):
        stats["pd_not_T1T2tile"] += 1
        print("pd-tiling set failing T1/T2/tiling/S_A | M:", M, A, S, t1, t2, tl)
    # Prop 3 with Z0 = Z_A and the optimal h returned by the LP
    hhat = G.R @ h  # value on elements of order e
    f = np.array([hhat[G.divs.index(G.ordx[x])] for x in range(M)]) / n
    for a in A:
        for b in A:
            if a != b and abs(f[(a - b) % M]) > TOL:
                stats["viol_3"] += 1
                print("VIOLATION Prop 3:", M, A, a, b, f[(a - b) % M])
    for z in range(M):
        if abs(sum(f[(z - a) % M] for a in A) - 1) > TOL:
            stats["viol_cover"] += 1
            print("VIOLATION covering:", M, A, z)
    forb = {e for ei, e in enumerate(G.divs) if e > 1 and hhat[ei] > TOL}
    if forb:
        stats["pd_with_forbidden"] += 1
    for D in divisors(M):
        if D == M:
            continue
        Gs = group(M // D)
        allowed = [e for e in Gs.divs if e > 1 and e not in forb]
        cap, _ = Gs.dplus(allowed)
        biggest = max(sum(1 for a in A if a % D == c) for c in range(D))
        stats["caps"] += 1
        if cap < Gs.M - TOL:
            stats["caps_nontrivial"] += 1
        if biggest > math.floor(cap + TOL):
            stats["viol_cap"] += 1
            print("VIOLATION cap:", M, A, D, biggest, cap)


def main():
    rng = random.Random(5)
    keys = ["sets", "pd", "viol_1i", "viol_1ii", "viol_1iii", "pd_not_T1T2tile", "viol_3", "viol_cover",
            "pd_with_forbidden", "caps", "caps_nontrivial", "viol_cap"]
    for M, mode in ((8, "all"), (9, "all"), (10, "all"), (12, "all"), (16, "sample"), (18, "sample"),
                    (20, "sample"), (24, "sample"), (30, "sample"), (36, "sample")):
        stats = dict.fromkeys(keys, 0)
        if mode == "all":
            sets = [[0] + [x for x in range(1, M) if mask >> (x - 1) & 1] for mask in range(1 << (M - 1))]
        else:
            sets = []
            # random sets
            for _ in range(250):
                k = rng.randint(1, M - 1)
                sets.append(sorted([0] + rng.sample(range(1, M), k - 1)) if k > 1 else [0])
            # sets likely to pd-tile: random tiles built as (complete residues mod m, lifted) and
            # subgroup-plus-shifts constructions, and one-element perturbations of them
            for _ in range(250):
                m = rng.choice([d for d in divisors(M) if 1 < d < M])
                A = sorted(set([0] + [r + m * rng.randrange(M // m) for r in range(1, m)]))
                sets.append(A)
                B = set(A)
                B.discard(rng.choice(A[1:]))
                B.add(rng.randrange(1, M))
                sets.append(sorted(B | {0}))
            for _ in range(100):
                m = rng.choice([d for d in divisors(M) if 1 < d < M])
                m2 = rng.choice([d for d in divisors(M // m)])
                A = sorted({(a * (M // m) + b) % M for a in range(m) for b in range(m2)})
                sets.append(A)
        for A in sets:
            check_set(A, M, stats)
        print(f"M={M} ({mode}): " + ", ".join(f"{k}={stats[k]}" for k in keys), flush=True)


if __name__ == "__main__":
    main()
