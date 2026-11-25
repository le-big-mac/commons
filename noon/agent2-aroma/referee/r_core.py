"""Referee's core: build per-rating table, per-molecule scores, structure flags. No results printed here."""
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import Descriptors

RDLogger.DisableLog("rdApp.*")

WORDS = ["EDIBLE", "BAKERY", "SWEET", "FRUIT", "FISH", "GARLIC", "SPICES", "COLD", "SOUR", "BURNT", "ACID",
         "WARM", "MUSKY", "SWEATY", "AMMONIA", "DECAYED", "WOOD", "GRASS", "FLOWER", "CHEMICAL"]
MAIN = ["STRENGTH", "PLEASANT", "FAMILIAR"]
ATTRS = MAIN + WORDS
CID_FIX = {"109-19-0": "8038", "3796-70-1": "1549778"}
ACID_SMARTS = "[CX3](=O)[OX2H1]"


def load_ratings(tidy_csv):
    df = pd.read_csv(tidy_csv, dtype=str, keep_default_na=False)
    df["cid"] = df["cid_raw"].replace(CID_FIX).astype(int)
    df["dil"] = df["dilution"].str.replace(",", "").map(lambda s: 1.0 / float(s.split("/")[1]))
    df["subject"] = df["subject"].astype(int)
    df["vial"] = df["vial"].astype(int)
    df["smelled"] = df["smell"] == "I smell something"
    assert set(df["smell"]) == {"I smell something", "I can't smell anything"}
    for c in ATTRS:
        df[c] = pd.to_numeric(df[c].replace("", np.nan))
    df["is_rep"] = df["odor"].str.contains("replicate", case=False)
    # the stronger of each molecule's two dilutions
    mx = df.groupby("cid")["dil"].transform("max")
    df["strong"] = df["dil"] == mx
    # canonical name: non-replicate name
    names = (df[~df["is_rep"]].groupby("cid")["odor"].first())
    df["name"] = df["cid"].map(names)
    return df


def fill_words(df, how="zero"):
    """how='zero': empty word cell from someone who smelled = 0.  how='nan': leave empty.
    how='zero_if_any': 0 only if the person touched at least one word slider on that vial, else left empty."""
    d = df.copy()
    if how == "zero":
        for w in WORDS:
            d.loc[d["smelled"] & d[w].isna(), w] = 0.0
    elif how == "zero_if_any":
        anyw = d[WORDS].notna().any(axis=1)
        for w in WORDS:
            d.loc[d["smelled"] & anyw & d[w].isna(), w] = 0.0
    elif how == "nan":
        pass
    else:
        raise ValueError(how)
    return d


def mol_scores(d, which="strong"):
    """mean over ratings (smellers only; non-smellers have NaN and drop out), repeat vials pooled."""
    if which == "strong":
        s = d[d["strong"] & d["smelled"]]
    elif which == "weak":
        s = d[~d["strong"] & d["smelled"]]
    elif which == "both":
        s = d[d["smelled"]]
    else:
        raise ValueError(which)
    sc = s.groupby("cid")[ATTRS].mean()
    return sc


def person_matrix(d, attr, which="strong"):
    """people x molecules matrix: a person's rating (mean over that person's repeat vials) at the chosen dilution."""
    if which == "strong":
        s = d[d["strong"]]
    elif which == "weak":
        s = d[~d["strong"]]
    else:
        s = d
    s = s[s["smelled"]]
    return s.groupby(["subject", "cid"])[attr].mean().unstack("cid")


def structures(prop_csv):
    prop = pd.read_csv(prop_csv)
    prop["CID"] = prop["CID"].astype(int)
    prop = prop.set_index("CID")
    acid = Chem.MolFromSmarts(ACID_SMARTS)
    rows = {}
    mols = {}
    for cid, smi in prop["SMILES"].items():
        m = Chem.MolFromSmiles(smi)
        assert m is not None, (cid, smi)
        syms = [a.GetSymbol() for a in m.GetAtoms()]
        rows[cid] = dict(S="S" in syms, N="N" in syms, acid=m.HasSubstructMatch(acid),
                         size=m.GetNumHeavyAtoms(), smiles=smi, iupac=prop.loc[cid, "IUPACName"],
                         formula=prop.loc[cid, "MolecularFormula"])
        mols[cid] = m
    return pd.DataFrame.from_dict(rows, orient="index"), mols


def descriptors(mols, order):
    rows = [Descriptors.CalcMolDescriptors(mols[c]) for c in order]
    X = pd.DataFrame(rows, index=order).astype(float)
    X = X.replace([np.inf, -np.inf], np.nan)
    # also treat absurdly large values as non-finite? No: follow the stated rule only (non-finite -> median).
    X = X.fillna(X.median())
    X = X.loc[:, X.nunique() > 1]
    return X


def pearson(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or a[ok].std() == 0 or b[ok].std() == 0:
        return np.nan
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def agreement_with_rest(M):
    """M: people x molecules (NaN where not smelled). For each person: Pearson across molecules between their
    ratings and the mean of everyone else's (mean over other people who smelled it)."""
    A = M.values
    n = np.isfinite(A).sum(axis=0)
    tot = np.nansum(A, axis=0)
    out = []
    for i in range(A.shape[0]):
        has = np.isfinite(A[i])
        rest_n = n - has
        rest = np.where(rest_n > 0, (tot - np.where(has, A[i], 0.0)) / np.maximum(rest_n, 1), np.nan)
        out.append(pearson(A[i], rest))
    return np.array(out)
