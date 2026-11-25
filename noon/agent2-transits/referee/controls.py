"""Referee controls. Usage: python -I controls.py pscomppars.csv ledger.csv"""
import sys
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv(sys.argv[1])
t = df[df.discoverymethod == "Transit"].copy()
P = print
TESS = "Transiting Exoplanet Survey Satellite (TESS)"
def route(f):
    if f in ("Kepler", "K2"): return "Kepler/K2"
    if f == TESS: return "TESS"
    return "other"
t["route"] = t.disc_facility.map(route)

P("==== A. WHAT THE CATALOGUE'S NUMBERS ARE")
P("facilities in 'other' (README calls them ground surveys):")
P(t[t.route == "other"].disc_facility.value_counts().to_dict())
# eccentricity
P("-- eccentricity: pl_orbeccenlim value counts among transit planets:", t.pl_orbeccenlim.value_counts(dropna=False).to_dict())
P("   e exactly 0:", int((t.pl_orbeccen == 0).sum()), "of", int(t.pl_orbeccen.notna().sum()), "stated; by route:")
for r, g in t.groupby("route"):
    s = g.pl_orbeccen.dropna()
    P(f"     {r}: stated {len(s)}/{len(g)}, zeros {int((s==0).sum())} ({(s==0).mean():.2f}), lim=1: {int((g.pl_orbeccenlim==1).sum())}, lim=-1: {int((g.pl_orbeccenlim==-1).sum())}")
g8 = t[(t.pl_rade >= 8) & t.pl_orbeccen.notna()]
for nm, sel in (("P<5", g8[g8.pl_orbper < 5]), ("P>20", g8[g8.pl_orbper > 20])):
    e = sel.pl_orbeccen
    P(f"   giants {nm}: n={len(e)} zeros={int((e==0).sum())} lim1={int((sel.pl_orbeccenlim==1).sum())} "
      f"measured(nonzero,lim=0)={int(((e>0)&(sel.pl_orbeccenlim==0)).sum())} median all={e.median():.3f} "
      f"median nonzero={e[e>0].median():.3f} median nonzero&lim0={e[(e>0)&(sel.pl_orbeccenlim==0)].median():.3f}")
    vc = e.round(4).value_counts().head(8)
    P("      most repeated values:", vc.to_dict())
# share of zeros by period in giants: is the P<5 vs P>20 contrast a contrast of defaults?
P("   giants: share of exact zero by period band:", {f"{a}-{b}": round(float((g8[(g8.pl_orbper>=a)&(g8.pl_orbper<b)].pl_orbeccen==0).mean()),2) for a,b in ((0,5),(5,10),(10,20),(20,1e9))})
# radii
P("-- radii: missing error bars (often = value computed/converted, not quoted with errors):")
t["noerr"] = t.pl_radeerr1.isna()
P("   pl_rade without errors:", int(t.noerr.sum()), "of", len(t), "; by route:", t.groupby("route").noerr.mean().round(3).to_dict())
dec = t.pl_rade.dropna().map(lambda v: len(f"{v:.8f}".rstrip("0").split(".")[1]))
P("   decimals in pl_rade (count):", dec.value_counts().sort_index().to_dict())
P("   most repeated pl_rade values:", t.pl_rade.round(3).value_counts().head(12).to_dict())
P("   pl_bmasse present:", int(t.pl_bmasse.notna().sum()), "(not used by the study)")
# metallicity
P("-- metallicity: st_metratio kinds:", t.st_metratio.value_counts(dropna=False).to_dict())
P("   most repeated st_met values:", t.st_met.round(4).value_counts().head(12).to_dict())
P("   share of st_met exactly 0:", round(float((t.st_met == 0).mean()), 4), "; by route:", t.groupby("route").st_met.apply(lambda s: round(float((s == 0).mean()), 3)).to_dict())
dec = t.st_met.dropna().map(lambda v: len(f"{v:.6f}".rstrip("0").split(".")[1]) if "." in f"{v:.6f}".rstrip("0") else 0)
P("   decimals in st_met:", dec.value_counts().sort_index().to_dict())
P("   st_metratio by route:"); P(pd.crosstab(t.route, t.st_metratio.fillna("none")).to_string())

