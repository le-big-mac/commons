"""Hand-built 'patience ladder' family: k cooperating states counting defections seen, then p punishing states.
Evaluate self-payoff and robustness against the test set (all <=3-state machines + all one-step mutants)."""
import sys, numpy as np, pickle
from multiprocessing import Pool
sys.argv = [sys.argv[0], "0.05", "0.99", "0", "0"] if len(sys.argv) < 3 else sys.argv[:3] + ["0", "0"]
import climb
from ipd import FSM, canonical

def build(k, p, rC, rD):
    S = k + p; play = np.array([0] * k + [1] * p); nxt = np.zeros((S, 2), dtype=np.int64)
    for i in range(k): nxt[i] = [i, i + 1]
    for j in range(p - 1): nxt[k + j] = [k, k + j + 1]
    nxt[S - 1] = [rC, rD]
    return play, nxt

def job(a):
    if climb.SMALL is None: climb.setup()
    k, p, rC, rD = a
    play, nxt = build(k, p, rC, rD)
    s, b = climb.evaluate(play, nxt, 0)
    return a, s, b

if __name__ == "__main__":
    jobs = [(k, p, rC, rD) for k in range(1, 11) for p in range(1, 5) for rC in range(k + p) for rD in range(k + p)]
    with Pool(14) as pool: res = pool.map(job, jobs, chunksize=4)
    pickle.dump(res, open("ladder.pkl", "wb"))
    print("best robust member for each (patience k, punishment length p):  self-payoff [return on C, return on D]")
    for k in range(1, 11):
        row = []
        for p in range(1, 5):
            c = [(s, a) for a, s, b in res if a[0] == k and a[1] == p and b <= s + 1e-12]
            if c:
                s, a = max(c); nm = lambda t: f"c{t}" if t < k else f"d{t-k}"
                row.append(f"{s:.4f} [{nm(a[2])},{nm(a[3])}]")
            else: row.append("   —   ")
        print(f"k={k:2d}: " + "   ".join(f"{x:22s}" for x in row))
