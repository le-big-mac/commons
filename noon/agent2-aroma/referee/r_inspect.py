"""Referee: look at the layout of the tidy table. usage: python -I r_inspect.py tidy.csv properties.csv"""
import sys
import pandas as pd
import numpy as np

pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", 60)
WORDS = ["EDIBLE", "BAKERY", "SWEET", "FRUIT", "FISH", "GARLIC", "SPICES", "COLD", "SOUR", "BURNT", "ACID",
         "WARM", "MUSKY", "SWEATY", "AMMONIA", "DECAYED", "WOOD", "GRASS", "FLOWER", "CHEMICAL"]
df = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
prop = pd.read_csv(sys.argv[2], dtype=str)
print(df.shape)
print("dilution values:\n", df["dilution"].value_counts())
print("smell values:\n", df["smell"].value_counts(dropna=False))
print("know values:\n", df["know"].value_counts(dropna=False))
print("subjects:", df["subject"].nunique(), " rows per subject:", df.groupby("subject").size().describe()[["min", "max"]].tolist())
print("vials:", df["vial"].nunique())
# non-numeric CIDs
bad = df[~df["cid_raw"].str.fullmatch(r"\d+")]
print("non-numeric CID rows:", len(bad))
print(bad.groupby(["cid_raw", "odor", "cas"]).size())
print("unique cid_raw:", df["cid_raw"].nunique(), " unique odor names:", df["odor"].nunique(), "unique CAS:", df["cas"].nunique())
# names with replicate
rep = df[df["odor"].str.contains("replic", case=False)]
print("rows with 'replic' in name:", len(rep), " unique names:", rep["odor"].nunique())
print(sorted(rep["odor"].unique()))
# cid -> names
g = df.groupby("cid_raw")["odor"].unique()
multi = g[g.map(len) > 1]
print("CIDs with more than one name:", len(multi))
for k, v in multi.items():
    print("  ", k, list(v))
# name -> cids
g2 = df.groupby("odor")["cid_raw"].unique()
print("names with more than one CID:", (g2.map(len) > 1).sum())
# vials per cid x dilution
vc = df.groupby(["cid_raw", "dilution"])["vial"].nunique().unstack()
print("vials per (cid,dilution) table - distribution of number of dilutions per CID:")
print(vc.notna().sum(axis=1).value_counts())
print("distribution of total vials per CID:")
print(vc.sum(axis=1).value_counts())
print("examples with >2 vials:")
print(vc[vc.sum(axis=1) > 2])
# pairs of dilutions
pairs = vc.notna().apply(lambda r: tuple(c for c in vc.columns if r[c]), axis=1)
print("dilution pairs:\n", pairs.value_counts())
# ratings blanks
sm = df["smell"] == "I smell something"
for c in ["STRENGTH", "PLEASANT", "FAMILIAR"] + WORDS:
    v = df[c]
    blank = (v == "")
    num = pd.to_numeric(v, errors="coerce")
    print(f"{c:10s} blank|smelled={blank[sm].sum():6d} blank|not={blank[~sm].sum():6d} filled|not={(~blank[~sm]).sum():5d}"
          f" zeros={int((num == 0).sum()):5d} min={num.min()} max={num.max()} nonnum={(num.isna() & ~blank).sum()}")
# number of word sliders touched per smelled row
touched = (df.loc[sm, WORDS] != "").sum(axis=1)
print("number of word sliders touched per smelled row:\n", touched.value_counts().sort_index())
print("ownwords top:", df["ownwords"].value_counts().head(5).to_dict())
# properties
print("prop shape", prop.shape, "unique CID", prop["CID"].nunique())
cids = set(df["cid_raw"].replace({"109-19-0": "8038", "3796-70-1": "1549778"}))
print("cids in data:", len(cids), " missing from properties:", sorted(cids - set(prop["CID"])), " extra in properties:", sorted(set(prop["CID"]) - cids))
print(prop.head())
print("prop NaN SMILES:", prop["SMILES"].isna().sum())
# check the two typed CIDs
print(prop[prop["CID"].isin(["8038", "1549778"])])
# age / gender
print(df.drop_duplicates("subject")[["gender", "race", "ethnicity"]].value_counts().head(10))
