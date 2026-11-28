# Referee's own program, written from the definitions in the text (result.md), not from the author's code.
# c_r, patterns, cnt(N), gamma(m,N), B(m), B_E(m), B3(m).
import sys, math
from fractions import Fraction as Fr
import numpy as np

def primes_upto(n):
    return [p for p in range(3, n + 1, 2) if all(p % q for q in range(3, int(p ** .5) + 1, 2))]

# ---------- patterns ----------
def plain_patterns(Nmax):
    """list every pattern (dict prime->rank) with N(d*) <= Nmax, by depth-first search"""
    ps = primes_upto(Nmax)
    out = []
    def rec(i, pat, G, P):
        if pat:
            out.append((G + P - 1, dict(pat)))
        for k in range(i, len(ps)):
            p = ps[k]
            j = 1
            while True:
                g = max(G, 1 + (j - 1) * (p - 1))
                if g + p - 1 > Nmax:
                    break
                pat.append((p, j))
                rec(k + 1, pat, g, p)
                pat.pop()
                j += 1
    rec(0, [], 1, 0)
    return out

def Jn(q, g):
    return 1 + (g - 1) // (q - 1)

def Hc(P, g, ps):
    if g < 1:
        return 0
    v = Jn(P, g)
    for q in ps:
        if q < P:
            v *= 1 + Jn(q, g)
    return v

def cnt_formula(Nmax):
    ps = primes_upto(Nmax)
    cnt = {}
    for N in range(3, Nmax + 1, 2):
        t = 0
        for P in ps:
            if P > N:
                break
            G = N - P + 1
            t += Hc(P, G, ps) - Hc(P, G - 2, ps)
        cnt[N] = t
    return cnt

def cnt_pp(N, pmax=10**9):
    """number of prime power patterns p^j with N(p^j) = j(p-1)+1 = N"""
    return sum(1 for p in primes_upto(N) if (N - 1) % (p - 1) == 0)

