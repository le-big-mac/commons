"""Score the expectations for the sharp fine analysis (expectations-sharp.md).   usage: python -I sharpscore.py sharp-2025.npz pairs.npz"""
import sys, datetime
import numpy as np
m = np.load(sys.argv[1])
counts, strides, stamps, land = m['counts'], m['strides'].tolist(), m['stamps'].tolist(), m['land'].astype(int)
mean = {k: counts[:, j].mean() for j, k in enumerate(strides)}
n = np.load(sys.argv[2])
wn = [datetime.datetime(1800, 1, 1) + datetime.timedelta(hours=float(h)) for h in n['time']]
idx = {w.strftime('%Y%m%d%H'): i for i, w in enumerate(wn)}
ncep = np.array([n['counts'][idx[s]] for s in stamps])
print(f"GFS analysis, 0.25 degrees, {len(stamps)} times of 2025 ({stamps[0]} to {stamps[-1]})")
print("H1  even counts at strides", strides, ":", [int((counts[:, j] % 2 == 0).sum()) for j in range(len(strides))])
g10 = counts[:, strides.index(10)]
print(f"H2  mean at 2.5 degrees (stride 10): {g10.mean():.2f}; NCEP/NCAR on the same times: {ncep.mean():.2f}; ratio {g10.mean() / ncep.mean():.2f}  (expected 1.0 to 1.6);"
      f" correlation across the times: {np.corrcoef(g10, ncep)[0, 1]:.2f}  (expected 0.6 or more)")
print(f"H3  mean at 0.25 degrees / mean at 1 degree: {mean[1]:.2f} / {mean[4]:.2f} = {mean[1] / mean[4]:.2f}  (expected 1.2 to 2.2)")


def land_share(recs):
    la, lo = recs[:, 1], recs[:, 2]
    north = la > 0
    i = np.rint((90 - la[north]) / 0.25).astype(int)
    j = np.rint(lo[north] / 0.25).astype(int) % 1440
    here, there = land[i, j], land[720 - i, (j + 720) % 1440]
    return ((here | there).mean(), (here & there).mean(), ((1 - here) & (1 - there)).mean(), int(north.sum()))


s1, s10 = land_share(m['recs1']), land_share(m['recs10'])
w = np.cos(np.radians(np.linspace(90, -90, 721)))[:, None] * np.ones((1, 1440))
w /= w.sum()
anti = np.roll(land[::-1], 720, axis=1)
print(f"H4  share of pairs with at least one end on land: at 0.25 degrees {100 * s1[0]:.1f}% of {s1[3]} pairs; at 2.5 degrees {100 * s10[0]:.1f}% of {s10[3]} pairs;"
      f" difference {100 * (s1[0] - s10[0]):+.1f} points  (expected +5 or more).  Share of the globe where that holds: {100 * (w * (land | anti)).sum():.1f}%")
print(f"    both ends on land: {100 * s1[1]:.1f}% at 0.25 degrees, {100 * s10[1]:.1f}% at 2.5 degrees (globe: {100 * (w * (land & anti)).sum():.1f}%);"
      f" both at sea: {100 * s1[2]:.1f}% and {100 * s10[2]:.1f}% (globe: {100 * (w * ((1 - land) & (1 - anti))).sum():.1f}%)")
print(f"H5  mean count at 0.25 degrees: {mean[1]:.2f}  (expected 50 to 150); median {np.median(counts[:, 0]):.0f}, min {counts[:, 0].min()}, max {counts[:, 0].max()}")
print("the count against the grid step:")
ks = sorted(strides, reverse=True)
for a, b in zip(ks[:-1], ks[1:]):
    print(f"    {0.25 * a:5.2f} -> {0.25 * b:5.2f} degrees: {mean[a]:7.2f} -> {mean[b]:7.2f}, local exponent {np.log(mean[b] / mean[a]) / np.log(a / b):.2f}")
month = np.array([int(s[4:6]) for s in stamps])
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
for k in (1, 4, 10):
    print(f"monthly means (6 fields each) at {0.25 * k:g} degrees:", " ".join(f"{a} {counts[month == q, strides.index(k)].mean():.0f}" for q, a in enumerate(names, 1)))
print("NCEP/NCAR 2.5 degrees, the same 72 times:  ", " ".join(f"{a} {ncep[month == q].mean():.0f}" for q, a in enumerate(names, 1)))
print("correlation across the 72 times of the 0.25-degree count with the 2.5-degree (stride 10) count:", round(float(np.corrcoef(counts[:, 0], g10)[0, 1]), 2))
# where the extra pairs are: latitude bands
for name, recs in (("0.25 degrees", m['recs1']), ("2.5 degrees", m['recs10'])):
    al = recs[recs[:, 1] > 0, 1]
    h, _ = np.histogram(al, [0, 20, 40, 60, 90])
    print(f"pairs by latitude of their ends, {name}: 0-20: {100 * h[0] / len(al):.0f}%, 20-40: {100 * h[1] / len(al):.0f}%, 40-60: {100 * h[2] / len(al):.0f}%, 60-90: {100 * h[3] / len(al):.0f}%")
