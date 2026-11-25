"""Referee, step 2, controls that need no forest.
usage: python -I r_controls1.py tidy.csv properties.csv noon-results-molecules.csv > controls1.out
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr, rankdata
from rdkit import Chem
import r_core as C

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 50)
W = C.WORDS


def hdr(s):
    print("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)


def topcount(score, flags, k):
    idx = score.dropna().sort_values(ascending=False).head(k).index
    return {f: int(flags.loc[idx, f].sum()) for f in flags.columns}


def main():
    tidy, propf, noonf = sys.argv[1:4]
    raw = C.load_ratings(tidy)
    d = C.fill_words(raw, "zero")
    st, mols = C.structures(propf)
    T = st.join(C.mol_scores(d, "strong"))
    T["name"] = raw.drop_duplicates("cid").set_index("cid")["name"]
    T["dil"] = raw[raw.strong].groupby("cid")["dilution"].first()
    T["share"] = d[d.strong].groupby("cid")["smelled"].mean()
    T["nsm"] = d[d.strong & d.smelled].groupby("cid").size()
    flags = T[["S", "N", "acid"]]

    # ------------------------------------------------------------------ 0. Noon's per-molecule table against mine
    hdr("0. Noon's results-molecules.csv against my per-molecule table")
    NM = pd.read_csv(noonf).set_index("cid")
    colmap = {"strength": "STRENGTH", "pleasantness": "PLEASANT", "familiarity": "FAMILIAR"}
    colmap.update({w.lower(): w for w in W})
    worst = 0
    for a, b in colmap.items():
        dd = (NM[a] - T.loc[NM.index, b]).abs().max()
        worst = max(worst, dd)
    print(f"largest absolute difference over 23 attributes x 480 molecules: {worst:.2e}")
    print("flags equal:", bool((NM["S"] == T.loc[NM.index, "S"]).all()), bool((NM["N"] == T.loc[NM.index, "N"]).all()),
          bool((NM["is_acid"] == T.loc[NM.index, "acid"]).all()), bool((NM["size"] == T.loc[NM.index, "size"]).all()))

    # ------------------------------------------------------------------ 1. what the word cells look like
    hdr("1. Word cells: value histogram ends, who touches sliders")
    sm = raw[raw.smelled]
    allw = sm[W].values.ravel(); allw = allw[np.isfinite(allw)]
    for nm_, v in [("word sliders", allw), ("strength", sm["STRENGTH"].values), ("pleasant", sm["PLEASANT"].values), ("familiar", sm["FAMILIAR"].values)]:
        vc = pd.Series(v).value_counts()
        print(f"{nm_:13s} n={len(v):7d}  count at 0: {int(vc.get(0, 0)):5d}  1: {int(vc.get(1, 0)):5d}  2: {int(vc.get(2, 0)):5d}  3: {int(vc.get(3,0)):5d} ... 98: {int(vc.get(98, 0)):5d}  99: {int(vc.get(99, 0)):5d}  100: {int(vc.get(100, 0)):5d}   non-integer: {int((v % 1 != 0).sum())}")
    touched = sm[W].notna().sum(axis=1)
    per = sm.assign(t=touched).groupby("subject")["t"].agg(["mean", lambda x: (x == 0).mean(), lambda x: (x == 20).mean(), "size"])
    per.columns = ["mean_touched", "share_none", "share_all20", "n_smelled_rows"]
    print("per person: mean number of word sliders touched per smelled vial: min %.2f median %.2f max %.2f" % (per.mean_touched.min(), per.mean_touched.median(), per.mean_touched.max()))
    print("rows with all 20 touched: %d, from %d people; the 3 people with most: %s" % ((touched == 20).sum(), (per.share_all20 > 0).sum(),
          sm.assign(t=touched)[touched == 20].groupby("subject").size().sort_values(ascending=False).head(3).to_dict()))
    print("rows with none touched: %d, from %d people; top 3: %s" % ((touched == 0).sum(), (per.share_none > 0).sum(),
          sm.assign(t=touched)[touched == 0].groupby("subject").size().sort_values(ascending=False).head(3).to_dict()))
    # share of the panel's garlic "mass" (sum of ratings at stronger dilution) contributed by each person
    ss = d[d.strong & d.smelled]
    for w in ["GARLIC", "FISH"]:
        mass = ss.groupby("subject")[w].sum().sort_values(ascending=False)
        print(f"{w}: share of all slider mass from the top 5 people: {mass.head(5).sum() / mass.sum():.2f}; people who never used it: {(mass == 0).sum()}")

    # ------------------------------------------------------------------ 2. readings of an untouched slider
    hdr("2. O2 / O3 under other readings of an untouched slider (stronger dilution)")
    s_raw = raw[raw.strong]
    sm_raw = s_raw[s_raw.smelled]
    anyw = sm_raw[W].notna().any(axis=1)
    all20 = sm_raw[W].notna().all(axis=1)
    out = []
    def row(label, g, f):
        cg, cf = topcount(g, flags, 20), topcount(f, flags, 10)
        out.append((label, cg["S"], cf["N"], cf["S"], int(g.notna().sum())))
    z = sm_raw.copy(); z[W] = z[W].fillna(0)
    row("blank=0 among smellers (Noon)", z.groupby("cid")["GARLIC"].mean(), z.groupby("cid")["FISH"].mean())
    z55 = s_raw.copy(); z55[W] = z55[W].fillna(0)
    row("blank=0, non-smellers also 0 (mean over everyone)", z55.groupby("cid")["GARLIC"].mean(), z55.groupby("cid")["FISH"].mean())
    row("blank=0, only vials where the person touched >=1 word slider", z[anyw].groupby("cid")["GARLIC"].mean(), z[anyw].groupby("cid")["FISH"].mean())
    row("blank=0, vials with all 20 sliders touched left out", z[~all20].groupby("cid")["GARLIC"].mean(), z[~all20].groupby("cid")["FISH"].mean())
    row("share of smellers who touched the slider", sm_raw.groupby("cid")["GARLIC"].apply(lambda x: x.notna().mean()), sm_raw.groupby("cid")["FISH"].apply(lambda x: x.notna().mean()))
    row("share of smellers who put it at 50 or more", sm_raw.groupby("cid")["GARLIC"].apply(lambda x: (x >= 50).mean()), sm_raw.groupby("cid")["FISH"].apply(lambda x: (x >= 50).mean()))
    row("median with blank=0 is 0 everywhere: use 90th percentile, blank=0", z.groupby("cid")["GARLIC"].quantile(0.9), z.groupby("cid")["FISH"].quantile(0.9))
    for k in (1, 3, 5, 10, 15):
        gu = sm_raw.groupby("cid")["GARLIC"].agg(["mean", "count"]); fu = sm_raw.groupby("cid")["FISH"].agg(["mean", "count"])
        row(f"letter of the rule: mean over users, at least {k} users", gu["mean"].where(gu["count"] >= k), fu["mean"].where(fu["count"] >= k))
    # within-person standardised: each person's garlic rating (blank=0) ranked within person
    print(f"{'reading':72s} garlic top20 S | fish top10 N | fish top10 S | molecules ranked")
    for r in out:
        print(f"{r[0]:72s} {r[1]:8d}       | {r[2]:6d}       | {r[3]:6d}       | {r[4]}")
    gu = sm_raw.groupby("cid")["GARLIC"].agg(["mean", "count"])
    print("number of users of the garlic slider per molecule (stronger dilution): median %.0f, 90th pct %.0f, max %d; molecules with >=5 users: %d, >=10: %d" %
          (gu["count"].median(), gu["count"].quantile(.9), gu["count"].max(), (gu["count"] >= 5).sum(), (gu["count"] >= 10).sum()))
    print("of molecules with >=10 garlic users: %d contain S (of %d)" % (T.loc[gu.index[gu["count"] >= 10], "S"].sum(), (gu["count"] >= 10).sum()))
    print("Spearman between blank=0 garlic score and share who touched: %.3f ; and mean among users (>=5 users): %.3f" % (
        spearmanr(T["GARLIC"], sm_raw.groupby("cid")["GARLIC"].apply(lambda x: x.notna().mean()).loc[T.index])[0],
        spearmanr(T.loc[gu.index[gu["count"] >= 5], "GARLIC"], gu.loc[gu["count"] >= 5, "mean"])[0]))
    # D-sorbitol
    for nm_ in ["D-Sorbitol"]:
        c = T.index[T["name"] == nm_][0]
        rows_ = sm_raw[sm_raw.cid == c]
        print(f"{nm_}: share smelled {T.loc[c,'share']:.2f} (n={len(rows_)}), garlic users {rows_['GARLIC'].notna().sum()}, their values {sorted(rows_['GARLIC'].dropna().astype(int).tolist())}, of them all-20 vials: {int(rows_[W].notna().all(axis=1).sum())}")

    # ------------------------------------------------------------------ 3. dilution mix
    hdr("3. Dilution: which stronger dilution, and the headline numbers by stratum and under other pooling rules")
    print(pd.crosstab(T["dil"], [T["S"]]).rename(columns={False: "no S", True: "S"}))
    print("N-containing by stronger dilution:", pd.crosstab(T["dil"], T["N"])[True].to_dict(), " acids:", pd.crosstab(T["dil"], T["acid"])[True].to_dict())
    print("mean share smelled by stronger dilution:", T.groupby("dil")["share"].mean().round(3).to_dict())
    print("mean scores by stronger dilution:\n", T.groupby("dil")[["STRENGTH", "PLEASANT", "FAMILIAR", "GARLIC", "FISH", "size"]].mean().round(2))
    print("\nby stratum of the stronger dilution:")
    for dl, g in T.groupby("dil"):
        a, b = g.loc[g.S, "PLEASANT"], g.loc[~g.S, "PLEASANT"]
        print(f"  {dl:>10s} n={len(g):3d}: pleasant S {a.mean():5.1f} (n={len(a):2d}) vs no S {b.mean():5.1f}: gap {b.mean()-a.mean():5.1f} | "
              f"fam-pleas {spearmanr(g.FAMILIAR, g.PLEASANT)[0]:+.2f}  str-pleas {spearmanr(g.STRENGTH, g.PLEASANT)[0]:+.2f}  size-pleas {spearmanr(g['size'], g.PLEASANT)[0]:+.2f}  size-str {spearmanr(g['size'], g.STRENGTH)[0]:+.2f}"
              f" | Pearson S-garlic {C.pearson(g.S.astype(float), g.GARLIC):.2f}  S-fish {C.pearson(g.S.astype(float), g.FISH):.2f}")
    # partial out the dilution stratum (centre every variable within stratum, ranks within stratum)
    def within(x):
        return x.groupby(T["dil"]).transform(lambda v: rankdata(v) / len(v))
    print("  Spearman-like, ranks taken within dilution stratum then pooled: fam-pleas %+.2f  str-pleas %+.2f  size-pleas %+.2f  size-str %+.2f" % (
        pearsonr(within(T.FAMILIAR), within(T.PLEASANT))[0], pearsonr(within(T.STRENGTH), within(T.PLEASANT))[0],
        pearsonr(within(T["size"]), within(T.PLEASANT))[0], pearsonr(within(T["size"]), within(T.STRENGTH))[0]))
    # pleasantness gap controlling for strength
    import numpy.linalg as la
    Xd = np.c_[np.ones(len(T)), T.S.astype(float), T.STRENGTH]
    beta = la.lstsq(Xd, T.PLEASANT.values, rcond=None)[0]
    print(f"  least squares pleasant ~ 1 + S + strength: S coefficient {beta[1]:.1f}, strength coefficient {beta[2]:.3f}")
    Xd = np.c_[np.ones(len(T)), T.S.astype(float), T.STRENGTH, pd.get_dummies(T.dil).values[:, 1:].astype(float)]
    beta = la.lstsq(Xd, T.PLEASANT.values, rcond=None)[0]
    print(f"  least squares pleasant ~ 1 + S + strength + dilution stratum: S coefficient {beta[1]:.1f}")
    print("\nheadline numbers under other pooling rules:")
    print(f"  {'rule':48s} gap   garlicS/20 fishN/10 fishS/10  fam-pl  str-pl  size-pl size-str  bottom10 S|acid  top2")
    def headline(label, Tx):
        gap = Tx.loc[~Tx.S, "PLEASANT"].mean() - Tx.loc[Tx.S, "PLEASANT"].mean()
        cg, cf = topcount(Tx["GARLIC"], Tx[["S", "N"]], 20), topcount(Tx["FISH"], Tx[["S", "N"]], 10)
        bot = Tx.sort_values("PLEASANT").head(10)
        top2 = "; ".join(Tx.sort_values("PLEASANT", ascending=False).head(2)["name"])
        print(f"  {label:48s} {gap:5.1f} {cg['S']:6d} {cf['N']:9d} {cf['S']:8d}    {spearmanr(Tx.FAMILIAR, Tx.PLEASANT)[0]:+.2f}   {spearmanr(Tx.STRENGTH, Tx.PLEASANT)[0]:+.2f}   "
              f"{spearmanr(Tx['size'], Tx.PLEASANT)[0]:+.2f}   {spearmanr(Tx['size'], Tx.STRENGTH)[0]:+.2f}     {int((bot.S | bot.acid).sum()):3d}           {top2}")
    headline("stronger dilution, smellers (Noon)", T)
    for which, lab in [("weak", "weaker dilution, smellers"), ("both", "both dilutions pooled, smellers")]:
        Tx = st.join(C.mol_scores(d, which)); Tx["name"] = T["name"]
        Tx = Tx.dropna(subset=["PLEASANT"])
        headline(lab + f" (n={len(Tx)})", Tx)
    # the letter of expectations.md: "all ratings given ... all people": strength with non-smellers at 0
    d0 = d.copy(); d0.loc[~d0.smelled, "STRENGTH"] = 0.0
    T0 = T.copy(); T0["STRENGTH"] = d0[d0.strong].groupby("cid")["STRENGTH"].mean()
    headline("stronger dil., strength: non-smellers = 0", T0)
    # at a common dilution: molecules that have a 1/1,000 vial, scored at 1/1,000 whichever of the two it is
    d1k = d[(d.dilution == "1/1,000") & d.smelled]
    T1k = st.join(d1k.groupby("cid")[C.ATTRS].mean(), how="inner"); T1k["name"] = T["name"]
    headline(f"every molecule that has a 1/1,000 vial, at 1/1,000 (n={len(T1k)})", T1k)
    d100k = d[(d.dilution == "1/100,000") & d.smelled]
    T100k = st.join(d100k.groupby("cid")[C.ATTRS].mean(), how="inner"); T100k["name"] = T["name"]
    headline(f"every molecule that has a 1/100,000 vial, at 1/100,000 (n={len(T100k)})", T100k)
    # molecules smelled by most people only
    headline(f"stronger dil., only molecules smelled by >=80% (n={(T.share >= .8).sum()})", T[T.share >= 0.8])
    headline(f"stronger dil., only molecules smelled by <80% (n={(T.share < .8).sum()})", T[T.share < 0.8])

    # ------------------------------------------------------------------ 4. bootstrap over people
    hdr("4. Bootstrap over the 55 people (2000 resamples): how stable are the counted headlines")
    ss = d[d.strong & d.smelled]
    subs = np.sort(ss.subject.unique()); cids = T.index.values
    cnt = ss.groupby(["subject", "cid"]).size().unstack("cid").reindex(index=subs, columns=cids).fillna(0).values
    sums = {a: ss.groupby(["subject", "cid"])[a].sum().unstack("cid").reindex(index=subs, columns=cids).fillna(0).values for a in ["PLEASANT", "STRENGTH", "FAMILIAR", "GARLIC", "FISH"]}
    S_, N_, A_ = T.S.values, T.N.values, T.acid.values
    names = T["name"].values
    rng = np.random.default_rng(1)
    B = 2000
    rec = {k: [] for k in ["gap", "gS", "fN", "fS", "bot", "van1", "van12", "mtb_last", "famp", "strp", "sizep", "sizes", "r_S_garlic", "r_S_fish", "r_N_fish"]}
    iv = int(np.where(names == "vanillin")[0][0]); iev = int(np.where(names == "Ethyl Vanillin")[0][0]); imt = int(np.where(names == "Methyl thiobutyrate")[0][0])
    size = T["size"].values
    for _ in range(B):
        w = np.bincount(rng.integers(0, len(subs), len(subs)), minlength=len(subs)).astype(float)
        n = w @ cnt
        ok = n > 0
        sc = {a: np.where(ok, (w @ sums[a]) / np.maximum(n, 1), np.nan) for a in sums}
        p = sc["PLEASANT"]
        rec["gap"].append(np.nanmean(p[~S_]) - np.nanmean(p[S_]))
        og = np.argsort(-np.nan_to_num(sc["GARLIC"], nan=-1))[:20]; rec["gS"].append(S_[og].sum())
        of = np.argsort(-np.nan_to_num(sc["FISH"], nan=-1))[:10]; rec["fN"].append(N_[of].sum()); rec["fS"].append(S_[of].sum())
        ob = np.argsort(np.nan_to_num(p, nan=999))[:10]; rec["bot"].append((S_[ob] | A_[ob]).sum())
        ot = np.argsort(-np.nan_to_num(p, nan=-1))
        rec["van1"].append(ot[0] == iv); rec["van12"].append(set(ot[:2]) == {iv, iev}); rec["mtb_last"].append(ob[0] == imt)
        rec["famp"].append(spearmanr(sc["FAMILIAR"][ok], p[ok])[0]); rec["strp"].append(spearmanr(sc["STRENGTH"][ok], p[ok])[0])
        rec["sizep"].append(spearmanr(size[ok], p[ok])[0]); rec["sizes"].append(spearmanr(size[ok], sc["STRENGTH"][ok])[0])
        rec["r_S_garlic"].append(C.pearson(S_[ok].astype(float), sc["GARLIC"][ok])); rec["r_S_fish"].append(C.pearson(S_[ok].astype(float), sc["FISH"][ok]))
        rec["r_N_fish"].append(C.pearson(N_[ok].astype(float), sc["FISH"][ok]))
    def q(k):
        v = np.array(rec[k], float); return f"median {np.median(v):.2f}, 2.5%-97.5%: {np.quantile(v, .025):.2f} to {np.quantile(v, .975):.2f}"
    print("O1 gap:", q("gap"))
    print("O2 garlic top-20 with S:", q("gS"), " share of resamples with >=10:", np.mean(np.array(rec["gS"]) >= 10))
    print("O3 fish top-10 with N:", q("fN"), " share of resamples with >=5:", np.mean(np.array(rec["fN"]) >= 5), "; distribution:", dict(zip(*np.unique(rec["fN"], return_counts=True))))
    print("   fish top-10 with S:", q("fS"), "; distribution:", dict(zip(*np.unique(rec["fS"], return_counts=True))))
    print("O4 fam-pleasant:", q("famp"), " share >=0.4:", np.mean(np.array(rec["famp"]) >= .4))
    print("O5 strength-pleasant:", q("strp"), " share within [-0.3,0.3]:", np.mean(np.abs(rec["strp"]) <= .3))
    print("O6 size-pleasant:", q("sizep"), " share within [0.1,0.5]:", np.mean((np.array(rec["sizep"]) >= .1) & (np.array(rec["sizep"]) <= .5)))
    print("O7 size-strength:", q("sizes"), " share <=-0.2:", np.mean(np.array(rec["sizes"]) <= -.2))
    print("O9 bottom-10 S or acid:", q("bot"), " share >=6:", np.mean(np.array(rec["bot"]) >= 6), "; distribution:", dict(zip(*np.unique(rec["bot"], return_counts=True))))
    print("   vanillin ranked first: %.3f of resamples; vanillin and ethyl vanillin the top two: %.3f; methyl thiobutyrate last: %.3f" % (np.mean(rec["van1"]), np.mean(rec["van12"]), np.mean(rec["mtb_last"])))
    print("Pearson S-garlic:", q("r_S_garlic"), "| S-fish:", q("r_S_fish"), "| N-fish:", q("r_N_fish"))

    # ------------------------------------------------------------------ 5. fish
    hdr("5. 'Fish'")
    rk = T["FISH"].rank(ascending=False, method="min")
    print("fish scores, ranks 1-25:", " ".join(f"{v:.1f}" for v in T["FISH"].sort_values(ascending=False).head(25)))
    print("Pearson across molecules, fish vs garlic: %.3f; fish vs decayed: %.3f; fish vs sweaty %.3f; fish vs ammonia %.3f; fish vs pleasant %.3f; Spearman fish-garlic %.3f" % (
        C.pearson(T.FISH, T.GARLIC), C.pearson(T.FISH, T.DECAYED), C.pearson(T.FISH, T.SWEATY), C.pearson(T.FISH, T.AMMONIA), C.pearson(T.FISH, T.PLEASANT), spearmanr(T.FISH, T.GARLIC)[0]))
    def partial(x, y, z):
        Z = np.c_[np.ones(len(z)), z]
        rx = x - Z @ np.linalg.lstsq(Z, x, rcond=None)[0]; ry = y - Z @ np.linalg.lstsq(Z, y, rcond=None)[0]
        return C.pearson(rx, ry)
    Sf = T.S.astype(float).values
    print("partial Pearson S-fish given garlic: %.3f; given garlic+decayed+sweaty+pleasant: %.3f;  S-garlic given fish: %.3f" % (
        partial(Sf, T.FISH.values, T.GARLIC.values), partial(Sf, T.FISH.values, T[["GARLIC", "DECAYED", "SWEATY", "PLEASANT"]].values), partial(Sf, T.GARLIC.values, T.FISH.values)))
    print("for every word: of the 10 highest molecules, how many contain S, N, acid; Pearson with S; Pearson with N")
    for w in W:
        c = topcount(T[w], flags, 10)
        print(f"   {w:9s} S {c['S']:2d}  N {c['N']:2d}  acid {c['acid']:2d}   r(S) {C.pearson(Sf, T[w]):+.2f}  r(N) {C.pearson(T.N.astype(float), T[w]):+.2f}   top score {T[w].max():5.1f}")
    # amines by structure
    pats = {"primary/secondary/tertiary aliphatic amine (not amide, not on aromatic ring, not N-oxide)": "[NX3;!$(N-C=[O,S,N]);!$(N-a);!$(N=*);!$(N#*);!$(N-[O,N,S])]",
            }
    amine = Chem.MolFromSmarts(list(pats.values())[0])
    acidp = Chem.MolFromSmarts(C.ACID_SMARTS)
    T["amine"] = [mols[c].HasSubstructMatch(amine) for c in T.index]
    T["amino_acid"] = T["amine"] & T["acid"]
    am = T[T.amine & ~T.acid].sort_values("FISH", ascending=False)
    print(f"\namines by SMARTS, carboxylic acids left out: {len(am)} (amine and acid, i.e. amino acids: {int(T.amino_acid.sum())})")
    for cid, r in am.iterrows():
        other = raw[(raw.cid == cid) & ~raw.strong]
        print(f"   {r['name'][:38]:38s} {r.smiles[:28]:28s} stronger dil {r.dil:>10s}  smelled by {r.share:.2f}  fish {r.FISH:5.2f} (rank {int(rk[cid]):3d})  ammonia {r.AMMONIA:5.2f}  strength {r.STRENGTH:5.1f}  pleasant {r.PLEASANT:5.1f}")
    # individual-level: among vials (stronger dilution, smelled), who used the fish slider, by class
    z = sm_raw.copy(); z[W] = z[W].fillna(0)
    z["cls"] = np.where(z.cid.map(T.S), "S", np.where(z.cid.map(T.amine & ~T.acid), "amine (no S, no acid)", np.where(z.cid.map(T.N), "other N", "rest")))
    g = z.groupby("cls").agg(vials=("FISH", "size"), used_fish=("FISH", lambda x: (x > 0).mean()), mean_fish=("FISH", "mean"), used_garlic=("GARLIC", lambda x: (x > 0).mean()),
                             used_ammonia=("AMMONIA", lambda x: (x > 0).mean()), used_decayed=("DECAYED", lambda x: (x > 0).mean()), strength=("STRENGTH", "mean"))
    print("\nper smelled vial at the stronger dilution, by class of molecule:\n", g.round(3))
    # the same, only vials rated at least 50 for strength
    g2 = z[z.STRENGTH >= 50].groupby("cls").agg(vials=("FISH", "size"), used_fish=("FISH", lambda x: (x > 0).mean()), mean_fish=("FISH", "mean"))
    print("only vials the person rated 50 or more for strength:\n", g2.round(3))
    # own words containing 'fish'
    ow = raw[raw.ownwords.str.contains("fish", case=False)]
    print(f"\nfree-text own words containing 'fish': {len(ow)} vials (all dilutions), from {ow.subject.nunique()} people")
    oc = ow.groupby("cid").size().sort_values(ascending=False)
    print("   by class: S %d, amine(no S) %d, other N (no S) %d, rest %d" % (ow.cid.map(T.S).sum(), (ow.cid.map(T.amine & ~T.S)).sum(), (ow.cid.map(T.N & ~T.S & ~T.amine)).sum(), (ow.cid.map(~T.S & ~T.N)).sum()))
    print("   molecules with most 'fish' in own words:", "; ".join(f"{T.loc[c,'name']} {n}{' [S]' if T.loc[c,'S'] else ''}{' [N]' if T.loc[c,'N'] else ''}" for c, n in oc.head(12).items()))
    owg = raw[raw.ownwords.str.contains("garlic|onion", case=False)]
    print(f"   for comparison 'garlic' or 'onion' in own words: {len(owg)} vials; S share {owg.cid.map(T.S).mean():.2f}")
    print("   trimethylamine in the set:", bool((T.smiles == "CN(C)C").any()), "; names containing 'amine':", list(T["name"][T["name"].str.contains("amine", case=False)]))
    # Noon's quoted shares
    for nm_ in ["Butylamine", "Isoamylamine", "Pyrrolidine", "Phenethylamine", "Piperidine"]:
        r = T[T["name"] == nm_].iloc[0]
        dl = sorted(raw[raw.cid == r.name]["dilution"].unique())
        print(f"   {nm_}: dilutions {dl}; smelled at the stronger by {r.share:.2f}; fish {r.FISH:.2f} rank {int(rk[r.name])}")

    # ------------------------------------------------------------------ 6. self against other
    hdr("6. A person against themself and against another person")
    rep_cids = sorted(raw.loc[raw.is_rep, "cid"].unique())
    s = d[d.cid.isin(rep_cids) & d.strong]
    print("vials per repeated molecule at the stronger dilution:", s.groupby("cid")["vial"].nunique().value_counts().to_dict(), " -> two different vial numbers, not one vial twice")
    print("stronger dilutions of the 20 repeated molecules:", T.loc[rep_cids, "dil"].value_counts().to_dict(), "; share smelled min %.2f median %.2f" % (T.loc[rep_cids, "share"].min(), T.loc[rep_cids, "share"].median()))
    print("spread (sd across molecules of the panel score): the 20 repeated: pleasant %.1f strength %.1f ; all 480: pleasant %.1f strength %.1f" % (
        T.loc[rep_cids, "PLEASANT"].std(), T.loc[rep_cids, "STRENGTH"].std(), T.PLEASANT.std(), T.STRENGTH.std()))
    res = {}
    for a_ in C.MAIN:
        by_label_1 = s[~s.is_rep].set_index(["subject", "cid"])[a_].unstack("cid")
        by_label_2 = s[s.is_rep].set_index(["subject", "cid"])[a_].unstack("cid")[by_label_1.columns]
        sv = s.sort_values("vial")
        v1 = sv.groupby(["subject", "cid"])[a_].first().unstack("cid")   # NB first() skips NaN: use nth via vial rank instead
        lo = s.groupby("cid")["vial"].transform("min")
        byv1 = s[s.vial == lo].set_index(["subject", "cid"])[a_].unstack("cid")
        byv2 = s[s.vial != lo].set_index(["subject", "cid"])[a_].unstack("cid")[byv1.columns]
        F1, F2 = by_label_1.values, by_label_2.values
        V1, V2 = byv1.values, byv2.values
        def self_med(A, B, minpairs):
            rs = []
            for i in range(A.shape[0]):
                ok = np.isfinite(A[i]) & np.isfinite(B[i])
                if ok.sum() >= minpairs:
                    rs.append(C.pearson(A[i], B[i]))
            rs = np.array(rs, float)
            return np.nanmedian(rs), int(np.isfinite(rs).sum())
        def other_med(A, B, minpairs):
            rs = []
            for i in range(A.shape[0]):
                for j in range(A.shape[0]):
                    if i != j:
                        ok = np.isfinite(A[i]) & np.isfinite(B[j])
                        if ok.sum() >= minpairs:
                            rs.append(C.pearson(A[i], B[j]))
            return np.nanmedian(rs)
        m0, n0 = self_med(F1, F2, 3); m10, n10 = self_med(F1, F2, 10); mv, nv = self_med(V1, V2, 10)
        o10 = other_med(F1, F2, 10)
        # Noon's version of "another person on the same 20": each person's mean of two vials
        P20 = C.person_matrix(d, a_, "strong")[rep_cids]
        cc = P20.T.corr(min_periods=10).values
        noon20 = np.nanmedian(cc[np.triu_indices_from(cc, 1)])
        Pall = C.person_matrix(d, a_, "strong")
        ca = Pall.T.corr(min_periods=100).values
        allmed = np.nanmedian(ca[np.triu_indices_from(ca, 1)])
        # bootstrap over the 20 molecules
        rng = np.random.default_rng(2)
        bs_self, bs_other, bs_diff = [], [], []
        for _ in range(300):
            ix = rng.integers(0, 20, 20)
            a1, _n = self_med(F1[:, ix], F2[:, ix], 10)
            # other: subsample of pairs for speed
            rs = []
            for i in range(0, 55):
                j = (i + 1 + rng.integers(0, 54)) % 55
                ok = np.isfinite(F1[i, ix]) & np.isfinite(F2[j, ix])
                if ok.sum() >= 10:
                    rs.append(C.pearson(F1[i, ix], F2[j, ix]))
            bs_self.append(a1); bs_other.append(np.nanmedian(rs)); bs_diff.append(a1 - np.nanmedian(rs))
        print(f"{a_:9s} self: by label, no minimum {m0:.3f} (n={n0}); by label, >=10 pairs {m10:.3f} (n={n10}); by vial number, >=10 pairs {mv:.3f} (n={nv})")
        print(f"          another person, same 20 molecules, single vials (i's first, j's second), >=10 pairs: {o10:.3f};  Noon's version (each person's two vials averaged): {noon20:.3f};  all 480 molecules: {allmed:.3f}")
        print(f"          resampling the 20 molecules (300x): self 2.5%-97.5% {np.nanquantile(bs_self, .025):.2f} to {np.nanquantile(bs_self, .975):.2f}; another person {np.nanquantile(bs_other, .025):.2f} to {np.nanquantile(bs_other, .975):.2f}; "
              f"self minus other {np.nanquantile(bs_diff, .025):.2f} to {np.nanquantile(bs_diff, .975):.2f}")
        # all-molecule between-person correlation on single ratings is what 0.29 is (460 single + 20 averaged); self on all molecules does not exist.
        # the weaker dilution gives a second set of 20 pairs
        s2 = d[d.cid.isin(rep_cids) & ~d.strong]
        w1 = s2[~s2.is_rep].set_index(["subject", "cid"])[a_].unstack("cid"); w2 = s2[s2.is_rep].set_index(["subject", "cid"])[a_].unstack("cid")[w1.columns]
        mw, nw = self_med(w1.values, w2.values, 10)
        print(f"          the same at the weaker dilution of the 20: self {mw:.3f} (n={nw}); another person {other_med(w1.values, w2.values, 10):.3f}")

    # ------------------------------------------------------------------ 7. the ceiling
    hdr("7. The 'ceiling': does Spearman-Brown describe these data? Predict the agreement of unequal disjoint sub-panels from the half-split value")
    ssd = d[d.strong & d.smelled]
    subs = np.sort(ssd.subject.unique())
    def sb(r, k):
        return k * r / (1 + (k - 1) * r)
    rng = np.random.default_rng(3)
    for a_ in ["PLEASANT", "STRENGTH", "FAMILIAR", "GARLIC", "FISH", "SWEET", "WARM", "COLD"]:
        tab = ssd.groupby(["subject", "cid"])[a_].agg(["sum", "count"])
        Sm = tab["sum"].unstack("cid").reindex(index=subs, columns=T.index).fillna(0).values
        Cn = tab["count"].unstack("cid").reindex(index=subs, columns=T.index).fillna(0).values
        def panel_mean(idx):
            n = Cn[idx].sum(0); return np.where(n > 0, Sm[idx].sum(0) / np.maximum(n, 1), np.nan)
        rh, r_10_45, r_14_14, r_5_50, r1 = [], [], [], [], []
        for _ in range(200):
            p = rng.permutation(len(subs))
            rh.append(C.pearson(panel_mean(p[:27]), panel_mean(p[27:])))
            r_10_45.append(C.pearson(panel_mean(p[:10]), panel_mean(p[10:])))
            r_14_14.append(C.pearson(panel_mean(p[:14]), panel_mean(p[14:28])))
            r_5_50.append(C.pearson(panel_mean(p[:5]), panel_mean(p[5:])))
            r1.append(C.pearson(panel_mean(p[:1]), panel_mean(p[1:])))
        rh = np.mean(rh)
        rho1 = rh / (27.5 - 26.5 * rh)          # single-person reliability implied by the half-split
        R = lambda k: sb(rho1, k)
        full = R(55)
        print(f"{a_:9s} halves {rh:.3f} -> full-panel reliability {full:.3f}, ceiling sqrt = {np.sqrt(full):.3f} | "
              f"10 vs 45: seen {np.mean(r_10_45):.3f}, SB predicts {np.sqrt(R(10) * R(45)):.3f} | 14 vs 14: seen {np.mean(r_14_14):.3f}, predicts {R(14):.3f} | "
              f"5 vs 50: seen {np.mean(r_5_50):.3f}, predicts {np.sqrt(R(5) * R(50)):.3f} | 1 vs 54: seen (mean) {np.nanmean(r1):.3f}, predicts {np.sqrt(R(1) * R(54)):.3f}")
    # how much of the reliable variance is tied to the dilution the experimenters chose: half A at the stronger dilution against half B at the weaker
    print("\nhalf A of the panel at the stronger dilution against half B (other people) at the WEAKER dilution of the same molecules, and against half B at the stronger (mean of 100 splits):")
    dsm = d[d.smelled]
    for a_ in ["PLEASANT", "STRENGTH", "GARLIC", "FISH"]:
        tabs = {}
        for which, sel in [("strong", dsm.strong), ("weak", ~dsm.strong)]:
            tab = dsm[sel].groupby(["subject", "cid"])[a_].agg(["sum", "count"])
            tabs[which] = (tab["sum"].unstack("cid").reindex(index=subs, columns=T.index).fillna(0).values, tab["count"].unstack("cid").reindex(index=subs, columns=T.index).fillna(0).values)
        def pm(which, idx):
            Sm, Cn = tabs[which]; n = Cn[idx].sum(0); return np.where(n > 0, Sm[idx].sum(0) / np.maximum(n, 1), np.nan)
        x_sw, x_ss, x_ww = [], [], []
        for _ in range(100):
            p = rng.permutation(len(subs))
            x_ss.append(C.pearson(pm("strong", p[:27]), pm("strong", p[27:])))
            x_sw.append(C.pearson(pm("strong", p[:27]), pm("weak", p[27:])))
            x_ww.append(C.pearson(pm("weak", p[:27]), pm("weak", p[27:])))
        dis = np.mean(x_sw) / np.sqrt(np.mean(x_ss) * np.mean(x_ww))
        print(f"   {a_:9s} strong-strong {np.mean(x_ss):.3f}; weak-weak {np.mean(x_ww):.3f}; strong-weak {np.mean(x_sw):.3f}; noise-corrected correlation between the score at the two dilutions {dis:.3f}")

    # ------------------------------------------------------------------ 8. O8 robustness
    hdr("8. O8: one person against the rest")
    ag = {}
    for a_ in C.MAIN:
        ag[a_] = C.agreement_with_rest(C.person_matrix(d, a_, "strong"))
    print("strength agreement above pleasantness agreement in %d of 55 people; median of the per-person difference %.3f" % ((ag["STRENGTH"] > ag["PLEASANT"]).sum(), np.median(ag["STRENGTH"] - ag["PLEASANT"])))
    d0 = d.copy(); d0.loc[~d0.smelled, "STRENGTH"] = 0.0; d0s = d0.copy(); d0s["smelled"] = True
    M0 = d0s[d0s.strong].groupby(["subject", "cid"])["STRENGTH"].mean().unstack("cid")
    print("strength with 'smelled nothing' counted as 0: median %.3f" % np.nanmedian(C.agreement_with_rest(M0)))
    for which in ["weak", "both"]:
        print(f"   {which} dilution(s): " + "; ".join(f"{a_} {np.nanmedian(C.agreement_with_rest(C.person_matrix(d, a_, which))):.3f}" for a_ in C.MAIN))
    rng = np.random.default_rng(4)
    Ms = {a_: C.person_matrix(d, a_, "strong") for a_ in C.MAIN}
    bs = {a_: [] for a_ in C.MAIN}; diff = []
    for _ in range(300):
        ix = rng.integers(0, 480, 480)
        v = {a_: np.nanmedian(C.agreement_with_rest(Ms[a_].iloc[:, ix])) for a_ in C.MAIN}
        for a_ in C.MAIN: bs[a_].append(v[a_])
        diff.append(v["STRENGTH"] - v["PLEASANT"])
    for a_ in C.MAIN:
        print(f"   resampling molecules (300x): {a_} 2.5%-97.5%: {np.quantile(bs[a_], .025):.3f} to {np.quantile(bs[a_], .975):.3f}")
    print("   strength minus pleasantness: %.3f to %.3f; share of resamples with strength higher: %.2f; share with pleasantness <= 0.55: %.2f" % (
        np.quantile(diff, .025), np.quantile(diff, .975), np.mean(np.array(diff) > 0), np.mean(np.array(bs["PLEASANT"]) <= 0.55)))
    # by dilution stratum
    for dl in ["1/10", "1/1,000", "1/100,000"]:
        cols = T.index[T.dil == dl]
        print(f"   only molecules whose stronger dilution is {dl}: " + "; ".join(f"{a_} {np.nanmedian(C.agreement_with_rest(Ms[a_][cols])):.3f}" for a_ in C.MAIN))

    # ------------------------------------------------------------------ 9. small README numbers
    hdr("9. Small numbers quoted in the README")
    med = T.PLEASANT.median()
    print("sulfur compounds above the median pleasantness of all:", int((T.loc[T.S, "PLEASANT"] > med).sum()), "of", int(T.S.sum()))
    rkp = T.PLEASANT.rank(ascending=False)
    ms = T[T.smiles.isin(["CS(=O)(=O)C", "CS(C)(=O)=O"])]
    print("methyl sulfone:", [(r["name"], round(r.PLEASANT, 1), int(rkp[c]), r.dil, round(r.share, 2)) for c, r in ms.iterrows()])
    print("S compounds ranked by pleasantness (top 6):", [(r["name"], round(r.PLEASANT, 1), int(rkp[c]), round(r.share, 2)) for c, r in T[T.S].sort_values("PLEASANT", ascending=False).head(6).iterrows()])
    print("share of rows 'smelled nothing': %.3f" % (1 - raw.smelled.mean()))
    plain = ~T.S & ~T.acid
    print("n neither S nor acid:", int(plain.sum()), " str-pleas among them: %+.2f; fam-pleas among them %+.2f" % (spearmanr(T.loc[plain, "STRENGTH"], T.loc[plain, "PLEASANT"])[0], spearmanr(T.loc[plain, "FAMILIAR"], T.loc[plain, "PLEASANT"])[0]))
    print("fam-strength across molecules: %+.2f" % spearmanr(T.FAMILIAR, T.STRENGTH)[0])
    print("partial Spearman-like fam-pleasant given strength (ranks, residualised): %+.3f" % partial(rankdata(T.FAMILIAR), rankdata(T.PLEASANT), rankdata(T.STRENGTH)))
    wr = sorted((spearmanr(T[w], T.PLEASANT)[0], w) for w in W)
    print("words with pleasantness (Spearman):", "; ".join(f"{w.lower()} {r:+.2f}" for r, w in wr))
    # within person fam-pleasant
    Pf, Pp = C.person_matrix(d, "FAMILIAR", "strong"), C.person_matrix(d, "PLEASANT", "strong")
    wi = [spearmanr(Pf.loc[s_].dropna(), Pp.loc[s_].dropna())[0] for s_ in Pf.index]
    print("fam-pleasant within person: median %+.2f, positive in %d of %d" % (np.median(wi), sum(w > 0 for w in wi), len(wi)))
    T.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref-molecules.csv"))


if __name__ == "__main__":
    main()
