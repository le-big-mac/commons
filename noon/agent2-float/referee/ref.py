"""Referee's own code (blind). Uniform unit cube / unit square, relative density d.

Method: for up-vector n (any length), the height along up of a uniform random point of the
body is Y = sum_i |n_i| X_i with X_i ~ U(-1/2,1/2).  With s measured from the lowest corner,
   V(s)  = P(Y <= s)        = 1/(k! prod a) * sum_S (-1)^|S| (s - a_S)_+^k
   M0(s) = E[Y_from_corner; Y<=s] = 1/(k! prod a) * sum_S (-1)^|S| [k/(k+1) (s-a_S)_+^(k+1) + a_S (s-a_S)_+^k]
where a = nonzero |n_i| (k of them), a_S = sum over subset S.  Solve V(s)=d, then
   h = [ (sum a)/2 - M0(s)/d ] / |n|.
Exact zeros in n are dropped (exact reduction to a prism / slab).
Three implementations: python float, Decimal(60 digits), numpy longdouble (vectorised, all comps nonzero).
Independent brute force: convex clipping (scipy ConvexHull) and sorted quasi-random points.
"""
import math, itertools
from decimal import Decimal as D, getcontext
import numpy as np

getcontext().prec = 60


def _subsets(k):
    out = []
    for r in range(k + 1):
        for S in itertools.combinations(range(k), r):
            out.append(S)
    return out


SUBS = {k: _subsets(k) for k in (1, 2, 3)}
FACT = {1: 1, 2: 2, 3: 6}


def _VM(s, a, zero):
    k = len(a)
    tV = zero; tM = zero; tdV = zero
    for S in SUBS[k]:
        aS = zero
        for i in S:
            aS = aS + a[i]
        t = s - aS
        if t <= 0:
            continue
        sg = -1 if (len(S) & 1) else 1
        tk1 = t ** (k - 1)
        tk = tk1 * t
        tV = tV + sg * tk
        tM = tM + sg * (tk * t * k / (k + 1) + aS * tk)
        tdV = tdV + sg * k * tk1
    den = FACT[k]
    for x in a:
        den = den * x
    return tV / den, tM / den, tdV / den


def h_float(n, d):
    """h for up-vector n (need not be unit), python floats."""
    a = [abs(float(x)) for x in n]
    norm = math.sqrt(sum(x * x for x in a))
    a = [x for x in a if x > 0.0]
    tot = sum(a)
    lo, hi = 0.0, tot
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        if _VM(mid, a, 0.0)[0] < d:
            lo = mid
        else:
            hi = mid
    s = 0.5 * (lo + hi)
    V, M, dV = _VM(s, a, 0.0)
    # one Newton correction of M for the residual in V (M' = s V')
    M = M + s * (d - V)
    return (tot / 2 - M / d) / norm


def h_dec(n, d):
    """h for up-vector n, Decimal arithmetic (60 digits). n, d: Decimal or anything D() accepts."""
    n = [abs(D(x)) for x in n]
    d = D(d)
    norm = sum(x * x for x in n).sqrt()
    a = [x for x in n if x != 0]
    tot = sum(a)
    zero = D(0)
    # start from float bisection
    af = [float(x) for x in a]
    lo, hi = 0.0, float(tot)
    df = float(d)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        if _VM(mid, af, 0.0)[0] < df:
            lo = mid
        else:
            hi = mid
    # widen bracket and bisect/Newton in Decimal
    s = D(0.5 * (lo + hi))
    blo, bhi = zero, tot
    for it in range(200):
        V, M, dV = _VM(s, a, zero)
        r = V - d
        if r < 0:
            blo = s
        else:
            bhi = s
        if abs(r) < D(10) ** (-52):
            break
        if dV > 0:
            s2 = s - r / dV
        else:
            s2 = (blo + bhi) / 2
        if not (blo < s2 < bhi):
            s2 = (blo + bhi) / 2
        s = s2
    V, M, dV = _VM(s, a, zero)
    M = M + s * (d - V)
    return (tot / 2 - M / d) / norm


