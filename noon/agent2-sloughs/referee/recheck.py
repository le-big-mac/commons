# recompute Table 1 and a few README numbers straight from Noon's run outputs (read only)
import glob, re, numpy as np
res = {}
for f in sorted(glob.glob("/home/agent2/meander/out/grid/P*-dc*-s*.out")):
    m = re.search(r"P([\d.]+)-dc([\d.]+)-s(\d+)", f); P, dc, s = float(m.group(1)), float(m.group(2)), int(m.group(3))
    a = np.loadtxt(f, comments="#"); t, S = a[:, 0], a[:, 2]; T = t[-1]; h = t >= T / 2
    res.setdefault((P, dc), []).append((S[h].mean(), S[h].min(), S[h].max(), S[h].std(), S[t < T / 4].mean(), S[(t >= T / 4) & (t < T / 2)].mean(), S[(t >= T/2) & (t < 3*T/4)].mean(), S[t >= 3*T/4].mean(), T))
print("P dc  mean  se   | min max over 2nd half | quarter means q1 q2 q3 q4 (mean of seeds) | T")
tab = {}
for k in sorted(res):
    r = np.array(res[k]); n = len(r); tab[k] = (r[:, 0].mean(), r[:, 0].std(ddof=1) / np.sqrt(n))
    print("%g %g  %.3f %.3f | %.2f %.2f | %.3f %.3f %.3f %.3f | %g  n=%d" % (k[0], k[1], tab[k][0], tab[k][1], r[:, 1].min(), r[:, 2].max(), r[:, 4].mean(), r[:, 5].mean(), r[:, 6].mean(), r[:, 7].mean(), r[0, 8], n))
Ps = [2, 3, 4.5, 6]; dcs = [0.2, 0.4, 0.8]
steps = []
for d in dcs:
    for a, b in zip(Ps[:-1], Ps[1:]):
        steps.append(("P %g->%g at dc %g" % (a, b, d), tab[(b, d)][0] - tab[(a, d)][0], np.hypot(tab[(b, d)][1], tab[(a, d)][1])))
for p in Ps:
    for a, b in zip(dcs[:-1], dcs[1:]):
        steps.append(("dc %g->%g at P %g" % (a, b, p), tab[(p, a)][0] - tab[(p, b)][0], np.hypot(tab[(p, a)][1], tab[(p, b)][1])))
for s in sorted(steps, key=lambda x: x[1] / x[2]): print("%-22s step %.3f  se %.3f  ratio %.1f" % (s[0], s[1], s[2], s[1] / s[2]))
# q3 vs q4 over all 48 runs: is there a drift inside the half?
allr = np.concatenate([np.array(res[k]) for k in res]); print("48 runs: mean q4-q3 = %.4f (se %.4f); mean q3-q2 = %.4f (se %.4f); mean q2-q1 %.4f" % ((allr[:,7]-allr[:,6]).mean(), (allr[:,7]-allr[:,6]).std(ddof=1)/np.sqrt(len(allr)), (allr[:,6]-allr[:,5]).mean(), (allr[:,6]-allr[:,5]).std(ddof=1)/np.sqrt(len(allr)), (allr[:,5]-allr[:,4]).mean()))
