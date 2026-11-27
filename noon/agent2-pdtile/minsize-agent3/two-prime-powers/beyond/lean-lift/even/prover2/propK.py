# Proposition K of even-result-2.md (odd number of elements, odd modulus n'):
#   R = sum over the live dangerous e > 1 of 2^(1 - D_e)  <=  0.801174 + R_fib,
#   R_fib = sum over the pairs (e2, i), e2 > 1 prime to 3, i >= 1, 3^i e2 live and dangerous, every class modulo 3^i
#           with an e2-dangerous restriction, of 2^(1 - D_{3^i e2}).
# Checked on multisets of 5 and 7 elements (R_fib = 0 for 5; R < 1 for both) and on larger random and structured ones.
import sys, random, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from ranks import factor, powrem2, rank2, live_levels
from ranks2 import gen
from lib2 import divisors

def R_values(F, n1):
    # F: multiset (list) on Z_{n1}; returns (R, R_fib, list of fibre pairs)
    mult = {}
    for x in F: mult[x % n1] = mult.get(x % n1, 0) + 1
    W = sorted(mult); W2 = [w for w in W if mult[w] % 2]
    assert len(W2) % 2 == 1
    f = factor(n1); a = f.get(3, 0)
    live = {q: live_levels(W, q, b) for q, b in f.items()}
    R = Fr(0); Rfib = Fr(0); pairs = []
    info = {}
    for e in divisors(n1):
        if e == 1: continue
        pr = powrem2(e); s = 0
        for w in W2: s ^= pr[w % e]
        lv = all(i in live[q] for q, i in factor(e).items())
        D = rank2([pr[w % e] for w in set(x % e for x in W)])
        info[e] = (lv, s == 0, D)
        if lv and s == 0: R += Fr(2, 2 ** D)
    for e2 in divisors(n1):
        if e2 == 1 or e2 % 3 == 0: continue
        pr2 = powrem2(e2)
        for i in range(1, a + 1):
            lv, dg, D = info[3 ** i * e2]
            if not (lv and dg): continue
            act = {}
            for w in W2: act[w % 3 ** i] = act.get(w % 3 ** i, 0) ^ pr2[w % e2]
            if not any(act.values()):
                assert info[e2][1]
                Rfib += Fr(2, 2 ** D); pairs.append((e2, i, D))
    return R, Rfib, pairs

if __name__ == '__main__':
    rnd = random.Random(31)
    BOUND = Fr(801174, 10 ** 6)
    for n1 in [15, 45, 105, 135, 225, 315, 525, 945, 1155]:
        mx5 = mx7 = Fr(0); c5 = c7 = 0; fib7 = 0
        for t in range(1500):
            m = 5 if t % 2 == 0 else 7
            if t % 4 < 2: F = [rnd.randrange(n1) for _ in range(m)]
            else:   # five points in one class modulo 3^j forming a dangerous shape if possible, plus two points
                q = rnd.choice([p for p in factor(n1) if p >= 5]); o = rnd.randrange(n1)
                F = [(o + s * (n1 // q)) % n1 for s in range(q)][:5]
                while len(F) < m:
                    x = rnd.choice(F); j = rnd.randint(1, factor(n1)[3])
                    F.append((x + rnd.randrange(1, 3) * (n1 // 3 ** j)) % n1)
            R, Rfib, pairs = R_values(F, n1)
            assert R - Rfib <= BOUND, (F, n1, R, Rfib)
            assert R < 1
            if m == 5:
                assert Rfib == 0, (F, n1); mx5 = max(mx5, R); c5 += 1
            else:
                assert Rfib <= Fr(3, 16); mx7 = max(mx7, R); c7 += 1; fib7 += bool(pairs)
        mxb = Fr(0); mxd = Fr(0); nf = 0
        for t in range(1500):
            W, W2 = gen(n1, t % 4, rnd)
            F = list(W2) + [w for w in W if w not in set(W2)] * 2
            R, Rfib, pairs = R_values(F, n1)
            assert R - Rfib <= BOUND, (F, n1, R, Rfib)
            mxb = max(mxb, R); mxd = max(mxd, R - Rfib); nf += bool(pairs)
        print("n'", n1, '| 5 elements:', c5, 'max R', mx5, '| 7 elements:', c7, 'max R', mx7, 'with a fibre pair', fib7,
              '| larger structured: 1500, max R %.4f' % float(mxb), 'max R - R_fib %.4f' % float(mxd), 'with a fibre pair', nf, flush=True)
