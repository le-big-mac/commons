"""Referee: random STRUCTURED multisets in larger groups, built level by level from pools of smaller classes so that
equal totals / equal shapes / balanced classes occur often (a uniformly random multiset has the empty pattern and
tests nothing).  Patterns are then computed literally from section 1 for every class of every multiset, and
Lemmas 2-6 are tested for every pair contained in the pattern; balanced multisets are tested against
Theorem A, Proposition 7 and Theorem B (lower bounds).

usage: ref_random.py p q n npool seed
"""
import sys, time, random
import numpy as np
from ref_common import set_tables, rule, literal_patterns, bits_to_set
from ref_lemmas import Tally, test_records


def main():
    p, q, n, npool, seed = (int(x) for x in sys.argv[1:6])
    rng = random.Random(seed)
    t0 = time.time()

    class Pool:
        def __init__(self):
            self.items = []          # (W array (p^j, q), g tuple)
            self.by_vec = {}
            self.by_tot = {}
            self.by_shape = {}
            self.balanced = []
            self.seen = set()

        def add(self, W):
            key = W.tobytes()
            if key in self.seen:
                return
            self.seen.add(key)
            g = tuple(int(v) for v in W.sum(axis=0))
            i = len(self.items)
            self.items.append((W, g))
            self.by_vec.setdefault(g, []).append(i)
            self.by_tot.setdefault(sum(g), []).append(i)
            mn = min(g)
            self.by_shape.setdefault(tuple(v - mn for v in g), []).append(i)
            if len(set(g)) == 1:
                self.balanced.append(i)

        def pick(self, idxs=None):
            # favour small totals: best of 2 or 3
            if idxs is None:
                c = [rng.randrange(len(self.items)) for _ in range(rng.choice((1, 2, 3)))]
            else:
                c = [rng.choice(idxs) for _ in range(rng.choice((1, 2, 3)))]
            return min(c, key=lambda i: sum(self.items[i][1]))

    # level 0: vectors
    pool = Pool()
    pool.add(np.zeros((1, q), dtype=np.int64))
    for w in range(q):
        for m in (1, 2, 3):
            v = np.zeros((1, q), dtype=np.int64)
            v[0, w] = m
            pool.add(v)
    for c in (1, 2, 3):
        pool.add(np.full((1, q), c, dtype=np.int64))
        for w in range(q):
            v = np.full((1, q), c, dtype=np.int64)
            v[0, w] -= 1
            pool.add(v)
            v = np.full((1, q), c, dtype=np.int64)
            v[0, w] += 1
            pool.add(v)
    for _ in range(60):
        pool.add(np.array([[rng.choice((0, 0, 0, 1, 1, 2)) for _ in range(q)]], dtype=np.int64))

    for j in range(1, n + 1):
        new = Pool()
        size = p ** (j - 1)
        zero = np.zeros((size, q), dtype=np.int64)
        cap = 4 * q * p ** j                           # keep totals near the sizes where the lemmas say something
        capchild = 4 * q * p ** (j - 1)
        tries = 0
        while len(new.items) < npool and tries < 3 * npool:
            tries += 1
            r = rng.random()
            kids = None
            if r < 0.10:                               # identical copies
                i = pool.pick()
                kids = [pool.items[i][0]] * p
            elif r < 0.25:                             # equal vectors, different insides
                i = pool.pick()
                g = pool.items[i][1]
                kids = [pool.items[rng.choice(pool.by_vec[g])][0] for _ in range(p)]
            elif r < 0.40:                             # equal shapes
                i = pool.pick()
                g = pool.items[i][1]
                mn = min(g)
                lst = pool.by_shape[tuple(v - mn for v in g)]
                kids = [pool.items[i][0]] + [pool.items[pool.pick(lst)][0] for _ in range(p - 1)]
            elif r < 0.55:                             # equal totals
                i = pool.pick()
                lst = pool.by_tot[sum(pool.items[i][1])]
                kids = [pool.items[i][0]] + [pool.items[rng.choice(lst)][0] for _ in range(p - 1)]
            elif r < 0.62:                             # one child, others empty
                i = pool.pick()
                kids = [pool.items[i][0]] + [zero] * (p - 1)
            elif r < 0.70:                             # balanced children only
                if pool.balanced:
                    kids = [pool.items[pool.pick(pool.balanced)][0] for _ in range(p)]
            elif r < 0.90:                             # balanced completion: last child = c*1 - sum of the others
                first = [pool.items[pool.pick()] for _ in range(p - 1)]
                if rng.random() < 0.4:                 # others with equal totals
                    lst = pool.by_tot[sum(first[0][1])]
                    first = [first[0]] + [pool.items[rng.choice(lst)] for _ in range(p - 2)]
                s = [sum(f[1][w] for f in first) for w in range(q)]
                c = max(s) + rng.choice((0, 0, 0, 1))
                tgt = tuple(c - v for v in s)
                if tgt in pool.by_vec:
                    last = pool.items[rng.choice(pool.by_vec[tgt])][0]
                else:
                    last = zero.copy()
                    for w in range(q):                 # spread the needed vector over random leaves
                        for _ in range(tgt[w]):
                            last[rng.randrange(size) if rng.random() < 0.3 else 0, w] += 1
                    if sum(tgt) <= capchild:
                        pool.add(last)
                kids = [f[0] for f in first] + [last]
            else:                                      # anything
                kids = [pool.items[pool.pick()][0] if rng.random() < 0.8 else zero for _ in range(p)]
            if kids is None:
                continue
            rng.shuffle(kids)
            # child i holds the strings with digit i at the new (shallowest) level: u = i + p * u'
            W = np.empty((size * p, q), dtype=np.int64)
            for i in range(p):
                W[i::p, :] = kids[i]
            if W.sum() > cap:
                continue
            if W.sum() > 0:
                new.add(W)
            # sometimes also the same class plus whole fibres on a coset-like set of strings
            if rng.random() < 0.15:
                T = [a for a in range(1, j + 1) if rng.random() < 0.5]
                u = np.arange(size * p)
                m = np.ones(size * p, dtype=bool)
                for a in range(1, j + 1):
                    if a not in T:
                        m &= ((u // p ** (a - 1)) % p) == (0 if rng.random() < 0.8 else rng.randrange(p))
                W2 = W.copy()
                W2[m, :] += rng.choice((1, 1, 2, p))
                if W2.sum() <= cap:
                    new.add(W2)
        pool = new
        print(f"  level {j}: pool of {len(pool.items)} classes, {len(pool.balanced)} balanced, totals up to "
              f"{max(sum(g) for _, g in pool.items)}  [{time.time() - t0:.0f} s]", flush=True)

    Wall = np.stack([W for W, _ in pool.items])            # (K, p^n, q); index u = sum u_a p^(a-1): level 1 is u mod p
    K = len(Wall)
    B = int(Wall.sum(axis=(1, 2)).max())
    tabs = set_tables(p, q, n + 1, B)
    tally = Tally()
    ex = []
    thm = Tally()
    chunk = max(1, 2000000 // (p ** n * q))
    nontriv = {}
    for s in range(0, K, chunk):
        W = Wall[s:s + chunk]
        pats = literal_patterns(p, q, n, W)
        for d in range(n + 1):
            r = pats[d]
            tot = r["tot"].ravel().astype(np.int64)
            keep = tot >= 1
            test_records(p, q, n - d, tot[keep], r["bal"].ravel()[keep], r["E"].ravel()[keep], r["F"].ravel()[keep],
                         tabs, tally, ex, controls=False, tag=f"depth{d}")
        r = pats[0]
        for k in range(len(W)):
            Es = bits_to_set(r["E"][k, 0])
            Fs = bits_to_set(r["F"][k, 0])
            t = int(r["tot"][k, 0])
            ukey = len(Es | Fs)
            if not r["bal"][k, 0]:
                nontriv[("unbalanced, |E u F| =", ukey)] = nontriv.get(("unbalanced, |E u F| =", ukey), 0) + 1
                continue
            val, x, a0, kp = rule(p, q, n, Es, Fs | {0})
            if x is None:
                thm.add("Theorem A lower bound", 1, t < val)
            else:
                thm.add("Proposition 7", 1, t < q * p ** (len(Es) + kp))
                thm.add(f"Theorem B lower bound (x={x}, k'={'0' if kp == 0 else '>=1'})", 1, t < val)
                if t == val:
                    thm.add(f"   ... of which with |A| equal to the claimed least size (x={x})", 1, 0)
                if x == 1 and t < val + q * p ** len(Es):
                    thm.add("   ... x=1 patterns with |A| < claimed + q p^e (the next possible size)", 1, 0)
    print(f"=== random structured: p={p} q={q} n={n} (Z_{p ** n * q}), {K} multisets, totals up to {B}, seed {seed} ===")
    tally.report("  ")
    thm.report("  ")
    print("  root patterns of the unbalanced ones:", sorted(nontriv.items()))
    if ex:
        print("  COUNTEREXAMPLE RECORDS:", ex[:10])
    print(f"  time {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
