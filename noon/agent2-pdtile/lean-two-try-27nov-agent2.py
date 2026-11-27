"""A trial, by exhaustion on small groups, of two statements Yonder fixed for Lean on 26 November 2026 (Sign.lean, Lift2.lean).
Noon (agent2), 27 November 2026.  Exact: X^x is reduced modulo each cyclotomic polynomial in whole numbers.

  signs(n, M):  every nonempty multiset w on Z_n with at most M elements can be split w = u + v so that no Phi_d, d | n (d = 1
                included), divides mask(u) - mask(v).              [exists_signs: n = p^a q^b, p and q odd primes]
  lift2(N, M):  every nonempty multiset w on Z_N with at most M elements has a w' on Z_2N that reduces to w (each element x
                goes to x or to x + N) with no Phi_d, d | 2N, d not dividing N, dividing mask(w').   [exists_lift_two]
Controls that must find failures: signs on n = 2 and n = 6 (the lemma is for odd n); lift2 asked for too much (no Phi_d at all).
usage: python -I try.py > try.out"""
import sys, itertools
from math import gcd

def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): out[i + j] += x * y
    return out
def polydiv_exact(a, b):                       # a / b for monic b, remainder asserted nought
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(q) - 1, -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, y in enumerate(b): a[i + j] -= q[i] * y
    assert not any(a), 'not exact'; return q
CYC = {}
def cyclotomic(d):                              # Phi_d = (X^d - 1) / product of Phi_e, e | d, e < d; coefficients from the constant up
    if d not in CYC:
        p = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0: p = polydiv_exact(p, cyclotomic(e))
        CYC[d] = p
    return CYC[d]
def residues(n, d):                             # X^x modulo Phi_d for x = 0 .. n-1, as tuples of whole numbers
    phi = cyclotomic(d); deg = len(phi) - 1; out = []; cur = [1] + [0] * (deg - 1) if deg > 1 else [1]
    cur = cur[:deg]
    for x in range(n):
        out.append(tuple(cur)); nxt = [0] + cur; top = nxt[deg]; nxt = nxt[:deg]
        if top:
            for j in range(deg): nxt[j] -= top * phi[j]
        cur = nxt
    return out
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def signs(n, M):
    ds = divisors(n); R = {d: residues(n, d) for d in ds}; tried = 0; bad = []
    for m in range(1, M + 1):
        for w in itertools.combinations_with_replacement(range(n), m):
            tried += 1; ok = False
            for eps in itertools.product((1, -1), repeat=m - 1):          # the first sign is +: a signing and its negative fail together
                e = (1,) + eps; good = True
                for d in ds:
                    r = R[d]; k = len(r[0])
                    if not any(sum(e[i] * r[w[i]][j] for i in range(m)) for j in range(k)): good = False; break
                if good: ok = True; break
            if not ok: bad.append(w)
    return tried, bad

def lift2(N, M, too_much=False):
    N2 = 2 * N; ds = [d for d in divisors(N2) if too_much or N % d]; R = {d: residues(N2, d) for d in ds}; tried = 0; bad = []
    for m in range(1, M + 1):
        for w in itertools.combinations_with_replacement(range(N), m):
            tried += 1; ok = False
            for up in itertools.product((0, 1), repeat=m):
                good = True
                for d in ds:
                    r = R[d]; k = len(r[0])
                    if not any(sum(r[w[i] + N * up[i]][j] for i in range(m)) for j in range(k)): good = False; break
                if good: ok = True; break
            if not ok: bad.append(w)
    return tried, bad

if __name__ == '__main__':
    assert cyclotomic(1) == [-1, 1] and cyclotomic(2) == [1, 1] and cyclotomic(6) == [1, -1, 1] and cyclotomic(15) == [1, -1, 0, 1, -1, 1, 0, -1, 1] and sum(len(cyclotomic(d)) - 1 for d in divisors(45)) == 45
    r = residues(6, 3); assert r[0] == (1, 0) and r[1] == (0, 1) and r[2] == (-1, -1) and r[3] == (1, 0)          # X^2 = -1 - X and X^3 = 1 modulo X^2 + X + 1
    print('SIGNS (exists_signs): nonempty multisets on Z_n with at most M elements; those with no good signing')
    total = 0
    for n, M in [(1, 6), (3, 6), (5, 6), (9, 6), (15, 6), (21, 5), (25, 5), (27, 5), (35, 4), (45, 4), (63, 4), (75, 3), (105, 3)]:
        tried, bad = signs(n, M); total += tried
        print('  n = %3d%s  M = %d: %8d multisets, %d without a good signing%s' % (n, '' if n != 105 else ' (three odd primes: outside the statement)', M, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
    print('  together %d multisets' % total)
    print('  controls, which must fail (even n, outside the statement):')
    for n, M in [(2, 3), (6, 3), (4, 3)]:
        tried, bad = signs(n, M); print('  n = %3d  M = %d: %8d multisets, %d without a good signing%s' % (n, M, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
    print('LIFT ALONG 2 (exists_lift_two): nonempty multisets on Z_N with at most M elements; those with no lift to Z_2N free of new cyclotomic divisors')
    total = 0
    for N, M in [(1, 6), (2, 6), (3, 6), (4, 6), (5, 5), (6, 5), (8, 5), (9, 5), (10, 5), (12, 5), (15, 4), (18, 4), (20, 4), (24, 4), (30, 4), (36, 3), (45, 3), (60, 3)]:
        tried, bad = lift2(N, M); total += tried
        print('  N = %3d  M = %d: %8d multisets, %d without such a lift%s' % (N, M, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
    print('  together %d multisets' % total)
    print('  control, which must fail (asked that no cyclotomic polynomial at all divide the lift; a multiset that is all of Z_3 cannot have that):')
    for N, M in [(3, 3), (6, 3)]:
        tried, bad = lift2(N, M, too_much=True); print('  N = %3d  M = %d: %8d multisets, %d without such a lift%s' % (N, M, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
