"""Referee's doubling measurements on the blind runs."""
import sys, glob
import numpy as np

PAIRS = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
GATES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
outdir = sys.argv[1] if len(sys.argv) > 1 else "/home/agent2/referee-trails/out"


def analyse(f):
    r = np.load(f)
    n = r["prof_n"]; mu = r["prof_sum"] / np.maximum(n, 1)
    sd = np.sqrt(np.maximum(r["prof_sq"] / np.maximum(n, 1) - mu ** 2, 0))
    nb = mu.shape[1]
    res = dict(cap=float(r["cap"]), seed=int(r["seed"]), det=float(r["mean_detour"]))
    seps = []; mids = []; sds = []; maxseps = []; ov = []; ovmid = []; peak_s = []
    h = float(r["h"]); x0 = float(r["x0"]); y0 = float(r["y0"])
    nx, ny = r["G"].shape
    X = x0 + (np.arange(nx) + 0.5) * h; Y = y0 + (np.arange(ny) + 0.5) * h
    XX, YY = np.meshgrid(X, Y, indexing="ij")
    for e in range(3):
        fwd, bwd = 2 * e, 2 * e + 1     # lo->hi and hi->lo, both in the lo->hi frame
        mid = slice(nb // 2 - 1, nb // 2 + 1)
        m_f = mu[fwd, mid].mean(); m_b = mu[bwd, mid].mean()
        s_f = sd[fwd, mid].mean(); s_b = sd[bwd, mid].mean()
        mids.append((m_f, m_b)); sds.append((s_f, s_b))
        seps.append(abs(m_f - m_b))
        d = np.abs(mu[fwd] - mu[bwd])
        maxseps.append(d[2:-2].max())
        # where along its own direction of travel each path bulges most (0 = start, 1 = end)
        jf = np.argmax(np.abs(mu[fwd])); jb = np.argmax(np.abs(mu[bwd]))
        peak_s.append(((jf + 0.5) / nb, 1 - (jb + 0.5) / nb))
        # footstep overlap: share of (normalised) footsteps on cells used by both
        a, b = PAIRS[fwd]
        Ff = r["foot"][fwd]; Fb = r["foot"][bwd]
        pf = Ff / Ff.sum(); pb = Fb / Fb.sum()
        ov.append(np.minimum(pf, pb).sum())
        # same, restricted to the middle half of the route (s in [0.25, 0.75])
        ax = GATES[b] - GATES[a]; ax /= np.linalg.norm(ax)
        s = (XX - GATES[a, 0]) * ax[0] + (YY - GATES[a, 1]) * ax[1]
        msk = (s > 0.25) & (s < 0.75)
        pf2 = Ff * msk; pb2 = Fb * msk
        pf2 = pf2 / pf2.sum(); pb2 = pb2 / pb2.sum()
        ovmid.append(np.minimum(pf2, pb2).sum())
    res.update(seps=np.array(seps), mids=np.array(mids), sds=np.array(sds), maxseps=np.array(maxseps),
               ov=np.array(ov), ovmid=np.array(ovmid), peak_s=np.array(peak_s), mu=mu, sd=sd)
    return res


if __name__ == "__main__":
    files = sorted(glob.glob(outdir + "/run_c*.npz"))
    allr = [analyse(f) for f in files]
    caps = sorted(set(a["cap"] for a in allr))
    np.set_printoptions(precision=4, suppress=True, linewidth=160)
    for c in caps:
        rs = [a for a in allr if a["cap"] == c]
        dets = np.array([a["det"] for a in rs])
        print(f"\n=== cap {c}: {len(rs)} seeds; mean detour {dets.mean():.4f} (sd over seeds {dets.std(ddof=1) if len(rs)>1 else 0:.4f})")
        for a in rs:
            print(f" seed {a['seed']}: detour {a['det']:.4f}")
            for e, nm in enumerate(["0-1", "0-2", "1-2"]):
                print(f"   edge {nm}: mid-route offset towards interior: out {a['mids'][e,0]:+.4f} (sd {a['sds'][e,0]:.4f}), "
                      f"back {a['mids'][e,1]:+.4f} (sd {a['sds'][e,1]:.4f}); |sep| mid {a['seps'][e]:.4f}, max sep along route {a['maxseps'][e]:.4f}; "
                      f"footstep overlap all {a['ov'][e]:.3f}, middle half {a['ovmid'][e]:.3f}; bulge at s_travel out {a['peak_s'][e,0]:.2f} back {a['peak_s'][e,1]:.2f}")
        print(f" summary cap {c}: mean |sep| at mid-route {np.mean([a['seps'] for a in rs]):.4f}; mean max sep {np.mean([a['maxseps'] for a in rs]):.4f}; "
              f"mean lateral sd of one direction at mid-route {np.mean([a['sds'] for a in rs]):.4f}; "
              f"footstep overlap (whole route) {np.mean([a['ov'] for a in rs]):.3f}, (middle half) {np.mean([a['ovmid'] for a in rs]):.3f}")
