"""Count-level exhaustive checks for lemmas-sharper-agent3.md (referee's own code).

Part 1  Fact 5 (normal form) on all small arrays, and the "compare the minima" triviality.
Part 2  Lemma A+ Steps 1-3, per residue class j mod q: ALL nonnegative integer arrays N(r, l),
        r in Z_{p^3}, l in Z_q, of total p^2 that are additive on every (3,2)-box and whose (2,2)-arrays
        are additive.  Claim: exactly the p*q arrays [r = rho mod p][l = l0].
        (a) naive brute force over all arrays (p = 2);  (b) box-structured enumeration (also p = 3).
Part 3  Lemma B+: (i) additive p x q arrays of total p^2 q with all row sums in p^2 Z  => p^2 [rho = rho0];
        (ii) [B3] additive p x q arrays of total p^2 q, column sums in qZ, each row constant mod p
             => pq [j = j0];  plus a direct brute force over N_{2,1} arrays at (2,3).
"""
import itertools
import sys
import time
import numpy as np

t00 = time.time()
fails = 0


def is_additive(N):
    N = np.asarray(N)
    return not (N - N[:, :1] - N[:1, :] + N[:1, :1]).any()


# ------------------------------------------------------------------ Part 1
print("Part 1: Fact 5 on all P x Q arrays with entries 0..K")
for P, Q, K in [(2, 2, 6), (2, 3, 4), (3, 2, 4), (3, 3, 2), (2, 5, 2), (5, 2, 2), (3, 3, 3), (3, 5, 1), (2, 7, 1)]:
    n_add = n_all = 0
    bad = 0
    for flat in itertools.product(range(K + 1), repeat=P * Q):
        n_all += 1
        N = np.array(flat).reshape(P, Q)
        if not is_additive(N):
            # no decomposition a + alpha_i + beta_l can exist (it would be additive) -- nothing to check
            continue
        n_add += 1
        # the note's construction: i0 minimises u, l0 minimises w; u(i) = N(i,0)+const, w(l) = N(0,l)+const
        i0 = int(np.argmin(N[:, 0]))
        l0 = int(np.argmin(N[0, :]))
        a = int(N[i0, l0])
        al = N[:, l0] - a
        be = N[i0, :] - a
        ok = (a >= 0 and al.min() == 0 and be.min() == 0 and (al >= 0).all() and (be >= 0).all()
              and (N == a + al[:, None] + be[None, :]).all()
              and N.sum() == P * Q * a + Q * al.sum() + P * be.sum()
              and (N.sum(axis=1) == Q * a + Q * al + be.sum()).all()
              and (N.sum(axis=0) == P * a + al.sum() + P * be).all()
              and (len(set(N.sum(axis=1))) == 1) == (not al.any())
              and (len(set(N.sum(axis=0))) == 1) == (not be.any())
              and a == N.min())
        bad += not ok
    print(f"  {P}x{Q}, K={K}: {n_all} arrays, {n_add} additive, normal-form failures: {bad}")
    fails += bad
bad = 0
cnt = 0
for L in (2, 3):
    for b1 in itertools.product(range(5), repeat=L):
        if min(b1):
            continue
        for b2 in itertools.product(range(5), repeat=L):
            if min(b2):
                continue
            for c in (1, 2, 3):
                d = [x - c * y for x, y in zip(b1, b2)]
                if len(set(d)) == 1:
                    cnt += 1
                    bad += d[0] != 0
print(f"  'compare the minima': {cnt} cases with beta - c*beta' constant, constant nonzero in {bad}")
fails += bad

# ------------------------------------------------------------------ Part 2 (a)
print("Part 2(a): Lemma A+ per class j, naive brute force over all arrays on Z_8 x Z_q of total 4 (p = 2)")
for q in (3, 5, 7):
    p = 2
    ncell = 8 * q
    combos = np.array(list(itertools.combinations_with_replacement(range(ncell), 4)), dtype=np.int32)
    N = np.zeros((len(combos), ncell), dtype=np.int8)
    for k in range(4):
        np.add.at(N, (np.arange(len(combos)), combos[:, k]), 1)
    N = N.reshape(len(combos), 8, q).astype(np.int16)       # N[s, r, l]
    ok = np.ones(len(combos), dtype=bool)
    # (3,2)-boxes: r in {c, c+4}
    for c in range(4):
        d = N[:, c + 4, :] - N[:, c, :]
        ok &= (d == d[:, :1]).all(axis=1)
    # (2,2): N2[c, l] = N[c] + N[c+4], boxes {rho, rho+2}
    N2 = N[:, :4, :] + N[:, 4:, :]
    for rho in range(2):
        d = N2[:, rho + 2, :] - N2[:, rho, :]
        ok &= (d == d[:, :1]).all(axis=1)
    V = N[ok]
    # claimed structure
    good = 0
    for arr in V:
        st = False
        for rho in range(2):
            for l0 in range(q):
                want = np.zeros((8, q), dtype=np.int16)
                want[rho::2, l0] = 1
                st |= (arr == want).all()
        good += st
    print(f"  q={q}: {len(combos)} arrays, {len(V)} satisfy both box conditions, {good} have the claimed structure "
          f"(expected {p*q} = p*q)  {'ok' if len(V) == good == p*q else 'FAIL'}")
    fails += not (len(V) == good == p * q)


