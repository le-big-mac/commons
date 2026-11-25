"""What the bell piece does, measured from its list of strikes.   usage: python piece_check.py step.json"""
import sys, json
import numpy as np
from scipy.stats import spearmanr
J = json.load(open(sys.argv[1])); S = J['strikes']; t = np.array([s[0] for s in S]); b = np.array([s[1] for s in S]); m = np.array([s[2] for s in S])
r = np.array(J['r']); tr = np.arange(len(r)) * J['r_dt']
print(f"{J['N']} bells, {len(S)} strikes in {J['tend']:.0f} s; own periods {2 * np.pi / max(J['omega']):.2f} to {2 * np.pi / min(J['omega']):.2f} s; critical coupling reached at {J['t1'] + (J['t2'] - J['t1']) / J['kmax']:.1f} s")
def pulses(a, z):
    k = np.nonzero((t >= a) & (t < z))[0]; groups = [[k[0]]]
    for i in k[1:]:
        if t[i] - t[groups[-1][-1]] > 1.0: groups.append([i])
        else: groups[-1].append(i)
    return [g for g in groups if len(g) == J['N']]
for name, a, z in (("held at three times critical", J['t2'], J['t3']),):
    P = pulses(a, z)
    width = [t[g[-1]] - t[g[0]] for g in P]; rho = [spearmanr(t[g], m[g])[0] for g in P]; gap = np.diff([t[g].mean() for g in P])
    print(f"{name}: {len(P)} complete rolls of {J['N']} strikes; first to last strike {np.mean(width):.2f} s (from {min(width):.2f} to {max(width):.2f}); one roll every {gap.mean():.2f} s;")
    print(f"   rank correlation between when a bell strikes within the roll and its pitch: {np.mean(rho):.3f} (lowest {min(rho):.3f})")
first = tr[np.argmax(r > 0.5)]; kc_t = J['t1'] + (J['t2'] - J['t1']) / J['kmax']
stay = tr[len(r) - 1 - np.argmax((r[::-1] < 0.5) & (tr[::-1] < J['t3']))]
print(f"r first above 0.5 at {first:.1f} s; last below 0.5 before the release at {stay:.1f} s, when the coupling is {(stay - J['t1']) / (J['t2'] - J['t1']) * J['kmax']:.2f} times critical")
after = tr[(tr > J['t3']) & (r < 0.5)][0]
print(f"after the release at {J['t3']:.0f} s, r falls below 0.5 at {after:.1f} s ({after - J['t3']:.1f} s, {(after - J['t3']) / J['period']:.1f} turns)")
for a, z, name in ((0, J['t1'], "no coupling"), (J['t2'], J['t3'], "held"), (J['t3'] + 15, J['tend'], "from 15 s after the release")):
    k = (tr >= a) & (tr < z); print(f"   r, {name}: mean {r[k].mean():.2f}")
print(f"   with {J['N']} bells and no rhythm at all, r would average about {np.sqrt(np.pi / (4 * J['N'])):.2f}")
