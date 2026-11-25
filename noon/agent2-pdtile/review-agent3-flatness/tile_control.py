"""Positive control for the three consequences of Proposition 3 as implemented in agent2's lp.py / sat.py,
at moduli where flatness.md relies on the "full" model alone (agent3 / Yonder, for the review).

For explicit tiles A of Z_M (Coven-Meyerowitz standard tiles, their complements, and tiles obtained by sliding the
elements of A along a period of the complement), and for patterns Z0 inside Z_A with D+(Z0) = |A| (Z_A itself and
inclusion-minimal ones reached by deleting orders in random sequence), compute with agent2's own functions
   E  = Setup.forbidden_orders(Z0),   f = Setup.complement(Z0),   caps ub[D] exactly as sat.search does,
and test on the set A, with my own code:
   (i) no two elements of A differ by an element whose order is in E;
  (ii) no residue class mod D holds more than ub[D] elements of A;
 (iii) sum over a in A of f(order(z - a)) = 1 for every z.
A failure would mean the full model can cut off a genuine set.  No solver is involved.
Usage: tile_control.py M [M ...] [sabotage=E|cap|f]
(the sabotage options spoil one ingredient on purpose, to show that the test can fail)"""
import sys, random, itertools, time
from math import gcd
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat")
from lp import Setup, divisors
from cyclo_exact import divides                      # my own exact test of Phi_d | A(X)

def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def cyclo_in(s, t, M):
    """coefficients of Phi_s(X^t) mod X^M - 1 for a prime power s = p^a: 1 + Y + ... + Y^(p-1), Y = X^(t p^(a-1))"""
    (p, a), = factor(s).items()
    v = [0] * M
    for i in range(p): v[(i * t * p ** (a - 1)) % M] += 1
    return v

def mulmod(u, v, M):
    w = [0] * M
    for i, x in enumerate(u):
        if x:
            for j, y in enumerate(v):
                if y: w[(i + j) % M] += x * y
    return w

def standard_pair(M, S):
    """Coven-Meyerowitz tile with prime-power zero set S, and its complement, both inside Z_M"""
    fm = factor(M); pps = [p ** a for p in fm for a in range(1, fm[p] + 1)]
    out = []
    for part in (S, [s for s in pps if s not in S]):
        v = [1] + [0] * (M - 1)
        for s in part:
            p = next(iter(factor(s))); t = M // p ** fm[p]
            v = mulmod(v, cyclo_in(s, t, M), M)
        assert set(v) <= {0, 1}, "not a set"
        out.append([i for i in range(M) if v[i]])
    A, B = out
    assert sorted((a + b) % M for a in A for b in B) == list(range(M)), "not a tiling"
    return A, B

def periods(B, M):
    Bs = set(B)
    return [g for g in divisors(M) if g < M and all((b + g) % M in Bs for b in B)]