P("\n==== B. RESONANCES")
pairs = []
tp = t[t.pl_orbper.notna()]
allp = df[df.pl_orbper.notna()]
byhost_all = {h: g for h, g in allp.groupby("hostname")}
for h, g in tp.groupby("hostname"):
    if len(g) < 2: continue
    g = g.sort_values("pl_orbper")
    ga = byhost_all[h]
    for i in range(len(g) - 1):
        a, b = g.iloc[i], g.iloc[i + 1]
        between = int(((ga.pl_orbper > a.pl_orbper) & (ga.pl_orbper < b.pl_orbper) & (ga.discoverymethod != "Transit")).sum())
        pairs.append(dict(host=h, nsys=len(g), p_in=a.pl_orbper, p_out=b.pl_orbper, r_in=a.pl_rade, r_out=b.pl_rade,
                          srad=a.st_rad, route_in=a.route, route_out=b.route, between=between, teff=a.st_teff,
                          sy_pnum=a.sy_pnum, y_in=a.disc_year, y_out=b.disc_year, e1_in=a.pl_radeerr1, e1_out=b.pl_radeerr1))
pr = pd.DataFrame(pairs); pr["ratio"] = pr.p_out / pr.p_in
P("pairs", len(pr), "; pairs with a non-transit-discovered planet lying between the two 'neighbours':", int((pr.between > 0).sum()))
P("hosts where sy_pnum > number of transit-discovered planets with a period:", int((pr.drop_duplicates('host').sy_pnum > pr.drop_duplicates('host').nsys).sum()), "of", pr.host.nunique())
def cnt(lo, hi, d=pr): return int(((d.ratio >= lo) & (d.ratio < hi)).sum())
P("window width sweep (inside | outside | ratio | one-sided binomial p for outside>inside):")
for c in (1.5, 2.0):
    for w in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08):
        i, o = cnt(c - w, c), cnt(c, c + w)
        p = stats.binomtest(o, o + i, 0.5, alternative="greater").pvalue if o + i else float("nan")
        P(f"   centre {c} width {w}: inside {i} outside {o} ratio {o/max(i,1):.2f} p={p:.2g}")
P("local density (pairs per 0.01 of ratio):")
for lo, hi in ((1.30, 1.44), (1.44, 1.47), (1.47, 1.50), (1.50, 1.53), (1.53, 1.56), (1.56, 1.70), (1.80, 1.92), (1.92, 1.96), (1.96, 2.00), (2.00, 2.04), (2.04, 2.08), (2.08, 2.20)):
    n = cnt(lo, hi); P(f"   {lo:.2f}-{hi:.2f}: {n} pairs, {n/((hi-lo)*100):.2f} per 0.01")
# same test at centres with no first-order resonance: how often does the 'outside/inside' ratio exceed threshold by chance shape?
P("placebo centres (same test, width 0.03, threshold >1.5x) and (width 0.04, >1.3x):")
cs = np.round(np.arange(1.25, 2.56, 0.05), 2)
res3 = [(c, cnt(c - 0.03, c), cnt(c, c + 0.03)) for c in cs]
res4 = [(c, cnt(c - 0.04, c), cnt(c, c + 0.04)) for c in cs]
P("   w=0.03:", [(float(c), i, o, round(o / max(i, 1), 2)) for c, i, o in res3])
P("   w=0.03 placebo 'held' at", sum(o > 1.5 * i for c, i, o in res3 if c not in (1.5, 2.0)), "of", len(cs) - 2, "non-resonant centres")
P("   w=0.04 placebo 'held' at", sum(o > 1.3 * i for c, i, o in res4 if c not in (1.5, 2.0)), "of", len(cs) - 2, "non-resonant centres")
P("by size of system (transit planets with period):")
for lab, d in (("2-planet systems", pr[pr.nsys == 2]), ("3", pr[pr.nsys == 3]), ("4+", pr[pr.nsys >= 4]), ("<=3", pr[pr.nsys <= 3])):
    P(f"   {lab}: pairs {len(d)}; 3:2 inside {cnt(1.47,1.50,d)} outside {cnt(1.50,1.53,d)}; 2:1 inside {cnt(1.96,2.00,d)} outside {cnt(2.00,2.04,d)}")
