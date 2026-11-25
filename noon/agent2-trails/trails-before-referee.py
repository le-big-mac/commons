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
}


def simulate(gates, I, T, sigma=0.06, n=160, margin=0.12, rate=1.0, t_end=None, seed=0, gain=1.0, record_from=0.6, cap=None):
    """Lengths are in units of the gate spacing; the grid has n cells per unit.  Returns G, the walkers' mean detour
    over the last part of the run, and the density of their footsteps there."""
    rng = np.random.default_rng(seed)
    gates = np.array(gates)
    lo = gates.min(0) - margin
    hi = gates.max(0) + margin
    nx, ny = int(round((hi[0] - lo[0]) * n)) + 1, int(round((hi[1] - lo[1]) * n)) + 1
    h = 1.0 / n
    G = np.zeros((ny, nx))
    # kernel of the attraction, cut off at 4 sigma
    r = int(np.ceil(4 * sigma * n))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    ker = np.exp(-np.hypot(xx, yy) * h / sigma)
    ker /= ker.sum()
    dt = 0.5 * h                                                        # half a cell per step
    T_steps = T / dt
    t_end = t_end if t_end is not None else 12 * T + 40
    steps = int(t_end / dt)
    pairs = [(a, b) for a in range(len(gates)) for b in range(len(gates)) if a != b]
    pos = np.zeros((0, 2)); dest = np.zeros((0, 2)); gone = np.zeros(0); direct = np.zeros(0)
    foot = np.zeros_like(G)
    detours = []
    Vx = Vy = None
    for s in range(steps):
        if s % 8 == 0:                                                  # the attraction changes slowly: refresh it now and then
            V = gain * fftconvolve(G, ker, mode='same')
            Vy, Vx = np.gradient(V, h)
        # new walkers: each ordered pair of gates at `rate` per unit time, with a little scatter at the gate
        k = rng.poisson(rate * dt, len(pairs))
        for (a, b), m in zip(pairs, k):
            for _ in range(m):
                pos = np.vstack([pos, gates[a] + rng.normal(0, 0.004, 2)])
                dest = np.vstack([dest, gates[b]])
                gone = np.append(gone, 0.0)
                direct = np.append(direct, np.hypot(*(gates[b] - gates[a])))
        if len(pos) == 0:
            continue
        ix = np.clip(np.rint((pos[:, 0] - lo[0]) * n).astype(int), 0, nx - 1)
        iy = np.clip(np.rint((pos[:, 1] - lo[1]) * n).astype(int), 0, ny - 1)
        to = dest - pos
        dist = np.hypot(to[:, 0], to[:, 1])
        pull = np.c_[Vx[iy, ix], Vy[iy, ix]]
        size = np.hypot(pull[:, 0], pull[:, 1])
        pull *= np.minimum(1.0, (CAP if cap is None else cap) / np.maximum(size, 1e-12))[:, None]   # my addition: a trail may bend a walker's course but never hold them
        e = to / np.maximum(dist, 1e-9)[:, None] + pull
        e /= np.maximum(np.hypot(e[:, 0], e[:, 1]), 1e-9)[:, None]
        pos = pos + dt * e
        gone = gone + dt
        # wear and regrowth
        np.add.at(G, (iy, ix), I * dt / h ** 2 * h * (1 - G[iy, ix]))   # a walker wears a strip one cell wide
        np.clip(G, 0, 1, out=G)
        G *= 1 - dt / T
        if s > record_from * steps:
            np.add.at(foot, (iy, ix), 1.0)
        arrived = dist < 1.5 * dt
        lost = gone > 4 * direct                                        # a walker going round in circles is taken off
        if arrived.any() and s > record_from * steps:
            detours += ((gone[arrived] + dist[arrived]) / direct[arrived]).tolist()
        keep = ~(arrived | lost)
        nlost = int(lost.sum())
        pos, dest, gone, direct = pos[keep], dest[keep], gone[keep], direct[keep]
    return dict(G=G, foot=foot, detour=float(np.mean(detours)) if detours else np.nan, n_arrived=len(detours), lo=lo, hi=hi, h=h)


if __name__ == '__main__':
    layout, kappa = sys.argv[1], float(sys.argv[2])
    gain = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    sigma = float(sys.argv[5]) if len(sys.argv) > 5 else 0.06
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    cap = float(sys.argv[7]) if len(sys.argv) > 7 else CAP
    T = 20.0
    res = simulate(LAYOUTS[layout], I=kappa / T, T=T, gain=gain, sigma=sigma, seed=seed, cap=cap)
    np.savez(sys.argv[3], kappa=kappa, gain=gain, sigma=sigma, seed=seed, cap=cap, gates=np.array(LAYOUTS[layout]), **res)
    print(f"{layout} kappa {kappa} gain {gain} sigma {sigma} cap {cap}: mean detour {res['detour']:.4f} over {res['n_arrived']} walkers; worn share of the lawn {float((res['G'] > 0.3).mean()):.3f}")
