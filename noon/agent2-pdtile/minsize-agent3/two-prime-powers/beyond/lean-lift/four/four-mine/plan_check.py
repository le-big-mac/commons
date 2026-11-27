"""A test of the statements of my plan for Lean (~/lean/signs-plan.md): S1 (step-down), S2 (a live level costs
2^((p-1) rank)), S3, S5 and step (i) of A1, on random multisets with every signing, by exact division by cyclotomic
polynomials. Nothing here is taken from the fourth instance's or the referee's programs.
usage: plan_check.py SEED COUNT"""
import sys, itertools, random
import numpy as np

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
_cyc = {}
def cyclo(d):
    """coefficients of Phi_d, lowest first, as a list of ints"""
    if d in _cyc: return _cyc[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            den = cyclo(e); q = [0] * (len(num) - len(den) + 1); r = num[:]
            for k in range(len(q) - 1, -1, -1):
                c = r[k + len(den) - 1] // den[-1]; q[k] = c
                for j, a in enumerate(den): r[k + j] -= c * a
            assert not any(r); num = q
    _cyc[d] = num; return num
def powers_mod(d, n):
    """row x: the coefficients of X^x mod Phi_d, for x < n"""
    phi = cyclo(d); deg = len(phi) - 1
    rows = []; cur = [1] + [0] * (deg - 1) if deg > 0 else []
    for x in range(n):
        rows.append(cur[:])
        nxt = [0] + cur
        c = nxt[deg]; nxt = nxt[:deg]
        if c:
            for j in range(deg): nxt[j] -= c * phi[j]
        cur = nxt
    return np.array(rows, dtype=np.int64)

def live(e, p, i):
    occ = {x % p ** i for x in e}
    return any(all((c + t * p ** (i - 1)) in occ for t in range(p)) for c in range(p ** (i - 1)))
def rank(e, p, i): return sum(1 for j in range(1, i + 1) if live(e, p, j))

def check(n, e, stats):
    m = len(e); f = factor(n); ds = divisors(n)
    signs = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64)       # every signing
    bad = {}
    for d in ds:
        T = powers_mod(d, n)[[x % n for x in e]]            # m rows
        bad[d] = ~np.any(signs @ T, axis=1)                  # True where Phi_d divides the signed mask
    lv = {(p, i): live(e, p, i) for p, a in f.items() for i in range(1, a + 1)}
    rk = {(p, i): rank(e, p, i) for p, a in f.items() for i in range(1, a + 1)}
    for (p, i), r in rk.items():
        assert (p - 1) * r + 1 <= m, ('S3', n, e, p, i); stats['S3'] += 1
    for d in ds:
        if d == 1: continue
        for p, i in factor(d).items():
            if not lv[(p, i)]:
                # S1: bad at d and level i of p not live => bad at d / p
                assert not np.any(bad[d] & ~bad[d // p]), ('S1', n, e, d, p); stats['S1'] += 1; stats['S1 with a bad signing'] += int(np.any(bad[d]))
            else:
                cnt = int(bad[d].sum()); stats['S2'] += 1
                assert cnt * 2 ** ((p - 1) * rk[(p, i)]) <= 2 ** m, ('S2', n, e, d, p, i, cnt)
                if cnt * 2 ** ((p - 1) * rk[(p, i)]) == 2 ** m: stats['S2 attained'] += 1
        if m >= 7 and d % 3 == 0 and factor(d) == {3: factor(d)[3]}:
            i = factor(d)[3]
            if lv[(3, i)] and rk[(3, i)] == 1:
                cnt = int(bad[d].sum()); stats['S5'] += 1
                assert cnt * 16 <= 3 * 2 ** m, ('S5', n, e, d, cnt)
    # A1 (i): every bad signing is bad at 1 or at some d all of whose prime levels are live
    Dstar = [d for d in ds if d > 1 and all(lv[(p, i)] for p, i in factor(d).items())]
    anybad = np.zeros(len(signs), bool); starbad = bad[1].copy()
    for d in ds: anybad |= bad[d]
    for d in Dstar: starbad |= bad[d]
    assert not np.any(anybad & ~starbad), ('A1(i)', n, e); stats['A1(i)'] += 1
    stats['good fraction min'] = min(stats['good fraction min'], 1 - anybad.mean())

if __name__ == '__main__':
    seed, count = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
    from collections import Counter
    stats = Counter(); stats['good fraction min'] = 1.0
    NS = [9, 15, 27, 45, 75, 81, 105, 135, 225, 315]
    for _ in range(count):
        n = rng.choice(NS); m = rng.randint(1, 11)
        kind = rng.random()
        if kind < 0.4: e = [rng.randrange(n) for _ in range(m)]
        elif kind < 0.7:                                    # clustered: few classes, to make levels dead or live
            base = [rng.randrange(n) for _ in range(rng.randint(1, 3))]; q = rng.choice(list(factor(n)))
            e = [(rng.choice(base) + rng.randrange(q) * (n // q ** rng.randint(1, factor(n)[q]))) % n for _ in range(m)]
        else:                                               # an interval or an arithmetic progression
            s = rng.choice([1, 1, 3, 5, 7, 9]); a = rng.randrange(n); e = [(a + s * k) % n for k in range(m)]
        check(n, e, stats)
    print('seed', seed, 'multisets', count, dict(stats))
