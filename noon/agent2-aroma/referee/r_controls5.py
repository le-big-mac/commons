"""Referee, last small details. usage: python -I r_controls5.py tidy.csv properties.csv > controls5.out"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import r_core as C

raw = C.load_ratings(sys.argv[1])
d = C.fill_words(raw, "zero")
st, mols = C.structures(sys.argv[2])
T = st.join(C.mol_scores(d, "strong"))
T["name"] = raw.drop_duplicates("cid").set_index("cid")["name"]
T["dil"] = raw[raw.strong].groupby("cid")["dilution"].first()
T["share"] = d[d.strong].groupby("cid")["smelled"].mean()
sm = raw[raw.strong & raw.smelled]
use = sm.groupby("cid")["FISH"].agg(lambda x: x.notna().mean())
n = sm.groupby("cid").size()
T["fish_use"] = use; T["n_sm"] = n
print("share of smellers who touched the fish slider (stronger dilution), top 12 molecules:")
for cid, r in T.sort_values("fish_use", ascending=False).head(12).iterrows():
    print(f"   {r['name'][:40]:40s} {r.fish_use:.2f} of {int(r.n_sm)}  S={int(r.S)} N={int(r.N)}  fish score {r.FISH:.1f}")
print("sulfur molecules: median share touching fish %.3f; molecules above piperidine's fish score: %d of 53 sulfur, %d of 427 others" % (
    T.loc[T.S, "fish_use"].median(), (T.loc[T.S, "FISH"] > T.loc[T["name"] == "Piperidine", "FISH"].iloc[0]).sum(), (T.loc[~T.S, "FISH"] > T.loc[T["name"] == "Piperidine", "FISH"].iloc[0]).sum()))
# own words: fish, counted at the stronger dilution only and at both
for label, sel in [("stronger dilution only", raw.strong), ("both dilutions", raw.strong | ~raw.strong)]:
    ow = raw[sel & raw.ownwords.str.contains("fish", case=False)]
    oc = ow.groupby("cid").size().sort_values(ascending=False)
    print(f"own words containing 'fish', {label}: {len(ow)} vials; top: " + "; ".join(f"{T.loc[c, 'name']} {k}{' [S]' if T.loc[c, 'S'] else ''}{' [N]' if T.loc[c, 'N'] else ''}" for c, k in oc.head(8).items()))
    print("    sample of the wording:", list(ow.ownwords.str.lower().value_counts().head(8).index))
# figure 1 title
ac = T.acid & ~T.S; rest = ~T.acid & ~T.S
print("mean pleasantness: sulfur %.1f; acid without sulfur %.1f (n=%d); neither %.1f (n=%d)" % (T.loc[T.S, "PLEASANT"].mean(), T.loc[ac, "PLEASANT"].mean(), ac.sum(), T.loc[rest, "PLEASANT"].mean(), rest.sum()))
print("of the 48 least pleasant (a tenth): sulfur %d, acid without sulfur %d" % (T.sort_values("PLEASANT").head(48).S.sum(), (T.sort_values("PLEASANT").head(48).acid & ~T.sort_values("PLEASANT").head(48).S).sum()))
# N count if the molecule the sheet calls omega-6-hexadecenlactone is given the lactone's structure
print("nitrogen count if CID 6753 is read as the lactone its name, CAS and catalogue number say: %d" % (T.N.sum() - 1))
# O5 by Pearson and O4 by Pearson
print("Pearson: fam-pleas %+.3f, str-pleas %+.3f" % (C.pearson(T.FAMILIAR, T.PLEASANT), C.pearson(T.STRENGTH, T.PLEASANT)))
