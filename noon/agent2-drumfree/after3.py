"""The referee's controls, redone in my own code.  None registered.   usage: python -u after3.py OUT.json"""
import sys, json, glob
import numpy as np
from scipy.optimize import minimize
from scipy.special import jn_zeros
import libfree as F
L = F.L; A = {}
def eight(s, k):
    """one even disc: the seven overtones' miss, the largest of eight with the lowest mode aimed at 1, and the place"""
    m, pl = F.disc_miss(s, k, F.FIVE); return m, max(m, abs(pl - 1)), pl
# A. the plain skin
j = {m: jn_zeros(m, 3) for m in range(5)}; note = j[1][0] / 2; A['plain'] = dict(place=float(j[0][0] / note), overtones=[float(j[m][n - 1] / note) for m, n in F.FIVE[1:]])
print(f"A. The plain skin: the lowest mode's place {A['plain']['place']:.4f}; the seven overtones in units of the note " + ", ".join(f"{x:.4f}" for x in A['plain']['overtones']))
# B. place against weight at a fixed radius
print("B. One even disc: the lowest mode's place (and the overtone miss) against weight at a fixed radius"); A['grid'] = []
for k in (0.40, 0.45, 0.50, 0.55):
    row = []
    for s in (2.5, 4.34, 6.25, 8.0, 10.0, 16.0):
        m, e, pl = eight(s, k); row.append(dict(s=s, k=k, miss=float(m), place=float(pl)))
    A['grid'] += row; mk = [r['place'] for r in row if 6.25 <= r['s'] <= 16]
    print(f"   radius {k:.2f}: " + "; ".join(f"{r['s']:g} times: {r['place']:.3f} ({100 * r['miss']:.1f}%)" for r in row) + f"; spread over makers' weights {max(mk) - min(mk):.3f}", flush=True)
pls = [r['place'] for r in A['grid']]; print(f"   over these 24 discs the place runs from {min(pls):.3f} to {max(pls):.3f}")
# C. the best disc with the lowest mode tuned, in this study's measure
print("C. The best even disc with the lowest mode aimed at 1 as well (the largest of eight misses, the note at half the second mode)")
best = None
for s in np.arange(4.0, 14.01, 0.5):
    for k in np.arange(0.30, 0.5001, 0.0125):
        v = eight(s, k)[1]
        if best is None or v < best[0]: best = (v, s, k)
r = minimize(lambda x: eight(min(60, max(1, x[0])), min(0.95, max(0.05, x[1])))[1], best[1:], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=800)); m, e, pl = eight(*r.x)
A['tuned_disc'] = dict(s=float(r.x[0]), k=float(r.x[1]), eight=float(e), seven=float(m), place=float(pl), grid=[float(x) for x in best])
print(f"   grid's best {100 * best[0]:.3f}% at ({best[1]:.2f}, {best[2]:.4f}); polished {100 * e:.4f}% at {r.x[0]:.3f} times over {r.x[1]:.4f}; its seven overtones alone {100 * m:.3f}%; place {pl:.4f}", flush=True)
# D. named discs in three measures
import drum
def first(s, k):
    w = drum.modes(float(s), float(k), L.NINE); return max(abs(v / w[0] / L.target(a, b) - 1) for v, (a, b) in zip(w, L.NINE))
print("D. Named discs in three measures"); A['named'] = []
for nm, s, k in (("the first study's best disc as printed, 9.94 over 0.400", 9.94, 0.400), ("the same in full, 9.938 over 0.4004", 9.938, 0.4004), ("the 1954 disc, 9.77 over 0.4", 9.77, 0.4), ("this study's best disc, 4.343 over 0.5042", 4.343, 0.5042), ("the disc of C", r.x[0], r.x[1])):
    m, e, pl = eight(s, k); f1 = first(s, k); A['named'].append(dict(name=nm, seven=float(m), eight=float(e), first=float(f1), place=float(pl)))
    print(f"   {nm}: seven overtones {100 * m:.3f}%; eight with the lowest at 1: {100 * e:.3f}%; the first study's measure (the lowest mode is the note): {100 * f1:.3f}%; place {pl:.4f}")
