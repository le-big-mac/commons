# Referee's test of Theorem U on abstract valued families with several systems of values.
# Written from the statement (theorem-twice.md, section 1, and the note); imports nothing of the author's.
# All signings; exact integers.
#
# A family: m elements; element i has a position u_i in Z_(2^k) and, for each e in E, a value in the
# group V_e = product of Z/q (q >= 2) and Z (written q = 0).  Events (sets of signings s, bit i of s
# set = sign -1 on element i):
#   Fe[d][e]  every class at depth d has sigma = 0 in V_e
#   Le[j][e]  j = 0: sigma(B) = 0 in V_e (computed on its own, not as Fe[0]);
#             j >= 1: every class at depth j-1 has equal half sums in V_e
#   B_j = union over e of Le[j][e];   G_d = union over e of Fe[d][e]
# Checked: G_0 = B_0; (a') G_d subset G_(d-1); (b') s in B_j iff tau_j(s) in G_(j-1), and the counts;
#          (c') G_j subset B_j and B_0; |B_0 or .. or B_k| <= 2 |B_0| - |G_k|.
# Deliberately false variants, counted: factor 3/2; - 2|G_k|; |B_j| = |G_j|;
#          "every class, some e" in place of "some e, every class" (in B_j, and in G_k);
#          tau_(j+1) in place of tau_j.
import sys, time, itertools, random
import numpy as np

_sg = {}
def signs(m):
    if m not in _sg:
        _sg[m] = np.array([[-1 if (s >> i) & 1 else 1 for i in range(m)] for s in range(1 << m)],
                          dtype=np.int64).reshape(1 << m, m)
    return _sg[m]

class Tally:
    def __init__(self):
        self.fam = 0
        self.fail = dict(main=0, G0=0, a=0, bset=0, bcount=0, c=0)
        self.var = dict(f32=0, m2G=0, bcountGj=0, Bstar=0, Gstar=0, tauwrong=0)
        self.eq = 0
        self.eq2 = 0
        self.Gk_pos = 0
        self.maxratio = (0, 1)
        self.union_strict = 0     # families where the union over e is strictly less than the sum over e
    def line(self, name):
        from math import gcd
        g = gcd(*self.maxratio) or 1
        return (f"{name}: families {self.fam}; failures {self.fail}; equality {self.eq}; "
                f"|union| = 2|B_0| > 0 in {self.eq2}; G_k nonempty in {self.Gk_pos}; "
                f"largest |union|/|B_0| = {self.maxratio[0]//g}/{self.maxratio[1]//g}; "
                f"families where the count for 'some e' is below the sum over e of the counts: {self.union_strict}; "
                f"false variants failing: {self.var}")

