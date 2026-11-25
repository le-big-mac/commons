"""Step 2: do the author's runs reproduce from the author's code and seeds? (first seeds, to order 800 only)
Also: is holes() the same set as (i) a plain reading-order scan and (ii) 'blocks empty before the deletion', at every step?"""
import sys, json, time
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, "/home/agent2/aztec")
import aztec as A
R = json.load(open("/home/agent2/aztec/runs.json"))
seeds = [int(s) for s in sys.argv[1].split(",")]
nmax = int(sys.argv[2])
at = [n for n in (100, 200, 400, 800, 1600) if n <= nmax]
t0 = time.time()
for seed in seeds:
    rng = np.random.default_rng(seed)
    x = np.zeros((2, 2), bool); w = A.holes(x); A.fill(x, w, rng.random(int(w.sum())) < 0.5); tosses = int(w.sum())
    diff_pre = 0; steps = 0; ncand_extra = 0
    for order in range(2, nmax + 1):
        # blocks empty before the deletion (referee's rule), from the embedded array
        n2 = x.shape[0]; y0 = np.zeros((n2 + 2, n2 + 2), bool); y0[1:-1, 1:-1] = x
        a, b, c, d = A.parts(y0); pre_empty = ~(a | b | c | d)
        x = A.shuffle(x); w = A.holes(x); k = int(w.sum())
        steps += 1; diff_pre += int((w != pre_empty).sum()); ncand_extra += int(A.fillable(x).sum()) - k
        A.fill(x, w, rng.random(k) < 0.5); tosses += k
        if order in at:
            r = A.readings(x, tosses); ref = R[seed - 100][str(order)]
            same = all(r[key] == ref[key] for key in ('K', 'frozen', 'centre', 'tosses', 'tiling'))
            print(f"seed {seed} order {order}: K {r['K']} frozen {r['frozen']:.6f} tosses {r['tosses']}; identical to runs.json: {same}", flush=True)
    print(f"seed {seed}: steps {steps}; blocks where holes() differs from 'empty before deletion': {diff_pre}; candidates rejected by holes() in all: {ncand_extra}; {time.time()-t0:.0f}s", flush=True)
