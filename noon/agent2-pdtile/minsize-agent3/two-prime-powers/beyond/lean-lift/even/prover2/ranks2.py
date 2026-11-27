# Section 5 of even-result-2.md: tests on an odd Z_{n'} (support W, odd-size W2 inside W).
#  (X)  fibre formula for e = 3^i * e2 (e2 prime to 3, i >= 1):
#         D_e(W) = sum over the classes r modulo 3^(i-1) of [ sum_t dim V_{r,t} - dim (V_{r,0} & V_{r,1} & V_{r,2}) ],
#         V_c = span of the X^w mod (2, Phi_e2), w in W, w = c mod 3^i
#  (A)  e live, dangerous, e2 > 1 not dangerous:  D_e >= max(2 * 3^(l'-1), D_e2(W) + 1)
#  (B)  e2 > 1 live and dangerous: rho = [sum over i >= 1 with 3^i e2 live and dangerous of 2^(1-D)] / 2^(1-mu(e2*)),
#       and the least value of D_{3^i e2} - mu(e2*) - (2l - 1)
import sys, random, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from ranks import factor, powrem2, rank2, live_levels, crt
from lib2 import divisors

def basis_of(vs):
    basis = {}
    for v in vs:
        while v:
            h = v.bit_length() - 1
            if h in basis: v ^= basis[h]
            else: basis[h] = v; break
    return list(basis.values())

def intersect(A, B, K):
    # bases A, B (bitmasks < 2^K) -> basis of the intersection
    rows = [(a << K) | a for a in A] + [(b << K) for b in B]
    piv = {}
    out = []
    for v in rows:
        while v >> K:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; break
        else:
            if v: out.append(v)
    return basis_of(out)

def analyse(W, W2, n1, st):
    f = factor(n1)
    W = sorted(set(W)); W2 = sorted(set(W2)); assert len(W2) % 2 == 1 and set(W2) <= set(W)
    live = {q: live_levels(W, q, b) for q, b in f.items()}
    info = {}
    for e in divisors(n1):
        if e == 1: continue
        pr = powrem2(e)
        s = 0
        for w in W2: s ^= pr[w % e]
        fe = factor(e)
        lv = all(i in live[q] for q, i in fe.items())
        D = rank2([pr[w % e] for w in set(x % e for x in W)])
        mu = max((live[q].index(i) + 1) * (q - 1) for q, i in fe.items()) if lv else None
        info[e] = (lv, s == 0, D, mu)
    tot = sum((Fr(2, 2 ** D) for (lv, dg, D, mu) in info.values() if lv and dg), Fr(0))
    if tot > st['maxsum']: st['maxsum'] = tot; st['arg'] = (W, W2)
    a = f.get(3, 0)
    for e2 in divisors(n1):
        if e2 == 1 or e2 % 3 == 0: continue
        pr2 = powrem2(e2); K = max(pr2).bit_length() + 1
        rho = Fr(0)
        for i in range(1, a + 1):
            e = 3 ** i * e2
            lv, dg, D, mu = info[e]
            # (X) fibre formula, checked on every e (live or not)
            if st['X'] < st['Xcap']:
                val = 0
                cls = {}
                for w in W: cls.setdefault(w % 3 ** (i - 1), {}).setdefault(w % 3 ** i, []).append(pr2[w % e2])
                for r, ch in cls.items():
                    bs = [basis_of(v) for v in ch.values()]
                    val += sum(len(b) for b in bs)
                    if len(bs) == 3:
                        val -= len(intersect(intersect(bs[0], bs[1], K), bs[2], K))
                assert val == D, ('X fails', W, e, val, D)
                st['X'] += 1
            if not (lv and dg): continue
            l = live[3].index(i) + 1
            De2 = info[e2][2]
            act = {}
            for w in W2: act[w % 3 ** (i - 1)] = act.get(w % 3 ** (i - 1), 0) ^ pr2[w % e2]
            nact = sum(1 for v in act.values() if v)
            if not info[e2][1]:
                lp = sum(1 for i2 in range(1, i + 1) if info[3 ** i2 * e2][1])
                assert nact >= 3 ** (lp - 1)
                assert D >= max(2 * nact, De2 + nact), ('A fails', W, W2, e, D, De2, lp, nact)
                st['A'] += 1; st['Amin'] = min(st['Amin'], D - max(2 * 3 ** (lp - 1), De2 + 3 ** (lp - 1)))
            else:
                st['B'] += 1
                if nact:
                    assert nact >= 2 and D >= De2 + 1 + nact, ('B1 fails', W, W2, e, D, De2, nact)
                    st['B1'] = st.get('B1', 0) + 1
                mu2 = info[e2][3]
                v = D - mu2 - (2 * l - 1)
                if v < st['Bmin']: st['Bmin'] = v; st['Barg'] = (W, W2, e, D, mu2, l)
                rho += Fr(2, 2 ** D) / Fr(2, 2 ** mu2)
        if rho > st['rho']: st['rho'] = rho; st['rhoarg'] = (W, W2, e2)