# E. ratios of tuned to free from the digits as printed, and with the tuned figure in this study's measure
B = json.load(open("best.json")); nine = {}
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); nine[d['weight']] = d['rings']
W = [M for M in sorted(nine) if 1 <= M <= 12 and B.get(f"five|{M:g}|40")]; full = [nine[M]['40']['exact'] / B[f"five|{M:g}|40"]['exact'] for M in W]; pr = [round(100 * nine[M]['40']['exact'], 2) / round(100 * B[f"five|{M:g}|40"]['exact'], 3) for M in W]; r80 = [nine[M]['80']['exact'] / B[f"five|{M:g}|80"]['exact'] for M in W]
l4 = json.load(open("leaveout3-2-4.json"))['nothing']['exact']; l1 = json.load(open("leaveout3-2-1.43.json"))['nothing']['exact']
A['ratios'] = dict(full=[min(full), max(full)], printed=[min(pr), max(pr)], rings80=[min(r80), max(r80)], this4=l4 / B["five|4|40"]['exact'], this143=l1 / B["five|1.43|40"]['exact'])
print(f"E. Tuned over free, five families, 40 rings, {len(W)} weights: {min(full):.2f} to {max(full):.2f} from the full digits; {min(pr):.2f} to {max(pr):.2f} from the digits as printed; on 80 rings {min(r80):.2f} to {max(r80):.2f}")
print(f"   with the tuned load searched in this study's measure: {l4 / B['five|4|40']['exact']:.1f} times with 4 skins, {l1 / B['five|1.43|40']['exact']:.1f} with 1.43")
s6 = {M: json.load(open(f"s-six-{M}.json"))['rings']['40']['exact'] for M in ("1.43", "4", "12")}; B12 = json.load(open("../drum12/best.json")); r6 = {M: B12[f"twelve|{M}|40"]['exact'] / s6[M] for M in s6}; A['six'] = r6
print("   six families, 40 rings: " + ", ".join(f"{r6[M]:.1f} times with {M} skins" for M in r6)); D = json.load(open("disc.json")); A['onedisc'] = 0.0316 / D['five']['miss']; print(f"   one even disc: 3.16% over {100 * D['five']['miss']:.2f}% is {A['onedisc']:.2f} times")
# F. the fits to the paper's table at the digits printed
RA = {(0, 1): 1.03, (2, 1): 3.00, (0, 2): 3.00, (3, 1): 4.00, (1, 2): 4.00, (0, 3): 5.04, (4, 1): 5.03, (2, 2): 5.08}
def fit(s, k):
    rr, pl = F.disc_modes(s, k, F.FIVE); mod = dict(zip(F.FIVE, rr)); mod[(0, 1)] = pl; return max(abs(mod[q] / v - 1) for q, v in RA.items())
A['raman'] = dict(printed=float(fit(6.426, 0.4413)), full=float(fit(D['raman']['s'], D['raman']['k'])), d54=float(fit(9.77, 0.4)), d54b=float(fit(3.125 ** 2, 0.4)))
print(f"F. Against the paper's eight measured ratios: 6.426 over 0.4413 as printed {100 * A['raman']['printed']:.3f}%; in full {100 * A['raman']['full']:.3f}%; the 1954 disc at 9.77 times {100 * A['raman']['d54']:.3f}%, at 3.125 squared = {3.125 ** 2:.4f} times {100 * A['raman']['d54b']:.3f}%")
# G. the two discs against the makers' range
G = json.load(open("after-G.json"))['two1.43']; mean = (G['outer'] * (G['ko'] ** 2 - G['ki'] ** 2) + G['inner'] * G['ki'] ** 2) / G['ko'] ** 2; rng = np.random.default_rng(7); z = rng.standard_normal(200000)
out_load = float(np.mean(1 + (G['outer'] - 1) * (1 + 0.01 * z) < 6.25)); A['two'] = dict(mean=float(mean), above=float(G['outer'] / 6.25 - 1), below_share=out_load)
print(f"G. The two discs: the outer is {G['outer']:.3f} times the skin, {100 * (G['outer'] / 6.25 - 1):.1f}% above the makers' light edge of 6.25; with its load off by 1% (standard deviation) it is below 6.25 in {100 * out_load:.0f}% of draws; the patch's mean weight per area is {mean:.2f} times the skin")
json.dump(A, open(sys.argv[1], "w"))
