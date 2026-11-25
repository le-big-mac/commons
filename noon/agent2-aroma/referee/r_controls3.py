"""Referee, step 2, small extra controls (no forest).
usage: python -I r_controls3.py tidy.csv properties.csv > controls3.out
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import r_core as C

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
W = C.WORDS


def hdr(s):
    print("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)


def main():
    tidy, propf = sys.argv[1:3]
    raw = C.load_ratings(tidy)
    d = C.fill_words(raw, "zero")
    st, mols = C.structures(propf)
    T = st.join(C.mol_scores(d, "strong"))
    T["name"] = raw.drop_duplicates("cid").set_index("cid")["name"]
    T["dil"] = raw[raw.strong].groupby("cid")["dilution"].first()
    T["share"] = d[d.strong].groupby("cid")["smelled"].mean()

    hdr("1. Self-agreement without an arbitrary 'first' and 'second': double-entry (intraclass) correlation, >=10 pairs")
    rep_cids = sorted(raw.loc[raw.is_rep, "cid"].unique())
    s = d[d.cid.isin(rep_cids) & d.strong]
    lo = s.groupby("cid")["vial"].transform("min")
    rng = np.random.default_rng(0)
    for a_ in C.MAIN:
        A = s[s.vial == lo].set_index(["subject", "cid"])[a_].unstack("cid")
        B = s[s.vial != lo].set_index(["subject", "cid"])[a_].unstack("cid")[A.columns]
        A, B = A.values, B.values
        icc, rnd = [], []
        for i in range(A.shape[0]):
            ok = np.isfinite(A[i]) & np.isfinite(B[i])
            if ok.sum() >= 10:
                x, y = A[i][ok], B[i][ok]
                icc.append(C.pearson(np.r_[x, y], np.r_[y, x]))
        # random assignment of the two vials to the two columns, 200 times: spread of the median
        for _ in range(200):
            flip = rng.random(A.shape[1]) < 0.5
            A2 = np.where(flip, B, A); B2 = np.where(flip, A, B)
            rr = []
            for i in range(A.shape[0]):
                ok = np.isfinite(A2[i]) & np.isfinite(B2[i])
                if ok.sum() >= 10:
                    rr.append(C.pearson(A2[i], B2[i]))
            rnd.append(np.nanmedian(rr))
        # another person, double entry not needed (single vial of i against single vial of j, all four combinations)
        oth = []
        for i in range(A.shape[0]):
            for j in range(A.shape[0]):
                if i != j:
                    for P, Q in ((A, A), (A, B), (B, B)):
                        ok = np.isfinite(P[i]) & np.isfinite(Q[j])
                        if ok.sum() >= 10:
                            oth.append(C.pearson(P[i], Q[j]))
        print(f"{a_:9s} self, double-entry: median {np.nanmedian(icc):.3f} (n={len(icc)}); median under random labelling of the two vials: 2.5%-97.5% {np.quantile(rnd, .025):.3f} to {np.quantile(rnd, .975):.3f} (mean {np.mean(rnd):.3f});"
              f" another person, single vials, all vial combinations: median {np.nanmedian(oth):.3f}")

    hdr("2. Which reading of an untouched slider gives a score the panel reproduces? Two random halves of the panel (100 splits), garlic and fish")
    sm_raw = raw[raw.strong & raw.smelled]
    subs = np.sort(sm_raw.subject.unique())
    rng = np.random.default_rng(1)
    for w in ["GARLIC", "FISH", "SWEET", "DECAYED"]:
        r0, ru, ru5, rs, n_u, n_u5 = [], [], [], [], [], []
        for _ in range(100):
            p = rng.permutation(subs); A = set(p[:27])
            a = sm_raw[sm_raw.subject.isin(A)]; b = sm_raw[~sm_raw.subject.isin(A)]
            za, zb = a.groupby("cid")[w].apply(lambda x: x.fillna(0).mean()), b.groupby("cid")[w].apply(lambda x: x.fillna(0).mean())
            ix = za.index.intersection(zb.index); r0.append(C.pearson(za[ix], zb[ix]))
            ua, ub = a.groupby("cid")[w].agg(["mean", "count"]), b.groupby("cid")[w].agg(["mean", "count"])
            ix = ua.index[ua["count"] >= 1].intersection(ub.index[ub["count"] >= 1]); ru.append(C.pearson(ua.loc[ix, "mean"], ub.loc[ix, "mean"])); n_u.append(len(ix))
            ix = ua.index[ua["count"] >= 3].intersection(ub.index[ub["count"] >= 3]); ru5.append(C.pearson(ua.loc[ix, "mean"], ub.loc[ix, "mean"])); n_u5.append(len(ix))
            sa, sb = a.groupby("cid")[w].apply(lambda x: x.notna().mean()), b.groupby("cid")[w].apply(lambda x: x.notna().mean())
            ix = sa.index.intersection(sb.index); rs.append(C.pearson(sa[ix], sb[ix]))
        print(f"{w:8s} blank=0: {np.mean(r0):.3f} | mean over users only (>=1 user in each half; {np.mean(n_u):.0f} molecules): {np.nanmean(ru):.3f} | mean over users, >=3 users in each half ({np.mean(n_u5):.0f} molecules): {np.nanmean(ru5):.3f} | share who touched the slider: {np.mean(rs):.3f}")

    hdr("3. Structure flags against names; salts; smallest 'molecules'")
    sn = T["name"].str.contains(r"thi|sulf|mercapt|cyst|methion", case=False)
    print("names that look sulfurous but flag S is False:", list(T["name"][sn & ~T.S]))
    print("flag S is True but the name gives no hint:", list(T["name"][~sn & T.S]))
    nn = T["name"].str.contains(r"amin|amid|nitr|pyri|pyra|pyrrol|indol|azol|cyan|quinol|piperid|urea|caffeine|glutam|prolin|alanin|glycin|lysin|serin|valin|leucin|tyros|trypto|histid|argin|aspar|threon|niacin|carbam|azine|imid|skatole|anthranil", case=False)
    print("flag N is True but the name gives no hint:", list(T["name"][~nn & T.N]))
    print("names that look nitrogenous but flag N is False:", list(T["name"][nn & ~T.N]))
    multi = T[T.smiles.str.contains(".", regex=False)]
    print("multi-component structures (salts etc.):", [(r["name"], r.smiles) for _, r in multi.iterrows()])
    carboxylate = T[T.smiles.str.contains(r"C\(=O\)\[O-\]|\[O-\]C\(=O\)", regex=True)]
    print("carboxylate salts (not counted as acids by the SMARTS):", [(r["name"], r.smiles) for _, r in carboxylate.iterrows()])
    print("smallest by heavy atoms:", [(r["name"], r.smiles, int(r["size"]), r.dil, round(r.share, 2), round(r.PLEASANT, 1)) for _, r in T.sort_values("size").head(6).iterrows()])
    print("molecules with no carbon:", [(r["name"], r.smiles) for _, r in T[~T.smiles.str.contains("C|c")].iterrows()])

    hdr("4. Faint molecules: who is left when few people smell it")
    print("molecules smelled at the stronger dilution by under half the panel: %d; by under 80%%: %d" % ((T.share < .5).sum(), (T.share < .8).sum()))
    lo_ = T[T.share < 0.8]; hi_ = T[T.share >= 0.8]
    print("mean pleasantness: under 80%% smelled %.1f (sd %.1f); at least 80%% %.1f (sd %.1f); mean strength %.1f vs %.1f; mean familiarity %.1f vs %.1f" % (
        lo_.PLEASANT.mean(), lo_.PLEASANT.std(), hi_.PLEASANT.mean(), hi_.PLEASANT.std(), lo_.STRENGTH.mean(), hi_.STRENGTH.mean(), lo_.FAMILIAR.mean(), hi_.FAMILIAR.mean()))
    print("Spearman, share smelled against: strength %+.2f, pleasantness %+.2f, familiarity %+.2f, size %+.2f" % tuple(spearmanr(T.share, T[c])[0] for c in ["STRENGTH", "PLEASANT", "FAMILIAR", "size"]))
    print("S compounds by share smelled: under 80%%: %d of %d; at least 80%%: %d of %d" % (lo_.S.sum(), len(lo_), hi_.S.sum(), len(hi_)))

    hdr("5. O8 and the In-short 'one against one other': exact definitions")
    for a_ in ["PLEASANT", "STRENGTH"]:
        M = C.person_matrix(d, a_, "strong")
        cc = M.T.corr(min_periods=100).values
        v = cc[np.triu_indices_from(cc, 1)]
        print(f"{a_}: pairs of people {np.isfinite(v).sum()}, median {np.nanmedian(v):.3f}, 10th-90th pct {np.nanquantile(v, .1):.2f} to {np.nanquantile(v, .9):.2f}; share of pairs below 0: {np.nanmean(v < 0):.3f}")


if __name__ == "__main__":
    main()
