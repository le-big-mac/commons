# Referee's test of item 5 of section 3 on actual multisets (3 does not divide n here, so n_3 = n).
# Written from the statements of Lemma L3 and Corollary 3; imports nothing of the author's.  Exact integers.
#
# usage: good3.py n m zero|rand [seconds]
# For each multiset (containing 0; or random ones built around full residue systems) and all 2^m signings:
#   3-bad at d (d | n): every coefficient of the remainder of S modulo Phi_d is divisible by 3
#   live e' > 1 (e' | n'', n = 2^k n''): every q^i || e' is a live level (some class modulo q^(i-1) has all
#   its q subclasses modulo q^i occupied);  e'* = prod q^(l_q), l_q = number of live levels of q up to v_q(e')
# Checked:  mu(e'*) <= m - 1;  share 3-bad at e' <= 2^(-mu(e'*));  sum over the live e' of the shares 3-bad at e'
#           <= W_m;  share of 3-good signings >= 1 - 2 p_m - 2 W_m.
# False variant counted: the cut one step lower, 1 - 2 p_m - 2 W_(m-2).
import sys, time, itertools, random
from fractions import Fraction as Fr
import numpy as np
from cyc import divisors, v2, xpow_mod

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % r for r in range(2, int(p ** 0.5) + 1))]

def factor(e):
    f, q = {}, 2
    while e > 1:
        while e % q == 0:
            f[q] = f.get(q, 0) + 1
            e //= q
        q += 1
    return f

def W_cut(m):
    s, t = Fr(0), 2
    def A(t):
        r = 1
        for p in primes_upto(t + 1):
            if p >= 5:
                r *= 1 + t // (p - 1)
        return r
    while t <= m - 1:
        s += Fr(A(t) - A(t - 2), 2 ** t)
        t += 2
    return s

def p(r):
    x = Fr(1)
    for _ in range(r):
        x = (1 - x) / 2
    return x

def main():
    n, m, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    limit = float(sys.argv[4]) if len(sys.argv) > 4 else 60.0
    assert n % 3 != 0
    t0 = time.time()
    k = v2(n); n2 = n >> k
    dn = divisors(n)
    rows = {d: np.array(xpow_mod(d, n), dtype=np.int64).reshape(n, -1) for d in dn}
    T = np.concatenate([rows[d] for d in dn], axis=1)
    starts = np.cumsum([0] + [rows[d].shape[1] for d in dn])[:-1]
    col = {d: i for i, d in enumerate(dn)}
    S = 1 << m
    sg = np.array([[-1 if (s >> i) & 1 else 1 for i in range(m)] for s in range(S)], dtype=np.int64)
    fac = {e: factor(e) for e in divisors(n2)}
    qs = sorted(factor(n2))
    vq = factor(n2)
    Wm, Wlow, pm = W_cut(m), W_cut(m - 2), p(m)
    bound = 1 - 2 * pm - 2 * Wm
    low = 1 - 2 * pm - 2 * Wlow
    if mode == "zero":
        gen = ((0,) + c for c in itertools.combinations_with_replacement(range(n), m - 1))
    else:
        rnd = random.Random(7)
        def randgen():
            while True:
                q = rnd.choice(qs)
                base = [(rnd.randrange(n // q) * q + t) % n for t in range(q)][:m]    # one element in each class modulo q
                yield tuple(sorted(base + [rnd.randrange(n) for _ in range(m - len(base))]))
        gen = randgen()
    cnt = fail_mu = fail_level = fail_sum = fail_share = fail_low = with_live = 0
    least = None; ex = None; maxmu = 0; cut = False
    for B in gen:
        if cnt % 500 == 0 and time.time() - t0 > limit:
            cut = True
            break
        cnt += 1
        Bl = list(B)
        R = sg @ T[Bl]
        Z = np.add.reduceat((R % 3 != 0).astype(np.int32), starts, axis=1) == 0     # Z[s, d]: 3-bad at d
        good = int((~Z.any(axis=1)).sum())
        sh = Fr(good, S)
        if least is None or sh < least:
            least, ex = sh, B
        if sh < bound: fail_share += 1
        if sh < low: fail_low += 1
        # live levels
        live = {}
        for q in qs:
            live[q] = []
            for i in range(1, vq[q] + 1):
                occ = {}
                for b in Bl:
                    occ.setdefault(b % q ** (i - 1), set()).add(b % q ** i)
                live[q].append(any(len(v) == q for v in occ.values()))
        tot = Fr(0); any_live = False
        for e, f in fac.items():
            if e == 1: continue
            if all(live[q][i - 1] for q, i in f.items()):
                any_live = True
                mu = max(sum(live[q][:i]) * (q - 1) for q, i in f.items())
                maxmu = max(maxmu, mu)
                if mu > m - 1: fail_mu += 1
                share_e = Fr(int(Z[:, col[e]].sum()), S)
                if share_e > Fr(1, 2 ** mu): fail_level += 1
                tot += share_e
        if any_live: with_live += 1
        if tot > Wm: fail_sum += 1
    print(f"n={n} m={m} mode={mode} multisets={cnt}{' (stopped by the time limit)' if cut or mode=='rand' else ''}: "
          f"with a live e'>1: {with_live}; largest mu(e'*) met {maxmu} (m-1 = {m-1}); failures: mu>m-1 {fail_mu}, "
          f"level bound {fail_level}, sum over live e' > W_m={Wm} {fail_sum}, share of 3-good < {bound} {fail_share}; "
          f"least share of 3-good met {least} at {ex}; false variant (cut at m-3: share >= {low}) fails in {fail_low}; "
          f"{time.time()-t0:.0f}s", flush=True)

main()
