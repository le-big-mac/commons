"""A long block of ice floating in sea water: statics of a rectangle, and crude dynamics.
usage: python berg.py statics results.json | python berg.py dynamics results.json
Units: H = 1 (the block's height when upright), g = 1, ice density = 1.  e = W/H.  d = 917/1025."""
import sys, json, math
import numpy as np
D = 917 / 1025
def clip_below(poly, h):
    """the part of a convex polygon (list of (x, y)) with y <= h"""
    out = []; n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]; pin, qin = p[1] <= h, q[1] <= h
        if pin: out.append(p)
        if pin != qin:
            t = (h - p[1]) / (q[1] - p[1]); out.append((p[0] + t * (q[0] - p[0]), h))
    return out
def area_centroid(poly):
    a = cx = cy = 0.0; n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]; x1, y1 = poly[(i + 1) % n]; c = x0 * y1 - x1 * y0; a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
    a *= 0.5
    return (a, cx / (6 * a), cy / (6 * a)) if abs(a) > 1e-15 else (0.0, 0.0, 0.0)
def corners(e, th, y=0.0):
    c, s = math.cos(th), math.sin(th); return [(c * x - s * yy, s * x + c * yy + y) for x, yy in ((-e / 2, -0.5), (e / 2, -0.5), (e / 2, 0.5), (-e / 2, 0.5))]
def floating(e, th, d=D):
    """water line height h above the centre of gravity, and the centre of buoyancy, with the share d of the area under water"""
    P = corners(e, th); lo = min(p[1] for p in P); hi = max(p[1] for p in P); target = d * e
    for _ in range(200):
        h = 0.5 * (lo + hi); a = area_centroid(clip_below(P, h))[0]
        if a < target: lo = h
        else: hi = h
    a, cx, cy = area_centroid(clip_below(P, h)); return h, cx, cy
def U(e, th, d=D):
    """height of the centre of gravity above the centre of buoyancy"""
    return -floating(e, th, d)[2]
def minima(e, d=D, n=3600):
    """stable tilts in [0, 90] degrees: local minima of U (U is even in the tilt and repeats every 180 degrees)"""
    ths = np.linspace(-0.5, 90.5, n + 1) * math.pi / 180; u = np.array([U(e, t, d) for t in ths]); out = []
    for i in range(1, n):
        if u[i] <= u[i - 1] and u[i] <= u[i + 1] and (u[i] < u[i - 1] or u[i] < u[i + 1]):
            a, b = ths[i - 1], ths[i + 1]; g = (math.sqrt(5) - 1) / 2
            for _ in range(80):
                c1, c2 = b - g * (b - a), a + g * (b - a)
                if U(e, c1, d) < U(e, c2, d): b = c2
                else: a = c1
            t = 0.5 * (a + b); t = 0.0 if abs(t) < 1e-6 else math.pi / 2 if abs(t - math.pi / 2) < 1e-6 else t
            if -1e-9 <= t <= math.pi / 2 + 1e-9: out.append((math.degrees(t), U(e, t, d)))
    return out
def stable_at(e, th0, d=D, eps=math.radians(0.2)):
    return U(e, th0 + eps, d) > U(e, th0, d)
def bisect(f, lo, hi, n=60):
    flo = f(lo)
    for _ in range(n):
        m = 0.5 * (lo + hi)
        if f(m) == flo: lo = m
        else: hi = m
    return 0.5 * (lo + hi)
def statics(R):
    print(f"d = {D:.6f}")
    t1 = bisect(lambda e: stable_at(e, 0.0), 0.5, 1.0); t2 = bisect(lambda e: stable_at(e, math.pi / 2), 1.0, 1.6)
    print(f"1. upright is stable for e above {t1:.5f} (metacentre: {math.sqrt(6 * D * (1 - D)):.5f}); on its side for e below {t2:.5f} (formula: {1 / math.sqrt(6 * D * (1 - D)):.5f})")
    print("2. stable attitudes by aspect ratio (tilt in degrees from upright; 90 is on its side)")
    table = []
    for e in (0.30, 0.50, 0.70, 0.72, 0.73, 0.735, 0.74, 0.745, 0.75, 0.76, 0.80, 1.00, 1.20, 1.32, 1.34, 1.50):
        m = minima(e); table.append((e, [round(t, 2) for t, _ in m])); print(f"   e = {e:.3f}: " + ", ".join(f"{t:.2f}" for t, _ in m))
    lean = [t for t, _ in minima(0.745) if 0.5 < t < 89.5]; print(f"3. at e = 0.745 the leaning attitude is at {lean[0]:.2f} degrees" if lean else "3. at e = 0.745 there is no leaning attitude")
    has_lean = lambda e: any(0.5 < t < 80 for t, _ in minima(e, n=1800)); lo, hi = 0.60, 0.745
    for _ in range(26):
        m = 0.5 * (lo + hi)
        if has_lean(m): hi = m
        else: lo = m
    e_end = 0.5 * (lo + hi); tl = [t for t, _ in minima(hi) if 0.5 < t < 80]
    print(f"4. leaning attitudes exist down to e = {e_end:.4f}, where the lean is {tl[0]:.1f} degrees; below that the block must roll right over. The top edge first goes under at a lean of {math.degrees(math.atan(2 * (1 - D) / e_end)):.1f} degrees there")
    ef = lambda e: e * (U(e, 0.0) - min(u for _, u in minima(e, n=900)))
    e5 = ef(0.5); print(f"5. energy set free at e = 0.5: {e5:.5f} (formula (1 - d) e (1 - e) / 2 = {(1 - D) * 0.25 / 2:.5f})")
    es = [round(0.05 + 0.01 * k, 2) for k in range(66)]; en = [ef(e) for e in es]; k = int(np.argmax(en)); print(f"6. over e from 0.05 to 0.70 the energy set free is greatest at e = {es[k]:.2f} ({en[k]:.5f})")
    print("   in the leaning range the energy set free by going from upright to the lean, and from upright to its side:")
    for e in (0.74, 0.745, 0.75):
        m = minima(e); l = [u for t, u in m if 0.5 < t < 80]; s = [u for t, u in m if t > 89.5]
        print(f"      e = {e}: to the lean {e * (U(e, 0.0) - l[0]):.6f}; to its side {e * (U(e, 0.0) - s[0]):.5f}" if l else f"      e = {e}: no lean")
    R.update(d=D, t_upright=t1, t_side=t2, lean_0745=lean[0] if lean else None, e_end=e_end, lean_at_end=tl[0], energy_05=e5, e_max=es[k], table=table, energies=list(zip(es, en)))
