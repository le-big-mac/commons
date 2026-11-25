# Referee: independent (slow, plain Python) water routing and measures on a saved bed,
# to check the C program's numbers, plus a look at how the roughness is distributed.
import sys, math
import numpy as np
NY, NX, S, CS = 256, 64, 0.05, 0.05
h = np.fromfile(sys.argv[1]).reshape(NY, NX)
Q = np.zeros((NY, NX)); Q[0] = 1.0
r2 = math.sqrt(2.0)
for j in range(NY - 1):
    for i in range(NX):
        q = Q[j, i]
        if q == 0: continue
        tg = [ii for ii in (i - 1, i, i + 1) if 0 <= ii < NX]
        s = [(h[j, i] - h[j + 1, ii]) / (1.0 if ii == i else r2) for ii in tg]
        if any(x > 0 for x in s):
            w = [math.sqrt(x) if x > 0 else 0.0 for x in s]
        else:
            w = [1.0 / math.sqrt(abs(x) + 1e-12) for x in s]
        tot = sum(w)
        for ii, ww in zip(tg, w):
            Q[j + 1, ii] += q * ww / tot
thr = 0.0035 * 64
sub = slice(64, 192)
wetm = Q[sub] > thr
runs = (wetm[:, 0].astype(int) + (wetm[:, 1:] & ~wetm[:, :-1]).sum(axis=1))
dev = (h[sub] - h[sub].mean(axis=1, keepdims=True)) / S
print("threads %.3f wet %.4f rough %.4f maxshare %.4f rough_wet %.4f" % (
    runs.mean(), wetm.mean(), math.sqrt((dev ** 2).mean()), (Q[sub].max(axis=1) / Q[sub].sum(axis=1)).mean(),
    math.sqrt((dev[wetm] ** 2).mean()) if wetm.any() else 0))
print("water kept per row: min %.6f max %.6f (should be 64)" % (Q.sum(axis=1).min(), Q.sum(axis=1).max()))
a = np.sort(np.abs(dev).ravel())[::-1]
print("dev/S: min %.2f max %.2f; share of rough^2 in top 1%% of cells %.3f, top 10%% %.3f" % (
    dev.min(), dev.max(), (a[:len(a) // 100] ** 2).sum() / (a ** 2).sum(), (a[:len(a) // 10] ** 2).sum() / (a ** 2).sum()))
slope = (h[:-1].mean(axis=1) - h[1:].mean(axis=1)) / S
print("row-mean slope/S: rows 1-63 %.3f, 64-191 %.3f, 192-254 %.3f; head step %.3f foot step %.3f" % (
    slope[1:63].mean(), slope[64:191].mean(), slope[192:254].mean(), slope[0], slope[254]))
