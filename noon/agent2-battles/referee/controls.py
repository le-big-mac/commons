"""Referee controls, step 2. usage: python -I controls.py DATADIR LEDGER"""
import sys
sys.path.insert(0, '/home/agent2/battles/referee')  # only referee code lives here
import numpy as np
import pandas as pd
from scipy import stats
from load import load
from blind import compute, auc

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200); pd.set_option("display.max_columns", 30)
D = sys.argv[1]
df = load(D)
g = pd.read_csv(f"{D}/belligerents.csv", dtype=str, keep_default_na=False)
g["isqno"] = g["isqno"].astype(int)
df["a_act"] = g[g.attacker == "1"].set_index("isqno")["actors"].reindex(df.index)
df["d_act"] = g[g.attacker == "0"].set_index("isqno")["actors"].reindex(df.index)
df["a_code"] = g[g.attacker == "1"].set_index("isqno")["code"].reindex(df.index)
dec = df[df.dec].copy()
quiet = lambda s: None


def wil(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def sh(s):
    k, n = int(s.aw.sum()), len(s)
    lo, hi = wil(k, n)
    return f"{k}/{n}={100*k/n:.1f}% [{100*lo:.0f},{100*hi:.0f}]" if n else "0/0"


def bigger(s):
    u = s[s.fr.notna() & (s.fr != 1)]
    k = int((((u.fr > 1) & (u.aw == 1)) | ((u.fr < 1) & (u.aw == 0))).sum())
    return k, len(u)


def bg(s):
    k, n = bigger(s); lo, hi = wil(k, n)
    return f"{k}/{n}={100*k/n:.1f}% [{100*lo:.0f},{100*hi:.0f}]" if n else "0/0"


def stats_all(s):
    """pooled statistics on a (resampled) frame of decisive battles"""
    o = {}
    o["att"] = s.aw.mean()
    k, n = bigger(s); o["bigger"] = k / n if n else np.nan
    f = s[s.fr.notna()]
    w, l = f.fr[f.aw == 1], f.fr[f.aw == 0]
    o["auc"] = auc(w, l) if len(w) and len(l) else np.nan
    t = f[f.fr >= 3]; o["ge3"] = t.aw.mean() if len(t) else np.nan
    u = f[f.fr < 3]; o["ge3_minus_lt3"] = o["ge3"] - u.aw.mean() if len(u) and len(t) else np.nan
    t = f[f.fr < 1]; o["lt1"] = t.aw.mean() if len(t) else np.nan
    t = f[f.fr < 0.5]; o["lt0.5"] = t.aw.mean() if len(t) else np.nan
    s1, s0 = s[s.surpa_n > 0], s[s.surpa_n == 0]
    o["surp_gap"] = s1.aw.mean() - s0.aw.mean() if len(s1) and len(s0) else np.nan
    p, h = s[s.post1.isin(["PD", "FD"])], s[s.post1 == "HD"]
    o["hd_minus_prep"] = h.aw.mean() - p.aw.mean() if len(p) and len(h) else np.nan
    c = s[s.a_cs.notna() & s.d_cs.notna()]
    lc = np.where(c.aw == 1, c.d_cs, c.a_cs); wc = np.where(c.aw == 1, c.a_cs, c.d_cs)
    o["loser_more"] = (lc > wc).mean() if len(c) else np.nan
    x = np.log(f.fr.values)
    if len(f) > 5 and x.std() > 0:
        o["lpm_slope_per_doubling"] = np.polyfit(x / np.log(2), f.aw.values, 1)[0]
    else:
        o["lpm_slope_per_doubling"] = np.nan
    return o


def cluster_boot(s, key, B=1500, seed=1):
    rng = np.random.default_rng(seed)
    groups = [grp for _, grp in s.groupby(key)]
    out = []
    for _ in range(B):
        pick = rng.integers(0, len(groups), len(groups))
        out.append(stats_all(pd.concat([groups[j] for j in pick])))
    r = pd.DataFrame(out)
    return r.quantile([0.025, 0.975]).T


def macro(s, key, fn, minn=1):
    vals = []
    for _, grp in s.groupby(key):
        v = fn(grp)
        if v is not None and not np.isnan(v): vals.append(v)
    vals = np.array(vals)
    if len(vals) == 0: return "none"
    # bootstrap over clusters for the macro mean
    rng = np.random.default_rng(2)
    bs = [vals[rng.integers(0, len(vals), len(vals))].mean() for _ in range(4000)]
    return f"{100*vals.mean():.1f}% over {len(vals)} clusters [boot {100*np.percentile(bs,2.5):.0f},{100*np.percentile(bs,97.5):.0f}]"


def f_big(v):
    k, n = bigger(v); return k / n if n else None
def f_att(v): return v.aw.mean()
def f_ge3(v):
    u = v[v.fr >= 3]; return u.aw.mean() if len(u) else None
def f_lt1(v):
    u = v[v.fr < 1]; return u.aw.mean() if len(u) else None
def f_w6(v):
    c = v[v.a_cs.notna() & v.d_cs.notna()]
    if not len(c): return None
    lc = np.where(c.aw == 1, c.d_cs, c.a_cs); wc = np.where(c.aw == 1, c.a_cs, c.d_cs)
    return (lc > wc).mean()


print("=" * 20, "1. DEPENDENCE")
dec["waryear"] = dec.war + "|" + dec.year.astype(int).astype(str)
for key in ["war", "war2", "war3", "war4", "campgn", "waryear"]:
    vc = dec[key].value_counts()
    print(f"{key}: {len(vc)} clusters among decisive; top six hold {vc.head(6).sum()} of {len(dec)}; singletons {int((vc==1).sum())}; top: " + "; ".join(f"{k[:30]} {v}" for k, v in vc.head(6).items()))
print("rows (all 660) with OKINAWA in war:", int(df.war.str.contains("OKINAWA").sum()), " decisive:", int(dec.war.str.contains("OKINAWA").sum()), "; campgn containing OKINAWA:", int(df.campgn.str.contains("OKINAWA").sum()))
print("rows with parent not empty (duplicated battles):", int((df.parent != "").sum()), " decisive:", int((dec.parent != "").sum()))
for key in ["war", "war4", "war3", "waryear", "campgn"]:
    print(f"-- each {key} counted once (macro mean of cluster shares):")
    for nm, fn in (("attacker won", f_att), ("bigger side won", f_big), (">=3:1 won", f_ge3), ("fewer men won", f_lt1), ("loser larger cas share", f_w6)):
        print(f"     {nm}: {macro(dec, key, fn)}")
print("-- bigger side won, macro over wars with at least m unequal decisive battles:")
for m in (1, 2, 3, 5, 10):
    vals = [f_big(v) for _, v in dec.groupby("war") if bigger(v)[1] >= m]
    print(f"     m>={m}: {100*np.mean(vals):.1f}% over {len(vals)} wars")
print("-- pooled stats and cluster-bootstrap 95% intervals")
base = stats_all(dec)
for key in ["war", "war4"]:
    ci = cluster_boot(dec, key)
    print(f"  resampling whole `{key}`:")
    for k in base:
        print(f"     {k:24s} {base[k]:+.3f}   [{ci.loc[k, 0.025]:+.3f}, {ci.loc[k, 0.975]:+.3f}]")
top6 = dec.war.value_counts().head(6).index
print("-- verdicts with six largest `war` dropped (all rows of those wars removed):")
r = compute(df[~df.war.isin(top6)], print)
big3 = df.war4.value_counts().head(3).index
print("-- three largest war4:", list(big3), "; verdicts without them:")
r = compute(df[~df.war4.isin(big3)], print)
print("-- verdicts without duplicated battles (parent not empty):")
r = compute(df[df.parent == ""], quiet)
print("   ", {k: (round(float(np.ravel(v[0])[0]), 3), bool(v[2])) for k, v in r.items()})

print("=" * 20, "2. YEAR SPLIT")
eras = [(1600, 1699), (1700, 1799), (1800, 1815), (1816, 1849), (1850, 1899), (1900, 1913), (1914, 1918), (1919, 1938), (1939, 1945), (1946, 1982),
        (1600, 1799), (1800, 1899), (1900, 1945), (1900, 1949), (1950, 1982), (1914, 1945), (1600, 1913)]
for lo, hi in eras:
    s = dec[(dec.year >= lo) & (dec.year <= hi)]
    f = s[s.fr.notna()]
    print(f"  {lo}-{hi}: n={len(s):3d} attacker {sh(s)}; bigger {bg(s)}; >=3: {sh(f[f.fr>=3])}; <1: {sh(f[f.fr<1])}; median fr {f.fr.median():.2f}")
s = dec[(dec.year >= 1900) & (dec.year <= 1945)]
ww = s.war.str.contains("WORLD WAR")
print("  1900-1945 world-war rows:", bg(s[ww]), "; other wars 1900-1945:", bg(s[~ww]), "| WWI:", bg(s[s.war.str.contains("WORLD WAR I ")| (s.war.str.contains('WORLD WAR I') & ~s.war.str.contains('WORLD WAR II'))]), "| WWII:", bg(s[s.war.str.contains("WORLD WAR II")]))
print("  by war, 1900 on (decisive n, attacker share, bigger-side share, median fr):")
for w, v in dec[dec.year >= 1900].groupby("war"):
    if len(v) >= 5:
        k, n = bigger(v)
        print(f"     {w[:44]:44s} n={len(v):3d} att {100*v.aw.mean():3.0f}%  bigger {k}/{n}={100*k/max(n,1):3.0f}%  med fr {v.fr.median():.2f}")
# who is the bigger side in WWII / WWI?
def side_big(r):
    return r.a_act if r.fr > 1 else (r.d_act if r.fr < 1 else None)
for nm, s in (("WWII", dec[dec.war.str.contains("WORLD WAR II")]), ("WWI", dec[dec.war.str.contains("WORLD WAR I") & ~dec.war.str.contains("WORLD WAR II")])):
    u = s[s.fr.notna() & (s.fr != 1)].copy()
    u["bigact"] = u.apply(side_big, axis=1)
    u["bigwon"] = ((u.fr > 1) & (u.aw == 1)) | ((u.fr < 1) & (u.aw == 0))
    u["winact"] = np.where(u.aw == 1, u.a_act, u.d_act)
    print(f"  {nm}: bigger side by actor (n, share bigger won):")
    print(u.groupby("bigact").bigwon.agg(["size", "mean"]).sort_values("size", ascending=False).head(8).round(2).to_string())
    print(f"  {nm}: winners by actor:"); print(u.winact.value_counts().head(6).to_string())
    print(f"  {nm}: attackers by actor:"); print(u.a_act.value_counts().head(6).to_string())
post = df[df.year >= 1946]; pdec = post[post.dec]
isr_a = pdec.a_act.str.contains("Israel"); isr_d = pdec.d_act.str.contains("Israel")
ai = post.war.str.contains("ARAB|ISRAEL|SIX DAY|SINAI|OCTOBER|LEBANON", regex=True)
print("  post-1945 rows:", len(post), "decisive:", len(pdec), "; wars:"); print(post.war.value_counts().to_string())
print("  rows with Israel on a side (all post-45):", int((post.a_act.str.contains('Israel') | post.d_act.str.contains('Israel')).sum()), "; Israel attacker:", int(post.a_act.str.contains('Israel').sum()))
ii = pdec[isr_a | isr_d]
isr_won = ((ii.a_act.str.contains("Israel")) & (ii.aw == 1)) | ((ii.d_act.str.contains("Israel")) & (ii.aw == 0))
isr_small = ((ii.a_act.str.contains("Israel")) & (ii.fr < 1)) | ((ii.d_act.str.contains("Israel")) & (ii.fr > 1))
print(f"  decisive with Israel: {len(ii)}; Israel won {int(isr_won.sum())}; Israel the smaller side {int(isr_small.sum())}; Israel smaller and won {int((isr_won & isr_small).sum())}; Israel bigger and won {int((isr_won & ~isr_small).sum())} of {int((~isr_small).sum())}")
print("  post-45 decisive without Israel:", bg(pdec[~(isr_a | isr_d)]), "attacker", sh(pdec[~(isr_a | isr_d)]))
# test 69 vs 53, 47 vs 53
def two(k1, n1, k2, n2):
    return stats.fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1]
