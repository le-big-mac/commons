# tree_single.py -- one tree T = Z_{p^a}.
# (1) cross-check of the vectorised "good" against the definition by explicit cubes;
# (2) Lemma T: for x : T -> V (vectors), the number of sign vectors s with total != 0 and s*x flat at some level
#     i >= 1 is at most (w + w^2 + .. + w^a) 2^(p^a), w = 2^(1-p);  also the count level by level;
# (3) Lemma S: least fraction of good sign vectors for scalar functions c != 0.
# usage: python tree_single.py p a q mode [args]
#   mode exh  : all c with entries in {0..(q-1)/2} (up to sign), a small tree (p^a <= 9)
#   mode samp N maxw : N random functions with at most maxw active leaves (structured kinds mixed in)
#   mode vec N d : Lemma T for N random vector-valued x in F_q^d (several kinds)
import sys, itertools, random
from fractions import Fraction
import numpy as np
import tb

def lam(p, a):
    w = Fraction(1, 2 ** (p - 1))
    return sum(w ** l for l in range(1, a + 1))

def flat_masks(SX, p, a, q):
    """SX: (N, n, d) signed vectors.  Returns total_nonzero (N,), flat[i] (N,) for i = 1..a."""
    N = SX.shape[0]
    tot = SX.sum(axis=1)
    if q: tot = tot % q
    tnz = tot.any(axis=1)
    flats = []
    for i in range(1, a + 1):
        B = tb.fold_axis(SX, 1, p, a, i)
        B = tb.diff_axis(B, 1, p, i)
        if q: B = B % q
        flats.append(~B.reshape(N, -1).any(axis=1))
    return tnz, flats

def analyse(x, p, a, q, S):
    """x: (n, d) integer array.  Returns (#good, #lost, [#lost at level i]) over all sign vectors S (N, n)."""
    SX = S[:, :, None] * x[None, :, :]
    tnz, flats = flat_masks(SX, p, a, q)
    anyflat = np.zeros(S.shape[0], dtype=bool)
    per = []
    for f in flats:
        anyflat |= f
        per.append(int((tnz & f).sum()))
    return int((tnz & ~anyflat).sum()), int((tnz & anyflat).sum()), per

