"""Referee, step 1 (blind): recompute the nine items from the description only.
usage: python -I r_blind.py tidy.csv properties.csv > blind.out
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
import r_core as C

pd.set_option("display.width", 250)


def cv_score(X, y, n_jobs=16):
    X = np.asarray(X, float); y = np.asarray(y, float)
    oof = np.zeros(len(y))
    for tr, te in KFold(10, shuffle=True, random_state=0).split(X):
        rf = RandomForestRegressor(n_estimators=500, random_state=0, n_jobs=n_jobs)
        rf.fit(X[tr], y[tr])
        oof[te] = rf.predict(X[te])
    return C.pearson(oof, y), oof


def main():
    tidy, propf = sys.argv[1], sys.argv[2]
    raw = C.load_ratings(tidy)
    d = C.fill_words(raw, "zero")
    st, mols = C.structures(propf)
    sc = C.mol_scores(d, "strong")
    assert len(sc) == 480 and set(sc.index) == set(st.index)
    T = st.join(sc)
    nm = raw.drop_duplicates("cid").set_index("cid")["name"]
    T["name"] = nm
    strongdil = raw[raw["strong"]].groupby("cid")["dilution"].first()
    T["dil"] = strongdil

    print("REFEREE BLIND RECOMPUTATION (own code; Noon's files other than expectations.md not opened)")
    print("score = mean over ratings at the stronger dilution, smellers only, repeat vials pooled; empty word cell from a smeller = 0\n")

    print("== 1. counts")
    print(f"molecules: {len(T)}   sulfur: {int(T.S.sum())}   nitrogen: {int(T.N.sum())}   carboxylic acids: {int(T.acid.sum())}"
          f"   (S and N both: {int((T.S & T.N).sum())}; S and acid: {int((T.S & T.acid).sum())}; N and acid: {int((T.N & T.acid).sum())})")
    print("stronger dilution used:", T["dil"].value_counts().to_dict())
    nsm = d[d["strong"]].groupby("cid")["smelled"].mean()
    print(f"share of ratings at the stronger dilution with 'I smell something': overall {d.loc[d.strong,'smelled'].mean():.3f}; "
          f"per molecule min {nsm.min():.2f} median {nsm.median():.2f} max {nsm.max():.2f}\n")

    print("== 2. mean pleasantness, with and without sulfur")
    a, b = T.loc[T.S, "PLEASANT"], T.loc[~T.S, "PLEASANT"]
    print(f"with S: {a.mean():.2f} (n={len(a)})   without S: {b.mean():.2f} (n={len(b)})   difference: {a.mean()-b.mean():.2f}\n")

    print("== 3. top 20 garlic / top 10 fish")
    g = T.sort_values("GARLIC", ascending=False).head(20)
    print(f"top-20 garlic: {int(g.S.sum())} contain sulfur")
    for cid, r in g.iterrows():
        print(f"   {r.GARLIC:6.2f}  S={int(r.S)} N={int(r.N)}  {r.dil:>10s}  {cid:>8d}  {r['name']}  [{r.smiles}]")
    f = T.sort_values("FISH", ascending=False).head(10)
    print(f"top-10 fish: {int(f.N.sum())} contain nitrogen, {int(f.S.sum())} contain sulfur")
    for cid, r in f.iterrows():
        print(f"   {r.FISH:6.2f}  S={int(r.S)} N={int(r.N)}  {r.dil:>10s}  {cid:>8d}  {r['name']}  [{r.smiles}]")
    print(f"   (20th garlic score {g.GARLIC.iloc[-1]:.2f}, 21st {T.GARLIC.sort_values(ascending=False).iloc[20]:.2f}; "
          f"10th fish {f.FISH.iloc[-1]:.2f}, 11th {T.FISH.sort_values(ascending=False).iloc[10]:.2f})\n")

    print("== 4. Spearman across molecules")
    for x, y in [("FAMILIAR", "PLEASANT"), ("STRENGTH", "PLEASANT"), ("size", "PLEASANT"), ("size", "STRENGTH")]:
        r, p = spearmanr(T[x], T[y])
        print(f"{x:9s} vs {y:9s}: rho = {r:+.3f}  (p={p:.2g})")
    print()

    print("== 5. agreement of one person with the rest (Pearson across molecules; median over 55 people)")
    for a_ in C.MAIN:
        M = C.person_matrix(d, a_, "strong")
        ag = C.agreement_with_rest(M)
        print(f"{a_:9s}: median {np.nanmedian(ag):.3f}   (min {np.nanmin(ag):.3f}, max {np.nanmax(ag):.3f}, n people {np.isfinite(ag).sum()})")
    print()

    print("== 6. most and least pleasant")
    top = T.sort_values("PLEASANT", ascending=False).head(10)
    bot = T.sort_values("PLEASANT").head(10)
    print("10 most pleasant:")
    for cid, r in top.iterrows():
        print(f"   {r.PLEASANT:6.2f}  {r.dil:>10s}  {cid:>8d}  {r['name']}")
    print("10 least pleasant:")
    for cid, r in bot.iterrows():
        print(f"   {r.PLEASANT:6.2f}  S={int(r.S)} acid={int(r.acid)} N={int(r.N)}  {r.dil:>10s}  {cid:>8d}  {r['name']}  [{r.smiles}]")
    print(f"bottom 10: {int(bot.S.sum())} contain sulfur, {int(bot.acid.sum())} are acids, {int((bot.S | bot.acid).sum())} are one or the other")
    van = T[T["name"].str.contains("vanillin", case=False)]
    rk = T["PLEASANT"].rank(ascending=False)
    for cid, r in van.iterrows():
        print(f"   vanillin-like: {r['name']} pleasant {r.PLEASANT:.2f} rank {int(rk[cid])}")
    print()

    print("== 7. model (RF 500 trees seed 0; RDKit CalcMolDescriptors; KFold(10, shuffle, seed 0)); Pearson of out-of-fold predictions")
    for label, order in [("molecules in the order of properties.csv", list(st.index)),
                         ("molecules sorted by CID", sorted(st.index)),
                         ("molecules in order of first appearance in the sheet", list(raw.drop_duplicates('cid')['cid']))]:
        X = C.descriptors(mols, order)
        res = []
        for a_ in ["PLEASANT", "STRENGTH", "GARLIC"]:
            r, _ = cv_score(X.values, T.loc[order, a_].values)
            res.append(f"{a_} {r:.3f}")
        print(f"[{label}; {X.shape[1]} descriptors]  " + "   ".join(res))
    print()

    print("== 8. sulfur yes/no against garlic and fish scores (Pearson, all molecules); forest for garlic on sulfur-free molecules only")
    print(f"Pearson(S, GARLIC) = {C.pearson(T.S.astype(float), T.GARLIC):.3f}    Pearson(S, FISH) = {C.pearson(T.S.astype(float), T.FISH):.3f}"
          f"    Pearson(N, FISH) = {C.pearson(T.N.astype(float), T.FISH):.3f}")
    for label, order in [("order of properties.csv", list(st.index)), ("sorted by CID", sorted(st.index)),
                         ("order of first appearance in the sheet", list(raw.drop_duplicates('cid')['cid']))]:
        o2 = [c for c in order if not T.loc[c, "S"]]
        X = C.descriptors(mols, o2)
        r, _ = cv_score(X.values, T.loc[o2, "GARLIC"].values)
        print(f"forest, garlic, sulfur-free only (n={len(o2)}, {X.shape[1]} descriptors, {label}): {r:.3f}")
    print()

    print("== 9. the 20 molecules given twice: a person against themself; and two different people on all molecules")
    rep_cids = sorted(raw.loc[raw.is_rep, "cid"].unique())
    print("n repeated molecules:", len(rep_cids))
    for a_ in ["STRENGTH", "PLEASANT"]:
        s = d[d.cid.isin(rep_cids) & d.strong]
        first = s[~s.is_rep].set_index(["subject", "cid"])[a_].unstack("cid")
        second = s[s.is_rep].set_index(["subject", "cid"])[a_].unstack("cid")
        rs, ns = [], []
        for subj in first.index:
            rs.append(C.pearson(first.loc[subj], second.loc[subj]))
            ns.append(int((first.loc[subj].notna() & second.loc[subj].notna()).sum()))
        # both dilutions (up to 40 pairs)
        s2 = d[d.cid.isin(rep_cids)]
        f2 = s2[~s2.is_rep].set_index(["subject", "cid", "dil"])[a_].unstack(["cid", "dil"])
        g2 = s2[s2.is_rep].set_index(["subject", "cid", "dil"])[a_].unstack(["cid", "dil"])
        g2 = g2[f2.columns]
        rs2 = [C.pearson(f2.loc[k], g2.loc[k]) for k in f2.index]
        print(f"{a_:9s} self, stronger dilution (20 pairs at most; median pairs available {np.median(ns):.0f}, min {min(ns)}): "
              f"median r = {np.nanmedian(rs):.3f}  (n people with a value {np.isfinite(rs).sum()});"
              f"   both dilutions (40 pairs at most): median r = {np.nanmedian(rs2):.3f}")
    for a_ in ["STRENGTH", "PLEASANT"]:
        # between two different people, all molecules, stronger dilution, first vial pooled with repeat
        M = C.person_matrix(d, a_, "strong")
        A = M.values
        rr = [C.pearson(A[i], A[j]) for i, j in itertools.combinations(range(A.shape[0]), 2)]
        # the same but on the 20 repeated molecules only, single vials (person i first vial vs person j second vial)
        s = d[d.cid.isin(rep_cids) & d.strong]
        first = s[~s.is_rep].set_index(["subject", "cid"])[a_].unstack("cid")
        second = s[s.is_rep].set_index(["subject", "cid"])[a_].unstack("cid")[first.columns]
        F, S2 = first.values, second.values
        rr20 = [C.pearson(F[i], S2[j]) for i in range(F.shape[0]) for j in range(F.shape[0]) if i != j]
        print(f"{a_:9s} two different people, all 480 molecules (stronger dilution): median r = {np.nanmedian(rr):.3f} over {len(rr)} pairs;"
              f"   like-for-like on the 20 repeated molecules (i's first vial vs j's second vial): median r = {np.nanmedian(rr20):.3f}")


if __name__ == "__main__":
    main()
