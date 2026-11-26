"""Waiting times: how long until a bed that starts all-defect becomes cooperative (escape), and how long a
bed planted with the handshake stays cooperative (persistence). Capped at GENS generations (censored if longer)."""
import pickle, time, numpy as np
from multiprocessing import Pool
from evolve import run
from ipd import M
GENS = 1500000
H = M("h", 0, [("D", 0, 1), ("D", 0, 2), ("C", 2, 0)])
def first_sustained(c, above, thr, w=50):          # series is every 10 generations; w=50 -> 500 generations
    ok = (c > thr) if above else (c < thr)
    run_ = np.convolve(ok.astype(int), np.ones(w, dtype=int), "valid") == w
    i = np.argmax(run_) if run_.any() else -1
    return int(i) * 10 if i >= 0 else None
def one(j):
    kind, e, N, s = j
    r = run((e, 0.99, s, GENS, N, 1.0 / N, 1.0, 0.0) + ((H,) if kind == "planted" else ()))
    c = r["series"][:, 1]
    t = first_sustained(c, True, 0.5) if kind == "escape" else first_sustained(c, False, 0.3)
    return (kind, e, N, s, t, float(c.mean()))
jobs = [("escape", 0.05, 1000, 13000 + s) for s in range(12)]
if __name__ == "__main__":
    t0 = time.time(); out = []
    with Pool(13) as p:
        for i, r in enumerate(p.imap_unordered(one, jobs, chunksize=1)):
            out.append(r); pickle.dump(out, open("waiting2.pkl", "wb"))
            if True: print(i + 1, "of", len(jobs), round(time.time() - t0), flush=True)
    print("done", round(time.time() - t0))