e = {nm: bigger(dec[(dec.year >= lo) & (dec.year <= hi)]) for nm, lo, hi in (("a", 1600, 1799), ("b", 1800, 1899), ("c", 1900, 1945), ("d", 1946, 1982))}
print("  Fisher p: 1900-45 vs 1600-1899:", round(two(*e["c"], e["a"][0] + e["b"][0], e["a"][1] + e["b"][1]), 4), "; post-45 vs 1600-1899:", round(two(*e["d"], e["a"][0] + e["b"][0], e["a"][1] + e["b"][1]), 3), "; post-45 vs 1900-45:", round(two(*e["d"], *e["c"]), 4))

print("=" * 20, "3. THREE TO ONE")
f = dec[dec.fr.notna()]
inn = (f.year >= 1900) & (f.year <= 1945)
for thr in (2, 3, 4, 5):
    print(f"  >= {thr}: all {sh(f[f.fr>=thr])} | 1900-45 {sh(f[inn&(f.fr>=thr)])} | outside {sh(f[~inn&(f.fr>=thr)])} || below thr: all {sh(f[f.fr<thr])} | 1900-45 {sh(f[inn&(f.fr<thr)])} | outside {sh(f[~inn&(f.fr<thr)])}")
print("  >=3 by era:", "; ".join(f"{lo}-{hi}: {sh(f[(f.year>=lo)&(f.year<=hi)&(f.fr>=3)])}" for lo, hi in ((1600, 1899), (1900, 1913), (1914, 1918), (1919, 1938), (1939, 1945), (1946, 1982))))
print("  >=3 by posture: PD/FD", sh(f[(f.fr >= 3) & f.post1.isin(['PD', 'FD'])]), "| HD", sh(f[(f.fr >= 3) & (f.post1 == 'HD')]), "| <3 vs PD/FD", sh(f[(f.fr < 3) & f.post1.isin(['PD', 'FD'])]))
print("  >=3 by war (n>=3):");
for w, v in f[f.fr >= 3].groupby("war"):
    if len(v) >= 3: print(f"     {w[:44]:44s} {int(v.aw.sum())}/{len(v)}")
