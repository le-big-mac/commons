"""Referee: independent recomputation at particular prime pairs.
For every pattern outside L2 and a: the optimum and every category property are computed with mylp (own formulation, own exact
simplex, every answer certified by an exact primal-dual pair), and compared with what the published certificate says AT THAT PAIR:
  - the leaf of the certificate tree reached by the signs of the split factors at (p, q)  (a leaf 'empty' or '?' is an error);
  - its formula for the optimum, evaluated at (p, q), must equal my optimum;
  - the property of its category must hold according to my programmes (b: D < k; R: restricted optimum = optimum; T: optimum with
    f = 1 on P or Q equal to the optimum, M not a zero, (T2) violated; U: max of f on P\\0 or Q\\0 over the optimal face > 0, M a zero;
    N: D/k not an integer; H: D = pq or p^2 q with the zeros of M0 / M2 / M4, M a zero, (T2) violated);
  - with --basis: the stored bases themselves, solved exactly at (p, q) against my rows: primal and dual feasible, same value;
    second basis feasible with the same value and the stated property.
usage: recheck.py PIECE [--basis] p,q [p,q ...]     PIECE: a band, C3, Cp, fam2q (family p = 2), or 'direct' (no certificate: my categories only)"""
import sys, pickle, time
from collections import Counter
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, '/home/agent2/p3q2/referee2')
from mylp import *
args = sys.argv[1:]; piece = args[0]; WITH_BASIS = "--basis" in args; pts = [tuple(int(v) for v in a.split(",")) for a in args[1:] if not a.startswith("--")]
D_ = '/home/agent2/p3q2/referee2/orig/'
inside = {
 'A1a': lambda p, q: p >= 5 and p + 2 <= q and 2 * q < 4 * p - 5, 'A1b': lambda p, q: p >= 5 and 2 * p - 1 <= q < p * p - p + 1,
 'A2': lambda p, q: p >= 3 and p * p - p + 1 <= q < p * p - 1, 'B1': lambda p, q: p >= 5 and p * p + 1 <= q < p * p + p,
 'B2': lambda p, q: p >= 3 and p * p + p + 1 <= q < p**3 - p * p + p - 1, 'B3': lambda p, q: p >= 3 and p**3 - p * p + p <= q < p**3 - 1,
 'C3': lambda p, q: p >= 3 and q >= p**3 + 1, 'Ap1': lambda p, q: q >= 3 and q + 1 <= p < q * q - q + 1,
 'Ap2': lambda p, q: q >= 3 and q * q - q + 1 <= p < q * q - 1, 'Cp': lambda p, q: q >= 2 and p >= q * q + 1,
 'fam2q': lambda p, q: p == 2 and q >= 9, 'direct': lambda p, q: True}[piece]
res = None
if piece != 'direct':
    res = pickle.load(open(D_ + {'C3': 'region_C3', 'Cp': 'region_Cp', 'fam2q': 'family_2_q'}.get(piece, 'split_' + piece) + '.pkl', 'rb'))
P_, Q_, T_ = sp.symbols('p q t'); PARSED = {}
def formula(leaf, p, q):
    if id(leaf) not in PARSED: PARSED[id(leaf)] = sp.sympify(leaf['v'], locals={'p': P_, 'q': Q_, 't': T_})
    val = PARSED[id(leaf)].subs({P_: p, Q_: q, T_: q}); return Fr(int(val.p), int(val.q))
FAC = {}
def fsign(fs, p, q):
    if fs not in FAC: FAC[fs] = sp.sympify(fs, locals={'p': P_, 'q': Q_})
    return FAC[fs].subs({P_: p, Q_: q})
def basic(R, rhs, cost, basis):
    """exact basic solution of a stored basis at this pair: (x, reduced costs) or None"""
    m = len(R); col = lambda j: [R[i][j] for i in range(m)] if j < n else [1 if i == j - n else 0 for i in range(m)]
    if len(basis) != m or len(set(basis)) != m: return None
    B = [[col(j)[i] for j in basis] for i in range(m)]
    xb = solve_square(B, rhs); y = solve_square([[col(basis[k])[i] for i in range(m)] for k in range(m)], [cost[j] if j < n else 0 for j in basis])
    if xb is None or y is None: return None
    x = [Fr(0)] * n
    for kk, j in enumerate(basis):
        if j < n: x[j] = xb[kk]
        elif xb[kk] != 0: return None
    red = [cost[j] - sum(y[i] * R[i][j] for i in range(m)) for j in range(n)]
    return x, red
