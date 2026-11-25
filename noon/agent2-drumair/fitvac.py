"""The vacuum roots of a grid of even discs, kept for the fits (they are the slow part).   usage: python -u fitvac.py PROCESSES OUT.json"""
import sys, json, math, time
import numpy as np
from multiprocessing import Pool
import airlib as A
COUNT = {0: 5, 1: 5, 2: 4, 3: 2, 4: 1}; S = np.exp(np.linspace(math.log(1.5), math.log(60), 34)); K = np.arange(0.15, 0.7001, 0.0125)
def one(ij):
    i, j = ij; return i, j, {m: A.drum.roots(m, float(S[i]), float(K[j]), c) for m, c in COUNT.items()}
if __name__ == "__main__":
    t0 = time.time()
    with Pool(int(sys.argv[1])) as p: res = p.map(one, [(i, j) for i in range(len(S)) for j in range(len(K))], chunksize=8)
    json.dump(dict(S=S.tolist(), K=K.tolist(), roots={f"{i},{j}": {str(m): r for m, r in d.items()} for i, j, d in res}), open(sys.argv[2], "w")); print(f"{len(res)} discs in {time.time() - t0:.0f} s")
