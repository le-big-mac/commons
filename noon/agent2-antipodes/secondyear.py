"""Score the expectations for a second year (expectations-2024.md).   usage: python -I secondyear.py pairs.npz pairs-2024.npz"""
import sys, datetime
import numpy as np


def summary(path):
    m = np.load(path)
    c = m['counts']
    when = [datetime.datetime(1800, 1, 1) + datetime.timedelta(hours=float(h)) for h in m['time']]
    month = np.array([w.month for w in when])
    hour = np.array([w.hour for w in when])
    return c, when, np.array([c[month == k].mean() for k in range(1, 13)]), np.array([c[hour == h].mean() for h in (0, 6, 12, 18)])


c25, w25, m25, h25 = summary(sys.argv[1])
c24, w24, m24, h24 = summary(sys.argv[2])
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
print(f"F1  times {len(c24)}; even counts: {int((c24 % 2 == 0).sum())}")
print(f"F2  mean {c24.mean():.2f} (2025: {c25.mean():.2f}); median {np.median(c24):.0f}; range {c24.min()} to {c24.max()}")
print("F3  monthly means 2024:", " ".join(f"{n} {x:.1f}" for n, x in zip(names, m24)))
print("    monthly means 2025:", " ".join(f"{n} {x:.1f}" for n, x in zip(names, m25)))
order = np.argsort(m24)
print("    two lowest months of 2024:", [names[k] for k in order[:2]], "; three highest:", [names[k] for k in order[::-1][:3]])
print(f"    correlation of the twelve monthly means, 2024 against 2025: {np.corrcoef(m24, m25)[0, 1]:.3f}")
print("F4  mean count at 00, 06, 12, 18 UTC, 2024:", [round(float(x), 1) for x in h24], " 2025:", [round(float(x), 1) for x in h25])
k = int(np.argmin(c24))
print(f"F5  fewest pairs in 2024: {c24[k]} on {w24[k]:%d %B %Y, %H} UTC; all times with that count: {[f'{w24[j]:%d %b %H}' for j in np.nonzero(c24 == c24.min())[0]]}")
k = int(np.argmax(c24))
print(f"    most pairs in 2024: {c24[k]} on {w24[k]:%d %B %Y, %H} UTC")
