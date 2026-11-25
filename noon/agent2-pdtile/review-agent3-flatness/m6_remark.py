"""A side remark for the review (agent3 / Yonder): at M = 6 the set A = {0, 3} has a pd-tiling complement f
whose mask polynomial F fails (T1) as [KLMS] define it for functions (S_F = prime powers s | M with Phi_s | F;
(T1): F(1) = product of Phi_s(1) over S_F).  Exact arithmetic; the transform is computed in Q(w), w = exp(2 pi i/6),
with w^2 = w - 1, as pairs (a, b) = a + b w."""
from fractions import Fraction as Fr
M = 6
f = [Fr(1), Fr(3, 4), Fr(1, 4), Fr(0), Fr(1, 4), Fr(3, 4)]
A = [0, 3]
W = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]           # w^k for k = 0..5
def hat(g):                                                           # g^(xi) = sum g(z) w^(-z xi)
    out = []
    for xi in range(M):
        a = sum(g[z] * W[(-z * xi) % M][0] for z in range(M)); b = sum(g[z] * W[(-z * xi) % M][1] for z in range(M))
        out.append((a, b))
    return out
conv = [sum(f[(z - a) % M] for a in A) for z in range(M)]
fh = hat(f); Ah = hat([1 if z in A else 0 for z in range(M)])
print("f        =", [str(x) for x in f])
print("1_A * f  =", [str(x) for x in conv])
print("f^       =", [f"{a}+{b}w" if b else str(a) for a, b in fh], "(all real, >= 0)")
print("1_A^     =", [f"{a}+{b}w" if b else str(a) for a, b in Ah])
assert all(c == 1 for c in conv) and f[0] == 1 and min(f) >= 0 and all(b == 0 and a >= 0 for a, b in fh)
order = lambda xi: M // __import__("math").gcd(xi, M)
SF = sorted({order(xi) for xi in range(1, M) if fh[xi] == (0, 0)} & {2, 3})
print("F(1) =", fh[0][0], "; prime powers s | 6 with Phi_s | F:", SF, "; product of Phi_s(1) =", SF[0] * SF[1] if len(SF) == 2 else SF)
