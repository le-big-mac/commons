"""Score the expectations for the finer grid (expectations-finer.md).   usage: python -I finerscore.py finer-1980.npz pairs.npz"""
import sys, datetime
import numpy as np
m = np.load(sys.argv[1])
counts, strides = m['counts'], m['strides'].tolist()
when = [datetime.datetime(1800, 1, 1) + datetime.timedelta(hours=float(h)) for h in m['time']]
print(f"20CRv3 (ensemble mean of 80), {when[0]:%d %b %Y %H} UTC to {when[-1]:%d %b %Y %H} UTC, {len(when)} three-hourly fields")
mean = {k: counts[:, j].mean() for j, k in enumerate(strides)}
print("G1  even counts at strides", strides, ":", [int((counts[:, j] % 2 == 0).sum()) for j in range(len(strides))])
print(f"G2  mean count at 5 degrees: {mean[5]:.2f}  (expected between 20.5 and 30.7; NCEP/NCAR 2025 on its 5-degree grid: 25.6)")
print(f"G3  mean at 1 degree / mean at 5 degrees: {mean[1]:.2f} / {mean[5]:.2f} = {mean[1] / mean[5]:.2f}  (expected between 2.5 and 4.5)")
print(f"G4  mean at 2 degrees / mean at 5 degrees: {mean[2]:.2f} / {mean[5]:.2f} = {mean[2] / mean[5]:.2f}  (expected between 1.6 and 2.2)")
month = np.array([w.month for w in when])
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
m80 = np.array([counts[month == k, 0].mean() for k in range(1, 13)])
n = np.load(sys.argv[2])
wn = [datetime.datetime(1800, 1, 1) + datetime.timedelta(hours=float(h)) for h in n['time']]
mn = np.array([n['counts'][np.array([w.month for w in wn]) == k].mean() for k in range(1, 13)])
order = np.argsort(m80)
print("G5  monthly means at 1 degree, 1980:", " ".join(f"{a} {x:.1f}" for a, x in zip(names, m80)))
print("    two lowest months:", [names[k] for k in order[:2]], "; three highest:", [names[k] for k in order[::-1][:3]],
      f"; correlation with the monthly means of NCEP/NCAR 2025: {np.corrcoef(m80, mn)[0, 1]:.3f}")
print("the count against the grid step:")
ks = sorted(strides, reverse=True)
for a, b in zip(ks[:-1], ks[1:]):
    print(f"    {a:2d} -> {b:2d} degrees: {mean[a]:6.2f} -> {mean[b]:6.2f}, local exponent {np.log(mean[b] / mean[a]) / np.log(a / b):.2f}")
hour = np.array([w.hour for w in when])
print("mean count at 1 degree by hour (UTC):", {int(h): round(float(counts[hour == h, 0].mean()), 1) for h in sorted(set(hour.tolist()))})