# ------------------------------------------------------------------ Part 2 (b)
def additive_arrays(P, Q, smax):
    """all additive P x Q nonnegative integer arrays with total <= smax, dict total -> list of arrays.
    Parametrised by the first column and first row (definition of additivity), no normal form."""
    out = {}

    def comps(n, tot):       # n nonneg integers with sum <= tot
        if n == 0:
            yield ()
            return
        for v in range(tot + 1):
            for rest in comps(n - 1, tot - v):
                yield (v,) + rest

    for col in comps(P, smax):
        v = col[0]
        for row in comps(Q - 1, smax - v):
            N = np.array(col)[:, None] + np.array((v,) + row)[None, :] - v
            if N.min() < 0:
                continue
            s = int(N.sum())
            if s <= smax:
                out.setdefault(s, []).append(N)
    return out


print("Part 2(b): Lemma A+ per class j, box-structured exhaustive enumeration")
for p, q in [(2, 3), (2, 5), (2, 7), (2, 11), (3, 2), (3, 5), (3, 7)]:
    t0 = time.time()
    S = p * p
    boxes = additive_arrays(p, q, S)            # (3,2)-boxes: p x q
    flat = [(s, N, tuple(N.sum(axis=0))) for s in sorted(boxes) for N in boxes[s]]
    # group = p boxes (c = rho + i p); (2,2)-array rows = column sums of the boxes; additive iff rows differ by constants
    groups = {}                                  # total -> list of tuples of boxes

    def rec(chosen, tot, shape):
        if len(chosen) == p:
            groups.setdefault(tot, []).append(tuple(chosen))
            return
        for s, N, cs in flat:
            if tot + s > S:
                break
            sh = tuple(x - min(cs) for x in cs)
            if shape is None or sh == shape:
                rec(chosen + [N], tot + s, sh)

    rec([], 0, None)
    ngroups = sum(len(v) for v in groups.values())
    # complete configurations: p groups with totals summing to p^2
    totals = sorted(groups)
    n_complete = 0
    n_struct = 0

    def rec2(i, rem, chosen):
        global n_complete, n_struct
        if i == p:
            if rem == 0:
                n_complete += 1
                nz = [g for g in chosen if any(b.any() for b in g)]
                if len(nz) == 1:
                    g = nz[0]
                    l0s = set()
                    okk = True
                    for b in g:
                        # every row of the box must be the unit vector e_{l0}
                        if not (b.sum(axis=1) == 1).all() or not (b.max() == 1):
                            okk = False
                            break
                        l0s |= set(int(x) for x in b.argmax(axis=1))
                    if okk and len(l0s) == 1:
                        n_struct += 1
            return
        for s in totals:
            if s > rem:
                break
            for g in groups[s]:
                rec2(i + 1, rem - s, chosen + [g])

    rec2(0, S, [])
    okp = n_complete == n_struct == p * q
    print(f"  (p,q)=({p},{q}): {sum(len(v) for v in boxes.values())} additive boxes of total <= {S}; group totals occurring "
          f"{totals}; {ngroups} valid groups; complete configurations: {n_complete}, with the claimed structure: {n_struct} "
          f"(expected {p*q})  {'ok' if okp else 'FAIL'}  [{time.time()-t0:.1f}s]")
    fails += not okp
    sys.stdout.flush()

# ------------------------------------------------------------------ Part 3
print("Part 3(i): additive p x q arrays, total p^2 q, all row sums in p^2 Z  =>  p^2 [rho = rho0]   (B1/B2 middle step)")


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for v in range(total + 1):
        for rest in compositions(total - v, parts - 1):
            yield (v,) + rest


