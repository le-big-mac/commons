"""Referee, step 2, controls that need the forest (and a scan of single descriptors).
usage: python -I r_controls2.py tidy.csv properties.csv chunk1|chunk2|chunk3|report
The forests are run in three chunks of 8 (one core each, 8 workers) so that no run takes more than about five minutes
on a shared machine; out-of-fold predictions are cached in oof_chunk*.npz; 'report' prints from the caches.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from rdkit import Chem
import r_core as C

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)


def hdr(s):
    print("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110, flush=True)


def folds(n, seed):
    return list(KFold(10, shuffle=True, random_state=seed).split(np.arange(n)))


def cv_forest(key, X, y, seed=0):
    X = np.asarray(X, float); y = np.asarray(y, float)
    oof = np.zeros(len(y))
    for tr, te in folds(len(y), seed):
        rf = RandomForestRegressor(n_estimators=500, random_state=seed, n_jobs=1).fit(X[tr], y[tr])
        oof[te] = rf.predict(X[te])
    return key, oof


def cv_groupmean(flag, y, seed=0):
    """the 'one fact' put through the same folds: predict the training-fold mean of the molecule's class"""
    flag = np.asarray(flag, bool); y = np.asarray(y, float)
    oof = np.zeros(len(y))
    for tr, te in folds(len(y), seed):
        m1, m0 = y[tr][flag[tr]].mean(), y[tr][~flag[tr]].mean()
        oof[te] = np.where(flag[te], m1, m0)
    return oof


def r2(pred, y):
    return 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def build(tidy, propf):
    raw = C.load_ratings(tidy)
    d = C.fill_words(raw, "zero")
    st, mols = C.structures(propf)
    T = st.join(C.mol_scores(d, "strong"))
    T = T.loc[sorted(T.index)]                       # Noon's order (groupby cid -> sorted)
    T["name"] = raw.drop_duplicates("cid").set_index("cid")["name"]
    T["dil"] = raw[raw.strong].groupby("cid")["dilution"].first()
    T["share"] = d[d.strong].groupby("cid")["smelled"].mean()
    order = list(T.index)
    Xdf = C.descriptors(mols, order)
    X = Xdf.values
    S = T.S.values; nos = ~S
    Y = {a: T[a].values for a in C.ATTRS}
    Xn = C.descriptors(mols, [c for c in order if not T.loc[c, "S"]]).values
    Xs = C.descriptors(mols, [c for c in order if T.loc[c, "S"]]).values
    Tw = C.mol_scores(d, "weak").reindex(order); Tb = C.mol_scores(d, "both").reindex(order)
    sm_raw = raw[raw.strong & raw.smelled]
    g_share = sm_raw.groupby("cid")["GARLIC"].apply(lambda x: x.notna().mean()).reindex(order).values
    logdil = np.log10(raw[raw.strong].groupby("cid")["dil"].first().reindex(order).values)
    dd = d[~d.subject.isin([52, 48])]
    g_wo = dd[dd.strong & dd.smelled].groupby("cid")["GARLIC"].mean().reindex(order).values
    spec = {
        "chunk1": [("all|GARLIC|0", X, Y["GARLIC"], 0), ("all|FISH|0", X, Y["FISH"], 0), ("all|PLEASANT|0", X, Y["PLEASANT"], 0), ("all|STRENGTH|0", X, Y["STRENGTH"], 0),
                   ("noS|GARLIC|0", Xn, Y["GARLIC"][nos], 0), ("noS|PLEASANT|0", Xn, Y["PLEASANT"][nos], 0), ("onlyS|GARLIC|0", Xs, Y["GARLIC"][S], 0), ("target|logdil|0", X, logdil, 0)],
        "chunk2": [("all|GARLIC|1", X, Y["GARLIC"], 1), ("all|GARLIC|2", X, Y["GARLIC"], 2), ("all|GARLIC|3", X, Y["GARLIC"], 3), ("all|GARLIC|4", X, Y["GARLIC"], 4),
                   ("weak|GARLIC|0", X, Tw["GARLIC"].values, 0), ("both|GARLIC|0", X, Tb["GARLIC"].values, 0), ("share_touched|GARLIC|0", X, g_share, 0), ("without_52_48|GARLIC|0", X, g_wo, 0)],
        "chunk3": [("weak|PLEASANT|0", X, Tw["PLEASANT"].values, 0), ("both|PLEASANT|0", X, Tb["PLEASANT"].values, 0), ("weak|STRENGTH|0", X, Tw["STRENGTH"].values, 0), ("both|STRENGTH|0", X, Tb["STRENGTH"].values, 0),
                   ("plusdil|PLEASANT|0", np.c_[X, logdil], Y["PLEASANT"], 0), ("plusdil|GARLIC|0", np.c_[X, logdil], Y["GARLIC"], 0), ("target|share|0", X, T["share"].values, 0), ("without_52_48_noS|GARLIC|0", Xn, g_wo[nos], 0)],
    }
    return dict(raw=raw, d=d, st=st, mols=mols, T=T, order=order, Xdf=Xdf, X=X, S=S, nos=nos, Y=Y, Tw=Tw, Tb=Tb, g_share=g_share, logdil=logdil, g_wo=g_wo, spec=spec)


