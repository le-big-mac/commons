# t9_direction.py -- an experiment, not a test of the text: for ten (or twelve) elements on Z_{2^k * odd}, 3 not dividing,
# how large is U[e'] = share of signings 3-bad at 2^j e' for some j, for the live e', against 2^(-mu(e'*))?
# (The text's count for general k charges (L+1) * 2^(-mu) for L live levels of the 2-tree; Theorem J's proofs get
#  2 * 2^(-mu) and 2.5 * 2^(-mu) for six and eight elements.)  Also rho_2 and the share of 3-good signings.
# usage: t9_direction.py m n3 count
import sys, random
from rlib import *

m, n3, count = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
random.seed(4242 + m + n3)
k = vp(n3, 2); tk = 2 ** k; nodd = n3 >> k
f = factor(nodd)
assert n3 % 3 and all(v == 1 for v in f.values())   # squarefree odd part: mu(e'*) = (largest prime of e') - 1

def crt(u, w):
    inv = pow(tk, -1, nodd)
    return (u + tk * (((w - u) * inv) % nodd)) % n3

def gen():
    for _ in range(count):
        q = random.choice(list(f))
        base = random.randrange(nodd)
        ws = [(base + t * (nodd // q)) % nodd for t in range(q)]        # a full group of q
        style = random.random()
        while len(ws) < m:
            if style < 0.5:        # pairs with equal odd part (flat when signed oppositely)
                w = random.choice(ws) if random.random() < 0.5 else random.randrange(nodd)
                ws += [w, w]
            elif style < 0.8:
                ws.append(random.choice(ws))
            else:
                ws.append(random.randrange(nodd))
        ws = ws[:m]
        t = random.random()
        if t < 0.35:               # a chain in the 2-tree: the full group together, the others split off one level at a time
            a = random.randrange(tk)
            us = [a] * q
            for i in range(q, m):
                lev = min(k - 1, (i - q) // 2) if k else 0
                us.append((a + 2 ** lev) % tk if random.random() < 0.9 else random.randrange(tk))
        elif t < 0.6:
            vals = random.sample(range(tk), min(tk, random.randint(2, 4)))
            us = [random.choice(vals) for _ in range(m)]
        elif t < 0.8:
            a = random.randrange(tk)
            us = [(a + 2 ** random.randrange(k)) % tk if random.random() < 0.5 else a for _ in range(m)]
        else:
            us = [random.randrange(tk) for _ in range(m)]
        yield [crt(u, w) for u, w in zip(us, ws)]

S = 1 << (m - 1)
phi = len(cyclo(n3)) - 1
bs = max(50, min(20000, 12_000_000 // (S * phi)))
maxratio = {}; minrho = None; mingood = None; mindiff = None; cnt = 0
for E in chunks(gen(), bs):
    N = len(E)
    two_bad = np.zeros((N, S), dtype=bool)
    for j in range(k + 1):
        two_bad |= batch_bad3(E, 2 ** j)
    notgood = two_bad.copy()
    rho = S - two_bad.sum(axis=1)
    for e in divisors(nodd):
        if e == 1:
            continue
        u = np.zeros((N, S), dtype=bool)
        for j in range(k + 1):
            u |= batch_bad3(E, 2 ** j * e)
        notgood |= u
        # live: every prime of e has all its classes occupied
        is_live = np.ones(N, dtype=bool)
        for q in factor(e):
            for c in range(q):
                is_live &= ((E % q) == c).any(axis=1)
        if is_live.any():
            mu = max(factor(e)) - 1
            c = np.where(is_live, u.sum(axis=1), -1)
            i0 = int(np.argmax(c))
            ratio = Fraction(int(c[i0]), S) * 2 ** mu
            if e not in maxratio or ratio > maxratio[e][0]:
                maxratio[e] = (ratio, E[i0].tolist())
    good3 = S - notgood.sum(axis=1)
    i0 = int(np.argmin(rho))
    if minrho is None or Fraction(int(rho[i0]), S) < minrho[0]:
        minrho = (Fraction(int(rho[i0]), S), E[i0].tolist())
    i0 = int(np.argmin(good3))
    if mingood is None or Fraction(int(good3[i0]), S) < mingood[0]:
        mingood = (Fraction(int(good3[i0]), S), E[i0].tolist())
    cnt += N
print(f"m = {m}, n_3 = {n3}: {cnt} structured multisets with a full group: least rho_2 {minrho[0]} = {float(minrho[0]):.4f}; "
      f"least share of 3-good {mingood[0]} = {float(mingood[0]):.4f} at {mingood[1]}; "
      "largest U[e'] * 2^mu(e'*) for the live e': " + ", ".join(f"e' = {e}: {v[0]} = {float(v[0]):.3f} at {v[1]}" for e, v in sorted(maxratio.items())), flush=True)
