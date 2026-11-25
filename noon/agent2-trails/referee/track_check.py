"""Referee: follow single walkers in Noon's code. Is the distance walked the length of the route, or cell-scale zig-zag?"""
import sys, numpy as np
h = 1 / 160; dt = h / 2
for fn in sys.argv[1:]:
    d = np.load(fn); t = d['trk']; gates = d['gates']
    # split into walkers: a new walker starts when 'gone' drops
    cuts = np.r_[0, np.nonzero(np.diff(t[:, 2]) < 0)[0] + 1, len(t)]
    rows = []; ex = None
    for a, b in zip(cuts[:-1], cuts[1:]):
        w = t[a:b]
        if len(w) < 64:   # pieces of track of at least 32 cells
            continue
        xy = w[:, 3:5]
        def plen(step):
            idx = np.r_[np.arange(0, len(xy) - 1, step), len(xy) - 1]
            return np.hypot(*np.diff(xy[idx], axis=0).T).sum()
        full = plen(1)
        # heading relative to the line of sight, and progress towards the destination
        rows.append([full, plen(4), plen(8), plen(16), plen(32)])
        if ex is None: ex = w
    r = np.array(rows)
    tot = r.sum(0)
    print(f"{fn.split('/')[-1]:22s} cap {float(d['cap'])}: {len(r)} pieces of track, {tot[0]:.1f} lawn-sides walked; distance walked / length of the same track sampled every "
          f"2, 4, 8, 16 cells: {tot[0]/tot[1]:.4f} {tot[0]/tot[2]:.4f} {tot[0]/tot[3]:.4f} {tot[0]/tot[4]:.4f}")
    if '-v' in sys.argv[0:1] or True:
        w = ex; n = len(w)
        # lateral position (cells) relative to chord for the example walker, every 40 steps, and angle between heading and line of sight
        a, b = [(i, j) for i in range(len(gates)) for j in range(len(gates)) if i != j][int(w[0, 1])]
        A, B = gates[a], gates[b]; ax = (B - A) / np.hypot(*(B - A)); nr = np.array([-ax[1], ax[0]])
        s = (w[:, 3:5] - A) @ ax; p = (w[:, 3:5] - A) @ nr
        los = (B - w[:, 3:5]); los /= np.hypot(*los.T)[:, None]
        ang = np.degrees(np.arctan2(w[:, 7] * los[:, 1] * -1 + w[:, 8] * los[:, 0], w[:, 7] * los[:, 0] + w[:, 8] * los[:, 1]))
        # fraction of steps where heading is more than 5 degrees off the line of sight, split by quarter of the journey
        q = np.clip((s / np.hypot(*(B - A)) * 4).astype(int), 0, 3)
        print("     example walker: mean |angle between heading and line of sight| by quarter of the journey: " + " ".join(f"{np.abs(ang[q == k]).mean():5.1f}" for k in range(4))
              + " deg; sign changes of that angle per cell walked, by quarter: " + " ".join(f"{(np.diff(np.sign(ang[q == k])) != 0).sum() / max((q == k).sum() * 0.5, 1):.2f}" for k in range(4))
              + f"; raw |grad V| median {np.median(w[:, 9]):.2f}, share of steps with |grad V| above the cap {np.mean(w[:, 9] > float(d['cap'])):.2f}")
