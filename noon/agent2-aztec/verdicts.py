"""Verdicts on the six sealed expectations, by the letter, and the readings behind them.   usage: python verdicts.py runs.json verdicts.json"""
import sys, json, math
import numpy as np
R = json.load(open(sys.argv[1])); sizes = [100, 200, 400, 800, 1600]; rng = np.random.default_rng(0)
get = lambda n, key: np.array([r[str(n)][key] for r in R])
V = {}; M = {}
print(f"{len(R)} runs; every configuration read is a tiling: {all(r[str(n)]['tiling'] for r in R for n in sizes)}")
print("n; mean K/n (se); (K - 0.1464 n)/n^(1/3); sd of K; sd/n^(1/3); skewness of K; frozen fraction (se); (fraction - 0.2146) n^(2/3); tosses / (n(n+1)/2)")
sd = []
for n in sizes:
    K = get(n, 'K'); fr = get(n, 'frozen'); t = get(n, 'tosses'); lim = (1 - 1 / math.sqrt(2)) / 2; sd.append(K.std(ddof=1))
    sk = float(((K - K.mean()) ** 3).mean() / K.std() ** 3)
    print(f"{n:5d}  {K.mean() / n:.4f} ({K.std(ddof=1) / math.sqrt(len(K)) / n:.4f})  {(K.mean() - lim * n) / n ** (1 / 3):+.3f}  {K.std(ddof=1):.3f}  {K.std(ddof=1) / n ** (1 / 3):.3f}  {sk:+.2f}  {fr.mean():.4f} ({fr.std(ddof=1) / math.sqrt(len(fr)):.4f})  {(fr.mean() - (1 - math.pi / 4)) * n ** (2 / 3):+.3f}  {t.mean() / (n * (n + 1) / 2):.1f}")
V['A1'] = False; M['A1'] = "as sealed: 112 sequences and 80 configurations at order 3, not all tilings (exhaustive-as-sealed.out)"
K = get(1600, 'K'); V['A2'] = 0.130 <= K.mean() / 1600 <= (1 - 1 / math.sqrt(2)) / 2; M['A2'] = f"{K.mean() / 1600:.4f}"
slope = float(np.polyfit(np.log(sizes), np.log(sd), 1)[0])
bs = [np.polyfit(np.log(sizes), np.log([get(n, 'K')[rng.integers(0, len(R), len(R))].std(ddof=1) for n in sizes]), 1)[0] for _ in range(2000)]
V['A3'] = 0.25 <= slope <= 0.42; M['A3'] = f"{slope:.3f} (resampling the runs: sd {np.std(bs):.3f})"
fr = get(1600, 'frozen'); V['A4'] = 0.185 <= fr.mean() <= 1 - math.pi / 4; M['A4'] = f"{fr.mean():.4f}"
cen = np.array([r['1600']['centre'] for r in R]).mean(0); V['A5'] = bool(((cen >= 0.22) & (cen <= 0.28)).all()); M['A5'] = ", ".join(f"{x:.4f}" for x in cen)
V['A6'] = all(r[str(n)]['tosses'] == n * (n + 1) // 2 for r in R for n in sizes); M['A6'] = f"at n = 1,600 between {get(1600, 'tosses').min():,} and {get(1600, 'tosses').max():,} tosses; n(n+1)/2 = {1600 * 1601 // 2:,}"
for k in sorted(V): print(f"{k}  {'held  ' if V[k] else 'failed'}  {M[k]}")
odds = dict(A1=0.80, A2=0.85, A3=0.80, A4=0.80, A5=0.93, A6=0.88); brier = float(np.mean([(odds[k] - (1.0 if V[k] else 0.0)) ** 2 for k in odds]))
print(f"held {sum(bool(v) for v in V.values())} of {len(V)}; my mean odds {np.mean(list(odds.values())):.3f}; Brier score {brier:.3f} (saying 0.5 every time: 0.250)")
json.dump(dict(verdicts={k: bool(v) for k, v in V.items()}, measured=M, slope=slope, brier=brier), open(sys.argv[2], 'w'), indent=1)
