"""The whole size series at rest, both recipes for placing the evenly spaced tempos, from the saved results.   usage: python series.py > series.out"""
import json, numpy as np
rng = np.random.default_rng(0)
L = json.load(open('long.json'))['sizes']; S6 = json.load(open('long6.json'))
def ld(name): return json.load(open(name))
def style(J): Q = np.array(J['eighths']); x = (Q[:, 5] + Q[:, 7]) / 2; return x
def pool(old, x):
    n0, n1 = old['runs'], len(x); r = (old['r'] * n0 + x.sum()) / (n0 + n1)
    return r, float(np.sqrt((old['sd'] ** 2 * (n0 - 1) + x.var(ddof=1) * (n1 - 1)) / (n0 + n1 - 2) / (n0 + n1)))
# my recipe, tempos at (i - 1/2)/N
half = [(q['N'], q['r'], q['sd'] / np.sqrt(q['runs'])) for q in L[:5]]
half.append((3200,) + pool(L[5], style(ld('long4-N3200.json')))); half.append((6400,) + pool(L[6], style(ld('long4-N6400.json'))))
for N in (12800, 25600): J = ld(f'long4-N{N}.json'); half.append((N, J['last_quarter'], J['se']))
# the other recipe, tempos at i/(N + 1)
plus = [(q['N'], q['mean_r'], q['se']) for q in S6 if q['recipe'] == 'plus']
for N in (3200, 6400): x = style(ld(f'long4-plus-N{N}.json')); plus.append((N, float(x.mean()), float(x.std(ddof=1) / np.sqrt(len(x)))))
J = ld('long4-plus-N12800.json'); plus.append((12800, J['last_quarter'], J['se']))
def fit(rows, name):
    n = np.array([a for a, _, _ in rows]); r = np.array([b for _, b, _ in rows]); se = np.array([c for _, _, c in rows])
    bs = np.array([np.polyfit(np.log(n), np.log(rng.normal(r, se)), 1)[0] for _ in range(4000)])
    w = 1 / (se / r) ** 2; X, Y = np.log(n), np.log(r); xm, ym = (w * X).sum() / w.sum(), (w * Y).sum() / w.sum(); bw = (w * (X - xm) * (Y - ym)).sum() / (w * (X - xm) ** 2).sum(); chi = (w * (Y - ym - bw * (X - xm)) ** 2).sum()
    print(f"{name}:"); print("   sizes:  " + ", ".join(f"{int(a):,}" for a in n)); print("   levels: " + ", ".join(f"{b:.4f}" for b in r)); print("   standard errors: " + ", ".join(f"{c:.4f}" for c in se))
    print(f"   slope {np.polyfit(X, Y, 1)[0]:+.4f} (sd {bs.std():.4f}; 95% {np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}); weighted {bw:+.4f}; chi-square of one power law {chi:.1f} on {len(n) - 2} degrees of freedom")
    print("   between neighbouring sizes: " + ", ".join(f"{np.log(b / a) / np.log(2):+.2f}" for a, b in zip(r, r[1:])))
    for lo, hi in ((0, 5), (3, len(n))): print(f"   sizes {int(n[lo]):,} to {int(n[hi - 1]):,} alone: {np.polyfit(X[lo:hi], Y[lo:hi], 1)[0]:+.3f}")
    return n, r, se
nh, rh, sh = fit(half, "my recipe, tempos at the quantiles (i - 1/2)/N"); npl, rp, sp = fit(plus, "the other recipe, tempos at the quantiles i/(N + 1)")
k = len(npl); print("the other recipe's level over mine, by size: " + ", ".join(f"{int(a):,}: {b / c:.3f}" for a, b, c in zip(npl, rp, rh[:k])))
print(f"   at 12,800: {rp[-1] / rh[k - 1]:.3f}, with a standard error of about {rp[-1] / rh[k - 1] * np.sqrt((sp[-1] / rp[-1]) ** 2 + (sh[k - 1] / rh[k - 1]) ** 2):.3f}")
print(f"the same eight sizes, 100 to 12,800: my recipe {np.polyfit(np.log(nh[:k]), np.log(rh[:k]), 1)[0]:+.4f}; the other {np.polyfit(np.log(npl), np.log(rp), 1)[0]:+.4f}")
