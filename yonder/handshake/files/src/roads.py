"""Which majority type did the handshake family take over from, in real beds?"""
import pickle, sys
from collections import Counter
from multiprocessing import Pool
from evolve import run
def one(j):
    r = run(j); return (j[0], j[4], r["trans"], r["log"])
jobs = [(e, 0.99, 9000 + s, 200000, N, 1.0 / N, 1.0, 0.0) for (e, N) in ((0.02, 100), (0.02, 400), (0.005, 400)) for s in range(8)]
if __name__ == "__main__":
    with Pool(12) as p: res = p.map(one, jobs, chunksize=1)
    pickle.dump(res, open("roads.pkl", "wb"))
    FAM = {"0:D[0,1] 1:D[0,2] 2:C[2,0]": "handshake", "0:D[1,2] 1:D[1,0] 2:C[2,1]": "shifty", "0:C[0,1] 1:D[1,2] 2:D[1,0]": "wooer"}
    NAME = dict(FAM); NAME.update({"0:D[0,0]": "all-defect", "0:D[1,0] 1:C[0,0]": "echo-once", "0:C[0,1] 1:D[0,1]": "tit-for-tat", "0:C[0,1] 1:D[1,1]": "grim", "0:C[0,0]": "all-cooperate", "0:C[0,1] 1:D[1,0]": "win-stay"})
    body = lambda d: d[d.index("0:"):-1] if "0:" in d else d
    for cond in sorted({(r[0], r[1]) for r in res}):
        into = Counter(); first = Counter()
        for e, N, trans, log in res:
            if (e, N) != cond: continue
            for a, b, v in trans:
                A, B = body(a), body(b)
                if B in FAM and A not in FAM: into[NAME.get(A, "other: " + A)] += v
        tot = sum(into.values())
        print(f"\nnoise {cond[0]}, bed {cond[1]}: {tot} takeovers by a handshake-family machine from a majority outside the family; predecessor:")
        for k, v in into.most_common(8): print(f"   {100*v/tot:5.1f}%  {k}")