o32 = pr[(pr.ratio >= 1.50) & (pr.ratio < 1.53)]; o21 = pr[(pr.ratio >= 2.00) & (pr.ratio < 2.04)]
P("   systems supplying the 60 pairs outside 3:2:", o32.host.nunique(), "; max pairs from one system:", int(o32.host.value_counts().max()), "; outside 2:1:", o21.host.nunique(), "max", int(o21.host.value_counts().max()))
P("   one pair per system (first by period) ->", end=" ")
d1 = pr.sort_values("p_in").drop_duplicates("host")
P(f"3:2 inside {cnt(1.47,1.50,d1)} outside {cnt(1.50,1.53,d1)}; 2:1 inside {cnt(1.96,2.00,d1)} outside {cnt(2.00,2.04,d1)}")
d2 = pr[pr.between == 0]
P(f"   dropping pairs with a non-transit planet between: 3:2 {cnt(1.47,1.50,d2)} vs {cnt(1.50,1.53,d2)}; 2:1 {cnt(1.96,2.00,d2)} vs {cnt(2.00,2.04,d2)}")
P("   by route of pair: ", {r: (cnt(1.47,1.50,d), cnt(1.50,1.53,d), cnt(1.96,2.00,d), cnt(2.00,2.04,d), len(d)) for r, d in pr.groupby("route_in")})
# system bootstrap of the two sealed ratios
rng = np.random.default_rng(1)
hosts = pr.host.unique(); idx = {h: np.where(pr.host.values == h)[0] for h in hosts}
rat = pr.ratio.values; b7 = []; b8 = []
for _ in range(2000):
    hs = rng.choice(hosts, len(hosts)); ii = np.concatenate([idx[h] for h in hs]); r = rat[ii]
    b7.append(((r >= 1.5) & (r < 1.53)).sum() / max(((r >= 1.47) & (r < 1.5)).sum(), 1))
    b8.append(((r >= 2.0) & (r < 2.04)).sum() / max(((r >= 1.96) & (r < 2.0)).sum(), 1))
P(f"   bootstrap over systems: X7 ratio 2.5-97.5%: {np.percentile(b7,2.5):.2f}-{np.percentile(b7,97.5):.2f}, share of resamples >1.5: {np.mean(np.array(b7)>1.5):.3f}; "
  f"X8: {np.percentile(b8,2.5):.2f}-{np.percentile(b8,97.5):.2f}, share >1.3: {np.mean(np.array(b8)>1.3):.3f}")

P("\n==== C. HOT JUPITERS ALONE")
hj = t[(t.pl_rade >= 8) & (t.pl_orbper < 10)]
P("hot Jupiters by facility group:", hj.route.value_counts().to_dict(), "; 'other' facilities that are space telescopes:",
  hj[hj.route == "other"].disc_facility[hj.disc_facility.str.contains("CoRoT|CHEOPS|Spitzer|Hubble|JWST|Webb", regex=True)].value_counts().to_dict())
