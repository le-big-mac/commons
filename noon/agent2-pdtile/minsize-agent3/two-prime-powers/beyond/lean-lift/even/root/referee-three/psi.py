"""Referee's own computation of Psi(m), Psi_e(m) and the sums W from the DEFINITIONS in result.md (sections 2, 3, 3a).
Not derived from the author's const.py.
Part 1: every odd e > 1 with need(e) <= MD is LISTED (as a factorisation) and Psi is summed over the list (m <= MD).
Part 2: the e are counted by (q, s) with a count obtained by a different route (a product over primes of the number of
        exponents with (j-1)(p-1) <= s, differenced), checked against the list of part 1; exact Psi for m <= 161.
Part 3: floating point for 162 <= m <= 3000 with a rigorous tail constant.
usage: psi.py MD"""
import sys, math
from fractions import Fraction as Fr

def is_prime(n): return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))
ODD_PRIMES = [p for p in range(3, 400) if is_prime(p)]

def cstar(r):
    if r <= 0: return Fr(1, 2)
    return Fr(math.comb(r, r // 2), 2 ** r)

def inv(fac):
    """fac: dict prime -> exponent >= 1.  returns q, s, kappa, kappa+, need"""
    q = max(fac); s = max((j - 1) * (p - 1) for p, j in fac.items())
    kap = s + q - 1
    kp = kap if len(fac) == 1 else kap + 1
    need = q + 2 * s
    if len(fac) >= 2 and s == 0: need = q + 1
    return q, s, kap, kp, need

def list_e(MD):
    """all e (as dicts) with need(e) <= MD."""
    out = []
    def rec(idx, fac, primes, smax):
        if idx == len(primes):
            if fac: out.append(dict(fac))
            return
        p = primes[idx]
        j = 0
        while j == 0 or (j - 1) * (p - 1) <= smax:
            if j: fac[p] = j
            rec(idx + 1, fac, primes, smax)
            if j: del fac[p]
            j += 1
    for q in ODD_PRIMES:
        if q > MD: break
        smax = (MD - q) // 2
        below = [p for p in ODD_PRIMES if p < q]
        j = 1
        while (j - 1) * (q - 1) <= smax:
            sub = []
            def rec2(idx, fac):
                if idx == len(below):
                    sub.append(dict(fac)); return
                p = below[idx]; jj = 0
                while jj == 0 or (jj - 1) * (p - 1) <= smax:
                    if jj: fac[p] = jj
                    rec2(idx + 1, fac)
                    if jj: del fac[p]
                    jj += 1
            rec2(0, {q: j})
            out.extend(sub)
            j += 1
    return [f for f in out if inv(f)[4] <= MD]

def psi_from_list(m, L):
    t = cstar(m) if m % 2 == 0 else Fr(0)
    for f in L:
        q, s, kap, kp, need = inv(f)
        if need <= m: t += Fr(1, 2 ** (kp - 1)) * cstar(m - 2 * kp + 2)
    return t

def psie_from_list(m, L):
    assert m % 2 == 0
    t = cstar(m)
    for f in L:
        q, s, kap, kp, need = inv(f)
        if need > m: continue
        if len(f) == 1:
            E1 = Fr(3, 4) * Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap) if m >= 2 * kap + 2 else Fr(0)
            E2 = Fr(1, 2 ** (kap + q - 3)) * cstar(m - 2 * kap - 2 * q + 6)
            t += max(E1, E2)
        else:
            t += Fr(1, 2 ** kap) * cstar(m - 2 * kap)
    return t

# ---- counts by (q, s)
def n_le(q, s):
    """number of e with largest prime q and s(e) <= s  (s >= 0)."""
    if s < 0: return 0
    r = 0
    # exponent of q: j >= 1 with (j-1)(q-1) <= s
    cq = sum(1 for j in range(1, s // (q - 1) + 3) if (j - 1) * (q - 1) <= s)
    r = cq
    for p in ODD_PRIMES:
        if p >= q: break
        r *= 1 + sum(1 for j in range(1, s // (p - 1) + 3) if (j - 1) * (p - 1) <= s)
    return r
def counts(q, s):
    """(number of prime powers, number of others) with largest prime q and s(e) = s exactly."""
    tot = n_le(q, s) - n_le(q, s - 1)
    pp = 1 if s % (q - 1) == 0 else 0
    return pp, tot - pp

def pairs_upto(kmax):
    P = []
    for q in ODD_PRIMES:
        if q - 1 > kmax: break
        for s in range(0, kmax - (q - 1) + 1):
            pp, nc = counts(q, s)
            if pp or nc: P.append((q, s, pp, nc))
    return P

def psi_pairs(m, P):
    t = cstar(m) if m % 2 == 0 else Fr(0)
    for (q, s, pp, nc) in P:
        kap = s + q - 1
        if pp and q + 2 * s <= m:
            t += pp * Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap + 2)
        if nc:
            need = q + 2 * s if s > 0 else q + 1
            if need <= m: t += nc * Fr(1, 2 ** kap) * cstar(m - 2 * kap)
    return t
def psie_pairs(m, P):
    t = cstar(m)
    for (q, s, pp, nc) in P:
        kap = s + q - 1
        if pp and q + 2 * s <= m:
            E1 = Fr(3, 4) * Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap) if m >= 2 * kap + 2 else Fr(0)
            E2 = Fr(1, 2 ** (kap + q - 3)) * cstar(m - 2 * kap - 2 * q + 6)
            t += max(E1, E2)
        if nc:
            need = q + 2 * s if s > 0 else q + 1
            if need <= m: t += nc * Fr(1, 2 ** kap) * cstar(m - 2 * kap)
    return t

def lncstar(r):
    if r <= 0: return -math.log(2)
    return math.lgamma(r + 1) - math.lgamma(r // 2 + 1) - math.lgamma(r - r // 2 + 1) - r * math.log(2)

if __name__ == '__main__':
    MD = int(sys.argv[1])
    L = list_e(MD)
    print(f"listed e with need(e) <= {MD}: {len(L)}")
    def val(f): return math.prod(p ** j for p, j in f.items())
    for m in (13, 15):
        print(f"--- Psi({m}) term by term (e, q, s, kappa+, need, weight 2^(1-k), index m-2k+2, term)")
        tot = Fr(0); n = 0
        for f in sorted(L, key=lambda f: (max(f), val(f))):
            q, s, kap, kp, need = inv(f)
            if need <= m:
                term = Fr(1, 2 ** (kp - 1)) * cstar(m - 2 * kp + 2); tot += term; n += 1
                print(f"   e = {val(f):8d} q = {q:2d} s = {s:2d} k+ = {kp:2d} need = {need:2d} weight = 1/{2 ** (kp - 1)} index = {m - 2 * kp + 2:3d} term = {term}")
        print(f"   {n} terms, Psi({m}) = {tot} = {float(tot):.8f}, sqrt(m) Psi = {math.sqrt(m) * float(tot):.8f}, m Psi^2 < 1: {m * tot * tot < 1}")
    print("Psi(m), m = 1..20 (from the list):", ", ".join(str(psi_from_list(m, L)) for m in range(1, 21)))
    print("Psi_e(m), m = 2..12 (from the list):", ", ".join(str(psie_from_list(m, L)) for m in range(2, 13, 2)))
    # counts against list
    bylist = {}
    for f in L:
        q, s, kap, kp, need = inv(f)
        a = bylist.setdefault((q, s), [0, 0]); a[0 if len(f) == 1 else 1] += 1
    bad = 0; chk = 0
    for (q, s), v in bylist.items():
        # the list is complete for (q, s) when q + 2 s <= MD (need <= q + 2s always)
        if q + 2 * s <= MD:
            chk += 1
            if tuple(v) != counts(q, s): bad += 1; print("COUNT MISMATCH", q, s, v, counts(q, s))
    print(f"counts by (q, s): {chk} pairs compared with the list, mismatches: {bad}")
    P = pairs_upto(160)
    mm = [m for m in range(1, MD + 1) if psi_pairs(m, P) != psi_from_list(m, L)]
    print(f"Psi by counts against Psi by list, m <= {MD}: differences at", mm)
    mm = [m for m in range(2, MD + 1, 2) if psie_pairs(m, P) != psie_from_list(m, L)]
    print(f"Psi_e by counts against Psi_e by list, even m <= {MD}: differences at", mm)
    # by kappa
    NP = {}; NC = {}
    for (q, s, pp, nc) in P:
        k = s + q - 1; NP[k] = NP.get(k, 0) + pp; NC[k] = NC.get(k, 0) + nc
    print("numbers (prime powers, others) with kappa = 2..12:", [(NP.get(k, 0), NC.get(k, 0)) for k in range(2, 13, 2)])
    W1 = sum(Fr(pp + nc, 2 ** (s + q - 2)) for (q, s, pp, nc) in P)
    Wp = sum(Fr(pp, 2 ** (s + q - 2)) + Fr(nc, 2 ** (s + q - 1)) for (q, s, pp, nc) in P)
    We = sum(Fr(3, 4) * Fr(pp, 2 ** (s + q - 2)) + Fr(nc, 2 ** (s + q - 1)) for (q, s, pp, nc) in P)
    print(f"kappa <= 160: 2W' = {float(W1):.10f}  2W+ = {float(Wp):.10f}  2W_e = {float(We):.10f}")
    x = 0.5783; u0 = 81
    tail = x ** u0 * ((u0 + 1) - u0 * x) / (1 - x) ** 2          # >= sum over kappa(e) > 160 of 2^(-kappa(e)), by (Q6)
    print(f"tail bound for sum of 2^(-kappa(e)), kappa > 160: {tail:.3e}")
    r2pi = math.sqrt(2 / math.pi)
    print(f"limits: even Psi {r2pi * (1 + float(Wp)):.5f}, even Psi_e {r2pi * (1 + float(We)):.5f}, odd {r2pi * float(Wp):.5f}; 1 + 2W' = {1 + float(W1):.6f}")
    # exact, m <= 161
    ex = {m: psi_pairs(m, P) for m in range(1, 162)}
    exe = {m: psie_pairs(m, P) for m in range(2, 162, 2)}
    print("odd m <= 161 with m Psi^2 >= 1:", [m for m in ex if m % 2 and m * ex[m] ** 2 >= 1])
    b = max((m * ex[m] ** 2, m) for m in ex if m % 2); print(f"largest sqrt(m) Psi(m), odd m <= 161: {math.sqrt(b[0]):.8f} at m = {b[1]}")
    b = max((m * ex[m] ** 2, m) for m in ex if m % 2 and m >= 17); print(f"largest sqrt(m) Psi(m), odd 17 <= m <= 161: {math.sqrt(b[0]):.8f} at m = {b[1]}")
    b = max((m * ex[m] ** 2, m) for m in ex if m % 2 == 0); print(f"largest sqrt(m) Psi(m), even m <= 161: {math.sqrt(b[0]):.8f} at m = {b[1]}")
    b = max((m * exe[m] ** 2, m) for m in exe); print(f"largest sqrt(m) Psi_e(m), even m <= 161: {math.sqrt(b[0]):.8f} at m = {b[1]}")
    print("Psi_e <= Psi for all even m <= 161:", all(exe[m] <= ex[m] for m in exe))
    def Q(m): return Fr(1, 2) if m <= 2 else Fr(1, 4) if (m % 2 and m >= 9) else Fr(47, 128) if (m % 2 == 0 and m >= 10) else Fr(3, 8)
    b = max((m * min(exe[m], Q(m)) ** 2, m) for m in exe); print(f"largest sqrt(m) min(Psi_e, Q), even m <= 161: {math.sqrt(b[0]):.8f} at m = {b[1]};  even m where Q < Psi_e: {[m for m in exe if Q(m) < exe[m]]}")
    b = max((m * min(ex[m], Q(m)) ** 2, m) for m in ex if m % 2 == 0); print(f"largest sqrt(m) min(Psi, Q), even m <= 161: {math.sqrt(b[0]):.8f} at m = {b[1]};  even m where Q < Psi: {[m for m in ex if m % 2 == 0 and Q(m) < ex[m]]}")
    print("sqrt(m) Psi, odd m <= 25:", ", ".join(f"{math.sqrt(m) * float(ex[m]):.4f}" for m in range(1, 26, 2)))
    print("sqrt(m) Psi_e, even 10..24:", ", ".join(f"{math.sqrt(m) * float(exe[m]):.4f}" for m in range(10, 25, 2)))
    print("even m <= 161 with Psi < 1/sqrt(m):", [m for m in ex if m % 2 == 0 and m * ex[m] ** 2 < 1])
    # variants (to see what each part buys), exact m <= 161
    def variant(m, noC=False, noneed=False, noq1=False):
        t = cstar(m) if m % 2 == 0 else Fr(0)
        for (q, s, pp, nc) in P:
            kap = s + q - 1
            okpp = (kap <= m - 1) if noneed else (q + 2 * s <= m)
            need = q + 2 * s if (s > 0 or noq1) else q + 1
            okc = (kap <= m - 1) if noneed else (need <= m)
            if pp and okpp: t += Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap + 2)
            if nc and okc: t += nc * (Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap + 2) if noC else Fr(1, 2 ** kap) * cstar(m - 2 * kap))
        return t
    for nm, kw in (("noC", dict(noC=True)), ("noneed", dict(noneed=True)), ("noq1", dict(noq1=True))):
        v = {m: variant(m, **kw) for m in range(1, 162)}
        b = max((m * v[m] ** 2, m) for m in v if m % 2 == 0)
        print(f"variant {nm}: odd m with Psi >= 1/sqrt(m): {[m for m in v if m % 2 and m * v[m] ** 2 >= 1]}; even max {math.sqrt(b[0]):.5f} at {b[1]}")
    # floating point 162..3000
    LP = [(q, s, pp, nc) for (q, s, pp, nc) in P]
    best = {0: (0, 0), 1: (0, 0)}; beste = (0, 0)
    for m in range(162, 3001):
        t = math.exp(lncstar(m)) if m % 2 == 0 else 0.0
        te = t
        for (q, s, pp, nc) in LP:
            if q + 2 * s > m: continue
            kap = s + q - 1
            if pp:
                a = math.exp(-(kap - 1) * math.log(2) + lncstar(m - 2 * kap + 2)); t += a
                if m % 2 == 0:
                    E1 = 0.75 * math.exp(-(kap - 1) * math.log(2) + lncstar(m - 2 * kap)) if m >= 2 * kap + 2 else 0.0
                    E2 = math.exp(-(kap + q - 3) * math.log(2) + lncstar(m - 2 * kap - 2 * q + 6))
                    te += max(E1, E2)
            if nc:
                a = nc * math.exp(-kap * math.log(2) + lncstar(m - 2 * kap)); t += a; te += a
        t += tail; te += tail
        v = t * math.sqrt(m)
        if v > best[m % 2][0]: best[m % 2] = (v, m)
        if m % 2 == 0 and te * math.sqrt(m) > beste[0]: beste = (te * math.sqrt(m), m)
    print(f"floating point 162..3000: largest sqrt(m) Psi: even {best[0]}, odd {best[1]}; largest sqrt(m) Psi_e: {beste}")
