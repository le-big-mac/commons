"""Referee extra checks. usage: python -I extra.py DATADIR"""
import sys
sys.path.insert(0, '/home/agent2/battles/referee')
import numpy as np, pandas as pd
from load import load
from blind import auc
D = sys.argv[1]
df = load(D); dec = df[df.dec]
t = pd.read_csv(f"{D}/battle_durations.csv").set_index("isqno")
t["span"] = (pd.to_datetime(t.datetime_max, errors="coerce") - pd.to_datetime(t.datetime_min, errors="coerce")).dt.total_seconds() / 86400
t["year"] = df.year.reindex(t.index)
t["midnight"] = t.datetime_min.str.endswith("T00:00:00") & t.datetime_max.str.endswith("T00:00:00")
print("a. duration1 vs span = datetime_max - datetime_min (days)")
print("   span unparsable:", int(t.span.isna().sum()))
for nm, m in (("before 1850", t.year < 1850), ("after 1900", t.year > 1900)):
    s = t[m]
    print(f"   {nm}: median duration1 {s.duration1.median():.3f}; median span {s.span.median():.3f}; median duration2 {s.duration2.median():.3f}; both ends at midnight {100*s.midnight.mean():.0f}%; span<=1 day {100*(s.span<=1).mean():.0f}%; span>=2 days {100*(s.span>=2).mean():.0f}%")
print("   duration1 minus span, value counts:", (t.duration1 - t.span).round(3).value_counts().head(6).to_dict())
print("   among duration1==2: span value counts", t[t.duration1 == 2].span.round(3).value_counts().head(5).to_dict(), "; midnight both ends:", int(t[t.duration1 == 2].midnight.sum()), "of", int((t.duration1 == 2).sum()))
print("   among duration1==1: span value counts", t[t.duration1 == 1].span.round(3).value_counts().head(5).to_dict(), "; n", int((t.duration1 == 1).sum()))
print("   sample rows:"); print(t[t.year > 1900].head(6)[["datetime_min", "datetime_max", "duration1", "duration2", "span"]].to_string())
print("   days counted as calendar dates touched (date_max - date_min + 1) when max ends at midnight counted as previous day:")
dmin = pd.to_datetime(t.datetime_min.str.slice(0, 10), errors="coerce"); dmaxdt = pd.to_datetime(t.datetime_max, errors="coerce")
dmax_adj = (dmaxdt - pd.Timedelta(seconds=1)).dt.normalize()
t["dates"] = (dmax_adj - dmin).dt.days + 1
for nm, m in (("before 1850", t.year < 1850), ("after 1900", t.year > 1900)):
    print(f"      {nm}: median calendar dates touched {t[m].dates.median()}; share ==1: {100*(t[m].dates==1).mean():.0f}%; >=2: {100*(t[m].dates>=2).mean():.0f}%")

def bigger(s):
    u = s[s.fr.notna() & (s.fr != 1)]
    return int((((u.fr > 1) & (u.aw == 1)) | ((u.fr < 1) & (u.aw == 0))).sum()), len(u)
ww = dec.war.str.contains("WORLD WAR")
f = dec[dec.fr.notna()]
print("b. bigger side won: world-war rows", bigger(dec[ww]), "; all other rows", bigger(dec[~ww]), "; AUC other rows", round(auc(f[~ww & (f.aw == 1)].fr, f[~ww & (f.aw == 0)].fr), 3), "; AUC world-war rows", round(auc(f[ww & (f.aw == 1)].fr, f[ww & (f.aw == 0)].fr), 3))
print("   bands, other rows vs world-war rows (attacker won k/n):")
for lo, hi in ((0, .5), (.5, .75), (.75, 1), (1, 1.5), (1.5, 2), (2, 3), (3, 1e9)):
    a = f[~ww & (f.fr >= lo) & (f.fr < hi)]; b = f[ww & (f.fr >= lo) & (f.fr < hi)]
    print(f"      {lo}-{hi if hi<1e9 else 'more'}: other {int(a.aw.sum())}/{len(a)}={100*a.aw.mean():.0f}% | world wars {int(b.aw.sum())}/{len(b)}={100*b.aw.mean():.0f}%")
