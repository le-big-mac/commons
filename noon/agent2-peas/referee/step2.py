# Referee's controls for Step 2. Uses only the referee's own counts (blind.py).
import math, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))   # the referee's own folder only (blind.py)
import numpy as np
from scipy import stats
from blind import F2, F3, PLANTS, BI, TRI, BACK, parse, zbin

rng = np.random.default_rng(20261122)
norm = stats.norm
SIMPLE = [(a, b, .75) for a, b in F2] + [(a, b, 2 / 3) for a, b in F3] + [(a, b, .75) for a, b in PLANTS]
MULTI = [('two-char', BI)] + [('three-char', TRI)] + list(BACK.items())


def split_sets(labels, order, scheme):
    st = {lab: parse(lab) for lab in labels}
    tests = []
    for depth, ch in enumerate(order):
        earlier = order[:depth]
        for combo in sorted({tuple(s[e] for e in earlier) for s in st.values()}):
            grp = {}
            for lab, s in st.items():
                if tuple(s[e] for e in earlier) == combo:
                    grp.setdefault(s[ch], []).append(lab)
            nm = f"{'ABC'[ch]}|" + ','.join(f"{'ABC'[e]}={c}" for e, c in zip(earlier, combo))
            if len(grp) == 3:
                D, H, R = grp['D'], grp['H'], grp['R']
                if scheme == 'hyb':
                    tests += [(nm + ' H v D+R', H, D + R, .5), (nm + ' D v R', D, R, .5)]
                elif scheme == 'pheno':
                    tests += [(nm + ' D+H v R (3:1)', D + H, R, .75), (nm + ' H v D (2:1)', H, D, 2 / 3)]
                elif scheme == 'dom':
                    tests += [(nm + ' D v H+R (1:3)', D, H + R, .25), (nm + ' H v R (2:1)', H, R, 2 / 3)]
            else:
                (s1, l1), (s2, l2) = sorted(grp.items())
                tests.append((nm + f' {s1} v {s2}', l1, l2, .5))
    return tests


def zs(counts, labels, tests):
    """counts: array (..., K). returns z array (..., ntests)."""
    idx = {l: i for i, l in enumerate(labels)}
    out = []
    for _, A, B, p in tests:
        a = counts[..., [idx[l] for l in A]].sum(-1); b = counts[..., [idx[l] for l in B]].sum(-1); n = a + b
        with np.errstate(invalid='ignore', divide='ignore'):
            out.append(np.where(n > 0, (a - n * p) / np.sqrt(np.maximum(n, 1) * p * (1 - p)), 0.0))
    return np.stack(out, -1)


def all_z(order3=(0, 1, 2), order2=(0, 1), scheme='hyb', orderbc=None):
    z = [zbin(a, b, p) for a, b, p in SIMPLE]; names = [f'simple {i+1}' for i in range(35)]
    for nm, d in MULTI:
        labels = list(d); o = order3 if nm == 'three-char' else (order2 if nm == 'two-char' else (orderbc or order2))
        t = split_sets(labels, o, scheme); v = zs(np.array([d[l] for l in labels]), labels, t)
        z += list(v); names += [f'{nm} {x[0]}' for x in t]
    return np.array(z), names


def fits(z):
    z = np.abs(z); n = len(z); s2 = np.mean(z ** 2); c = z.max(); p = np.sort(2 * norm.sf(z))
    ll_s = float(np.sum(-0.5 * np.log(s2) - z ** 2 / (2 * s2) + z ** 2 / 2)); ll_c = float(-n * np.log(2 * norm.cdf(c) - 1))
    cum = np.concatenate([[0], np.cumsum(np.log(2 * p))]); nxt = np.concatenate([p, [1.0]])     # a -> next p from below (supremum of each piece)
    sup = cum + (n - np.arange(n + 1)) * np.log1p(nxt); k = int(np.argmax(sup))
    left = cum[1:] + (n - np.arange(1, n + 1)) * np.log1p(p)                                      # the author's choice: a just above each p (bottom of each piece)
    return dict(s=math.sqrt(s2), c=c, ll_s=ll_s, ll_c=ll_c, ll_a=float(sup[k]), a=float(nxt[k]), ll_a_left=float(left.max()), a_left=float(p[int(np.argmax(left))]), p=p)


