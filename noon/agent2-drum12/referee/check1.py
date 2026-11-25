import sys; sys.path.insert(0, "/home/agent2/drum12/referee")
import numpy as np, json, time
import sol
D12 = "/home/agent2/drum12/"
best = json.load(open(D12 + "best.json"))
t0 = time.time()
def ex(a, F):
    a = np.asarray(a); modes = sol.fam_modes(F)
    c = sol.misses(sol.ring_edges(len(a)), 1 + a, modes, max(10, 1600 // len(a)), exact=True)
    return np.abs(c).max(), c, modes
print("== A. author's loads by my solver (exact shooting): key, author's exact %, mine %, mass, heaviest ring, loaded out to")
for key in ["sixteen|4|40", "sixteen|4|80", "twelve|2.79|40", "twelve|2.79|80", "twelve|12|40", "twelve|12|80", "sixteen|12|40", "sixteen|12|80", "sixteen|2.79|40", "twelve|2|40", "twelve|1.43|40", "twelve|6|80", "twelve|4|80"]:
    v = best[key]; a = np.array(v['a']); F = 6 if key.startswith("twelve") else 7
    f, c, modes = ex(a, F); R = len(a)
    print("%-16s %.4f  %.4f  mass %.4f  max ring %.1f  out to %.3f" % (key, 100 * v['exact'], 100 * f, sol.ring_w(R) @ a, a.max(), (np.max(np.nonzero(a > 1e-6)[0]) + 1) / R))
    if key == "sixteen|4|40":
        om = sol.freqs(sol.ring_edges(R), 1 + a, sol.need_of(modes), 40, exact=True)
        print("   ratios:", ", ".join("%.3f" % (om[(m, n)] / om[(0, 1)]) for m, n, f_ in modes))
for F in (8, 9, 10):
    for M in ("12", "4"):
        d = json.load(open(D12 + "after-N-%d-%s.json" % (F, M)))
        for R in ("40", "80"):
            a = np.array(d['rings'][R]['a']); f, c, modes = ex(a, F)
            print("N F=%d M=%s R=%s: author's exact %.4f  mine %.4f  (modes %d) mass %.4f max ring %.1f out to %.3f" % (F, M, R, 100 * d['rings'][R]['exact'], 100 * f, len(modes), sol.ring_w(len(a)) @ a, a.max(), (np.max(np.nonzero(a > 1e-6)[0]) + 1) / len(a)))
print("# t=%.0fs" % (time.time() - t0))
print("== B. strays: every mode (m<=40, n<=10) outside the set, below top harmonic + 1; (FEM, ~1e-4)")
def strays(name, a, F):
    sp = sol.spectrum(a, 40, 10); fam = set((m, n) for m, n, f in sol.fam_modes(F))
    out = [(x, m, n) for x, m, n in sp if x < F + 1.0 and (m, n) not in fam]
    ins = [x for x, m, n in sp if (m, n) in fam]
    print("  %-28s set's top mode at %.3f; outsiders below %d+1: %s" % (name, max(ins), F, ", ".join("(%d,%d) %.3f" % (m, n, x) for x, m, n in out) or "none"))
strays("plain", np.zeros(40), 7)
for key, F in [("sixteen|4|40", 7), ("sixteen|4|80", 7), ("sixteen|12|40", 7), ("sixteen|12|80", 7), ("sixteen|2.79|40", 7), ("sixteen|6|40", 7), ("sixteen|9.6|40", 7), ("twelve|2.79|40", 6), ("twelve|2.79|80", 6), ("twelve|12|40", 6), ("twelve|12|80", 6), ("twelve|2|40", 6), ("twelve|4|40", 6)]:
    strays(key, np.array(best[key]['a']), F)
for F in (8, 9, 10):
    for M in ("12", "4"):
        d = json.load(open(D12 + "after-N-%d-%s.json" % (F, M)))
        for R in ("40", "80"):
            strays("N F=%d M=%s R=%s" % (F, M, R), np.array(d['rings'][R]['a']), F)
print("# t=%.0fs" % (time.time() - t0))
print("== C. T3/T4 on the sealed search's twelve-mode load of 12 skins (s-twelve-12.json, 40 rings)")
s12 = json.load(open(D12 + "s-twelve-12.json"))['rings']['40']; a = np.array(s12['a'])
f, c, modes = ex(a, 6)
print("  exact miss %.4f%% (author %.4f%%); per mode: %s" % (100 * f, 100 * s12['exact'], " ".join("(%d,%d)%+.4f" % (m, n, 100 * ci) for (m, n, _), ci in zip(modes[1:], c))))
print("  (1,3) miss / largest = %.4f ; modes within a hundredth of the largest: %d" % (abs(c[-1]) / f, (np.abs(c) >= 0.99 * f).sum()))
print("  loads by ring:", " ".join("%.1f" % x for x in a[:20]), "| max %.1f; max rise over a ring nearer the centre %.1f" % (a.max(), max(a[j] - a[:j].min() for j in range(1, 40))))
print("== D. my reading of D (FEM mode shapes). columns: as the author (strike .5, top 6.6, m=0 halved, roll-off) | author's value | strike .3 | strike .7 | top 7.6 | m=0 by 1/sqrt2 | no roll-off")
nine = np.array(next(r for r in json.load(open("/home/agent2/drum/chain-free-up.json")) if abs(r['weight'] - 1.43) < 1e-9)['a'])
cases = [("plain", [1.0], [1.0], 192.5), ("nine-mode disc 9.938/.4004", [0.4004, 1.0], [9.938, 1.0], 41.4), ("nine rings 1.43", sol.ring_edges(40), 1 + nine, 17.7)]
for key in ["twelve|1.43|40", "twelve|2.79|40", "twelve|12|40", "sixteen|4|40", "sixteen|12|40", "sixteen|4|80"]:
    a = np.array(best[key]['a']); cases.append((key, sol.ring_edges(len(a)), 1 + a, best[key]['D']))
cases.append(("twelve|12|40 sealed", sol.ring_edges(40), 1 + np.array(s12['a']), s12['D']))
for name, e, rho, auth in cases:
    p = 800 if len(rho) <= 2 else max(10, 1600 // len(rho))
    v = [sol.myD(e, rho, p=p), auth, sol.myD(e, rho, strike=0.3, p=p), sol.myD(e, rho, strike=0.7, p=p), sol.myD(e, rho, top=7.6, p=p), sol.myD(e, rho, c0=2**-0.5, p=p), sol.myD(e, rho, rolloff=False, p=p)]
    print("  %-28s" % name + " | ".join("%6.1f" % x for x in v))
for key in ["sixteen|4|40", "twelve|2.79|40"]:
    a = np.array(best[key]['a']); d, parts = sol.myD(sol.ring_edges(40), 1 + a, parts=True)
    print("  parts of D for %s: " % key + "; ".join("(%d,%d) %.3f w%.0f%% %.0fc" % (m, n, r, 100 * e, c) for r, m, n, e, c in parts if e > 0.005))
    print("    share of D's weight on partials above 5.5: %.1f%%; above 4.5: %.1f%%" % (100 * sum(e for r, m, n, e, c in parts if r > 5.5), 100 * sum(e for r, m, n, e, c in parts if r > 4.5)))
print("# t=%.0fs" % (time.time() - t0))
print("== E. the Maxwell fish-eye: smooth load a(r) = 4/(1+r^2)^2 - 1 (added mass 1 skin exactly); ratios of the 16 modes (FEM, 4000 cells)")
nodes = np.linspace(0, 1, 4001); rm = (nodes[1:] + nodes[:-1]) / 2; rho_e = 4 / (1 + rm**2)**2
modes = sol.fam_modes(7); need = sol.need_of(modes); om = {}
for m, nmax in need.items():
    w = sol.fem(nodes, rho_e, m, nmax)
    for n in range(1, nmax + 1): om[(m, n)] = np.sqrt(w[n - 1])
print("  " + ", ".join("(%d,%d) %.4f" % (m, n, om[(m, n)] / om[(0, 1)]) for m, n, f in modes))
print("  sqrt(l(l+1)/2) for l=1..7: " + ", ".join("%.4f" % np.sqrt(l * (l + 1) / 2) for l in range(1, 8)), "; added mass %.4f" % (np.sum((rho_e - 1) * (nodes[1:]**2 - nodes[:-1]**2))))
print("# t=%.0fs" % (time.time() - t0))