tall = time.time()
for (p, q) in pts:
    assert inside(p, q) or "--outside" in args, (piece, p, q); assert sp.isprime(p) and sp.isprime(q) and p != q
    pr = Prog(p, q); cnt = Counter(); bad = []; nchk = 0; t0 = time.time(); certcats = Counter(); tuh_t2 = 0
    for Z in patterns():
        if (1, 0) not in Z and (0, 1) not in Z: cnt['L2'] += 1; continue
        t2, orph = t2_orph(Z)
        if t2 and not orph: cnt['a'] += 1; continue
        cat0, v, prop = pr.category(Z); cnt[cat0.split(':')[0]] += 1; cnt[cat0] += (':' in cat0)
        if cat0[0] in 'TUH' and t2: tuh_t2 += 1
        if cat0 == 'LEFT': bad.append((sorted(Z), 'my computation leaves this pattern open'))
        if res is None: continue
        leaf = res[Z]
        while leaf['cat'] == 'split': leaf = leaf['pos'] if fsign(leaf['factor'], p, q) >= 0 else leaf['neg']
        nchk += 1; c = leaf['cat']; kind = leaf.get('kind'); certcats[c] += 1
        if c in ('empty', '?', 'empty?', 'L2', 'a', 'retry'): bad.append((sorted(Z), 'leaf ' + c)); continue
        if formula(leaf, p, q) != v: bad.append((sorted(Z), c, 'optimum', str(formula(leaf, p, q)), str(v))); continue
        top = TOP in Z
        ok = {'b': lambda: prop('b'), 'R': lambda: prop(kind), 'T': lambda: prop(kind) and not top and not t2, 'U': lambda: prop(kind) and top and not (t2 and not orph),
              'N': lambda: prop('N'), 'H': lambda: prop(kind) and top and not t2}[c]()
        if not ok: bad.append((sorted(Z), c, kind, 'property fails'))
        if WITH_BASIS:
            R, rhs = pr.rows(Z); bs = basic(R, rhs, pr.tot, leaf['basis'])
            if bs is None or min(bs[0]) < 0 or min(bs[1]) < 0 or sum(pr.tot[j] * bs[0][j] for j in range(n)) != v: bad.append((sorted(Z), c, 'stored basis not optimal at this pair')); continue
            if c in ('R', 'T', 'U'):
                R2, rhs2, cost2 = R, rhs, pr.tot
                if c == 'T': R2 = R + [pr.e(pr.Pc if kind == 'TP' else pr.Qc)]; rhs2 = rhs + [1]
                if c == 'U': R2 = R + [pr.tot]; rhs2 = rhs + [v]; cost2 = [-t for t in pr.e(pr.Pc if kind == 'UP' else pr.Qc)]
                b2 = basic(R2, rhs2, cost2, leaf['basis2'])
                if b2 is None or min(b2[0]) < 0 or sum(pr.tot[j] * b2[0][j] for j in range(n)) != v: bad.append((sorted(Z), c, kind, 'second basis: not a feasible point with the optimal value')); continue
                x2 = b2[0]
                good = (all(x2[j] == 0 for j in (pr.outp if kind == 'Rp' else pr.outq)) if c == 'R' else x2[pr.Pc if kind == 'TP' else pr.Qc] == 1 if c == 'T' else x2[pr.Pc if kind == 'UP' else pr.Qc] > 0)
                if not good: bad.append((sorted(Z), c, kind, 'second basis: property fails'))
    mine = ", ".join(f"{k} {cnt[k]}" for k in ('L2', 'a', 'b', 'N', 'R', 'T', 'U', 'H')) + f"; H: M0 {cnt['H:M0']}, M2 {cnt['H:M2']}, M4 {cnt['H:M4']}, left {cnt['LEFT']}; T,U,H with (T2): {tuh_t2}"
    print(f"{piece} ({p}, {q}): mine [{mine}]  certificate leaves {dict(sorted(certcats.items()))}  checks {nchk}  MISMATCHES {len(bad)}   [{time.time() - t0:.0f} s]", flush=True)
    for b_ in bad[:8]: print("     ", str(b_)[:400], flush=True)