def report(B):
    res = {}
    for ch in ("chunk1", "chunk2", "chunk3"):
        z = np.load(os.path.join(HERE, f"oof_{ch}.npz"))
        res.update({k: z[k] for k in z.files})
    T, order, Xdf, X, S, nos, Y, mols, d, raw = B["T"], B["order"], B["Xdf"], B["X"], B["S"], B["nos"], B["Y"], B["mols"], B["d"], B["raw"]
    Tw, Tb, g_share, logdil, g_wo = B["Tw"], B["Tb"], B["g_share"], B["logdil"], B["g_wo"]
    n = len(T); Sf = S.astype(float)
    print("descriptors:", X.shape, "; values beyond +-1e6 (Noon clips these; the description given to me did not say so):", int((np.abs(X) > 1e6).sum()))

    hdr("A. Molecules the forest 'has not seen': identical descriptor rows / same connectivity")
    prop = pd.read_csv(sys.argv[2]).set_index("CID")
    canon = np.array([Chem.MolToSmiles(Chem.MolFromSmiles(s)) for s in prop.loc[order, "ConnectivitySMILES"].values])
    vc = pd.Series(canon).value_counts()
    print("groups of molecules sharing one connectivity (stereo-isomers of each other):", int((vc > 1).sum()), "groups,", int(vc[vc > 1].sum()), "molecules")
    rowkey = np.array([r.tobytes() for r in np.ascontiguousarray(X)], dtype=object)
    vr = pd.Series(rowkey).value_counts()
    print("groups of molecules with identical descriptor rows:", int((vr > 1).sum()), "groups,", int(vr[vr > 1].sum()), "molecules")
    f0 = np.zeros(n, int)
    for i, (tr, te) in enumerate(folds(n, 0)):
        f0[te] = i
    for k in vr[vr > 1].index:
        ix = np.where(rowkey == k)[0]
        print("    ", " | ".join(f"{T['name'].iloc[i]} (fold {f0[i]}, pleasant {T.PLEASANT.iloc[i]:.0f}, strength {T.STRENGTH.iloc[i]:.0f}, {T.dil.iloc[i]})" for i in ix))
    for k in vc[vc > 1].index:
        ix = np.where(canon == k)[0]
        print("     same connectivity:", " | ".join(f"{T['name'].iloc[i]} (fold {f0[i]})" for i in ix))

    hdr("B. Garlic (and fish, pleasantness): 'sulfur yes/no' against the forest, on equal terms")
    for a in ["GARLIC", "FISH", "PLEASANT", "STRENGTH"]:
        y = Y[a]; f = res[f"all|{a}|0"]; g = cv_groupmean(S, y, 0)
        print(f"{a:9s} forest out-of-fold: Pearson {C.pearson(f, y):.3f}  Spearman {spearmanr(f, y)[0]:.3f}  R2 {r2(f, y):+.3f} | "
              f"sulfur yes/no in-sample Pearson {abs(C.pearson(Sf, y)):.3f}; put through the same folds (training-fold class means): Pearson {C.pearson(g, y):.3f}  Spearman {spearmanr(g, y)[0]:.3f}  R2 {r2(g, y):+.3f}")
    y = Y["GARLIC"]; f = res["all|GARLIC|0"]; g = cv_groupmean(S, y, 0)
    rng = np.random.default_rng(5)
    dP, dS = [], []
    for _ in range(4000):
        ix = rng.integers(0, n, n)
        dP.append(C.pearson(f[ix], y[ix]) - C.pearson(g[ix], y[ix])); dS.append(spearmanr(f[ix], y[ix])[0] - spearmanr(g[ix], y[ix])[0])
    print(f"garlic, forest minus sulfur-alone, resampling molecules (4000x): Pearson difference 2.5%-97.5%: {np.quantile(dP, .025):+.3f} to {np.quantile(dP, .975):+.3f}; Spearman difference {np.quantile(dS, .025):+.3f} to {np.quantile(dS, .975):+.3f}")
    print("garlic forest over fold/forest seeds 0-4: " + " ".join(f"{C.pearson(res[f'all|GARLIC|{s}'], y):.3f}" for s in range(5))
          + " ; sulfur alone through the folds of seeds 0-4: " + " ".join(f"{C.pearson(cv_groupmean(S, y, s), y):.3f}" for s in range(5)))
    print(f"correlation between the forest's garlic prediction and sulfur yes/no: {C.pearson(f, Sf):.3f}")
    rS = C.pearson(f[S], y[S]); z = np.arctanh(rS); se = 1 / np.sqrt(S.sum() - 3)
    print(f"forest (trained on all) within the {S.sum()} sulfur molecules: Pearson {rS:.3f} (95% interval by Fisher z {np.tanh(z - 1.96 * se):+.2f} to {np.tanh(z + 1.96 * se):+.2f}), Spearman {spearmanr(f[S], y[S])[0]:.3f};"
          f" over seeds 0-4: " + " ".join(f"{C.pearson(res[f'all|GARLIC|{s}'][S], y[S]):.2f}" for s in range(5)))
    print(f"forest (trained on all) within the {nos.sum()} sulfur-free: Pearson {C.pearson(f[nos], y[nos]):.3f}, Spearman {spearmanr(f[nos], y[nos])[0]:.3f}")
    fn = res["noS|GARLIC|0"]
    print(f"forest trained and tested on sulfur-free only: garlic Pearson {C.pearson(fn, y[nos]):.3f} Spearman {spearmanr(fn, y[nos])[0]:.3f}; pleasantness {C.pearson(res['noS|PLEASANT|0'], Y['PLEASANT'][nos]):.3f}")
    print(f"forest trained and tested on the 53 sulfur molecules only: garlic Pearson {C.pearson(res['onlyS|GARLIC|0'], y[S]):.3f}")
    print(f"garlic score: sd among sulfur molecules {y[S].std():.2f} (mean {y[S].mean():.2f}); sd among sulfur-free {y[nos].std():.2f} (mean {y[nos].mean():.2f}); share of garlic variance between the two classes {C.pearson(Sf, y) ** 2:.2f}; "
          f"within the sulfur class {(S.sum() * y[S].var()) / (n * y.var()):.2f}; within sulfur-free {(nos.sum() * y[nos].var()) / (n * y.var()):.2f}")
    ssd = d[d.strong & d.smelled]
    subs = np.sort(ssd.subject.unique())
    rng = np.random.default_rng(6)
    for a in ["GARLIC", "FISH", "PLEASANT"]:
        tab = ssd.groupby(["subject", "cid"])[a].agg(["sum", "count"])
        Sm = tab["sum"].unstack("cid").reindex(index=subs, columns=order).fillna(0).values
        Cn = tab["count"].unstack("cid").reindex(index=subs, columns=order).fillna(0).values
        hs, hn, ha = [], [], []
        for _ in range(200):
            p = rng.permutation(len(subs)); A, Bh = p[:27], p[27:]
            mA = Sm[A].sum(0) / np.maximum(Cn[A].sum(0), 1); mB = Sm[Bh].sum(0) / np.maximum(Cn[Bh].sum(0), 1)
            hs.append(C.pearson(mA[S], mB[S])); hn.append(C.pearson(mA[nos], mB[nos])); ha.append(C.pearson(mA, mB))
        cs = lambda r: np.sqrt(2 * r / (1 + r))
        print(f"{a:9s} two halves of the panel agree: all {np.mean(ha):.3f} (ceiling {cs(np.mean(ha)):.2f}); among the 53 sulfur molecules {np.mean(hs):.3f} (ceiling {cs(np.mean(hs)):.2f}); among the 427 sulfur-free {np.mean(hn):.3f} (ceiling {cs(np.mean(hn)):.2f})")
    pat = Chem.MolFromSmarts("[SX2;!a]")
    sx2 = np.array([mols[c].HasSubstructMatch(pat) for c in order])
    print(f"referee's own single fact, 'has a two-connected non-aromatic sulfur' (thiol, sulfide, di/trisulfide, thioester; {sx2.sum()} molecules, all among the sulfur ones: {sx2[S].sum()}): Pearson with garlic, all molecules {C.pearson(sx2.astype(float), y):.3f}; "
          f"through the folds {C.pearson(cv_groupmean(sx2, y, 0), y):.3f}; among the 53 sulfur molecules {C.pearson(sx2[S].astype(float), y[S]):.3f}; with fish, all {C.pearson(sx2.astype(float), Y['FISH']):.3f}; with pleasantness {C.pearson(sx2.astype(float), Y['PLEASANT']):.3f}")
    print(f"garlic without the two people who move every slider (52, 48): sulfur alone {C.pearson(Sf, g_wo):.3f}; forest {C.pearson(res['without_52_48|GARLIC|0'], g_wo):.3f}; forest among sulfur-free {C.pearson(res['without_52_48_noS|GARLIC|0'], g_wo[nos]):.3f}; top-20 with sulfur {int(S[np.argsort(-g_wo)[:20]].sum())}")
    gs = res["share_touched|GARLIC|0"]
    print(f"garlic as 'share of smellers who touched the slider': sulfur alone {C.pearson(Sf, g_share):.3f}; forest {C.pearson(gs, g_share):.3f} (Spearman: sulfur {spearmanr(Sf, g_share)[0]:.3f}, forest {spearmanr(gs, g_share)[0]:.3f})")
    Tn = T[nos]
    oth = [w for w in C.WORDS if w != "GARLIC"]
    print("among sulfur-free molecules, garlic score against: mean of the other 19 words %.2f; decayed %.2f; burnt %.2f; fish %.2f; strength %.2f; pleasant %.2f; share smelled %.2f (Pearson)" % (
        C.pearson(Tn.GARLIC, Tn[oth].mean(axis=1)), C.pearson(Tn.GARLIC, Tn.DECAYED), C.pearson(Tn.GARLIC, Tn.BURNT), C.pearson(Tn.GARLIC, Tn.FISH), C.pearson(Tn.GARLIC, Tn.STRENGTH), C.pearson(Tn.GARLIC, Tn.PLEASANT), C.pearson(Tn.GARLIC, Tn.share)))

    hdr("D. Dilution and the model")
    print(f"can the forest tell from the structure which dilution the experimenters chose? log10(stronger dilution) out-of-fold Pearson {C.pearson(res['target|logdil|0'], logdil):.3f}; share of the panel that smelled it: {C.pearson(res['target|share|0'], T['share'].values):.3f}")
    for a in ["PLEASANT", "STRENGTH", "GARLIC"]:
        f = res[f"all|{a}|0"]
        parts = []
        for dl in ["1/10", "1/1,000", "1/100,000"]:
            m = (T.dil == dl).values
            parts.append(f"{dl} (n={m.sum()}): {C.pearson(f[m], Y[a][m]):.3f}")
        gm = T.groupby("dil")[a].transform("mean").values
        extra = f" | forest + dilution as input {C.pearson(res[f'plusdil|{a}|0'], Y[a]):.3f}" if f"plusdil|{a}|0" in res else ""
        print(f"{a:9s} forest within stratum: " + "; ".join(parts) + f" | stratum alone (in-sample) {C.pearson(gm, Y[a]):.3f}" + extra)
    for a in ["PLEASANT", "STRENGTH", "GARLIC"]:
        print(f"{a:9s} target at the weaker dilution: forest {C.pearson(res[f'weak|{a}|0'], Tw[a].values):.3f};  both dilutions pooled: forest {C.pearson(res[f'both|{a}|0'], Tb[a].values):.3f}"
              + f";  sulfur alone: weaker {abs(C.pearson(Sf, Tw[a].values)):.3f}, both {abs(C.pearson(Sf, Tb[a].values)):.3f}")

    hdr("E. 'Sulfur is the single strongest fact': every single descriptor and yes/no fact against the scores (in-sample, as Noon's sulfur number is)")
    facts = {}
    for el in ["S", "N", "O", "Cl", "Br"]:
        facts[f"contains {el}"] = np.array([any(a.GetSymbol() == el for a in mols[c].GetAtoms()) for c in order], float)
    smarts = {"carboxylic acid": C.ACID_SMARTS, "ester": "[CX3](=O)[OX2H0][#6]", "aromatic ring": "a", "aldehyde": "[CX3H1](=O)[#6]", "ketone": "[#6][CX3](=O)[#6]",
              "alcohol OH": "[CX4][OX2H]", "phenol OH": "c[OX2H]", "any OH": "[OX2H]", "C=C": "C=C", "ring": "[R]", "thiol SH": "[SX2H]", "amine": "[NX3;!$(N-C=[O,S,N]);!$(N-a)]"}
    for k, s in smarts.items():
        p = Chem.MolFromSmarts(s)
        facts[k] = np.array([mols[c].HasSubstructMatch(p) for c in order], float)
    for col in Xdf.columns:
        if col.startswith("fr_"):
            v = (Xdf[col].values > 0).astype(float)
            if 5 <= v.sum() <= n - 5:
                facts[col + ">0"] = v
    F = pd.DataFrame(facts, index=order)
    for a in ["PLEASANT", "GARLIC", "FISH", "STRENGTH", "DECAYED", "SWEET", "FRUIT"]:
        y = Y[a]
        rb = F.apply(lambda v: C.pearson(v.values, y)).dropna()
        rc = Xdf.apply(lambda v: spearmanr(v.values, y)[0]).dropna()
        rcp = Xdf.apply(lambda v: C.pearson(v.values, y)).dropna()
        tb = rb.abs().sort_values(ascending=False)
        tc = rc.abs().sort_values(ascending=False)
        rs = abs(C.pearson(Sf, y)); rss = abs(spearmanr(Sf, y)[0])
        print(f"{a:9s} yes/no facts by |Pearson|: " + "; ".join(f"{k} {rb[k]:+.2f} (n={int(F[k].sum())})" for k in tb.index[:6]))
        print(f"          sulfur's rank among {len(rb)} yes/no facts: {int((tb > rs + 1e-12).sum()) + 1}; sulfur |Pearson| {rs:.2f}, |Spearman| {rss:.2f}; continuous descriptors with |Pearson| above sulfur's: {int((rcp.abs() > rs).sum())} of {len(rcp)}; with |Spearman| above sulfur's |Spearman|: {int((tc > rss).sum())}; the top by |Spearman|: "
              + "; ".join(f"{k} {rc[k]:+.2f}" for k in tc.index[:5]))
    y = Y["PLEASANT"]
    for k in ["ester", "carboxylic acid", "contains N", "contains O"]:
        Z = np.c_[np.ones(n), Sf, F[k].values]
        beta = np.linalg.lstsq(Z, y, rcond=None)[0]
        print(f"   pleasantness ~ sulfur + {k}: coefficients {beta[1]:+.1f}, {beta[2]:+.1f}; multiple R {np.sqrt(r2(Z @ beta, y)):.3f}")


def main():
    tidy, propf, mode = sys.argv[1:4]
    B = build(tidy, propf)
    if mode == "report":
        report(B)
    else:
        out = dict(Parallel(n_jobs=8)(delayed(cv_forest)(*t) for t in B["spec"][mode]))
        np.savez(os.path.join(HERE, f"oof_{mode}.npz"), **out)
        print(mode, "done:", list(out))


if __name__ == "__main__":
    main()
