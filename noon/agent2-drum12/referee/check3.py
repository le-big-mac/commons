import sys; sys.path.insert(0, "/home/agent2/drum12/referee")
import numpy as np, json, hashlib
import sol
D12 = "/home/agent2/drum12/"; best = json.load(open(D12 + "best.json"))
print("sha256 of expectations.md:", hashlib.sha256(open(D12 + "expectations.md", "rb").read()).hexdigest()); print("expectations.sha256:      ", open(D12 + "expectations.sha256").read().strip())
for nm in ("sixteen-4", "sixteen-12", "twelve-12", "twelve-2.79"):
    d = json.load(open(D12 + "after-R-%s.json" % nm)); a = np.array(d['a']); s = nm.split("-"); k40 = np.array(best["%s|%s|40" % (s[0], s[1])]['a']); k80 = np.array(best["%s|%s|80" % (s[0], s[1])]['a'])
    print("heaviest ring, %s: 40 rings %.0f, 80 rings %.0f, 160 rings %.0f; its mass in skins: %.3f, %.3f, %.3f" % (nm, k40.max(), k80.max(), a.max(), (k40 * sol.ring_w(40)).max(), (k80 * sol.ring_w(80)).max(), (a * sol.ring_w(160)).max()))
c = sol.misses(np.array([0.4004, 1.0]), np.array([9.938, 1.0]), sol.fam_modes(6), 400, True); print("nine-mode disc (9.938, 0.4004) over twelve modes: %.3f%%" % (100 * np.abs(c).max()))
modes = sol.fam_modes(6); a0 = np.array(best["twelve|9.6|80"]['a']); a0 = a0 * 6.0 / (sol.ring_w(80) @ a0)
a, f = sol.slp(a0, modes, 6.0, p=10, iters=300); a, f = sol.slp(a, modes, 6.0, p=10, iters=30, exact=True, tr0=0.05)
c = sol.misses(sol.ring_edges(80), 1 + a, modes, 20, exact=True); print("twelve modes, 80 rings, 6 skins from the author's 9.6-skin load scaled: %.4f%% exact, mass %.4f, min load %.3g" % (100 * np.abs(c).max(), sol.ring_w(80) @ a, a.min()))
json.dump(dict(a=a.tolist(), exact=float(np.abs(c).max())), open("/home/agent2/drum12/referee/twelve_6_80_referee.json", "w"))
for k in ("twelve", "sixteen"):
    for R in ("40", "80"):
        W = ["1", "1.43", "1.6", "1.8", "2", "2.2", "2.4", "2.79", "4", "6", "9.6", "12"]; v = [best["%s|%s|%s" % (k, w, R)]['exact'] for w in W]
        bad = [(W[i], W[i + 1]) for i in range(len(W) - 1) if v[i + 1] > v[i]]; print("table column %s, %s rings: rises with more weight allowed at: %s" % (k, R, bad or "nowhere"))
