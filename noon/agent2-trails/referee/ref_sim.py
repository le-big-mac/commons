"""Referee's blind re-implementation of the desire-path simulation.

Written from the prose specification only (trails.py / measure.py not opened).
Array convention: G[ix, iy]; cell (ix, iy) covers
[x0 + ix*h, x0 + (ix+1)*h) x [y0 + iy*h, y0 + (iy+1)*h), centre at +h/2.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import sys
import numpy as np
from scipy.signal import fftconvolve

GATES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
PAIRS = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]  # ordered (src, dst)
NSBIN = 50  # bins along the route for the mean-path profile


def make_kernel(sigma, h):
    R = int(np.floor(4 * sigma / h + 1e-9))
    a = np.arange(-R, R + 1) * h
    rr = np.hypot(a[:, None], a[None, :])
    K = np.where(rr <= 4 * sigma + 1e-12, np.exp(-rr / sigma), 0.0)
    return K / K.sum()


def run(cap, seed=0, N=160, margin=0.12, sigma=0.12, gain=64.0, rate=1.0,
        I=0.15, T=20.0, t_end=280.0, every=8, scatter=0.004, frac=0.4,
        variant="spec", keep_tracks=40, dtfac=0.5, coarse_cells=8.0):
    """variant:
       'spec'      -- the walking rule exactly as specified
       'bidir'     -- control: flip the sign of nothing, but symmetrise wear between the
                      two directions is impossible; instead see run-time options below
    """
    rng = np.random.default_rng(seed)
    h = 1.0 / N
    dt = h * dtfac
    x0 = GATES[:, 0].min() - margin
    y0 = GATES[:, 1].min() - margin
    nx = int(np.ceil((GATES[:, 0].max() + margin - x0) / h - 1e-9))
    ny = int(np.ceil((GATES[:, 1].max() + margin - y0) / h - 1e-9))
    G = np.zeros((nx, ny))
    K = make_kernel(sigma, h)
    nsteps = int(round(t_end / dt))
    t_meas = (1 - frac) * t_end

    # walker state
    pos = np.zeros((0, 2))
    pair = np.zeros(0, dtype=int)
    walked = np.zeros(0)
    wid = np.zeros(0, dtype=int)
    next_id = 0
    cpos = np.zeros((0, 2)); clen = np.zeros(0); nst = np.zeros(0, dtype=int)   # route length sampled every coarse_cells
    csteps = int(round(coarse_cells * h / dt)); route = []

    L = np.array([np.linalg.norm(GATES[b] - GATES[a]) for a, b in PAIRS])
    dst = np.array([GATES[b] for a, b in PAIRS])
    src = np.array([GATES[a] for a, b in PAIRS])

    # outputs
    foot = np.zeros((6, nx, ny))          # footsteps per ordered pair, measurement window
    Gsum = np.zeros((nx, ny)); nG = 0     # time-averaged wear in the window
    det = [[] for _ in range(6)]          # detours of walkers arriving in the window
    det_t = []                            # (t, pair, detour) for all arrivals
    nlost = 0; nlost_win = 0
    # mean-path profile: for each ordered pair, in bins of s (fraction along src->dst
    # measured in the frame of the UNordered edge, lower gate index = s 0), sum of the signed
    # perpendicular offset (positive = towards the third gate / triangle interior)
    prof_sum = np.zeros((6, NSBIN)); prof_sq = np.zeros((6, NSBIN)); prof_n = np.zeros((6, NSBIN))
    # edge frames
    e_ax = np.zeros((6, 2)); e_nrm = np.zeros((6, 2)); e_org = np.zeros((6, 2))
    for k, (a, b) in enumerate(PAIRS):
        lo, hi = min(a, b), max(a, b)
        third = 3 - a - b
        ax = GATES[hi] - GATES[lo]
        ax = ax / np.linalg.norm(ax)
        nrm = np.array([-ax[1], ax[0]])
        if np.dot(GATES[third] - GATES[lo], nrm) < 0:
            nrm = -nrm
        e_ax[k] = ax; e_nrm[k] = nrm; e_org[k] = GATES[lo]
    tracks = {}       # walker id -> list of positions (only for late walkers)
    track_pair = {}
    done_tracks = [[] for _ in range(6)]

    V = np.zeros((nx, ny)); gx = np.zeros((nx, ny)); gy = np.zeros((nx, ny))
    wear = I * (dt / h)
    decay = 1.0 - dt / T

    for step in range(nsteps):
        t = step * dt
        if step % every == 0:
            V = gain * fftconvolve(G, K, mode="same")
            # central differences (one-sided on the border rows only)
            gx, gy = np.gradient(V, h)
        # --- new walkers
        n_new = rng.poisson(rate * dt, size=6)
        if n_new.any():
            newpair = np.repeat(np.arange(6), n_new)
            m = len(newpair)
            newpos = src[newpair] + rng.normal(0.0, scatter, size=(m, 2))
            pos = np.vstack([pos, newpos])
            pair = np.concatenate([pair, newpair])
            walked = np.concatenate([walked, np.zeros(m)])
            wid = np.concatenate([wid, np.arange(next_id, next_id + m)])
            cpos = np.vstack([cpos, newpos]); clen = np.concatenate([clen, np.zeros(m)]); nst = np.concatenate([nst, np.zeros(m, dtype=int)])
            next_id += m
        n = len(pair)
        if n:
            ix = np.clip(np.floor((pos[:, 0] - x0) / h).astype(int), 0, nx - 1)
            iy = np.clip(np.floor((pos[:, 1] - y0) / h).astype(int), 0, ny - 1)
            pull = np.stack([gx[ix, iy], gy[ix, iy]], axis=1)
            mag = np.linalg.norm(pull, axis=1)
            big = mag > cap
            if big.any():
                pull[big] *= (cap / mag[big])[:, None]
            to = dst[pair] - pos
            d = np.linalg.norm(to, axis=1)
            e = to / np.maximum(d, 1e-12)[:, None]
            dirn = e + pull
            dirn /= np.maximum(np.linalg.norm(dirn, axis=1), 1e-12)[:, None]
            # --- wear on the cell stood on before moving (sequential, so G stays <= 1)
            for j in range(n):
                G[ix[j], iy[j]] += wear * (1.0 - G[ix[j], iy[j]])
            if t >= t_meas:
                np.add.at(foot, (pair, ix, iy), 1.0)
                rel = pos - e_org[pair]
                s = np.einsum("ij,ij->i", rel, e_ax[pair]) / L[pair]
                p = np.einsum("ij,ij->i", rel, e_nrm[pair])
                sb = np.floor(s * NSBIN).astype(int)
                ok = (sb >= 0) & (sb < NSBIN)
                np.add.at(prof_sum, (pair[ok], sb[ok]), p[ok])
                np.add.at(prof_sq, (pair[ok], sb[ok]), p[ok] ** 2)
                np.add.at(prof_n, (pair[ok], sb[ok]), 1.0)
                if t >= t_end - 12.0:
                    for j in range(n):
                        w = int(wid[j])
                        if w not in tracks:
                            if walked[j] == 0.0:
                                tracks[w] = [pos[j].copy()]; track_pair[w] = int(pair[j])
                        else:
                            tracks[w].append(pos[j].copy())
            # --- move
            pos = pos + dt * dirn
            walked = walked + dt
            nst = nst + 1
            tick = nst % csteps == 0
            if tick.any():
                clen[tick] += np.linalg.norm(pos[tick] - cpos[tick], axis=1); cpos[tick] = pos[tick]
        # --- regrowth
        G *= decay
        np.clip(G, 0.0, 1.0, out=G)
        if t >= t_meas and step % every == 0:
            Gsum += G; nG += 1
        # --- arrivals / lost
        if n:
            rem = np.linalg.norm(dst[pair] - pos, axis=1)
            arrived = rem < 1.5 * dt
            lost = (~arrived) & (walked > 4 * L[pair])
            if arrived.any() or lost.any():
                for j in np.nonzero(arrived)[0]:
                    dd = (walked[j] + rem[j]) / L[pair[j]]
                    det_t.append((t + dt, int(pair[j]), float(dd)))
                    if t + dt >= t_meas:
                        det[pair[j]].append(dd)
                        route.append((clen[j] + np.linalg.norm(pos[j] - cpos[j]) + rem[j]) / L[pair[j]])
                    w = int(wid[j])
                    if w in tracks:
                        done_tracks[track_pair[w]].append(np.array(tracks.pop(w)))
                nl = int(lost.sum())
                nlost += nl
                if t + dt >= t_meas:
                    nlost_win += nl
                for j in np.nonzero(lost)[0]:
                    tracks.pop(int(wid[j]), None)
                keep = ~(arrived | lost)
                pos = pos[keep]; pair = pair[keep]; walked = walked[keep]; wid = wid[keep]
                cpos = cpos[keep]; clen = clen[keep]; nst = nst[keep]

    alld = np.concatenate([np.asarray(x) for x in det]) if any(len(x) for x in det) else np.zeros(0)
    out = dict(cap=cap, seed=seed, h=h, dt=dt, x0=x0, y0=y0, nx=nx, ny=ny,
               G=G, Gmean=Gsum / max(nG, 1), foot=foot,
               mean_detour=float(alld.mean()) if len(alld) else np.nan,
               n_arr=len(alld), nlost=nlost, nlost_win=nlost_win,
               det_pair=np.array([np.mean(x) if len(x) else np.nan for x in det]),
               det_t=np.array(det_t), route=np.array(route), mean_route=float(np.mean(route)) if route else np.nan,
               prof_sum=prof_sum, prof_sq=prof_sq, prof_n=prof_n)
    for k in range(6):
        trk = done_tracks[k][-keep_tracks:]
        out[f"ntrk{k}"] = len(trk)
        for q, tr in enumerate(trk):
            out[f"trk{k}_{q}"] = tr
    return out


if __name__ == "__main__":
    cap = float(sys.argv[1]); seed = int(sys.argv[2])
    outdir = sys.argv[3] if len(sys.argv) > 3 else "/home/agent2/referee-trails/out"
    extra = {}
    for a in sys.argv[4:]:
        k, v = a.split("=")
        extra[k] = float(v) if k not in ("N", "every", "keep_tracks") else int(v)
    os.makedirs(outdir, exist_ok=True)
    import time
    t0 = time.time()
    r = run(cap, seed, **extra)
    np.savez_compressed(os.path.join(outdir, f"run_c{cap:.2f}_s{seed}.npz"), **r)
    print(f"cap={cap} seed={seed} mean_detour={r['mean_detour']:.4f} route(sampled every 8 cells)={r['mean_route']:.4f} n={r['n_arr']} lost={r['nlost']} "
          f"(window {r['nlost_win']}) per-pair={np.round(r['det_pair'],4)} time={time.time()-t0:.0f}s", flush=True)
