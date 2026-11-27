# First-order ranks modulo 2 on an odd Z_{n'}:  for a support W and an odd-size subset W2 of W (the points of odd
# multiplicity), for every e | n', e > 1:  live?  dangerous?  D_e(W) = F_2-rank of the X^w mod (2, Phi_e), w in W.
# Tests of the fibre formula's consequences (section 5 of even-result-2.md) for e = 3^i * e2, e2 > 1 prime to 3:
#   (A)  e live and dangerous, e2 NOT dangerous:  D_e >= max(2 * 3^(l'-1), D_{e2}(W) + 1),
#        l' = index of i among the levels i' >= 1 with 3^i' * e2 dangerous;
#   (B)  e live and dangerous, e2 dangerous: record the least value of D_e - D_{e2}(W) - l and of D_e - D_{e2}(W) - (2l - 1),
#        l = index of i among the live levels of 3;
#   and the sum over the live dangerous e of 2^(1 - D_e).
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import cyclo, divisors

def factor(n):
    f = {}; p = 2
    while n > 1:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    return f

_pr = {}
def powrem2(e):
    # list: x -> bitmask of X^x mod (2, Phi_e)
    if e in _pr: return _pr[e]
    phi = [c & 1 for c in cyclo(e)]; deg = len(phi) - 1
    low = sum(b << j for j, b in enumerate(phi[:-1]))
    out = []; cur = 1
    for x in range(e):
        out.append(cur)
        cur <<= 1
        if cur >> deg & 1: cur ^= (1 << deg) | low
    _pr[e] = out
    return out

def rank2(vs):
    basis = {}
    r = 0
    for v in vs:
        while v:
            h = v.bit_length() - 1
            if h in basis: v ^= basis[h]
            else: basis[h] = v; r += 1; break
    return r

def live_levels(W, q, b):
    out = []
    for i in range(1, b + 1):
        occ = {}
        for x in W: occ.setdefault(x % q ** (i - 1), set()).add(x % q ** i)
        if any(len(s) == q for s in occ.values()): out.append(i)
    return out

def analyse(W, W2, n1, st):
    f = factor(n1)
    live = {q: live_levels(W, q, b) for q, b in f.items()}
    info = {}
    for e in divisors(n1):
        if e == 1: continue
        pr = powrem2(e)
        s = 0
        for w in W2: s ^= pr[w % e]
        dang = (s == 0)
        fe = factor(e)
        lv = all(i in live[q] for q, i in fe.items())
        D = rank2([pr[w % e] for w in set(x % e for x in W)])
        info[e] = (lv, dang, D)
    tot = Fr(0)
    for e, (lv, dang, D) in info.items():
        if lv and dang: tot += Fr(2, 2 ** D)
    st['maxsum'] = max(st['maxsum'], tot)
    if tot == st['maxsum']: st['arg'] = (sorted(W), sorted(W2))
    a = f.get(3, 0)
    for e, (lv, dang, D) in info.items():
        i = 0
        while e % 3 ** (i + 1) == 0: i += 1
        e2 = e // 3 ** i
        if i == 0 or e2 == 1 or not (lv and dang): continue
        De2 = info[e2][2]
        l = live[3].index(i) + 1
        if not info[e2][1]:
            lp = sum(1 for i2 in range(1, i + 1) if info[3 ** i2 * e2][1])
            assert D >= max(2 * 3 ** (lp - 1), De2 + 1), ('A fails', sorted(W), sorted(W2), e, D, De2, lp)
            st['A'] += 1
            st['Amin'] = min(st['Amin'], D - max(2 * 3 ** (lp - 1), De2 + 1))
        else:
            st['B'] += 1
            v1 = D - De2 - l; v2 = D - De2 - (2 * l - 1)
            if v1 < st['Bmin_l']: st['Bmin_l'] = v1; st['Barg1'] = (sorted(W), sorted(W2), e)
            if v2 < st['Bmin_2l1']: st['Bmin_2l1'] = v2; st['Barg2'] = (sorted(W), sorted(W2), e)

def crt(res, mods):
    n = 1
    for m in mods: n *= m
    return next(x for x in range(n) if all(x % m == r % m for r, m in zip(res, mods)))

def gen(n1, kind, rnd):
    f = factor(n1); ps = sorted(f)
    if kind == 0:
        W = set(rnd.randrange(n1) for _ in range(rnd.randint(3, 16)))
    elif kind == 1:     # cosets of subgroups of prime order, plus a few points
        W = set()
        for _ in range(rnd.randint(1, 3)):
            p = rnd.choice(ps); o = rnd.randrange(n1); W |= {(o + t * (n1 // p)) % n1 for t in range(p)}
        W |= set(rnd.randrange(n1) for _ in range(rnd.randint(0, 6)))
    elif kind == 2:     # a coset, then points chosen to make levels live cheaply (few new residues)
        p = rnd.choice(ps); o = rnd.randrange(n1); W = {(o + t * (n1 // p)) % n1 for t in range(p)}
        for _ in range(rnd.randint(2, 10)):
            x = rnd.choice(sorted(W)); q = rnd.choice(ps); j = rnd.randint(1, f[q])
            W.add((x + rnd.randrange(1, q) * (n1 // q ** j)) % n1)
    else:               # product sets: residues modulo the prime powers chosen separately
        mods = [p ** f[p] for p in ps]
        sets = [rnd.sample(range(m), rnd.randint(1, min(m, 4))) for m in mods]
        W = set()
        import itertools
        for tup in itertools.product(*sets):
            if rnd.random() < 0.8: W.add(crt(tup, mods))
        if not W: W = {0}
    W = sorted(W)
    # W2: all of W if odd; else drop one; or a random odd subset; or a coset inside W if there is one
    c = rnd.random()
    if c < 0.5:
        W2 = list(W) if len(W) % 2 else W[:-1]
    else:
        k = rnd.randrange(1, len(W) + 1, 2) if len(W) > 1 else 1
        W2 = rnd.sample(W, k)
    return W, W2

if __name__ == '__main__':
    rnd = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    reps = int(sys.argv[1])
    for n1 in [15, 45, 105, 135, 225, 315, 525, 675, 945, 1155]:
        st = {'maxsum': Fr(0), 'A': 0, 'Amin': 99, 'B': 0, 'Bmin_l': 99, 'Bmin_2l1': 99, 'arg': None, 'Barg1': None, 'Barg2': None}
        for t in range(reps):
            W, W2 = gen(n1, t % 4, rnd)
            analyse(W, W2, n1, st)
        print("n'", n1, 'supports', reps, '| max sum', st['maxsum'], float(st['maxsum']), '| (A) cases', st['A'], 'least slack', st['Amin'],
              '| (B) cases', st['B'], 'least D_e - D_e2 - l:', st['Bmin_l'], 'least D_e - D_e2 - (2l-1):', st['Bmin_2l1'], flush=True)
        print('    arg max sum', st['arg']); print('    arg B(l)', st['Barg1']); print('    arg B(2l-1)', st['Barg2'], flush=True)
