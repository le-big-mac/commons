"""K_pi(D) against direct counts.
(a) K from the definition by another road: all signings of D, Q(zeta) at every L-th root of unity in floating point,
    the integer values collected (r <= 12), against lib.K (reduction modulo Phi_d).
(b) h copies of 0 beside D: the share by all 2^m signings (m <= 15), against the share by multiplicities, and
    share <= c_h * K_(h mod 2)(D), for h of both parities.  Decorations with 0 and on Z_1 included.
(c) large h: share/(c_h K) and share/c_m against K.
usage: t_K.py SEED SECONDS"""
import sys, math, cmath, random, itertools
from fractions import Fraction
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/limit/referee')
from lib import *

def K_def(L, D):
    r = len(D); tot = [0, 0]
    Z = np.array([[cmath.exp(2j * math.pi * ((b * j) % L) / L) for b in D] for j in range(L)]) if r else np.zeros((L, 0))
    for eps in itertools.product((1, -1), repeat=r):
        if r: q = Z @ np.array(eps, dtype=float)
        else: q = np.zeros(L, dtype=complex)
        vs = set()
        for z in q:
            if abs(z.imag) < 1e-9 and abs(z.real - round(z.real)) < 1e-9: vs.add(-int(round(z.real)))
        for v in vs: tot[v % 2] += 1
    return Fraction(tot[0], 2 ** r), Fraction(tot[1], 2 ** r)

if __name__ == '__main__':
    import time
    rng = random.Random(int(sys.argv[1])); secs = float(sys.argv[2]); t0 = time.time()
    decs = [(1, []), (1, [0]), (1, [0, 0]), (1, [0, 0, 0]), (3, []), (3, [0]), (3, [1, 2]), (3, [0, 1, 2]), (3, [0, 0, 1, 2]), (3, [1, 1, 2, 2]),
            (3, [0, 1, 1, 2, 2]), (3, [1, 1, 1, 2, 2, 2]), (5, [1, 2, 3, 4]), (5, [0, 1, 2, 3, 4]), (9, [1, 2, 3, 6]), (9, [3, 6]), (9, [1, 1, 2, 2, 3, 3, 6, 6]),
            (9, [0, 3, 6, 1, 4, 7]), (15, [3, 5, 6, 9, 10, 12]), (15, [0, 3, 5, 6, 9, 10, 12]), (15, [5, 5, 10, 10, 3, 6, 9, 12]),
            (27, [9, 18, 3, 6, 1, 2]), (45, [15, 30, 9, 18, 27, 36]), (21, [7, 14, 3, 6, 9, 12, 15, 18]), (105, [35, 70, 21, 42, 63, 84])]
    for _ in range(60):
        L = rng.choice((3, 9, 15, 15, 21, 27, 45, 45, 63, 105)); r = rng.randint(1, 9); D = []
        while len(D) < r:
            p = rng.choice([q for q in (3, 5, 7) if L % q == 0]); x0 = rng.choice([0, 0, rng.randrange(L)])
            cos = [(x0 + j * (L // p)) % L for j in range(p)]
            if rng.random() < 0.6: cos = [b for b in cos if b != 0]
            D += cos * rng.choice((1, 1, 2))
            if rng.random() < 0.2: D.append(rng.randrange(L))
        decs.append((L, D[:10]))
    na = nb = nc = 0; fail = 0; worst_b = Fraction(0); rows = []
    done = 0
    for L, D in decs:
        if time.time() - t0 > secs: break
        done += 1
        r = len(D); k = K(L, D)
        if r <= 9:
            kd = K_def(L, D); na += 1
            if kd != k: fail += 1; print("K: definition and reduction DIFFER", L, D, kd, k, flush=True)
        # the value at zeta = 1 has the parity of r and always exists, so K_(r mod 2) >= 1
        if k[r % 2] < 1: fail += 1; print("K_(r mod 2) < 1 ?", L, D, k, flush=True)
        for h in range(1, max(0, 12 - r) + 1):
            s_b = brute_share(L, [0] * h + D); s_m, m = share(L, [(0, h)] + [(b, 1) for b in D]); nb += 1
            if s_b != s_m: fail += 1; print("share: all signings and multiplicities DIFFER", L, D, h, s_b, s_m, flush=True)
            bound = c(h) * k[h % 2]
            if s_b > bound: fail += 1; print("share > c_h K_pi(D) !", L, D, h, s_b, bound, flush=True)
            if bound > 0: worst_b = max(worst_b, s_b / bound)
            elif s_b != 0: fail += 1; print("share > 0 = K", L, D, h, flush=True)
        line = f"Z_{L} D = {D} (r = {r}): K_0 = {k[0]}, K_1 = {k[1]};"
        for h in (300, 301, 3000, 3001):
            s_m, m = share(L, [(0, h)] + [(b, 1) for b in D]); nc += 1
            kk = k[h % 2]
            if s_m > c(h) * kk: fail += 1; print("share > c_h K_pi(D) at large h !", L, D, h, flush=True)
            line += f"  h = {h} (m {'even' if m % 2 == 0 else 'odd'}): share/c_m = {float(s_m / c(m)):.5f} K = {float(kk):.5f}"
            if h >= 3000 and kk > 0 and float(s_m / (c(h) * kk)) < 0.99: fail += 1; print("share/(c_h K) < 0.99 at h >= 3000", L, D, h, float(s_m / (c(h) * kk)), flush=True)
        rows.append(line); print(line, flush=True)
    print(f"{done} decorations done of {len(decs)} prepared")
    print(f"(a) K by the definition (float roots) = K by reduction: {na} decorations;  (b) small h: {nb} comparisons of the two counts, share <= c_h K_pi in each, largest share/(c_h K) {float(worst_b):.6f};  (c) large h: {nc} cases, share <= c_h K_pi(D) and share/(c_h K) >= 0.99 for h >= 3000;  failures: {fail}")
