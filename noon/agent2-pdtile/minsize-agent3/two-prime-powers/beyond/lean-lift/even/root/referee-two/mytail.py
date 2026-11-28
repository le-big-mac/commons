# Referee's check of the tail conditions (T0), (T2s), (T2l), (T3s), (T3l) of section 3 and of the constants of
# section 4 of two/result.md, in EXACT rational arithmetic (no floating-point comparison), from my own table
# mytable3-1000.txt.  kappa = sqrt(2/pi) is replaced by the rational upper bound KU = 0.797885; square roots are
# removed by squaring or replaced by rational bounds whose squares are checked.
import sys
from fractions import Fraction as F
from math import comb, isqrt
M0, R0, R1 = 1000, 400, 200
E = [0] * (M0 + 1)
for line in open("mytable3-1000.txt"):
    w = line.split(); E[int(w[0])] = int(w[1], 16)
c = [F(comb(r, r // 2), 1 << r) if r % 2 == 0 else F(0) for r in range(M0 + 1)]
e = [F(E[r], 1 << r) for r in range(M0 + 1)]
u = [c[r] + e[r] for r in range(M0 + 1)]
KU = F(797885, 10**6)
assert KU * KU * 314159266 >= 2 * 10**8          # KU^2 >= 2/3.14159266 > 2/pi  (pi < 3.14159266)
def check(a_ev, a_od):
    a = (F(a_ev), F(a_od)); amax = max(a); amin = min(a); out = []
    # (T0): E(r)^2 r <= a^2 for 200 < r <= 1000
    w = max(e[r] * e[r] * r / (a[r % 2] ** 2) for r in range(R1 + 1, M0 + 1)); out.append(("T0 (ratio squared)", w))
    # (T2s): sigma(r2)^2 X^2 <= a^2,  sigma^2 = 1001/(1001 - r2)
    worst = F(0); wa = None
    for r2 in range(1, R0 + 1):
        for p1 in (0, 1):
            X = a[p1] * u[r2] + (KU if p1 == 0 else 0) * e[r2]
            v = F(M0 + 1, M0 + 1 - r2) * X * X / a[(p1 + r2) % 2] ** 2
            if v > worst: worst = v; wa = (r2, p1)
    out.append((f"T2s (ratio squared) at (r2, parity r1) = {wa}", worst))
    # (T2l): 2 amax^2 (2 kappa + amax)^2 / R0 <= amin^2
    out.append(("T2l (ratio squared)", 2 * amax ** 2 * (2 * KU + amax) ** 2 / R0 / amin ** 2))
    # (T3s)
    worst = F(0); wa = None
    for r3 in range(1, R0 // 2 + 1):
        for r2 in range(r3, R0 - r3 + 1):
            for p1 in (0, 1):
                same = (r2 - r3) % 2 == 0 and (r2 - p1) % 2 == 0
                X = (KU * (c[r2 + r3] - c[r2] * c[r3]) if same else 0) + a[p1] * u[r2] * u[r3] \
                    + (KU if p1 == 0 else 0) * (u[r2] * u[r3] - c[r2] * c[r3])
                v = F(M0 + 1, M0 + 1 - r2 - r3) * X * X / a[(p1 + r2 + r3) % 2] ** 2
                if v > worst: worst = v; wa = (r2, r3, p1)
    out.append((f"T3s (ratio squared) at (r2, r3, parity r1) = {wa}", worst))
    # (T3l): kappa^2/sqrt(den) + sqrt3 (amax+kappa)^2 / (2 sqrt(R0/2)) <= amin
    den = min(F(2 * M0, 9), R0 * (1 - F(R0, M0)))
    lo = F(isqrt(int(den * 10**12)), 10**6); assert lo * lo <= den          # lo <= sqrt(den)
    s3 = F(isqrt(3 * 10**12) + 1, 10**6); assert s3 * s3 >= 3               # s3 >= sqrt 3
    l2 = F(isqrt(R0 // 2 * 10**12), 10**6); assert l2 * l2 <= R0 // 2       # l2 <= sqrt(R0/2)
    out.append(("T3l (ratio)", (KU * KU / lo + s3 * (amax + KU) ** 2 / (2 * l2)) / amin))
    ok = all(v <= 1 for _, v in out)
    print(f"a_even = {a_ev}, a_odd = {a_od}:")
    for name, v in out: print(f"   {name}: {float(v):.6f}  {'<= 1' if v <= 1 else 'FAILS'}")
    print("   ALL HOLD (exact rational comparison)" if ok else "   FAIL")
    return ok
check("0.14", "0.40")
check("0.138", "0.40")
check("0.14", "0.3995")
# u(r) <= 1/2 on the table (used in (T3l)); u(1) = 0
print("u(r) <= 1/2 for r <= 1000:", all(u[r] <= F(1, 2) for r in range(1, M0 + 1)), "; u(1) =", u[1])
# final constants of Theorem 1
print("kappa + 0.14 <= KU + 0.14 =", float(KU + F("0.14")), "< 0.9379:", KU + F("0.14") < F("0.9379"))
# q(r) sqrt(r) <= kappa: exact check of q(r)^2 r <= 2/3.14159266 < 2/pi for r <= 2000 (the text proves it for all r)
print("q(r)^2 r <= 2/3.14159266 for 1 <= r <= 2000:", all(F(comb(r, r // 2), 1 << r) ** 2 * r * 314159266 <= 2 * 10**8 for r in range(1, 2001)))
print("P(S_r = 2) <= 1/4 for even r <= 2000:", all(4 * comb(r, r // 2 + 1) <= (1 << r) for r in range(2, 2001, 2)))

# ---------------- section 4 ----------------
from decimal import Decimal as D, getcontext
getcontext().prec = 40
pi = D("3.14159265358979323846264338327950288419716939937510")
kap = (D(2) / pi).sqrt()
print("\nsection 4, 40 digits: kappa =", kap)
print(" two classes: r2=2:", D("0.5") * (D(7) / 5).sqrt(), " r2=3,4:", D("0.375") * (D(9) / 5).sqrt(), " 5<=r2<p:", D("0.375") * D(2).sqrt())
print("   r2>=p odd:", D(2).sqrt() * (D("0.25") + kap / D(5).sqrt()), "  r2>=p even:", D(2).sqrt() * (D("0.375") + kap / D(6).sqrt()))
vals = [(j, D("0.75") ** (j - 1) * (D("0.375") + j * kap / D(5).sqrt())) for j in range(1, 60)]
print(" max over j of (3/4)^(j-1)(3/8 + j kappa/sqrt5):", max(vals, key=lambda t: t[1]), " <= 0.8165:", max(v for _, v in vals) <= D("0.8165"))
print(" top term: kappa (3/4)^(p-2) <= 1/2 at p=5:", kap * D("0.75") ** 3, "; kappa 2^(3-p) <= 1 at p=5:", kap / 4)
def isprime(x): return x > 1 and all(x % t for t in range(2, int(x ** 0.5) + 1))
tot = D(0)
for p in range(5, 400):
    if isprime(p):
        tau = D(p).sqrt() * D(2) ** (1 - p); th = D("0.8165") * D(p).sqrt() * D(2) ** (2 - p); a = tau / (1 - th); tot += a
        if p <= 19: print(f" p={p}: tau = {tau:.8f} theta = {th:.6f} a_p = {a:.8f}  kappa + a_p = {kap + a:.6f}")
tailb = sum(D(p).sqrt() * D(2) ** (1 - p) * 2 for p in range(401, 600))   # crude bound for the primes >= 401
print(" sum of a_p over primes 5 <= p < 400 =", f"{tot:.8f}", "; beyond at most", f"{tailb:.2e}", "; claimed 0.22964:", tot + tailb <= D("0.22964"))
print(" Corollary 4: 0.9487 + sum =", D("0.9487") + tot, " 0.4331 + sum =", D("0.4331") + tot)

# ---------------- own tables for p = 5 and p = 7 (exact), from Lemma 2 ----------------
def parts(m, k, lo=1):
    if k == 1:
        if m >= lo: yield (m,)
        return
    for x in range(lo, m // k + 1):
        for rest in parts(m - x, k - 1, x): yield (x,) + rest
def table(p, M):
    cc = [comb(r, r // 2) if r % 2 == 0 else 0 for r in range(M + 1)]
    Ep = [0] * (M + 1); Up = cc[:]
    for m in range(2, M + 1):
        best = 0
        for k in range(2, min(p, m) + 1):
            for rs in parts(m, k):
                pu = 1; pc = 1
                for r in rs: pu *= Up[r]; pc *= cc[r]
                t = pu - pc
                if k == p and len({r % 2 for r in rs}) == 1:
                    for v in range(-rs[0], rs[0] + 1):
                        if v != 0 and (v - rs[0]) % 2 == 0:
                            t0 = 1
                            for r in rs: t0 *= comb(r, (r + v) // 2)
                            t += t0
                best = max(best, t)
        Ep[m] = best; Up[m] = cc[m] + best
    return Ep
for p, M in ((5, int(sys.argv[1]) if len(sys.argv) > 1 else 50), (7, int(sys.argv[2]) if len(sys.argv) > 2 else 28)):
    Ep = table(p, M)
    tau2 = F(p, 4 ** (p - 1))                       # tau_p^2
    mx = max(range(1, M + 1), key=lambda m: F(Ep[m] ** 2 * m, 4 ** m))
    print(f"p = {p}, m <= {M}: E_p(m)^2 m <= tau_p^2 for every m: {all(F(Ep[m] ** 2 * m, 4 ** m) <= tau2 for m in range(1, M + 1))};"
          f" largest E_p sqrt(m) = {float(F(Ep[mx] ** 2 * mx, 4 ** mx)) ** 0.5:.6f} at m = {mx}; E_p(p..p+7) = {[str(F(Ep[m], 1 << m)) for m in range(p, p + 8)]}")
    with open(f"mytable{p}.txt", "w") as f:
        for m in range(1, M + 1): f.write(f"{m} {Ep[m]:x}\n")
