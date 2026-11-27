"""Part T (card_exists_levelBad_le), by all signings, from the definitions csum and levelBad as Lean has them.

A valued family: positions pos_k (natural numbers, not reduced), values val_k in a group V, any values (0 allowed).
  csum(M, r)   = sum over the k with pos_k % M == r of sg_k * val_k
  level 0 bad  : sum over all k of sg_k * val_k == 0
  level j+1 bad: for every r < 2^j: csum(2^(j+1), r) == csum(2^(j+1), r + 2^j)
Statement: for every K, #{signings with some level j <= K bad} <= 2 * #{signings with level 0 bad}.
Groups: Z (N = 0), Z/N (N = 2, 3, 4, 6), Z^2 ("Z2": pairs of integers).
K runs from 0 to k0 + 2, where 2^k0 exceeds every position: from level k0 + 1 on, the levels say the same thing
(the class r + 2^j is empty for j >= k0), so this covers every K.

usage: t1_twice.py exh GROUP KPOS MMAX      every multiset of at most MMAX pairs (position < 2^KPOS, value in the set)
       t1_twice.py rand GROUP COUNT SEED    random families, up to 11 elements, positions up to 40
       t1_twice.py slow                     the fast code against a slow word-for-word transcription
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random
import time
from itertools import combinations_with_replacement
from fractions import Fraction
import numpy as np
from ecore import signs

VALS = {
    'Z': (0, 1, [(-2,), (-1,), (0,), (1,), (2,)]),
    'Z2g': (2, 1, [(0,), (1,)]),
    'Z3g': (3, 1, [(0,), (1,), (2,)]),
    'Z4g': (4, 1, [(0,), (1,), (2,), (3,)]),
    'Z6g': (6, 1, [(0,), (1,), (2,), (3,), (4,), (5,)]),
    'ZxZ': (0, 2, [(0, 0), (1, 0), (0, 1), (1, 1), (1, -1), (2, 1)]),
}


def levels_bad(pos, val, N, K):
    """list over j = 0..K of boolean vectors over the signings: level j is bad"""
    m = len(pos)
    sg = signs(m)
    v = np.array(val, dtype=np.int64).reshape(m, -1) if m else np.zeros((0, 1), dtype=np.int64)
    dim = v.shape[1]
    out = []
    s0 = sg @ v
    if N:
        s0 = s0 % N
    out.append(~np.any(s0 != 0, axis=1))
    for j in range(K):
        half = 1 << j
        W = np.zeros((m, half, dim), dtype=np.int64)
        for k in range(m):
            c = pos[k] % (2 * half)
            if c < half:
                W[k, c, :] = v[k]           # contributes to csum(2^(j+1), r), r = c
            else:
                W[k, c - half, :] = -v[k]   # contributes to csum(2^(j+1), r + 2^j), r = c - 2^j
        D = sg @ W.reshape(m, half * dim)
        if N:
            D = D % N
        out.append(~np.any(D != 0, axis=1))
    return out


def slow_level_bad(pos, val, eps, j, N):
    """word for word: eps a tuple of +1/-1"""
    dim = len(val[0]) if val else 1

    def red(x):
        return tuple((c % N) if N else c for c in x)

    def csum(M, r):
        s = [0] * dim
        for k in range(len(pos)):
            if pos[k] % M == r:
                for c in range(dim):
                    s[c] += eps[k] * val[k][c]
        return red(s)

    if j == 0:
        s = [0] * dim
        for k in range(len(pos)):
            for c in range(dim):
                s[c] += eps[k] * val[k][c]
        return red(s) == red([0] * dim)
    jj = j - 1
    return all(csum(2 ** (jj + 1), r) == csum(2 ** (jj + 1), r + 2 ** jj) for r in range(2 ** jj))


def k0_of(pos):
    k0 = 0
    while (1 << k0) <= max(pos, default=0):
        k0 += 1
    return k0


class Stats:
    def __init__(self):
        self.fam = 0
        self.checks = 0
        self.viol = 0
        self.eq = 0          # families with Q_K = 2 z > 0 for some K
        self.maxratio = Fraction(0)
        self.example = None
        self.zpos = 0        # families with z > 0
        self.beyond = 0      # families where a level beyond k0 is bad for some signing
        self.first_viol = None

    def add(self, pos, val, N):
        m = len(pos)
        k0 = k0_of(pos)
        K = k0 + 2
        lv = levels_bad(pos, val, N, K)
        z = int(lv[0].sum())
        acc = np.zeros(1 << m, dtype=bool)
        self.fam += 1
        if z:
            self.zpos += 1
        if lv[K].any():
            self.beyond += 1
        hit = False
        for j in range(K + 1):
            acc |= lv[j]
            q = int(acc.sum())
            self.checks += 1
            if q > 2 * z:
                self.viol += 1
                if self.first_viol is None:
                    self.first_viol = (pos, val, N, j, q, z)
            if z and q == 2 * z:
                hit = True
            if z:
                r = Fraction(q, z)
                if r > self.maxratio:
                    self.maxratio = r
                    self.example = (pos, val, j, q, z)
        if hit:
            self.eq += 1

    def report(self, label):
        print(f"{label}: families {self.fam}, inequalities checked {self.checks}, violations {self.viol}, "
              f"families with level 0 bad for some signing {self.zpos}, with equality (factor 2 attained) {self.eq}, "
              f"with a level beyond the largest position bad {self.beyond}, largest ratio {self.maxratio} "
              f"at {self.example}")
        if self.first_viol:
            print("  FIRST VIOLATION:", self.first_viol)
        sys.stdout.flush()


def main():
    mode = sys.argv[1]
    t0 = time.time()
    if mode == 'slow':
        random.seed(11)
        n = 0
        for trial in range(1500):
            g = random.choice(list(VALS))
            N, dim, vs = VALS[g]
            m = random.randint(0, 6)
            pos = [random.randrange(0, random.choice([2, 4, 8, 11])) for _ in range(m)]
            val = [random.choice(vs) for _ in range(m)]
            K = k0_of(pos) + 2
            lv = levels_bad(pos, val, N, K)
            for s in range(1 << m):
                eps = tuple(1 if (s >> k) & 1 else -1 for k in range(m))
                for j in range(K + 1):
                    assert slow_level_bad(pos, val, eps, j, N) == bool(lv[j][s]), (pos, val, g, s, j)
                    n += 1
        print(f"slow: the fast levels equal the word-for-word transcription on {n} (family, signing, level) triples")
        # the empty family and K = 0
        lv = levels_bad([], [], 0, 3)
        print("empty family: signings", len(lv[0]), "level 0..3 bad:", [bool(x[0]) for x in lv],
              "-> left side 1, right side 2 for every K")
        return
    g = sys.argv[2]
    N, dim, vs = VALS[g]
    st = Stats()
    if mode == 'exh':
        kpos = int(sys.argv[3])
        mmax = int(sys.argv[4])
        kinds = [(p, v) for p in range(1 << kpos) for v in vs]
        for m in range(0, mmax + 1):
            for fam in combinations_with_replacement(kinds, m):
                st.add([f[0] for f in fam], [f[1] for f in fam], N)
            if time.time() - t0 > 270:
                print(f"  (stopped by the clock inside m = {m + 1}; complete up to m = {m})")
                break
        st.report(f"exh {g} positions < {1 << kpos}, values {vs}, up to {mmax} elements ({time.time() - t0:.0f} s)")
    else:
        count = int(sys.argv[3])
        random.seed(int(sys.argv[4]))
        for trial in range(count):
            m = random.randint(1, 11)
            style = random.random()
            top = random.choice([2, 4, 8, 16, 32, 40])
            if style < 0.4:
                pos = [random.randrange(0, top) for _ in range(m)]
            elif style < 0.7:
                base = [random.randrange(0, top) for _ in range(3)]
                pos = [random.choice(base) for _ in range(m)]
            else:
                base = random.randrange(0, top)
                pos = [(base + random.choice([0, 1, 2, 4, 8, 16])) for _ in range(m)]
            if random.random() < 0.5:
                v0 = random.choice(vs)
                val = [random.choice([v0, tuple(-c for c in v0), v0, (0,) * dim]) for _ in range(m)]
            else:
                val = [random.choice(vs) for _ in range(m)]
            st.add(pos, val, N)
            if time.time() - t0 > 270:
                print("  (stopped by the clock)")
                break
        st.report(f"rand {g} seed {sys.argv[4]} ({time.time() - t0:.0f} s)")


main()
