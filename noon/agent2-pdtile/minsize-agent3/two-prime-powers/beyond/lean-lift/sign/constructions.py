"""Constructive signings and exact verification.

  two_primes(B, p, a, q, b)   n = p^a q^b  (b = 0 allowed): the 'path in the p-tree' construction (Theorem 2 of the result file)
  three_primes(B, p, r, q, b) n = p r q^b:                  the 'balanced signing of a bipartite graph' construction (Theorem 3)
  good(n, S)                  exact test: the signed mask S (list of n integers) is divisible by no Phi_d, d | n
                              (remainders of integer polynomials modulo Phi_d, exact integer arithmetic)

A multiset B is a list of residues (with repetition).  A signing is returned as the vector S of signed multiplicities.
Run as a script: tests (exhaustive for small n, random and structured sets for larger n).   usage: constructions.py [quick]"""
import sys, itertools, random
from functools import lru_cache
import numpy as np
from sympy import Poly, cyclotomic_poly, symbols, ZZ, factorint
X = symbols('X')

@lru_cache(maxsize=None)
def remainder_maps(n):
    out = {}
    for d in range(1, n + 1):
        if n % d: continue
        phi = Poly(cyclotomic_poly(d, X), X, domain=ZZ); deg = phi.degree()
        R = np.zeros((deg, n), dtype=object)
        # X^i mod Phi_d by repeated multiplication by X (exact Python integers)
        c = [0] * deg; c[0] = 1 if deg > 0 else 0
        coeffs = [int(t) for t in phi.all_coeffs()[::-1]]          # low to high, monic
        cur = [1] + [0] * (deg - 1)
        for i in range(n):
            for j in range(deg): R[j, i] = cur[j]
            top = cur[-1]; cur = [0] + cur[:-1]
            if top:
                for j in range(deg): cur[j] -= top * coeffs[j]
        out[d] = R
    return out

def bad_divisors(n, S):
    v = np.array(S, dtype=object)
    return [d for d, R in remainder_maps(n).items() if not any(int(t) != 0 for t in R.dot(v))]

def good(n, S): return not bad_divisors(n, S)

def alternating(count, total):
    """signs for `count` copies summing to `total` in {0, 1, -1, 2} (parity must fit)"""
    if total == 2: return [1, 1] + [(-1) ** (i + 1) for i in range(count - 2)]
    if total == 0: return [(-1) ** i for i in range(count)]
    return [total * (-1) ** i for i in range(count)]          # total = +-1, count odd

def two_primes(B, p, a, q, b):
    n = p ** a * q ** b; pa = p ** a
    B = sorted(x % n for x in B)
    ustar = B[0] % pa
    def depth(x):
        u = x % pa; e = 0
        while e < a and (u - ustar) % p ** (e + 1) == 0: e += 1
        return e
    blocks = {}                                   # key (level e, class c mod p^e) for off-path subtrees; ('leaf',) for the leaf
    for idx, x in enumerate(B):
        de = depth(x)
        key = ('leaf',) if de == a else (de + 1, (x % pa) % p ** (de + 1))
        blocks.setdefault(key, []).append(idx)
    sign = [0] * len(B)
    leaf = blocks[('leaf',)]
    t = 1 if len(leaf) % 2 else 2
    for i, sg in zip(leaf, alternating(len(leaf), t)): sign[i] = sg
    for e in range(a, 0, -1):
        sib = [k for k in blocks if k[0] == e]
        odd = [k for k in sib if len(blocks[k]) % 2]; even = [k for k in sib if len(blocks[k]) % 2 == 0]
        eta = {}
        kk = len(odd)
        for j, k in enumerate(odd[: kk - kk % 2]): eta[k] = 1 if j % 2 == 0 else -1
        if kk % 2:
            e0 = 1 if t == 1 else -1                 # keeps t in {1, 2}
            assert (t + e0) % q != 0
            eta[odd[-1]] = e0; t += e0
        for k in even:
            for i, sg in zip(blocks[k], alternating(len(blocks[k]), 0)): sign[i] = sg
        for k in odd:
            for i, sg in zip(blocks[k], alternating(len(blocks[k]), eta[k])): sign[i] = sg
    S = [0] * n
    for x, sg in zip(B, sign): S[x] += sg
    return S

