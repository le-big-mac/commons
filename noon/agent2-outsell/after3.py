"""The referee's controls, redone here with my own code (not registered).   usage: python -u after3.py SECTIONS after3-SECTIONS.json
A the early lead and the lock-in for other weights a; B does copying help, on a wider net, and under a strict reading of "ahead";
C the Gamma form against the exact values, and the sales needed where double precision gave out; D the least number of sales over even
numbers as well as odd; E the other form of copying without the two imaginary buyers; F how much is settled by the first waits."""
import sys, json, math
import numpy as np
from scipy.special import betainc, betaln, gammainc, gammaln, zeta
from scipy.integrate import quad
import urn
from after import run, power_rule
SEC = sys.argv[1]; A = {}
def Pgen(q, a, mA, mB):
    """the chance that A's first mA sales take less time than B's first mB (g = 1): B' < B^(1/q) with B ~ Beta(a, mA), B' ~ Beta(a, mB)"""
    lognorm = -betaln(a, mA)
    def f(v):
        b = v / mA
        if b >= 1: return 0.0
        return betainc(a, mB, b ** (1 / q)) * math.exp(lognorm + (a - 1) * math.log(b) + (mA - 1) * math.log1p(-b)) / mA
    top = min(mA, a + 60 * math.sqrt(a) + 200.0); pts = sorted(set([x for x in (a * 1e-4, a * 1e-3, a * 0.01, a * 0.1, a * 0.3, a, 2 * a, 4 * a, a + 10, a + 30, a + 100) if 0 < x < top]))
    return quad(f, 0, top, points=pts, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
def Pany(q, a, N):
    """P after any number N of sales, odd or even, from the formula (half a tie counted for even N)"""
    if N % 2: m = (N + 1) // 2; return Pgen(q, a, m, m)
    m = N // 2; return 0.5 * (Pgen(q, a, m + 1, m) + Pgen(q, a, m, m + 1))
if 'A' in SEC:
    print("A. Other weights a (q = 1.1). Copying in proportion: the leader after 100 sales and after 10,000"); A['lead'] = {}
    for a in (0.1, 1.0, 10.0, 100.0):
        rule = power_rule(1.1, 1.0, a); p100 = run(rule, 100); k = np.arange(101); res = {}
        for name, mask in (("A", k > 50), ("B", k < 50)):
            w = float(p100[mask].sum()); p = run(rule, 10000, start=(100, np.where(mask, p100, 0.0))); res[name] = (w, urn.ahead(p) / w)
        same = (res["A"][0] * res["A"][1] + res["B"][0] * (1 - res["B"][1])) / (res["A"][0] + res["B"][0]); A['lead'][str(a)] = dict(same=same, back=res["B"][1])
        print(f"   a = {a:g}: the leader after 100 is the leader after 10,000 with chance {same:.4f}; where the worse product led after 100, the better is ahead after 10,000 with chance {res['B'][1]:.4f}", flush=True)
    print("   More than in proportion (g = 1.5): P after 1,000, 10,000 and 100,000 sales, and the same for the leader after 100"); A['lock'] = {}
    for a in (0.1, 1.0, 10.0, 100.0):
        p, kept = urn.dist(1.1, 1.5, 100000, a=a, keep=(1000, 10000)); vals = [urn.ahead(kept[1000]), urn.ahead(kept[10000]), urn.ahead(p)]
        rule = power_rule(1.1, 1.5, a); p100 = run(rule, 100); k = np.arange(101); wA = float(p100[k > 50].sum()); wB = float(p100[k < 50].sum())
        pa = urn.ahead(run(rule, 10000, start=(100, np.where(k > 50, p100, 0.0)))) / wA; pb = urn.ahead(run(rule, 10000, start=(100, np.where(k < 50, p100, 0.0)))) / wB; same = (wA * pa + wB * (1 - pb)) / (wA + wB)
        lose = np.minimum(np.arange(10001), 10000 - np.arange(10001)); c = np.zeros(5001); np.add.at(c, lose, kept[10000]); cum = np.cumsum(c); med = int(np.searchsorted(cum, 0.5))
        A['lock'][str(a)] = dict(P=vals, same=same, median=med, over100=float(1 - cum[100]), over1000=float(1 - cum[1000]))
        print(f"   a = {a:g}: P = {vals[0]:.4f}, {vals[1]:.4f}, {vals[2]:.4f}; the leader after 100 is the leader after 10,000 with chance {same:.4f}; after 10,000 sales the product behind has sold a median of {med}, more than 100 with chance {1 - cum[100]:.3f}, more than 1,000 with chance {1 - cum[1000]:.3f}", flush=True)
if 'B' in SEC:
    print("B. Does copying raise P? Every number of sales up to 2,000; P with half a tie, as sealed"); A['help'] = []
    keep = tuple(range(1, 2001))
    for q in (1.02, 1.1, 2.0):
        for a in (1.0, 10.0, 100.0):
            base = urn.dist(q, 0.0, 2000, a=a, keep=keep)[1]; b = np.array([urn.ahead(base[N]) for N in keep])
            for g in (0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0):
                k = urn.dist(q, g, 2000, a=a, keep=keep)[1]; d = np.array([urn.ahead(k[N]) for N in keep]) - b; up = [N for N in keep if d[N - 1] > 1e-13]; up100 = [N for N in up if N >= 100]
                rec = dict(q=q, a=a, g=g, last=max(up, default=0), n100=len(up100), odd100=sum(N % 2 for N in up100), gain100=float(max((d[N - 1] for N in up100), default=0.0)), most=float(d.max()), at=int(np.argmax(d)) + 1); A['help'].append(rec)
            rows = [r for r in A['help'] if r['q'] == q and r['a'] == a]
            print(f"   q = {q}, a = {a:g}: " + "; ".join(f"g = {r['g']}: up to {r['last']} sales" + (f" ({r['n100']} sizes from 100 up, {r['odd100']} of them odd, most +{r['gain100']:.7f})" if r['n100'] else "") for r in rows), flush=True)
    print(f"   the largest rise at 100 sales or more, over all of these: {max(r['gain100'] for r in A['help']):.7f}; the latest number of sales at which any of them raises P: {max(r['last'] for r in A['help'])}; at 1,000 sales or more: {sum(1 for r in A['help'] if r['last'] >= 1000)} cases")
    print("   the largest rise at any number of sales (a = 1): " + "; ".join(f"q = {q}, g = {g}: +{max(urn.ahead(urn.dist(q, g, N)) - urn.ahead(urn.dist(q, 0.0, N)) for N in range(1, 31)):.4f}" for q, g in ((2.0, 0.5), (2.0, 1.0), (2.0, 1.5), (5.0, 1.0))))
    print("   A strict reading (\"A has sold more\", a tie counting nothing), 100 sales, a = 1:"); A['strict'] = {}
    for q in (1.02, 1.1):
        for g in (0.0, 0.25, 1.0):
            p = urn.dist(q, g, 100); A['strict'][f"{q}|{g}"] = (float(p[51:].sum()), float(p[50]), float(p[:50].sum())); print(f"      q = {q}, g = {g}: A has sold more with chance {p[51:].sum():.4f}, a tie {p[50]:.4f}, B more {p[:50].sum():.4f}")
if 'C' in SEC:
    print("C. The Gamma form (G' < G^(1/q) c, with G and G' independent Gamma(a) variables) against the exact value after 999 sales, q = 1.1"); A['gamma'] = {}
    def Pg(q, a, c):
        if a < 1:                                        # x = t^(1/a) removes the spike of the Gamma density at 0
            f = lambda t: math.exp(-t ** (1 / a) - gammaln(a) - math.log(a)) * gammainc(a, c * t ** (1 / (a * q)))
            return quad(f, 0, 60.0 ** a, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
        f = lambda x: math.exp((a - 1) * math.log(x) - x - gammaln(a)) * gammainc(a, c * x ** (1 / q)) if x > 0 else 0.0
        top = a + 12 * math.sqrt(a) + 60; return quad(f, 0, top, points=[a * 0.3, a, 2 * a] if a > 3 else None, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
    for a in (0.1, 1.0, 10.0, 100.0):
        ex = Pgen(1.1, a, 500, 500); g1 = Pg(1.1, a, 500 ** (1 - 1 / 1.1)); g2 = Pg(1.1, a, (a + 500) ** (1 - 1 / 1.1)); A['gamma'][str(a)] = (ex, g1, g2)
        print(f"   a = {a:g}: exact {ex:.4f}; Gamma form with c = (N/2)^(1 - 1/q): {g1:.4f}; with c = (a + N/2)^(1 - 1/q): {g2:.4f}")
    print("   Sales needed for nine times in ten where double precision gave out (q = 1.1; the Gamma form with c = (a + N/2)^(1 - 1/q))"); A['needed'] = {}
    for a in (0.1, 0.3, 1.0, 3.0):
        lo, hi = 2.0, 150.0
        for it in range(60):
            mid = 0.5 * (lo + hi)
            if Pg(1.1, a, (a + 0.5 * 10 ** mid) ** (1 - 1 / 1.1)) >= 0.9: hi = mid
            else: lo = mid
        A['needed'][str(a)] = hi; print(f"   a = {a:g}: about 10^{hi:.1f} sales" + (f" (the exact formula gave {dict([(1.0, '9.82e9'), (3.0, '594,539')])[a]})" if a in (1.0, 3.0) else ""), flush=True)
    print(f"   exact P at m = 10^15 (N = 2 x 10^15 - 1): a = 0.1: {Pgen(1.1, 0.1, 1e15, 1e15):.4f}; a = 0.3: {Pgen(1.1, 0.3, 1e15, 1e15):.4f}")
if 'D' in SEC:
    print("D. The least number of sales, even numbers allowed"); A['least'] = []
    print("   the formula for even numbers against the step-by-step computation: largest difference " + f"{max(abs(Pany(q, a, N) - urn.ahead(urn.dist(q, 1.0, N, a=a))) for q in (1.1, 2.0) for a in (0.3, 1.0, 10.0) for N in (2, 10, 100, 1000)):.1e} in 24 cases")
    def least(q, a, target, odd):                      # odd: the least odd number, as tabled; then is the even number below it enough?
        return odd - 1 if odd > 1 and Pany(q, a, odd - 1) >= target else odd
    T3 = json.load(open("after-3.json"))['sales_needed']; B2 = json.load(open("after2.json"))['needed']
    for q in ("1.05", "1.1", "1.25", "1.5", "2.0"):
        for t in ("0.75", "0.9", "0.99"):
            odd = T3[q]['imitation'][t]
            if odd < 1e7: N = least(float(q), 1.0, float(t), int(round(odd))); A['least'].append(dict(kind="copying", q=float(q), a=1.0, target=float(t), odd=int(round(odd)), least=N)); print(f"   copying in proportion, a = 1, q = {q}, {t}: least odd {int(round(odd)):,}; least of all {N:,}")
    for a in ("3.0", "10.0", "30.0", "100.0"):
        odd = int(round(B2['1.1'][a])); N = least(1.1, float(a), 0.9, odd); A['least'].append(dict(kind="copying", q=1.1, a=float(a), target=0.9, odd=odd, least=N)); print(f"   copying in proportion, q = 1.1, a = {a}, 0.9: least odd {odd:,}; least of all {N:,}")
    from scipy.stats import binom
    def Pb(q, N): pr = q / (1 + q); return float(binom.sf(N // 2, N, pr) + (0.5 * binom.pmf(N // 2, N, pr) if N % 2 == 0 else 0.0))
    for q in ("1.05", "1.1", "1.25", "1.5", "2.0"):
        for t in ("0.75", "0.9", "0.99"):
            odd = T3[q]['alone'][t]; N = odd - 1 if odd > 1 and Pb(float(q), odd - 1) >= float(t) else odd; A['least'].append(dict(kind="alone", q=float(q), a=None, target=float(t), odd=odd, least=N))
    print("   judging alone: " + "; ".join(f"q = {r['q']}, {r['target']}: {r['odd']:,} -> {r['least']:,}" for r in A['least'] if r['kind'] == "alone"))
    print("   is the first crossing the only one? P at each number of sales from the least to the least + 40: never back below the target in " + f"{sum(all(Pany(r['q'], r['a'], N) >= r['target'] for N in range(r['least'], r['least'] + 41)) for r in A['least'] if r['kind'] == 'copying')} of {sum(1 for r in A['least'] if r['kind'] == 'copying')} copying cases")
if 'E' in SEC:
    print("E. The other form of copying, with and without two imaginary buyers (q = 1.1, 1,000 sales)"); A['copy'] = {}
    for s in (0.1, 0.25, 0.5, 0.75, 0.9):
        w = urn.ahead(run(lambda k, n, s=s: (1 - s) * 1.1 / 2.1 + s * (1 + k) / (2 + n), 1000)); wo = urn.ahead(run(lambda k, n, s=s: np.where(n == 0, 1.1 / 2.1, (1 - s) * 1.1 / 2.1 + s * k / max(n, 1)), 1000)); A['copy'][str(s)] = (w, wo)
        print(f"   s = {s}: with one imaginary earlier buyer of each product (as computed before) {w:.4f}; copying real buyers only (the first buyer judges alone) {wo:.4f}")
if 'F' in SEC:
    print("F. How much the first waits settle"); A['first'] = {}
    for g in (1.25, 1.5, 2.0):
        for a in (1.0, 10.0):
            tot = float(zeta(2 * g, a)); one = a ** (-2 * g); three = sum((a + j) ** (-2 * g) for j in range(3)); A['first'][f"{g}|{a}"] = (one / tot, three / tot)
            print(f"   g = {g}, a = {a:g}: of the scatter (variance) in a product's total time, the first wait carries {100 * one / tot:.0f}% and the first three {100 * three / tot:.0f}%")
    sc = json.load(open("after-v.json"))['scatter']; print("   lead over scatter after 1,000 sales, (mean share - 1/2) / standard deviation: " + "; ".join(f"g = {g}: {(sc[g]['rows']['1000'][0] - 0.5) / sc[g]['rows']['1000'][1]:.2f}" for g in ("0.0", "0.25", "0.5", "0.75")))
    A['ratio'] = {g: (sc[g]['rows']['1000'][0] - 0.5) / sc[g]['rows']['1000'][1] for g in sc}
json.dump(A, open(sys.argv[2], "w"))
