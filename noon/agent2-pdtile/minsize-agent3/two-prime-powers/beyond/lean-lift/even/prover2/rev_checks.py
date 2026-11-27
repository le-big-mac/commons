# Checks made for the revision after the referee's report (27 November 2026).  Exact; own programs.
#  f1   finding 1: n = 100, B = {0, 20, 40, 60, 80}; and how often "at most four classes modulo every prime q >= 5"
#       fails as a hypothesis for the construction on Z_25, Z_50, Z_75, Z_100, against the corrected hypotheses
#  f3   finding 3: B = {0, 18, 21, 39, 42, 1, 1, 2, 2} modulo 45
#  f6   finding 6: the nine exhaustive lines of more_F.out
#  s2   suggestion 2: two residues modulo 2^k, k = 2, 3, 4: a signing is 3-good on Z_{n_3} iff it is 3-good for the
#       multiset on Z_{2 n''} that keeps the residue modulo n'' and puts the two residues modulo 2^k at 0 and 1
#  s3   suggestion 3: nine elements in the shape of equality of Corollary K: every fibrewise pair with a live level
#       has e_2 a power of 5 and R_fib <= 1/16
#  s5   suggestion 5: four elements on an odd modulus: the share of good signings is exactly 5/8
#  s6   suggestion 6 (Corollary C): share of 3-good >= rho_2 - (L + 1) * (sum over the live e' of 2^(-mu(e'*)))
import sys, random, re, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *
from thmF import sign3
from thmG import factor, live_levels
from propK import R_values

def live_big(B, n):
    f = factor(n)
    return {q: live_levels(B, q, b) for q, b in f.items() if q >= 5}

def construction_good(B, n):
    K, odd = two_part(n); q = 1 << K
    sg = sign3([(i, x % q) for i, x in enumerate(B)], K)
    if sg is None: return None
    return good(B, [sg[i] for i in range(len(B))], n)

mode = sys.argv[1]
if mode == 'f1':
    n = 100; B = [0, 20, 40, 60, 80]
    K, odd = two_part(n); q = 1 << K
    sg = sign3([(i, x % q) for i, x in enumerate(B)], K); signs = [sg[i] for i in range(5)]
    S = all_signs(5, fix_first=False); bad = bad_table(B, n, S)
    g = np.ones(S.shape[0], dtype=bool)
    for d in divisors(n): g &= ~bad[d]
    print('n = 100, B =', B, '| classes modulo 5:', sorted(set(x % 5 for x in B)), '| live levels of 5:', live_levels(B, 5, 2),
          '| signs of the construction:', signs, '| bad at:', [d for d in divisors(n) if is_bad(B, signs, n, d)],
          '| share of good signings:', Fr(int(g.sum()), S.shape[0]))
    for n, mmax in [(25, 6), (50, 5), (75, 4), (100, 4)]:
        f = factor(n)
        fail_old = fail_new = cnt_old = cnt_new = 0; lev2 = 0
        for m in range(1, mmax + 1):
            for B in multisets_with_zero(n, m):
                old = all(len(set(x % p for x in B)) <= 4 for p in f if p >= 5)       # the sentence as it was
                new = all(len(set(x % p ** f[p] for x in B)) <= 4 for p in f if p >= 5)  # the replacement
                if not old: continue
                r = construction_good(B, n)
                if r is None: continue
                cnt_old += 1
                if not r:
                    fail_old += 1
                    lev2 += any(2 in v for v in live_big(B, n).values())
                if new:
                    cnt_new += 1
                    assert not any(live_big(B, n).values())
                    if not r: fail_new += 1
        print('n', n, 'multisets with 0 up to', mmax, 'elements meeting at most four classes modulo 5:', cnt_old,
              '| the construction fails on', fail_old, '(all with level 2 of 5 live:', lev2 == fail_old, ')',
              '| at most four values modulo 25:', cnt_new, 'failures', fail_new, flush=True)
