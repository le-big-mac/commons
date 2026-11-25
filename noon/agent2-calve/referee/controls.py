# Referee's controls (step 2). Uses only the referee's own geometry from blind.py.
import sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/calve/referee')
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import solve_ivp
import blind as B

D = B.D
rad = math.radians


def run(e, th0deg=1.0, T=40.0, dy0=0.0, fric=0.0, n=None):
    M = e; I = M * (e * e + 1) / 12.0; th0 = rad(th0deg); y0 = B.float_at(e, th0)[0] + dy0

    def rhs(t, s):
        y, th, vy, w = s
        A, cx, cy = B.sub(e, th, y)
        return [vy, w, (A / B.D - M) / M - fric * vy, cx * A / B.D / I - fric * w]
    sol = solve_ivp(rhs, (0, T), [y0, th0, 0, 0], method='DOP853', rtol=1e-10, atol=1e-12, dense_output=True, max_step=0.05)
    ts = np.linspace(0, T, n or int(T * 200) + 1)
    return ts, sol.sol(ts)


def energy(e, s):
    y, th, vy, w = s; M = e; I = M * (e * e + 1) / 12.0
    A, cx, cy = B.sub(e, th, y)
    return 0.5 * M * vy * vy + 0.5 * I * w * w + M * y - A * cy / B.D


which = sys.argv[1:] or list('abcdefgh')

if 'a' in which:
    print('a. In the leaning range: is a block let go near upright caught by the lean, or does it go over the barrier?')
    print('   e, lean, h(0)-h(lean), barrier tilt, h(barrier)-h(0)  [negative: barrier lower than upright]')

    def barrier(e):
        ms = [a for a, b in B.minima(e) if 0.01 < a < 80]
        if not ms: return None
        lean = ms[0]
        res = minimize_scalar(lambda t: -B.h(e, rad(t)), bounds=(lean, 89.0), method='bounded', options={'xatol': 1e-8})
        return lean, B.h(e, 0.0) - B.h(e, rad(lean)), res.x, -res.fun - B.h(e, 0.0)
    for e in (0.7515, 0.75, 0.7475, 0.745, 0.7425, 0.74, 0.738, 0.737, 0.7364):
        print('  ', e, ['%.6g' % v for v in barrier(e)])
    es = brentq(lambda e: barrier(e)[3], 0.7364, 0.7515, xtol=1e-8)
    print('   barrier is as high as upright at e = %.5f (lean there %.2f, barrier at %.2f deg)' % (es, barrier(es)[0], barrier(es)[2]))
    print('   dynamics, no friction, let go at 1 degree (and 0.1), T = 600: greatest tilt, time of first passing 45 deg')
    for e in (0.75, 0.748, 0.747, 0.746, 0.745, 0.744, 0.742, 0.74, 0.737):
        for a0 in (1.0, 0.1):
            ts, S = run(e, a0, 600.0, n=60001); deg = np.degrees(S[1]); i = np.argmax(deg >= 45)
            print('   e %.3f from %.1f deg: greatest tilt %.2f, least %.3f, first passes 45 deg at t = %s' % (e, a0, deg.max(), deg.min(), ('%.1f' % ts[i]) if deg.max() >= 45 else 'never'))

if 'b' in which:
    print('b. e = 0.5: the energy not in the attitude at the greatest tilt')
    e = 0.5; ts, S = run(e, 1.0, 40.0, n=400001); k = int(np.argmax(S[1])); s = S[:, k]
    freed = (1 - D) * e * (1 - e) / 2; E0 = energy(e, S[:, 0])
    kh = 0.5 * e * s[2] ** 2; kr = 0.5 * e * (e * e + 1) / 12 * s[3] ** 2
    yeq, hth, _ = B.float_at(e, s[1])
    print('   t = %.3f tilt %.2f; y = %.4f, floating depth at that tilt %.4f; vy = %.4f, omega = %.5f' % (ts[k], math.degrees(s[1]), s[0], yeq, s[2], s[3]))
    print('   total E0 = %.6f = M h(1 deg) = %.6f ; M h(0) = %.6f' % (E0, e * B.h(e, rad(1.0)), e * B.h(e, 0.0)))
    print('   M h(tilt) = %.6f ; so heave energy (kinetic + potential) = E0 - M h(tilt) - KE_turn = %.6f = %.1f%% of the energy set free' % (e * hth, E0 - e * hth - kr, 100 * (E0 - e * hth - kr) / freed))
    print('   of which kinetic %.6f (%.1f%%), potential (off its floating depth) %.6f (%.1f%%)' % (kh, 100 * kh / freed, E0 - e * hth - kr - kh, 100 * (E0 - e * hth - kr - kh) / freed))
    print('   check h(180 - x) = h(x):', B.h(e, rad(148.66)), B.h(e, rad(31.34)))
    # deepest point of the block during the roll
    low = []
    for j in range(0, S.shape[1], 50):
        y, th = S[0, j], S[1, j]
        low.append(min(u * math.sin(th) + v * math.cos(th) + y for u in (-e / 2, e / 2) for v in (-0.5, 0.5)))
    print('d. deepest point of the block in 40 units: %.4f block heights below the water (upright draught %.4f); statics along the roll:' % (-min(low), D), end=' ')
    dd = []
    for t in np.linspace(0, 90, 181):
        yc = B.float_at(e, rad(t))[0]; dd.append((min(u * math.sin(rad(t)) + v * math.cos(rad(t)) + yc for u in (-e / 2, e / 2) for v in (-0.5, 0.5)), t))
    print('deepest %.4f at tilt %.1f' % (-min(dd)[0], min(dd)[1]))

