"""Desire paths: the active-walker model of trail formation (Helbing, Keltsch, Molnar 1997), on a grid.

Ground G(r, t) in [0, 1]: worn where walkers step, regrowing everywhere:
    dG/dt = -G / T  +  I (1 - G) * (walkers stepping on r)
Attraction of a trail seen from r:  V(r) = sum over r' of exp(-|r - r'| / sigma) G(r')   (visibility sigma)
A walker at r bound for d moves at unit speed in the direction of   (d - r)/|d - r|  +  grad V(r),  normalised.
One change from the published model: |grad V| is capped at 0.9, so that the destination always wins and no walker
can be held by a trail (without the cap, strong trails near a gate trap walkers in this implementation).
Walkers leave each gate for every other gate at a steady rate.

usage (as a script): python trails.py LAYOUT kappa out.npz [gain [sigma [seed [cap]]]]      LAYOUT = triangle | square
    kappa = I * T: how well a single walker's wear lasts.  Other parameters are fixed below.
"""
import sys
import numpy as np
from scipy.signal import fftconvolve

CAP = 0.9                                                               # the trail's pull is capped below the pull of the destination (1)

LAYOUTS = {
    'triangle': [(0.0, 0.0), (1.0, 0.0), (0.5, np.sqrt(3) / 2)],
    'square': [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
    'two': [(0.0, 0.0), (1.0, 0.0)],                                      # a control: one straight trail
}


def simulate(gates, I, T, sigma=0.06, n=160, margin=0.12, rate=1.0, t_end=None, seed=0, gain=1.0, record_from=0.6, cap=None):
    """Lengths are in units of the gate spacing; the grid has n cells per unit.  Returns the worn ground, footstep maps for
    each ordered pair of gates over the last part of the run, and two measures of how far walkers go there:
      walked: every step counted (this includes a cell-sized zig-zag across the trail when the pull is strong);
      route:  the length of the walker's track sampled every 8 cells, which leaves the zig-zag out.
    Changes after the referee's report: the detour no longer counts one step too many; the kernel is cut at 4 sigma
    as the description says; grass regrows on every step, also when the lawn is empty; the route measure and the
    footstep maps by direction are new."""
    rng = np.random.default_rng(seed)
    gates = np.array(gates)
    lo = gates.min(0) - margin
    hi = gates.max(0) + margin
    nx, ny = int(round((hi[0] - lo[0]) * n)) + 1, int(round((hi[1] - lo[1]) * n)) + 1
    h = 1.0 / n
    G = np.zeros((ny, nx))
    r = int(np.ceil(4 * sigma * n))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    dist_k = np.hypot(xx, yy) * h
    ker = np.where(dist_k <= 4 * sigma, np.exp(-dist_k / sigma), 0.0)
    ker /= ker.sum()
    dt = 0.5 * h                                                        # half a cell per step
    t_end = t_end if t_end is not None else 12 * T + 40
    steps = int(t_end / dt)
    pairs = [(a, b) for a in range(len(gates)) for b in range(len(gates)) if a != b]
    pos = np.zeros((0, 2)); dest = np.zeros((0, 2)); gone = np.zeros(0); direct = np.zeros(0)
    last = np.zeros((0, 2)); route = np.zeros(0); nstep = np.zeros(0, int); which = np.zeros(0, int)
    foot = np.zeros((len(pairs), ny, nx), np.float32)
    walked, routes, lost_total = [], [], 0
    SAMPLE = 16                                                         # steps between samples of a walker's track: 8 cells
    Vx = Vy = None
    for s in range(steps):
        if s % 8 == 0:                                                  # the attraction changes slowly: refresh it now and then
            V = gain * fftconvolve(G, ker, mode='same')
            Vy, Vx = np.gradient(V, h)
        k = rng.poisson(rate * dt, len(pairs))
        for j, ((a, b), m) in enumerate(zip(pairs, k)):
            for _ in range(m):
                start = gates[a] + rng.normal(0, 0.004, 2)
                pos = np.vstack([pos, start]); dest = np.vstack([dest, gates[b]]); last = np.vstack([last, start])
                gone = np.append(gone, 0.0); route = np.append(route, 0.0); nstep = np.append(nstep, 0); which = np.append(which, j)
                direct = np.append(direct, np.hypot(*(gates[b] - gates[a])))
        recording = s > record_from * steps
        if len(pos):
            to = dest - pos
            dist = np.hypot(to[:, 0], to[:, 1])
            arrived = dist < 1.5 * dt
            lost = gone > 4 * direct                                    # a walker going round in circles would be taken off (none is)
            if arrived.any() and recording:
                walked += ((gone[arrived] + dist[arrived]) / direct[arrived]).tolist()
                routes += ((route[arrived] + np.hypot(*(dest[arrived] - last[arrived]).T)) / direct[arrived]).tolist()
            lost_total += int(lost.sum())
            keep = ~(arrived | lost)
            pos, dest, gone, direct, last, route, nstep, which = pos[keep], dest[keep], gone[keep], direct[keep], last[keep], route[keep], nstep[keep], which[keep]
        if len(pos):
            ix = np.clip(np.rint((pos[:, 0] - lo[0]) * n).astype(int), 0, nx - 1)
            iy = np.clip(np.rint((pos[:, 1] - lo[1]) * n).astype(int), 0, ny - 1)
            to = dest - pos
            dist = np.hypot(to[:, 0], to[:, 1])
            pull = np.c_[Vx[iy, ix], Vy[iy, ix]]
            size = np.hypot(pull[:, 0], pull[:, 1])
            pull *= np.minimum(1.0, (CAP if cap is None else cap) / np.maximum(size, 1e-12))[:, None]   # my addition: a trail may bend a walker's course but never hold them
            e = to / np.maximum(dist, 1e-9)[:, None] + pull
            e /= np.maximum(np.hypot(e[:, 0], e[:, 1]), 1e-9)[:, None]
            np.add.at(G, (iy, ix), I * dt / h * (1 - G[iy, ix]))        # a walker wears the cell it stands on
            np.clip(G, 0, 1, out=G)
            if recording:
                np.add.at(foot, (which, iy, ix), 1.0)
            pos = pos + dt * e
            gone = gone + dt
            nstep = nstep + 1
            samp = nstep % SAMPLE == 0
            if samp.any():
                route[samp] += np.hypot(*(pos[samp] - last[samp]).T)
                last[samp] = pos[samp]
        G *= 1 - dt / T                                                 # regrowth, every step
    return dict(G=G, foot=foot.sum(0), foot_pair=foot, pairs=np.array(pairs), detour=float(np.mean(walked)) if walked else np.nan,
                route=float(np.mean(routes)) if routes else np.nan, n_arrived=len(walked), lost=lost_total, lo=lo, hi=hi, h=h)


if __name__ == '__main__':
    layout, kappa = sys.argv[1], float(sys.argv[2])
    gain = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    sigma = float(sys.argv[5]) if len(sys.argv) > 5 else 0.06
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    cap = float(sys.argv[7]) if len(sys.argv) > 7 else CAP
    T = 20.0
    res = simulate(LAYOUTS[layout], I=kappa / T, T=T, gain=gain, sigma=sigma, seed=seed, cap=cap)
    np.savez(sys.argv[3], kappa=kappa, gain=gain, sigma=sigma, seed=seed, cap=cap, gates=np.array(LAYOUTS[layout]), **res)
    print(f"{layout} kappa {kappa} gain {gain} sigma {sigma} cap {cap}: walked {res['detour']:.4f}, route {res['route']:.4f} over {res['n_arrived']} walkers; lost {res['lost']}; worn share of the lawn {float((res['G'] > 0.3).mean()):.3f}")