print("  draws among >=3:", int(((df.fr >= 3) & (df.wina_n == 0)).sum()), "; among <1:", int(((df.fr < 1) & (df.wina_n == 0)).sum()))
print("  <1 (fewer men) by era and who:", "; ".join(f"{lo}-{hi}: {sh(f[(f.year>=lo)&(f.year<=hi)&(f.fr<1)])}" for lo, hi in ((1600, 1799), (1800, 1899), (1900, 1945), (1946, 1982))))
lt = f[f.fr < 1]
print("  fewer-men attackers without Israel as attacker:", sh(lt[~lt.a_act.str.contains('Israel')]), "| pre-1946:", sh(lt[lt.year < 1946]))

print("=" * 20, "4. PREPARED DEFENCES")
for p in ["PD", "FD", "HD", "DL", "WD", ""]:
    s = dec[dec.post1 == p]; print(f"  post1={p or 'empty'}: {sh(s)}  median fr {s.fr.median():.2f}")
prep = dec.post1.isin(["PD", "FD"]); hd = dec.post1 == "HD"
print("  by war (n>=8 decisive): prepared k/n, hasty k/n")
rows = []
for w, v in dec.groupby("war"):
    a, b = v[v.post1.isin(["PD", "FD"])], v[v.post1 == "HD"]
    rows.append((w, len(a), int(a.aw.sum()), len(b), int(b.aw.sum()), int(v.year.min())))
    if len(v) >= 8: print(f"     {w[:44]:44s} prep {int(a.aw.sum())}/{len(a)}  hasty {int(b.aw.sum())}/{len(b)}")
