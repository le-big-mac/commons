"""Referee controls, second pass. Usage: python -I controls2.py pscomppars.csv ledger.csv"""
import sys
import numpy as np
import pandas as pd
from scipy import stats
df = pd.read_csv(sys.argv[1]); t = df[df.discoverymethod == "Transit"].copy(); P = print
TESS = "Transiting Exoplanet Survey Satellite (TESS)"
t["route"] = t.disc_facility.map(lambda f: "Kepler/K2" if f in ("Kepler", "K2") else ("TESS" if f == TESS else "other"))

P("== size gap: the heap at exactly 2.00 and Noon's 12 bins")
s = t[(t.pl_orbper < 100) & t.pl_rade.notna()]; R = s.pl_rade.values
fine = np.round(np.logspace(0, np.log10(4), 13), 3)
h = [int(((R >= fine[i]) & (R < fine[i + 1])).sum()) for i in range(12)]
P("   Noon's edges:", fine.tolist()); P("   counts:", h)
n2 = int((R == 2.0).sum()); P("   planets with pl_rade exactly 2.0 (P<100):", n2, "; in [1.995,2.005):", int(((R >= 1.995) & (R < 2.005)).sum()))
h2 = [int(((R > fine[i]) & (R <= fine[i + 1])).sum()) for i in range(12)]
P("   same bins but upper edge included, lower excluded:", h2)
d, l, r = h2[5], h2[4], h2[6]
P(f"   dip then {d} vs {l} and {r}: z vs mean of neighbours = {((l+r)/2-d)/np.sqrt(d+(l+r)/4):.2f}")
P("   sealed three bins with upper edge included instead:", [int(((R > a) & (R <= b)).sum()) for a, b in ((1.26, 1.58), (1.58, 2.0), (2.0, 2.51))])
lin = np.histogram(R, np.arange(1.0, 3.01, 0.1))[0]
flank = np.r_[lin[1:7], lin[12:15]]; trough = lin[7:12]
P(f"   linear 0.1 bins: trough 1.7-2.2 mean {trough.mean():.1f}/bin; flanks 1.1-1.7 mean {lin[1:7].mean():.1f}, 2.2-2.5 mean {lin[12:15].mean():.1f}; "
  f"z = {(flank.mean()-trough.mean())/np.sqrt(trough.sum()/25 + flank.sum()/81):.2f}; depth {1-trough.mean()/flank.mean():.2f}")
dec = s.pl_rade.map(lambda v: len(f"{v:.8f}".rstrip("0").split(".")[1]) if "." in f"{v:.8f}".rstrip("0") else 0)
for lab, m in (("<=3 decimals (as quoted)", dec <= 3), (">=5 decimals (converted or computed)", dec >= 5), ("no error bars", s.pl_radeerr1.isna())):
    x = s[m].pl_rade.values
    P(f"   {lab}: n={m.sum()} 12 bins {[int(((x >= fine[i]) & (x < fine[i+1])).sum()) for i in range(12)]}; sealed 3 bins {[int(((x >= a) & (x < b)).sum()) for a, b in ((1.26, 1.58), (1.58, 2.0), (2.0, 2.51))]}")
P("   >=5-decimal radii by route:", s[dec >= 5].route.value_counts().to_dict(), "; by disc_year:", s[dec >= 5].disc_year.value_counts().sort_index().to_dict())

P("== X10: what the eccentricity values are")
g = t[(t.pl_rade >= 8) & t.pl_orbeccen.notna()]
P("   zeros x limit flag among giants:"); P(pd.crosstab(g.pl_orbeccen == 0, g.pl_orbeccenlim).to_string())
lo = g[g.pl_orbper > 20].pl_orbeccen.values; sh = g[g.pl_orbper < 5].pl_orbeccen.values
rng = np.random.default_rng(3)
bl = [np.median(rng.choice(lo, len(lo))) for _ in range(5000)]
P(f"   P>20 median {np.median(lo):.3f}; bootstrap 2.5-97.5%: {np.percentile(bl,2.5):.3f}-{np.percentile(bl,97.5):.3f}; share of resamples >0.10: {np.mean(np.array(bl)>0.10):.3f}")
shm = g[(g.pl_orbper < 5) & (g.pl_orbeccen > 0) & (g.pl_orbeccenlim == 0)].pl_orbeccen.values
bs = [np.median(rng.choice(shm, len(shm))) for _ in range(5000)]
P(f"   P<5 measured (nonzero, not a limit) n={len(shm)} median {np.median(shm):.3f}; bootstrap {np.percentile(bs,2.5):.3f}-{np.percentile(bs,97.5):.3f}; share <0.05: {np.mean(np.array(bs)<0.05):.3f}")
shn = g[(g.pl_orbper < 5) & (g.pl_orbeccen > 0)].pl_orbeccen.values
P(f"   P<5 nonzero incl. limits n={len(shn)} median {np.median(shn):.3f}; P<5 limits only median {np.median(g[(g.pl_orbper<5)&(g.pl_orbeccenlim==1)].pl_orbeccen):.3f}")
lom = g[(g.pl_orbper > 20) & (g.pl_orbeccen > 0) & (g.pl_orbeccenlim == 0)].pl_orbeccen
P(f"   P>20 measured n={len(lom)} median {lom.median():.3f}")
P("   all transit planets: share of stated eccentricities that are exactly 0: %.3f; under 4 Re: %.3f" % ((t.pl_orbeccen.dropna() == 0).mean(), (t[t.pl_rade < 4].pl_orbeccen.dropna() == 0).mean()))