def alone(d): return f"{int((d.sy_pnum==1).sum())}/{len(d)} = {(d.sy_pnum==1).mean():.3f}" if len(d) else "0/0"
classes = (("HJ (R>=8,P<10)", (t.pl_rade >= 8) & (t.pl_orbper < 10)), ("warm giants (R>=8,P>=10)", (t.pl_rade >= 8) & (t.pl_orbper >= 10)),
           ("R 4-8, P<10", (t.pl_rade >= 4) & (t.pl_rade < 8) & (t.pl_orbper < 10)), ("R<4, P<10", (t.pl_rade < 4) & (t.pl_orbper < 10)),
           ("all non-HJ", ~((t.pl_rade >= 8) & (t.pl_orbper < 10))))
for r in ("other", "Kepler/K2", "TESS"):
    for nm, m in classes:
        P(f"   {r:10s} {nm:26s} alone {alone(t[m & (t.route == r)])}")
for f in ("Kepler", "K2"):
    P(f"   {f} alone HJ: {alone(hj[hj.disc_facility == f])}")
comp = hj[hj.sy_pnum > 1]
P("   the", len(comp), "hot Jupiters with company: discovery method of the companions:")
cm = df[df.hostname.isin(comp.hostname) & ~df.pl_name.isin(comp.pl_name)]
P("     ", cm.discoverymethod.value_counts().to_dict(), "; by HJ route:", comp.route.value_counts().to_dict())
P("   sy_pnum vs rows in this table per host (mismatch count):", int((df.groupby('hostname').size() != df.groupby('hostname').sy_pnum.first()).sum()))
for lo in (6, 8, 10, 12):
    for ph in (5, 10):
        d = t[(t.pl_rade >= lo) & (t.pl_orbper < ph)]
        P(f"   definition R>={lo}, P<{ph}: alone {alone(d)}")

P("\n==== D. METALLICITY")
small = t[t.pl_rade < 4]
def mdiff(a, b, lab):
    a = a.st_met.dropna(); b = b.st_met.dropna()
    if len(a) < 5 or len(b) < 5: P(f"   {lab}: too few ({len(a)}, {len(b)})"); return
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    P(f"   {lab}: HJ {a.mean():+.3f} (n={len(a)}), small {b.mean():+.3f} (n={len(b)}), diff {a.mean()-b.mean():+.3f} se {se:.3f}; medians diff {a.median()-b.median():+.3f}")
mdiff(hj, small, "all, per planet")
mdiff(hj.drop_duplicates("hostname"), small.drop_duplicates("hostname"), "per star")
for k in ("[Fe/H]", "[M/H]"):
    mdiff(hj[hj.st_metratio == k], small[small.st_metratio == k], f"st_metratio {k} only")
P("   kinds: HJ", hj.st_metratio.value_counts(dropna=False).to_dict(), "small", small.st_metratio.value_counts(dropna=False).to_dict())
P("   mean st_met by kind among small:", small.groupby("st_metratio").st_met.agg(["mean", "count"]).round(3).to_dict("index"))
for r in ("other", "Kepler/K2", "TESS"):
    mdiff(hj[hj.route == r], small[small.route == r], f"route {r}")
P("   mean Teff: HJ", round(hj.st_teff.mean()), "small", round(small.st_teff.mean()))
tb = [(0, 4500), (4500, 5000), (5000, 5500), (5500, 6000), (6000, 6500), (6500, 20000)]
wsum = 0; wn = 0
for lo, hi in tb:
    a = hj[(hj.st_teff >= lo) & (hj.st_teff < hi)]; b = small[(small.st_teff >= lo) & (small.st_teff < hi)]
    mdiff(a, b, f"Teff {lo}-{hi}")
    aa = a.st_met.dropna(); bb = b.st_met.dropna()
    if len(aa) >= 5 and len(bb) >= 5:
        w = 1 / (1 / len(aa) + 1 / len(bb)); wsum += w * (aa.mean() - bb.mean()); wn += w
