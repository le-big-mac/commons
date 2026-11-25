"""Checks made after the sealed sheet was scored; none was registered.   usage: python -u after.py SECTIONS after.json   (for example 12 or 345)
1 the ruler: sampling against the exact computation; 2 the table over edges, strengths and sizes, and where P fails to fall as imitation grows;
3 how many sales the better product needs (g = 1, exact formula with many digits); 4 the weight a of a product that has sold nothing;
5 another form of imitation (a share s of buyers copy an earlier buyer, the rest judge alone); 6 the early lead; 7 the edge needed at each strength;
8 shares after a thousand sales; 9 more than in proportion: has P stopped changing?"""
import sys, json, math, os
import numpy as np
import urn
SEC = sys.argv[1]; OUT = sys.argv[2]; A = json.load(open(OUT)) if os.path.exists(OUT) else {}
def run(prob, N, start=None, keep=()):
    """as urn.dist, for any rule prob(k, n) -> chance that the next buyer takes A when A has sold k of n; start = (n0, p0)"""
    n0, p0 = start if start else (0, np.array([1.0])); p = np.zeros(N + 2); p[:n0 + 1] = p0; out = {}
    for n in range(n0, N):
        k = np.arange(n + 1); move = p[:n + 1] * prob(k, n); p[:n + 1] -= move; p[1:n + 2] += move
        if n + 1 in keep: out[n + 1] = p[:n + 2].copy()
    return (p[:N + 1], out) if keep else p[:N + 1]
def power_rule(q, g, a=1.0):
    return lambda k, n: q * (a + k) ** g / (q * (a + k) ** g + (a + n - k) ** g)
if '1' in SEC:
    print("1. The ruler: 400,000 sampled markets against the exact computation (q = 1.1, N = 1,000)")
    rng = np.random.default_rng(2026); M = 400000; A['ruler'] = []
    for g in (0.5, 1.0, 1.5):
        nA = np.zeros(M)
        for n in range(1000): pa = 1.1 * (1 + nA) ** g; pa = pa / (pa + (1 + n - nA) ** g); nA += rng.random(M) < pa
        est = float(np.mean(nA > 500) + 0.5 * np.mean(nA == 500)); se = math.sqrt(est * (1 - est) / M); ex = urn.ahead(urn.dist(1.1, g, 1000)); p = urn.dist(1.1, g, 1000)
        print(f"   g = {g}: sampled {est:.4f} (standard error {se:.4f}); exact {ex:.4f}; apart by {abs(est - ex) / se:.1f} standard errors; the exact probabilities sum to 1 within {abs(p.sum() - 1):.1e}", flush=True); A['ruler'].append(dict(g=g, sampled=est, se=se, exact=ex))
    for N in (999, 1000, 1001): print(f"   g = 1, q = 1.1, N = {N}: P = {urn.ahead(urn.dist(1.1, 1.0, N)):.5f}")
if '2' in SEC:
    print("2. P for each edge q, strength g and number of sales N (a = 1)")
    Q = (1.02, 1.05, 1.1, 1.25, 1.5, 2.0); G = (0, 0.1, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 2); NS = (10, 100, 1000, 10000); T = {}
    for q in Q:
        for g in G:
            p, kept = urn.dist(q, float(g), 10000, keep=(10, 100, 1000)); kept[10000] = p
            for N in NS: T[f"{q}|{g}|{N}"] = urn.ahead(kept[N])
        print(f"   q = {q} done", flush=True)
    A['table'] = T; rises = []
    for N in NS:
        print(f"   after {N:,} sales:   g = " + "  ".join(f"{g:>6}" for g in G))
        for q in Q:
            row = [T[f"{q}|{g}|{N}"] for g in G]; print(f"      q = {q:<5}        " + "  ".join(f"{x:.4f}" for x in row))
            rises += [(q, N, G[i], G[i + 1], row[i], row[i + 1]) for i in range(len(G) - 1) if row[i + 1] > row[i] + 1e-12]
    print(f"   places where P rises as g grows: {len(rises)} of {len(Q) * len(NS) * (len(G) - 1)} steps"); A['rises'] = rises
    for q, N, g0, g1, x, y in rises: print(f"      q = {q}, N = {N:,}: from {x:.5f} at g = {g0} to {y:.5f} at g = {g1}")
