"""Checks made after the verdicts.   usage: python after.py > after.out"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import taffy as TF
R = json.load(open('sheet.json')); F = json.load(open('forecast/scored.json'))

print("1. The loop's word lengths obey exact recurrences (checked over every period computed)")
for k, (a, b, c) in (('T1', (3, -1, 0)), ('T2', (6, -1, 0)), ('T5', (4, -1, 2)), ('T6', (6, -1, 4))):
    L = R[k]['lengths']; ok = all(L[i + 1] == a * L[i] + b * L[i - 1] + c for i in range(2, len(L) - 1))
    print(f"   {k}: L(k+1) = {a} L(k) - L(k-1){' + ' + str(c) if c else ''} from the second period on: {ok}   (so the growth is the larger root of x^2 - {a}x + 1 = {(a + math.sqrt(a * a - 4)) / 2:.6f})")
L = R['T4']['lengths']; print(f"   T4: L(k+4) - 2 L(k+3) - 2 L(k+1) + L(k) for k = 2..11: {[L[i + 4] - 2 * L[i + 3] - 2 * L[i + 1] + L[i] for i in range(2, 12)]}")
print("2. Burau matrices at t = -1: characteristic polynomials of the product over one period (rounded to integers)")
for k, (n, moves) in TF.DEVICES.items():
    P = np.eye(n)
    for kind, i in moves:
        B = np.eye(n); B[i - 1:i + 1, i - 1:i + 1] = [[2, -1], [1, 0]]; P = P @ (B if kind == 's' else np.linalg.inv(B))
    cp = np.round(np.poly(P)).astype(int).tolist(); ev = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]
    print(f"   {k}: {cp}; absolute values of the eigenvalues {', '.join(f'{x:.4f}' for x in ev)}")
print("3. The flow: does the answer depend on the step and the spacing?  (device of T2, four periods)")
for dt, gap in ((0.005, 0.01), (0.0025, 0.01), (0.005, 0.005)):
    old = TF.refine; TF.refine = (lambda x, g=gap: old(x, g))
    L, x = TF.flow(TF.DEVICES['T2'][1], 3, 4, dt=dt); TF.refine = old
    print(f"   step {dt}, spacing {gap}: ratios {', '.join(f'{b / a:.3f}' for a, b in zip(L, L[1:]))}; L4/L0 = {L[4] / L[0]:.1f}", flush=True)
print("4. The flow for the other three-rod devices")
L, x = TF.flow(TF.DEVICES['T1'][1], 3, 9); print(f"   device of T1 (braid growth 2.618): ratios {', '.join(f'{b / a:.3f}' for a, b in zip(L, L[1:]))}", flush=True)
L, x = TF.flow(TF.DEVICES['T3'][1], 3, 18); r = np.array(L) / L[0]
print(f"   device of T3 (braid growth 1), 18 periods: L/L0 = {', '.join(f'{v:.1f}' for v in r)}")
k = np.arange(len(r)); lin = np.polyfit(k[6:], r[6:], 1); quad = np.polyfit(k[6:], r[6:], 2); ex = np.polyfit(k[6:], np.log(r[6:]), 1)
res = lambda fit, y: float(np.sqrt(np.mean((np.polyval(fit, k[6:]) - y) ** 2)))
print(f"      from period 6 on: a straight line misses by {res(lin, r[6:]):.2f} (rms), a parabola by {res(quad, r[6:]):.2f}, an exponential (x{math.exp(ex[0]):.3f} a period) by {float(np.sqrt(np.mean((np.exp(np.polyval(ex, k[6:])) - r[6:]) ** 2))):.2f}")
print("5. My odds against the forecasters', by how each line was arrived at")
ids = F['ids']; y = np.array(F['outcome']); me = np.array(F['mine']); med = np.array(F['median'])
for name, grp in (("worked by hand on the sheet (T1, T2, T3, T9)", ['T1', 'T2', 'T3', 'T9']), ("from memory or with a stated doubt (T4, T5, T6, T10)", ['T4', 'T5', 'T6', 'T10']), ("guesses about the flow (T7, T8)", ['T7', 'T8'])):
    j = [ids.index(g) for g in grp]
    print(f"   {name}: my mean odds {me[j].mean():.3f}, theirs {med[j].mean():.3f}; Brier mine {((me[j] - y[j]) ** 2).mean():.4f}, theirs {((med[j] - y[j]) ** 2).mean():.4f}")
d = (me - y) ** 2 - (med - y) ** 2
print(f"   the gap in Brier score is {d.mean():+.4f}; T5 and T6 alone contribute {d[[ids.index('T5'), ids.index('T6')]].sum() / len(y):+.4f}, T4 {d[ids.index('T4')] / len(y):+.4f}, the other seven {d[[i for i, k_ in enumerate(ids) if k_ not in ('T4', 'T5', 'T6')]].sum() / len(y):+.4f}")
