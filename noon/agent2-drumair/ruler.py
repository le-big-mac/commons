"""The ruler, tried before use.   usage: python -u ruler.py OUT.json
1. the plain skin with air as a spring: the closed form  w^2 J0(w) + pi B J2(w) = 0  against the exact matching and against finite differences
2. a disc with air: exact matching against finite differences; B -> 0 against the vacuum
3. the derivative of each miss with respect to a ring's load against a difference quotient, with air
4. the tube: its limit of a shallow cavity is the spring"""
import sys, json, math
import numpy as np
from scipy.optimize import brentq
from scipy.special import jv, jn_zeros
import airlib as A
L = A.L; out = {}
print("1. The plain skin, air as a spring: the first three round modes (frequency over the vacuum's)"); out['plain'] = []
j0 = jn_zeros(0, 4)
for B in (0.5, 1.0, 2.0):
    closed = [brentq(lambda w: w * w * jv(0, w) + math.pi * B * jv(2, w), j0[n] * (1 + 1e-9), j0[n + 1] * (1 - 1e-9), xtol=1e-13) for n in range(3)]
    ex = A.round_modes([1.0], [1.0], B, 3); sk = A.AirSkin(40, [(0, 1), (0, 2), (0, 3)], B); sk.solve(np.zeros(40), grad=False); fd = list(sk.W)
    out['plain'].append(dict(B=B, closed=closed, exact=ex, fd=fd, rise=[closed[n] / j0[n] - 1 for n in range(3)]))
    print(f"   B = {B:g}: closed form " + ", ".join(f"{closed[n] / j0[n]:.6f}" for n in range(3)) + "; exact matching differs by at most " + f"{max(abs(a / b - 1) for a, b in zip(ex, closed)):.1e}" + "; finite differences by at most " + f"{max(abs(a / b - 1) for a, b in zip(fd, closed)):.1e}")
print("2. The 1954 disc (9.77 times over 0.4) with air as a spring: exact matching against finite differences on 40 rings (the disc's edge is on a ring's edge)"); out['disc'] = []
sk0 = L.Skin(40, L.NINE); a = L.disc(sk0, 8.77, 0.4); e, r = A.disc_pieces(9.77, 0.4); round3 = [(0, 1), (0, 2), (0, 3)]
for B in (0.0, 1e-6, 0.5, 1.0, 2.0):
    ex = A.round_modes(e, r, B, 3); sk = A.AirSkin(40, round3, B); sk.solve(a, grad=False); fd = list(sk.W); out['disc'].append(dict(B=B, exact=ex, fd=fd))
    print(f"   B = {B:g}: exact " + ", ".join(f"{x:.6f}" for x in ex) + "; finite differences differ by at most " + f"{max(abs(p / q - 1) for p, q in zip(fd, ex)):.1e}")
print("3. Derivatives with air (B = 1): each miss with respect to the load of rings 3, 9 and 20, against a difference quotient")
rng = np.random.default_rng(3); a = rng.uniform(0, 12, 40) * (np.arange(40) < 22); sk = A.AirSkin(40, L.NINE, 1.0); c, J = sk.solve(a); worst = 0.0
for j in (3, 9, 20):
    d = np.zeros(40); d[j] = 1e-2; num = (sk.solve(a + d, grad=False) - sk.solve(a - d, grad=False)) / 2e-2; worst = max(worst, float(np.abs(num - J[:, j]).max()))
out['derivative'] = worst; print(f"   largest difference {worst:.1e} with a step of 0.01 (the derivatives themselves are up to {np.abs(J).max():.1e}; with smaller steps the quotient is noisier, 1.5e-05 at a step of 1e-05, because the eigenvalues are good to about 1e-9)")
print("4. The tube with a shallow cavity is the spring: the 1954 disc, B = 1, lowest mode"); out['tube'] = []
for X in (1e-4, 0.1, 0.3):
    t = A.tube_modes(e, r, 1.0, X, 2.0)[0]; s = A.round_modes(e, r, 1.0, 1)[0]; out['tube'].append(dict(X=X, tube=t, spring=s)); print(f"   X = {X:g}: tube {t:.6f}, spring {s:.6f}")
print("5. The pole-free condition has the same spring roots: the 1954 disc, B = 1")
sp = A.round_modes(e, r, 1.0, 3); hh = [brentq(A._H, w * (1 - 1e-6), w * (1 + 1e-6), args=(e, r, 1.0)) for w in sp]; out['polefree'] = max(abs(p / q - 1) for p, q in zip(hh, sp)); print(f"   largest relative difference {out['polefree']:.1e}")
print("6. Derivatives when the air's strength follows the load (RefSkin, added after the referee's report): each miss with respect to the load of rings 2, 8, 15 and 21, against a difference quotient with a step of 0.01"); out['refskin'] = {}
FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; a2 = np.random.default_rng(5).uniform(0, 12, 40) * (np.arange(40) < 22)
for kind, modes, free in (("all nine, the lowest as the note", L.NINE, False), ("the lowest aimed at 1.10 and seven overtones", [(1, 1), (0, 1)] + FIVE[1:], True)):
    sk = A.RefSkin(40, modes, free=free)
    if free: sk.T[1] = 0.55
    c, J = sk.solve(a2); worst = 0.0
    for j in (2, 8, 15, 21):
        d = np.zeros(40); d[j] = 1e-2; num = (sk.solve(a2 + d, grad=False) - sk.solve(a2 - d, grad=False)) / 2e-2; worst = max(worst, float(np.abs(num - J[:, j]).max()))
    out['refskin'][kind] = dict(worst=worst, size=float(np.abs(J).max())); print(f"   {kind}: largest difference {worst:.1e} (the derivatives are up to {np.abs(J).max():.1e})")
json.dump(out, open(sys.argv[1], "w"))
