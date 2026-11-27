"""For product groups with tree coordinates: for each set E containing 0, the affine subspaces
A_D = {g in F_2^E : every D-cube has  <kappa, E - 2g> = 0 mod 4}  for D in D2(E).
Statistics: the union bound  sum over DISTINCT nonempty A_D of 2^(-codim A_D)  (if < 1 a good g exists by counting),
and the exact fraction of good g.   usage: cover_stats.py "3;5" [maxshow]"""
import sys, itertools
spec = sys.argv[1]; maxshow = int(sys.argv[2]) if len(sys.argv) > 2 else 8
chains = [[1] + [int(t) for t in c.split(',')] for c in spec.split(';')]
sizes = [c[-1] for c in chains]; r = len(chains); N = 1
for s in sizes: N *= s
def coords(x):
    out = []
    for s in sizes: out.append(x % s); x //= s
    return out
C = [coords(x) for x in range(N)]
levels = list(itertools.product(*[range(len(c)) for c in chains]))
cubes = {}
for L in levels:
    pairs = []
    for i, e in enumerate(L):
        if e == 0: pairs.append([None]); continue
        m, m0 = chains[i][e], chains[i][e - 1]
        pairs.append([(u, v) for u in range(m) for v in range(u + 1, m) if u % m0 == v % m0])
    lst = []
    for choice in itertools.product(*pairs):
        P = Mi = 0
        for x in range(N):
            sgn = 1; inside = True
            for i, e in enumerate(L):
                if e == 0: continue
                c = C[x][i] % chains[i][e]
                if c == choice[i][0]: pass
                elif c == choice[i][1]: sgn = -sgn
                else: inside = False; break
            if inside:
                if sgn > 0: P |= 1 << x
                else: Mi |= 1 << x
        lst.append((P, Mi))
    cubes[L] = lst
pc = lambda v: bin(v).count('1')
def solve(rows):
    """rows: list of (mask, rhs) over F_2.  returns (rank, consistent, reduced-row-echelon key)"""
    basis = {}
    ok = True
    for m, b in rows:
        while m:
            h = m.bit_length() - 1
            if h in basis: m ^= basis[h][0]; b ^= basis[h][1]
            else: basis[h] = (m, b); break
        else:
            if b: ok = False
    # canonical reduced form
    keys = sorted(basis, reverse=True)
    red = {}
    for h in sorted(basis):
        m, b = basis[h]
        for h2 in sorted(red):
            if m >> h2 & 1 and h2 != h: m ^= red[h2][0]; b ^= red[h2][1]
        red[h] = (m, b)
    return len(basis), ok, tuple(sorted(red.values()))
worst = []; maxsum = 0; minfrac = 2; nE = 0
for E in range(1, 1 << N, 2):
    D2 = [L for L in levels if all(pc(E & (P | Mi)) % 2 == 0 for P, Mi in cubes[L])]
    if not D2: continue
    nE += 1
    subs = {}
    for L in D2:
        rows = [(E & (P | Mi), ((pc(E & P) - pc(E & Mi)) // 2) % 2) for P, Mi in cubes[L]]
        rk, ok, key = solve(rows)
        if ok: subs[key] = (rk, L)
    ub = sum(2.0 ** (-rk) for rk, L in subs.values())
    if ub > maxsum - 1e-12:
        if ub > maxsum + 1e-12: worst = []
        maxsum = ub
        if len(worst) < maxshow: worst.append(([x for x in range(N) if E >> x & 1], sorted((L, rk) for rk, L in subs.values())))
print(f'{spec}: sets with D2 nonempty: {nE}; largest union bound (distinct nonempty A_D): {maxsum}')
for w in worst: print('   ', w)