def balanced_signing(edges):
    """edges: list of (x, y) (two vertex classes, labels need not be disjoint).  Returns signs +-1 with every vertex sum and the total
    sum in {-1, 0, 1}  (Euler circuits of the graph with two auxiliary vertices)."""
    E = [(('x', x), ('y', y)) for x, y in edges]
    deg = {}
    for u, v in E:
        deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
    x0, y0 = ('x', '*'), ('y', '*')
    extra = []
    for v, dg in deg.items():
        if dg % 2: extra.append((x0, v) if v[0] == 'y' else (v, y0))
    if sum(1 for e in extra if e[0] == x0) % 2: extra.append((x0, y0))
    allE = E + extra
    adj = {}
    for i, (u, v) in enumerate(allE):
        adj.setdefault(u, []).append((i, v)); adj.setdefault(v, []).append((i, u))
    used = [False] * len(allE); sign = [0] * len(allE)
    for start in list(adj):
        if all(used[i] for i, _ in adj[start]): continue
        # Hierholzer: circuit as a sequence of edge indices
        stack = [(start, None)]; circuit = []
        ptr = {}
        while stack:
            v, ein = stack[-1]
            lst = adj[v]; k = ptr.get(v, 0)
            while k < len(lst) and used[lst[k][0]]: k += 1
            ptr[v] = k
            if k == len(lst):
                stack.pop()
                if ein is not None: circuit.append(ein)
            else:
                i, w = lst[k]; used[i] = True; stack.append((w, i))
        assert len(circuit) % 2 == 0
        for j, i in enumerate(circuit): sign[i] = 1 if j % 2 == 0 else -1
    eps = sign[: len(E)]
    return eps

def lemma2d(cells):
    """cells: nonempty list of distinct (x, y).  Signs as in Lemma 2D: balanced; if the number of cells is even, one -1 turned to +1."""
    eps = balanced_signing(cells)
    if len(cells) % 2 == 0:
        i = eps.index(-1); eps[i] = 1
    return eps

def additive_mod(cells, eps, xs, ys, q):
    """is the matrix (eps on the cells, 0 elsewhere) on the grid xs x ys of the form alpha_x + beta_y modulo q ?"""
    s = {c: e for c, e in zip(cells, eps)}
    x0, y0 = xs[0], ys[0]
    g = lambda x, y: s.get((x, y), 0)
    return all((g(x, y) - g(x0, y) - g(x, y0) + g(x0, y0)) % q == 0 for x in xs for y in ys)

def lemma_grid(cells, xs, ys, q):
    """Lemma E of the result file: a signing of the cells whose total is nonzero mod q, whose row sums and whose column sums are
    not all congruent mod q, and which is not additive mod q on the grid xs x ys.
    Candidates: |cells| odd: the balanced signing and its flips at cells whose sign equals the total; |cells| even: all single flips.
    The first candidate that is not additive mod q is returned (the proof shows that at most one candidate is additive)."""
    eps = balanced_signing(cells); sig = sum(eps)
    if len(cells) % 2: cands = [eps] + [eps[:i] + [-eps[i]] + eps[i + 1:] for i in range(len(eps)) if eps[i] == sig]
    else: cands = [eps[:i] + [-eps[i]] + eps[i + 1:] for i in range(len(eps))]
    assert len(cands) >= 2 or len(cells) == 1
    for c in cands:
        if not additive_mod(cells, c, xs, ys, q): return c
    raise AssertionError('no candidate')

def three_primes(B, p, r, q, b):
    n = p * r * q ** b
    B = sorted(x % n for x in B)
    cellidx = {}
    for idx, x in enumerate(B): cellidx.setdefault((x % p, x % r), []).append(idx)
    odd = sorted(c for c, l in cellidx.items() if len(l) % 2)
    target = {c: 0 for c in cellidx}
    if odd:
        for c, e in zip(odd, lemma_grid(odd, list(range(p)), list(range(r)), q)): target[c] = e
    else:
        target[sorted(cellidx)[0]] = 2
    sign = [0] * len(B)
    for c, l in cellidx.items():
        for i, sg in zip(l, alternating(len(l), target[c])): sign[i] = sg
    S = [0] * n
    for x, sg in zip(B, sign): S[x] += sg
    return S

