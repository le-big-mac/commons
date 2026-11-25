"""Trial of the rulers on a made-up sky shaped like the real tables: the same two 76-year windows 2,231 years
apart, the same sampling, planets on ellipses (so the circle models have a floor), a Moon with evection and
variation, a precession between the two frames, and sky rates that differ from the gears' by planted amounts,
one of them more than half a turn (the wrap case)."""
import numpy as np
import gears, mech
from mech import D2R, wrap

T0, T1, SPAN = 1646667.5, 2461368.0, 27759.0
YS = 365.256363                      # days per turn of the made-up Sun against the made-up stars
PREC = 50.29 / 3600.0 / 365.25       # degrees per day, made-up precession (linear)
PLANT = {'moon': -261.0, 'apsides': -331.0, 'node': 2.0, 'mercury': -12.0, 'venus': 14.5, 'mars': 4.5,
         'jupiter': -1.7, 'saturn': -9.3}      # pointer minus sky after the span, against the stars
ORB = {'mercury': (0.387, 0.2056, 77.0), 'venus': (0.723, 0.0068, 131.0), 'earth': (1.0, 0.0167, 103.0),
       'mars': (1.524, 0.0934, 336.0), 'jupiter': (5.203, 0.0484, 14.0), 'saturn': (9.537, 0.0542, 93.0)}
PH0 = {'mercury': 40.0, 'venus': 200.0, 'earth': 310.0, 'mars': 95.0, 'jupiter': 250.0, 'saturn': 20.0}


def kepler(M, e):
    E = M.copy()
    for _ in range(12): E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def helio(name, L):
    a, e, w = ORB[name]
    M = (L - w) * D2R
    E = kepler(M, e)
    v = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    r = a * (1 - e * np.cos(E))
    return r * np.exp(1j * (v + w * D2R))


def make():
    tmid = {'then': T0 + SPAN / 2, 'now': T1 - SPAN / 2}
    dt = T1 - T0                                                  # the span the rulers measure over: edge to edge
    rs = 360.0 / YS
    dn = dt / YS                                                  # turns of the made-up Sun over the span
    def rate(gear, name):                                         # sky rate so that the planted drift results
        return (360.0 * float(gear) * dn - PLANT[name]) / dt
    r_moon, r_aps, r_node = rate(gears.MOON, 'moon'), rate(gears.APSIDES, 'apsides'), rate(gears.NODE, 'node')
    r_pl = {}
    for p in gears.SYNODIC:
        if p in gears.INFERIOR: r_pl[p] = rs + rate(gears.SYNODIC[p], p)      # heliocentric rate = Sun's + synodic
        else: r_pl[p] = rate(1 - gears.SYNODIC[p], p)
    sky = {}
    for w, (a, b) in (('then', (T0, T0 + SPAN)), ('now', (T1 - SPAN, T1))):
        sky[w] = {}
        for body in mech.BODIES:
            step = 1.0 / 3.0 if body == 'moon' else 1.0
            jd = a + step * np.arange(int(round((b - a) / step)) + 1)
            tau = jd - tmid['then']
            LE = PH0['earth'] + rs * tau
            E = helio('earth', LE)
            if body == 'sun':
                S = np.angle(-E) / D2R; lat = 0 * jd
            elif body == 'moon':
                L = 77.0 + r_moon * tau
                peri = 120.0 + r_aps * tau
                Om = 250.0 + r_node * tau
                M, D, Ms = (L - peri) * D2R, (L - (LE + 180.0)) * D2R, (LE - ORB['earth'][2]) * D2R
                S = L + 6.289 * np.sin(M) + 1.274 * np.sin(2 * D - M) + 0.658 * np.sin(2 * D) + 0.214 * np.sin(2 * M) - 0.186 * np.sin(Ms)
                lat = 5.128 * np.sin((S - Om) * D2R)
            else:
                P = helio(body, PH0[body] + r_pl[body] * tau)
                S = np.angle(P - E) / D2R; lat = 0 * jd
            sky[w][body] = dict(jd=jd, S=S % 360.0, T=(S + PREC * (jd - 2451545.0)) % 360.0, lat=lat)
    return sky, dt


if __name__ == '__main__':
    sky, dt = make()
    dp = PREC * dt
    print(f'made-up sky; span {dt / 365.25:.2f} Julian years; precession over it {dp:.3f} deg')
    for frame in ('S', 'T'):
        R = mech.analyse(sky, frame)
        print(f'\nframe {frame}: turns of b1 over the span {R["dn"]:.5f}')
        print('  drift (pointer minus sky, degrees): planted, recovered, difference')
        for k in ('moon', 'apsides', 'node', 'mercury', 'venus', 'mars', 'jupiter', 'saturn'):
            exp = PLANT[k]
            if frame == 'T':
                g = {'moon': gears.MOON, 'apsides': gears.APSIDES, 'node': gears.NODE}.get(k)
                if g is not None: exp += (float(g) - 1) * dp
                elif k in gears.INFERIOR: exp += float(gears.SYNODIC[k]) * dp
                else: exp -= float(gears.SYNODIC[k]) * dp
            print(f'   {k:8s} {exp:9.2f} {R["drift"][k]:9.2f} {R["drift"][k] - exp:7.2f}')
        print('  floors of the free fits, then | now: rms, max (degrees); fitted size')
        for b in mech.BODIES:
            ft, fn = R['fit']['then'][b], R['fit']['now'][b]
            a, c = mech.stats(ft['res']), mech.stats(fn['res'])
            size = ft.get('e', ft.get('rho'))
            print(f'   {b:8s} {a["rms"]:6.3f} {a["max"]:6.2f} | {c["rms"]:6.3f} {c["max"]:6.2f}   size {size:.4f}')
        err = mech.pointer_now(R, sky, frame)
        print('  the mechanism set in the first window and turned to the second: mean error, rms about it, max')
        for b in mech.BODIES:
            e = err[b]; m = np.mean(e)
            print(f'   {b:8s} {m:8.2f} {np.std(e):6.2f} {np.max(np.abs(e)):7.2f}')