if '3' in SEC:
    print("3. Imitation in proportion (g = 1): the number of sales after which the better product is ahead with a given chance, from the exact formula")
    import mpmath as mp
    mp.mp.dps = 70
    def P(q, m):
        m = mp.mpf(m); f = lambda v: mp.exp(m * mp.log1p(-(v / m) ** q) + (m - 1) * mp.log1p(-v / m)) if v < m else mp.mpf(0)
        top = min(m, mp.mpf(200)); pts = [x for x in (0, mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.5'), 1, 2, 4, 8, 16, 32, 64, 128, 200) if x < top] + [top]; return mp.quad(f, pts)
    print("   check of the many-digit formula against line R4's:", ", ".join(f"q = {q}, m = {m}: {float(P(q, m)):.12f} against {urn.formula(q, m):.12f}" for q, m in ((1.1, 500), (2.0, 50))))
    print(f"   q = 1.1, N = 99,999 (m = 50,000): {float(P(1.1, 50000)):.6f}; the step-by-step computation gave 0.744173 at N = 100,000")
    A['sales_needed'] = {}
    for q in (1.05, 1.1, 1.25, 1.5, 2.0):
        row = {}
        for target in (0.75, 0.9, 0.99):
            lo, hi = 0.0, 80.0                            # log10 of m
            if float(P(q, 1)) >= target: row[str(target)] = 1.0; continue
            for it in range(50):
                mid = 0.5 * (lo + hi)
                if P(q, mp.mpf(10) ** mid) >= target: hi = mid
                else: lo = mid
            if hi < 7:                                   # small enough to settle on whole numbers: the least whole m with P >= target
                m = max(1, int(10 ** hi) - 3)
                while P(q, m) < target: m += 1
                row[str(target)] = float(2 * m - 1)
            else: row[str(target)] = 2 * 10 ** hi - 1
        # without imitation: the least N with P >= target, from the binomial
        from scipy.stats import binom
        def Pb(N): pr = q / (1 + q); return float(binom.sf(N // 2, N, pr) + (0.5 * binom.pmf(N // 2, N, pr) if N % 2 == 0 else 0.0))
        alone = {}
        for target in (0.75, 0.9, 0.99):
            N = 1
            while Pb(N) < target: N += 2
            alone[str(target)] = N
        A['sales_needed'][str(q)] = dict(imitation=row, alone=alone)
        print(f"   q = {q}: ahead three times in four after {row['0.75']:.3g} sales, nine in ten after {row['0.9']:.3g}, 99 in 100 after {row['0.99']:.3g}; with no imitation (odd N): {alone['0.75']:,}, {alone['0.9']:,}, {alone['0.99']:,}", flush=True)
    for N in (10 ** 3, 10 ** 6, 10 ** 9, 10 ** 12): print(f"   q = 1.1 after {N:.0e} sales: P = {float(P(1.1, N // 2)):.4f}")
    A['big'] = {str(N): float(P(1.1, N // 2)) for N in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8, 10 ** 9, 10 ** 10, 10 ** 11, 10 ** 12)}
if '4' in SEC:
    print("4. The weight a of a product that has sold nothing (g = 1, q = 1.1, N = 1,000)"); A['a'] = {}
    for a in (0.1, 0.3, 1, 3, 10, 30, 100, 1000): A['a'][str(a)] = urn.ahead(urn.dist(1.1, 1.0, 1000, a=float(a))); print(f"   a = {a}: P = {A['a'][str(a)]:.4f}")
    print(f"   no imitation at all: {urn.ahead(urn.dist(1.1, 0.0, 1000)):.4f}")
if '5' in SEC:
    print("5. Another form of imitation: a share s of buyers copy one earlier buyer picked at random (weight 1 for each product before any sale); the rest judge alone with odds q = 1.1"); A['copy'] = {}
    for N in (100, 1000, 10000):
        row = {}
        for s in (0, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99):
            row[str(s)] = urn.ahead(run(lambda k, n, s=s: (1 - s) * 1.1 / 2.1 + s * (1 + k) / (2 + n), N))
        A['copy'][str(N)] = row; print(f"   N = {N:,}: " + "; ".join(f"s = {s}: {v:.4f}" for s, v in row.items()), flush=True)
if '6' in SEC:
    print("6. The early lead (q = 1.1, a = 1): who is ahead after 100 sales, and after 10,000"); A['lead'] = {}
    for g in (0.0, 0.5, 1.0, 1.5):
        rule = power_rule(1.1, g); p100 = run(rule, 100); res = {}
        for name, mask in (("A", np.arange(101) > 50), ("B", np.arange(101) < 50), ("tie", np.arange(101) == 50)):
            w = float(p100[mask].sum()); p = run(rule, 10000, start=(100, np.where(mask, p100, 0.0))); res[name] = (w, urn.ahead(p) / w if w > 0 else float('nan'))
        same = res["A"][0] * res["A"][1] + res["B"][0] * (1 - res["B"][1]); A['lead'][str(g)] = dict(res=res, same=same / (res["A"][0] + res["B"][0]))
        print(f"   g = {g}: A is ahead after 100 with chance {res['A'][0]:.4f}, B {res['B'][0]:.4f}, tied {res['tie'][0]:.4f}. Given A ahead at 100, A is ahead at 10,000 with chance {res['A'][1]:.4f}; given B ahead at 100, {res['B'][1]:.4f}. The leader at 100 is the leader at 10,000 with chance {A['lead'][str(g)]['same']:.4f}", flush=True)
if '7' in SEC:
    print("7. The edge q at which the better product is ahead nine times in ten, by strength of imitation"); A['edge'] = {}
    for N in (100, 1000, 10000):
        row = {}
        for g in (0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 2):
            lo, hi = 1.0, 60.0
            for it in range(34):
                mid = math.sqrt(lo * hi)
                if urn.ahead(urn.dist(mid, float(g), N)) >= 0.9: hi = mid
                else: lo = mid
            row[str(g)] = hi
        A['edge'][str(N)] = row; print(f"   N = {N:,}: " + "; ".join(f"g = {g}: {v:.3f}" for g, v in row.items()), flush=True)
if '8' in SEC:
    print("8. The better product's share after 1,000 sales (q = 1.1): quartiles and extremes"); A['shares'] = {}
    for g in (0.0, 0.5, 1.0, 1.5):
        p = urn.dist(1.1, g, 1000); c = np.cumsum(p); qs = {f: int(np.searchsorted(c, f)) / 1000 for f in (0.05, 0.25, 0.5, 0.75, 0.95)}; A['shares'][str(g)] = dict(p=p.tolist(), q=qs)
        print(f"   g = {g}: one market in twenty below {qs[0.05]:.3f}, a quarter below {qs[0.25]:.3f}, half below {qs[0.5]:.3f}, a quarter above {qs[0.75]:.3f}, one in twenty above {qs[0.95]:.3f}; share under a tenth with chance {float(p[:100].sum()):.4f}, over nine tenths {float(p[901:].sum()):.4f}")
if '9' in SEC:
    print("9. More than in proportion: P as the sales grow (q = 1.1), and the limit by another route (the two clocks, sampled)"); A['lockin'] = {}
    rng = np.random.default_rng(99)
    for g in (1.25, 1.5, 2.0):
        p, kept = urn.dist(1.1, g, 100000, keep=(100, 1000, 10000)); kept[100000] = p; vals = {N: urn.ahead(kept[N]) for N in (100, 1000, 10000, 100000)}
        J = 20000; j = np.arange(1, J + 1.0) ** g; tail = float(np.sum(np.arange(J + 1, 40 * J + 1.0) ** -g)) + (40 * J) ** (1 - g) / (g - 1); M = 400000; SA = np.zeros(M); SB = np.zeros(M)
        for lo in range(0, J, 500): SA += (rng.exponential(size=(M, 500)) / j[lo:lo + 500]).sum(axis=1); SB += (rng.exponential(size=(M, 500)) / j[lo:lo + 500]).sum(axis=1)
        est = float(np.mean((SA + tail) / 1.1 < SB + tail)); se = math.sqrt(est * (1 - est) / M); A['lockin'][str(g)] = dict(vals={str(k): v for k, v in vals.items()}, limit=est, se=se)
        print(f"   g = {g}: " + "; ".join(f"{N:,}: {v:.4f}" for N, v in vals.items()) + f"; the limit, sampled from the clocks: {est:.4f} (standard error {se:.4f})", flush=True)
if 'r' in SEC:
    print("r. The early lead by sampling: 200,000 markets, q = 1.1, g = 1, a = 1"); rng = np.random.default_rng(7); M = 200000; nA = np.zeros(M)
    for n in range(10000):
        pa = 1.1 * (1 + nA); pa = pa / (pa + (1 + n - nA)); nA += rng.random(M) < pa
        if n + 1 == 100: lead = np.sign(nA - 50)
    end = np.sign(nA - 5000); sel = lead != 0; same = float(np.mean(lead[sel] == end[sel])); back = float(np.mean(end[lead < 0] > 0) + 0.5 * np.mean(end[lead < 0] == 0)); A['lead_sampled'] = dict(same=same, back=back, n=int(sel.sum()), nB=int((lead < 0).sum()))
    print(f"   the leader after 100 is the leader after 10,000 in {same:.4f} of {int(sel.sum()):,} markets (standard error {math.sqrt(same * (1 - same) / sel.sum()):.4f}); where the worse product led after 100, the better is ahead after 10,000 in {back:.4f} of {int((lead < 0).sum()):,} (standard error {math.sqrt(back * (1 - back) / (lead < 0).sum()):.4f})")
if 'v' in SEC:
    print("v. Less than in proportion: the better product's mean share and its scatter as the sales grow (q = 1.1, a = 1)"); A['scatter'] = {}
    for g in (0.0, 0.25, 0.5, 0.75):
        p, kept = urn.dist(1.1, g, 100000, keep=(1000, 10000)); kept[100000] = p; odds = 1.1 ** (1 / (1 - g)); xs = odds / (1 + odds); row = {}
        for N in (1000, 10000, 100000):
            k = np.arange(N + 1) / N; mean = float(kept[N] @ k); sd = math.sqrt(float(kept[N] @ (k - mean) ** 2)); row[str(N)] = (mean, sd)
        A['scatter'][str(g)] = dict(settles=xs, rows=row)
        print(f"   g = {g}: the share should settle at {xs:.4f}; mean share {row['1000'][0]:.4f}, {row['10000'][0]:.4f}, {row['100000'][0]:.4f} after 1,000, 10,000, 100,000 sales; scatter (standard deviation) {row['1000'][1]:.5f}, {row['10000'][1]:.5f}, {row['100000'][1]:.5f}; scatter times the square root of the sales: {row['1000'][1] * math.sqrt(1000):.3f}, {row['10000'][1] * 100:.3f}, {row['100000'][1] * math.sqrt(100000):.3f}" + (f" (theory for large numbers: {math.sqrt(xs * (1 - xs) / (1 - 2 * g)):.3f})" if g < 0.5 else ""), flush=True)
if 'c' in SEC:
    print("c. Curves for the figure: P against the number of sales, q = 1.1"); NS = (10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000); A['curves'] = {}
    for g in (0.0, 0.5, 1.0, 1.5):
        p, kept = urn.dist(1.1, g, 100000, keep=NS[:-1]); kept[100000] = p; A['curves'][str(g)] = {str(N): urn.ahead(kept[N]) for N in NS}; print(f"   g = {g}: " + "; ".join(f"{N:,}: {A['curves'][str(g)][str(N)]:.4f}" for N in NS), flush=True)
if '0' in SEC:
    print("0. Does a little imitation ever help? P at g = 0.1 and g = 0.25 less P at g = 0, for each number of sales up to 300 (a = 1)"); A['help'] = {}
    for q in (1.02, 1.05, 1.1, 1.25, 1.5, 2.0):
        keep = tuple(range(1, 301)); base = urn.dist(q, 0.0, 300, keep=keep)[1]; res = {}
        for g in (0.1, 0.25):
            k = urn.dist(q, g, 300, keep=keep)[1]; d = {N: urn.ahead(k[N]) - urn.ahead(base[N]) for N in keep}; last = max((N for N in keep if d[N] > 1e-12), default=0); big = max(d, key=d.get); res[str(g)] = dict(last=last, most=d[big], at=big)
        A['help'][str(q)] = res; print(f"   q = {q}: g = 0.1 helps up to {res['0.1']['last']} sales (by at most {res['0.1']['most']:.5f}, at {res['0.1']['at']} sales); g = 0.25 helps up to {res['0.25']['last']} sales (by at most {res['0.25']['most']:.5f}, at {res['0.25']['at']})", flush=True)
json.dump(A, open(OUT, "w"))
