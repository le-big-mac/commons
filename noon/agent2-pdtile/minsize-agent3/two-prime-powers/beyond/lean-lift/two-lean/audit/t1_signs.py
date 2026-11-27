# exists_signs, by brute force.  For a modulus n and every multiset of size 1..S on Z_n that contains 0 (every multiset has a
# translate that contains 0; translation multiplies the signed mask by a power of X modulo X^n - 1, which changes no
# divisibility by Phi_d, d | n -- checked in t0_selftest.py), search the signings for one whose signed mask
#       S(X) = sum of (+-) X^x     (x the representative in [0, n); Lean: maskW u - maskW v, u = the elements signed +, v = those signed -)
# is divisible by no Phi_d, d | n, d = 1 included.  The first element is signed + (S and -S have the same divisors), the
# other t - 1 signs run through all 2^(t-1) choices (bit i of the mask = 1: element i + 2 is signed -).
#   quick mode: stop at the first good signing;   full mode: count the good signings of every multiset.
# usage: t1_signs.py small | main [work budget of the quick mode, default 3e9] | control
import sys, time, math
import numpy as np
from numba import njit
from core import Grp, code_of, pattern_slow, divisors


@njit(cache=True)
def signs_kernel(C, off, nd, n, S, full, stat, exfail, exhard, exfew):
    # stat[t] = [multisets, all-plus fails, no good signing, max index of first good signing, min number of good signings (full)]
    vecs = np.zeros((S + 1, n), dtype=np.int64)
    el = np.zeros(S + 1, dtype=np.int64)
    nxt = np.zeros(S + 2, dtype=np.int64)
    v = np.zeros(n, dtype=np.int64)
    for t in range(S + 1):
        stat[t, 4] = -1
    t = 0
    nxt[0] = 0
    first = True
    while t >= 0:
        descend = False
        if t == 0:
            if first:
                first = False
                t = 1
                el[1] = 0
                for j in range(n):
                    vecs[1, j] = C[0, j]
                nxt[1] = 0
                descend = True
            else:
                break
        elif t < S and nxt[t] < n:
            y = nxt[t]
            nxt[t] += 1
            t += 1
            el[t] = y
            for j in range(n):
                vecs[t, j] = vecs[t - 1, j] + C[y, j]
            nxt[t] = y
            descend = True
        else:
            t -= 1
        if not descend:
            continue
        # the multiset el[1..t]
        stat[t, 0] += 1
        firstgood = -1
        ngood = 0
        if code_of(vecs[t], off, nd) == 0:
            firstgood = 0
            ngood = 1
        else:
            stat[t, 1] += 1
        if firstgood < 0 or full:
            for m in range(1, 1 << (t - 1)):
                for j in range(n):
                    v[j] = C[el[1], j]
                for i in range(2, t + 1):
                    if (m >> (i - 2)) & 1:
                        for j in range(n):
                            v[j] -= C[el[i], j]
                    else:
                        for j in range(n):
                            v[j] += C[el[i], j]
                if code_of(v, off, nd) == 0:
                    ngood += 1
                    if firstgood < 0:
                        firstgood = m
                        if not full:
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
            if full and (stat[t, 4] < 0 or ngood < stat[t, 4]):
                stat[t, 4] = ngood
                for i in range(t):
                    exfew[t, i] = el[i + 1]
    return 0


