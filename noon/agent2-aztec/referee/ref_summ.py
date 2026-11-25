"""Summarise sampler readings. usage: ref_summ.py file1.npz [file2.npz ...]"""
import sys
import numpy as np

R = np.concatenate([np.load(f)["rows"] for f in sys.argv[1:]])
ns = sorted(set(R[:, 1].astype(int)))
print(f"files {[f.split('/')[-1] for f in sys.argv[1:]]}: growths {len(set(R[:,0]))}")
for n in ns:
    r = R[R[:, 1] == n]
    g = len(r)
    K = r[:, 2]; ff = r[:, 3]
    cnt = r[:, 8:12]; cnt2 = r[:, 12:16]
    sh = cnt.sum(0) / cnt.sum(); sh2 = cnt2.sum(0) / cnt2.sum()
    shr = cnt / cnt.sum(1, keepdims=True)
    t = r[:, 16]
    sdK = K.std(ddof=1)
    # rough standard error of an sd from g samples: sd*sqrt((kurt-1)/(4g)); use normal approx 1/sqrt(2(g-1))
    print(f" n={n}: growths {g}; K mean {K.mean():.3f} (se {sdK/np.sqrt(g):.3f}), sd {sdK:.3f} (se~{sdK/np.sqrt(2*(g-1)):.3f}); "
          f"K/n {K.mean()/n:.5f}; excess 0.146447n-K = {0.1464466*n-K.mean():.3f} = {(0.1464466*n-K.mean())/n**(1/3):.3f} n^(1/3); "
          f"sd/n^(1/3) {sdK/n**(1/3):.3f}")
    print(f"       frozen fraction mean {ff.mean():.5f} (sd {ff.std(ddof=1):.5f}); (0.214602-ff) n^(2/3) = {(0.2146018-ff.mean())*n**(2/3):.3f}")
    print(f"       central shares a,b,c,d [0.4n<=i<0.6n] pooled {np.round(sh,4)}; per-growth sd {np.round(shr.std(0,ddof=1),4)}; inclusive ends {np.round(sh2,4)}")
    print(f"       tosses mean {t.mean():.1f} min {t.min():.0f} max {t.max():.0f}; n(n+1)/2 = {n*(n+1)//2}; ratio mean/(n(n+1)/2) {t.mean()/(n*(n+1)/2):.4f}; "
          f"growths with exactly n(n+1)/2: {(t==n*(n+1)//2).sum()}; pair blocks mean {r[:,17].mean():.1f}, empty blocks mean {r[:,18].mean():.1f}")
if len(ns) > 1:
    sds = [R[R[:, 1] == n][:, 2].std(ddof=1) for n in ns]
    p = np.polyfit(np.log(ns), np.log(sds), 1)
    print(f" log-log slope of sd(K) over n={ns}: {p[0]:.3f}")