# ---------- c ----------
def c_exact(L):
    c = [Fr(1)]
    for r in range(1, L + 1):
        c.append(Fr(math.comb(r, r // 2), 2 ** r))
    return c

def c_float(L):
    f = [1.0]
    for h in range(1, L // 2 + 2):
        f.append(f[-1] * (2 * h - 1) / (2 * h))
    c = [1.0] + [f[(r + 1) // 2] for r in range(1, L + 1)]
    return np.array(c)

class Calc:
    def __init__(self, c, exact):
        self.c = c
        self.exact = exact
        self.memo = {}
    def cc(self, x):
        return self.c[x] if x > 0 else self.c[0]
    def gamma(self, m, N):
        key = (m, N)
        if key in self.memo:
            return self.memo[key]
        if self.exact:
            best = None
            for r in range(1, (m - 1) // 2 + 1):
                v = 2 * self.c[r] * self.cc(max(m - 2 * r, r) - 2 * (N - 3))
                if best is None or v > best:
                    best = v
        else:
            r = np.arange(1, (m - 1) // 2 + 1)
            idx = np.maximum(np.maximum(m - 2 * r, r) - 2 * (N - 3), 0)
            best = float(np.max(2 * self.c[r] * self.c[idx]))
        self.memo[key] = best
        return best
    def LC(self, m, N):
        g = self.gamma(m, N)
        return g / (2 ** (N - 2)) if self.exact else g * 2.0 ** (-(N - 2))
    def Fb(self, m, p, k, g):
        smax = m - (-(-m // (p * k)))
        if self.exact:
            best = 0
            for s in range(0, smax + 1):
                v = self.c[m - s] * min(g, 2 * self.cc(-(-s // 2) - 2 * (k + p - 4)))
                if v > best:
                    best = v
            return best / 2 ** (k + p - 3)
        s = np.arange(0, smax + 1)
        idx = np.maximum((s + 1) // 2 - 2 * (k + p - 4), 0)
        v = self.c[m - s] * np.minimum(float(g), 2 * self.c[idx])
        return float(np.max(v)) * 2.0 ** (-(k + p - 3))
    def PPE(self, m, p, j):
        G = 1 + (j - 1) * (p - 1)
        if p >= 11:
            return self.LC(m, G + p - 1)
        q = max(2, p - 2)
        best = self.LC(m, G + q + p - 1)
        for k in range(G, G + q):
            g = Fr(1, 2 ** (p - 2))
            if p == 3 and j == 1 and k == 1:
                g = Fr(17, 64)
            v = min(self.LC(m, k + p - 1), self.Fb(m, p, k, g))
            if v > best:
                best = v
        return best

TAIL = 5.5e-5   # the text's bound for the sum over N >= 63 of cnt(N) sqrt(N) 2^-(N-2)
NTOP = 61

def B_parts(calc, m, cnt, exact):
    """returns (level0, list of (N, cnt, LC)) for odd N <= min(m, NTOP), and the tail term for m > NTOP"""
    lev0 = calc.cc(m) if m % 2 == 0 else 0
    terms = [(N, cnt[N], calc.LC(m, N)) for N in range(3, min(m, NTOP) + 1, 2)]
    tail = 0
    if m > NTOP:
        tail = math.sqrt(2 / (math.pi * m)) * TAIL
        if exact:
            tail = Fr(tail) + Fr(1, 10 ** 12)   # rounded up
    return lev0, terms, tail

def B(calc, m, cnt, exact):
    lev0, terms, tail = B_parts(calc, m, cnt, exact)
    return lev0 + sum(cn * lc for (_, cn, lc) in terms) + tail

def B3_odd(calc, m, cnt, exact):
    lev0, terms, tail = B_parts(calc, m, cnt, exact)
    # patterns 3^j : exactly one for each odd N >= 3; replaced by c_(m-2)/2 (first text, Theorem A)
    return sum((cn - 1) * lc for (_, cn, lc) in terms) + calc.cc(m - 2) / 2 + tail

def BE_parts(calc, m, cnt, exact):
    assert m % 2 == 0
    lev0 = calc.cc(m)
    comp = 0
    pp3 = 0
    ppo = 0
    for N in range(3, min(m, NTOP) + 1, 2):
        npp = 0
        for p in primes_upto(N):
            if (N - 1) % (p - 1) == 0:
                j = (N - 1) // (p - 1)
                npp += 1
                v = calc.PPE(m, p, j)
                if p == 3:
                    pp3 += v
                else:
                    ppo += v
        comp += (cnt[N] - npp) * calc.LC(m, N)
    tail = 0
    if m > NTOP:
        tail = math.sqrt(2 / (math.pi * m)) * TAIL
        if exact:
            tail = Fr(tail) + Fr(1, 10 ** 12)
    return lev0, comp, pp3, ppo, tail

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "counts":
        Nmax = int(sys.argv[2])
        pl = plain_patterns(Nmax)
        cp = {}
        for N, pat in pl:
            cp[N] = cp.get(N, 0) + 1
        cf = cnt_formula(61)
        print("N, cnt by plain list, cnt by formula, prime-power patterns")
        for N in range(3, Nmax + 1, 2):
            print(N, cp.get(N, 0), cf[N], cnt_pp(N), "EQUAL" if cp.get(N, 0) == cf[N] else "DIFFER")
        print("all N(d*) odd:", all(N % 2 == 1 for N, _ in pl))
        # N(d*) >= mu(d*)+1
        print("N >= mu+1 on the list:", all(N >= max(j * (p - 1) for p, j in pat.items()) + 1 for N, pat in pl))
        print("cnt(N), N = 3..61:", [cf[N] for N in range(3, 62, 2)])
        s1 = sum(Fr(cf[N], 2 ** (N - 2)) for N in range(3, 62, 2))
        sh = sum(cf[N] * math.sqrt(N) * 2.0 ** (-(N - 2)) for N in range(3, 62, 2))
        print("Sigma_1 up to N=61: %.9f   Sigma_h up to N=61: %.9f" % (float(s1), sh))
        # further, exact counts to N = 401, to see the true tails
        cf2 = cnt_formula(401)
        t1 = sum(Fr(cf2[N], 2 ** (N - 2)) for N in range(63, 402, 2))
        th = sum(cf2[N] * math.sqrt(N) * 2.0 ** (-(N - 2)) for N in range(63, 402, 2))
        print("exact terms 63..401: Sigma_1 part %.3e  Sigma_h part %.3e" % (float(t1), th))
        # check cnt(N) <= A(N-1) and the bound A(t) 2^-t <= (u+1) x^u for t <= 400
        x = 0.5783
        ok = True
        ok2 = True
        for N in range(3, 402, 2):
            t = N - 1
            A = 1
            for p in primes_upto(t + 1):
                A *= 1 + t // (p - 1)
            u = t // 2
            if cf2[N] > A - 1:
                ok = False
            if A * 2.0 ** (-t) > (u + 1) * x ** u:
                ok2 = False
        print("cnt(N) <= A(N-1) - 1 for N <= 401:", ok, "  A(t) 2^-t <= (u+1) x^u for t <= 400:", ok2)
        # the tail bound of the text
        u = 31
        first = 2 * math.sqrt(2 * u + 1) * (u + 1) * x ** u
        print("first tail term (u=31) %.4e, /(1-0.607) = %.4e" % (first, first / (1 - 0.607)))
        K = sum(math.log(1 + 1 / k) / k for k in range(1, 2000000))
        print("K partial (k<2e6) = %.7f, x = exp(2K/3)/4 <= %.6f" % (K, math.exp(2 * (K + 1 / 1999999) / 3) / 4))
        r2p = math.sqrt(2 / math.pi)
        print("sqrt(2/pi)(1+Sigma_h) <= %.6f ; sqrt(2/pi) Sigma_1 <= %.6f" % (r2p * (1 + sh + TAIL), r2p * (float(s1) + TAIL)))
        ppsum = sum(2 / (2 ** (p - 1) - 1) for p in primes_upto(200))
        ppfac = sum(2 / (2 ** (p - 1) - 1) * (1 - 2.0 ** (-(p - 2))) for p in primes_upto(200))
        se = float(s1) + TAIL - ppfac - (0.25 - 17 / 128)
        print("prime powers: sum 2^-(N-2) = %.6f, with factor (1-2^-(p-2)): %.6f; Sigma_even <= %.6f; sqrt(2/pi)(1+Sigma_even) <= %.6f"
              % (ppsum, ppfac, se, r2p * (1 + se)))
        print("sqrt(2/pi)(Sigma_1 - 1/6) <= %.6f" % (r2p * (float(s1) + TAIL - 1 / 6)))
    elif what == "float":
        M = int(sys.argv[2])
        cnt = cnt_formula(61)
        calc = Calc(c_float(M + 5), False)
        resB = {}
        resBE = {}
        resB3 = {}
        for m in range(3, M + 1):
            calc.memo = {}
            resB[m] = B(calc, m, cnt, False) * math.sqrt(m)
            if m % 2 == 1:
                resB3[m] = B3_odd(calc, m, cnt, False) * math.sqrt(m)
            else:
                l0, comp, pp3, ppo, tail = BE_parts(calc, m, cnt, False)
                resBE[m] = (l0 + comp + pp3 + ppo + tail) * math.sqrt(m)
                resB3[m] = (l0 + comp + min(pp3, 309 / 8192) + ppo + tail) * math.sqrt(m)
        def mx(d, lo, hi, par):
            ks = [m for m in d if lo <= m <= hi and m % 2 == par]
            b = max(ks, key=lambda m: d[m])
            return "%.5f at m = %d" % (d[b], b)
        print("sqrt(m) B(m):")
        for lo, par in ((47, 1), (85, 1), (87, 1), (101, 1), (48, 0), (100, 0)):
            print("  max over m in [%d, %d], parity %d: %s" % (lo, M, par, mx(resB, lo, M, par)))
        print("  least odd m0 with sqrt(m)B(m) < 1 for all odd m in [m0, M]:",
              min(m0 for m0 in range(3, M + 1, 2) if all(resB[m] < 1 for m in range(m0, M + 1, 2))))
        print("  odd m with sqrt(m)B(m) >= 1 and m >= 60:", [m for m in range(61, M + 1, 2) if resB[m] >= 1])
        print("sqrt(m) B_E(m), even m:")
        for lo in (48, 50, 64, 114, 300, 1000, 3000):
            if lo <= M:
                print("  max over even m in [%d, %d]: %s" % (lo, M, mx(resBE, lo, M, 0)))
        print("sqrt(m) B3(m):")
        if M >= 400:
            print("  odd 47..400: %s" % mx(resB3, 47, 400, 1))
            print("  even 48..400: %s" % mx(resB3, 48, 400, 0))
            if M > 402:
                print("  even 402..%d of B_E: %s" % (M, mx(resBE, 402, M, 0)))
        print("  odd m in [47, 400] with sqrt(m) B3(m) >= 1:", [m for m in range(47, min(M, 400) + 1, 2) if resB3[m] >= 1])
        for m in (3, 4, 5, 24, 25, 26, 27, 28, 31, 46, 47, 48, 49, 50, 83, 85, 99, 100, 101, 400, 1000, 3000):
            if m <= M:
                print("  m = %4d  sqrt(m)B = %.6f  sqrt(m)B_E = %s  sqrt(m)B3 = %.6f" % (
                    m, resB[m], ("%.6f" % resBE[m]) if m in resBE else "-", resB3[m]))
        import json
        json.dump({"B": resB, "BE": resBE, "B3": resB3}, open(sys.argv[3], "w"))
    elif what == "exact":
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        cnt = cnt_formula(61)
        calc = Calc(c_exact(hi + 5), True)
        for m in range(lo, hi + 1):
            calc.memo = {}
            b = B(calc, m, cnt, True)
            if m % 2 == 1:
                b3 = B3_odd(calc, m, cnt, True)
                print("m = %3d odd   m B^2 < 1: %s   m B3^2 < 1: %s   sqrt(m)B = %.8f  sqrt(m)B3 = %.8f" % (
                    m, m * b * b < 1, m * b3 * b3 < 1, math.sqrt(m) * float(b), math.sqrt(m) * float(b3)))
            else:
                l0, comp, pp3, ppo, tail = BE_parts(calc, m, cnt, True)
                be = l0 + comp + pp3 + ppo + tail
                b3 = l0 + comp + min(pp3, Fr(309, 8192)) + ppo + tail
                K = Fr(15529, 10000)
                print("m = %3d even  m B3^2 < 1.5529^2: %s  m BE^2 < 1.5529^2: %s  sqrt(m)B = %.8f sqrt(m)B_E = %.8f sqrt(m)B3 = %.8f  pp3 = %.6f" % (
                    m, m * b3 * b3 < K * K, m * be * be < K * K, math.sqrt(m) * float(b), math.sqrt(m) * float(be),
                    math.sqrt(m) * float(b3), float(pp3)))