def h_vec(a, b, c, d):
    """Vectorised longdouble; a,b,c arrays of components (all must be nonzero), d scalar."""
    LD = np.longdouble
    a = np.abs(np.asarray(a, LD)); b = np.abs(np.asarray(b, LD)); c = np.abs(np.asarray(c, LD))
    comp = [a, b, c]
    norm = np.sqrt(a * a + b * b + c * c)
    tot = a + b + c
    d = LD(d)

    def VM(s):
        tV = 0; tM = 0
        for S in SUBS[3]:
            aS = 0
            for i in S:
                aS = aS + comp[i]
            t = np.maximum(s - aS, 0)
            sg = -1 if (len(S) & 1) else 1
            t3 = t * t * t
            tV = tV + sg * t3
            tM = tM + sg * (t3 * t * LD(3) / LD(4) + aS * t3)
        den = 6 * a * b * c
        return tV / den, tM / den

    lo = np.zeros_like(tot); hi = tot.copy()
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        V, _ = VM(mid)
        m = V < d
        lo = np.where(m, mid, lo); hi = np.where(m, hi, mid)
    s = 0.5 * (lo + hi)
    V, M = VM(s)
    M = M + s * (d - V)
    return (tot / 2 - M / d) / norm


# ---------------- independent brute force 1: convex clipping ----------------
def clip_h(n, d):
    from scipy.spatial import ConvexHull
    from scipy.optimize import brentq
    n = np.asarray(n, float); n = n / np.linalg.norm(n)
    verts = np.array(list(itertools.product([-0.5, 0.5], repeat=3)))
    edges = [(i, j) for i in range(8) for j in range(i + 1, 8)
             if np.sum(np.abs(verts[i] - verts[j]) > 0) == 1]

    def poly(L):
        hv = verts @ n - L
        pts = [verts[i] for i in range(8) if hv[i] <= 0]
        for i, j in edges:
            if (hv[i] < 0) != (hv[j] < 0) and hv[i] != hv[j]:
                t = hv[i] / (hv[i] - hv[j])
                pts.append(verts[i] + t * (verts[j] - verts[i]))
        return np.array(pts)

    def volcen(L):
        P = poly(L)
        if len(P) < 4:
            return 0.0, np.zeros(3)
        try:
            hull = ConvexHull(P)
        except Exception:
            return 0.0, np.zeros(3)
        c0 = P.mean(axis=0)
        vol = 0.0; cen = np.zeros(3)
        for simp in hull.simplices:
            A, B, C = P[simp]
            v = abs(np.dot(A - c0, np.cross(B - c0, C - c0))) / 6
            vol += v
            cen += v * (A + B + C + c0) / 4
        return vol, cen / vol

    Lmax = np.sum(np.abs(n)) / 2
    L = brentq(lambda L: volcen(L)[0] - d, -Lmax + 1e-9, Lmax - 1e-9, xtol=1e-15, rtol=1e-15)
    vol, cen = volcen(L)
    return -float(n @ cen)


# ---------------- independent brute force 2: sorted points ----------------
def points_h(n, d, N=160):
    n = np.asarray(n, float); n = n / np.linalg.norm(n)
    g = (np.arange(N) + 0.5) / N - 0.5
    X, Y, Z = np.meshgrid(g, g, g, indexing='ij')
    y = (n[0] * X + n[1] * Y + n[2] * Z).ravel()
    y.sort()
    m = int(round(d * y.size))
    return -float(y[:m].mean())


def unit(n):
    n = np.asarray(n, float)
    return n / np.linalg.norm(n)


if __name__ == '__main__':
    rng = np.random.default_rng(7)
    worst = 0
    print("check closed form (float, Decimal) against clipping and sorted points")
    for trial in range(40):
        n = rng.normal(size=3)
        if trial % 5 == 0:
            n[rng.integers(3)] = 0.0       # prism case
        if trial % 7 == 0:
            n = np.array([1.0, 1e-3 * rng.random(), 0.3 * rng.random()])
        d = rng.uniform(0.02, 0.98)
        hf = h_float(n, d); hd = float(h_dec([D(float(x)) for x in n], D(float(d))))
        hc = clip_h(n, d)
        hp = points_h(n, d, 100)
        worst = max(worst, abs(hf - hc), abs(hd - hc))
        if trial < 8:
            print(f"  d={d:.3f} float={hf:.13f} dec={hd:.13f} clip={hc:.13f} points={hp:.6f}")
    print("worst |closed - clip| over 40 trials:", worst)
    for n in [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0.3, 0)]:
        for d in (0.1, 0.22, 0.5):
            print(n, d, h_float(n, d), float(h_dec(n, D(str(d)))), clip_h(n, d) if True else None)
