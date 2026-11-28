"""The constants of result.md (Theorem 1).
For an odd e > 1 with exponents j_p and largest prime q put s(e) = max_p (j_p - 1)(p - 1) (even, >= 0),
  kappa(e) = s + q - 1,   kappa+(e) = kappa(e) for a prime power e and kappa(e) + 1 otherwise,
  need(e) = q + 2 s, and q + 1 if e has two or more primes and s = 0.
The e are counted by the pair (q, s): G(q, s) = number of e with largest prime q and s(e) = s; exactly one of them is a
prime power if (q - 1) | s (namely q^(1 + s/(q-1))), none otherwise.
c*_r = c_r for r >= 1 and 1/2 for r <= 0.
  Psi(m) = [m even] c_m + sum over the e with need(e) <= m of 2^(1-k) c*_(m-2k+2), k = kappa+(e)                  (Theorem 1)
Psi_e(m) (Theorem 1', m even): the same with Lemma E for the prime powers: max(E1, E2) in place of 2^(1-k) c*_(m-2k+2),
  E1 = (3/4) 2^(1-k) c_(m-2k) if m >= 2k + 2 (else 0),  E2 = 2^(3-k-q) c*_(m-2k-2q+6).
Variants printed for comparison: 'noC' (kappa in place of kappa+, i.e. without Lemma C), 'noneed' (the e with
kappa(e) <= m - 1 in place of need(e) <= m), 'noq1' (need(e) = q + 2s for every e).
Prints the counts (formula against a listing of the e), the sums W' and W+, sqrt(m) Psi(m), exact comparisons of Psi(m)
with 1/sqrt(m) and with Theorem Q, and the largest values.
usage: const.py KMAX MMAX"""
import sys, math
from fractions import Fraction
from lib import factor
def primes_upto(n): return [p for p in range(3, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
def F(q, s, odd_primes):
    """number of e with largest prime q and s(e) <= s."""
    r = 1 + s // (q - 1)
    for p in odd_primes:
        if p < q: r *= 2 + s // (p - 1)
    return r
def pairs(kmax):
    """list of (q, s, number of prime powers, number of e with two or more primes) with kappa = s + q - 1 <= kmax."""
    ps = primes_upto(kmax + 1); out = []
    for q in ps:
        for s in range(0, kmax - (q - 1) + 1, 2):
            g = F(q, s, ps) - (F(q, s - 2, ps) if s >= 2 else 0)
            pp = 1 if s % (q - 1) == 0 else 0
            out.append((q, s, pp, g - pp))
    return out
def invariants(e):
    f = factor(e); q = max(f); s = max((j - 1) * (p - 1) for p, j in f.items())
    return q, s, len(f) == 1
def mu_of(e):
    f = factor(e)
    return max(j * (p - 1) for p, j in f.items())
def cs(r): return Fraction(1, 2) if r <= 0 else Fraction(math.comb(r, r // 2), 2 ** r)
def even_pp(m, q, k):
    """Lemma E: m even, e = q^j, k = kappa(e) = j (q - 1): max(E1, E2)."""
    E1 = Fraction(3, 4) * Fraction(1, 2 ** (k - 1)) * cs(m - 2 * k) if m >= 2 * k + 2 else Fraction(0)
    E2 = Fraction(1, 2 ** (k + q - 3)) * cs(m - 2 * (k + q - 2) + 2)
    return max(E1, E2)
def Psi_exact(m, PR, lemmaC=True, need=True, q1=True, parity=False):
    t = cs(m) if m % 2 == 0 else Fraction(0)
    for (q, s, pp, nc) in PR:
        k = s + q - 1
        if (q + 2 * s > m) if need else (k > m - 1): continue
        t += pp * even_pp(m, q, k) if (parity and m % 2 == 0) else Fraction(pp, 2 ** (k - 1)) * cs(m - 2 * k + 2)
        if need and q1 and s == 0 and m < q + 1: continue      # two or more primes, all ranks 1: at least q + 1 elements
        t += (Fraction(nc, 2 ** k) * cs(m - 2 * k)) if lemmaC else (Fraction(nc, 2 ** (k - 1)) * cs(m - 2 * k + 2))
    return t
def clog(r):                                   # ln c*_r
    if r <= 0: return -math.log(2)
    return math.lgamma(r + 1) - math.lgamma(r // 2 + 1) - math.lgamma(r - r // 2 + 1) - r * math.log(2)
def Qbound(m):                                 # Theorem Q of the brief (m >= 3), and the trivial 1/2 below
    return Fraction(1, 2) if m <= 2 else Fraction(1, 4) if (m % 2 and m >= 9) else Fraction(47, 128) if (m % 2 == 0 and m >= 10) else Fraction(3, 8)
if __name__ == '__main__':
    kmax = int(sys.argv[1]); mmax = int(sys.argv[2])
    PR = pairs(kmax)
    # check of the counts against a listing of the e with kappa <= 16
    lim = 16; listed = {}; es = [1]
    for p in (3, 5, 7, 11, 13, 17):
        es = [e * p ** j for e in es for j in range(0, lim // (p - 1) + 2)]
    for e in es:
        if e > 1:
            q, s, ispp = invariants(e); assert s + q - 1 >= mu_of(e)
            if s + q - 1 <= lim:
                a = listed.setdefault((q, s), [0, 0]); a[0 if ispp else 1] += 1
    formula = {(q, s): [pp, nc] for (q, s, pp, nc) in PR if s + q - 1 <= lim}
    assert all(formula.get(k, [0, 0]) == v for k, v in listed.items()) and all(listed.get(k, [0, 0]) == v for k, v in formula.items())
    print(f"counts by (q, s), kappa <= {lim}: formula and listing agree on {len(formula)} pairs, {sum(v[0] + v[1] for v in formula.values())} numbers e")
    NP = {}; NC = {}
    for (q, s, pp, nc) in PR:
        k = s + q - 1; NP[k] = NP.get(k, 0) + pp; NC[k] = NC.get(k, 0) + nc
    print("NP(k), NC(k) for k = 2..12:", {k: (NP[k], NC[k]) for k in range(2, 13, 2)})
    W0 = sum(Fraction(NP[k] + NC[k], 2 ** k) for k in NP)
    Wp = sum(Fraction(NP[k], 2 ** k) + Fraction(NC[k], 2 ** (k + 1)) for k in NP)
    print(f"up to kappa = {kmax}:  2 W' = sum of 2^(1-kappa(e)) = {float(2 * W0):.9f};   2 W+ = sum of 2^(1-kappa+(e)) = {float(2 * Wp):.9f}")
    part = Fraction(0)
    for k in range(2, 22, 2):
        part += Fraction(NP[k], 2 ** k) + Fraction(NC[k], 2 ** (k + 1))
        print(f"  k = {k:2d}  NP = {NP[k]:3d}  NC = {NC[k]:8d}  NP 2^(1-k) + NC 2^(-k) = {float(Fraction(NP[k], 2 ** (k - 1)) + Fraction(NC[k], 2 ** k)):.6f}  partial 2W+ = {float(2 * part):.6f}")
    # beyond kmax: the number of e with kappa(e) = k is at most A(k) <= (k/2 + 1) x^(k/2) 2^k, x < 0.5783 (Lemma W of the earlier text; kappa >= mu)
    x = 0.5783; u0 = kmax // 2 + 1
    tail = x ** u0 * ((u0 + 1) - u0 * x) / (1 - x) ** 2
    print(f"sum over kappa(e) > {kmax} of 2^(-kappa(e)): at most {tail:.3e}")
    LP = [(q, s, math.log(pp) - (s + q - 2) * math.log(2) if pp else None, math.log(nc) - (s + q - 1) * math.log(2) if nc else None) for (q, s, pp, nc) in PR]
    rows = []
    for m in range(1, mmax + 1):
        tot = math.exp(clog(m)) if m % 2 == 0 else 0.0
        for (q, s, lp, lc) in LP:
            if q + 2 * s > m: continue
            k = s + q - 1
            if lp is not None: tot += math.exp(lp + clog(m - 2 * k + 2))
            if lc is not None and not (s == 0 and m < q + 1): tot += math.exp(lc + clog(m - 2 * k))
        if m - 1 > kmax: tot += 2 * tail          # the e with kappa > kmax: each term at most 2^(1-kappa)
        rows.append((m, tot, tot * math.sqrt(m)))
    for m, tot, v in rows:
        if m <= 60 or m in (80, 100, 150, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 50000, mmax):
            print(f"m = {m:6d}  Psi = {tot:.6f}  sqrt(m) Psi = {v:.5f}   with Theorem Q: {min(tot, float(Qbound(m))) * math.sqrt(m):.5f}")
    print(f"limits: sqrt(2/pi) (1 + 2W+) = {math.sqrt(2 / math.pi) * (1 + 2 * float(Wp)):.5f} (even),  sqrt(2/pi) 2W+ = {math.sqrt(2 / math.pi) * 2 * float(Wp):.5f} (odd);"
          f"  without Lemma C: {math.sqrt(2 / math.pi) * (1 + 2 * float(W0)):.5f}, {math.sqrt(2 / math.pi) * 2 * float(W0):.5f}")
    top = min(kmax + 1, 161)
    for name, kw in (("Psi (Theorem 1)", {}), ("variant noq1 (need = q + 2s for every e)", dict(q1=False)), ("variant noneed", dict(need=False)), ("variant noC", dict(lemmaC=False)), ("variant noC, noneed", dict(lemmaC=False, need=False))):
        ex = {m: Psi_exact(m, PR, **kw) for m in range(1, top + 1)}
        print(f"exact (fractions), m <= {top}, {name}:")
        print("  odd m with Psi(m) >= 1/sqrt(m):", [m for m in ex if m % 2 and ex[m] ** 2 * m >= 1])
        print("  even m with Psi(m) < 1/sqrt(m):", [m for m in ex if m % 2 == 0 and ex[m] ** 2 * m < 1])
        for par, pn in ((0, 'even'), (1, 'odd')):
            b = max((ex[m] ** 2 * m, m) for m in ex if m % 2 == par); bq = max((min(ex[m], Qbound(m)) ** 2 * m, m) for m in ex if m % 2 == par)
            print(f"  m {pn}: largest sqrt(m) Psi(m) = {math.sqrt(b[0]):.5f} at m = {b[1]};  with Theorem Q: {math.sqrt(bq[0]):.5f} at m = {bq[1]}")
        if not kw:
            print("  Psi(m) for m = 1..20:", ", ".join(f"{m}: {ex[m]}" for m in range(1, 21)))
            print("  sqrt(m) Psi(m) for odd m <= 25:", ", ".join(f"{m}: {math.sqrt(ex[m] ** 2 * m):.5f}" for m in range(1, 26, 2)))
            print("  even m where Theorem Q is smaller than Psi:", [m for m in ex if m % 2 == 0 and Qbound(m) < ex[m]], " odd m:", [m for m in ex if m % 2 and Qbound(m) < ex[m]])
            exact_rows = {m: float(ex[m]) for m in ex}
            assert all(abs(exact_rows[m] - tot) < 1e-12 for m, tot, v in rows if m <= top)
    # Theorem 1' (even m): Lemma E for the prime powers
    exe = {m: Psi_exact(m, PR, parity=True) for m in range(2, top + 1, 2)}
    assert all(exe[m] <= Psi_exact(m, PR) for m in exe)
    b = max((exe[m] ** 2 * m, m) for m in exe); bq = max((min(exe[m], Qbound(m)) ** 2 * m, m) for m in exe)
    print(f"Theorem 1' (even m <= {top}, exact): largest sqrt(m) Psi_e(m) = {math.sqrt(b[0]):.5f} at m = {b[1]};  with Theorem Q: {math.sqrt(bq[0]):.5f} at m = {bq[1]}")
    print("  Psi_e(m) for even m <= 30:", ", ".join(f"{m}: {exe[m]}" for m in range(2, 31, 2)))
    print("  sqrt(m) Psi_e(m) for even m <= 60:", ", ".join(f"{m}: {math.sqrt(exe[m] ** 2 * m):.4f}" for m in range(2, 61, 2)))
    print("  even m where Theorem Q is smaller than Psi_e:", [m for m in exe if Qbound(m) < exe[m]], "; even m with Psi_e(m) < 1/sqrt(m):", [m for m in exe if exe[m] ** 2 * m < 1])
    We = sum(Fraction(3, 4) * Fraction(pp, 2 ** (s + q - 2)) + Fraction(nc, 2 ** (s + q - 1)) for (q, s, pp, nc) in PR)
    print(f"  2W_e = sum over prime powers of (3/4) 2^(1-kappa) + sum over the other e of 2^(-kappa) = {float(We):.9f};  limit sqrt(2/pi) (1 + 2W_e) = {math.sqrt(2 / math.pi) * (1 + float(We)):.5f}")
    def fl(m):
        tot = math.exp(clog(m))
        for (q, s, pp, nc) in PR:
            k = s + q - 1
            if q + 2 * s > m: continue
            if pp:
                E1 = 0.75 * math.exp(-(k - 1) * math.log(2) + clog(m - 2 * k)) if m >= 2 * k + 2 else 0.0
                E2 = math.exp(-(k + q - 3) * math.log(2) + clog(m - 2 * (k + q - 2) + 2))
                tot += max(E1, E2)
            if nc and not (s == 0 and m < q + 1): tot += math.exp(math.log(nc) - k * math.log(2) + clog(m - 2 * k))
        return tot + (2 * tail if m - 1 > kmax else 0.0)
    assert all(abs(fl(m) - float(exe[m])) < 1e-12 for m in exe)
    if mmax > top:
        be = max((fl(m) * math.sqrt(m), m) for m in range(top + 1, mmax + 1) if m % 2 == 0)
        print(f"  floating point, {top} < m <= {mmax}, m even: largest sqrt(m) Psi_e(m) = {be[0]:.5f} at m = {be[1]};  at m = {mmax if mmax % 2 == 0 else mmax - 1}: {fl(mmax if mmax % 2 == 0 else mmax - 1) * math.sqrt(mmax if mmax % 2 == 0 else mmax - 1):.5f}")
    if mmax > top:
        print(f"floating point, {top} < m <= {mmax}: largest sqrt(m) Psi(m): even {max((v, m) for m, tot, v in rows if m % 2 == 0 and m > top)}, odd {max((v, m) for m, tot, v in rows if m % 2 and m > top)}")
