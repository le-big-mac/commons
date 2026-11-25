"""Checks made after the sealed lines were scored.   usage: python after.py"""
import math, numpy as np
import berg
D = berg.D
print("A. Where the energy of the roll goes (e = 0.5, released at 1 degree, no friction)")
e = 0.5; tr = berg.run(e, 1.0, 40.0); M = e; I = M * (e * e + 1) / 12
kr = 0.5 * I * tr[:, 4] ** 2; kh = 0.5 * M * tr[:, 3] ** 2; tot = np.array([berg.energy(e, r) for r in tr[::200]]); pot = tot[0] - (kr + kh)[::200]
i = int(np.argmax(kr)); j = int(np.argmax(kh)); k = int(np.argmax(np.degrees(tr[:, 2])))
print(f"   energy set free in all (upright to on its side): {(1 - D) * e * (1 - e) / 2:.5f}")
print(f"   kinetic energy of turning is greatest at t = {tr[i, 0]:.2f} (tilt {math.degrees(tr[i, 2]):.0f} degrees): {kr[i]:.5f}; of rising and sinking at t = {tr[j, 0]:.2f}: {kh[j]:.5f}")
print(f"   at the greatest tilt ({math.degrees(tr[k, 2]):.1f} degrees, t = {tr[k, 0]:.2f}) the block is turning at {tr[k, 4]:+.4f} and rising at {tr[k, 3]:+.3f}: energy of rising and sinking {kh[k]:.5f}; its centre of gravity is {tr[k, 1]:+.3f} from the water line (at rest upright {-berg.floating(e, 0.0)[0]:+.3f}, on its side {-berg.floating(e, math.pi / 2)[0]:+.3f})")
print(f"   upside down (180 degrees) at rest would need all of the energy back in the attitude; share then in rising and sinking: {100 * kh[k] / ((1 - D) * e * (1 - e) / 2):.0f}% of the energy set free")
print("B. The same with the block held at its floating depth at every instant (turning only): how far does it swing?")
def run1(e, th0_deg, T, dt=0.002):
    I = (e * e + 1) / 12; th = math.radians(th0_deg); om = 0.0; out = []
    def acc(th):
        h, cx, cy = berg.floating(e, th); return cx * 1.0 / I            # buoyancy equals the weight (mass e, per unit mass 1): moment cx * e / (e * I)
    for k in range(int(T / dt) + 1):
        out.append((k * dt, th, om)); a1 = acc(th); a2 = acc(th + 0.5 * dt * om); a3 = acc(th + 0.5 * dt * (om + 0.5 * dt * a1)); a4 = acc(th + dt * (om + 0.5 * dt * a2))
        th, om = th + dt * (om + dt * (a1 + a2 + a3) / 6), om + dt * (a1 + 2 * a2 + 2 * a3 + a4) / 6
    return np.array(out)
t1 = run1(0.5, 1.0, 40.0, dt=0.004); d1 = np.degrees(t1[:, 1]); j = int(np.argmax(d1 >= 90))
print(f"   turning only: reaches 90 degrees at t = {t1[j, 0]:.2f}; greatest tilt in 40 units {d1.max():.1f} degrees")
print("C. Time to roll over against the first tilt (e = 0.5), and against the aspect ratio (released at 1 degree)")
for th0 in (0.01, 0.1, 1, 5, 10):
    t2 = berg.run(0.5, th0, 60.0, dt=0.004); d2 = np.degrees(t2[:, 2]); print(f"   first tilt {th0:5.2f} degrees: 90 degrees at t = {t2[int(np.argmax(d2 >= 90)), 0]:6.2f}")
for ee in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.73):
    t2 = berg.run(ee, 1.0, 150.0, dt=0.004); d2 = np.degrees(t2[:, 2]); GM = ee * ee / (12 * D) - (1 - D) / 2; print(f"   e = {ee:.2f}: 90 degrees at t = {t2[int(np.argmax(d2 >= 90)), 0]:6.2f}; growth rate by hand {math.sqrt(-GM / ((ee * ee + 1) / 12)):.3f}; greatest tilt {d2.max():.1f}")
print("D. In real units, for a block 800 m tall (sqrt(H/g) = %.2f s; ice 917 kg/m3)" % math.sqrt(800 / 9.81))
H = 800.0; unit = 917 * 9.81 * H ** 3
for ee in (0.3, 0.5, 0.7):
    E = (1 - D) * ee * (1 - ee) / 2 * unit; print(f"   e = {ee}: width {ee * H:.0f} m; energy set free {E:.2e} J per metre of length; for a block 1 km long {E * 1000:.2e} J, {E * 1000 / 4.184e12:.0f} kilotons of TNT")
print("E. The leaning range for other densities of ice and water (d), from the same code")
for dd in (0.85, 0.88, D, 0.90, 0.92):
    up = berg.bisect(lambda e: berg.stable_at(e, 0.0, dd), 0.5, 1.0); has = lambda e: any(0.5 < t < 80 for t, _ in berg.minima(e, dd, n=900)); lo, hi = 0.5, up - 1e-4
    for _ in range(20):
        m = 0.5 * (lo + hi)
        if has(m): hi = m
        else: lo = m
    print(f"   d = {dd:.4f}: upright stable above {up:.4f}; leaning down to {0.5 * (lo + hi):.4f}")
