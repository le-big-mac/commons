import sys; sys.path.insert(0, "/home/agent2/drum12/referee")
import numpy as np, json, time
import sol
D12 = "/home/agent2/drum12/"; best = json.load(open(D12 + "best.json")); SEC = sys.argv[1]; t0 = time.time()
A = lambda k: np.array(best[k]['a'])
def ex(a, F):
    a = np.asarray(a); return np.abs(sol.misses(sol.ring_edges(len(a)), 1 + a, sol.fam_modes(F), max(10, 1600 // len(a)), exact=True)).max()
def scale(a, M):
    w = sol.ring_w(len(a)); return a * min(1.0, M / (w @ a))
def run(starts, F, M, polish=True):
    modes = sol.fam_modes(F); R = len(starts[0][1]); res = []
    for nm, a0 in starts:
        a, f = sol.slp(scale(a0, M), modes, M, p=max(8, 800 // R), iters=300)
        res.append((f, nm, a))
    res.sort(key=lambda z: z[0]); f, nm, a = res[0]
    if polish: a, f = sol.slp(a, modes, M, p=max(8, 800 // R), iters=30, exact=True, tr0=0.05)
    return ex(a, F), nm, a, [(round(100 * r[0], 4), r[1]) for r in res]
if SEC == "A":
    for key, F, M in (("sixteen|4|40", 7, 4.0), ("twelve|2.79|40", 6, 2.79)):
        a, f = sol.slp(A(key), sol.fam_modes(F), M, p=20, iters=60, exact=True, tr0=0.05)
        print("exact-measure polish of the author's %s: author %.4f%% -> %.4f%% (largest change in a ring %.2f)" % (key, 100 * best[key]['exact'], 100 * ex(a, F), np.abs(a - A(key)).max()), flush=True)
        json.dump(a.tolist(), open("/home/agent2/drum12/referee/polished_%s.json" % key.replace("|", "_"), "w"))
    b16 = np.array(json.load(open("/home/agent2/drum12/referee/blind2_F7_M4_R40_s2.json"))['a'])
    for M in (3.0, 3.2, 3.4, 3.6):
        f, nm, a, allr = run([("author 2.79", A("sixteen|2.79|40")), ("author 4 scaled", A("sixteen|4|40")), ("my blind 4 scaled", b16)], 7, M)
        print("sixteen modes, 40 rings, %.1f skins: least I find %.4f%% (exact) from '%s'; ends %s  t=%.0fs" % (M, 100 * f, nm, allr, time.time() - t0), flush=True)
if SEC == "B":
    f, nm, a, allr = run([("author 4|80 as is", A("twelve|4|80")), ("author 9.6|80 scaled", A("twelve|9.6|80")), ("author 6|80", A("twelve|6|80"))], 6, 6.0)
    print("twelve modes, 80 rings, 6 skins: author 0.6986%%; least I find %.4f%% (exact) from '%s'; ends %s; mass used %.3f  t=%.0fs" % (100 * f, nm, allr, sol.ring_w(80) @ a, time.time() - t0), flush=True)
    b16 = np.array(json.load(open("/home/agent2/drum12/referee/blind2_F7_M4_R40_s2.json"))['a'])
    f, nm, a, allr = run([("author 6|80 scaled", A("sixteen|6|80")), ("author 2.79|80", A("sixteen|2.79|80")), ("my blind 40-ring split", np.repeat(b16, 2)), ("author 4|80", A("sixteen|4|80"))], 7, 4.0)
    print("sixteen modes, 80 rings, 4 skins: author 0.9235%%; least I find %.4f%% (exact) from '%s'; ends %s  t=%.0fs" % (100 * f, nm, allr, time.time() - t0), flush=True)
if SEC == "C":
    ch = json.load(open("/home/agent2/drum/chain-free-up.json"))
    print("first study's walk up, nine modes: " + ", ".join("%g: %.3f%%" % (r['weight'], 100 * r['miss']) for r in ch))
    for r in ch:
        if r['weight'] in (1.2, 1.3): print("   my exact value of its load at %g skins: %.4f%%" % (r['weight'], 100 * ex(np.array(r['a']), 5)))
    f, nm, a, allr = run([("author 1.8", A("twelve|1.8|40")), ("author 2 scaled", A("twelve|2|40"))], 6, 1.9)
    print("twelve modes, 40 rings, 1.9 skins: least I find %.4f%% (exact); ends %s" % (100 * f, allr), flush=True)
    f, nm, a, allr = run([("author 1.8", A("twelve|1.8|40")), ("author 2 scaled", A("twelve|2|40"))], 6, 1.85)
    print("twelve modes, 40 rings, 1.85 skins: least I find %.4f%% (exact); ends %s" % (100 * f, allr), flush=True)
    # tolerance
    rng = np.random.default_rng(5); modes = sol.fam_modes(7); a = A("sixteen|4|40"); e = sol.ring_edges(40)
    mi = lambda x: np.abs(sol.misses(e, 1 + x, modes, 20)).max()
    v = np.array([mi(a * (1 + 0.01 * rng.standard_normal(40))) for _ in range(300)])
    print("tolerance, sixteen|4|40 (FEM): as found %.3f%%; each ring off 1%% sd, 300 draws: median %.3f%%, 90th %.3f%%; all rings x1.01 together %.3f%%, x0.99 %.3f%%; moved out one ring %.2f%%, moved in one ring %.2f%%" % (100 * mi(a), 100 * np.median(v), 100 * np.quantile(v, 0.9), 100 * mi(1.01 * a), 100 * mi(0.99 * a), 100 * mi(np.concatenate([[a[0]], a[:-1]])), 100 * mi(np.concatenate([a[1:], [0]]))), flush=True)
    # two discs
    from scipy.optimize import differential_evolution, minimize
    m12 = sol.fam_modes(6)
    def two(ko, ki, Mo, Mi, exact=False, p=120):
        ko, ki = max(ko, ki), min(ko, ki)
        if ko - ki < 1e-4 or ki < 1e-3: return 9.0
        lo, li = Mo / ko**2, Mi / ki**2
        return np.abs(sol.misses(np.array([ki, ko, 1.0]), np.array([1 + lo + li, 1 + lo, 1.0]), m12, p, exact)).max()
    d = json.load(open(D12 + "after-2-twelve-2.79.json")); ko, ki = d['radii']; sh = d['share']
    print("author's two discs at 2.79 skins (radii %.4f, %.4f, share %.3f): author's figure (800 finite-difference cells) %.3f%%; exact by my solver %.4f%%" % (ko, ki, sh, 100 * d['miss'], 100 * two(ko, ki, sh * 2.79, (1 - sh) * 2.79, True, 300)), flush=True)
    g = lambda y: two(y[0], y[1], y[3] * y[2], (1 - y[3]) * y[2])
    r = differential_evolution(g, [(0.1, 0.95), (0.03, 0.7), (0.3, 2.79), (0.0, 1.0)], seed=1, tol=1e-8, maxiter=120, popsize=14, x0=[ko, ki, 2.79, sh])
    r2 = minimize(lambda y: two(y[0], y[1], y[3] * y[2], (1 - y[3]) * y[2], True, 300) if (0.3 <= y[2] <= 2.79 and 0 <= y[3] <= 1) else 9.0, r.x, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=500))
    y = r2.x; print("two discs, total mass free up to 2.79 (DE on FEM, then Nelder-Mead on exact): %.4f%% at radii %.4f, %.4f, total mass %.3f, share in wider %.3f   t=%.0fs" % (100 * r2.fun, max(y[0], y[1]), min(y[0], y[1]), y[2], y[3], time.time() - t0), flush=True)
if SEC == "D":
    d = json.load(open(D12 + "after-N-10-12.json"))['rings']['40']; a12 = np.array(d['a']); modes = sol.fam_modes(10); rng = np.random.default_rng(3)
    for M, tag in ((24.0, "24 skins"), (12.0, "12 skins")):
        st = [a12 * (M / 12.0), a12, a12 * (M / 12.0) * np.exp(0.2 * rng.standard_normal(40))]
        out = []
        for a0 in st:
            a, f = sol.slp(scale(a0, M), modes, M, p=20, iters=150)
            out.append((ex(a, 10), sol.ring_w(40) @ a)); print("  thirty modes, 40 rings, %s: end %.4f%% exact, mass used %.2f  t=%.0fs" % (tag, 100 * out[-1][0], out[-1][1], time.time() - t0), flush=True)
            if time.time() - t0 > 75: break
        if time.time() - t0 > 75: break
if SEC == "E":
    def st(name, a, F):
        sp = sol.spectrum(a, 40, 10); fam = set((m, n) for m, n, f in sol.fam_modes(F))
        print("  %-34s outsiders below %d+1: %s" % (name, F, ", ".join("(%d,%d) %.3f" % (m, n, x) for x, m, n in sp if x < F + 1.0 and (m, n) not in fam) or "none"))
    st("sealed twelve|12|40 (0.7047%)", np.array(json.load(open(D12 + "s-twelve-12.json"))['rings']['40']['a']), 6)
    st("walk's twelve|12|40 (0.6954%)", A("twelve|12|40"), 6)
    st("sealed twelve|2.79|40", np.array(json.load(open(D12 + "s-twelve-2.79.json"))['rings']['40']['a']), 6)
    a = A("twelve|12|40"); w = sol.ring_w(40); print("  walk's twelve|12|40: mass beyond r=0.45: %.2f skins of %.2f; miss with that outer ring removed: %.3f%%" % (w[18:] @ a[18:], w @ a, 100 * ex(np.where(np.arange(40) < 18, a, 0), 6)))
    a = A("twelve|2.79|40"); print("  walk's twelve|2.79|40: mass beyond r=0.45: %.3f skins; miss with it removed: %.3f%%" % (w[18:] @ a[18:], 100 * ex(np.where(np.arange(40) < 18, a, 0), 6)))
    # D with the fundamental floated
    nine = np.array(next(r for r in json.load(open("/home/agent2/drum/chain-free-up.json")) if abs(r['weight'] - 1.43) < 1e-9)['a'])
    for name, e, rho, p in (("nine-mode disc", [0.4004, 1.0], [9.938, 1.0], 800), ("nine rings 1.43", sol.ring_edges(40), 1 + nine, 40), ("sixteen|4|40", sol.ring_edges(40), 1 + A("sixteen|4|40"), 40)):
        dpin, parts = sol.myD(e, rho, p=p, parts=True)
        def dfl(g): return sum(wt * abs(1200 * np.log2((r / g) / max(1, round(r / g)))) for r, m, n, wt, c in parts)
        gs = np.linspace(0.96, 1.04, 1601); v = [dfl(g) for g in gs]; i = int(np.argmin(v))
        print("  D for %-16s pinned to the lowest mode %.1f; with the fundamental floated %.1f (base at %.4f of the lowest mode)" % (name, dpin, v[i], gs[i]))
print("# section %s done in %.0fs" % (SEC, time.time() - t0))
