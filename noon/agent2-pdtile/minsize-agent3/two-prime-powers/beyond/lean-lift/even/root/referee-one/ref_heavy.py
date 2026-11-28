# Referee's own: one heavy element (h copies of 0) and a decoration D given with multiplicities.
# From the definition: with t the signed sum of the heavy copies and Q the signed mask of D, the signing is bad at d
# iff t + Q = 0 modulo Phi_d, i.e. the remainder of Q modulo Phi_d is the constant -t.  For every vector of signed sums
# of D the set of such integers over all d | n is collected; A[v] = number of signings of D with v in the set.
# Then K_parity = sum over v of that parity of A[v] / 2^r, and the exact bad share for h copies is
# sum_v A[v] P_h(v) / 2^r.
import sys, math, json
from fractions import Fraction as Fr
import numpy as np
from ref_test import powers, divisors

def heavy(n, deco, chunk=150000):
    res = sorted(deco)
    assert 0 not in res
    hs = [deco[b] for b in res]
    r = sum(hs)
    divs = divisors(n)
    dims = [hb + 1 for hb in hs]
    K = 1
    for x in dims:
        K *= x
    A = {}
    Ms = []
    for d in divs:
        Ms.append(powers(d)[[b % d for b in res]])
    SENT = 10 ** 9
    for start in range(0, K, chunk):
        idx = np.arange(start, min(K, start + chunk))
        T = np.empty((len(idx), len(res)), dtype=np.int64)
        W = np.ones(len(idx), dtype=object)
        rem = idx.copy()
        for col in range(len(res) - 1, -1, -1):
            dig = rem % dims[col]
            rem //= dims[col]
            T[:, col] = 2 * dig - hs[col]
            w = np.array([math.comb(hs[col], i) for i in range(hs[col] + 1)], dtype=object)
            W = W * w[dig]
        vals = np.full((len(idx), len(divs)), SENT, dtype=np.int64)
        for k_, Md in enumerate(Ms):
            V = T @ Md
            ok = ~V[:, 1:].any(axis=1) if V.shape[1] > 1 else np.ones(len(idx), dtype=bool)
            vals[ok, k_] = -V[ok, 0]
        vals.sort(axis=1)
        first = np.ones(vals.shape, dtype=bool)
        first[:, 1:] = vals[:, 1:] != vals[:, :-1]
        first &= vals != SENT
        rows, cols = np.nonzero(first)
        vv = vals[rows, cols]
        for v in np.unique(vv):
            A[int(v)] = A.get(int(v), 0) + int(W[rows[vv == v]].sum())
    return r, A

def Kpar(r, A, par):
    return Fr(sum(a for v, a in A.items() if (v - par) % 2 == 0), 2 ** r)

def share(r, A, h):
    tot = 0
    for v, a in A.items():
        if (v - h) % 2 == 0 and abs(v) <= h:
            tot += a * math.comb(h, (h + v) // 2)
    return Fr(tot, 2 ** (r + h))

FAM = {
 "Z3: 1,2 single": (3, {1: 1, 2: 1}),
 "Z15: one in each nonzero class mod 3 and 5": (15, {5: 1, 10: 1, 3: 1, 6: 1, 9: 1, 12: 1}),
 "Z105: one in each nonzero class mod 3, 5, 7": (105, {35: 1, 70: 1, 21: 1, 42: 1, 63: 1, 84: 1, 15: 1, 30: 1, 45: 1, 60: 1, 75: 1, 90: 1}),
 "Z3: pairs at 1,2": (3, {1: 2, 2: 2}),
 "Z9: pairs at 1,2,3,6": (9, {1: 2, 2: 2, 3: 2, 6: 2}),
 "Z9: pairs at 1,2; fours at 3,6": (9, {1: 2, 2: 2, 3: 4, 6: 4}),
 "Z27: pairs at 1,2,3,6,9,18": (27, {1: 2, 2: 2, 3: 2, 6: 2, 9: 2, 18: 2}),
 "Z27: pairs at 1,2,3,6; fours at 9,18": (27, {1: 2, 2: 2, 3: 2, 6: 2, 9: 4, 18: 4}),
 "Z45: pairs at 5,10,15,30 and 9,18,27,36": (45, {5: 2, 10: 2, 15: 2, 30: 2, 9: 2, 18: 2, 27: 2, 36: 2}),
 "Z135: pairs 5,10,15,30; fours 45,90; pairs 27,54,81,108": (135, {5: 2, 10: 2, 15: 2, 30: 2, 45: 4, 90: 4, 27: 2, 54: 2, 81: 2, 108: 2}),
 "Z135: pairs 5,10,15,30; fours 45,90; fours 27,54,81,108": (135, {5: 2, 10: 2, 15: 2, 30: 2, 45: 4, 90: 4, 27: 4, 54: 4, 81: 4, 108: 4}),
 "Z81: pairs at 1,2,3,6,9,18,27,54": (81, {1: 2, 2: 2, 3: 2, 6: 2, 9: 2, 18: 2, 27: 2, 54: 2}),
 "Z105: pairs in each nonzero class mod 3, 5; singles mod 7": (105, {35: 2, 70: 2, 21: 2, 42: 2, 63: 2, 84: 2, 15: 1, 30: 1, 45: 1, 60: 1, 75: 1, 90: 1}),
}

if __name__ == "__main__":
    names = sys.argv[2:] if len(sys.argv) > 2 else list(FAM)
    bounds = json.load(open(sys.argv[1]))     # my floating point table: sqrt(m) B, B_E, B3
    worst = {"odd": (0, None), "even": (0, None)}
    for name in FAM:
        if not any(name.startswith(x) for x in names):
            continue
        n, deco = FAM[name]
        r, A = heavy(n, deco)
        ks, ko = Kpar(r, A, r % 2), Kpar(r, A, (r + 1) % 2)
        print("%s: r = %d, values v: %s" % (name, r, sorted(A)))
        print("   K_same (m even) = %s = %.6f   K_other (m odd) = %s = %.6f" % (ks, float(ks), ko, float(ko)))
        line = []
        for h in list(range(1, 60)) + list(range(60, 3000 - r, 37)) + [2999 - r, 3000 - r]:
            m = r + h
            s = share(r, A, h)
            par = "odd" if m % 2 else "even"
            v = float(s) * math.sqrt(m)
            const = 1.0 if m % 2 else 1.56
            ok = (m * s * s < 1) if m % 2 else (m * s * s <= Fr(156, 100) ** 2)
            if not ok:
                print("   FAILURE of Theorem 5 at m =", m, "share", s)
            msg = ""
            for key in ("B", "BE", "B3"):
                tab = bounds[key]
                if str(m) in tab and m >= 47:
                    if v > tab[str(m)] * (1 + 1e-12):
                        print("   FAILURE: share above %s at m = %d" % (key, m))
            if v / const > worst[par][0]:
                worst[par] = (v / const, (name, m, v))
            if h in (9, 10, 39, 40, 2999 - r, 3000 - r) or m in (47, 48):
                line.append("m=%d: %.4f" % (m, v))
        print("   sqrt(m)*share at some m:", "; ".join(line))
        sys.stdout.flush()
    print("largest sqrt(m)*share/claimed constant met: odd", worst["odd"], " even", worst["even"])