P(f"   Teff-stratified (precision-weighted) difference: {wsum/wn:+.3f}")
d = pd.concat([hj.assign(g=1), small.assign(g=0)]).dropna(subset=["st_met", "st_teff"])
X = np.column_stack([np.ones(len(d)), d.g, (d.st_teff - 5500) / 1000, ((d.st_teff - 5500) / 1000) ** 2])
beta = np.linalg.lstsq(X, d.st_met.values, rcond=None)[0]
P(f"   regression st_met ~ HJ + teff + teff^2: HJ coefficient {beta[1]:+.3f}")
dd = d[d.st_metratio.isin(["[Fe/H]"])]
X = np.column_stack([np.ones(len(dd)), dd.g, (dd.st_teff - 5500) / 1000, ((dd.st_teff - 5500) / 1000) ** 2])
P(f"   same, [Fe/H] only: HJ coefficient {np.linalg.lstsq(X, dd.st_met.values, rcond=None)[0][1]:+.3f}")
# small planets with zero-heaped or default metallicities removed
mdiff(hj[hj.st_met != 0], small[small.st_met != 0], "excluding st_met exactly 0")
P("   small-planet hosts mean st_met by disc_year band:", small.groupby(pd.cut(small.disc_year, [2000, 2013, 2015, 2017, 2020, 2030])).st_met.agg(["mean", "count"]).round(3).to_dict("index"))

P("\n==== E. HOT NEPTUNES")
bands = ((0, 3), (3, 10), (10, 30), (30, 100))
tr = t[t.pl_rade.notna()]
for r in ("all", "Kepler/K2", "Kepler", "TESS", "other"):
    d = tr if r == "all" else (tr[tr.disc_facility == "Kepler"] if r == "Kepler" else tr[tr.route == r])
    line = []
    for lo, hi in bands:
        s = d[(d.pl_orbper >= lo) & (d.pl_orbper < hi)]
        n = len(s); k = int(((s.pl_rade >= 3) & (s.pl_rade < 8)).sum()); gi = int((s.pl_rade >= 8).sum()); sm = int((s.pl_rade < 3).sum())
        line.append(f"{lo}-{hi}d: {k}/{n}={k/max(n,1):.3f} [giants {gi}, <3Re {sm}; Nep/(Nep+<3Re)={k/max(k+sm,1):.3f}; Nep/giants={k/max(gi,1):.2f}]")
    P(f"   {r}: " + " | ".join(line))
P("   mix of routes by period band (share Kepler/K2, TESS, other):")
for lo, hi in bands:
    s = tr[(tr.pl_orbper >= lo) & (tr.pl_orbper < hi)]
    P(f"     {lo}-{hi}d:", s.route.value_counts(normalize=True).round(3).to_dict())
P("   threshold sweep for X3 (share 3-8 at P<Pmax):", {pm: round(float(((tr[tr.pl_orbper < pm].pl_rade >= 3) & (tr[tr.pl_orbper < pm].pl_rade < 8)).mean()), 3) for pm in (1, 2, 3, 4, 5)})

P("\n==== F. NEIGHBOURS")
q = pr.dropna(subset=["r_in", "r_out"]).copy()
q["lx"] = np.log10(q.r_in); q["ly"] = np.log10(q.r_out)
def corr(d): return float(np.corrcoef(d.lx, d.ly)[0, 1]) if len(d) > 2 else float("nan")
def outl(d): return float((d.r_out > d.r_in).mean()) if len(d) else float("nan")
P(f"   all: r={corr(q):.3f} n={len(q)} outer larger {outl(q):.3f}")
s6 = q[(q.r_in < 6) & (q.r_out < 6)]
P(f"   both <6 Re: r={corr(s6):.3f} n={len(s6)} outer larger {outl(s6):.3f}; both <4: r={corr(q[(q.r_in<4)&(q.r_out<4)]):.3f} n={len(q[(q.r_in<4)&(q.r_out<4)])}")
# one pair per system; system bootstrap
P(f"   one pair per system: r={corr(q.sort_values('p_in').drop_duplicates('host')):.3f}")
# dividing out the stellar radius entirely (Rp/Rstar ~ transit depth^0.5)
qs = s6[s6.srad > 0].copy()
qs["kx"] = qs.lx - np.log10(qs.srad); qs["ky"] = qs.ly - np.log10(qs.srad)
P(f"   both<6, log(Rp/Rstar) (i.e. removing star's size with slope 1 not 0.28): r={np.corrcoef(qs.kx, qs.ky)[0,1]:.3f} n={len(qs)}")
# within narrow bands of stellar radius
qs["band"] = pd.qcut(qs.srad, 12)
rows = []
for b, d in qs.groupby("band", observed=True):
    rows.append((str(b), len(d), round(corr(d), 3), round(outl(d), 3)))
