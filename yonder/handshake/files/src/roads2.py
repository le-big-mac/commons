"""Every entry into the handshake family, in real beds: what did the bed pass through since it was last all-defect?"""
import pickle
from collections import Counter
from multiprocessing import Pool
from evolve import run
def one(j):
    r = run(j); return (j[0], j[4], r["log"])
jobs = [(e, 0.99, 9500 + s, 200000, N, 1.0 / N, 1.0, 0.0) for (e, N) in ((0.02, 100), (0.02, 400), (0.005, 400), (0.05, 100)) for s in range(10)]
if __name__ == "__main__":
    with Pool(13) as p: res = p.map(one, jobs, chunksize=1)
    pickle.dump(res, open("roads2.pkl", "wb"))
    FAM = {"0:D[0,1] 1:D[0,2] 2:C[2,0]", "0:D[1,2] 1:D[1,0] 2:C[2,1]", "0:C[0,1] 1:D[1,2] 2:D[1,0]"}
    N_ = {"0:D[0,0]": "alld", "0:D[1,0] 1:C[0,0]": "echo", "0:C[0,1] 1:D[0,1]": "tft", "0:C[0,1] 1:D[1,1]": "grim", "0:C[0,0]": "allc"}
    body = lambda d: d[d.index("0:"):-1] if "0:" in d else d
    for cond in sorted({(r[0], r[1]) for r in res}):
        first = Counter(); via = Counter(); lens = []; n = 0; runs = 0
        for e, N, log in res:
            if (e, N) != cond: continue
            runs += 1
            seq = ["alld"] + [N_.get(body(d), "FAM" if body(d) in FAM else "x") for g, d in log]
            last = 0
            for i, x in enumerate(seq):
                if x == "alld": last = i
                elif x == "FAM" and last is not None:
                    path = seq[last + 1:i]; n += 1
                    first[path[0] if path else "(direct)"] += 1
                    via["echo" if "echo" in path else "-"] += 1; via["tft or grim" if ("tft" in path or "grim" in path) else "-"] += 1; via["allc" if "allc" in path else "-"] += 1
                    lens.append(len(path)); last = None      # count each excursion from all-defect once
        if n == 0: print(f"\nnoise {cond[0]}, bed {cond[1]}: no entries in {runs} runs"); continue
        import numpy as np
        print(f"\nnoise {cond[0]}, bed {cond[1]}: {n} journeys from an all-defect majority to a handshake-family majority, in {runs} runs")
        print("   first step out of all-defect:", ", ".join(f"{k} {100*v/n:.0f}%" for k, v in first.most_common(5)), "  (x = an unnamed machine)")
        print("   journeys passing through echo-once: %.0f%%;  through tit-for-tat or grim: %.0f%%;  through all-cooperate: %.0f%%" % (100 * via["echo"] / n, 100 * via["tft or grim"] / n, 100 * via["allc"] / n))
        print("   intermediate majorities per journey: median %d, range %d-%d" % (np.median(lens), min(lens), max(lens)))
