# (F')  Theorem F in its general form: any n; no level of any q-tree (q >= 5) of B is live  =>  the construction's
#       signing (it reads only the residues modulo 2^k) is good on Z_n.
# (G')  Remark after Theorem G: any k, B with at most two residues modulo 2^k: share of 3-good signings on Z_{n_3} > 0.
# (H)   Proposition H: odd n, m >= 3: more than half of the signings are good.
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *
from thmF import sign3
from thmG import factor, live_levels

def no_big_live(B, n):
    f = factor(n)
    return all(not live_levels(B, q, b) for q, b in f.items() if q >= 5)

mode = sys.argv[1]
random.seed(23)
if mode == 'F':
    for n, mmax in [(10, 6), (20, 5), (30, 5), (60, 4), (40, 4), (120, 4), (210, 3), (84, 4), (140, 3)]:
        ok = exc = skipped = 0
        K, odd = two_part(n); q = 1 << K
        for m in range(1, mmax + 1):
            for B in multisets_with_zero(n, m):
                if not no_big_live(B, n): skipped += 1; continue
                sg = sign3([(i, x % q) for i, x in enumerate(B)], K)
                if sg is None:
                    assert m == 2 and (B[0] - B[1]) % q != 0; exc += 1; continue
                assert good(B, [sg[i] for i in range(m)], n), (B, n)
                ok += 1
        print('F: n', n, 'all multisets with 0 up to', mmax, 'elements: good', ok, 'exceptional', exc, 'with a live q >= 5 (not covered)', skipped, flush=True)
    for n in [60, 120, 240, 420, 840, 1680, 2520, 3360, 9240]:
        ok = exc = 0
        K, odd = two_part(n); q = 1 << K; f = factor(n)
        for t in range(300):
            m = random.randint(3, 30)
            # at most 4 residues modulo every prime q >= 5, arbitrary modulo 2^K and the powers of 3
            res = {p: random.sample(range(p), min(p, random.randint(1, 4))) for p in f if p >= 5}
            B = []
            for _ in range(m):
                while True:
                    x = random.randrange(n)
                    if all(x % p in res[p] for p in res): break
                B.append(x)
            assert no_big_live(B, n)
            sg = sign3([(i, x % q) for i, x in enumerate(B)], K)
            if sg is None: exc += 1; continue
            assert good(B, [sg[i] for i in range(m)], n), (B, n)
            ok += 1
        print('F: n', n, 'random, at most 4 residues modulo each prime >= 5, 3..30 elements: good', ok, 'exceptional', exc, flush=True)
if mode == 'G2':
    for n in [12, 20, 60, 84, 120, 140, 180, 280, 420, 840, 1320]:
        K, odd = two_part(n); q = 1 << K; f = factor(n); a = f.get(3, 0); n3 = n // 3 ** a
        mn = Fr(1); cnt = 0
        for t in range(120):
            m = random.randint(3, 11)
            u = random.sample(range(q), 2)
            B = []
            for _ in range(m):
                uu = random.choice(u); w = random.randrange(odd) if t % 2 else random.choice([0, 1, odd // 3 if odd % 3 == 0 else 2, 5 % odd])
                B.append(next(x for x in range(uu, n, q) if x % odd == w))
            S = all_signs(m, fix_first=False)
            bad3 = bad3_table([x % n3 for x in B], n3, S)
            g3 = np.ones(S.shape[0], dtype=bool)
            for d in divisors(n3): g3 &= ~bad3[d]
            bad = bad_table(B, n, S)
            g = np.ones(S.shape[0], dtype=bool)
            for d in divisors(n): g &= ~bad[d]
            assert not (g3 & ~g).any()
            if len(set(x % q for x in B)) == 2 and m == 2: continue
            sh = Fr(int(g3.sum()), S.shape[0])
            if len(set(x % q for x in B)) == 1 and False: pass
            assert sh > 0, (B, n)
            mn = min(mn, sh); cnt += 1
        print('G2: n', n, 'multisets with at most two residues modulo', q, ':', cnt, 'least share of 3-good signings', mn, flush=True)
if mode == 'H':
    for n, mmax in [(3, 9), (9, 7), (15, 6), (21, 5), (27, 5), (45, 5), (35, 5), (105, 4), (75, 4)]:
        least = {}
        for m in range(1, mmax + 1):
            for B in multisets_with_zero(n, m):
                S = all_signs(m, fix_first=False)
                bad = bad_table(B, n, S)
                g = np.ones(S.shape[0], dtype=bool)
                for d in divisors(n): g &= ~bad[d]
                sh = Fr(int(g.sum()), S.shape[0])
                least[m] = min(least.get(m, Fr(1)), sh)
                if m >= 3: assert sh > Fr(1, 2), (B, n, sh)
        print('H: n', n, 'all multisets with 0 up to', mmax, ': least share of good signings by m:', {m: str(v) for m, v in least.items()}, flush=True)
    for n in [45, 105, 135, 315, 525, 1155]:
        least = Fr(1)
        for t in range(150):
            m = random.randint(3, 13)
            kind = t % 3
            if kind == 0: B = [random.randrange(n) for _ in range(m)]
            elif kind == 1:
                g = random.choice([d for d in divisors(n) if 1 < d <= 7]); B = []
                while len(B) + g <= 13:
                    o = random.randrange(n // g); B += [o + i * (n // g) for i in range(g)]
                    if random.random() < 0.3: break
            else:
                B = [3 * random.randrange(n // 3) + c for c in range(3) for _ in range(random.randint(1, 4))]
            m = len(B)
            S = all_signs(m, fix_first=False)
            bad = bad_table(B, n, S)
            g_ = np.ones(S.shape[0], dtype=bool)
            for d in divisors(n): g_ &= ~bad[d]
            sh = Fr(int(g_.sum()), S.shape[0])
            assert sh > Fr(1, 2), (B, n, sh)
            least = min(least, sh)
        print('H: n', n, 'random and structured, 3..13 elements: least share of good signings', least, '=%.4f' % float(least), flush=True)