def main():
    p, a, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    q = q or None
    mode = sys.argv[4]
    n = p ** a
    rnd = random.Random(12345)
    L = lam(p, a)
    if mode == "exh":
        S = tb.all_signs(n)
        # cross-check on a few functions
        for _ in range(20):
            c = np.array([rnd.randrange(-2, 3) for _ in range(n)], dtype=np.int64)
            if not c.any(): continue
            for t in range(6):
                s = S[rnd.randrange(S.shape[0])]
                assert tb.good_one(s * c, [(p, a)], q) == tb.good_one_slow(s * c, [(p, a)], q)
        vals = range(0, (q - 1) // 2 + 1) if q else range(0, 3)
        least = None; worst = None; maxlost = Fraction(0); cnt = 0
        for c in itertools.product(vals, repeat=n):
            if not any(c): continue
            cnt += 1
            x = np.array(c, dtype=np.int64)[:, None]
            g, lost, per = analyse(x, p, a, q, S)
            fr = Fraction(g, 2 ** n)
            if least is None or fr < least: least, worst = fr, c
            maxlost = max(maxlost, Fraction(lost, 2 ** n))
            assert Fraction(lost, 2 ** n) <= L
        print("tree Z_%d over %s: all %d nonzero functions with entries in %s (up to sign): least fraction of good sign vectors %s (at %s); largest lost fraction %s <= bound %s"
              % (n, "F_%d" % q if q else "Q", cnt, list(vals), least, worst, maxlost, L))
    elif mode == "samp":
        N, maxw = int(sys.argv[5]), int(sys.argv[6])
        least = None; worst = None; maxlost = Fraction(0)
        hi = (q - 1) // 2 if q else 3
        for it in range(N):
            w = rnd.randrange(1, maxw + 1)
            kind = it % 4
            if kind == 0:
                act = rnd.sample(range(n), w)
            elif kind == 1:   # inside one class modulo p^(a-1) .. clustered low in the tree
                i = rnd.randrange(0, a)
                base = rnd.randrange(p ** i)
                pool = [v for v in range(n) if v % p ** i == base]
                act = rnd.sample(pool, min(w, len(pool)))
            elif kind == 2:   # whole sibling groups of leaves
                grp = rnd.sample(range(p ** (a - 1)), max(1, w // p))
                act = [gq + t * p ** (a - 1) for gq in grp for t in range(p)]
                act = act[:maxw]
            else:             # leaves spread over the top classes
                act = [rnd.randrange(n) for _ in range(w)]
                act = list(set(act))
            c = np.zeros(n, dtype=np.int64)
            for v in act:
                c[v] = rnd.choice([1, 1, 1, -1, 2]) if it % 3 else rnd.randrange(1, hi + 1)
            act = [v for v in range(n) if c[v]]
            # enumerate signs on the active leaves only (the others do not matter)
            S = np.ones((2 ** len(act), n), dtype=np.int64)
            S[:, act] = tb.all_signs(len(act))
            g, lost, per = analyse(c[:, None], p, a, q, S)
            fr = Fraction(g, S.shape[0]); lo = Fraction(lost, S.shape[0])
            if least is None or fr < least: least, worst = fr, (sorted(act), [int(c[v]) for v in sorted(act)])
            maxlost = max(maxlost, lo)
            assert lo <= L, (act, c)
        print("tree Z_%d over %s: %d functions with at most %d active leaves: least fraction of good sign vectors %s (at %s); largest lost fraction %s <= bound %s"
              % (n, "F_%d" % q if q else "Q", N, maxw, least, worst, maxlost, L))
    elif mode == "vec":
        N, d = int(sys.argv[5]), int(sys.argv[6])
        maxw = int(sys.argv[7]) if len(sys.argv) > 7 else n
        maxlost = Fraction(0); maxper = [Fraction(0)] * a
        hi = (q - 1) // 2 if q else 2
        for it in range(N):
            x = np.zeros((n, d), dtype=np.int64)
            kind = it % 5
            w = rnd.randrange(1, maxw + 1)
            act = rnd.sample(range(n), w)
            if kind == 0:
                for v in act: x[v] = [rnd.randrange(-hi, hi + 1) for _ in range(d)]
            elif kind == 1:      # all equal to one vector up to sign
                b = [rnd.randrange(1, hi + 1) for _ in range(d)]
                for v in act: x[v] = [rnd.choice([1, -1]) * t for t in b]
            elif kind == 2:      # one vector on whole sibling groups of leaves (the extreme case of the bound)
                b = [rnd.randrange(1, hi + 1) for _ in range(d)]
                for gq in rnd.sample(range(p ** (a - 1)), rnd.randrange(1, min(3, p ** (a - 1)) + 1)):
                    for t in range(p): x[gq + t * p ** (a - 1)] = b
            elif kind == 3:      # one vector b_D on each of a few groups at a random level, on one leaf of each class
                i = rnd.randrange(1, a + 1)
                for D in rnd.sample(range(p ** (i - 1)), rnd.randrange(1, min(3, p ** (i - 1)) + 1)):
                    b = [rnd.randrange(-hi, hi + 1) for _ in range(d)]
                    for t in range(p):
                        cls = D + t * p ** (i - 1)
                        leaf = cls + p ** i * rnd.randrange(p ** (a - i))
                        x[leaf] = b
            else:                # rank one: scalar multiples of one vector
                b = [rnd.randrange(1, hi + 1) for _ in range(d)]
                for v in act: x[v] = [rnd.randrange(-hi, hi + 1) * t for t in b]
            act = [v for v in range(n) if x[v].any()]
            if not act or len(act) > 16: continue
            S = np.ones((2 ** len(act), n), dtype=np.int64)
            S[:, act] = tb.all_signs(len(act))
            g, lost, per = analyse(x, p, a, q, S)
            lo = Fraction(lost, S.shape[0])
            maxlost = max(maxlost, lo)
            for i in range(a): maxper[i] = max(maxper[i], Fraction(per[i], S.shape[0]))
            assert lo <= L, (x,)
        print("Lemma T, tree Z_%d over %s, %d vector-valued x in dimension %d: largest lost fraction %s <= bound %s; largest per level %s"
              % (n, "F_%d" % q if q else "Q", N, d, maxlost, L, [str(t) for t in maxper]))

if __name__ == "__main__":
    main()