def marginal(z):
    """log marginal likelihood relative to honest, each model's one number given a flat prior on (0,1): s; p-threshold of the cut; a."""
    z = np.abs(z); n = len(z); p = np.sort(2 * norm.sf(z))
    s = np.linspace(1e-3, 1, 20000); ls = np.array([np.sum(-np.log(x) - z ** 2 / (2 * x * x) + z ** 2 / 2) for x in s]); m_s = np.log(np.trapezoid(np.exp(ls - ls.max()), s)) + ls.max()
    m_c = np.log(((1 - p[0]) ** (-(n - 1)) - 1) / (n - 1))
    a = np.linspace(0, 1, 400001)[:-1]; k = np.searchsorted(p, a, side='right'); cum = np.concatenate([[0], np.cumsum(np.log(2 * p))]); la = cum[k] + (n - k) * np.log1p(a)
    m_a = np.log(np.mean(np.exp(la - la.max()))) + la.max()
    return float(m_s), float(m_c), float(m_a)


def report(tag, z, names=None):
    f = fits(z); k = int(np.argmax(np.abs(z)))
    s = f"{tag:34s} sum z2 {np.sum(z**2):6.2f}  max|z| {np.abs(z).max():.3f}  none beyond: 1 in {1/(2*norm.cdf(np.abs(z).max())-1)**len(z):9,.0f}  <0.3: {int((np.abs(z)<.3).sum()):2d}  <0.5: {int((np.abs(z)<.5).sum()):2d}  logL s/c/a {f['ll_s']:5.2f} {f['ll_c']:5.2f} {f['ll_a']:5.2f}"
    if names: s += f"  [{names[k]}]"
    print(s); return f


print('=== A. the author\'s split, redone; other thresholds for "very close" ===')
z0, n0 = all_z(); f0 = report('author order, hyb contrasts', z0, n0)
for t in (.1, .2, .3, .4, .5, .6, .9):
    e = 84 * (2 * norm.cdf(t) - 1); es = 84 * (2 * norm.cdf(t / f0['s']) - 1); k = int((np.abs(z0) < t).sum())
    print(f"   |z|<{t}: seen {k:2d}; honest {e:5.1f} (sd {math.sqrt(e*(1-e/84)):.1f}); shrunk {es:5.1f}; P(<=seen | shrunk) {stats.binom.cdf(k, 84, es/84):.3f}; P(>=seen | honest) {stats.binom.sf(k-1, 84, e/84):.3f}")
print('   values of |z| between 0.25 and 0.35:', np.round(np.sort(np.abs(z0)[(np.abs(z0) > .25) & (np.abs(z0) < .35)]), 3))

print('=== B. other lawful splits ===')
res = {}
for scheme in ('hyb', 'pheno', 'dom'):
    rows = []
    for o3 in itertools.permutations(range(3)):
        for o2 in itertools.permutations(range(2)):
            for obc in itertools.permutations(range(2)):
                z, nm = all_z(o3, o2, scheme, obc); f = fits(z)
                rows.append((o3, o2, obc, np.abs(z).max(), int((np.abs(z) < .3).sum()), float(np.sum(z ** 2)), f['ll_s'], f['ll_c'], f['ll_a'], nm[int(np.argmax(np.abs(z)))], f['s']))
    mx = [r[3] for r in rows]; sm = [r[4] for r in rows]; su = [r[5] for r in rows]
    print(f"scheme {scheme}: 24 orders. max|z| from {min(mx):.3f} to {max(mx):.3f} (beyond 1.8 in {sum(m > 1.8 for m in mx)}, beyond 2.0 in {sum(m > 2 for m in mx)}); count <0.3 from {min(sm)} to {max(sm)} (mean {np.mean(sm):.1f}); sum z2 {min(su):.2f} to {max(su):.2f}")
    print(f"   cut-off over shrunk: factor {math.exp(min(r[7]-r[6] for r in rows)):.3f} to {math.exp(max(r[7]-r[6] for r in rows)):.2f}; better-of-two over shrunk {math.exp(min(r[8]-r[6] for r in rows)):.2f} to {math.exp(max(r[8]-r[6] for r in rows)):.2f}; largest spread among the three: {math.exp(max(max(r[6:9]) - min(r[6:9]) for r in rows)):.1f}; smallest {math.exp(min(max(r[6:9]) - min(r[6:9]) for r in rows)):.1f}")
    w = max(rows, key=lambda r: r[3]); print(f"   furthest: orders {w[0]} {w[1]} {w[2]}: {w[3]:.3f} at {w[9]}")
    lo = min(rows, key=lambda r: r[4]); hi = max(rows, key=lambda r: r[4]); print(f"   fewest <0.3: {lo[4]} (shrunk predicts {84*(2*norm.cdf(.3/lo[10])-1):.1f}); most: {hi[4]} (shrunk predicts {84*(2*norm.cdf(.3/hi[10])-1):.1f})")
    res[scheme] = rows
