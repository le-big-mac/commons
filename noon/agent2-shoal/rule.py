"""The 40-seed runs of trend.py again, with the combining rule as Couzin et al. (2002) print it.
Expectations sealed in rule-prediction.md before this was run (26 November 2026).
usage: python -I rule.py rule.json        (numpy; couzin.py beside it; eight processes, about a quarter of an hour)"""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from multiprocessing import Pool
from couzin import School

class Printed(School):
    """as School, but with d = (d_o + d_a)/2 for the plain sums of unit vectors, as on page 3 of the paper"""
    def step(s):
        d = s.x[None] - s.x[:, None]; dist = np.linalg.norm(d, axis=2); np.fill_diagonal(dist, np.inf)
        u = d / np.where(np.isfinite(dist), dist, 1)[..., None]
        vis = (u * s.v[:, None]).sum(2) > np.cos(np.pi - s.blind / 2)
        rep = dist < s.rr
        zo = (dist >= s.rr) & (dist < s.ro) & vis; za = (dist >= s.ro) & (dist < s.ra) & vis
        d_r = -(u * rep[..., None]).sum(1)
        d_o = (s.v[None] * zo[..., None]).sum(1); d_a = (u * za[..., None]).sum(1)
        ho = zo.any(1)[:, None]; ha = za.any(1)[:, None]
        want = np.where(ho & ha, .5 * (d_o + d_a), np.where(ho, d_o, d_a))            # the one changed line
        want = np.where(rep.any(1)[:, None], d_r, want)
        want = np.where(np.linalg.norm(want, axis=1, keepdims=True) < 1e-9, s.v, want)
        cur = np.arctan2(s.v[:, 1], s.v[:, 0]); tgt = np.arctan2(want[:, 1], want[:, 0]) + s.rng.normal(0, s.noise, s.N)
        dth = (tgt - cur + np.pi) % (2 * np.pi) - np.pi; dth = np.clip(dth, -s.turn * s.dt, s.turn * s.dt)
        cur += dth; s.v = np.stack([np.cos(cur), np.sin(cur)], 1); s.x += s.v * s.speed * s.dt

def run(a):
    dro, seed, which = a
    s = (Printed if which == 'printed' else School)(ro=1 + dro, seed=1000 + seed)
    for t in range(4000): s.step()
    P = []; M = []
    for t in range(500):
        s.step()
        if t % 50 == 0: p, m, n, k = s.order_largest(); P.append(p); M.append(m)
    p, m = float(np.mean(P)), float(np.mean(M))
    return dro, seed, 'A' if p > .65 and p > m else ('M' if m > .5 else '.'), n, k, p, m

if __name__ == '__main__':
    W = (2, 3, 4, 5, 6, 7, 8)
    control = [(d, k, 'mine') for d in (2, 6) for k in range(4)]                       # eight runs of my own rule, to see that this file reproduces trend.json
    with Pool(8) as pool: res = pool.map(run, control + [(d, k, 'printed') for d in W for k in range(40)], chunksize=2)
    ctl, res = res[:len(control)], res[len(control):]
    json.dump(dict(control=ctl, printed=res), open(sys.argv[1], 'w'))
    old = {(r[0], r[1]): r for r in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trend.json')))}
    print("control, my rule, eight runs against trend.json (label, largest group, groups): " + ("all eight the same" if all(tuple(c[:5]) == tuple(old[(c[0], c[1])]) for c in ctl) else "DIFFER: " + str([(c[:5], old[(c[0], c[1])]) for c in ctl if tuple(c[:5]) != tuple(old[(c[0], c[1])])])))
    print("width  mills  aligned  neither   mean alignment  mean rotation   mean largest group   schools split   | my rule (trend.json): mills aligned neither")
    for d in W:
        r = [x for x in res if x[0] == d]; o = [x for x in old.values() if x[0] == d]
        print(f"{d:5d}  {sum(x[2] == 'M' for x in r):5d}  {sum(x[2] == 'A' for x in r):7d}  {sum(x[2] == '.' for x in r):7d}   {np.mean([x[5] for x in r]):14.2f}  {np.mean([x[6] for x in r]):13.2f}   {np.mean([x[3] for x in r]):18.1f}   {sum(x[4] > 1 for x in r):13d}   | {sum(x[2] == 'M' for x in o):5d} {sum(x[2] == 'A' for x in o):7d} {sum(x[2] == '.' for x in o):7d}")
    n = len(res); mills = sum(x[2] == 'M' for x in res); al = sum(x[2] == 'A' for x in res); nei = sum(x[2] == '.' for x in res)
    big = float(np.mean([x[3] for x in res])); split = sum(x[4] > 1 for x in res)
    lo = float(np.mean([x[6] for x in res if x[0] in (2, 3)])); hi = float(np.mean([x[6] for x in res if x[0] in (6, 7, 8)]))
    shares = [sum(x[2] == 'M' for x in res if x[0] == d) / 40 for d in W]
    print(f"all {n}: mills {mills}, aligned {al}, neither {nei}; largest group {big:.1f} fish on average; {split} schools split")
    print("the sealed lines:")
    print(f"  R1 (largest group above 90 on average): {big:.1f} -> {'held' if big > 90 else 'failed'}")
    print(f"  R2 (fewer than a quarter aligned, that is fewer than 70): {al} -> {'held' if al < 70 else 'failed'}")
    print(f"  R3 (at least 14 neither): {nei} -> {'held' if nei >= 14 else 'failed'}")
    print(f"  R4 (mean rotation at widths 6 to 8 above that at widths 2 to 3): {hi:.3f} against {lo:.3f} -> {'held' if hi > lo else 'failed'}")
    print(f"  R5 (mill share outside 35 to 60% at one width at least): shares {[round(100 * s) for s in shares]} -> {'held' if any(s < 0.35 or s > 0.60 for s in shares) else 'failed'}")
