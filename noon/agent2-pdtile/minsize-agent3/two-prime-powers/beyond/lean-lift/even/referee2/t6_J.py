# t6_J.py -- Theorem J by brute force (all signings, exact; "3-bad at d" from the definition).
# For a multiset B on Z_{n3} (3 does not divide n3 = 2^k * n''), with all signings:
#   rho2      = share of signings 3-bad at no 2^j
#   U[e]      = share of signings 3-bad at 2^j * e for some j   (e | n'', e > 1)
#   good3     = share of 3-good signings
# Claims of the proofs, for the LIVE e: six elements: U[5^i] <= 1/8, good3 >= 3/16;
#   eight elements: U[5^i] <= 5/32, U[7^i'] <= 1/32, U[5^i 7^i'] = 0, good3 >= 9/64.
# usage: t6_J.py MODE ...   (modes below)
import sys, random
from itertools import combinations_with_replacement, product
from rlib import *

def occupancy_live(E, q, i):
    # boolean N: level i of the q-tree is live
    N = E.shape[0]
    qi = q ** i
    occ = np.zeros((N, qi), dtype=bool)
    occ[np.arange(N)[:, None], E % qi] = True
    occ = occ.reshape(N, q, qi // q)       # index = t * q^(i-1) + r  ->  [t, r]
    return occ.all(axis=1).any(axis=1)

class Stat:
    def __init__(self, m):
        self.m = m
        self.cnt = 0
        self.min_rho = None
        self.min_good3 = None
        self.maxU = {}          # kind -> (value, example)
        self.with_live = 0
        self.viol = []
    def report(self, title):
        s = f"{title}: {self.cnt} multisets ({self.with_live} with a live level at 5 or 7); least rho_2 {self.min_rho[0]} at {self.min_rho[1]}; "
        s += "largest share 3-bad at 2^j e' for some j, by kind of live e': " + ", ".join(f"{k}: {v[0]} at {v[1]}" for k, v in sorted(self.maxU.items())) + "; "
        s += f"least share of 3-good {self.min_good3[0]} at {self.min_good3[1]}; violations of the proof's bounds: {len(self.viol)} {self.viol[:3]}"
        print(s, flush=True)

def analyse(E, n3, st):
    N, m = E.shape
    S = 1 << (m - 1)
    k = vp(n3, 2)
    nodd = n3 >> k
    assert n3 % 3 != 0
    f = factor(nodd)
    two_bad = np.zeros((N, S), dtype=bool)
    for j in range(k + 1):
        two_bad |= batch_bad3(E, 2 ** j)
    U = {}
    for e in divisors(nodd):
        if e == 1:
            continue
        u = np.zeros((N, S), dtype=bool)
        for j in range(k + 1):
            u |= batch_bad3(E, 2 ** j * e)
        U[e] = u
    notgood = two_bad.copy()
    for e in U:
        notgood |= U[e]
    rho = S - two_bad.sum(axis=1)
    good3 = S - notgood.sum(axis=1)
    live = {(q, i): occupancy_live(E, q, i) for q in f for i in range(1, f[q] + 1)}
    anylive = np.zeros(N, dtype=bool)
    for v in live.values():
        anylive |= v
    st.with_live += int(anylive.sum())
    st.cnt += N
    i0 = int(np.argmin(rho))
    if st.min_rho is None or Fraction(int(rho[i0]), S) < st.min_rho[0]:
        st.min_rho = (Fraction(int(rho[i0]), S), E[i0].tolist())
    i0 = int(np.argmin(good3))
    if st.min_good3 is None or Fraction(int(good3[i0]), S) < st.min_good3[0]:
        st.min_good3 = (Fraction(int(good3[i0]), S), E[i0].tolist())
    lim_good = Fraction(3, 16) if m == 6 else Fraction(9, 64)
    lim_rho = Fraction(5, 16) if m == 6 else Fraction(21, 64)
    bad_rows = np.nonzero((good3 * lim_good.denominator < lim_good.numerator * S) | (rho * lim_rho.denominator < lim_rho.numerator * S))[0]
    for r in bad_rows[:3]:
        st.viol.append(('share', E[r].tolist()))
    for e, u in U.items():
        fe = factor(e)
        is_live = np.ones(N, dtype=bool)
        for q, i in fe.items():
            is_live &= live[(q, i)]
        if not is_live.any():
            continue
        cnt = u.sum(axis=1)
        kind = "*".join(f"{q}^i" for q in sorted(fe))
        if m == 6:
            lim = Fraction(1, 8) if set(fe) == {5} else None
        else:
            lim = Fraction(5, 32) if set(fe) == {5} else Fraction(1, 32) if set(fe) == {7} else Fraction(0) if set(fe) == {5, 7} else None
        c = np.where(is_live, cnt, -1)
        i0 = int(np.argmax(c))
        val = Fraction(int(c[i0]), S)
        if kind not in st.maxU or val > st.maxU[kind][0]:
            st.maxU[kind] = (val, E[i0].tolist())
        if lim is not None:
            v = np.nonzero(is_live & (cnt * lim.denominator > lim.numerator * S))[0]
            for r in v[:3]:
                st.viol.append((kind, E[r].tolist()))
    return good3

def run(gen, n3, m, title, bs=None):
    st = Stat(m)
    S = 1 << (m - 1)
    phi = len(cyclo(n3)) - 1
    bs = bs or max(200, min(100000, 20_000_000 // (S * phi)))
    for E in chunks(gen, bs):
        analyse(E, n3, st)
    st.report(title)
    return st

def crt(u, w, tk, nodd):
    # the residue modulo tk*nodd that is u mod tk and w mod nodd
    inv = pow(tk, -1, nodd) if nodd > 1 else 0
    return (u + tk * (((w - u) * inv) % nodd)) % (tk * nodd)

mode = sys.argv[1]
random.seed(2027)

if mode == 'exhaust':           # exhaust m n3 : every multiset with 0
    m, n3 = int(sys.argv[2]), int(sys.argv[3])
    run(multisets(n3, m, with0=True), n3, m, f"m = {m}, n_3 = {n3}, every multiset with 0")

elif mode == 'live1':           # live1 m q k : every multiset of m elements on Z_{2^k q} that meets every class modulo q (up to translation)
    m, q, k = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    tk = 2 ** k
    n3 = tk * q
    def gen():
        # residues modulo q: 0..q-1 once each, and m-q further residues (a multiset, up to translation: not reduced);
        # 2-parts: all, with the 2-part of the first element 0 (translation by multiples of q)
        for extra in combinations_with_replacement(range(q), m - q):
            ws = list(range(q)) + list(extra)
            for us in product(range(tk), repeat=m - 1):
                yield [crt(u, w, tk, q) for u, w in zip((0,) + us, ws)]
    if len(sys.argv) > 5:       # a random sample instead
        cnt = int(sys.argv[5])
        def gen():
            for _ in range(cnt):
                ws = list(range(q)) + [random.randrange(q) for _ in range(m - q)]
                yield [crt(random.randrange(tk), w, tk, q) for w in ws]
    run(gen(), n3, m, f"m = {m}, n_3 = {n3}, every class modulo {q} occupied" + (" (random sample)" if len(sys.argv) > 5 else " (all, up to translation; some repeated)"))

elif mode == 'level2':          # level2 m k : Z_{2^k 25}: five elements 0,5,10,15,20 modulo 25 and m-5 further, all 2-parts
    m, k = int(sys.argv[2]), int(sys.argv[3])
    tk = 2 ** k
    n3 = tk * 25
    cnt = int(sys.argv[4]) if len(sys.argv) > 4 else None
    def gen():
        if cnt is None:
            for extra in combinations_with_replacement(range(25), m - 5):
                ws = [0, 5, 10, 15, 20] + list(extra)
                for us in product(range(tk), repeat=m - 1):
                    yield [crt(u, w, tk, 25) for u, w in zip((0,) + us, ws)]
        else:
            for _ in range(cnt):
                ws = [0, 5, 10, 15, 20] + [random.randrange(25) for _ in range(m - 5)]
                yield [crt(random.randrange(tk), w, tk, 25) for w in ws]
    run(gen(), n3, m, f"m = {m}, n_3 = {n3}, level 2 of 5 live (0,5,10,15,20 modulo 25 and {m - 5} further)" + (" (random sample)" if cnt else " (all)"))

elif mode == 'random':          # random m n3 count : random and structured multisets with a live level at 5 or 7
    m, n3, cnt = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    k = vp(n3, 2); tk = 2 ** k; nodd = n3 >> k
    f = factor(nodd)
    def gen():
        made = 0
        while made < cnt:
            style = random.random()
            ws = []
            q = random.choice(list(f))
            i = random.randint(1, f[q])
            # a full group of q at level i
            base = random.randrange(nodd)
            step = nodd // (q ** (f[q] - i + 1))      # adding step runs through the q subclasses of one class modulo q^(i-1)
            ws = [(base + t * step) % nodd for t in range(q)]
            if len(ws) > m:
                continue
            if 5 in f and 7 in f and m >= 8 and style < 0.5 and nodd in (35,):
                # both live: seven residues modulo 7, all residues modulo 5
                w7 = list(range(7)); random.shuffle(w7)
                w5 = [0, 1, 2, 3, 4] + [random.randrange(5) for _ in range(2)]; random.shuffle(w5)
                rest = nodd // 35
                ws = [crt(crt(a, b, 5, 7), random.randrange(rest) if rest > 1 else 0, 35, rest) if rest > 1 else crt(a, b, 5, 7) for a, b in zip(w5, w7)]
            while len(ws) < m:
                if style < 0.75:
                    ws.append(random.choice(ws) if random.random() < 0.6 else random.randrange(nodd))
                else:
                    ws.append((random.choice(ws) + random.choice(list(f)) ** random.randint(0, 1) * random.randrange(nodd)) % nodd)
            # 2-parts: shapes of the proof: one class of the 2-tree holding five or seven, a pair or triple apart; or random
            t = random.random()
            if t < 0.3:
                us = [random.randrange(tk) for _ in range(m)]
            elif t < 0.6:
                a = random.randrange(tk); b = random.randrange(tk)
                us = [a] * q + [b] * (m - q)
            elif t < 0.8:
                a = random.randrange(tk); j = random.randrange(k) if k else 0
                us = [(a + (2 ** j) * random.randrange(2)) % tk for _ in range(m)]
            else:
                vals = random.sample(range(tk), min(tk, 3))
                us = [random.choice(vals) for _ in range(m)]
            made += 1
            yield [crt(u, w, tk, nodd) for u, w in zip(us, ws)]
    run(gen(), n3, m, f"m = {m}, n_3 = {n3}, random and structured with a full group")

elif mode == 'direct':          # direct m n count [liveonly] : a good signing on Z_n by brute force; and "3-good on Z_{n_3} implies good on Z_n"
    m, n, cnt = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    n3 = n
    while n3 % 3 == 0:
        n3 //= 3
    S = 1 << (m - 1)
    tot = 0; least = None; nogood = 0; lemmaM_viol = 0; least3 = None
    def gen():
        if cnt == 0:
            yield from multisets(n, m, with0=True)
        else:
            for _ in range(cnt):
                yield [random.randrange(n) for _ in range(m)]
    phi = len(cyclo(n)) - 1
    bs = max(200, min(50000, 20_000_000 // (S * phi)))
    for E in chunks(gen(), bs):
        if len(sys.argv) > 5:
            keep = np.ones(len(E), dtype=bool)
            for c in range(5):
                keep &= ((E % 5) == c).any(axis=1)
            E = E[keep]
            if len(E) == 0:
                continue
        good = np.ones((len(E), S), dtype=bool)
        good3 = np.ones((len(E), S), dtype=bool)
        for d in divisors(n):
            R = batch_res(E, d)
            good &= R.any(axis=2)
            if n3 % d == 0:
                good3 &= (R % 3).any(axis=2)
        lemmaM_viol += int((good3 & ~good).sum())
        g = good.sum(axis=1); g3 = good3.sum(axis=1)
        nogood += int((g == 0).sum())
        tot += len(E)
        i0 = int(np.argmin(g))
        if least is None or Fraction(int(g[i0]), S) < least[0]:
            least = (Fraction(int(g[i0]), S), E[i0].tolist())
        i0 = int(np.argmin(g3))
        if least3 is None or Fraction(int(g3[i0]), S) < least3[0]:
            least3 = (Fraction(int(g3[i0]), S), E[i0].tolist())
    print(f"m = {m}, n = {n}: {tot} multisets ({'every multiset with 0' if cnt == 0 else 'random'}{', only those meeting every class modulo 5' if len(sys.argv) > 5 else ''}): "
          f"without a good signing: {nogood}; least share of good signings {least[0]} at {least[1]}; least share of 3-good (on Z_{n3}) {least3[0]} at {least3[1]}; "
          f"signings 3-good on Z_{n3} but not good on Z_{n}: {lemmaM_viol}", flush=True)
