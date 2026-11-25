# Referee's own free-group code. Generators x_j = anticlockwise loop round the rod in place j,
# tethered straight from a base point far below. Derived by hand:
#   s_i (clockwise swap of places i,i+1; left rod goes over the top):
#        x_i -> x_i^-1 x_{i+1} x_i ,  x_{i+1} -> x_i
#   S_i (anticlockwise): x_i -> x_{i+1},  x_{i+1} -> x_{i+1} x_i x_{i+1}^-1
# Loop round places a,b (adjacent) anticlockwise = x_b x_a.
import sys, json
from fractions import Fraction

def reduce(w):
    out = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return out

def cyc(w):
    w = reduce(w)
    i, j = 0, len(w) - 1
    while i < j and w[i] == -w[j]:
        i += 1; j -= 1
    return w[i:j + 1]

def move_map(n, i, cw):
    m = {k: [k] for k in range(1, n + 1)}
    if cw:
        m[i] = [-i, i + 1, i]; m[i + 1] = [i]
    else:
        m[i] = [i + 1]; m[i + 1] = [i + 1, i, -(i + 1)]
    return m

def apply(w, m):
    out = []
    for a in w:
        if a > 0:
            out.extend(m[a])
        else:
            out.extend([-b for b in reversed(m[-a])])
    return out

def parse(dev):
    # "s1 S2" -> [(1,True),(2,False)]
    return [(int(t[1:]), t[0] == 's') for t in dev.split()]

def period(w, n, moves):
    for (i, cw) in moves:
        w = cyc(apply(w, move_map(n, i, cw)))
    return w

def lengths(n, dev, start, cap=2_000_000, maxper=200):
    moves = parse(dev)
    w = cyc(start)
    L = [len(w)]
    for k in range(maxper):
        w2 = period(w, n, moves)
        if len(w2) > cap:
            break
        w = w2
        L.append(len(w))
    return L

def berlekamp_massey(seq):
    # over rationals; returns connection polynomial C (C[0]=1): sum_j C[j] s[n-j] = 0
    s = [Fraction(x) for x in seq]
    C = [Fraction(1)]; B = [Fraction(1)]
    L = 0; m = 1; b = Fraction(1)
    for n in range(len(s)):
        d = s[n]
        for i in range(1, L + 1):
            d += C[i] * s[n - i]
        if d == 0:
            m += 1
        elif 2 * L <= n:
            T = C[:]
            coef = d / b
            C = C + [Fraction(0)] * (len(B) + m - len(C))
            for i, bv in enumerate(B):
                C[i + m] -= coef * bv
            L = n + 1 - L; B = T; b = d; m = 1
        else:
            coef = d / b
            C = C + [Fraction(0)] * (len(B) + m - len(C))
            for i, bv in enumerate(B):
                C[i + m] -= coef * bv
            m += 1
    return C[:L + 1]

DEVICES = [(3, "s1 S2"), (3, "s1 s1 S2 S2"), (3, "s1 s2"),
           (4, "s1 s2 S3"), (4, "s1 s3 S2"), (4, "s1 s3 S2 S2")]

if __name__ == "__main__":
    import numpy as np
    res = {}
    for n, dev in DEVICES:
        start = [2, 1]
        L = lengths(n, dev, start, maxper=60 if dev != "s1 s2" else 30)
        g = L[-1] / L[-2]
        C = berlekamp_massey(L)
        poly = [float(c) for c in C]
        roots = np.roots(poly) if len(poly) > 1 else []
        rmax = max(abs(r) for r in roots) if len(roots) else None
        print(f"n={n} {dev}: periods={len(L)-1} last L={L[-1]} growth={g:.8f}")
        print("   lengths:", L[:16])
        print("   recurrence (connection poly, C[0]=1):", [str(c) for c in C], " order", len(C) - 1,
              " largest root modulus", rmax)
        res[dev] = dict(n=n, L=L, growth=g, rec=[str(c) for c in C], rmax=float(rmax) if rmax else None)
    json.dump(res, open("/home/agent2/taffy/referee/words.json", "w"))