def check_lemma2d(nx, ny):
    """exhaustive: every nonempty set of cells of an nx x ny grid; conditions (1)-(4) of Lemma 2D"""
    cells_all = [(x, y) for x in range(nx) for y in range(ny)]; bad = 0; tot = 0
    for mask in range(1, 1 << (nx * ny)):
        cells = [c for i, c in enumerate(cells_all) if mask >> i & 1]; tot += 1
        eps = lemma2d(cells)
        s = [[0] * ny for _ in range(nx)]
        for (x, y), e in zip(cells, eps): s[x][y] = e
        rho = [sum(row) for row in s]; gam = [sum(s[x][y] for x in range(nx)) for y in range(ny)]; sig = sum(rho)
        c1 = abs(sig) in (1, 2)
        c2 = any(abs(u - v) in (1, 2) for u in rho for v in rho)
        c3 = any(abs(u - v) in (1, 2) for u in gam for v in gam)
        c4 = any(s[x][y] - s[x2][y] - s[x][y2] + s[x2][y2] != 0 for x in range(nx) for x2 in range(x) for y in range(ny) for y2 in range(y))
        if not (c1 and c2 and c3 and c4): bad += 1
    return tot, bad

def check_lemma_grid(nx, ny, q):
    """exhaustive: every nonempty set of cells of an nx x ny grid; the four conditions of Lemma E modulo q"""
    cells_all = [(x, y) for x in range(nx) for y in range(ny)]; bad = 0; tot = 0
    for mask in range(1, 1 << (nx * ny)):
        cells = [c for i, c in enumerate(cells_all) if mask >> i & 1]; tot += 1
        eps = lemma_grid(cells, list(range(nx)), list(range(ny)), q)
        s = [[0] * ny for _ in range(nx)]
        for (x, y), e in zip(cells, eps): s[x][y] = e
        rho = [sum(row) for row in s]; gam = [sum(s[x][y] for x in range(nx)) for y in range(ny)]; sig = sum(rho)
        ok = sig % q != 0 and len({v % q for v in rho}) > 1 and len({v % q for v in gam}) > 1 and \
             any((s[x][y] - s[x2][y] - s[x][y2] + s[x2][y2]) % q for x in range(nx) for x2 in range(x) for y in range(ny) for y2 in range(y))
        bad += (not ok)
    return tot, bad