for tag, kw in (('reverse order C,B,A / B,A, hyb', dict(order3=(2, 1, 0), order2=(1, 0), scheme='hyb')), ('author order, pheno (3:1 then 2:1)', dict(scheme='pheno')),
                ('reverse order, pheno', dict(order3=(2, 1, 0), order2=(1, 0), scheme='pheno')), ('author order, dom (1:3 then 2:1)', dict(scheme='dom'))):
    z, nm = all_z(**kw); report(tag, z, nm)

print('=== C. models: edge fitting ===')
print(f"   better of two: supremum {f0['ll_a']:.3f} as a -> {f0['a']:.4f} from below ({math.exp(f0['ll_a']):,.0f} times honest); author's rule (a just above a data value) {f0['ll_a_left']:.3f} at {f0['a_left']:.4f} ({math.exp(f0['ll_a_left']):,.0f})")
print('   p values near there:', np.round(f0['p'][(f0['p'] > .33) & (f0['p'] < .47)], 4))
print(f"   factors at the suprema: cut/shrunk {math.exp(f0['ll_c']-f0['ll_s']):.2f}; b2/shrunk {math.exp(f0['ll_a']-f0['ll_s']):.2f}; b2/cut {math.exp(f0['ll_a']-f0['ll_c']):.2f}")
ms, mc, ma = marginal(z0); print(f"   flat prior on each model's number (log marginal likelihood over honest): shrunk {ms:.2f}, cut-off {mc:.2f}, better of two {ma:.2f}; factors cut/shrunk {math.exp(mc-ms):.2f}, b2/shrunk {math.exp(ma-ms):.2f}, b2/cut {math.exp(ma-mc):.2f}")
zz = np.sort(np.abs(z0)); print(f"   two largest |z|: {zz[-1]:.4f}, {zz[-2]:.4f}. Cut-off logL if c were 1.8 / 2.0 instead: {-84*math.log(2*norm.cdf(1.8)-1):.2f} / {-84*math.log(2*norm.cdf(2.0)-1):.2f}")
f83 = fits(zz[:-1]); print(f"   without the single largest value (83): logL s/c/a {f83['ll_s']:.2f} {f83['ll_c']:.2f} {f83['ll_a']:.2f}; cut/shrunk {math.exp(f83['ll_c']-f83['ll_s']):.1f}")
z35 = z0[:35]; f35 = fits(z35); m35 = marginal(z35); print(f"   the 35: logL s/c/a {f35['ll_s']:.2f} {f35['ll_c']:.2f} {f35['ll_a']:.2f}; cut/shrunk {math.exp(f35['ll_c']-f35['ll_s']):.1f}; flat-prior marginals {m35[0]:.2f} {m35[1]:.2f} {m35[2]:.2f} (cut/shrunk {math.exp(m35[1]-m35[0]):.1f})")

print('=== D. goodness of fit of each fitted account (Kolmogorov distance of p, refitted in each of 2000 sets drawn from the fitted account) ===')
def cdfs(f):
    pc = 2 * norm.sf(f['c'])
    return dict(shrunk=lambda x: 2 * norm.sf(norm.isf(x / 2) / f['s']), cut=lambda x: np.clip((x - pc) / (1 - pc), 0, 1), b2=lambda x: np.where(x <= f['a'], x ** 2, (1 + f['a']) * x - f['a']))
def ks(f):
    p = f['p']; n = len(p); out = {}
    for k, F in cdfs(f).items():
        v = F(p); out[k] = float(max(np.max(np.arange(1, n + 1) / n - v), np.max(v - np.arange(n) / n)))
    return out
def draw(model, f, size):
    if model == 'shrunk': return rng.normal(0, f['s'], size)
    if model == 'cut': return norm.ppf(rng.uniform(norm.cdf(-f['c']), norm.cdf(f['c']), size))
    u = rng.random(size); v = rng.random(size); return norm.isf(np.where(u < f['a'], np.maximum(u, v), u) / 2)
