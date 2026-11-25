"""slabs.py: what is kept of one slab of one window (the mean depth of each column's points in a slab 4 thick): how spread, how
skewed, how peaked the column means are, and how different two columns j apart are. study.py uses it on the raw files of slabs
(cell2 -snap); reduce.py writes the same things to small files, which study.py reads when the raw files are not there."""
import numpy as np
ALL_LAGS = (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048, 3072, 4096)
def lags_for(ncol): return [j for j in ALL_LAGS if j <= ncol // 4]
def slabstats(row, lags):
    """row: the column means of one slab (not-a-number where a column had no point). The window is a ring."""
    z = row[~np.isnan(row)]; z = z - z.mean(); v = (z ** 2).mean(); g = []; n = []
    for j in lags:
        d = (np.roll(row, -j) - row) ** 2; ok = ~np.isnan(d); g.append(float(d[ok].sum())); n.append(int(ok.sum()))
    return {'v': float(v), 'sk': float((z ** 3).mean() / v ** 1.5), 'ku': float((z ** 4).mean() / v ** 2 - 3), 'g': g, 'n': n, 'cols': int(len(z))}
