"""Blind recomputation of X1..X12 from expectations.md. Referee's own code.
Usage: python -I blind.py /path/to/pscomppars.csv
"""
import sys
import numpy as np
import pandas as pd

path = sys.argv[1]
df = pd.read_csv(path)
out = []
def P(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)

P("rows total", len(df), "unique pl_name", df.pl_name.nunique())
P("discoverymethod counts:", df.discoverymethod.value_counts().to_dict())
t = df[df.discoverymethod == "Transit"].copy()
P("transit rows", len(t), " controversial among them", int(t.pl_controv_flag.sum()))
P("missing: rade", int(t.pl_rade.isna().sum()), "per", int(t.pl_orbper.isna().sum()),
  "met", int(t.st_met.isna().sum()), "teff", int(t.st_teff.isna().sum()),
  "ecc", int(t.pl_orbeccen.isna().sum()))

def verdict(name, held, *vals):
    P(f"{name}: {'HELD' if held else 'FAILED'} |", *vals)

# X1
s = t[(t.pl_orbper < 100) & t.pl_rade.notna()]
edges = [1.26, 1.58, 2.00, 2.51]
c = [int(((s.pl_rade >= edges[i]) & (s.pl_rade < edges[i+1])).sum()) for i in range(3)]
verdict("X1", c[1] < c[0] and c[1] < c[2], "counts 1.26-1.58, 1.58-2.00, 2.00-2.51 =", c)

# X2
hj = t[(t.pl_rade >= 8) & (t.pl_orbper < 10)]
small = t[(t.pl_rade < 4)]
m_hj = hj.st_met.dropna(); m_sm = small.st_met.dropna()
d = m_hj.mean() - m_sm.mean()
verdict("X2", d >= 0.08, f"mean met HJ {m_hj.mean():.4f} (n={len(m_hj)}), small {m_sm.mean():.4f} (n={len(m_sm)}), diff {d:.4f}")
# per-star variant (not sealed), for information
hs = hj.dropna(subset=['st_met']).drop_duplicates('hostname').st_met
ss = small.dropna(subset=['st_met']).drop_duplicates('hostname').st_met
P(f"   [per-star variant] HJ {hs.mean():.4f} (n={len(hs)}), small {ss.mean():.4f} (n={len(ss)}), diff {hs.mean()-ss.mean():.4f}")

# X3
s = t[(t.pl_orbper < 3) & t.pl_rade.notna()]
n = len(s); k = int(((s.pl_rade >= 3) & (s.pl_rade < 8)).sum())
verdict("X3", k / n < 0.08, f"{k}/{n} = {k/n:.4f}")

# X4
mp = t.pl_orbper.median()
verdict("X4", 5 < mp < 15, f"median period {mp:.4f} d (n={int(t.pl_orbper.notna().sum())})")

# pairs
pairs = []
for h, g in t[t.pl_orbper.notna()].groupby("hostname"):
    if len(g) < 2:
        continue
    g = g.sort_values("pl_orbper")
    r = g.pl_rade.values; p = g.pl_orbper.values; nm = g.pl_name.values
    for i in range(len(g) - 1):
        pairs.append((h, nm[i], nm[i+1], p[i], p[i+1], r[i], r[i+1], len(g)))
pr = pd.DataFrame(pairs, columns=["host", "in_name", "out_name", "p_in", "p_out", "r_in", "r_out", "nsys"])
pr["ratio"] = pr.p_out / pr.p_in
P("adjacent pairs", len(pr), " systems", pr.host.nunique(), " pairs with both radii", int((pr.r_in.notna() & pr.r_out.notna()).sum()))

# X5
q = pr.dropna(subset=["r_in", "r_out"])
rho = np.corrcoef(np.log10(q.r_in), np.log10(q.r_out))[0, 1]
from scipy.stats import spearmanr
verdict("X5", rho >= 0.4, f"Pearson r of log sizes {rho:.4f} (n={len(q)}), Spearman {spearmanr(q.r_in, q.r_out)[0]:.4f}")

# X6
gt = int((q.r_out > q.r_in).sum()); eq = int((q.r_out == q.r_in).sum())
verdict("X6", gt / len(q) >= 0.55, f"outer larger {gt}/{len(q)} = {gt/len(q):.4f}; ties {eq}; excluding ties {gt/(len(q)-eq):.4f}")

# X7
a = int(((pr.ratio >= 1.50) & (pr.ratio < 1.53)).sum()); b = int(((pr.ratio >= 1.47) & (pr.ratio < 1.50)).sum())
verdict("X7", a > 1.5 * b, f"1.50-1.53: {a}, 1.47-1.50: {b}, ratio {a/b if b else float('inf'):.3f}")
# X8
a = int(((pr.ratio >= 2.00) & (pr.ratio < 2.04)).sum()); b = int(((pr.ratio >= 1.96) & (pr.ratio < 2.00)).sum())
verdict("X8", a > 1.3 * b, f"2.00-2.04: {a}, 1.96-2.00: {b}, ratio {a/b if b else float('inf'):.3f}")

# X9
hj = t[(t.pl_rade >= 8) & (t.pl_orbper < 10)]
k = int((hj.sy_pnum == 1).sum())
verdict("X9", k / len(hj) >= 0.90, f"{k}/{len(hj)} = {k/len(hj):.4f}")

# X10
g = t[(t.pl_rade >= 8) & t.pl_orbeccen.notna() & t.pl_orbper.notna()]
sh = g[g.pl_orbper < 5].pl_orbeccen; lo = g[g.pl_orbper > 20].pl_orbeccen
verdict("X10", sh.median() < 0.05 and lo.median() > 0.10,
        f"median e P<5: {sh.median():.4f} (n={len(sh)}, zeros {int((sh==0).sum())}); P>20: {lo.median():.4f} (n={len(lo)}, zeros {int((lo==0).sum())})")
# variant: nonzero only
sh2 = sh[sh > 0]; lo2 = lo[lo > 0]
P(f"   [nonzero-only variant] P<5: {sh2.median():.4f} (n={len(sh2)}); P>20: {lo2.median():.4f} (n={len(lo2)})")

# X11
s = t[t.pl_rade.notna() & t.st_teff.notna()]
hot = s[s.st_teff >= 5000]; cool = s[s.st_teff < 3900]
fh = (hot.pl_rade >= 8).mean(); fc = (cool.pl_rade >= 8).mean()
verdict("X11", fh >= 3 * fc, f"hot {int((hot.pl_rade>=8).sum())}/{len(hot)} = {fh:.4f}; cool {int((cool.pl_rade>=8).sum())}/{len(cool)} = {fc:.4f}; ratio {fh/fc:.3f}")

# X12
s = t[t.pl_rade.notna()]
new = s[s.disc_year >= 2019].pl_rade; old = s[(s.disc_year >= 2014) & (s.disc_year <= 2016)].pl_rade
verdict("X12", new.median() > old.median(), f"median size 2019+: {new.median():.4f} (n={len(new)}); 2014-2016: {old.median():.4f} (n={len(old)})")

open(sys.argv[2], "w").write("\n".join(out) + "\n")