big4 = ["WORLD WAR II (OKINAWA)", "WORLD WAR I (WESTERN FRONT 1918)", "WORLD WAR II (EASTERN FRONT)", "WORLD WAR II (EUROPEAN THEATER)"]
t3 = f[f.fr >= 3]
print("c. >=3: in four labels", [w for w in big4], int(t3[t3.war.isin(big4)].aw.sum()), "/", int(t3.war.isin(big4).sum()), "; elsewhere", int(t3[~t3.war.isin(big4)].aw.sum()), "/", int((~t3.war.isin(big4)).sum()))
print("   exact war labels containing 1918/OKINAWA/EASTERN/EUROPEAN:", sorted(set(w for w in dec.war if any(k in w for k in ("1918", "OKINAWA", "EASTERN FRONT)", "EUROPEAN")))))
print("d. duplicates (parent not empty):")
p = df[df.parent != ""]
print("   wars:", p.war.value_counts().to_dict())
pi = p.parent.astype(float).astype(int)
same = [(df.loc[c, "a_str"] == df.loc[q, "a_str"]) and (df.loc[c, "wina"] == df.loc[q, "wina"]) for c, q in zip(p.index, pi) if q in df.index]
print("   parent in table:", len(same), "; same attacker strength and winner as parent:", int(np.sum(same)))
print(p.head(4)[["name", "war", "parent", "wina", "a_str", "d_str"]].to_string())
print(df.loc[pi.head(4).values, ["name", "war", "wina", "a_str", "d_str"]].to_string())
print("e. cluster (war) bootstrap intervals for the seven bands, vs Wilson")
rng = np.random.default_rng(5); grp = [v for _, v in f.groupby("war")]; edges = [0, .5, .75, 1, 1.5, 2, 3, 1e9]; res = []
for _ in range(2000):
    s = pd.concat([grp[j] for j in rng.integers(0, len(grp), len(grp))]); res.append([s[(s.fr >= lo) & (s.fr < hi)].aw.mean() for lo, hi in zip(edges[:-1], edges[1:])])
res = np.array(res, dtype=float)
print("   ", [f"{100*np.nanpercentile(res[:,i],2.5):.0f}-{100*np.nanpercentile(res[:,i],97.5):.0f}" for i in range(7)])
print("   resamples in which the 3+ band beats the under-1/2 band:", round(np.nanmean(res[:, 6] > res[:, 0]), 3), "; in which under-1 share (W5) < 0.5: see controls")
print("f. era table casualty medians, winner/loser:")
c = dec[dec.a_cs.notna() & dec.d_cs.notna()]
for lo, hi in ((1600, 1799), (1800, 1899), (1900, 1945), (1946, 1982)):
    v = c[(c.year >= lo) & (c.year <= hi)]
    print(f"   {lo}-{hi}: winner {100*np.median(np.where(v.aw==1, v.a_cs, v.d_cs)):.1f}% loser {100*np.median(np.where(v.aw==1, v.d_cs, v.a_cs)):.1f}%")
pr = dec[dec.post1.isin(["PD", "FD"])]; hd = dec[dec.post1 == "HD"]
print("g. median fr prepared", round(pr.fr.median(), 2), "hasty", round(hd.fr.median(), 2), "; share after 1900:", round((pr.year > 1900).mean(), 3), round((hd.year > 1900).mean(), 3))
print("h. W7 with each war once: see controls. W7 on WWI rows alone vs pre-1800:", round(pd.concat([df[df.war.str.contains('WORLD WAR I') & ~df.war.str.contains('WORLD WAR II')].a_cs, df[df.war.str.contains('WORLD WAR I') & ~df.war.str.contains('WORLD WAR II')].d_cs]).median(), 4))
print("i. fewer-men attackers 1800-1945:", int(f[(f.fr < 1) & (f.year >= 1800) & (f.year <= 1945)].aw.sum()), "/", int(((f.fr < 1) & (f.year >= 1800) & (f.year <= 1945)).sum()))
