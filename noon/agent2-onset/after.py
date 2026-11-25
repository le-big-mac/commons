"""After the referee: its checks redone with my own lines.   usage: python after.py > after.out"""
import json, math, re
import numpy as np
from scipy.special import wofz
from scipy.integrate import quad
rng = np.random.default_rng(0)
S = json.load(open('sheet.json')); RA = json.load(open('sizes-random.json'))['sizes']; RE = json.load(open('sizes-regular.json'))['sizes']
C = json.load(open('curves.json')); V = json.load(open('results.json')); F = json.load(open('forecast/scored.json'))

print("1. Fluctuations below the onset: the referee's formula, N x mean r^2 = integral of g(w) / |1 - K w(x)|^2, x = w / (sigma sqrt 2), w(.) the Faddeeva function (for this Gaussian)")
sig = math.sqrt(math.pi / 8); g = lambda w: math.exp(-w * w / (2 * sig * sig)) / (sig * math.sqrt(2 * math.pi))
for K in (0.0, 0.25, 0.5, 0.75):
    val = quad(lambda w: g(w) / abs(1 - K * wofz(w / (sig * math.sqrt(2)))) ** 2, -8, 8, limit=400)[0]
    print(f"   K = {K}: {val:.3f}   (1/(1 - K) = {1 / (1 - K):.3f})")
print("   for a Lorentzian the same integral, g(w) / |1 - K (1/2) / (1/2 - i w)|^2, gives: " + ", ".join(f"{quad(lambda w: (0.5 / math.pi / (w * w + 0.25)) / abs(1 - K * 0.5 / (0.5 - 1j * w)) ** 2, -np.inf, np.inf, limit=400)[0]:.3f} at K = {K}" for K in (0.25, 0.5, 0.75)))

print("2. The slope at the onset with random tempos: resampling the runs within each size, 4000 times")
def slopes(rows, keep=slice(None)):
    out = []
    for _ in range(4000):
        m = [np.mean(rng.choice(q['each'], len(q['each']))) for q in rows[keep]]
        out.append(np.polyfit(np.log([q['N'] for q in rows[keep]]), np.log(m), 1)[0])
    return np.array(out)
b = slopes(RA); print(f"   eight sizes: {np.polyfit(np.log([q['N'] for q in RA]), np.log([q['r'] for q in RA]), 1)[0]:+.3f}, sd {b.std():.3f}, 95% from {np.percentile(b, 2.5):+.3f} to {np.percentile(b, 97.5):+.3f}; share of resamples outside the sealed range (-0.26 to -0.14): {np.mean((b < -0.26) | (b > -0.14)):.2f}")
b6 = slopes(RA, slice(0, 6)); print(f"   six sizes to 3,200: {np.polyfit(np.log([q['N'] for q in RA[:6]]), np.log([q['r'] for q in RA[:6]]), 1)[0]:+.3f}, sd {b6.std():.3f}")
print("   slopes between neighbouring sizes: " + ", ".join(f"{math.log(b_['r'] / a['r']) / math.log(2):+.2f}" for a, b_ in zip(RA, RA[1:])))
for q in RA[-2:]:
    e = np.array(q['each']); print(f"   N = {q['N']}: {len(e)} runs, {np.mean(e < 0.08):.2f} of them read below 0.08; the lowest reads {e.min():.4f}")
print(f"   lowest single run at any size, random tempos: {min(min(q['each']) for q in RA):.4f}; evenly spaced at 800 and up read {', '.join(f'{q[chr(114)]:.4f}' for q in RE[3:])}")

print("3. The sweep with a uniform spread, the two legs side by side")
up = {s['K']: s['r'] for s in S['sweep'] if s['leg'] == 'up'}; down = {s['K']: s['r'] for s in S['sweep'] if s['leg'] == 'down'}
for K in (0.8, 0.9, 0.96, 0.98, 1.0, 1.02):
    print(f"   K = {K:.2f}: up {up[K]:.4f}, down {down.get(K, float('nan')):.4f}")