def gen(n1, kind, rnd):
    f = factor(n1); ps = sorted(f); big = [p for p in ps if p >= 5]
    def near(W, cnt):
        W = set(W)
        for _ in range(cnt):
            x = rnd.choice(sorted(W)); q = rnd.choice(ps); j = rnd.randint(1, f[q])
            W.add((x + rnd.randrange(1, q) * (n1 // q ** j)) % n1)
        return W
    if kind == 0:      # odd number of cosets of H_q (q >= 5) close to one another in the 3-tree, then cheap liveness
        q = rnd.choice(big); W2 = set(); o = rnd.randrange(n1)
        for t in range(rnd.choice([1, 1, 3])):
            j = rnd.randint(1, f[3]); oo = (o + t * rnd.randrange(0, 3) * (n1 // 3 ** j)) % n1
            W2 ^= {(oo + s * (n1 // q)) % n1 for s in range(q)}
        if len(W2) % 2 == 0: W2 = {(o + s * (n1 // q)) % n1 for s in range(q)}
        W = near(W2, rnd.randint(2, 9))
    elif kind == 1:    # a full group of 3 with the same pattern, or the pattern plus a coset, in each child
        q = rnd.choice(big); j = rnd.randint(1, f[3]); o = rnd.randrange(n1)
        P = {(o + rnd.randrange(q) * (n1 // q)) % n1 for _ in range(rnd.randint(1, 2))}
        cos = {(o + s * (n1 // q)) % n1 for s in range(q)}
        W2 = set()
        for t in range(3):
            Pt = set(P) if rnd.random() < 0.6 else set(P) ^ cos
            W2 ^= {(x + t * (n1 // 3 ** j)) % n1 for x in Pt}
        if rnd.random() < 0.5:
            W2 ^= {(x + (n1 // 3 ** rnd.randint(1, f[3])) * rnd.randrange(1, 3)) % n1 for x in cos}
        if len(W2) % 2 == 0:
            W2 ^= cos
        if len(W2) % 2 == 0 or not W2: W2 = set(cos)
        W = near(W2, rnd.randint(0, 8))
    elif kind == 2:    # everything: W2 = W = odd union of cosets of several subgroups
        W2 = set()
        for _ in range(rnd.randint(1, 4)):
            p = rnd.choice(ps); o = rnd.randrange(n1); W2 ^= {(o + s * (n1 // p)) % n1 for s in range(p)}
        if len(W2) % 2 == 0 or not W2:
            p = rnd.choice(big); o = rnd.randrange(n1); W2 = {(o + s * (n1 // p)) % n1 for s in range(p)}
        W = near(W2, rnd.randint(0, 6))
    else:              # one point in every class modulo q (dangerous at q), spread over the 3-tree, plus liveness
        q = rnd.choice(big); W2 = {c + q * rnd.randrange(n1 // q) for c in range(q)}
        W = near(W2, rnd.randint(0, 8))
    return sorted(W), sorted(W2)

if __name__ == '__main__':
    reps = int(sys.argv[1]); rnd = random.Random(int(sys.argv[2]))
    mods = [int(x) for x in sys.argv[3].split(',')]
    for n1 in mods:
        st = {'maxsum': Fr(0), 'A': 0, 'Amin': 99, 'B': 0, 'Bmin': 99, 'arg': None, 'Barg': None, 'rho': Fr(0), 'rhoarg': None, 'X': 0, 'Xcap': 4000}
        for t in range(reps):
            W, W2 = gen(n1, t % 4, rnd)
            analyse(W, W2, n1, st)
        print("n'", n1, 'supports', reps, '| fibre formula checked', st['X'], '| max sum', st['maxsum'], '=%.4f' % float(st['maxsum']),
              '| (A) cases', st['A'], 'least slack', st['Amin'], '| (B) cases', st['B'], 'of them with an active class (B1)', st.get('B1', 0), '| least D - mu - (2l-1):', st['Bmin'], '| max rho', st['rho'], flush=True)
        print('    arg max sum', st['arg']); print('    arg (B)', st['Barg']); print('    arg rho', st['rhoarg'], flush=True)