if mode == 'f3':
    B = [0, 18, 21, 39, 42, 1, 1, 2, 2]; n1 = 45
    R, Rfib, pairs = R_values(B, n1)
    W = sorted(set(B))
    print('B =', B, 'modulo 45 | live levels of 3:', live_levels(W, 3, 2), '| of 5:', live_levels(W, 5, 1),
          '| fibrewise pairs with a live level (e_2, i, D):', pairs, '| R =', R, '| R_fib =', Rfib)
if mode == 'f6':
    s = open('/home/agent3/lean/lift-check/even/prover2/more_F.out').read()
    ex = [int(x) for x in re.findall(r"all multisets with 0 up to \d+ elements: good (\d+)", s)]
    rn = [int(x) for x in re.findall(r"3\.\.30 elements: good (\d+)", s)]
    print('exhaustive lines:', len(ex), ex, 'sum', sum(ex), '| random lines:', len(rn), 'sum', sum(rn), '| together', sum(ex) + sum(rn))
if mode == 's2':
    rnd = random.Random(5); tot = 0
    for n3 in [20, 40, 80, 100, 140, 200, 280, 440]:
        k, odd = two_part(n3); q = 1 << k
        for t in range(150):
            m = rnd.randint(2, 9); u = rnd.sample(range(q), 2)
            cls = [rnd.randrange(2) for _ in range(m)]
            w = [rnd.randrange(odd) if t % 2 else rnd.choice([0, 1, 5, 7]) % odd for _ in range(m)]
            B = [next(x for x in range(u[c], n3, q) if x % odd == ww) for c, ww in zip(cls, w)]
            Bt = [next(x for x in range(c, 2 * odd, 2) if x % odd == ww) for c, ww in zip(cls, w)]
            S = all_signs(m, fix_first=False)
            b1 = bad3_table(B, n3, S); b2 = bad3_table(Bt, 2 * odd, S)
            g1 = np.ones(S.shape[0], dtype=bool); g2 = np.ones(S.shape[0], dtype=bool)
            for d in divisors(n3): g1 &= ~b1[d]
            for d in divisors(2 * odd): g2 &= ~b2[d]
            assert (g1 == g2).all(), (B, n3)
            tot += 1
    print('s2: two residues modulo 2^k, k = 2, 3, 4: the 3-good signings on Z_{n_3} and on Z_{2 n\'\'} are the same for', tot, 'multisets (all signings)')
