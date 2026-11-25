import numpy as np, sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fem import *

D = "/home/agent2/drumair/"
X0 = 2 * np.pi * 440 * 0.125 / 343.0
print("X0 =", X0, " pipe resonance in notes: pi/X0*2 =", 2 * np.pi / X0)


def tube_w(rho_fn, B, w11, n, Ns=400, depth=1.0):
    """n-th round mode with B -> B x cot x, x = X0*depth*w/w11, by fixed-point on the root index nearest continuation"""
    w = rich(Ns, rho_fn, B=B)[(0, n)]
    for it in range(60):
        x = X0 * depth * w / w11
        wn = rich(Ns, rho_fn, B=B * x / np.tan(x))[(0, n)]
        if abs(wn - w) < 1e-10:
            break
        w = 0.5 * w + 0.5 * wn
    return w


print("--- the 1954 disc read as density 9.77 (load a = 8.77) inside 0.4")
d = disc_rho(8.77, 0.4)
wv = rich(400, d, B=0.0)
w11 = wv[(1, 1)]
print("w11 %.5f  B_ref %.4f  vacuum place %.4f" % (w11, CREF * w11**2, report(wv)["place"]))
for nm, f in (("reference", 1.0), ("doubled", 0.5), ("halved", 2.0)):
    ww = rich(400, d, B=None, cref=CREF * f)
    print("  %-10s B %.4f place %.4f  (0,2) %+.2f%%  (0,3) %+.2f%%  (0,3) in notes %.3f" % (nm, ww["B"], report(ww)["place"], 100 * (ww[(0, 2)] / wv[(0, 2)] - 1), 100 * (ww[(0, 3)] / wv[(0, 3)] - 1), 2 * ww[(0, 3)] / w11))
Bref = CREF * w11**2
wt = [tube_w(d, Bref, w11, n) for n in (1, 2, 3)]
print("  tube: place %.4f ; (0,2) %.3f notes; (0,3) %.3f notes (vac %.3f)" % (2 * wt[0] / w11, 2 * wt[1] / w11, 2 * wt[2] / w11, 2 * wv[(0, 3)] / w11))
# air mass, crude: 0.265 added evenly, on the round modes only / on all modes
for add in (0.265,):
    dd = lambda N: d(N) + add
    wm0 = rich(400, dd, B=Bref)
    wsp = rich(400, d, B=Bref)
    print("  +0.265 even mass: (0,1) falls %.2f%%, (1,1) falls %.2f%%, place %.4f -> %.4f" % (100 * (1 - wm0[(0, 1)] / wsp[(0, 1)]), 100 * (1 - wm0[(1, 1)] / wsp[(1, 1)]), 2 * wsp[(0, 1)] / wsp[(1, 1)], 2 * wm0[(0, 1)] / wm0[(1, 1)]))
print("--- plain skin on the reference drum")
p = disc_rho(0, 0.5)
ww = rich(400, p, B=None)
print("  B %.3f place %.4f (vac %.4f)" % (ww["B"], report(ww)["place"], 2 * 2.404825558 / 3.831705970))
print("--- every ref-*.json, recomputed (N = 320/640 Richardson)")
edges = np.linspace(0, 1, 41)
area = edges[1:] ** 2 - edges[:-1] ** 2
for f in sorted(glob.glob(D + "ref-*.json")):
    j = json.load(open(f))
    a = np.array(j["a"])
    a = np.where(a < 1e-9, 0, a)
    ww = rich(320, ring_rho(a), B=None, cref=CREF / j["volume"])
    r = report(ww)
    mine = dict(tuned=r["missB"], free=r["missA"], tabla=max(r["missA"], abs(r["place"] / 1.10 - 1)))[j["kind"]]
    flag = "" if abs(mine - j["exact"]) < 3e-6 and abs(r["place"] - j["place"]) < 2e-5 and abs(r["B"] - j["B"]) < 2e-5 else "  <-- DIFFERS"
    print("%-24s author %.4f%% place %.4f B %.4f used %.3f | mine %.4f%% place %.4f B %.4f mass %.3f inside0.5 %.3f max a %.0f%s" % (
        os.path.basename(f), 100 * j["exact"], j["place"], j["B"], j["used"], 100 * mine, r["place"], r["B"], area @ a, area[:20] @ a[:20], a.max(), flag))
    if os.path.basename(f) in ("ref-free-4-1.json", "ref-tabla-6-1.json", "ref-tuned-4-1.json"):
        # tube, and crude air mass on this load
        w11 = ww[(1, 1)]
        wt = [tube_w(ring_rho(a), r["B"], w11, n, Ns=320) for n in (1, 3)]
        wm = rich(320, lambda N: ring_rho(a)(N) + 0.265, B=r["B"])
        print("      tube: place %.4f, (0,3) %.3f notes (spring %.3f) -> overtone miss with tube %.2f%% ; +0.265 even: place %.4f, (0,1) falls %.2f%%, (1,1) falls %.2f%%" % (
            2 * wt[0] / w11, 2 * wt[1] / w11, 2 * ww[(0, 3)] / w11, 100 * abs(2 * wt[1] / w11 / 5 - 1), 2 * wm[(0, 1)] / wm[(1, 1)], 100 * (1 - wm[(0, 1)] / ww[(0, 1)]), 100 * (1 - wm[(1, 1)] / ww[(1, 1)])))
