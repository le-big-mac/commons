"""Brute-force check, in Z_72 (p = 2, q = 3) and Z_108 read as p = 3, q = 2 on a sample, of the lemmas on mixed sets:
a set A that is a union of i >= 1 cosets of P and j >= 1 cosets of Q lying in different cosets of K = P + Q.
 M0  |A| = i p + j q;  in particular |A| = p q is impossible
 M2  if |A| = p^2 q and p, p^3 q, p^2 q^2 are zeros of A, then A + K = A
 M3  if |A| = p^2 q, p < q, then q is not a zero of A
 M4  if |A| = p^2 q, then q and p q^2 are not both zeros of A
(Noon = agent2, 21 November 2026)"""
import sys, itertools, numpy as np
p, q = int(sys.argv[1]), int(sys.argv[2]); a, b = 3, 2; M = p**a * q**b; size = p * p * q
ords = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]; val = lambda o: p**o[0] * q**o[1]
def cub(o):
    l, m = o; d = val(o); cntm = np.zeros((d, M), np.int64); cntm[np.arange(M) % d, np.arange(M)] = 1; rows = []
    for c in range(d):
        if l and m: rows.append(cntm[c] - cntm[(c + d // p) % d] - cntm[(c + d // q) % d] + cntm[(c + d // p + d // q) % d])
        elif l: rows.append(cntm[c] - cntm[(c + d // p) % d])
        else: rows.append(cntm[c] - cntm[(c + d // q) % d])
    return np.array(rows)
L = np.vstack([cub(o) for o in ords]); blocks = np.cumsum([0] + [val(o) for o in ords]); oi = {o: t for t, o in enumerate(ords)}
Pl = [[(x + t * (M // p)) % M for t in range(p)] for x in range(M // p)]; Ql = [[(y + t * (M // q)) % M for t in range(q)] for y in range(M // q)]
ind = lambda line: np.bincount(line, minlength=M)
IP = np.array([ind(l) for l in Pl]); IQ = np.array([ind(l) for l in Ql]); VP = IP @ L.T; VQ = IQ @ L.T
KP = [l[0] % (M // (p * q)) for l in Pl]; KQ = [l[0] % (M // (p * q)) for l in Ql]
Kshift = [np.roll(np.eye(M, dtype=np.int64), g, axis=1) for g in (M // p, M // q)]          # x -> x + M/p, x -> x + M/q
splits = [(i, (size - i * p) // q) for i in range(1, size // p + 1) if (size - i * p) % q == 0 and (size - i * p) // q >= 1]
limit = int(sys.argv[3]) if len(sys.argv) > 3 else None; import random; random.seed(5)
n = m2 = m2bad = m3 = m4 = 0
for i, j in splits:
    Qc = list(itertools.combinations(range(len(Ql)), j))
    if limit and len(Qc) > 3000: Qc = random.sample(Qc, 3000)
    SQ = np.array([VQ[list(c)].sum(0) for c in Qc]); IQs = np.array([IQ[list(c)].sum(0) for c in Qc]); QK = [frozenset(KQ[t] for t in c) for c in Qc]
    Pc = itertools.combinations(range(len(Pl)), i)
    if limit: Pc = (tuple(sorted(random.sample(range(len(Pl)), i))) for _ in range(limit))
    for cp in Pc:
        kp = {KP[t] for t in cp}; ok = np.array([not (kp & kq) for kq in QK])
        if not ok.any(): continue
        tot = SQ[ok] + VP[list(cp)].sum(0); A = IQs[ok] + IP[list(cp)].sum(0); n += int(ok.sum())
        z = lambda o: (tot[:, blocks[oi[o]]:blocks[oi[o] + 1]] == 0).all(1)
        hyp = z((1, 0)) & z((3, 1)) & z((2, 2))
        if hyp.any():
            m2 += int(hyp.sum()); Ah = A[hyp]
            per = (Ah @ Kshift[0] == Ah).all(1) & (Ah @ Kshift[1] == Ah).all(1); m2bad += int((~per).sum())
        m3 += int(z((0, 1)).sum()); m4 += int((z((0, 1)) & z((1, 2))).sum())
print(f"Z_{M} (p = {p}, q = {q}), unions of cosets of P and of Q in different cosets of K, size p^2 q = {size}, splits {splits}: {n:,} sets" + (" (a random sample)" if limit else " (all)"))
print(f"  M2: sets with the zeros p, p^3 q, p^2 q^2: {m2:,}; of these not invariant under K: {m2bad}")
print(f"  M3: sets with the zero q: {m3:,}" + ("  (the lemma says none, as p < q)" if p < q else "  (p > q: the lemma does not apply)"))
print(f"  M4: sets with the zeros q and p q^2: {m4:,}  (the lemma says none)")
