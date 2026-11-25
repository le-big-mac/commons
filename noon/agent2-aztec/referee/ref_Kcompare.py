"""Step 2: sampled K against the exact law of K (ref_Kkraw.K_law)."""
import sys, json, math
import numpy as np
from scipy import stats
from ref_Kkraw import K_law
def compare(label, n, k):
    r = K_law(n); pmf = np.clip(r["pmf"], 0, None); N = len(k)
    zmean = (k.mean() - r["mean"]) / (r["sd"] / math.sqrt(N))
    # exact-law test for the variance by simulation-free normal approx using the exact 4th moment
    ks = np.arange(len(pmf)); m4 = (pmf * (ks - r["mean"]) ** 4).sum(); var = r["sd"] ** 2
    se_var = math.sqrt((m4 - var ** 2) / N)
    s2 = ((k - r["mean"]) ** 2).mean()                  # variance about the exact mean
    zvar = (s2 - var) / se_var
    # chi-square goodness of fit, bins pooled to expected >= 5
    order = np.argsort(ks); exp = N * pmf; obs = np.bincount(k, minlength=len(pmf))[:len(pmf)].astype(float)
    lo = 0; E = []; O = []; accE = accO = 0.0
    for i in ks:
        accE += exp[i]; accO += obs[i]
        if accE >= 5: E.append(accE); O.append(accO); accE = accO = 0.0
    if accE > 0: E[-1] += accE; O[-1] += accO
    E = np.array(E); O = np.array(O); chi2 = ((O - E) ** 2 / E).sum(); p = stats.chi2.sf(chi2, len(E) - 1)
    print(f"{label} n={n}: {N} growths; mean K {k.mean():.4f} vs exact {r['mean']:.4f} (z = {zmean:+.2f}); sd {k.std(ddof=1):.4f} vs exact {r['sd']:.4f} (variance z = {zvar:+.2f}, "
          f"lower-tail p = {stats.norm.cdf(zvar):.4f}); chi2 fit {chi2:.1f} on {len(E)-1} dof, p = {p:.4f}")
    return zmean, zvar
print("--- referee's sampler")
a = np.concatenate([np.load(f"/home/agent2/aztec/referee/Konly100_{s}.npy") for s in (1, 2, 3, 4)])
for c, n in enumerate((16, 25, 50, 100)): compare("referee K-only", n, a[:, c])
b = np.concatenate([np.load(f"/home/agent2/aztec/referee/Konly400_{s}.npy") for s in (1, 2, 3, 4)])
R1 = np.concatenate([np.load(f"/home/agent2/aztec/referee/s_{s}.npz")["rows"] for s in "abcd"])
R2 = np.concatenate([np.load(f"/home/agent2/aztec/referee/s800_{s}.npz")["rows"] for s in (5000, 6000, 7000)])
for c, n in enumerate((200, 400)):
    k = np.concatenate([b[:, c], R1[R1[:, 1] == n][:, 2].astype(int), R2[R2[:, 1] == n][:, 2].astype(int)])
    compare("referee, all growths", n, k)
    compare("   of which the first 592 (blind + 800 batch)", n, np.concatenate([R1[R1[:, 1] == n][:, 2].astype(int), R2[R2[:, 1] == n][:, 2].astype(int)]))
    compare("   of which the later 1200", n, b[:, c])
compare("referee", 100, np.concatenate([R1[R1[:, 1] == 100][:, 2].astype(int), R2[R2[:, 1] == 100][:, 2].astype(int)]))
compare("referee", 800, R2[R2[:, 1] == 800][:, 2].astype(int))
print("--- the author's runs.json")
R = json.load(open("/home/agent2/aztec/runs.json"))
zs = []
for n in (100, 200, 400, 800, 1600):
    zs.append(compare("author", n, np.array([r[str(n)]['K'] for r in R])))
