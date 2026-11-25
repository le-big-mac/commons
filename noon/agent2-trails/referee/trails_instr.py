"""Referee's instrumented copy of Noon's trails.py simulate().

The dynamics are Noon's line for line (same RNG calls in the same order). Added, without touching the dynamics:
  - which ordered pair each walker belongs to; a footstep map per ordered pair (foot6)
  - a count of lost walkers; a count of steps skipped by the `continue`
  - the detour computed two ways: Noon's (gone AFTER the move + distance BEFORE the move) and corrected
    (gone after the move + distance after the move)
  - snapshots of G through the recording window
Switches (all default off = Noon's behaviour):
  circ=1     kernel cut to r <= 4 sigma (the specification) instead of a square of half-width ceil(4 sigma n)
  noskip=1   do wear/regrowth bookkeeping even on steps with no walkers
  flipx=1    mirror the gates left-right (x -> 1 - x): checks for a handedness in the code
  swapxy=1   transpose the lawn (x <-> y): checks the axis order of the gradient
"""
import sys
import numpy as np
from scipy.signal import fftconvolve

CAP = 0.9
TRI = [(0.0, 0.0), (1.0, 0.0), (0.5, np.sqrt(3) / 2)]


def simulate(gates, I, T, sigma=0.06, n=160, margin=0.12, rate=1.0, t_end=None, seed=0, gain=1.0, record_from=0.6, cap=None,
             circ=False, noskip=False, refresh=8, shift=0.0):
    rng = np.random.default_rng(seed)
    gates = np.array(gates)
    lo = gates.min(0) - margin - shift / n                              # referee: shift = move the grid by this fraction of a cell
    hi = gates.max(0) + margin
    nx, ny = int(round((hi[0] - lo[0]) * n)) + 1, int(round((hi[1] - lo[1]) * n)) + 1
    h = 1.0 / n
    G = np.zeros((ny, nx))
    r = int(np.ceil(4 * sigma * n))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    ker = np.exp(-np.hypot(xx, yy) * h / sigma)
    if circ:
        ker[np.hypot(xx, yy) * h > 4 * sigma] = 0.0
    ker /= ker.sum()
    dt = 0.5 * h
    t_end = t_end if t_end is not None else 12 * T + 40
    steps = int(t_end / dt)
    pairs = [(a, b) for a in range(len(gates)) for b in range(len(gates)) if a != b]
    pos = np.zeros((0, 2)); dest = np.zeros((0, 2)); gone = np.zeros(0); direct = np.zeros(0)
    pidx = np.zeros(0, dtype=int)                                       # referee: ordered pair of each walker
    cpos = np.zeros((0, 2)); clen = np.zeros(0); nst = np.zeros(0, dtype=int); routes = []   # referee: route length sampled every 8 cells
    foot = np.zeros_like(G)
    foot6 = np.zeros((len(pairs),) + G.shape)                           # referee
    detours = []; detours_fixed = []; det_pair = []                     # referee
    nlost_total = 0; nlost_window = 0; nskipped = 0; nwalk_sum = 0      # referee
    snaps = []; snap_t = []; trk = []
    snap_every = int(steps * (1 - record_from) / 8)
    Vx = Vy = None
    for s in range(steps):
        if s % refresh == 0:
            V = gain * fftconvolve(G, ker, mode='same')
            Vy, Vx = np.gradient(V, h)
        k = rng.poisson(rate * dt, len(pairs))
        for j, ((a, b), m) in enumerate(zip(pairs, k)):
            for _ in range(m):
                pos = np.vstack([pos, gates[a] + rng.normal(0, 0.004, 2)])
                dest = np.vstack([dest, gates[b]])
                gone = np.append(gone, 0.0)
                direct = np.append(direct, np.hypot(*(gates[b] - gates[a])))
                pidx = np.append(pidx, j)
                cpos = np.vstack([cpos, pos[-1]]); clen = np.append(clen, 0.0); nst = np.append(nst, 0)
        if s > record_from * steps and (s - int(record_from * steps)) % snap_every == 0:
            snaps.append(G.copy()); snap_t.append(s * dt)
        if len(pos) == 0:
            nskipped += 1
            if noskip:
                np.clip(G, 0, 1, out=G)
                G *= 1 - dt / T
            continue
        nwalk_sum += len(pos)
        ix = np.clip(np.rint((pos[:, 0] - lo[0]) * n).astype(int), 0, nx - 1)
        iy = np.clip(np.rint((pos[:, 1] - lo[1]) * n).astype(int), 0, ny - 1)
        to = dest - pos
        dist = np.hypot(to[:, 0], to[:, 1])
        pull = np.c_[Vx[iy, ix], Vy[iy, ix]]
        size = np.hypot(pull[:, 0], pull[:, 1])
        pull *= np.minimum(1.0, (CAP if cap is None else cap) / np.maximum(size, 1e-12))[:, None]
        e = to / np.maximum(dist, 1e-9)[:, None] + pull
        e /= np.maximum(np.hypot(e[:, 0], e[:, 1]), 1e-9)[:, None]
        if s >= steps - 6400:                                           # referee: follow the oldest walker
            trk.append([s, pidx[0], gone[0], pos[0, 0], pos[0, 1], pull[0, 0], pull[0, 1], e[0, 0], e[0, 1], size[0]])
        pos = pos + dt * e
        gone = gone + dt
        nst = nst + 1
        tick = nst % 16 == 0
        if tick.any():
            clen[tick] += np.hypot(*(pos[tick] - cpos[tick]).T); cpos[tick] = pos[tick]
        np.add.at(G, (iy, ix), I * dt / h ** 2 * h * (1 - G[iy, ix]))
        np.clip(G, 0, 1, out=G)
        G *= 1 - dt / T
        if s > record_from * steps:
            np.add.at(foot, (iy, ix), 1.0)
            np.add.at(foot6, (pidx, iy, ix), 1.0)
        arrived = dist < 1.5 * dt
        lost = gone > 4 * direct
        if arrived.any() and s > record_from * steps:
            detours += ((gone[arrived] + dist[arrived]) / direct[arrived]).tolist()
            after = np.hypot(*(dest[arrived] - pos[arrived]).T)         # referee: distance left AFTER the move
            detours_fixed += ((gone[arrived] + after) / direct[arrived]).tolist()
            det_pair += pidx[arrived].tolist()
            routes += ((clen[arrived] + np.hypot(*(pos[arrived] - cpos[arrived]).T) + after) / direct[arrived]).tolist()
        keep = ~(arrived | lost)
        nl = int((lost & ~arrived).sum())
        nlost_total += nl
        if s > record_from * steps:
            nlost_window += nl
        pos, dest, gone, direct, pidx = pos[keep], dest[keep], gone[keep], direct[keep], pidx[keep]
        cpos, clen, nst = cpos[keep], clen[keep], nst[keep]
    return dict(G=G, foot=foot, foot6=foot6, pairs=np.array(pairs),
                detour=float(np.mean(detours)) if detours else np.nan, n_arrived=len(detours),
                detour_fixed=float(np.mean(detours_fixed)) if detours else np.nan,
                detours=np.array(detours), detours_fixed=np.array(detours_fixed), det_pair=np.array(det_pair),
                route=float(np.mean(routes)) if routes else np.nan, routes=np.array(routes),
                nlost_total=nlost_total, nlost_window=nlost_window, nskipped=nskipped, mean_walkers=nwalk_sum / steps,
                snaps=np.array(snaps), snap_t=np.array(snap_t), trk=np.array(trk), lo=lo, hi=hi, h=h)