P("   both<6, within 12 quantile bands of stellar radius (band, n, r, outer larger):"); [P("     ", r) for r in rows]
P(f"   mean within-band r: {np.nanmean([r[2] for r in rows]):.3f}; pooled within-band (band means removed): "
  f"{np.corrcoef(qs.lx - qs.groupby('band', observed=True).lx.transform('mean'), qs.ly - qs.groupby('band', observed=True).ly.transform('mean'))[0,1]:.3f}")
# within route x band
kq = qs[(qs.route_in == "Kepler/K2") & (qs.route_out == "Kepler/K2")].copy()
kq["band"] = pd.qcut(kq.srad, 10)
P(f"   Kepler/K2 pairs both<6: r={corr(kq):.3f} n={len(kq)}; within 10 st_rad bands pooled: "
  f"{np.corrcoef(kq.lx - kq.groupby('band', observed=True).lx.transform('mean'), kq.ly - kq.groupby('band', observed=True).ly.transform('mean'))[0,1]:.3f}")
# well above a crude detection floor: floor = 10th percentile of all transit planet radii in the star's radius band (same route), scaled
single = t[(t.pl_rade < 6) & (t.st_rad > 0) & (t.route == "Kepler/K2")].copy()
edges = np.quantile(single.st_rad, np.linspace(0, 1, 11)); edges[0] = 0; edges[-1] = 1e9
single["b"] = np.digitize(single.st_rad, edges[1:-1]); floor = single.groupby("b").pl_rade.quantile(0.10)
kq["floor"] = floor.reindex(np.digitize(kq.srad, edges[1:-1])).values
for k in (1.0, 1.5, 2.0):
    d = kq[(kq.r_in > k * kq.floor) & (kq.r_out > k * kq.floor)]
    P(f"   Kepler/K2 both<6 and both > {k} x (10th-percentile size for that stellar-radius band): n={len(d)} r={corr(d):.3f} outer larger {outl(d):.3f}")
# range-restriction comparison: same cut applied to shuffled pairs gives ~0 so nothing to show; show instead cut on absolute size
for lo in (1.5, 2.0, 2.5):
    d = kq[(kq.r_in >= lo) & (kq.r_out >= lo)]
    P(f"   Kepler/K2 both in [{lo},6) Re: n={len(d)} r={corr(d):.3f} outer larger {outl(d):.3f}")
# outer-larger: is it a within-system fact or the catalogue-wide size-period slope?
rng = np.random.default_rng(2)
def shuffled_outer(d, nrep=400, bands=None):
    out = []
    for _ in range(nrep):
        if bands is None:
            y = rng.permutation(d.r_out.values)
        else:
            y = d.r_out.values.copy()
            for b in np.unique(bands):
                m = bands == b; y[m] = rng.permutation(y[m])
        out.append((y > d.r_in.values).mean())
    return float(np.mean(out)), float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))
