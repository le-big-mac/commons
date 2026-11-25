# Referee control: is the model velocity field incompressible?  Divergence by central differences.
import numpy as np
from flow import vel, rods
n = 3; sig2 = 0.35 ** 2; e = 1e-5
xs = np.linspace(-0.5, 4.5, 501); ys = np.linspace(-2, 2, 401)
X, Y = np.meshgrid(xs, ys); P = np.stack([X.ravel(), Y.ravel()], 1)
for u in (0.25, 0.5, 0.75):
    mv = (1, True)
    f = lambda Q: vel(Q, n, mv, u, sig2)
    dvx = (f(P + [e, 0])[:, 0] - f(P - [e, 0])[:, 0]) / (2 * e)
    dvy = (f(P + [0, e])[:, 1] - f(P - [0, e])[:, 1]) / (2 * e)
    cx = (f(P + [e, 0])[:, 1] - f(P - [e, 0])[:, 1]) / (2 * e) - (f(P + [0, e])[:, 0] - f(P - [0, e])[:, 0]) / (2 * e)
    div = dvx + dvy
    Pr, Vr = rods(n, mv, u)
    sp = np.hypot(*f(P).T)
    print(f"u={u}: rod speed {np.hypot(*Vr[0]):.3f}; max fluid speed on grid {sp.max():.3f}; max |div v| {np.abs(div).max():.3f}; "
          f"max |curl v| {np.abs(cx).max():.3f}; fluid velocity at rods minus rod velocity: {np.abs(f(Pr) - Vr).max():.2e}")
