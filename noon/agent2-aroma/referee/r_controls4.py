"""Referee, step 2, follow-ups. usage: python -I r_controls4.py tidy.csv properties.csv > controls4.out"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
import r_core as C

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_colwidth", 70)


def hdr(s):
    print("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110, flush=True)


def cv(X, y, seed=0):
    oof = np.zeros(len(y))
    for tr, te in KFold(10, shuffle=True, random_state=seed).split(X):
        oof[te] = RandomForestRegressor(n_estimators=500, random_state=seed, n_jobs=8).fit(X[tr], y[tr]).predict(X[te])
    return oof


def main():
    tidy, propf = sys.argv[1:3]
    raw = C.load_ratings(tidy)
    d = C.fill_words(raw, "zero")
    st, mols = C.structures(propf)
    T = st.join(C.mol_scores(d, "strong"))
    T = T.loc[sorted(T.index)]
    T["name"] = raw.drop_duplicates("cid").set_index("cid")["name"]
    T["dil"] = raw[raw.strong].groupby("cid")["dilution"].first()
    T["share"] = d[d.strong].groupby("cid")["smelled"].mean()
    T["cas"] = raw.drop_duplicates("cid").set_index("cid")["cas"]

    hdr("1. The sheet's name against PubChem's structure for the same compound number")
    for nm in ["omega-6-Hexadecenlactone", "musk ketone", "D-Sorbitol", "Water", "Sodium phosphate dibasic", "Methyl sulfone"]:
        r = T[T["name"] == nm].iloc[0]
        print(f"   {nm}: CID {r.name}, CAS in sheet {r.cas}, PubChem formula {r.formula}, IUPAC '{r.iupac}', SMILES {r.smiles}; stronger dilution {r.dil}, smelled by {r.share:.2f}, pleasant {r.PLEASANT:.1f}, strength {r.STRENGTH:.1f}, garlic {r.GARLIC:.1f}")
    # crude element hints
    hint = {"Cl": r"chlor", "Br": r"brom", "I": r"iod"}
    for el, pat in hint.items():
        has = T.smiles.str.contains(el, regex=False)
        nm_ = T["name"].str.contains(pat, case=False)
        print(f"   element {el}: in structure but not in name {list(T['name'][has & ~nm_])}; in name but not in structure {list(T['name'][~has & nm_])}")
    # heavy-atom count in formula against a carbon count implied by simple alkyl names is not attempted; a random sample to read by eye
    rs = np.random.default_rng(0).choice(len(T), 45, replace=False)
    print("   a random 45 to read by eye (sheet name | PubChem formula | PubChem IUPAC name):")
    for i in sorted(rs):
        r = T.iloc[i]
        print(f"      {r['name'][:42]:42s} | {r.formula:10s} | {str(r.iupac)[:70]}")

    hdr("2. The baseline for 'I smell something': the least-smelled molecules at their stronger dilution")
    for _, r in T.sort_values("share").head(22).iterrows():
        print(f"   {r['name'][:40]:40s} {r.dil:>10s} smelled by {r.share:.2f}  strength {r.STRENGTH:5.1f} pleasant {r.PLEASANT:5.1f} familiar {r.FAMILIAR:5.1f}")
    # share smelled at the weaker dilution, all molecules
    wk = d[~d.strong].groupby("cid")["smelled"].mean()
    print("   share smelled at the WEAKER dilution: median %.2f, 10th pct %.2f; at the stronger: median %.2f, 10th pct %.2f" % (wk.median(), wk.quantile(.1), T.share.median(), T.share.quantile(.1)))
    w = T[T["name"] == "Water"].iloc[0]
    print(f"   water: smelled by {w.share:.2f} at {w.dil}; at its weaker dilution {wk[w.name]:.2f}")
    # per person: share of water vials 'smelled'
    wv = d[d.cid == w.name]
    print(f"   water vials: {len(wv)} ratings, {wv.smelled.mean():.2f} smelled; mean strength among those who smelled {wv.loc[wv.smelled, 'STRENGTH'].mean():.1f}")

    hdr("3. O10's garlic part under the letter of the rule (mean over the people who used the slider)")
    order = list(T.index)
    sm_raw = raw[raw.strong & raw.smelled]
    gu = sm_raw.groupby("cid")["GARLIC"].agg(["mean", "count"]).reindex(order)
    X = C.descriptors(mols, order)
    for k in (1, 5):
        m = (gu["count"] >= k).values
        Xk = C.descriptors(mols, [c for c, mm in zip(order, m) if mm]).values
        y = gu["mean"].values[m]
        oof = cv(Xk, y)
        print(f"   garlic = mean over users, molecules with >= {k} users (n={m.sum()}): forest out-of-fold Pearson {C.pearson(oof, y):.3f}; sulfur yes/no Pearson {C.pearson(T.S.values[m].astype(float), y):.3f}")


if __name__ == "__main__":
    main()