k0 = ks(f0); B = 2000; n84 = 84
band = lambda z: int(((np.abs(z) >= .6) & (np.abs(z) < .9)).sum())
for model in ('shrunk', 'cut', 'b2'):
    sims = draw(model, f0, (B, n84)); d = []; small = []; sums = []; mid = []
    for r in sims:
        fr = fits(r); d.append(ks(fr)[model]); small.append(int((np.abs(r) < .3).sum())); sums.append(float(np.sum(r ** 2))); mid.append(band(r))
    print(f"   {model:7s} distance {k0[model]:.4f}; as large or larger in {100*np.mean(np.array(d) >= k0[model]):.1f}% of sets; <0.3: mean {np.mean(small):.1f}, 21 or fewer in {100*np.mean(np.array(small) <= 21):.1f}%; sum: mean {np.mean(sums):.1f}, <=41.54 in {100*np.mean(np.array(sums) <= 41.5407):.1f}%, >= in {100*np.mean(np.array(sums) >= 41.5407):.1f}%; 0.6-0.9 band: mean {np.mean(mid):.1f}, 27 or more in {100*np.mean(np.array(mid) >= 27):.2f}%")
# the sealed simulations again with another seed
def lr(r):
    fr = fits(r); return fr['ll_c'] - fr['ll_s']
s35 = rng.normal(0, f35['s'], (20000, 35)); s84 = rng.normal(0, f0['s'], (20000, 84))
print(f"   P13 again: {100*np.mean([lr(r) >= f35['ll_c']-f35['ll_s'] for r in s35]):.1f}%   Q5 again: {100*np.mean([lr(r) >= f0['ll_c']-f0['ll_s'] for r in s84]):.1f}%   Q6 again: {100*np.mean((np.abs(s84) < .3).sum(1) <= 21):.1f}% (exact binomial {100*stats.binom.cdf(21, 84, 2*norm.cdf(.3/f0['s'])-1):.1f}%)")

print('=== E. discreteness: the true binomials and multinomials, honest sampling ===')
c = float(np.abs(z0).max()) + 1e-9; edges = [0, .3, .6, .9, 1.2, 1.5, 1.8, 99]
exp_b = np.zeros(7); logp_none = 0.0
for a, b, p in SIMPLE:
    n = a + b; k = np.arange(n + 1); pm = stats.binom.pmf(k, n, p); zk = np.abs((k - n * p) / math.sqrt(n * p * (1 - p)))
    exp_b += np.array([pm[(zk >= lo) & (zk < hi)].sum() for lo, hi in zip(edges, edges[1:])]); logp_none += math.log(pm[zk <= c].sum())
print(f"   the 35 simple tests, exact: expected within 0.3: {exp_b[0]:.2f} (normal: {35*(2*norm.cdf(.3)-1):.2f}); chance none beyond {c:.4f}: {math.exp(logp_none):.5f} (normal: {(2*norm.cdf(c)-1)**35:.5f})")
N = 400000; cnt = np.zeros(N, int); tot = np.zeros(N); mx = np.zeros(N)
for a, b, p in SIMPLE:
    n = a + b; k = rng.binomial(n, p, N); z = (k - n * p) / math.sqrt(n * p * (1 - p)); cnt += np.abs(z) < .3; tot += z ** 2; mx = np.maximum(mx, np.abs(z))
pear = tot.copy()
for nm, d in MULTI:
    labels = list(d); n = sum(d.values()); w = np.array([2.0 ** parse(l).count('H') for l in labels]) if nm in ('two-char', 'three-char') else np.ones(4); w /= w.sum()
    X = rng.multinomial(n, w, N); z = zs(X, labels, split_sets(labels, tuple(range(len(parse(labels[0])))), 'hyb')); az = np.abs(z)
    exp_b += np.array([((az >= lo) & (az < hi)).sum(1).mean() for lo, hi in zip(edges, edges[1:])]); pn = float((az.max(1) <= c).mean()); logp_none += math.log(pn)
    cnt += (az < .3).sum(1); tot += (z ** 2).sum(1); mx = np.maximum(mx, az.max(1)); pear += ((X - n * w) ** 2 / (n * w)).sum(1)
    print(f"      {nm:12s} {z.shape[1]:2d} tests: within 0.3 on average {(az<.3).sum(1).mean():.2f} (normal {z.shape[1]*(2*norm.cdf(.3)-1):.2f}); none beyond: {pn:.4f} (normal {(2*norm.cdf(c)-1)**z.shape[1]:.4f})")
