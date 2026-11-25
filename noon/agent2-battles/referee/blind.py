"""Blind recomputation of W1..W11 and the force-ratio bands. Written before opening Noon's results."""
import sys
import numpy as np
import pandas as pd
from scipy import stats
sys.path.insert(0, '/home/agent2/battles/referee')  # -I drops the script dir; this folder holds only referee code
from load import load


def auc(x1, x0):
    # P(x1 > x0) + 0.5 P(tie)
    x1 = np.asarray(x1); x0 = np.asarray(x0)
    r = stats.rankdata(np.concatenate([x1, x0]))
    u = r[: len(x1)].sum() - len(x1) * (len(x1) + 1) / 2
    return u / (len(x1) * len(x0))


def compute(df, out=print, tag="", cuts=(1800, 1900, 1850), strict=True, posture="post1"):
    res = {}
    dec = df[df.dec]
    # W1
    n = len(dec); k = int(dec.aw.sum())
    res["W1"] = (k / n, n, k / n >= 0.55)
    out(f"W1 attacker wins {k}/{n} = {k/n:.4f}  (draws {int((df.wina_n==0).sum())}, uncoded {int(df.wina_n.isna().sum())})  held={k/n>=0.55}")
    # W2
    d2 = dec[dec.fr.notna() & (dec.fr != 1)]
    big = ((d2.fr > 1) & (d2.aw == 1)) | ((d2.fr < 1) & (d2.aw == 0))
    p = big.mean()
    res["W2"] = (p, len(d2), 0.45 <= p <= 0.62)
    out(f"W2 larger side wins {int(big.sum())}/{len(d2)} = {p:.4f} (equal strengths dropped: {int((dec.fr==1).sum())})  held={0.45<=p<=0.62}")
    # W3
    d3 = dec[dec.fr.notna()]
    a = auc(d3.fr[d3.aw == 1], d3.fr[d3.aw == 0])
    res["W3"] = (a, len(d3), 0.50 <= a <= 0.62)
    out(f"W3 AUC force ratio = {a:.4f} (n={len(d3)}, aw={int(d3.aw.sum())})  held={0.50<=a<=0.62}")
    # W4
    d4 = d3[d3.fr >= 3]
    p = d4.aw.mean() if len(d4) else np.nan
    res["W4"] = (p, len(d4), p >= 0.65)
    out(f"W4 fr>=3: attacker wins {int(d4.aw.sum())}/{len(d4)} = {p:.4f}  held={p>=0.65}")
    # W5
    d5 = d3[d3.fr < 1]
    p = d5.aw.mean()
    res["W5"] = (p, len(d5), p >= 0.5)
    out(f"W5 fr<1: attacker wins {int(d5.aw.sum())}/{len(d5)} = {p:.4f}  held={p>=0.5}")
    # W6
    d6 = dec[dec.a_cs.notna() & dec.d_cs.notna()]
    loser_cs = np.where(d6.aw == 1, d6.d_cs, d6.a_cs)
    winner_cs = np.where(d6.aw == 1, d6.a_cs, d6.d_cs)
    gt = (loser_cs > winner_cs).sum(); eq = (loser_cs == winner_cs).sum()
    p = gt / len(d6)
    res["W6"] = (p, len(d6), p >= 0.75)
    out(f"W6 loser's casualty share larger {gt}/{len(d6)} = {p:.4f} (ties {eq})  held={p>=0.75}")
    # W7
    c1, c2, c3 = cuts
    if strict:
        early = df[df.year < c1]; late = df[df.year > c2]; e50 = df[df.year < c3]
    else:
        early = df[df.year <= c1]; late = df[df.year >= c2]; e50 = df[df.year <= c3]
    es = pd.concat([early.a_cs, early.d_cs]).dropna(); ls = pd.concat([late.a_cs, late.d_cs]).dropna()
    me, ml = es.median(), ls.median()
    res["W7"] = (ml / me, (len(es), len(ls)), ml < me / 2)
    out(f"W7 median casualty share early {me:.4f} (n={len(es)}), late {ml:.4f} (n={len(ls)}), ratio {ml/me:.3f}  held={ml<me/2}")
    # W8
    s1 = dec[dec.surpa_n > 0]; s0 = dec[dec.surpa_n == 0]
    p1, p0 = s1.aw.mean(), s0.aw.mean()
    res["W8"] = (p1 - p0, (len(s1), len(s0)), p1 - p0 >= 0.15)
    out(f"W8 attacker surprise {int(s1.aw.sum())}/{len(s1)} = {p1:.4f}; neither {int(s0.aw.sum())}/{len(s0)} = {p0:.4f}; diff {p1-p0:.4f}; (defender surprise n={int((dec.surpa_n<0).sum())}, surpa missing among decisive {int(dec.surpa_n.isna().sum())})  held={p1-p0>=0.15}")
    # W9
    d9 = df[(df.a_s > 0) & (df.d_s > 0) & (df.a_cas > 0) & (df.d_cas > 0)]
    r, pv = stats.pearsonr(np.log(d9.a_s / d9.d_s), np.log(d9.a_cas / d9.d_cas))
    rs = stats.spearmanr(d9.a_s / d9.d_s, d9.a_cas / d9.d_cas)[0]
    res["W9"] = (r, len(d9), r > 0)
    out(f"W9 pearson r(log fr, log cas ratio) = {r:.4f} (n={len(d9)}, p={pv:.2g}; spearman {rs:.4f})  held={r>0}")
    # W10
    m1 = e50.dur.dropna().median(); m2 = late.dur.dropna().median()
    res["W10"] = ((m1, m2), (e50.dur.notna().sum(), late.dur.notna().sum()), (m1 == 1) and (m2 >= 2))
    out(f"W10 median duration early {m1} (n={e50.dur.notna().sum()}), late {m2} (n={late.dur.notna().sum()})  held={(m1==1) and (m2>=2)}")
    # W11
    pf = dec[dec[posture].isin(["PD", "FD"])]; hd = dec[dec[posture] == "HD"]
    pp, ph = pf.aw.mean(), hd.aw.mean()
    res["W11"] = (ph - pp, (len(pf), len(hd)), ph - pp >= 0.10)
    out(f"W11 vs PD/FD {int(pf.aw.sum())}/{len(pf)} = {pp:.4f}; vs HD {int(hd.aw.sum())}/{len(hd)} = {ph:.4f}; HD minus PD/FD {ph-pp:.4f}  held={ph-pp>=0.10}")
    return res


def bands(df, out=print):
    d3 = df[df.dec & df.fr.notna()]
    edges = [0, 0.5, 0.75, 1, 1.5, 2, 3, np.inf]
    out("force-ratio bands [lo, hi): attacker wins / decisive battles")
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = d3[(d3.fr >= lo) & (d3.fr < hi)]
        out(f"  {lo:>4} to {hi:<4}: {int(s.aw.sum()):>3}/{len(s):<3} = {s.aw.mean():.4f}")


if __name__ == "__main__":
    d = sys.argv[1]
    df = load(d)
    lines = []
    def out(s):
        print(s); lines.append(s)
    out(f"battles {len(df)}; decisive {int(df.dec.sum())}; year range {df.year.min()}-{df.year.max()}; year missing {int(df.year.isna().sum())}")
    compute(df, out)
    bands(df, out)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write("\n".join(lines) + "\n")
