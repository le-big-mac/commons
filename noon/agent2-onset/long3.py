"""Afterwards: twelve more runs at N = 12,800 (evenly spaced Gaussian tempos, K = 1, T = 30,000), read as in long2.py, to tell a flattening slope from scatter.
usage: python long3.py long3.json"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import long2 as L2
from concurrent.futures import ProcessPoolExecutor
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=8) as ex: Q = np.array(list(ex.map(L2.job, range(604, 616))))
    old = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'long2.json')))
    half = (Q[:, 2] + Q[:, 3]) / 2; allr = np.r_[old['each'], half]
    print(f"twelve new runs: mean {half.mean():.4f} (sd {half.std(ddof=1):.4f}); each: " + ", ".join(f"{x:.4f}" for x in half))
    print(f"quarters, twelve new runs: " + ", ".join(f"{x:.4f}" for x in Q.mean(0)))
    print(f"all sixteen runs: mean {allr.mean():.4f}, standard error {allr.std(ddof=1) / 4:.4f}")
    S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'long.json')))['sizes']
    n = np.array([q['N'] for q in S] + [12800]); rr = np.array([q['r'] for q in S] + [allr.mean()])
    print(f"slope over the eight sizes with all sixteen runs at 12,800: {np.polyfit(np.log(n), np.log(rr), 1)[0]:+.3f}; from 6,400 to 12,800 alone: {np.log(allr.mean() / S[-1]['r']) / np.log(2):+.2f}")
    json.dump(dict(new=half.tolist(), quarters=Q.mean(0).tolist(), all=allr.tolist(), mean=float(allr.mean()), se=float(allr.std(ddof=1) / 4)), open(sys.argv[1], 'w'))