def control(M, rng, max_n=700, tiles_per_M=40):
    S = Setup(M); fm = factor(M); pps = [p ** a for p in fm for a in range(1, fm[p] + 1)]
    orders = [d for d in divisors(M) if d > 1]
    order = lambda x: M // gcd(x, M)
    capcache = {}
    def caps(E):
        key = frozenset(E)
        if key not in capcache:
            ub = {}
            for D in divisors(M):
                mm = M // D
                if mm > 1:
                    allowed = [d for d in divisors(mm) if d > 1 and d not in key]
                    ub[D] = int(Setup(mm).Dplus(allowed)[0]) if allowed else 1
            capcache[key] = ub
        return capcache[key]
    seen = set(); stats = dict(tiles=0, patterns=0, minimal=0, nonempty_E=0, binding_caps=0, fails=0, slid=0, sizes=set())
    subsets = [tuple(c) for r in range(len(pps) + 1) for c in itertools.combinations(pps, r)]
    rng.shuffle(subsets)
    for Sset in subsets:
        if stats["tiles"] >= tiles_per_M: break
        A0, B0 = standard_pair(M, list(Sset))
        cands = []
        for A, B in ((A0, B0), (B0, A0)):
            cands.append((A, False))
            gs = periods(B, M)
            if gs:                                     # slide each element of A by a random multiple of a period of B
                g = rng.choice(gs)
                A2 = sorted({(a + g * rng.randrange(M // g)) % M for a in A})
                if len(A2) == len(A) and sorted((a + b) % M for a in A2 for b in B) == list(range(M)):
                    a0 = A2[0]; cands.append((sorted((a - a0) % M for a in A2), True))
        for A, slid in cands:
            n = len(A)
            if n < 2 or n > max_n or n == M or tuple(A) in seen: continue
            seen.add(tuple(A))
            ZA = [d for d in orders if divides(d, A, M)]
            assert S.Dplus(ZA)[0] == n, ("a tile that does not pd-tile?", M, A)      # Prop. 1(ii), positive direction
            diff_orders = {order(a - b) for a, b in itertools.combinations(A, 2)}
            pats = {tuple(ZA)}
            for _ in range(3):                         # inclusion-minimal patterns of size n inside Z_A
                Z = list(ZA); seq = Z[:]; rng.shuffle(seq)
                for d in seq:
                    Z2 = [e for e in Z if e != d]
                    if S.Dplus(Z2)[0] == n: Z = Z2
                pats.add(tuple(Z)); 
            stats["tiles"] += 1; stats["slid"] += slid; stats["sizes"].add(n)
            for Z in pats:
                stats["patterns"] += 1; stats["minimal"] += (Z != tuple(ZA)) or all(S.Dplus([e for e in Z if e != d])[0] < n for d in Z)
                E = S.forbidden_orders(list(Z)); f = S.complement(list(Z)); ub = caps(E)
                if SABOTAGE == "E":                      # negative controls: each must make the test fail
                    E = list(E) + [sorted(diff_orders)[0]]
                elif SABOTAGE == "cap":
                    ub = dict(ub); D0 = max(ub); ub[D0] = 0
                elif SABOTAGE == "f":
                    f = dict(f); e0 = max(e for e in f if f[e] != 0); f[e0] = f[e0] * 2
                stats["nonempty_E"] += bool(E)
                # the kind of pattern, as flatness.md classifies them: only T1-short and T2-open ones are ever searched
                Zs = set(Z); k = 1
                for s_ in pps:
                    if s_ in Zs: k *= next(iter(factor(s_)))
                closed = all(d in Zs for d in orders if len(factor(d)) > 1 and all(p ** a in Zs for p, a in factor(d).items()))
                kind = "safe" if (k == n and closed) else "T2-open" if k == n else "T1-short" if n % k == 0 else "impossible"
                stats[kind] = stats.get(kind, 0) + 1
                bad = []
                if diff_orders & set(E): bad.append(("forbidden difference", sorted(diff_orders & set(E))))
                for D, cap in ub.items():
                    cnt = {}
                    for a in A: cnt[a % D] = cnt.get(a % D, 0) + 1
                    mx = max(cnt.values())
                    if mx > cap: bad.append(("cap", D, cap, mx))
                    if cap < min(n, M // D) and mx == cap: stats["binding_caps"] += 1
                if any(sum(f[order(z - a)] for a in A) != 1 for z in range(M)): bad.append(("covering equation",))
                if bad:
                    stats["fails"] += 1; print("FAIL", M, "A =", A, "Z0 =", Z, bad, flush=True)
    return stats

SABOTAGE = next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("sabotage=")), None)
rng = random.Random(20261119)
for M in [int(x) for x in sys.argv[1:] if x.isdigit()]:
    t0 = time.time(); st = control(M, rng)
    print(f"M={M} ({'·'.join(f'{p}^{a}' if a > 1 else str(p) for p, a in factor(M).items())}): tiles {st['tiles']} (of which slid {st['slid']}), sizes {sorted(st['sizes'])}; "
          f"patterns {st['patterns']} ({st['minimal']} inclusion-minimal; safe {st.get('safe', 0)}, T1-short {st.get('T1-short', 0)}, T2-open {st.get('T2-open', 0)}; {st['nonempty_E']} with forbidden orders); "
          f"caps met with equality below the trivial bound {st['binding_caps']} times; FAILURES {st['fails']}  [{time.time() - t0:.0f} s]", flush=True)
