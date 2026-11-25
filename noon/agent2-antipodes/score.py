"""Score the expectations written down before the computation (expectations.md) against pairs.npz.

usage: python -I score.py pairs.npz LAND.nc seeds/s1.npz seeds/s2.npz ...
"""
import sys
import numpy as np
import h5py

main = np.load(sys.argv[1])
counts, recs, lat, lon = main['counts'], main['recs'], main['lat'], main['lon']
with h5py.File(sys.argv[2], 'r') as f:
    land = f['land'][0].astype(int)                                     # (73, 144), 1 = land
others = [np.load(a)['counts'] for a in sys.argv[3:]]
nt = len(counts)

print("E1  parity")
print(f"    times {nt}; even counts with the main tie-breaking: {int((counts % 2 == 0).sum())};"
      f" with {len(others)} other tie-breakings: {[int((c % 2 == 0).sum()) for c in others]}")

allc = np.array([counts] + others)
spread = allc.max(0) - allc.min(0)
print("    tie-breaking: times at which the", len(allc), "runs do not all give the same count:", int((spread > 0).sum()),
      f"({100 * (spread > 0).mean():.1f}%); spread 2: {int((spread == 2).sum())}, 4: {int((spread == 4).sum())}, more: {int((spread > 4).sum())}")
print("    medians of the runs:", [float(np.median(c)) for c in allc], " means:", [round(float(c.mean()), 2) for c in allc])

print("E2  how many")
q = np.percentile(counts, [5, 25, 50, 75, 95])
print(f"    min {counts.min()}, 5% {q[0]:.0f}, quartile {q[1]:.0f}, median {q[2]:.0f}, quartile {q[3]:.0f}, 95% {q[4]:.0f}, max {counts.max()}, mean {counts.mean():.2f}")
print(f"    share of times with between 3 and 13 pairs: {100 * ((counts >= 3) & (counts <= 13)).mean():.1f}%;  with exactly 1: {100 * (counts == 1).mean():.1f}%")
smallest = np.argsort(counts)[:5]
print("    the five smallest counts are at time indices", smallest.tolist(), "with", counts[smallest].tolist())

print("E3  where (latitude)")
north = recs[recs[:, 1] > 0]                                            # one member of each pair (the northern one)
assert len(north) == counts.sum(), (len(north), counts.sum())
al = north[:, 1]
print(f"    pairs in all: {len(north)};  within 40 degrees of the equator: {100 * (al < 40).mean():.1f}%"
      f"  (share of the sphere's area there: {100 * np.sin(np.radians(40)):.1f}%)")
edges = np.arange(0, 91, 10)
h, _ = np.histogram(al, edges)
area = np.diff(np.sin(np.radians(edges)))
for a, b, n, w in zip(edges[:-1], edges[1:], h, area):
    print(f"    {a:2d}-{b:2d}: {100 * n / len(al):5.1f}% of pairs, {100 * w:5.1f}% of area, ratio {n / len(al) / w:4.2f}")

print("E4  land and sea")
i = np.rint((90 - north[:, 1]) / 2.5).astype(int)
j = np.rint(north[:, 2] / 2.5).astype(int) % 144
here = land[i, j]
there = land[72 - i, (j + 72) % 144]
both_land, both_sea = (here & there).mean(), ((1 - here) & (1 - there)).mean()
w = np.cos(np.radians(lat))[:, None] * np.ones((1, 144))
w[0] = w[-1] = 0
w /= w.sum()
anti = np.roll(land[::-1], 72, axis=1)
base_ll, base_ss = (w * (land & anti)).sum(), (w * ((1 - land) & (1 - anti))).sum()
print(f"    both points on land: {100 * both_land:.1f}% of pairs (share of the sphere where that holds: {100 * base_ll:.1f}%)")
print(f"    both at sea:         {100 * both_sea:.1f}% of pairs (share of the sphere: {100 * base_ss:.1f}%)")
print(f"    one of each:         {100 * (1 - both_land - both_sea):.1f}% of pairs (share of the sphere: {100 * (1 - base_ll - base_ss):.1f}%)")
print(f"    land share of the grid: {100 * (w * land).sum():.1f}%")

print("E5  change from one six-hour field to the next")
d = np.diff(counts)
ch = d != 0
print(f"    steps: {len(d)}; the count changes at {int(ch.sum())} ({100 * ch.mean():.1f}%)")
vals, n = np.unique(np.abs(d[ch]), return_counts=True)
print("    size of the change:", {int(v): int(k) for v, k in zip(vals, n)})
print(f"    by exactly 2: {100 * (np.abs(d[ch]) == 2).mean():.1f}% of the changes")
print(f"    correlation of the count with the count 6 h, 24 h, 5 days, 30 days later:",
      [round(float(np.corrcoef(counts[:-k], counts[k:])[0, 1]), 2) for k in (1, 4, 20, 120)])
print("    by month (mean count):", [round(float(counts[(np.arange(nt) // 4 >= a) & (np.arange(nt) // 4 < b)].mean()), 1)
                                     for a, b in zip(np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]), np.cumsum([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]))])
print("    by hour (mean count at 00, 06, 12, 18 UTC):", [round(float(counts[k::4].mean()), 1) for k in range(4)])