def arrays_rowsums(p, q, S, rowmod, extra=None):
    """all additive p x q nonneg arrays with total S and every row sum = 0 mod rowmod:
    row i = row 0 + delta_i (definition of additivity)."""
    res = []
    for R0 in range(0, S + 1, rowmod):
        for r in compositions(R0, q):
            mn = min(r)
            # delta_i with R0 + q*delta_i in rowmod*Z, in [0, S], delta_i >= -mn
            cand = [d for d in range(-mn, (S - R0) // q + 1) if (R0 + q * d) % rowmod == 0]
            for ds in itertools.product(cand, repeat=p - 1):
                if p * R0 + q * sum(ds) == S:
                    N = np.array([list(r)] + [[x + d for x in r] for d in ds])
                    if extra is None or extra(N):
                        res.append(N)
    return res


for p, q in [(2, 3), (3, 2), (2, 5), (5, 2), (2, 7), (7, 2), (3, 5), (5, 3), (7, 3), (11, 2), (5, 7) if False else (3, 2)]:
    t0 = time.time()
    S = p * p * q
    res = arrays_rowsums(p, q, S, p * p)
    good = sum(1 for N in res if sorted(N.sum(axis=1)) == [0] * (p - 1) + [S] and (N.max(axis=1).max() == p * p) and (N[N.sum(axis=1).argmax()] == p * p).all())
    b1 = sum(1 for N in res if (N.sum(axis=0) % q == 0).all())
    okp = len(res) == good == p
    print(f"  (p,q)=({p},{q}): {len(res)} arrays, {good} of the form p^2[rho=rho0] (expected {p}); "
          f"of these with all column sums in qZ (B1): {b1} (expected 0)  {'ok' if okp and b1 == 0 else 'FAIL'}  [{time.time()-t0:.1f}s]")
    fails += not (okp and b1 == 0)
    sys.stdout.flush()

print("Part 3(ii): additive p x q arrays, total p^2 q, column sums in qZ, each row constant mod p  =>  pq [j = j0]   (B3 middle step)")
for p, q in [(2, 3), (3, 2), (2, 5), (5, 2), (2, 7), (3, 5), (5, 3), (3, 7), (2, 11), (2, 13)]:
    t0 = time.time()
    S = p * p * q
    # transpose: rows <-> columns
    res = arrays_rowsums(q, p, S, q, extra=lambda Nt: not ((Nt - Nt[:1, :]) % p).any())
    good = sum(1 for Nt in res if sorted(Nt.sum(axis=1)) == [0] * (q - 1) + [S] and (Nt[Nt.sum(axis=1).argmax()] == p * q).all())
    okp = len(res) == good == q
    print(f"  (p,q)=({p},{q}): {len(res)} arrays, {good} of the form pq[j=j0] (expected {q})  {'ok' if okp else 'FAIL'}  [{time.time()-t0:.1f}s]")
    fails += not okp
    sys.stdout.flush()

print("Part 3(iii): B3 middle step, direct brute force at (p,q)=(2,3): all 4 x 3 arrays N_{2,1} of total 12")
p, q = 2, 3
t0 = time.time()
cells = p * p * q
tot = p * p * q
n_all = n_ok = n_onecol = 0
# enumerate compositions of 12 into 12 cells in chunks via stars and bars
bars = itertools.combinations(range(tot + cells - 1), cells - 1)
chunk = []


def process(chunk):
    global n_all, n_ok, n_onecol
    B = np.array(chunk, dtype=np.int16)
    ext = np.concatenate([np.full((len(B), 1), -1, dtype=np.int16), B, np.full((len(B), 1), tot + cells - 1, dtype=np.int16)], axis=1)
    N = (np.diff(ext, axis=1) - 1).reshape(len(B), p * p, q)       # N[s, u, j], u in Z_{p^2}
    n_all += len(N)
    ok = np.ones(len(N), dtype=bool)
    # column sums N01(j) in qZ   (consequence of Phi_{q^2})
    ok &= (N.sum(axis=1) % q == 0).all(axis=1)
    # (2,1)-boxes {rho + i p} x Z_q additive (Phi_{p^2 q})
    for rho in range(p):
        d = N[:, rho + p, :] - N[:, rho, :]
        ok &= (d == d[:, :1]).all(axis=1)
    # N11 additive (Phi_{pq})
    N11 = N[:, :p, :] + N[:, p:, :]
    d = N11[:, 1, :] - N11[:, 0, :]
    ok &= (d == d[:, :1]).all(axis=1)
    V = N[ok]
    n_ok += len(V)
    n_onecol += int(((V.sum(axis=1) > 0).sum(axis=1) == 1).sum())


for b in bars:
    chunk.append(b)
    if len(chunk) == 200000:
        process(chunk)
        chunk = []
if chunk:
    process(chunk)
print(f"  {n_all} arrays; {n_ok} satisfy [col sums in qZ, boxes additive, N11 additive]; {n_onecol} of them live in one column "
      f"{'ok' if n_ok == n_onecol else 'FAIL'}  [{time.time()-t0:.1f}s]")
fails += n_ok != n_onecol
print(f"FAILED CHECKS: {fails}   total time {time.time()-t00:.1f}s")
