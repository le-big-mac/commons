import numpy as np, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fem import *
from scipy.stats import spearmanr
D = "/home/agent2/drumair/"
N = json.load(open(D + "named.json"))
print("named.json keys:", list(N[0].keys()))
lift, B, mass, nm = [], [], [], []
for r in N[1:]:
    lift.append(r["reference"]["place"] / r["vacuum"] - 1); B.append(r["reference"]["B"]); nm.append(r["name"][:40])
    mass.append(r.get("mass", r.get("weight", np.nan)))
print("rank corr lift vs B: %.3f (n=%d)" % (spearmanr(lift, B)[0], len(lift)))
if not np.isnan(mass).any():
    print("rank corr lift vs added mass: %.3f" % spearmanr(lift, mass)[0])
    for a, b, c, d in sorted(zip(mass, lift, B, nm)): print("   mass %.2f lift %.1f%% B %.2f %s" % (a, 100 * b, c, d))
else:
    print("no mass in named.json:", mass)
# the 0.072% load with an even layer of air mass (0.265 skins) on every mode
for f in ("ref-free-4-1.json", "ref-tuned-4-1.json"):
    a = np.maximum(np.array(json.load(open(D + f))["a"]), 0)
    w0 = rich(320, ring_rho(a)); r0 = report(w0)
    w1 = rich(320, lambda n: ring_rho(a)(n) + 0.265, B=r0["B"]); r1 = report(w1)
    print(f, "spring: free miss %.3f%% tuned miss %.3f%% place %.4f | +0.265 even on all modes (B held): free miss %.3f%% tuned miss %.3f%% place %.4f" % (100 * r0["missA"], 100 * r0["missB"], r0["place"], 100 * r1["missA"], 100 * r1["missB"], r1["place"]))
    print("    shifts by mode:", {str(k): round(100 * (w1[k] / w0[k] - 1), 2) for k in w0 if k != "B"})
# the disc the fit without (3,2) picks: 4.10 times over 0.5625, on the reference drum
for mu, k in ((3.10, 0.5625), (3.20, 0.4838)):
    d = disc_rho(mu, 0.5625) if k == 0.5625 else None
    def dr(n, mu=mu, k=k):
        e = np.arange(n + 1) / n; frac = np.clip((k - e[:-1]) * n, 0, 1); return 1 + mu * frac
    wv = rich(640, dr, B=0.0); wr = rich(640, dr)
    print("disc %.2f times over %.4f: vacuum place %.3f; reference drum B %.2f place %.3f" % (mu + 1, k, report(wv)["place"], wr["B"], report(wr)["place"]))
