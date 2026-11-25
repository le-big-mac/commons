"""Referee's own loader. Reads the Keller 2016 sheet and writes a tidy CSV cache in the referee folder.
usage: python -I r_load.py keller2016.xlsx out.csv
"""
import sys
import pandas as pd
import numpy as np

WORDS = ["EDIBLE", "BAKERY", "SWEET", "FRUIT", "FISH", "GARLIC", "SPICES", "COLD", "SOUR", "BURNT", "ACID",
         "WARM", "MUSKY", "SWEATY", "AMMONIA", "DECAYED", "WOOD", "GRASS", "FLOWER", "CHEMICAL"]
COLS = ["cas", "catno", "cid_raw", "odor", "dilution", "subject", "subject_dream", "gender", "race", "ethnicity",
        "age", "vial", "smell", "know", "ownwords", "STRENGTH", "PLEASANT", "FAMILIAR"] + WORDS


def main():
    src, out = sys.argv[1], sys.argv[2]
    raw = pd.read_excel(src, sheet_name="data", header=None, dtype=object)
    print("raw shape", raw.shape)
    for i in range(4):
        print("row", i, list(raw.iloc[i].values))
    hdr = list(raw.iloc[2].values)
    print("n header cols", len(hdr))
    df = raw.iloc[3:].reset_index(drop=True)
    assert df.shape[1] == len(COLS), (df.shape, len(COLS))
    # check the header order against my names
    for h, c in zip(hdr, COLS):
        print(f"  {c:14s} <- {h!r}")
    df.columns = COLS
    df.to_csv(out, index=False)
    print("written", out, df.shape)


if __name__ == "__main__":
    main()