P("   outer larger, real:", round(outl(q), 3), "; outer planets shuffled between systems (keeps 'inner' and 'outer' roles): mean %.3f (%.3f-%.3f)" % shuffled_outer(q))
qb = q[q.srad > 0].copy(); bands = pd.qcut(qb.srad, 10, labels=False).values
P("   same, shuffled only within 10 bands of stellar radius: real %.3f; shuffled mean %.3f (%.3f-%.3f)" % ((outl(qb),) + shuffled_outer(qb, bands=bands)))
P("   median size of inner members %.2f, outer members %.2f; median period inner %.1f outer %.1f" % (q.r_in.median(), q.r_out.median(), q.p_in.median(), q.p_out.median()))
P("   catalogue-wide (all transit planets <6 Re): Spearman(size, period) = %.3f; singles only (sy_pnum=1): %.3f" % (
    stats.spearmanr(t[t.pl_rade < 6].pl_rade, t[t.pl_rade < 6].pl_orbper)[0],
    stats.spearmanr(t[(t.pl_rade < 6) & (t.sy_pnum == 1)].pl_rade, t[(t.pl_rade < 6) & (t.sy_pnum == 1)].pl_orbper)[0]))
# random cross-system pairs matched on period: take the outer planet of another system with the nearest outer period
P("   outer larger by period ratio of the pair:", {f"{a}-{b}": (round(outl(q[(q.ratio >= a) & (q.ratio < b)]), 3), len(q[(q.ratio >= a) & (q.ratio < b)])) for a, b in ((1, 1.5), (1.5, 2), (2, 3), (3, 1e9))})
P("   outer larger with size difference beyond 1 sigma of quoted errors unavailable for all; with |log ratio|>0.1 only: %.3f (n=%d)" % (outl(q[np.abs(q.ly - q.lx) > 0.1]), int((np.abs(q.ly - q.lx) > 0.1).sum())))
P("   same discovery year for both members: %.3f of pairs; r among same-year pairs %.3f, different-year %.3f" % ((q.y_in == q.y_out).mean(), corr(q[q.y_in == q.y_out]), corr(q[q.y_in != q.y_out])))

P("\n==== G. SIZE GAP")
s100 = t[(t.pl_orbper < 100) & t.pl_rade.notna()]
R = s100.pl_rade.values
P("   local-minimum scan: for n bins from 1 to 4 Re (log), which interior bins are lower than both neighbours:")
for nb in (6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 24):
    e = np.logspace(0, np.log10(4), nb + 1); h, _ = np.histogram(R, e)
    mins = [(round(float(e[i]), 2), round(float(e[i + 1]), 2), int(h[i]), int(h[i - 1]), int(h[i + 1])) for i in range(1, nb - 1) if h[i] < h[i - 1] and h[i] < h[i + 1]]
    P(f"     {nb} bins: {mins}")
P("   12 bins with shifted edges (shift in fraction of a bin): bin containing 1.89 vs neighbours, and the sealed-style three-bin test with shifted edges")
w = np.log10(4) / 12
for sh in (0, 0.25, 0.5, 0.75):
    e = 10 ** (np.arange(-2, 16) * w + sh * w); h, _ = np.histogram(R, e)
    i = np.searchsorted(e, 1.89) - 1
    P(f"     shift {sh}: bin {e[i]:.2f}-{e[i+1]:.2f}: {h[i]}; left {h[i-1]}, right {h[i+1]}; local min: {h[i] < h[i-1] and h[i] < h[i+1]}")
P("   three bins of width 0.1 dex, sliding the centre bin's lower edge: counts (left, middle, right), middle lowest?")
for lo in (1.4, 1.5, 1.58, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9):
    e = lo * 10 ** (np.array([-0.1, 0, 0.1, 0.2])); h, _ = np.histogram(R, e)
    P(f"     middle {lo:.2f}-{e[2]:.2f}: {h.tolist()} {'YES' if h[1] < h[0] and h[1] < h[2] else 'no'}")
