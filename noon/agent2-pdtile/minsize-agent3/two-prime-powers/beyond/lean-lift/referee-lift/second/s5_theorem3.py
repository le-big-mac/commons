"""The instance's Theorem 3 (signs for n = p r q^b, three different odd primes), how far the referee went: its Lemma D (balanced signing
by Euler circuits), Lemma E (candidates; at most one additive modulo q) and the signing of Theorem 3, implemented from the text of
sign-lemma-result.md (sections 2 and 4), not from the instance's programs, and tested with exact arithmetic.
(1) Lemma D and the claims inside the proof of Lemma E, for EVERY nonempty set O of cells of the grids 3x3, 3x4, 3x5, 4x4 and q = 3, 5, 7:
    row sums, column sums and total of eps in {-1, 0, 1}; every candidate satisfies (i), (ii), (iii); at most one candidate is additive mod q.
(2) Theorem 3: random multisets on Z_n; the signed mask is divisible by no Phi_d, d | n (integer remainders).
usage: python -I -B s5_theorem3.py [small]"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift/second')
import itertools, random
import numpy as np
from cyc import divisors, tables
rnd = random.Random(33)
def lemma_D(O, nx, ny):
    """O: list of cells (x, y).  Returns {cell: +-1} with all row sums, column sums and the total in {-1, 0, 1} (the proof's construction)."""
    edges = [(('x', x), ('y', y), (x, y)) for (x, y) in O]
    degx = {}; degy = {}
    for x, y in O: degx[x] = degx.get(x, 0) + 1; degy[y] = degy.get(y, 0) + 1
    oddy = [y for y in degy if degy[y] % 2]; oddx = [x for x in degx if degx[x] % 2]
    for y in oddy: edges.append((('x0',), ('y', y), None))
    for x in oddx: edges.append((('x', x), ('y0',), None))
    assert len(oddx) % 2 == len(oddy) % 2 == len(O) % 2
    if len(oddy) % 2: edges.append((('x0',), ('y0',), None))
    adj = {}
    for i, (u, v, _) in enumerate(edges): adj.setdefault(u, []).append((i, v)); adj.setdefault(v, []).append((i, u))
    assert all(len(a) % 2 == 0 for a in adj.values())
    used = [False] * len(edges); sign = [0] * len(edges)
    for start in list(adj):
        if all(used[i] for i, _ in adj[start]): continue
        # Hierholzer: an Euler circuit of the component of start, as a list of edge indices
        stack = [(start, None)]; circuit = []
        ptr = {}
        while stack:
            u, ein = stack[-1]; a = adj[u]; j = ptr.get(u, 0)
            while j < len(a) and used[a[j][0]]: j += 1
            ptr[u] = j
            if j == len(a):
                stack.pop()
                if ein is not None: circuit.append(ein)
            else:
                i, v = a[j]; used[i] = True; stack.append((v, i))
        assert len(circuit) % 2 == 0
        for h, i in enumerate(circuit): sign[i] = 1 if h % 2 == 0 else -1
        # consecutive edges of the circuit (cyclically) share a vertex: checked through the vertex sums below
    vs = {}
    for (u, v, _), s in zip(edges, sign): vs[u] = vs.get(u, 0) + s; vs[v] = vs.get(v, 0) + s
    assert all(t == 0 for t in vs.values()), 'vertex sums not 0'
    return {c: s for (u, v, c), s in zip(edges, sign) if c is not None}
def flip(eps, e):
    t = dict(eps); t[e] = -t[e]; return t
def matrix(tau, nx, ny):
    Mx = np.zeros((nx, ny), dtype=np.int64)
    for (x, y), s in tau.items(): Mx[x, y] = s
    return Mx
def additive(Mx, q): return not ((Mx - Mx[:, :1] - Mx[:1, :] + Mx[0, 0]) % q).any()
def props(Mx, q):
    r = Mx.sum(axis=1) % q; c = Mx.sum(axis=0) % q
    return (Mx.sum() % q != 0, len(set(r.tolist())) > 1, len(set(c.tolist())) > 1, not additive(Mx, q))
def lemma_E(O, nx, ny, q, check=None):
    eps = lemma_D(O, nx, ny); Mx = matrix(eps, nx, ny)
    assert all(abs(v) <= 1 for v in Mx.sum(axis=1)) and all(abs(v) <= 1 for v in Mx.sum(axis=0)) and abs(Mx.sum()) <= 1
    sigma = int(Mx.sum())
    if len(O) % 2:
        assert sigma in (1, -1)
        cands = [dict(eps)] + [flip(eps, e) for e in O if eps[e] == sigma]
    else:
        assert sigma == 0
        cands = [flip(eps, e) for e in O]
    assert len(cands) >= 2
    P = [props(matrix(t, nx, ny), q) for t in cands]
    assert all(pr[0] and pr[1] and pr[2] for pr in P), ('a candidate fails (i)-(iii)', O, q)
    assert sum(1 for pr in P if not pr[3]) <= 1, ('two additive candidates', O, q)
    if check is not None: check['sets'] += 1; check['candidates'] += len(cands); check['with one additive candidate'] += any(not pr[3] for pr in P)
    return next(t for t, pr in zip(cands, P) if pr[3])
def give(idxs, total, sg):
    k = len(idxs); assert abs(total) <= k and (k - total) % 2 == 0
    e = 1 if total >= 0 else -1
    for j, ix in enumerate(idxs): sg[ix] = e if j < abs(total) else (1 if (j - abs(total)) % 2 == 0 else -1)
def theorem3_signs(B, p, r, q):
    cells = {}
    for j, x in enumerate(B): cells.setdefault((x % p, x % r), []).append(j)
    O = [c for c in cells if len(cells[c]) % 2]; sg = [0] * len(B)
    if O:
        tau = lemma_E(O, p, r, q)
        for c, js in cells.items(): give(js, tau[c] if c in tau else 0, sg)
    else:
        c0 = next(iter(cells))
        for c, js in cells.items(): give(js, 2 if c == c0 else 0, sg)
    return sg
def good(B, sg, n):
    T = tables(n); idx = np.array(B); w = np.array(sg)
    return all((t[idx] * w[:, None]).sum(axis=0).any() for t in T.values())
def rand_multiset(n):
    rr = rnd.random()
    if rr < 0.35: return sorted(rnd.randrange(n) for _ in range(rnd.randint(1, 14)))
    if rr < 0.5: return sorted(rnd.sample(range(n), rnd.randint(1, min(n, 60))))
    el = []
    for _ in range(rnd.randint(1, 4)):
        c = rnd.choice(divisors(n)); x0 = rnd.randrange(n); el += [(x0 + c * j) % n for j in range(n // c)]
    for _ in range(rnd.randint(0, 3)): el.append(rnd.randrange(n))
    return sorted(el)
if __name__ == '__main__':
    small = len(sys.argv) > 1
    print('(1) Lemma D and the inner claims of Lemma E, every nonempty set of cells')
    for nx, ny in ([(3, 3)] if small else [(3, 3), (3, 4), (3, 5), (4, 4)]):
        allc = [(x, y) for x in range(nx) for y in range(ny)]
        for q in (3, 5, 7):
            st = {'sets': 0, 'candidates': 0, 'with one additive candidate': 0}
            for mask in range(1, 1 << len(allc)):
                lemma_E([c for i, c in enumerate(allc) if mask >> i & 1], nx, ny, q, st)
            print(f'   grid {nx}x{ny}, q = {q}: {st}; no assertion failed', flush=True)
    print('(2) Theorem 3, the signing: random multisets')
    tot = 0; bad = []; allplus = 0
    CASES = [(3, 5, 7, 1, 1500), (3, 7, 5, 1, 1500), (5, 7, 3, 1, 1500), (3, 5, 11, 1, 800), (5, 11, 3, 1, 800), (3, 5, 13, 1, 600), (5, 7, 3, 2, 800), (3, 7, 5, 2, 600),
             (3, 5, 7, 2, 500), (5, 7, 3, 3, 400), (7, 11, 13, 1, 300), (3, 11, 5, 2, 300), (3, 5, 7, 0, 800), (5, 7, 3, 0, 800)]
    if small: CASES = [(3, 5, 7, 1, 200), (5, 7, 3, 2, 100)]
    for p, r, q, b, Tn in CASES:
        n = p * r * q ** b; nb = 0; ap = 0
        for _ in range(Tn):
            B = rand_multiset(n); sg = theorem3_signs(B, p, r, q)
            assert all(s in (1, -1) for s in sg)
            if not good(B, sg, n): nb += 1; bad.append((n, p, r, q, B))
            ap += good(B, [1] * len(B), n)
        tot += Tn; allplus += ap
        print(f'   n = {n} = {p}*{r}*{q}^{b}: {Tn} random multisets; signed mask divisible by some Phi_d: {nb}; (all signs + is good for {ap})', flush=True)
    print(f'TOTAL {tot} multisets; failures of the signing: {len(bad)} {bad[:2]}; all signs + good for {allplus}')