def check(k, pos, systems, T):
    """pos: list of positions; systems: list of (moduli tuple, list of value tuples)."""
    m = len(pos)
    sg = signs(m)
    S = 1 << m
    sidx = np.arange(S)
    nE = len(systems)
    posa = np.array(pos, dtype=np.int64)
    # zero[(kind, level, e)] : array (S, number of classes) of booleans "this class's condition holds"
    Fc, Lc, L0 = {}, {}, {}
    for e, (mods, vals) in enumerate(systems):
        va = np.array(vals, dtype=np.int64).reshape(m, len(mods))
        for d in range(k + 1):
            ok = np.ones((S, 2 ** d), dtype=bool)
            ind = (posa[:, None] % 2 ** d == np.arange(2 ** d)[None, :]).astype(np.int64)   # (m, classes)
            for c, q in enumerate(mods):
                R = sg @ (ind * va[:, c:c + 1])
                if q:
                    R = R % q
                ok &= (R == 0)
            Fc[(d, e)] = ok
        ok0 = np.ones(S, dtype=bool)
        for c, q in enumerate(mods):
            R = sg @ va[:, c]
            if q:
                R = R % q
            ok0 &= (R == 0)
        L0[e] = ok0
        for j in range(1, k + 1):
            ok = np.ones((S, 2 ** (j - 1)), dtype=bool)
            rem = posa % 2 ** j
            cl = np.arange(2 ** (j - 1))
            ind = ((rem[:, None] == cl[None, :]).astype(np.int64)
                   - (rem[:, None] == cl[None, :] + 2 ** (j - 1)).astype(np.int64))
            for c, q in enumerate(mods):
                R = sg @ (ind * va[:, c:c + 1])
                if q:
                    R = R % q
                ok &= (R == 0)
            Lc[(j, e)] = ok
    false = np.zeros(S, dtype=bool)
    def union(arrs):
        r = false.copy()
        for a in arrs:
            r |= a
        return r
    Bj = [union(L0[e] for e in range(nE))]
    Bstar = [Bj[0]]
    for j in range(1, k + 1):
        Bj.append(union(Lc[(j, e)].all(axis=1) for e in range(nE)))
        if nE:
            anye = np.zeros((S, 2 ** (j - 1)), dtype=bool)
            for e in range(nE):
                anye |= Lc[(j, e)]
            Bstar.append(anye.all(axis=1))
        else:
            Bstar.append(false.copy())
    Gd = [union(Fc[(d, e)].all(axis=1) for e in range(nE)) for d in range(k + 1)]
    if nE:
        anye = np.zeros((S, 2 ** k), dtype=bool)
        for e in range(nE):
            anye |= Fc[(k, e)]
        Gstar = anye.all(axis=1)
    else:
        Gstar = false.copy()
    T.fam += 1
    if (Gd[0] != Bj[0]).any():
        T.fail["G0"] += 1
    for j in range(1, k + 1):
        mask = 0
        maskw = 0
        for i, u in enumerate(pos):
            if u % 2 ** j >= 2 ** (j - 1):
                mask |= 1 << i
            if j < k and u % 2 ** (j + 1) >= 2 ** j:
                maskw |= 1 << i
        if (Gd[j] & ~Gd[j - 1]).any():
            T.fail["a"] += 1
        if (Bj[j] != Gd[j - 1][sidx ^ mask]).any():
            T.fail["bset"] += 1
        if j < k and (Bj[j] != Gd[j - 1][sidx ^ maskw]).any():
            T.var["tauwrong"] += 1
        if Bj[j].sum() != Gd[j - 1].sum():
            T.fail["bcount"] += 1
        if Bj[j].sum() != Gd[j].sum():
            T.var["bcountGj"] += 1
        if (Gd[j] & ~(Bj[j] & Bj[0])).any():
            T.fail["c"] += 1
    U = union(Bj)
    nu, n0, gk = int(U.sum()), int(Bj[0].sum()), int(Gd[k].sum())
    if nu > 2 * n0 - gk:
        T.fail["main"] += 1
    if nu == 2 * n0 - gk:
        T.eq += 1
    if n0 > 0 and nu == 2 * n0:
        T.eq2 += 1
    if gk:
        T.Gk_pos += 1
    if n0 > 0 and nu * T.maxratio[1] > T.maxratio[0] * n0:
        T.maxratio = (nu, n0)
    if 2 * nu > 3 * n0:
        T.var["f32"] += 1
    if nu > 2 * n0 - 2 * gk:
        T.var["m2G"] += 1
    if int(union(Bstar).sum()) > 2 * n0 - gk:
        T.var["Bstar"] += 1
    if nu > 2 * n0 - int(Gstar.sum()):
        T.var["Gstar"] += 1
    # is "some e" really less than adding the e up?  (sum over e of the single-e unions)
    tot = 0
    for e in range(nE):
        ue = L0[e].copy()
        for j in range(1, k + 1):
            ue |= Lc[(j, e)].all(axis=1)
        tot += int(ue.sum())
    if nu < tot:
        T.union_strict += 1

def group_elems(mods, zrange=(-1, 0, 1)):
    comps = [list(range(q)) if q else list(zrange) for q in mods]
    return list(itertools.product(*comps))