def run(n, S, full):
    G = Grp(n)
    stat = np.zeros((S + 1, 5), dtype=np.int64)
    exfail = np.zeros((S + 1, S), dtype=np.int64)
    exhard = np.zeros((S + 1, S), dtype=np.int64)
    exfew = np.zeros((S + 1, S), dtype=np.int64)
    t0 = time.time()
    signs_kernel(G.C, G.off, G.nd, n, S, full, stat, exfail, exhard, exfew)
    for t in range(1, S + 1):
        assert stat[t, 0] == math.comb(n + t - 2, t - 1)
    tot = int(stat[:, 0].sum())
    apf = int(stat[:, 1].sum())
    fail = int(stat[:, 2].sum())
    line = f"n={n:4d} S={S:2d} {'full ' if full else 'quick'} multisets={tot:10d} all-plus-fails={apf:9d} without-good-signing={fail:7d}"
    line += f" max-index-of-first-good={int(stat[:, 3].max())}"
    if full:
        fr = []
        for t in range(1, S + 1):
            fr.append(f"{int(stat[t, 4])}/{1 << (t - 1)}")
        line += " fewest-good-signings-by-size=" + ",".join(fr)
    line += f" [{time.time() - t0:.1f}s]"
    print(line, flush=True)
    # examples, re-checked by long division
    if fail:
        t = min(t for t in range(1, S + 1) if stat[t, 2])
        e = [int(x) for x in exfail[t, :t]]
        # confirm literally: every one of the 2^t signings has some Phi_d, d | n, dividing the signed mask
        allbad = True
        for m in range(1 << t):
            sg = [-1 if (m >> i) & 1 else 1 for i in range(t)]
            if not pattern_slow(e, n, sg):
                allbad = False
        print(f"      smallest multiset without a good signing: {e}; confirmed by long division over all {1 << t} signings: {allbad}",
              flush=True)
    else:
        t = max(range(1, S + 1), key=lambda t: stat[t, 3])
        if stat[t, 3] > 0:
            e = [int(x) for x in exhard[t, :t]]
            m = int(stat[t, 3])
            sg = [1] + [-1 if (m >> (i - 2)) & 1 else 1 for i in range(2, t + 1)]
            ok = not pattern_slow(e, n, sg)
            plus = sorted(pattern_slow(e, n))
            print(f"      latest first good signing: multiset {e}, signs {sg}; all-plus mask is divisible by Phi_d for d in {plus}; "
                  f"the signed mask has no divisor (long division): {ok}", flush=True)
            assert ok
    return tot, apf, fail


def budget_full(n, cost, smax=16):
    """largest S <= smax with  sum_t  C(n+t-2, t-1) * 2^(t-1) * t * n  <= cost  (the work of the full mode)"""
    S, tot = 0, 0
    while S < smax:
        t = S + 1
        tot += math.comb(n + t - 2, t - 1) * (1 << (t - 1)) * t * n
        if tot > cost:
            break
        S = t
    return max(S, 1)


def budget_quick(n, cost, smax=24):
    """largest S <= smax with  C(n+S-1, S-1) * n <= cost  (the work of the quick mode when the first signing is good)"""
    S = 1
    while S < smax and math.comb(n + S, S) * n <= cost:
        S += 1
    return S


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'small':
        for n in [1, 3, 5, 9, 15]:
            run(n, 5, True)
        for n in [2, 4, 6]:
            run(n, 4, True)
    elif mode == 'main':
        T = A = F = 0
        ns = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 33, 35, 39, 45, 49, 51, 55, 63, 65, 75, 77, 81, 99, 117, 121,
              125, 135, 147, 175, 225, 243, 245, 275, 297, 325, 375]
        for n in ns:
            pf = [p for p in range(2, n + 1) if n % p == 0 and all(p % k for k in range(2, p))]
            assert n % 2 == 1 and len(pf) <= 2
            tot, apf, fail = run(n, budget_full(n, 1_000_000_000), True)
            T += tot; A += apf; F += fail
            S2 = budget_quick(n, int(float(sys.argv[2])) if len(sys.argv) > 2 else 3_000_000_000)
            tot, apf, fail = run(n, S2, False)
            T += tot; A += apf; F += fail
        print(f"TOTAL over {len(ns)} moduli of the form p^a q^b (p, q odd): multisets examined {T}, all-plus fails {A}, without a good signing {F}")
    elif mode == 'control':
        print("moduli outside the lemma: even n (the statement is false there), and odd n with three prime factors")
        for n in [2, 4, 6, 8, 10, 12, 14, 18, 20, 30]:
            run(n, budget_quick(n, 20_000_000, 8), False)
        for n in [105, 165, 195, 231, 315]:
            run(n, budget_quick(n, 3_000_000_000, 8), False)
