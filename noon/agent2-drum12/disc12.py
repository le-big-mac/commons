"""Lines T6 and T7 of the sealed sheet: the best one even disc for twelve modes, by exact Bessel matching, and my ruler D.
usage: python -u disc12.py disc12.json"""
import sys, json, math
sys.path.insert(0, "../drum")
import numpy as np
from scipy.optimize import minimize
import drum, lib12 as L
T12 = [L.target(m, n) for m, n in L.TWELVE]
def miss(s, k, which=L.TWELVE, T=T12):
    w = drum.modes(float(s), float(k), which); return max(abs(w[i] / w[0] / T[i] - 1) for i in range(1, len(which)))
def fine_disc(s, k, N=2000):
    """the disc as loads on N thin rings (the ring the edge cuts takes its share by area), for the struck-skin model"""
    e = np.arange(N + 1) / N; return (s - 1) * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / (e[1:] ** 2 - e[:-1] ** 2), 0, 1)
out = {}
print(f"the best nine-mode disc (9.938 over 0.4004): largest miss over nine modes {100 * miss(9.938, 0.4004, L.NINE, T12[:9]):.3f}%, over twelve {100 * miss(9.938, 0.4004):.3f}%", flush=True)
S = np.exp(np.linspace(0, math.log(60), 30)); K = np.arange(0.05, 0.951, 0.025); grid = [(miss(s, k), s, k) for s in S for k in K]; grid.sort(); best = None
for t, s, k in grid[:6]:
    r = minimize(lambda x: miss(min(60, max(1, x[0])), min(0.95, max(0.05, x[1]))), [s, k], method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=400)); s1, k1 = min(60, max(1, r.x[0])), min(0.95, max(0.05, r.x[1]))
    if best is None or r.fun < best[0]: best = (float(r.fun), float(s1), float(k1))
t, s, k = best; w = drum.modes(s, k, L.TWELVE); ratios = [x / w[0] for x in w]; out['T6'] = dict(miss=t, s=s, k=k, ratios=ratios, mass=(s - 1) * k * k)
print(f"T6. the best one even disc for twelve modes: {s:.3f} times the skin over {k:.4f} of the radius (added mass {(s - 1) * k * k:.2f}); largest miss {100 * t:.3f}%; ratios " + ", ".join(f"{x:.4f}" for x in ratios) + f"; the six best grid points ran from {100 * grid[0][0]:.2f}% to {100 * grid[5][0]:.2f}%", flush=True)
nine_ring = np.array(json.load(open("../drum/rings2-free-1.43.json"))['rings']['40']['a']); walk = None
for r in json.load(open("../drum/chain-free-up.json")):
    if abs(r['weight'] - 1.43) < 1e-9: walk = np.array(r['a'])
out['T7'] = dict(disc=L.D(fine_disc(9.938, 0.4004), per=1), ringed=L.D(walk), ringed_rings2=L.D(nine_ring), plain=L.D(np.zeros(40)), disc12=L.D(fine_disc(s, k), per=1))
print(f"T7. D, the weighted distance of the struck skin's partials from whole multiples: the best nine-mode disc {out['T7']['disc']:.1f} cents; the nine-mode ringed load of drum2.mp3 {out['T7']['ringed']:.1f} cents (the later 40-ring load of rings2.py: {out['T7']['ringed_rings2']:.1f}); a plain skin {out['T7']['plain']:.1f}; the best twelve-mode disc {out['T7']['disc12']:.1f}")
for name, load, per in (("the nine-mode disc", fine_disc(9.938, 0.4004), 1), ("the ringed load of drum2.mp3", walk, 50)):
    P = L.struck(load, per=per); tot = sum(p['strength'] ** 2 * (1.3 * p['ratio'] ** -0.8) * (1 - math.exp(-1.2 / (1.3 * p['ratio'] ** -0.8))) for p in P)
    print(f"   {name}: " + "; ".join(f"({p['m']},{p['n']}) {p['ratio']:.3f}: {100 * p['strength'] ** 2 * (1.3 * p['ratio'] ** -0.8) * (1 - math.exp(-1.2 / (1.3 * p['ratio'] ** -0.8))) / tot:.0f}%" for p in P if p['strength'] ** 2 * (1.3 * p['ratio'] ** -0.8) * (1 - math.exp(-1.2 / (1.3 * p['ratio'] ** -0.8))) / tot > 0.005))
json.dump(out, open(sys.argv[1], "w"))