def digits_missing(n, support):
    """the hypothesis of Proposition 4: for every prime p | n and every e <= v_p(n) the digit floor((x mod p^e) / p^(e-1)) misses a value"""
    for p, a in factorint(n).items():
        for e in range(1, a + 1):
            if len({(x % p ** e) // p ** (e - 1) for x in support}) == p: return False
    return True

def structured_sets(n, rng, count):
    """unions of cosets of subgroups, with a few points added or removed; and plain random sets; and multisets"""
    divs = [d for d in range(1, n + 1) if n % d == 0]
    for _ in range(count):
        kind = rng.randrange(4)
        if kind == 0:
            k = rng.randrange(1, min(n, 40) + 1); yield rng.sample(range(n), k)
        elif kind == 1:
            S = set()
            for _ in range(rng.randrange(1, 4)):
                d = rng.choice(divs[1:]); c = rng.randrange(n); S ^= {(c + j * (n // d)) % n for j in range(d)}
            for _ in range(rng.randrange(0, 3)): S ^= {rng.randrange(n)}
            if S: yield sorted(S)
        elif kind == 2:
            S = []
            for _ in range(rng.randrange(1, 4)):
                d = rng.choice(divs[1:]); c = rng.randrange(n); S += [(c + j * (n // d)) % n for j in range(d)]
            for _ in range(rng.randrange(0, 3)): S.append(rng.randrange(n))
            yield S                                   # a multiset
        else:
            k = rng.randrange(1, 12); yield [rng.randrange(n) for _ in range(k)]   # a small multiset

if __name__ == '__main__':
    # usage: constructions.py PART     PART in lemmas, prop4, t2small, t2a, t2b, t2rand, t3a, t3b   (each part runs a few minutes at most)
    part = sys.argv[1] if len(sys.argv) > 1 else 'lemmas'
    rng = random.Random(20261126 + sum(map(ord, part)))
    def sample_test(n, sign_fn, count):
        bad = 0; tot = 0; plain_bad = 0
        for Bm in structured_sets(n, rng, count):
            tot += 1
            S0 = [0] * n
            for x in Bm: S0[x % n] += 1
            plain_bad += (not good(n, S0))
            if not good(n, sign_fn(Bm)): bad += 1; print('      FAIL', Bm)
        return tot, plain_bad, bad
    if part == 'lemmas':
        print('Remark after Lemma E (one signing for all q >= 5: balanced, plus one turn if the number of cells is even), exhaustive:')
        for nx, ny in [(3, 3), (3, 4), (4, 4), (3, 5), (3, 6)]:
            tot, bad = check_lemma2d(nx, ny); print(f'   grid {nx} x {ny}: sets {tot}, failures of (1)-(4): {bad}', flush=True)
        print('Lemma E (modulo q), exhaustive over all nonempty sets of cells:')
        for nx, ny in [(3, 3), (3, 4), (4, 4), (3, 5)]:
            for q in (3, 5, 7):
                tot, bad = check_lemma_grid(nx, ny, q); print(f'   grid {nx} x {ny}, q = {q}: sets {tot}, failures: {bad}', flush=True)
    if part == 'prop4':
        print('Proposition 4 (every digit misses a value => all signs + is already good):')
        for n in [15, 45, 105, 225, 315, 1155]:
            tot = 0; bad = 0
            for _ in range(3000):
                k = rng.randrange(1, 9); Bm = [rng.randrange(n) for _ in range(k)]
                if not digits_missing(n, set(Bm)): continue
                tot += 1; S0 = [0] * n
                for x in Bm: S0[x] += 1
                bad += (not good(n, S0))
            print(f'   n = {n}: multisets satisfying the hypothesis {tot}; all signs + not good: {bad}', flush=True)
    if part in ('t2small', 't2a', 't2b'):
        print('Theorem 2 (n = p^a q^b), exhaustive over all nonempty subsets (for n = 21: those containing 0):')
        cases = {'t2small': [(3, 1, 1, 0), (5, 1, 1, 0), (3, 2, 1, 0), (3, 1, 5, 1), (5, 1, 3, 1)], 't2a': [(3, 1, 7, 1)], 't2b': [(7, 1, 3, 1)]}[part]
        for (p, a, q, b) in cases:
            n = p ** a * (q ** b if q > 1 else 1); bad = 0; tot = 0
            for mask in range(1, 1 << n):
                if n > 15 and mask % 2 == 0: continue
                Bm = [i for i in range(n) if mask >> i & 1]; tot += 1
                if not good(n, two_primes(Bm, p, a, q if q > 1 else 3, b if q > 1 else 0)): bad += 1
            print(f'   n = {n} (tree prime {p}, other prime {q if q > 1 else "none"}): sets {tot}, failures {bad}', flush=True)
    if part == 't2rand':
        print('Theorem 2, random and structured sets and multisets:')
        for (p, a, q, b) in [(3, 2, 5, 1), (5, 1, 3, 2), (3, 2, 7, 1), (7, 1, 3, 2), (3, 1, 5, 2), (5, 2, 3, 1), (3, 3, 5, 1), (5, 1, 3, 3), (3, 2, 5, 2), (5, 2, 3, 2), (3, 4, 1, 0), (5, 3, 1, 0), (7, 2, 1, 0), (3, 3, 7, 1), (11, 1, 13, 1)]:
            n = p ** a * (q ** b if q > 1 else 1)
            tot, plain_bad, bad = sample_test(n, lambda Bm: two_primes(Bm, p, a, q if q > 1 else 3, b if q > 1 else 0), 600)
            print(f'   n = {n} = {p}^{a} * {q}^{b}: tried {tot} (all signs + fails for {plain_bad} of them); construction fails: {bad}', flush=True)
    if part in ('t3a', 't3b'):
        print('Theorem 3 (n = p r q^b), random and structured sets and multisets:')
        cases = {'t3a': [(3, 5, 7, 1), (3, 7, 5, 1), (5, 3, 7, 1), (5, 7, 3, 1), (3, 5, 11, 1), (3, 11, 5, 1), (3, 5, 13, 1), (7, 13, 3, 1)],
                 't3b': [(5, 7, 11, 1), (3, 7, 5, 2), (3, 5, 7, 2), (7, 11, 13, 1), (5, 7, 3, 2), (5, 11, 3, 2), (5, 7, 3, 3), (5, 13, 3, 2)]}[part]
        for (p, r, q, b) in cases:
            n = p * r * q ** b
            tot, plain_bad, bad = sample_test(n, lambda Bm: three_primes(Bm, p, r, q, b), 500)
            print(f'   n = {n} = {p} * {r} * {q}^{b}: tried {tot} (all signs + fails for {plain_bad} of them); construction fails: {bad}', flush=True)
