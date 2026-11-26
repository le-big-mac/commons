"""The four lines of the paragraph added before section 8, item (2), run step by step in exact integers.
For a multiset A on Z_M, M = p^n q, with q not dividing |A|:
  G(X) = A(X) * prod of Phi_{p^r} over the levels r in 1..n that are in neither E nor F;
  R(u) = sum of the coefficients of G at the exponents congruent to u mod p^n   (reduction mod X^(p^n) - 1);
  claim 1: all R(u) are congruent mod q to one c with 0 < c < q;  Q = (R - c)/q >= 0;
  claim 2: Q, as a multiset on Z_{p^n}, has Phi_{p^r} | Q at every level r not in F minus E, and not at the levels of F minus E;
  claim 3: if k >= 1 then Q != 0 and Q(1) >= p^(n-k) (indeed p^(n-k) divides Q(1));
  claim 4: |A| p^(n-e-k) = c p^n + q Q(1) >= p^n + q p^(n-k)   when k >= 1.
Patterns here by the tree conditions of section 1 of the note (exact integers), written afresh.
usage: four_lines.py p q n max_size"""
import sys, itertools

def tree_pattern(p, q, n, w):
    """w: weights on Z_M. returns (E, F) with E in 1..n, F in 0..n, by equal totals / equal shapes of the p children."""
    P = p ** n; M = P * q
    def vec(d, c):          # layer vector of the class c mod p^d
        v = [0] * q
        for x in range(M):
            if w[x] and x % (p ** d) == c: v[x % q] += w[x]
        return v
    E = []; F = []
    root = vec(0, 0)
    if len(set(root)) == 1: F.append(0)
    for a in range(1, n + 1):
        inE = inF = True
        for c in range(p ** (a - 1)):
            ch = [vec(a, c + i * p ** (a - 1)) for i in range(p)]
            if len({sum(v) for v in ch}) > 1: inE = False
            d0 = [x - y for x, y in zip(ch[0], ch[0])]
            for v in ch[1:]:
                diff = [x - y for x, y in zip(v, ch[0])]
                if len(set(diff)) > 1: inF = False
        if inE: E.append(a)
        if inF: F.append(a)
    return tuple(E), tuple(F)

def polymul_mod(a, b, M):
    out = [0] * M
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: out[(i + j) % M] += x * y
    return out

def phi_ppower(p, r, M):      # Phi_{p^r}(X) = 1 + X^(p^(r-1)) + ... + X^((p-1) p^(r-1)), as weights mod X^M - 1
    v = [0] * M
    for i in range(p): v[(i * p ** (r - 1)) % M] += 1
    return v

def levels_E_of_function_on_Zpn(p, n, Qv):     # levels r in 1..n with Phi_{p^r} | Q, by equal totals of children
    out = []
    for a in range(1, n + 1):
        ok = True
        for c in range(p ** (a - 1)):
            tots = [sum(Qv[u] for u in range(p ** n) if u % (p ** a) == c + i * p ** (a - 1)) for i in range(p)]
            if len(set(tots)) > 1: ok = False
        if ok: out.append(a)
    return set(out)

def multisets(M, s):           # all weight vectors on Z_M of total s
    for comb in itertools.combinations_with_replacement(range(M), s):
        w = [0] * M
        for x in comb: w[x] += 1
        yield w

p, q, n, smax = map(int, sys.argv[1:5]); P = p ** n; M = P * q
tested = with_k = fails = 0; eq = 0; cases_qdiv = 0; qdiv_lines_give = 0
for s in range(1, smax + 1):
    for w in multisets(M, s):
        E, F = tree_pattern(p, q, n, w)
        if 0 in F: continue
        F1 = [a for a in F if a >= 1]; e = len(E); GmE = [a for a in F1 if a not in E]; k = len(GmE)
        G = list(w)
        for r in range(1, n + 1):
            if r not in E and r not in F1: G = polymul_mod(G, phi_ppower(p, r, M), M)
        R = [sum(G[x] for x in range(M) if x % P == u) for u in range(P)]
        assert sum(R) == s * p ** (n - e - k)
        res = {r % q for r in R}
        if s % q == 0:
            cases_qdiv += 1
            assert len(res) == 1         # the coefficients are still congruent mod q; c may be 0
            continue
        tested += 1
        ok = len(res) == 1 and 0 not in res
        if ok:
            c = R[0] % q; Qv = [(r - c) // q for r in R]
            ok = min(Qv) >= 0
            lev = levels_E_of_function_on_Zpn(p, n, Qv) if any(Qv) else set(range(1, n + 1))
            ok = ok and all((r in lev) == (r not in GmE) for r in range(1, n + 1)) if any(Qv) else ok and k == 0
            if k >= 1:
                with_k += 1
                ok = ok and any(Qv) and sum(Qv) % p ** (n - k) == 0 and sum(Qv) >= p ** (n - k)
                ok = ok and s * p ** (n - e - k) == c * P + q * sum(Qv) >= P + q * p ** (n - k) and s >= p ** e * (p ** k + q)
                if s == p ** e * (p ** k + q): eq += 1
        if not ok:
            fails += 1
            if fails <= 3: print('   FAILS', w, E, F)
print(f"Z_{M} (p = {p}, q = {q}, n = {n}), all multisets of 1 to {smax} elements with Phi_q not dividing A: with q not dividing |A| {tested}, of them with k >= 1 {with_k}; some line of the four fails in {fails}; bound met with equality in {eq}; with q dividing |A| (lines not applied, congruence of the coefficients checked) {cases_qdiv}")