if __name__ == '__main__':
    cap = float(sys.argv[1]); seed = int(sys.argv[2]); out = sys.argv[3]
    opts = dict(a.split('=') for a in sys.argv[4:])
    gates = np.array(TRI)
    if opts.get('two') == '1':                                          # control: two gates only, no third to bow the trail
        gates = gates[:2]
    if opts.get('flipx') == '1':
        gates = np.c_[1.0 - gates[:, 0], gates[:, 1]]
    if opts.get('swapxy') == '1':
        gates = gates[:, ::-1].copy()
    if 'rot' in opts:                                                   # rotate the lawn about its centre by this many degrees
        th = np.radians(float(opts['rot'])); c0 = gates.mean(0)
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        gates = (gates - c0) @ R.T + c0
    T = 20.0
    res = simulate(gates, I=3.0 / T, T=T, gain=float(opts.get('gain', 64.0)), sigma=0.12, seed=seed, cap=cap,
                   circ=opts.get('circ') == '1', noskip=opts.get('noskip') == '1', refresh=int(opts.get('refresh', 8)),
                   n=int(opts.get('n', 160)), shift=float(opts.get('shift', 0.0)))
    np.savez_compressed(out, cap=cap, seed=seed, gates=gates, **res)
    print(f"cap {cap} seed {seed} {opts}: Noon's detour {res['detour']:.4f}, corrected {res['detour_fixed']:.4f}, route sampled every 8 cells {res['route']:.4f}, over {res['n_arrived']} walkers; "
          f"lost {res['nlost_total']} (in window {res['nlost_window']}); steps skipped {res['nskipped']}; mean walkers {res['mean_walkers']:.2f}")