print("4. The rise times: resampling the 20 runs at each K")
t = {q['K']: np.array(q['times']) for q in S['rise']}
rat = np.array([np.median(rng.choice(t[1.2], 20)) / np.median(rng.choice(t[2.0], 20)) for _ in range(4000)])
print(f"   ratio of medians {np.median(t[1.2]) / np.median(t[2.0]):.2f}; share of resamples below 3: {np.mean(rat < 3):.3f}")

print("5. My odds against the forecasters', looked at three more ways")
y = np.array(F['outcome']); me = np.array(F['mine']); med = np.array(F['median']); ids = F['ids']
brier = lambda p, yy=y: float(((p - yy) ** 2).mean())
shift = med.mean() - me.mean()
print(f"   mine {brier(me):.4f}, theirs {brier(med):.4f}; my odds moved up by {shift:.3f} (to their mean) and capped at 0.99: {brier(np.minimum(me + shift, 0.99)):.4f}; their mean on every line: {brier(np.full(10, med.mean())):.4f}")
print(f"   share of the forecasters' score that is O7: {((med - y) ** 2)[ids.index('O7')] / ((med - y) ** 2).sum():.2f}; of mine: {((me - y) ** 2)[ids.index('O7')] / ((me - y) ** 2).sum():.2f}")
for k in ('O4', 'O5', 'O6', 'O10'):
    yy = y.copy(); yy[ids.index(k)] = 0
    print(f"   had {k} failed as well: mine {brier(me, yy):.3f}, theirs {brier(med, yy):.3f}")
sheet = open('forecast/sheet.md').read(); print(f"   remarks of mine that stayed on the forecasters' sheet: {len(re.findall(r'Marked down', sheet))} beginning 'Marked down', {len(re.findall(r'[(]I believe', sheet))} beginning 'I believe'")

print("6. The simulated curves against the limit (41 couplings, 2,000 evenly spaced)")
for sh in ('lorentz', 'gauss', 'uniform'):
    th = dict((round(k, 3), v) for k, v in C['theory'][sh]); pts = [p for p in C['curves'] if p['shape'] == sh]
    hi = max(abs(p['r'] - th[round(p['K'], 3)]) for p in pts if p['K'] >= 1.05); lo = [p['r'] for p in pts if p['K'] < 1]
    print(f"   {sh}: largest gap for K of 1.05 or more {hi:.4f}; below 1 the simulation reads {min(lo):.3f} to {max(lo):.3f} where the limit is 0")

print("7. The longer run (long.json): evenly spaced tempos at K = 1, read at rest")
L = json.load(open('long.json'))['sizes']
N = np.array([q['N'] for q in L]); r = np.array([q['r'] for q in L]); se = np.array([q['sd'] / math.sqrt(q['runs']) for q in L])
bs = np.array([np.polyfit(np.log(N), np.log(rng.normal(r, se)), 1)[0] for _ in range(4000)])
print(f"   slope {np.polyfit(np.log(N), np.log(r), 1)[0]:+.3f}, sd {bs.std():.3f} (each mean redrawn within its standard error), 95% from {np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}")
print("   between neighbouring sizes: " + ", ".join(f"{math.log(b_ / a) / math.log(2):+.2f}" for a, b_ in zip(r, r[1:])))
for q, e in zip(L, RE):
    a, b_ = q['quarters'][2], q['quarters'][3]
    print(f"   N = {q['N']:5d}: at rest {q['r']:.4f} +- {q['sd'] / math.sqrt(q['runs']):.4f}; third and fourth quarters {a:.4f}, {b_:.4f}, apart by {abs(a - b_) / ((a + b_) / 2):.1%} of their mean ({abs(a - b_) / max(a, b_):.1%} of the larger); the 600-unit recipe read {e['r']:.4f}")
