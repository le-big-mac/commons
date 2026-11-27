# exists_lift_two, by brute force, read literally.  For N and every multiset w of size 1..S on Z_N that contains 0, search for a
# multiset w' on Z_{2N} with reduce w' = w (each element x of w, representative in [0, N), goes to x or to x + N: these are the two
# elements of Z_{2N} whose residue modulo N is x; Lean's `reduce` counts, for each x, the elements y with y.val % N = x.val) such
# that no Phi_d with d | 2N, d not dividing N, divides the mask of w' (exponents = representatives in [0, 2N)).
# Lifts are tried in the order of the bit mask m (bit i = 1: element i + 1 goes to x + N); mask 0 is "everything low".
# At the lift found, the divisors d | N of w' are compared with those of w computed in Z_N (cyclotomic_dvd_reduce_iff for r = 2).
# Restricting to multisets containing 0 loses nothing: translating w' by t in Z_{2N} translates its reduction by t mod N and
# changes no divisibility by Phi_d, d | 2N (t0_selftest.py).
# usage: t2_lift2.py small | main [work budget, default 1.5e9] | control
import sys, time, math
import numpy as np
from numba import njit
from core import Grp, code_of, pattern_slow, divisors


@njit(cache=True)
def lift2_kernel(C1, off1, nd1, C2, off2, nd2, N, S, newmask, oldmap, stat, exfail, exhard):
    # stat[t] = [multisets, all-low fails, no lift, max index of first good lift, disagreements on the old divisors]
    M = 2 * N
    vecs = np.zeros((S + 1, M), dtype=np.int64)   # the all-low lift, in the tables of Z_{2N}
    vec1 = np.zeros((S + 1, N), dtype=np.int64)   # w itself, in the tables of Z_N
    el = np.zeros(S + 1, dtype=np.int64)
    nxt = np.zeros(S + 2, dtype=np.int64)
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
        firstgood = -1
        codegood = 0
        c = code_of(vecs[t], off2, nd2)
        if (c & newmask) == 0:
            firstgood = 0
            codegood = c
        else:
            stat[t, 1] += 1
            for m in range(1, 1 << t):
                for j in range(M):
                    v[j] = 0
                for i in range(1, t + 1):
                    y = el[i]
                    if (m >> (i - 1)) & 1:
                        y += N
                    for j in range(M):
                        v[j] += C2[y, j]
                c = code_of(v, off2, nd2)
                if (c & newmask) == 0:
                    firstgood = m
                    codegood = c
                    break
        if firstgood < 0:
            if stat[t, 2] == 0:
                for i in range(t):
                    exfail[t, i] = el[i + 1]
            stat[t, 2] += 1
        else:
            if firstgood > stat[t, 3]:
                stat[t, 3] = firstgood
                for i in range(t):
                    exhard[t, i] = el[i + 1]
            # old divisors: bit i of code1 (divisor i of N) against the bit of the same divisor in the code of the lift
            for i in range(nd1):
                b1 = (code1 >> i) & 1
                b2 = (codegood >> oldmap[i]) & 1
                if b1 != b2:
                    stat[t, 4] += 1
    return 0


def run(N, S):
    G1, G2 = Grp(N), Grp(2 * N)
    new = [d for d in G2.divs if N % d != 0]
    newmask = G2.mask_of(new)
    oldmap = np.array([G2.divs.index(d) for d in G1.divs], dtype=np.int64)
    stat = np.zeros((S + 1, 5), dtype=np.int64)
    exfail = np.zeros((S + 1, S), dtype=np.int64)
    exhard = np.zeros((S + 1, S), dtype=np.int64)
    t0 = time.time()
    lift2_kernel(G1.C, G1.off, G1.nd, G2.C, G2.off, G2.nd, N, S, newmask, oldmap, stat, exfail, exhard)
    for t in range(1, S + 1):
        assert stat[t, 0] == math.comb(N + t - 2, t - 1)
    tot, alf, fail, dis = (int(stat[:, k].sum()) for k in (0, 1, 2, 4))
    print(f"N={N:4d} 2N={2 * N:4d} new divisors={new} S={S:2d} multisets={tot:10d} all-low-fails={alf:9d} without-lift={fail:6d} "
          f"max-index-of-first-good-lift={int(stat[:, 3].max())} old-divisor-disagreements={dis} [{time.time() - t0:.1f}s]", flush=True)
    if fail:
        t = min(t for t in range(1, S + 1) if stat[t, 2])
        e = [int(x) for x in exfail[t, :t]]
        allbad = True
        for m in range(1 << t):
            lifted = [y + N * ((m >> i) & 1) for i, y in enumerate(e)]
            if not (pattern_slow(lifted, 2 * N) & set(new)):
                allbad = False
        print(f"      smallest multiset without a lift: {e}; confirmed by long division over all {1 << t} lifts: {allbad}", flush=True)
    else:
        t = max(range(1, S + 1), key=lambda t: stat[t, 3])
        if stat[t, 3] > 0:
            e = [int(x) for x in exhard[t, :t]]
            m = int(stat[t, 3])
            lifted = [y + N * ((m >> i) & 1) for i, y in enumerate(e)]
            low = sorted(pattern_slow(e, 2 * N) & set(new))
            pl = pattern_slow(lifted, 2 * N)
            ok = not (pl & set(new)) and (pl == pattern_slow(e, N)) and sorted(y % N for y in lifted) == sorted(e)
            print(f"      latest first good lift: w = {e} on Z_{N}; the all-low lift has the new divisors {low}; the lift {lifted} "
                  f"on Z_{2 * N} has none, the same old ones, and reduces to w (long division): {ok}", flush=True)
            assert ok
    return tot, alf, fail, dis


def budget(N, cost, smax=24):
    S = 1
    while S < smax and math.comb(N + S, S) * 3 * N <= cost:
        S += 1
    return S


def oddpart_primes(N):
    while N % 2 == 0:
        N //= 2
    return [p for p in range(3, N + 1) if N % p == 0 and all(p % k for k in range(2, p))]


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'small':
        for N in [1, 2, 3, 4, 6, 9, 10, 12, 15]:
            run(N, 5)
    elif mode == 'main':
        Ns = [N for N in range(1, 101) if len(oddpart_primes(N)) <= 2]
        Ns += [108, 112, 120, 125, 135, 144, 147, 150, 162, 175, 180, 225]
        T = A = F = D = 0
        for N in Ns:
            assert len(oddpart_primes(N)) <= 2
            tot, alf, fail, dis = run(N, budget(N, int(float(sys.argv[2])) if len(sys.argv) > 2 else 1_500_000_000))
            T += tot; A += alf; F += fail; D += dis
        print(f"TOTAL over {len(Ns)} values of N = 2^k p^a q^b: multisets examined {T}, all-low fails {A}, without a lift {F}, "
              f"old-divisor disagreements {D}")
    elif mode == 'control':
        print("N whose odd part has three prime factors (outside the Lean statement; the paper proves the case p r q^b on paper)")
        for N in [105, 165, 195, 210, 231, 315, 330, 420]:
            run(N, budget(N, 3_000_000_000, 8))
