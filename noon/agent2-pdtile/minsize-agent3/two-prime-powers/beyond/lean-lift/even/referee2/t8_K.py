# t8_K.py -- Corollary K by brute force: multisets of 5, 7, 9 elements on n with 4 | n and 15 | n: all signings, exact:
# a good signing exists; the share of bad signings against 0.8012 (m = 5, 7) and 0.9887 (m = 9).
# usage: t8_K.py exhaust m n | random m n count | struct9 n count
import sys, random
from rlib import *

def bad_share(E, n):
    N, m = E.shape
    S = 1 << (m - 1)
    good = np.ones((N, S), dtype=bool)
    for d in divisors(n):
        good &= ~batch_bad(E, d)
    return S - good.sum(axis=1), S

def crt(u, w, tk, nodd):
    inv = pow(tk, -1, nodd)
    return (u + tk * (((w - u) * inv) % nodd)) % (tk * nodd)

def run(gen, n, m, title):
    S = 1 << (m - 1)
    phi = len(cyclo(n)) - 1
    bs = max(100, min(100000, 20_000_000 // (S * phi)))
    lim = Fraction(8012, 10000) if m in (5, 7) else Fraction(9887, 10000)
    worst = None; cnt = 0
    for E in chunks(gen, bs):
        b, S = bad_share(E, n)
        i0 = int(np.argmax(b))
        v = Fraction(int(b[i0]), S)
        if worst is None or v > worst[0]:
            worst = (v, E[i0].tolist())
        cnt += len(E)
    assert worst[0] < lim, ("Corollary K's share fails", worst)
    print(f"{title}: {cnt} multisets; every one has a good signing; largest share of bad signings {worst[0]} = {float(worst[0]):.4f} at {worst[1]} (Corollary K: < {float(lim)})", flush=True)

mode = sys.argv[1]
random.seed(99)
if mode == 'exhaust':
    m, n = int(sys.argv[2]), int(sys.argv[3])
    run(multisets(n, m, with0=True), n, m, f"m = {m}, n = {n}, every multiset with 0")
elif mode == 'random':
    m, n, cnt = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    k = vp(n, 2); tk = 2 ** k; nodd = n // tk
    f = factor(nodd)
    def gen():
        for _ in range(cnt):
            style = random.random()
            if style < 0.3:
                ws = [random.randrange(nodd) for _ in range(m)]
            elif style < 0.7:    # cosets of prime order (dangerous shapes), then filled up
                ws = []
                while len(ws) < m - 2:
                    q = random.choice(list(f)); x = random.randrange(nodd)
                    co = [(x + t * (nodd // q)) % nodd for t in range(q)]
                    if len(ws) + len(co) <= m:
                        ws += co
                    else:
                        break
                while len(ws) < m:
                    ws.append(random.choice(ws) if ws and random.random() < 0.5 else random.randrange(nodd))
            else:                # few distinct points
                base = random.sample(range(nodd), random.randint(2, 5))
                ws = [random.choice(base) for _ in range(m)]
            t = random.random()
            if t < 0.4:
                us = [random.randrange(tk) for _ in range(m)]
            elif t < 0.7:
                vals = random.sample(range(tk), 3)
                us = [random.choice(vals) for _ in range(m)]
            else:
                a = random.randrange(tk)
                us = [(a + random.choice([0, tk // 2, tk // 4 if tk >= 4 else 0])) % tk for _ in range(m)]
            yield [crt(u, w, tk, nodd) for u, w in zip(us, ws)]
    run(gen(), n, m, f"m = {m}, n = {n}, random and structured")
elif mode == 'struct9':
    # the case of equality in the proof for nine elements: five points of multiplicity one in a class c* modulo 3^i, one in each
    # class modulo 5, and two elements, congruent modulo 5 (hence equal modulo 15 if 3 || n'), in each of the two sister classes
    n, cnt = int(sys.argv[2]), int(sys.argv[3])
    k = vp(n, 2); tk = 2 ** k; nodd = n // tk
    a = vp(nodd, 3)
    rest = nodd // 3 ** a            # prime to 3, divisible by 5
    def gen():
        for _ in range(cnt):
            i = random.randint(1, a)
            # residues modulo 3^a: c* = class r0 modulo 3^i ; sisters r0 + 3^(i-1), r0 + 2*3^(i-1)
            r0 = random.randrange(3 ** i)
            def in_class(r):
                return (r + 3 ** i * random.randrange(3 ** (a - i))) % 3 ** a
            pts = []
            base5 = random.randrange(rest)
            for t in range(5):
                w5 = (base5 + t * (rest // 5)) % rest if random.random() < 0.8 else None
                if w5 is None:
                    w5 = (base5 + t * (rest // 5)) % rest
                pts.append(crt(in_class(r0), w5, 3 ** a, rest) if a else w5)
            for s in (1, 2):
                r = (r0 + s * 3 ** (i - 1)) % 3 ** i
                w5 = random.randrange(rest)
                x = crt(in_class(r), w5, 3 ** a, rest)
                y = x if random.random() < 0.5 else crt(in_class(r), w5, 3 ** a, rest)
                pts += [x, y]
            us = [random.randrange(tk) for _ in range(9)]
            if random.random() < 0.3:
                vals = random.sample(range(tk), 2)
                us = [random.choice(vals) for _ in range(9)]
            yield [crt(u, w, tk, nodd) for u, w in zip(us, pts)]
    run(gen(), n, 9, f"m = 9, n = {n}, the shape of equality (five points on a coset of order 5 in one class modulo 3^i, a pair in each sister class)")
