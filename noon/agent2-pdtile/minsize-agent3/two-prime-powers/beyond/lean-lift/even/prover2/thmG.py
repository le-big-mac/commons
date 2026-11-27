# Theorem G: n = 2 * 3^a * n'', gcd(n'', 6) = 1.  Checks, over ALL signings of each multiset:
#  (M)  Lemma M: bad at 3^i d' (i >= 1, d' | n_3 = n / 3^a)  ==>  3-bad at d'
#  (S)  step-down modulo 3: 3-bad at q^i d'' with level i of q not live  ==>  3-bad at q^(i-1) d''
#  (L)  share of 3-bad at c*e' (c in {1,2}, e' > 1 live)  <=  2^(-mu(e'*))
#  (T)  share of signings 3-good at 1 and 2  =  p_E + p_D - 2 p_E p_D  >= 1/4 (not an exceptional pair)
#  (G)  share of signings 3-good on Z_{n_3}  >= 1/4 - sum over live e' of 2 * 2^(-mu(e'*)), and > 0; all of them good on Z_n
import sys, random, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *

def factor(n):
    f = {}; p = 2
    while n > 1:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    return f

def live_levels(B, q, b):
    # list of live levels i in 1..b of the q-tree of B
    out = []
    for i in range(1, b + 1):
        occ = {}
        for x in B:
            occ.setdefault(x % q ** (i - 1), set()).add(x % q ** i)
        if any(len(s) == q for s in occ.values()): out.append(i)
    return out

def p0(r):
    # P(sum of r signs = 0 mod 3)
    p = Fr(1)
    for _ in range(r): p = (1 - p) / 2
    return p

def check(B, n, st):
    m = len(B)
    f = factor(n); a = f.get(3, 0); n3 = n // 3 ** a
    assert f.get(2, 0) == 1
    S = all_signs(m, fix_first=False)
    tot = S.shape[0]
    bad = bad_table(B, n, S)
    B3 = [x % n3 for x in B]
    bad3 = bad3_table(B3, n3, S)
    # (M)
    for d1 in divisors(n3):
        for i in range(1, a + 1):
            assert not (bad[d1 * 3 ** i] & ~bad3[d1]).any(), ('M', B, n, d1, i)
        assert not (bad[d1] & ~bad3[d1]).any()
    # liveness
    odd = n3 // 2
    fo = factor(odd)
    live = {q: live_levels(B, q, b) for q, b in fo.items()}
    # (S)
    for d in divisors(n3):
        for q, b in fo.items():
            i = 0
            while d % q ** (i + 1) == 0: i += 1
            if i >= 1 and i not in live[q]:
                assert not (bad3[d] & ~bad3[d // q]).any(), ('S', B, n, d, q)
    # (L) and the sum
    ssum = Fr(0)
    for e in divisors(odd):
        if e == 1: continue
        fe = factor(e)
        if all(i in live[q] for q, i in fe.items()):
            mu = max((live[q].index(i) + 1) * (q - 1) for q, i in fe.items())
            for c in (1, 2):
                sh = Fr(int(bad3[c * e].sum()), tot)
                assert sh <= Fr(1, 2 ** mu), ('L', B, n, e, c, sh, mu)
                st['Lmax'] = max(st['Lmax'], sh * 2 ** mu)
                ssum += Fr(1, 2 ** mu)
    # (T)
    rE = sum(1 for x in B if x % 2 == 0); rD = m - rE
    good12 = ~bad3[1] & ~bad3[2]
    sh12 = Fr(int(good12.sum()), tot)
    pe, pd = p0(rE), p0(rD)
    assert sh12 == pe + pd - 2 * pe * pd, ('T', B, n)
    exc = (m == 2 and rE == 1)
    if not exc: assert sh12 >= Fr(1, 4), ('T2', B, n)
    # (G)
    g3 = np.ones(tot, dtype=bool)
    for d in divisors(n3): g3 &= ~bad3[d]
    g = np.ones(tot, dtype=bool)
    for d in divisors(n): g &= ~bad[d]
    assert not (g3 & ~g).any()
    shg3 = Fr(int(g3.sum()), tot)
    assert shg3 >= sh12 - ssum, ('G', B, n, shg3, sh12, ssum)
    if exc:
        assert not g.any(); st['exc'] += 1
    else:
        assert g3.any(), ('no 3-good signing', B, n)
        st['min3good'] = min(st['min3good'], shg3)
        st['maxsum'] = max(st['maxsum'], ssum)
        st['ok'] += 1

def newst(): return {'ok': 0, 'exc': 0, 'Lmax': Fr(0), 'min3good': Fr(1), 'maxsum': Fr(0)}

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'exhaust':
        for n, mmax in [(6, 8), (18, 6), (10, 7), (30, 5), (42, 4), (54, 4), (66, 4), (90, 4), (70, 4)]:
            st = newst()
            for m in range(1, mmax + 1):
                for B in multisets_with_zero(n, m): check(B, n, st)
            print('n', n, 'all multisets with 0 up to', mmax, ':', {k: str(v) for k, v in st.items()}, flush=True)
    if mode == 'random':
        random.seed(11)
        for n in [30, 42, 66, 90, 150, 210, 330, 390, 630, 1050, 2310, 70, 770]:
            st = newst()
            f = factor(n); odd = n // 2
            for t in range(160):
                kind = t % 6
                m = random.randint(3, 12)
                if kind == 0: B = [random.randrange(n) for _ in range(m)]
                elif kind == 1:
                    h = [random.randrange(n // 2) for _ in range(m // 2)]; B = h + [x + n // 2 for x in h]
                elif kind == 2:
                    g = random.choice([d for d in divisors(n) if 1 < d <= 7]); s_ = n // g; B = []
                    while len(B) + g <= 12 or not B:
                        o = random.randrange(s_); B += [o + i * s_ for i in range(g)]
                        if random.random() < 0.4: break
                    B = B[:12]
                elif kind == 3:  # all three classes modulo 3 even
                    B = []
                    for c in range(3): B += [(3 * random.randrange(n) + c * (n + 1)) % n if n % 3 else random.randrange(n) for _ in range(2 * random.randint(1, 2))]
                elif kind == 4:  # one element in every class modulo a prime q >= 5, plus a few
                    q = random.choice([p for p in f if p >= 5]); B = [random.randrange(n // q) * q + c for c in range(q)]
                    B = [x % n for x in B][:11] + [random.randrange(n) for _ in range(random.randint(0, 2))]
                    B = B[:12]
                else:            # few values modulo the odd part
                    ws = [random.randrange(odd) for _ in range(3)]
                    B = [random.choice(ws) + odd * random.randrange(2) for _ in range(m)]
                check(B, n, st)
            print('n', n, 'random and structured (3..12 elements):', {k: str(v) for k, v in st.items()}, flush=True)
