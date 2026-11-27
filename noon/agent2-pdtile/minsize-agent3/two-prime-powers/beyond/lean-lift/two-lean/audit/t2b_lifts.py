# The fact behind sizes_eq_two / sizes_eq_odd / sizes_eq_mul, for a general factor s (prime or not), by brute force:
# every nonempty multiset w on Z_N has a multiset w' on Z_{N s} of the same size whose residues modulo N give w and whose mask is
# divisible by no Phi_d with d | N s, d not dividing N.  (Then the divisors d | N of w' are those of w: also checked here.)
# For every multiset of size 1..S on Z_N containing 0: the lifts x_i + N * j_i, j_i in [0, s), are tried in odometer order
# (all j = 0 first, the last element's digit moving fastest) until one has no new divisor; at most CAP lifts are tried.
# usage: t2b_lifts.py small | main
import sys, time, math
import numpy as np
from numba import njit
from core import Grp, code_of, pattern_slow

CAP = 200000


@njit(cache=True)
def lifts_kernel(C1, off1, nd1, C2, off2, nd2, N, s, S, newmask, oldmap, cap, stat, exfail, exhard):
    # stat[t] = [multisets, all-low fails, no lift within cap, max number of lifts tried, old-divisor disagreements]
    M = N * s
    vecs = np.zeros((S + 1, M), dtype=np.int64)
    vec1 = np.zeros((S + 1, N), dtype=np.int64)
    el = np.zeros(S + 1, dtype=np.int64)
    nxt = np.zeros(S + 2, dtype=np.int64)
    dig = np.zeros(S + 1, dtype=np.int64)
    v = np.zeros(M, dtype=np.int64)
    t = 1
    el[1] = 0
    for j in range(M):
        vecs[1, j] = C2[0, j]
    for j in range(N):
        vec1[1, j] = C1[0, j]
    nxt[1] = 0
    fresh = True
    while t >= 1:
        if not fresh:
            if t < S and nxt[t] < N:
                y = nxt[t]
                nxt[t] += 1
                t += 1
                el[t] = y
                for j in range(M):
                    vecs[t, j] = vecs[t - 1, j] + C2[y, j]
                for j in range(N):
                    vec1[t, j] = vec1[t - 1, j] + C1[y, j]
                nxt[t] = y
                fresh = True
            else:
                t -= 1
            continue
        fresh = False
        stat[t, 0] += 1
        code1 = code_of(vec1[t], off1, nd1)
        found = False
        tried = 1
        c = code_of(vecs[t], off2, nd2)
        if (c & newmask) == 0:
            found = True
        else:
            stat[t, 1] += 1
            for i in range(1, t + 1):
                dig[i] = 0
            while tried < cap:
                # next odometer state
                i = t
                while i >= 1:
                    dig[i] += 1
                    if dig[i] < s:
                        break
                    dig[i] = 0
                    i -= 1
                if i < 1:
                    break            # all s^t lifts tried
                tried += 1
                for j in range(M):
                    v[j] = 0
                for i2 in range(1, t + 1):
                    y = el[i2] + N * dig[i2]
                    for j in range(M):
                        v[j] += C2[y, j]
                c = code_of(v, off2, nd2)
                if (c & newmask) == 0:
                    found = True
                    break
        if not found:
            if stat[t, 2] == 0:
                for i in range(t):
                    exfail[t, i] = el[i + 1]
            stat[t, 2] += 1
        else:
            if tried > stat[t, 3]:
                stat[t, 3] = tried
                for i in range(t):
                    exhard[t, i] = el[i + 1]
            for i in range(nd1):
                if ((code1 >> i) & 1) != ((c >> oldmap[i]) & 1):
                    stat[t, 4] += 1
    return 0


def run(N, s, S):
    G1, G2 = Grp(N), Grp(N * s)
    new = [d for d in G2.divs if N % d != 0]
    newmask = G2.mask_of(new)
    oldmap = np.array([G2.divs.index(d) for d in G1.divs], dtype=np.int64)
    stat = np.zeros((S + 1, 5), dtype=np.int64)
    exfail = np.zeros((S + 1, S), dtype=np.int64)
    exhard = np.zeros((S + 1, S), dtype=np.int64)
    t0 = time.time()
    lifts_kernel(G1.C, G1.off, G1.nd, G2.C, G2.off, G2.nd, N, s, S, newmask, oldmap, CAP, stat, exfail, exhard)
    for t in range(1, S + 1):
        assert stat[t, 0] == math.comb(N + t - 2, t - 1)
    tot, alf, fail, dis = (int(stat[:, k].sum()) for k in (0, 1, 2, 4))
    print(f"N={N:3d} s={s:2d} M={N * s:4d} new divisors: {len(new):2d}  S={S:2d} multisets={tot:10d} all-low-fails={alf:9d} "
          f"without-lift={fail:5d} most-lifts-tried={int(stat[:, 3].max())} old-divisor-disagreements={dis} [{time.time() - t0:.1f}s]",
          flush=True)
    if fail:
        t = min(t for t in range(1, S + 1) if stat[t, 2])
        print(f"      smallest multiset without a lift among the first {CAP}: {[int(x) for x in exfail[t, :t]]}", flush=True)
    return tot, alf, fail, dis


def budget(N, s, cost, smax=20):
    S = 1
    while S < smax and math.comb(N + S, S) * (N * s + N) <= cost:
        S += 1
    return S


def is_pnq(N):
    pr = [p for p in range(2, N + 1) if N % p == 0 and all(p % k for k in range(2, p))]
    if len(pr) == 1:
        return N == pr[0]
    if len(pr) == 2:
        return any(N % (p * p) != 0 for p in pr)
    return False


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'small':
        for N, s in [(1, 4), (2, 4), (3, 4), (6, 4), (6, 6), (5, 9), (12, 6)]:
            run(N, s, 5)
    else:
        T = A = F = D = 0
        n = 0
        # N = p^n q (sizes_eq_mul) with every s in the list; then any N with odd composite s (sizes_eq_odd)
        cases = [(N, s) for N in [2, 3, 5, 7, 6, 10, 14, 15, 21, 12, 18, 20, 45, 50, 24, 40, 54] for s in [4, 6, 8, 9, 10, 12, 15, 16]
                 if N * s <= 400]
        cases += [(N, s) for N in [1, 4, 8, 9, 16, 25, 27, 30, 36, 60] for s in [9, 15, 21, 25] if N * s <= 400]
        for N, s in cases:
            assert is_pnq(N) or s % 2 == 1
            tot, alf, fail, dis = run(N, s, budget(N, s, 1_000_000_000))
            T += tot; A += alf; F += fail; D += dis; n += 1
        print(f"TOTAL over {n} pairs (N, s): multisets examined {T}, all-low fails {A}, without a lift {F}, old-divisor disagreements {D}")
