# A proof of Corollary N without valuations, proposed by the referee, tested here.
# Fix e odd, eta of order e.  For j >= 1 and a residue r modulo 2^j let
#     s_j(r) = sum over x with u_x = r (mod 2^j) of eps_x eta^{w_x}   (signed),   U_j(r) the same without signs.
# (a) [S0 for p = 2, and its converse]  eps is bad at 2^j e  iff  s_j(r) = s_j(r + 2^(j-1)) for every r < 2^(j-1).
# (b) Hence, if eps is bad at 2^j e:  beta_0 - 2 Lambda = S(eta) = 2 * sum_{r < 2^(j-1)} s_j(r),  Lambda = sum_{x in N} eta^{w_x},
#     so   lambda_e(N) = gamma_j := beta_0/2 + sum_{r < 2^(j-1)} U_j(r)   modulo 2 Z[eta]      (j >= 1),
#     and  lambda_e(N) = gamma_0 := beta_0/2 modulo 2 for j = 0.
# (c) Let J be the largest j >= 1 such that every class modulo 2^(j-1) has U in 2 Z[eta] (J = 0 if beta_0 is not in 2 Z[eta];
#     then nothing is bad).  A signing can be bad at 2^j e only for j <= J, and gamma_j = gamma_0 for 1 <= j < J.
#     So lambda_e(N) is gamma_0 or gamma_J: two values.
# Everything is computed in Z[Y]/(Phi_e) with integer vectors (exact), and reduced modulo 2 only at the end.
import sys, random, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

st = dict(multisets=0, a_checks=0, bad_signings=0, levels_bad=0, gamma_diff=0, e_seen={})

def check(B, n):
    k, npr = split2(n)
    K = 1 << k
    m = len(B)
    u = [x % K for x in B]
    w = [x % npr for x in B]
    bl = bad_levels(B, n)
    S = signmat(m)
    st['multisets'] += 1
    for e in divisors(npr):
        if e == 1:
            rows = np.ones((m, 1), dtype=np.int64)
        else:
            Te = table(e, e)
            rows = Te[np.array([x % e for x in w]), :]                 # eta^{w_x} as integer vectors
        beta0 = rows.sum(axis=0)
        # (a) for every j >= 1, all signings at once
        for j in range(1, k + 1):
            h = 1 << (j - 1)
            ok = np.ones(1 << m, dtype=bool)
            for r in range(h):
                c1 = np.array([1 if ux % (2 * h) == r else 0 for ux in u], dtype=np.int64)
                c2 = np.array([1 if ux % (2 * h) == r + h else 0 for ux in u], dtype=np.int64)
                diff = (S * (c1 - c2)[None, :]) @ rows                 # s_j(r) - s_j(r + h) for every signing
                ok &= ~diff.any(axis=1)
            assert (ok == bl[(1 << j) * e]).all(), ("S0 iff", n, B, e, j)
            st['a_checks'] += 1
        # J
        if (beta0 % 2).any():
            for j in range(k + 1):
                assert not bl[(1 << j) * e].any()
            continue
        J = 0
        for j in range(1, k + 1):
            h = 1 << (j - 1)
            allin = True
            for r in range(h):
                U = rows[[i for i in range(m) if u[i] % h == r], :].sum(axis=0) if any(ux % h == r for ux in u) else np.zeros(rows.shape[1], dtype=np.int64)
                if (U % 2).any():
                    allin = False
            if allin:
                J = j
            else:
                break
        half = (beta0 // 2) % 2
        gam = {0: half}
        for j in range(1, k + 1):
            h = 1 << (j - 1)
            sel = [i for i in range(m) if u[i] % (2 * h) < h]
            U = rows[sel, :].sum(axis=0) if sel else np.zeros(rows.shape[1], dtype=np.int64)
            gam[j] = (half + U) % 2
        for j in range(k + 1):
            idx = np.nonzero(bl[(1 << j) * e])[0]
            if len(idx) == 0:
                continue
            assert j <= J, ("bad above J", n, B, e, j, J)
            st['levels_bad'] += 1
            st['e_seen'][e] = st['e_seen'].get(e, 0) + 1
            if 1 <= j < J:
                assert (gam[j] == gam[0]).all()
            if (gam[j] != gam[0]).any():
                assert j == J
                st['gamma_diff'] += 1
            # lambda_e(N) for the bad signings: N = elements with sign -
            neg = (1 - S[idx, :]) // 2                                  # rows: indicator of N
            lam = (neg @ rows) % 2
            assert (lam == gam[j][None, :]).all(), ("lambda != gamma_j", n, B, e, j)
            st['bad_signings'] += len(idx)

def el(n, uu, ww):
    k, npr = split2(n)
    K = 1 << k
    for x in range(uu % K, n, K):
        if x % npr == ww % npr:
            return x

mode = sys.argv[1]
if mode == 'exh':
    n, m = int(sys.argv[2]), int(sys.argv[3])
    for B in multisets_with_zero(n, m):
        check(list(B), n)
    head = "EXHAUSTIVE n = %d, m = %d" % (n, m)
else:
    rnd = random.Random(int(sys.argv[2]))
    cnt = int(sys.argv[3])
    mods = [14, 28, 56, 30, 60, 120, 42, 84, 62, 124, 146, 70, 90, 126, 102, 34, 46, 170, 210, 24, 48, 36, 72, 40, 80]
    for _ in range(cnt):
        n = rnd.choice(mods)
        k, npr = split2(n)
        K = 1 << k
        t = rnd.random()
        if t < 0.15:
            B = [rnd.randrange(n) for _ in range(rnd.randint(3, 10))]
        elif t < 0.5:
            B = []
            for _ in range(rnd.randint(2, 5)):
                wv = rnd.randrange(npr)
                B += [el(n, rnd.randrange(K), wv), el(n, rnd.randrange(K), wv)]
        elif t < 0.7:
            h = [rnd.randrange(n) for _ in range(rnd.randint(2, 5))]
            B = h + [(x + n // 2) % n for x in h]
        elif t < 0.85:
            g = rnd.choice([d for d in divisors(n) if 1 < d <= 9])
            B = []
            while len(B) + g <= 11 and (not B or rnd.random() < 0.7):
                r = rnd.randrange(n)
                B += [(r + (n // g) * i) % n for i in range(g)]
        else:
            ws = [rnd.randrange(npr) for _ in range(3)]
            us = [rnd.randrange(K) for _ in range(3)]
            B = [el(n, rnd.choice(us), rnd.choice(ws)) for _ in range(rnd.randint(4, 10))]
        check(B[:11], n)
    head = "RANDOM AND STRUCTURED seed %s" % sys.argv[2]
print(head)
print("  multisets %(multisets)d; (a) 'bad at 2^j e iff the two halves of every class have equal signed sums' checked for %(a_checks)d (multiset, e, j), all signings;"
      " (b) lambda_e(N) = gamma_j for all %(bad_signings)d (bad signing, level); (c) %(levels_bad)d (multiset, e, level) with a bad signing, all with j <= J,"
      " gamma_j = gamma_0 for j < J; gamma_J differs from gamma_0 in %(gamma_diff)d of them" % st)
print("  e with bad signings:", dict(sorted(st['e_seen'].items())))
print("OK")
