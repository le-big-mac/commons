"""Referee loader: builds one row per battle. Data paths passed in; nothing in the data dir is executed."""
import sys
import numpy as np
import pandas as pd


def num(s):
    return pd.to_numeric(s, errors="coerce")


def load(d, strcol="str"):
    b = pd.read_csv(f"{d}/battles.csv", dtype=str, keep_default_na=False)
    g = pd.read_csv(f"{d}/belligerents.csv", dtype=str, keep_default_na=False)
    t = pd.read_csv(f"{d}/battle_durations.csv", dtype=str, keep_default_na=False)
    b["isqno"] = b["isqno"].astype(int)
    g["isqno"] = g["isqno"].astype(int)
    t["isqno"] = t["isqno"].astype(int)
    assert b["isqno"].is_unique and t["isqno"].is_unique
    for c in ["str", "intst", "cas"]:
        g[c + "_n"] = num(g[c])
    g["attacker"] = g["attacker"].astype(int)
    cnt = g.groupby(["isqno", "attacker"]).size()
    assert cnt.max() == 1, "more than one row per battle-side"
    a = g[g.attacker == 1].set_index("isqno")
    dfn = g[g.attacker == 0].set_index("isqno")
    df = b.set_index("isqno")
    df["wina_n"] = num(df["wina"])
    df["surpa_n"] = num(df["surpa"])
    for c in ["str", "intst", "cas"]:
        df["a_" + c] = a[c + "_n"].reindex(df.index)
        df["d_" + c] = dfn[c + "_n"].reindex(df.index)
    tt = t.set_index("isqno")
    df["dt"] = tt["datetime_min"].reindex(df.index)
    df["year"] = num(df["dt"].str.slice(0, 4))
    df["dur"] = num(tt["duration1"].reindex(df.index))
    df["a_s"] = df["a_" + strcol]
    df["d_s"] = df["d_" + strcol]
    ok = (df.a_s > 0) & (df.d_s > 0)
    df["fr"] = np.where(ok, df.a_s / df.d_s, np.nan)
    df["a_cs"] = np.where((df.a_s > 0) & df.a_cas.notna(), df.a_cas / df.a_s, np.nan)
    df["d_cs"] = np.where((df.d_s > 0) & df.d_cas.notna(), df.d_cas / df.d_s, np.nan)
    df["dec"] = df.wina_n.isin([1, -1])
    df["aw"] = np.where(df.dec, (df.wina_n == 1).astype(float), np.nan)
    return df


if __name__ == "__main__":
    df = load(sys.argv[1])
    print(len(df))
    print(df.wina.value_counts(dropna=False))
    print(df.surpa.value_counts(dropna=False))
    print(df.post1.value_counts(dropna=False))
    print(df.post2.value_counts(dropna=False))
    print(df[["a_str", "d_str", "a_intst", "d_intst", "a_cas", "d_cas", "year", "dur"]].describe().T)
    print(df.year.isna().sum(), df.dur.isna().sum())