def exhaustive(name, k, groups, mmax, limit, zrange=(-1, 0, 1)):
    """every multiset of at most mmax elements; an element type is (position, value in each V_e)."""
    t0 = time.time()
    elems = [group_elems(g, zrange) for g in groups]
    types = list(itertools.product(range(2 ** k), *elems))
    T = Tally()
    cut = False
    for m in range(0, mmax + 1):
        for fam in itertools.combinations_with_replacement(types, m):
            if T.fam % 500 == 0 and time.time() - t0 > limit:
                cut = True
                break
            pos = [t[0] for t in fam]
            systems = [(g, [t[1 + e] for t in fam]) for e, g in enumerate(groups)]
            check(k, pos, systems, T)
        if cut:
            break
    print(T.line(f"exhaustive {name}: k={k} groups={groups} types={len(types)} m<={mmax}"
                 + (" CUT OFF BY TIME" if cut else "")), f"[{time.time()-t0:.0f}s]", flush=True)

GROUPS = [(2,), (3,), (4,), (6,), (0,), (2, 2), (2, 4), (0, 2), (3, 3), (0, 0)]

def rand_runs(seed, count, limit):
    rnd = random.Random(seed)
    t0 = time.time()
    T = Tally()
    while T.fam < count and time.time() - t0 < limit:
        k = rnd.choice((0, 1, 1, 2, 2, 2, 3, 3, 4))
        m = rnd.randint(0, 10)
        nE = rnd.choice((0, 1, 2, 2, 3, 3, 4, 6))
        style = rnd.random()
        if style < 0.3:      # few positions
            pool = [rnd.randrange(2 ** k) for _ in range(rnd.choice((1, 2, 3)))]
            pos = [rnd.choice(pool) for _ in range(m)]
        else:
            pos = [rnd.randrange(2 ** k) for _ in range(m)]
        systems = []
        for e in range(nE):
            g = rnd.choice(GROUPS)
            els = group_elems(g, (-2, -1, 0, 1, 2))
            st = rnd.random()
            if st < 0.35:    # few values, so that coincidences are common
                pool = [rnd.choice(els) for _ in range(rnd.choice((1, 2)))]
                vals = [rnd.choice(pool) for _ in range(m)]
            elif st < 0.5:   # many zeros
                zero = tuple(0 for _ in g)
                vals = [zero if rnd.random() < 0.5 else rnd.choice(els) for _ in range(m)]
            else:
                vals = [rnd.choice(els) for _ in range(m)]
            systems.append((g, vals))
        check(k, pos, systems, T)
    print(T.line(f"random seed={seed} (k<=4, m<=10, |E| in 0..6, groups {GROUPS})"), f"[{time.time()-t0:.0f}s]", flush=True)

if __name__ == "__main__":
    part = sys.argv[1]
    if part == "edge":
        T = Tally()
        for k in (0, 1, 2, 3):
            check(k, [], [], T)                              # empty family, empty E
            check(k, [], [((2,), []), ((3,), [])], T)        # empty family, two systems
            check(k, [0, 1 % 2 ** k], [], T)                 # two elements, empty E
        print(T.line("edge cases (empty family, empty E)"))
    elif part == "ex1":
        exhaustive("A", 0, [(2,), (3,)], 8, 60)
        exhaustive("B", 1, [(2,), (3,)], 5, 100)
        exhaustive("C", 2, [(2,), (2,), (2,)], 3, 100)
    elif part == "ex2":
        exhaustive("D", 2, [(3,), (4,)], 3, 120)
        exhaustive("E", 3, [(2,), (0,)], 3, 120)
    elif part == "ex3":
        exhaustive("F", 1, [(4,), (6,), (0,)], 2, 60)
        exhaustive("G", 2, [(2, 2), (3,)], 3, 150)
        exhaustive("H", 3, [(2,), (3,)], 3, 60)
    elif part == "rand":
        rand_runs(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
    elif part == "ex4":
        exhaustive("D4", 2, [(3,), (4,)], 4, 110)
    elif part == "ex5":
        exhaustive("I", 2, [(2,), (3,), (0,)], 3, 110, zrange=(-1, 0, 1))
