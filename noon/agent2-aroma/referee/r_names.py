"""Referee: list every molecule's name in the sheet beside PubChem's formula and IUPAC name, to read by eye.
usage: python -I r_names.py tidy.csv properties.csv > names.out"""
import sys
import pandas as pd

raw = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
raw["cid"] = raw["cid_raw"].replace({"109-19-0": "8038", "3796-70-1": "1549778"}).astype(int)
raw = raw[~raw["odor"].str.contains("replicate", case=False)].drop_duplicates("cid").set_index("cid")
prop = pd.read_csv(sys.argv[2]).set_index("CID")
for cid in sorted(raw.index):
    print(f"{cid}|{raw.loc[cid, 'odor'][:34]}|{raw.loc[cid, 'catno'][:8]}|{prop.loc[cid, 'MolecularFormula']}|{str(prop.loc[cid, 'IUPACName'])[:58]}")