if mode == 's3':
    rnd = random.Random(9); tot = 0; withpair = 0; mx = Fr(0); es = set()
    for n1 in [15, 45, 75, 105, 225, 315, 525, 1155, 1575]:
        f = factor(n1); a = f[3]
        for t in range(1200):
            i = rnd.randint(1, a)
            base = rnd.randrange(n1)
            # five points in one class modulo 3^i: either a coset of order 5, or one point in each class modulo 5, or random
            kind = t % 3
            def inclass(x): return (base + 3 ** i * x) % n1
            if kind == 0: five = [(base + s * (n1 // 5)) % n1 for s in range(5)]
            elif kind == 1: five = [inclass(next(y for y in range(rnd.randrange(n1), 10 ** 9) if (base + 3 ** i * y) % 5 == c)) for c in range(5)]
            else: five = [inclass(rnd.randrange(n1)) for _ in range(5)]
            if len(set(five)) < 5: continue
            rest = []
            for sgn in (1, 2):
                x = (rnd.choice(five) + sgn * (n1 // 3 ** i) + 3 ** i * rnd.randrange(n1)) % n1 if rnd.random() < 0.5 else (base + sgn * (n1 // 3 ** i)) % n1
                if rnd.random() < 0.5: rest += [x, x]
                else:
                    e2 = rnd.choice([d for d in divisors(n1 // 3 ** a) if d > 1])
                    rest += [x, (x + e2 * 3 ** a * rnd.randrange(1, 4)) % n1]
            B = five + rest
            R, Rfib, pairs = R_values(B, n1)
            tot += 1
            if pairs:
                withpair += 1
                for (e2, ii, D) in pairs:
                    es.add(e2)
                    assert set(factor(e2)) == {5}, (B, n1, pairs)
                    assert D >= 5, (B, n1, pairs)
                assert Rfib <= Fr(1, 16), (B, n1, Rfib)
                mx = max(mx, Rfib)
            assert R < Fr(86368, 10 ** 5), (B, n1, R)
    print('s3: nine elements, five in one class modulo 3^i and two in each of two other classes:', tot, 'multisets,', withpair,
          'with a fibrewise pair at a live level; e_2 always a power of 5:', sorted(es), '; largest R_fib', mx)
if mode == 's5':
    tot = 0
    for n in [3, 5, 9, 15, 21, 25, 27, 35, 45, 63, 75, 105]:
        for B in multisets_with_zero(n, 4):
            S = all_signs(4, fix_first=False); bad = bad_table(B, n, S)
            g = np.ones(16, dtype=bool)
            for d in divisors(n): g &= ~bad[d]
            assert int(g.sum()) == 10, (B, n)
            tot += 1
    print('s5: every multiset of four elements with 0 on n = 3, 5, 9, 15, 21, 25, 27, 35, 45, 63, 75, 105 (', tot, '): exactly 10 of 16 signings good')
if mode == 's6':
    rnd = random.Random(13); tot = 0; least = Fr(10)
    for n3 in [20, 40, 80, 100, 140, 200, 280, 400, 700]:
        k, odd = two_part(n3); f = factor(odd)
        for t in range(250):
            m = rnd.randint(3, 10)
            kind = t % 4
            if kind == 0: B = [rnd.randrange(n3) for _ in range(m)]
            elif kind == 1:
                o = rnd.randrange(n3); B = [(o + s * (n3 // 5) + rnd.choice([0, 0, n3 // 2, n3 // 4])) % n3 for s in range(5)] + [rnd.randrange(n3) for _ in range(m - 5)]
                B = B[:max(m, 5)]
            elif kind == 2:
                B = [(5 * rnd.randrange(n3) + c + rnd.choice([0, n3 // 4])) % n3 for c in range(5)] + [rnd.randrange(n3) for _ in range(max(0, m - 5))]
            else:
                us = [rnd.randrange(1 << k) for _ in range(3)]
                B = []
                for _ in range(m):
                    uu = rnd.choice(us); ww = rnd.randrange(odd)
                    B.append(next(x for x in range(uu, n3, 1 << k) if x % odd == ww))
            m = len(B)
            S = all_signs(m, fix_first=False); tot_s = S.shape[0]
            bad3 = bad3_table(B, n3, S)
            two = np.zeros(tot_s, dtype=bool); anyb = np.zeros(tot_s, dtype=bool)
            for d in divisors(n3):
                anyb |= bad3[d]
                if d & (d - 1) == 0: two |= bad3[d]
            rho2 = 1 - Fr(int(two.sum()), tot_s); g3 = 1 - Fr(int(anyb.sum()), tot_s)
            # L = number of live levels of the 2-tree
            L = 0
            for j in range(1, k + 1):
                occ = {}
                for x in B: occ.setdefault(x % (1 << (j - 1)), set()).add(x % (1 << j))
                L += any(len(v) == 2 for v in occ.values())
            live = {q: live_levels(B, q, b) for q, b in f.items()}
            ssum = Fr(0)
            for e in divisors(odd):
                if e == 1: continue
                fe = factor(e)
                if all(i in live[q] for q, i in fe.items()):
                    ssum += Fr(1, 2 ** max((live[q].index(i) + 1) * (q - 1) for q, i in fe.items()))
            assert g3 >= rho2 - (L + 1) * ssum, (B, n3, g3, rho2, L, ssum)
            least = min(least, g3 - (rho2 - (L + 1) * ssum)); tot += 1
    print('s6: share of 3-good >= rho_2 - (L + 1) * (sum over the live e\' of 2^(-mu)) on', tot, 'multisets of 3 to 10 elements (all signings); least slack', least)