P("== resonances: expected from flanks, and by era")
tp = t[t.pl_orbper.notna()]; rows = []
for hname, gg in tp.groupby("hostname"):
    if len(gg) < 2: continue
    gg = gg.sort_values("pl_orbper")
    for i in range(len(gg) - 1):
        rows.append((gg.pl_orbper.values[i + 1] / gg.pl_orbper.values[i], max(gg.disc_year.values[i], gg.disc_year.values[i + 1]), gg.route.values[i]))
pr = pd.DataFrame(rows, columns=["ratio", "year", "route"])
c = lambda a, b, d=pr: int(((d.ratio >= a) & (d.ratio < b)).sum())
f32 = (c(1.30, 1.47) + c(1.56, 1.70)) / (0.17 + 0.14) * 0.03
f21 = (c(1.80, 1.96) + c(2.08, 2.20)) / (0.16 + 0.12) * 0.04
P(f"   3:2: expected per 0.03 window from flanks (1.30-1.47, 1.56-1.70): {f32:.1f}; observed inside 14 (Poisson P<=14: {stats.poisson.cdf(14, f32):.3f}), outside 60 (P>=60: {stats.poisson.sf(59, f32):.2g})")
P(f"   2:1: expected per 0.04 window from flanks (1.80-1.96, 2.08-2.20): {f21:.1f}; observed inside 6 (Poisson P<=6: {stats.poisson.cdf(6, f21):.2g}), outside 35 (P>=35: {stats.poisson.sf(34, f21):.3f})")
for lab, d in (("pair complete by 2013", pr[pr.year <= 2013]), ("2014-2016", pr[(pr.year >= 2014) & (pr.year <= 2016)]), ("2017 or later", pr[pr.year >= 2017])):
    P(f"   {lab}: pairs {len(d)}; 3:2 in/out {c(1.47,1.50,d)}/{c(1.50,1.53,d)}; 2:1 in/out {c(1.96,2.00,d)}/{c(2.00,2.04,d)}; share of pairs within 0.05 of 1.5 or 2.0: {(c(1.45,1.55,d)+c(1.95,2.05,d))/len(d):.3f}")

P("== metallicity: giants further out")
small = t[t.pl_rade < 4].st_met.dropna()
for lab, m in (("hot Jupiters R>=8 P<10", (t.pl_rade >= 8) & (t.pl_orbper < 10)), ("giants R>=8 P>=10", (t.pl_rade >= 8) & (t.pl_orbper >= 10)), ("R 4-8", (t.pl_rade >= 4) & (t.pl_rade < 8))):
    a = t[m].st_met.dropna(); P(f"   {lab}: mean {a.mean():+.3f} n={len(a)} diff over small {a.mean()-small.mean():+.3f} se {np.sqrt(a.var(ddof=1)/len(a)+small.var(ddof=1)/len(small)):.3f}")
hjK = t[(t.pl_rade >= 8) & (t.pl_orbper < 10) & (t.route == "Kepler/K2")].st_met.dropna(); sK = t[(t.pl_rade < 4) & (t.route == "Kepler/K2")].st_met.dropna()
se = np.sqrt(hjK.var(ddof=1) / len(hjK) + sK.var(ddof=1) / len(sK)); P(f"   Kepler/K2 only: {hjK.mean()-sK.mean():+.3f}, 95% interval {hjK.mean()-sK.mean()-1.96*se:+.3f} to {hjK.mean()-sK.mean()+1.96*se:+.3f}")

P("== X12: who found the planets of 2019 or later")
n = t[(t.disc_year >= 2019) & t.pl_rade.notna()]; o = t[(t.disc_year >= 2014) & (t.disc_year <= 2016) & t.pl_rade.notna()]
P("   2019+:", n.groupby("route").pl_rade.agg(["count", "median"]).round(2).to_dict("index")); P("   2014-16:", o.groupby("route").pl_rade.agg(["count", "median"]).round(2).to_dict("index"))

P("== hot Neptunes: X3 within each route, Wilson intervals")
def wil(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n; cc = (p + z * z / (2 * n)) / den; hh = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den; return cc - hh, cc + hh
for r in ("Kepler/K2", "TESS", "other"):
    d = t[(t.route == r) & (t.pl_orbper < 3) & t.pl_rade.notna()]; k = int(((d.pl_rade >= 3) & (d.pl_rade < 8)).sum()); a, b = wil(k, len(d))
    P(f"   {r}: {k}/{len(d)} = {k/len(d):.3f} ({a:.3f}-{b:.3f})")

P("== figure panel a: planets outside the drawn frame (x 0.3-1000 d, y 0.4-30 Re):", int(((t.pl_orbper < 0.3) | (t.pl_orbper > 1000) | (t.pl_rade < 0.4) | (t.pl_rade > 30)).sum()))

P("== ledger precise")
L = pd.read_csv(sys.argv[2]); bm = (L.my_odds - L.outcome) ** 2; bf = (L.forecasters_median - L.outcome) ** 2
P(f"   34: mine {bm.mean():.5f} theirs {bf.mean():.5f}; first two studies only (22): mine {bm[L.study!='transits'].mean():.4f} theirs {bf[L.study!='transits'].mean():.4f}")
P("   items where forecasters' median beat me:", int((bf < bm).sum()), "of", len(L), "; sign test p =", round(stats.binomtest(int((bf < bm).sum()), int((bf != bm).sum()), 0.5).pvalue, 3))
X = L[L.study == "transits"]; P("   transits: items where forecasters beat me:", int(((X.forecasters_median - X.outcome) ** 2 < (X.my_odds - X.outcome) ** 2).sum()), "of 12")
