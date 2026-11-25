"""The referee's controls, redone here.   usage: python after2.py"""
import math, numpy as np
import berg
D = berg.D
print("A. The barrier between the lean and lying on its side, against the height at upright")
def barrier(e):
    ths = np.radians(np.linspace(0, 90, 1801)); u = np.array([berg.U(e, t) for t in ths]); m = berg.minima(e, n=1800); lean = [t for t, _ in m if 0.5 < t < 80]
    if not lean: return None
    i0 = int(round(lean[0] * 20)); return float(u[i0:].max() - u[0]), lean[0], float(np.degrees(ths[i0 + int(np.argmax(u[i0:]))]))
for e in (0.737, 0.740, 0.742, 0.7425, 0.743, 0.745, 0.750):
    b = barrier(e); print(f"   e = {e:.4f}: lean {b[1]:5.2f} degrees; barrier at {b[2]:5.2f} degrees stands {b[0]:+.2e} above upright")
lo, hi = 0.737, 0.750
for _ in range(30):
    m = 0.5 * (lo + hi)
    if barrier(m)[0] < 0: lo = m
    else: hi = m
estar = 0.5 * (lo + hi); print(f"   the barrier is level with upright at e = {estar:.5f}: below that, a block let go at rest near upright has the energy to pass it")
print(f"   the top corner goes under on the lean at e = {math.sqrt(6 * D * (1 - D) - 2 * (1 - D) ** 2):.5f} (the sealed sheet has 0.7375), at a lean of {math.degrees(math.atan(2 * (1 - D) / math.sqrt(6 * D * (1 - D) - 2 * (1 - D) ** 2))):.2f} degrees")
print("B. Let go at rest at 1 degree, no friction, 600 units of time (step 0.004): the least and greatest tilt")
for e in (0.737, 0.740, 0.742, 0.744, 0.745, 0.750):
    tr = berg.run(e, 1.0, 600.0, dt=0.004, every=5); d = np.degrees(tr[:, 2]); print(f"   e = {e:.3f}: tilt between {d.min():.1f} and {d.max():.1f} degrees")
print("C. The same block as in the sealed lines (e = 0.5), run for longer")
tr = berg.run(0.5, 1.0, 60.0, dt=0.002); d = np.degrees(tr[:, 2]); om = tr[:, 4]; turns = [i for i in range(1, len(om)) if om[i - 1] * om[i] < 0]
print("   turning points in the first 40 units: " + ", ".join(f"{d[i]:.1f} at t = {tr[i, 0]:.1f}" for i in turns if tr[i, 0] <= 40))
i90 = int(np.argmax(d >= 90)); print(f"   as it first passes 90 degrees (t = {tr[i90, 0]:.2f}) it is turning at {math.degrees(om[i90]):.0f} degrees a unit")
for th0, T in ((0.5, 400.0), (1.0, 1000.0), (2.0, 1000.0)):
    tr = berg.run(0.5, th0, T, dt=0.004, every=5); d = np.degrees(tr[:, 2]); j = int(np.argmax(d >= 170)) if (d >= 170).any() else None
    print(f"   let go at {th0} degrees, {T:.0f} units: greatest tilt {d.max():.1f}; " + (f"first passes 170 at t = {tr[j, 0]:.0f}" if j is not None else "never passes 170") + f"; greatest in the first 40 units {d[tr[:, 0] <= 40].max():.1f}")
print("D. The energy in rising and sinking at the top of the second swing (e = 0.5)")
e = 0.5; tr = berg.run(e, 1.0, 25.0); k = int(np.argmax(np.degrees(tr[:, 2]))); t, y, th, vy, om = tr[k]; M = e
h_eq = berg.floating(e, th)[0]; y_eq = -h_eq
def pot(yy):
    a, cx, cy = berg.area_centroid(berg.clip_below(berg.corners(e, th, yy), 0.0)); return M * yy - (a / D) * cy
freed = (1 - D) * e * (1 - e) / 2; kin = 0.5 * M * vy * vy; pp = pot(y) - pot(y_eq)
print(f"   tilt {math.degrees(th):.1f} at t = {t:.2f}: kinetic {kin:.5f} ({100 * kin / freed:.1f}% of {freed:.5f}); it is {y - y_eq:+.3f} from its floating depth at that tilt, worth {pp:.5f} ({100 * pp / freed:.1f}%); together {100 * (kin + pp) / freed:.1f}%")
print("E. How deep the lowest corner goes (e = 0.5; the upright block draws %.3f of its height)" % D)
tr = berg.run(0.5, 1.0, 40.0, dt=0.004); low = min(min(p[1] for p in berg.corners(0.5, th, y)) for _, y, th, _, _ in tr[::5]); ths = np.radians(np.linspace(0, 90, 361)); lows = [min(p[1] for p in berg.corners(0.5, t, -berg.floating(0.5, t)[0])) for t in ths]
print(f"   in the run: {-low:.3f} of the height; at rest at every tilt from 0 to 90: at most {-min(lows):.3f}. For 800 m: {-low * 800:.0f} m and {-min(lows) * 800:.0f} m, against {D * 800:.0f} m upright")
print("F. Friction and the lean (e = 0.745 let go at 3 degrees, friction 0.22 as in the film): the tilt at times 30, 60, 90")
M = 0.745; I = M * (M * M + 1) / 12; tr = berg.run(0.745, 3.0, 90.0, dt=0.004, cy=0.22 * M, cth=0.22 * I, every=25); d = np.degrees(tr[:, 2])
print("   " + ", ".join(f"{d[int(np.argmin(abs(tr[:, 0] - tt)))]:.2f} at t = {tt}" for tt in (30, 60, 90)) + "; the lean at rest is 11.04")
M = 0.5; I = M * (M * M + 1) / 12; a = berg.run(0.5, 2.0, 30.0, dt=0.004, cy=0.22 * M, cth=0.22 * I); b = berg.run(0.5, 2.0, 30.0, dt=0.004)
print(f"   e = 0.5 let go at 2 degrees: passes 90 degrees at t = {a[int(np.argmax(np.degrees(a[:, 2]) >= 90)), 0]:.1f} with the film's friction, {b[int(np.argmax(np.degrees(b[:, 2]) >= 90)), 0]:.1f} without")