# ---------------------------------------------------------------- dynamics
def forces(e, y, th, d=D):
    """buoyancy (upward force) and its moment about the centre of gravity; water surface at height 0, centre of gravity at height y"""
    a, cx, cy = area_centroid(clip_below(corners(e, th, y), 0.0)); return a / d, cx * a / d
def run(e, th0_deg, T, dt=0.002, cy=0.0, cth=0.0, every=1):
    M = e; I = M * (e * e + 1) / 12; th = math.radians(th0_deg); y = -floating(e, th)[0]; vy = om = 0.0; out = []
    def acc(y, th, vy, om):
        F, tq = forces(e, y, th); return (F - M - cy * vy) / M, (tq - cth * om) / I
    n = int(round(T / dt))
    for k in range(n + 1):
        if k % every == 0: out.append((k * dt, y, th, vy, om))
        a1, b1 = acc(y, th, vy, om); a2, b2 = acc(y + 0.5 * dt * vy, th + 0.5 * dt * om, vy + 0.5 * dt * a1, om + 0.5 * dt * b1)
        a3, b3 = acc(y + 0.5 * dt * (vy + 0.5 * dt * a1), th + 0.5 * dt * (om + 0.5 * dt * b1), vy + 0.5 * dt * a2, om + 0.5 * dt * b2)
        a4, b4 = acc(y + dt * (vy + 0.5 * dt * a2), th + dt * (om + 0.5 * dt * b2), vy + dt * a3, om + dt * b3)
        y, th, vy, om = y + dt * (vy + dt * (a1 + a2 + a3) / 6), th + dt * (om + dt * (b1 + b2 + b3) / 6), vy + dt * (a1 + 2 * a2 + 2 * a3 + a4) / 6, om + dt * (b1 + 2 * b2 + 2 * b3 + b4) / 6
    return np.array(out)
def energy(e, row):
    t, y, th, vy, om = row; M = e; I = M * (e * e + 1) / 12; a, cx, cyy = area_centroid(clip_below(corners(e, th, y), 0.0))
    return 0.5 * M * vy * vy + 0.5 * I * om * om + M * y - (a / D) * cyy            # kinetic + weight's potential + the displaced water's
def dynamics(R):
    e = 0.5; tr = run(e, 1.0, 40.0); deg = np.degrees(tr[:, 2]); i90 = int(np.argmax(deg >= 90)) if (deg >= 90).any() else None
    E = np.array([energy(e, r) for r in tr[::500]]); GM = e * e / (12 * D) - (1 - D) / 2; sig = math.sqrt(-GM / ((e * e + 1) / 12))
    print(f"7. e = 0.5, released at 1 degree: growth rate by hand {sig:.4f}; first reaches 90 degrees at t = {tr[i90, 0]:.2f}" if i90 is not None else "7. never reaches 90 degrees")
    print(f"8. in 40 units of time the tilt reaches {deg.max():.1f} degrees at most; energy drifts by {abs(E - E[0]).max():.2e} (total at start {E[0]:.5f})")
    for dt in (0.004, 0.001):
        t2 = run(e, 1.0, 40.0, dt=dt); d2 = np.degrees(t2[:, 2]); j = int(np.argmax(d2 >= 90)); print(f"      with a step of {dt}: reaches 90 degrees at t = {t2[j, 0]:.2f}; greatest tilt {d2.max():.1f}")
    for th0 in (0.1, 5.0):
        t2 = run(e, th0, 60.0); d2 = np.degrees(t2[:, 2]); j = int(np.argmax(d2 >= 90)); print(f"      released at {th0} degrees: reaches 90 degrees at t = {t2[j, 0]:.2f}; greatest tilt in 60 units {d2.max():.1f}")
    for ee in (0.3, 0.7):
        t2 = run(ee, 1.0, 60.0); d2 = np.degrees(t2[:, 2]); j = int(np.argmax(d2 >= 90)); print(f"      e = {ee}: reaches 90 degrees at t = {t2[j, 0]:.2f}; greatest tilt in 60 units {d2.max():.1f}; heave between {t2[:, 1].min():+.3f} and {t2[:, 1].max():+.3f}")
    R.update(t90=float(tr[i90, 0]) if i90 is not None else None, max_tilt_40=float(deg.max()), sigma=sig)
if __name__ == "__main__":
    try: R = json.load(open(sys.argv[2]))
    except Exception: R = {}
    {"statics": statics, "dynamics": dynamics}[sys.argv[1]](R); json.dump(R, open(sys.argv[2], 'w'), indent=1)