P("   heaping near the dip: counts of pl_rade values rounded to 0.01 between 1.7 and 2.1 (top):", pd.Series(R[(R >= 1.7) & (R < 2.1)]).round(2).value_counts().head(8).to_dict())
h01, e01 = np.histogram(R, np.arange(1.0, 3.01, 0.1)); P("   linear 0.1-Re bins 1.0-3.0:", h01.tolist())
for r in ("Kepler/K2", "TESS", "other"):
    e = np.logspace(0, np.log10(4), 13); h, _ = np.histogram(s100[s100.route == r].pl_rade, e); P(f"   12 bins, {r}: {h.tolist()}")
relerr = ((s100.pl_radeerr1 - s100.pl_radeerr2) / 2 / s100.pl_rade)
P("   three sealed bins by precision cut (cut chosen afterwards by Noon at 8%):")
for cut in (0.03, 0.05, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.30, 9):
    d = s100[relerr < cut].pl_rade; c = [int(((d >= a) & (d < b)).sum()) for a, b in ((1.26, 1.58), (1.58, 2.0), (2.0, 2.51))]
    z = (c[0] - c[1]) / np.sqrt(c[0] + c[1]) if c[0] + c[1] else float("nan")
    P(f"     relerr<{cut}: n={len(d)} bins {c} middle lowest {c[1] < c[0] and c[1] < c[2]}; (left-middle)/sqrt(sum) = {z:+.2f}")
# significance of the 12-bin dip against its two neighbours
P("   12-bin dip: 260 against neighbours 301 and 347: z vs mean of neighbours = %.2f" % ((324 - 260) / np.sqrt(260 + (301 + 347) / 4)))

P("\n==== H. BRIER / LEDGER")
L = pd.read_csv(sys.argv[2])
L["bm"] = (L.my_odds - L.outcome) ** 2; L["bf"] = (L.forecasters_median - L.outcome) ** 2
P("   ledger rows", len(L), "; by study:", L.groupby("study").agg(n=("bm", "size"), mine=("bm", "mean"), theirs=("bf", "mean"), held=("outcome", "mean")).round(4).to_dict("index"))
P(f"   all: mine {L.bm.mean():.4f} theirs {L.bf.mean():.4f} diff {L.bm.mean()-L.bf.mean():+.4f}")
d = (L.bm - L.bf).values; rng = np.random.default_rng(0)
bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
P(f"   bootstrap over the 34 expectations: {np.percentile(bs,2.5):+.3f} to {np.percentile(bs,97.5):+.3f}; paired t: t={d.mean()/(d.std(ddof=1)/np.sqrt(len(d))):.2f}")
X = L[L.study == "transits"].copy(); dx = (X.bm - X.bf).values
P("   transits per-item mine-theirs:", dict(zip(X.label, np.round(dx, 3))))
P(f"   transits: diff {dx.mean():+.4f}; paired t = {dx.mean()/(dx.std(ddof=1)/np.sqrt(len(dx))):.2f}; without X10: mine {X[X.label!='X10'].bm.mean():.4f} theirs {X[X.label!='X10'].bf.mean():.4f}")
X2 = X.copy(); X2.loc[X2.label == "X10", "outcome"] = 0
P(f"   transits if X10 scored failed (zeros not counted as stated values): mine {((X2.my_odds-X2.outcome)**2).mean():.4f} theirs {((X2.forecasters_median-X2.outcome)**2).mean():.4f}")
L2 = L.copy(); L2.loc[(L2.study == "transits") & (L2.label == "X10"), "outcome"] = 0
P(f"   all 34 if X10 scored failed: mine {((L2.my_odds-L2.outcome)**2).mean():.4f} theirs {((L2.forecasters_median-L2.outcome)**2).mean():.4f}")
P(f"   mean odds mine {L.my_odds.mean():.3f}, theirs {L.forecasters_median.mean():.3f}, held {L.outcome.mean():.3f}; base-rate constant Brier {(L.outcome.mean()*(1-L.outcome.mean())):.4f}")
