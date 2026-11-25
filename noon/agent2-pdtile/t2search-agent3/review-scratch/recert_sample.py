import sys, pickle, time, random
from multiprocessing import Pool
import wt
M = 108
def work(mask):
    A = [x for x in range(M) if mask >> x & 1]
    v, cert, feas = wt.certified(A, M)
    return v
if __name__ == "__main__":
    res = pickle.load(open("res108.pkl", "rb")); und = [r[0] for r in res if r[2] == "?"]; random.Random(7).shuffle(und); und = und[:240]; t0 = time.time(); c = {}
    with Pool(3) as pool:
        for v in pool.imap_unordered(work, und, chunksize=4): c[v] = c.get(v, 0) + 1
    print(f"Z_108: random sample of {len(und)} of the float-only negatives, integer Farkas certificate search: {c}   [{time.time() - t0:.0f} s]")