print(f"   all 84: expected in the seven bands {np.round(exp_b, 1)} (normal: {np.round([84*2*(norm.cdf(hi)-norm.cdf(lo)) for lo, hi in zip(edges, edges[1:])], 1)})")
print(f"   chance of none beyond {c:.4f}: {math.exp(logp_none):.3e} = 1 in {math.exp(-logp_none):,.0f} (normal: 1 in {1/(2*norm.cdf(c)-1)**84:,.0f}); direct count in {N} tables: {int((mx <= c).sum())}")
print(f"   count within 0.3: mean {cnt.mean():.2f}, sd {cnt.std():.2f}; 21 or more in {100*(cnt >= 21).mean():.1f}%; 21 or fewer in {100*(cnt <= 21).mean():.1f}%")
print(f"   sum of 84 z squared: mean {tot.mean():.2f}, sd {tot.std():.2f} (chi-squared: 84, {math.sqrt(168):.2f}); P(<=50) {np.mean(tot <= 50):.5f} (chi-squared {stats.chi2.cdf(50, 84):.5f}); P(<=41.5407) {np.mean(tot <= 41.5407):.2e}")
print(f"   Pearson total as Fisher grouped it: mean {pear.mean():.2f}, sd {pear.std():.2f}; P(<=50) {np.mean(pear <= 50):.5f}; P(<=45) {np.mean(pear <= 45):.2e} (chi-squared {stats.chi2.cdf(45, 84):.2e}); P(<=41.6055) {np.mean(pear <= 41.6055):.2e} (chi-squared {stats.chi2.cdf(41.6055, 84):.2e})")

print('=== F. counting on until it looks right: the rule tried, and wider bands ===')
T = 400
def stopping(n, p, trials, band, lo_f=.5, hi_f=1.5):
    lo, hi = math.ceil(n * lo_f), math.floor(n * hi_f); out = np.empty(trials); done = 0
    while done < trials:
        b = min(trials - done, max(1, int(4e6 // hi))); cs = np.cumsum(rng.random((b, hi)) < p, axis=1)[:, lo - 1:]; kk = np.arange(lo, hi + 1)
        zz = (cs - kk * p) / np.sqrt(kk * p * (1 - p)); ok = np.abs(zz) <= band; first = np.where(ok.any(1), ok.argmax(1), hi - lo); out[done:done + b] = zz[np.arange(b), first]; done += b
    return out
obs_in = int((np.abs(z35) <= .5).sum()); obs_small = int((np.abs(z35) < .3).sum())
for bandw, lo_f in ((.5, .5), (1.0, .5), (1.25, .5), (1.5, .5), (1.5, 1.0), (2.0, .5)):
    Z = np.array([stopping(a + b, p, T, bandw, lo_f) for a, b, p in SIMPLE]); ins = (np.abs(Z) <= .5).sum(0); sm = (np.abs(Z) < .3).sum(0); mxs = np.abs(Z).max(0)
    lrs = np.array([lr(Z[:, j]) for j in range(T)])
    print(f"   band {bandw} sd, from {lo_f} n: mean chi2 {np.mean(Z**2):.3f} (seen {np.mean(z35**2):.3f}); within 0.5: {ins.mean():.1f} of 35 (seen {obs_in}; {obs_in} or fewer in {100*np.mean(ins <= obs_in):.1f}%); within 0.3: {sm.mean():.1f} (seen {obs_small}); largest |z| <= 1.424 in {100*np.mean(mxs <= 1.4238):.1f}%; median largest {np.median(mxs):.2f}; mean sum z2 {np.mean((Z**2).sum(0)):.1f} (seen {np.sum(z35**2):.1f}), <= seen in {100*np.mean((Z**2).sum(0) <= np.sum(z35**2)):.1f}%")

print('=== G. fifteen simple experiments ===')
z15 = [zbin(a, b, p) for a, b, p in SIMPLE[:15]]; print('   z against 3:1 and 2:1:', np.round(z15, 3))
pf = (2 / 3) * (1 - .75 ** 10); print('   the six of 100 against Fisher\'s share:', np.round([(a - 100 * pf) / math.sqrt(100 * pf * (1 - pf)) for a, b in F3[2:]], 2))