def mh(s, key):
    num = den = 0.0; nstr = 0; nb = 0
    for _, v in s.groupby(key):
        a, b = v[v.post1.isin(["PD", "FD"])], v[v.post1 == "HD"]
        if len(a) and len(b):
            w = len(a) * len(b) / (len(a) + len(b)); num += w * (b.aw.mean() - a.aw.mean()); den += w; nstr += 1; nb += len(a) + len(b)
    return f"HD minus prepared = {100*num/den:+.1f} points within {nstr} strata holding {nb} battles" if den else "none"
dec["era4"] = pd.cut(dec.year, [0, 1799, 1899, 1945, 2000], labels=["a", "b", "c", "d"]).astype(str)
dec["frb"] = pd.cut(dec.fr, [0, 1, 2, 1e9], right=False, labels=["lt1", "1to2", "ge2"]).astype(str)
dec["erafr"] = dec.era4 + dec.frb
dec["decade"] = (dec.year // 10 * 10).astype(int).astype(str)
for key in ["war", "war4", "campgn", "era4", "erafr", "decade", "waryear"]:
    print(f"  stratified by {key}: {mh(dec, key)}")
print("  by era4: " + "; ".join(f"{lo}-{hi}: prep {sh(dec[prep&(dec.year>=lo)&(dec.year<=hi)])} vs hasty {sh(dec[hd&(dec.year>=lo)&(dec.year<=hi)])}" for lo, hi in ((1600, 1799), (1800, 1899), (1900, 1913), (1914, 1918), (1919, 1938), (1939, 1945), (1946, 1982))))
print("  finer force bands (prep vs hasty):")
for lo, hi in ((0, .5), (.5, .75), (.75, 1), (1, 1.5), (1.5, 2), (2, 3), (3, 1e9)):
    m = (dec.fr >= lo) & (dec.fr < hi); print(f"     {lo}-{hi}: prep {sh(dec[prep&m])} vs hasty {sh(dec[hd&m])}")
print("  from 1900, by force band:");
for lo, hi in ((0, 1), (1, 2), (2, 1e9)):
    m = (dec.fr >= lo) & (dec.fr < hi) & (dec.year >= 1900); m0 = (dec.fr >= lo) & (dec.fr < hi) & (dec.year < 1900)
    print(f"     {lo}-{hi}: 1900 on prep {sh(dec[prep&m])} vs hasty {sh(dec[hd&m])} | before 1900 prep {sh(dec[prep&m0])} vs hasty {sh(dec[hd&m0])}")
gaps = []
for w in dec.war.unique():
    s = dec[dec.war != w]; gaps.append((s[s.post1 == "HD"].aw.mean() - s[s.post1.isin(["PD", "FD"])].aw.mean(), w))
gaps.sort(); print(f"  leave one war out: gap ranges {100*gaps[0][0]:+.1f} (without {gaps[0][1][:30]}) to {100*gaps[-1][0]:+.1f} (without {gaps[-1][1][:30]})")
s = dec[~dec.war.isin(top6)]; print("  without six largest wars: prep", sh(s[s.post1.isin(['PD', 'FD'])]), "hasty", sh(s[s.post1 == 'HD']))
s = dec[~dec.war.str.contains("WORLD WAR")]; print("  without world-war rows: prep", sh(s[s.post1.isin(['PD', 'FD'])]), "hasty", sh(s[s.post1 == 'HD']))
s = dec[dec.war.str.contains("WORLD WAR")]; print("  world-war rows only: prep", sh(s[s.post1.isin(['PD', 'FD'])]), "hasty", sh(s[s.post1 == 'HD']))
# post2 variants
anyprep = dec.post1.isin(["PD", "FD"]) | dec.post2.isin(["PD", "FD"])
purehd = (dec.post1 == "HD") & ~dec.post2.isin(["PD", "FD"])
print("  post2: prepared if post1 or post2 is PD/FD:", sh(dec[anyprep]), "| HD with no PD/FD in post2:", sh(dec[purehd]), "| post1 HD + post2 PD/FD:", sh(dec[(dec.post1 == 'HD') & dec.post2.isin(['PD', 'FD'])]), "| post1 PD/FD, post2 empty:", sh(dec[prep & (dec.post2 == '')]))
print("  prepared incl. DL/WD on hasty side:", sh(dec[dec.post1.isin(['HD', 'DL', 'WD'])]), "| DL/WD or post2 DL/WD:", sh(dec[dec.post1.isin(['DL', 'WD']) | dec.post2.isin(['DL', 'WD'])]))
print("  draws by posture:", df[df.wina_n == 0].post1.value_counts().to_dict(), "; draws-as-half: prep", round((df[df.post1.isin(['PD', 'FD']) & df.wina_n.notna()].wina_n.add(1).div(2)).mean(), 4), "hasty", round((df[(df.post1 == 'HD') & df.wina_n.notna()].wina_n.add(1).div(2)).mean(), 4))
# who attacks prepared after 1900
s = dec[(dec.year >= 1900)]
print("  1900 on, attackers of prepared/fortified by actor:"); print(s[s.post1.isin(["PD", "FD"])].groupby("a_act").aw.agg(["size", "mean"]).sort_values("size", ascending=False).head(8).round(2).to_string())
print("  1900 on, attackers of hasty by actor:"); print(s[s.post1 == "HD"].groupby("a_act").aw.agg(["size", "mean"]).sort_values("size", ascending=False).head(8).round(2).to_string())
print("  stratified by attacker's actor (all years):", mh(dec, "a_act"))

print("=" * 20, "5. DEFINITIONS")
print("  battles in year 1800:", int((df.year == 1800).sum()), " 1850:", int((df.year == 1850).sum()), " 1900:", int((df.year == 1900).sum()))
for nm, kw, d2 in (("intst", {}, load(D, "intst")), ("inclusive cuts (<=1800, >=1900, <=1850)", dict(strict=False), df), ("cuts 1700/1914/1815", dict(cuts=(1700, 1914, 1815)), df), ("cuts 1815/1945/1900", dict(cuts=(1815, 1945, 1900)), df)):
    r = compute(d2, quiet, **kw)
    print(f"  {nm}: " + "; ".join(f"{k} {np.round(np.ravel(v[0]).astype(float),3).tolist()} {'held' if v[2] else 'FAILED'}" for k, v in r.items()))
di = load(D, "intst"); print("  intst: decisive battles with both intst:", int((di.dec & di.fr.notna()).sum()), "; rows where intst ratio and str ratio fall on different sides of 1:", int((((di.fr > 1) & (df.fr < 1)) | ((di.fr < 1) & (df.fr > 1))).sum()))
# draws as half
h = df[df.wina_n.notna()].copy(); h["sc"] = (h.wina_n + 1) / 2
u = h[h.fr.notna() & (h.fr != 1)]; bsc = np.where(u.fr > 1, u.sc, 1 - u.sc).mean()
print(f"  draws as half: W1 {h.sc.mean():.4f}; W2 {bsc:.4f}; W4 {h[h.fr>=3].sc.mean():.4f} (n={int((h.fr>=3).sum())}); W5 {h[h.fr<1].sc.mean():.4f} (n={int((h.fr<1).sum())}); W8 {h[h.surpa_n>0].sc.mean()-h[h.surpa_n==0].sc.mean():+.4f}; W11 HD-prep {h[h.post1=='HD'].sc.mean()-h[h.post1.isin(['PD','FD'])].sc.mean():+.4f}")
# duration2
t = pd.read_csv(f"{D}/battle_durations.csv").set_index("isqno")
df["dur2"] = t.duration2.reindex(df.index)
for col in ("dur", "dur2"):
    e, l = df[df.year < 1850][col].dropna(), df[df.year > 1900][col].dropna()
    print(f"  {col}: median before 1850 {e.median():.3f} (n={len(e)}; share ==1: {100*(e==1).mean():.0f}%, <1: {100*(e<1).mean():.0f}%, >1: {100*(e>1).mean():.0f}%); after 1900 {l.median():.3f} (n={len(l)}; share >=2: {100*(l>=2).mean():.1f}%, <2: {100*(l<2).mean():.1f}%)")
print("  duration1 after 1900 by war group: WW", df[(df.year > 1900) & df.war.str.contains('WORLD WAR')].dur.median(), "non-WW", df[(df.year > 1900) & ~df.war.str.contains('WORLD WAR')].dur.median(), "; 1900-45", df[(df.year > 1900) & (df.year <= 1945)].dur.median(), "; 1946 on", df[df.year >= 1946].dur.median())
print("  duration1 value counts after 1900:", df[df.year > 1900].dur.round(2).value_counts().head(6).to_dict())
# W7 per-battle combined share
c = df[(df.a_s > 0) & (df.d_s > 0) & df.a_cas.notna() & df.d_cas.notna()].copy(); c["comb"] = (c.a_cas + c.d_cas) / (c.a_s + c.d_s)
print(f"  W7 with one combined share per battle: before 1800 {c[c.year<1800].comb.median():.4f}, after 1900 {c[c.year>1900].comb.median():.4f}, ratio {c[c.year>1900].comb.median()/c[c.year<1800].comb.median():.3f}")
# surpaa alternative
df["surpaa_n"] = pd.to_numeric(df.surpaa, errors="coerce")
print("  surpaa crosstab with surpa sign:"); print(pd.crosstab(np.sign(df.surpa_n), df.surpaa_n).to_string())
d8 = df[df.dec]
print("  W8 alt: surpa>0 vs all others (incl. defender surprise):", round(d8[d8.surpa_n > 0].aw.mean() - d8[d8.surpa_n <= 0].aw.mean(), 4), "; W8 by era:", "; ".join(f"{lo}-{hi}: {sh(d8[(d8.surpa_n>0)&(d8.year>=lo)&(d8.year<=hi)])} vs {sh(d8[(d8.surpa_n==0)&(d8.year>=lo)&(d8.year<=hi)])}" for lo, hi in ((1600, 1899), (1900, 1945), (1946, 1982))))
print("  W8 stratified by war (surprise minus none):", end=" ")
num = den = 0; ns = 0
for _, v in d8.groupby("war"):
    a, b = v[v.surpa_n > 0], v[v.surpa_n == 0]
    if len(a) and len(b):
        w = len(a) * len(b) / (len(a) + len(b)); num += w * (a.aw.mean() - b.aw.mean()); den += w; ns += 1
print(f"{100*num/den:+.1f} points within {ns} wars")

print("=" * 20, "6. CASUALTIES")
print("  crit value counts:", df.crit.value_counts().to_dict())
print("  str 'code' (attacker):", df.a_code.value_counts().to_dict())
c = dec[dec.a_cs.notna() & dec.d_cs.notna()].copy()
c["l_cs"] = np.where(c.aw == 1, c.d_cs, c.a_cs); c["w_cs"] = np.where(c.aw == 1, c.a_cs, c.d_cs)
c["l_cas"] = np.where(c.aw == 1, c.d_cas, c.a_cas); c["w_cas"] = np.where(c.aw == 1, c.a_cas, c.d_cas)
c["l_str"] = np.where(c.aw == 1, c.d_s, c.a_s); c["w_str"] = np.where(c.aw == 1, c.a_s, c.d_s)
print(f"  loser larger share: {(c.l_cs>c.w_cs).mean():.4f} n={len(c)}; loser larger ABSOLUTE casualties: {(c.l_cas>c.w_cas).mean():.4f} (ties {(c.l_cas==c.w_cas).sum()}); loser was the smaller side in {(c.l_str<c.w_str).mean():.3f}")
print(f"  loser larger share when loser is smaller side: {(c.l_cs>c.w_cs)[c.l_str<c.w_str].mean():.3f} (n={(c.l_str<c.w_str).sum()}); when loser is bigger side: {(c.l_cs>c.w_cs)[c.l_str>c.w_str].mean():.3f} (n={(c.l_str>c.w_str).sum()})")
print(f"  loser abs larger when loser smaller: {(c.l_cas>c.w_cas)[c.l_str<c.w_str].mean():.3f}; when loser bigger: {(c.l_cas>c.w_cas)[c.l_str>c.w_str].mean():.3f}")
for thr in (0.3, 0.5, 0.9, 1.0):
    print(f"  loser's share >= {thr}: {int((c.l_cs>=thr).sum())} battles; winner's share >= {thr}: {int((c.w_cs>=thr).sum())}")
for thr in (0.2, 0.3, 0.5):
    k = c[(c.l_cs < thr) & (c.w_cs < thr)]; print(f"  W6 with battles where either share >= {thr} removed: {(k.l_cs>k.w_cs).mean():.4f} (n={len(k)})")
print("  W6 by era:", "; ".join(f"{lo}-{hi}: {(v.l_cs>v.w_cs).mean():.3f} (n={len(v)})" for lo, hi in ((1600, 1799), (1800, 1899), (1900, 1945), (1946, 1982)) for v in [c[(c.year >= lo) & (c.year <= hi)]]))
print("  W6 by who won: attacker won:", round((c.l_cs > c.w_cs)[c.aw == 1].mean(), 3), int((c.aw == 1).sum()), "; defender won:", round((c.l_cs > c.w_cs)[c.aw == 0].mean(), 3), int((c.aw == 0).sum()))
print("  defender's share larger than attacker's regardless of winner:", round((c.d_cs > c.a_cs).mean(), 3), "; draws: defender larger", round((df[df.wina_n == 0].d_cs > df[df.wina_n == 0].a_cs).mean(), 3))
print("  median ratio loser share / winner share:", round((c.l_cs / c.w_cs.replace(0, np.nan)).median(), 2))
# W7 like for like
both = pd.concat([df[["year", "war", "dur"]].assign(cs=df.a_cs, s=df.a_s, win=(df.wina_n == 1)), df[["year", "war", "dur"]].assign(cs=df.d_cs, s=df.d_s, win=(df.wina_n == -1))]).dropna(subset=["cs"])
both["era"] = np.where(both.year < 1800, "pre1800", np.where(both.year > 1900, "post1900", "mid"))
print("  W7 by finer era (median share, n sides):", "; ".join(f"{lo}-{hi}: {100*v.cs.median():.1f}% ({len(v)})" for lo, hi in ((1600, 1699), (1700, 1799), (1800, 1849), (1850, 1900), (1901, 1913), (1914, 1918), (1919, 1938), (1939, 1945), (1946, 1982)) for v in [both[(both.year >= lo) & (both.year <= hi)]]))
print("  strength (median men per side): pre-1800", both[both.era == 'pre1800'].s.median(), "post-1900", both[both.era == 'post1900'].s.median())
both["sb"] = pd.cut(both.s, [0, 5000, 15000, 40000, 100000, 1e9], labels=["<5k", "5-15k", "15-40k", "40-100k", ">100k"])
print("  median share by strength band and era (n):")
print(both.groupby(["sb", "era"], observed=True).cs.agg(["median", "size"]).unstack().round(3).to_string())
both["perday"] = both.cs / both.dur.clip(lower=1)
print("  median share per day of duration1 (clipped at 1): pre1800", round(both[both.era == 'pre1800'].perday.median(), 4), "post1900", round(both[both.era == 'post1900'].perday.median(), 4))
print("  winners only: pre1800", round(both[(both.era == 'pre1800') & both.win].cs.median(), 4), "post1900", round(both[(both.era == 'post1900') & both.win].cs.median(), 4), "; losers only: pre1800", round(both[(both.era == 'pre1800') & ~both.win].cs.median(), 4), "post1900", round(both[(both.era == 'post1900') & ~both.win].cs.median(), 4))
wm = both.groupby(["war", "era"]).cs.median().reset_index()
print("  median of war medians: pre1800", round(wm[wm.era == 'pre1800'].cs.median(), 4), f"({(wm.era=='pre1800').sum()} wars)", "post1900", round(wm[wm.era == 'post1900'].cs.median(), 4), f"({(wm.era=='post1900').sum()} wars)")
print("  post-1900 without world wars:", round(both[(both.era == 'post1900') & ~both.war.str.contains('WORLD WAR')].cs.median(), 4), "; world wars only:", round(both[(both.era == 'post1900') & both.war.str.contains('WORLD WAR')].cs.median(), 4))

print("=" * 20, "7. W9 and 'whatever the numbers'")
d9 = df[(df.a_s > 0) & (df.d_s > 0) & (df.a_cas > 0) & (df.d_cas > 0)].copy()
d9["x"] = np.log(d9.a_s / d9.d_s); d9["y"] = np.log(d9.a_cas / d9.d_cas)
print("  W9 r by era:", "; ".join(f"{lo}-{hi}: {np.corrcoef(v.x, v.y)[0,1]:+.3f} (n={len(v)})" for lo, hi in ((1600, 1799), (1800, 1899), (1900, 1945), (1946, 1982)) for v in [d9[(d9.year >= lo) & (d9.year <= hi)]]))
rng = np.random.default_rng(3); grp = [v for _, v in d9.groupby("war")]; bs = []
for _ in range(2000):
    s = pd.concat([grp[j] for j in rng.integers(0, len(grp), len(grp))]); bs.append(np.corrcoef(s.x, s.y)[0, 1])
print(f"  W9 r cluster bootstrap by war: [{np.percentile(bs,2.5):+.3f}, {np.percentile(bs,97.5):+.3f}]; share of resamples <= 0: {np.mean(np.array(bs)<=0):.3f}")
d9["xd"] = d9.x - d9.groupby("war").x.transform("mean"); d9["yd"] = d9.y - d9.groupby("war").y.transform("mean")
print(f"  W9 within-war (demeaned by war) r: {np.corrcoef(d9.xd, d9.yd)[0,1]:+.3f}; slope {np.polyfit(d9.x, d9.y, 1)[0]:+.3f}; correlation of log fr with log ratio of casualty SHARES: {np.corrcoef(d9.x, d9.y - d9.x)[0,1]:+.3f}")
print(f"  W9 decisive only r: {np.corrcoef(d9[d9.dec].x, d9[d9.dec].y)[0,1]:+.3f}")
f = dec[dec.fr.notna()].copy(); f["lx"] = np.log2(f.fr)
sl = np.polyfit(f.lx, f.aw, 1)
print(f"  linear-probability slope: {100*sl[0]:+.1f} points per doubling of force ratio (pooled)")
f["lxd"] = f.lx - f.groupby("war").lx.transform("mean"); f["awd"] = f.aw - f.groupby("war").aw.transform("mean")
m = f.groupby("war").aw.transform("size") > 1
print(f"  within-war slope: {100*np.polyfit(f.lxd[m], f.awd[m], 1)[0]:+.1f} points per doubling ({int(m.sum())} battles in wars with 2+)")
rng = np.random.default_rng(4); grp = [v for _, v in f.groupby("war")]; bs = []; bw = []
for _ in range(2000):
    s = pd.concat([grp[j] for j in rng.integers(0, len(grp), len(grp))]); bs.append(np.polyfit(s.lx, s.aw, 1)[0])
    mm = s.groupby("war").aw.transform("size") > 1
    bw.append(np.polyfit(s.lxd[mm], s.awd[mm], 1)[0])
print(f"  pooled slope cluster CI: [{100*np.percentile(bs,2.5):+.1f}, {100*np.percentile(bs,97.5):+.1f}]; within-war slope cluster CI: [{100*np.percentile(bw,2.5):+.1f}, {100*np.percentile(bw,97.5):+.1f}]")
print("  slope by era:", "; ".join(f"{lo}-{hi}: {100*np.polyfit(v.lx, v.aw, 1)[0]:+.1f}" for lo, hi in ((1600, 1799), (1800, 1899), (1900, 1945), (1946, 1982)) for v in [f[(f.year >= lo) & (f.year <= hi)]]))
print("  attacker share under 0.5 vs 3+: Fisher p", round(two(11, 23, 83, 108), 4), "; under 1 vs 1+:", sh(f[f.fr < 1]), sh(f[f.fr >= 1]), "p", round(two(int(f[f.fr < 1].aw.sum()), int((f.fr < 1).sum()), int(f[f.fr >= 1].aw.sum()), int((f.fr >= 1).sum())), 4))

print("=" * 20, "8. BRIER")
L = pd.read_csv(sys.argv[2])
L["dm"] = (L.my_odds - L.outcome) ** 2; L["df"] = (L.forecasters_median - L.outcome) ** 2
print(L.groupby("study")[["dm", "df"]].mean().round(4).to_string(), "\n  all:", round(L.dm.mean(), 4), round(L.df.mean(), 4), "n", len(L), "held", int(L.outcome.sum()))
b = L[L.study == "battles"].copy(); b["d"] = b.dm - b.df
print("  battles per-item mine-minus-theirs:", dict(zip(b.label, b.d.round(4))))
print(f"  W11 share of net difference: {b[b.label=='W11'].d.iloc[0]/b.d.sum():.3f}; without W11: mine {b[b.label!='W11'].dm.mean():.4f} theirs {b[b.label!='W11'].df.mean():.4f}")
d = (L.dm - L.df).values; rng = np.random.default_rng(0)
bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
print(f"  22-item difference {d.mean():+.4f}, bootstrap [{np.percentile(bs,2.5):+.3f}, {np.percentile(bs,97.5):+.3f}]; items where mine closer: {int((d<0).sum())} of {len(d)}; sign test p {stats.binomtest(int((d<0).sum()), len(d)).pvalue:.3f}")
print(f"  battles: items where mine closer: {int((b.d<0).sum())} of {len(b)}; constant 0.91 Brier {((0.909-b.outcome)**2).mean():.4f}; mine with every odd raised by 0.1: {((np.minimum(b.my_odds+0.1,0.99)-b.outcome)**2).mean():.4f}")
