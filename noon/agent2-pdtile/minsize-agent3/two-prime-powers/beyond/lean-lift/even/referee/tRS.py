# Lemma R and Lemma S, tested from the statements (exact remainders).
# Lemma R: for a signed multiset on Z_n, n even, the set of bad levels of S is compared with the set predicted
#   from the two halves S_0, S_1 on Z_N, N = n/2:
#     e odd:  bad at e   iff  S_0(theta) = -eta S_1(theta),  eta = theta^((e+1)/2)  [theta = eta^2, both of order e]
#             bad at 2e  iff  S_0(theta) =  eta S_1(theta)
#     d | N even:  bad at 2d  iff  S_0 and S_1 are both bad at d.
#   The predictions use only the tables of Z_N.
# Lemma S: the four masks of the last case.
import sys, random
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

rnd = random.Random(3)
cnt = badsome = 0
kinds = {'odd e': 0, '2e': 0, '2d': 0}
for trial in range(60000):
    n = rnd.choice([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 48, 60, 72, 84, 90, 96, 120])
    N = n // 2
    m = rnd.randint(1, 9)
    t = rnd.random()
    if t < 0.4:
        B = [rnd.randrange(n) for _ in range(m)]
    elif t < 0.8:
        g = rnd.choice([d for d in divisors(n) if d > 1])
        B = [(rnd.randrange(n // g) * g + rnd.choice([0, 0, 0, 1])) % n for _ in range(m)]
    else:
        h = [rnd.randrange(n) for _ in range(max(1, m // 2))]
        B = h + [(x + rnd.choice([N, n // rnd.choice([d for d in divisors(n) if d > 1])])) % n for x in h]
    s = [rnd.choice([1, -1]) for _ in range(len(B))]
    direct = set(d for d in divisors(n) if bad_one(B, s, n, d))
    E = [(x // 2, sg) for x, sg in zip(B, s) if x % 2 == 0]
    D = [((x - 1) // 2, sg) for x, sg in zip(B, s) if x % 2 == 1]
    pred = set()
    for e in divisors(n):
        if e % 2 == 1:
            T = table(max(N, 1) * e, e)          # X^y mod Phi_e for y up to N*e (enough for y + (e+1)/2)
            v0 = np.zeros(T.shape[1], dtype=np.int64)
            v1 = np.zeros(T.shape[1], dtype=np.int64)
            for y, sg in E:
                v0 += sg * T[y % e]
            for y, sg in D:
                v1 += sg * T[(y + (e + 1) // 2) % e]
            if not (v0 + v1).any():
                pred.add(e); kinds['odd e'] += 1
            if not (v0 - v1).any():
                pred.add(2 * e); kinds['2e'] += 1
    for d in divisors(N):
        if d % 2 == 0:
            b0 = bad_one([y for y, _ in E], [sg for _, sg in E], N, d)
            b1 = bad_one([y for y, _ in D], [sg for _, sg in D], N, d)
            if b0 and b1:
                pred.add(2 * d); kinds['2d'] += 1
    assert direct == pred, (n, B, s, direct, pred)
    cnt += 1
    badsome += bool(direct)
print("Lemma R: %d random signed multisets on 24 even moduli up to 120: the set of bad levels equals the predicted set every time"
      " (%d bad somewhere; predicted bad levels: %s)" % (cnt, badsome, kinds))

# Lemma S, last case: O = {a, b} an exceptional pair, c not in O with multiplicity >= 2 (or a with multiplicity 3)
def good(coefs, n):
    """coefs: dict exponent -> integer coefficient"""
    for d in divisors(n):
        T = table(n, d)
        v = np.zeros(T.shape[1], dtype=np.int64)
        for x, c in coefs.items():
            v += c * T[x % n]
        if not v.any():
            return False
    return True
cS = 0
for n in range(2, 49, 2):
    k, npr = split2(n)
    K = 1 << k
    for a in range(n):
        for b in range(n):
            if (a - b) % K == 0:
                continue
            v = v2((a - b) % K)
            assert good({a: 3, b: 1}, n) and good({a: 3, b: -1}, n)
            cS += 2
            if a != 0:
                continue          # the rest with a = 0 only (the statement is invariant under translation), every b, c
            for c in range(n):
                if c in (a, b):
                    continue
                u = k if (a - c) % K == 0 else v2((a - c) % K)
                if u >= v:
                    assert good({a: 1, b: 1, c: 2}, n), (n, a, b, c)
                else:
                    assert good({a: 1, b: -1, c: -2}, n), (n, a, b, c)
                cS += 1
print("Lemma S: 3X^a +- X^b for every exceptional pair, and the mask chosen by the rule u >= v / u < v for every (0, b, c): %d cases on even n <= 48, all good" % cS)
print("OK")