if 'c' in which:
    print('c. e = 0.5, long runs without friction: greatest tilt by window')
    for a0 in (1.0, 0.99, 1.01):
        ts, S = run(0.5, a0, 1000.0, n=100001); deg = np.degrees(S[1])
        print('   from %.2f deg:' % a0, ', '.join('T=%d: %.1f' % (T, deg[ts <= T].max()) for T in (40, 60, 150, 400, 1000)), '; least tilt after t=15: %.2f' % deg[ts > 15].min(), '; energy drift %.1e' % (energy(0.5, S[:, -1]) - energy(0.5, S[:, 0])))
    for e, T in ((0.3, 60), (0.3, 150), (0.7, 60), (0.7, 150), (0.4, 40), (0.4, 150)):
        ts, S = run(e, 1.0, float(T)); print('   e = %.1f, T = %d: greatest tilt %.1f' % (e, T, np.degrees(S[1]).max()))
    print('   e = 0.5 let go at 1 deg but not at its floating depth:')
    for dy in (0.01, -0.01, 0.05, -0.05):
        ts, S = run(0.5, 1.0, 40.0, dy0=dy); deg = np.degrees(S[1]); i = np.argmax(deg >= 90)
        print('     start %+.2f off its depth: 90 deg at t = %.2f; greatest tilt in 40: %.1f' % (dy, ts[i], deg.max()))

if 'e' in which:
    print('e. minima at e = 0.736 exactly:', [(round(float(a), 3)) for a, b in B.minima(0.736)], ' at 0.7363:', [(round(float(a), 3)) for a, b in B.minima(0.7363)], ' at 0.7365:', [(round(float(a), 3)) for a, b in B.minima(0.7365)])
    print('   corner goes under on the lean branch at e = sqrt(6d(1-d) - 2(1-d)^2) = %.6f' % math.sqrt(6 * D * (1 - D) - 2 * (1 - D) ** 2))

if 'f' in which:
    print('f. the film\'s leaning block: e = 0.745, let go at 3 deg, friction 0.22 on both velocities')
    ts, S = run(0.745, 3.0, 300.0, fric=0.22); deg = np.degrees(S[1])
    for T in (30, 60, 100, 150, 200, 300):
        k = int(np.argmin(abs(ts - T))); print('   t = %d: tilt %.2f, turning at %.5f deg per unit' % (T, deg[k], math.degrees(S[3, k])))
    print('   rest lean 11.04; first within 0.1 deg of it at t = %.0f' % ts[np.argmax(deg > 10.94)])
    ts, S = run(0.5, 2.0, 60.0, fric=0.22); deg = np.degrees(S[1]); print('   e = 0.5 from 2 deg with the friction: 90 deg at t = %.1f, greatest %.1f, at t = 60: %.1f' % (ts[np.argmax(deg >= 90)], deg.max(), deg[-1]))
    ts, S = run(0.5, 2.0, 60.0); deg = np.degrees(S[1]); print('   e = 0.5 from 2 deg without it: 90 deg at t = %.1f, greatest %.1f' % (ts[np.argmax(deg >= 90)], deg.max()))

if 'g' in which:
    print('g. other shares under water: upright threshold and the end of the lean (referee\'s fold finder)')

    def gmax(e):
        ths = np.linspace(0.5, 80.0, 796); gs = np.array([-B.xb(e, rad(t)) for t in ths]); i = int(np.argmax(gs))
        res = minimize_scalar(lambda t: B.xb(e, rad(t)), bounds=(ths[max(i - 1, 0)], ths[min(i + 1, 795)]), method='bounded', options={'xatol': 1e-9})
        return -res.fun
    for dd in (0.85, 0.88, 0.90, 0.92):
        B.D = dd; up = math.sqrt(6 * dd * (1 - dd)); ef = brentq(gmax, up - 0.06, up - 1e-4, xtol=1e-8)
        print('   d = %.2f: upright above %.4f; lean down to %.4f; width %.4f' % (dd, up, ef, up - ef))
    B.D = D

if 'h' in which:
    H = 800.0; unit = 917 * 9.81 * H ** 3; E = (1 - D) * 0.25 / 2 * unit
    print('h. 800 m: unit %.4e J/m; e = 0.5: %.4e J/m; per km %.4e J = %.2f kt; sqrt(H/g) = %.4f s; 10.336 units = %.1f s' % (unit, E, E * 1000, E * 1000 / 4.184e12, math.sqrt(H / 9.81), 10.336 * math.sqrt(H / 9.81)))
    print('   growth rate by hand at e = 0.5: %.4f; ln(10)/rate = %.3f; acosh(90)/rate = %.2f' % (math.sqrt((0.5 * (1 - D) - 0.25 / (12 * D)) / (1.25 / 12)), math.log(10) / math.sqrt((0.5 * (1 - D) - 0.25 / (12 * D)) / (1.25 / 12)), math.acosh(90) / math.sqrt((0.5 * (1 - D) - 0.25 / (12 * D)) / (1.25 / 12))))
