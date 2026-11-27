"""The second proof of Corollary N (the referee's, from S0 for p = 2, no valuations): test of its statements, all signings,
exact, for every odd e | n'.  Coordinates: Z[eta_e] = Z[X]/(Phi_e), integer vectors in the basis 1, X, ..., so that
"in 2 Z[eta]" is "all coordinates even".
  U_j(r) = sum of eta^{w_x} over the elements with u_x = r modulo 2^j (unsigned),  beta_0 = U_0(0);
  J = the largest j in 1..k such that every class modulo 2^(j-1) has U in 2 Z[eta]  (J = 0 if beta_0 is not in 2 Z[eta]);
  gamma_0 = beta_0 / 2 mod 2,  gamma_j = gamma_0 + sum_{r < 2^(j-1)} U_j(r) mod 2.
Claims tested: a signing bad at 2^j e has j <= J (and beta_0 in 2 Z[eta] if j = 0) and lambda_e(N) = gamma_j;
gamma_j = gamma_0 for 1 <= j < J.   And, for e = 1, the fact used when part (2) of Proposition P is read with this
proof: if gamma_J != gamma_0 then some class modulo 2^J has an odd number of elements."""
import sys, itertools, random
import numpy as np
from lib import *
from test_D import gen

def check(n, els, st):
    k, n1 = two_part(n); m = len(els)
    signs = all_signs(m, fix_first=False); idx = [x % n for x in els]
    neg = (signs == -1).astype(np.int64)
    for e in divisors(n1):
        Te = table(e, n)
        def U(j, r):
            v = np.zeros(Te.shape[1], dtype=np.int64)
            for x in idx:
                if x % 2 ** j == r: v += Te[x]
            return v
        beta0 = U(0, 0)
        dangerous = not np.any(beta0 % 2)
        J = 0
        if dangerous:
            for j in range(1, k + 1):
                if all(not np.any(U(j - 1, r) % 2) for r in range(2 ** (j - 1))): J = j
                else: break
        gamma = {}
        if dangerous:
            gamma[0] = (beta0 // 2) % 2
            for j in range(1, J + 1):
                s = np.zeros_like(beta0)
                for r in range(2 ** (j - 1)): s += U(j, r)
                gamma[j] = (gamma[0] + s) % 2
            for j in range(1, J): assert (gamma[j] == gamma[0]).all(), ('gamma_j', n, els, e, j); st['equal'] += 1
            if e == 1 and J >= 1 and (gamma[J] != gamma[0]).any():
                assert any(sum(1 for x in idx if x % 2 ** J == r) % 2 for r in range(2 ** J)), ('odd class', n, els); st['e1special'] += 1
        lam = (neg @ Te[idx]) % 2
        for j in range(k + 1):
            badm = ~np.any(signs @ table(2 ** j * e, n)[idx], axis=1)
            if not badm.any(): continue
            assert dangerous and j <= J, ('bad level above J', n, els, e, j, J)
            assert (lam[badm] == gamma[j]).all(), ('lambda', n, els, e, j); st['badlevels'] += 1; st['badsignings'] += int(badm.sum())
    st['n'] += 1

random.seed(91)
st = dict(n=0, badlevels=0, badsignings=0, equal=0, e1special=0)
for n in (4, 8, 16, 6, 12, 24, 30, 60, 42, 70, 90, 62, 146, 20, 40, 126, 210):
    if n <= 30:
        for m in range(1, (6 if n <= 8 else 5 if n <= 16 else 4) + 1):
            for rest in itertools.combinations_with_replacement(range(n), m - 1): check(n, [0] + list(rest), st)
    for trial in range(240):
        els = gen(n, random.randint(3, 10), trial % (6 if two_part(n)[1] > 1 else 5))   # shape 5 needs an odd prime
        if els: check(n, els[:10], st)
    print(f'n={n} done; totals {st}', flush=True)
