"""Times of true new and full moon from Meeus, Astronomical Algorithms, chapter 49 ("Phases of the Moon"), typed from
memory of the algorithm and therefore TESTED below against syzygies found in JPL's tables before anything rests on it.
k is the lunation number: integer for new moon, integer + 0.5 for full moon; k = 0 is the new moon of 6 January 2000.
Returns JDE (dynamical time)."""
import math
R = math.radians


def true_phase(k):
    T = k / 1236.85
    JDE = (2451550.09766 + 29.530588861 * k + 0.00015437 * T * T - 0.000000150 * T ** 3 + 0.00000000073 * T ** 4)
    E = 1 - 0.002516 * T - 0.0000074 * T * T
    M = R(2.5534 + 29.10535670 * k - 0.0000014 * T * T - 0.00000011 * T ** 3)
    Mp = R(201.5643 + 385.81693528 * k + 0.0107582 * T * T + 0.00001238 * T ** 3 - 0.000000058 * T ** 4)
    F = R(160.7108 + 390.67050284 * k - 0.0016118 * T * T - 0.00000227 * T ** 3 + 0.000000011 * T ** 4)
    Om = R(124.7746 - 1.56375588 * k + 0.0020672 * T * T + 0.00000215 * T ** 3)
    full = abs(k - math.floor(k) - 0.5) < 1e-6
    s = math.sin
    if not full:
        c = (-0.40720 * s(Mp) + 0.17241 * E * s(M) + 0.01608 * s(2 * Mp) + 0.01039 * s(2 * F) + 0.00739 * E * s(Mp - M)
             - 0.00514 * E * s(Mp + M) + 0.00208 * E * E * s(2 * M) - 0.00111 * s(Mp - 2 * F) - 0.00057 * s(Mp + 2 * F)
             + 0.00056 * E * s(2 * Mp + M) - 0.00042 * s(3 * Mp) + 0.00042 * E * s(M + 2 * F) + 0.00038 * E * s(M - 2 * F)
             - 0.00024 * E * s(2 * Mp - M) - 0.00017 * s(Om) - 0.00007 * s(Mp + 2 * M) + 0.00004 * s(2 * Mp - 2 * F)
             + 0.00004 * s(3 * M) + 0.00003 * s(Mp + M - 2 * F) + 0.00003 * s(2 * Mp + 2 * F) - 0.00003 * s(Mp + M + 2 * F)
             + 0.00003 * s(Mp - M + 2 * F) - 0.00002 * s(Mp - M - 2 * F) - 0.00002 * s(3 * Mp + M) + 0.00002 * s(4 * Mp))
    else:
        c = (-0.40614 * s(Mp) + 0.17302 * E * s(M) + 0.01614 * s(2 * Mp) + 0.01043 * s(2 * F) + 0.00734 * E * s(Mp - M)
             - 0.00515 * E * s(Mp + M) + 0.00209 * E * E * s(2 * M) - 0.00111 * s(Mp - 2 * F) - 0.00057 * s(Mp + 2 * F)
             + 0.00056 * E * s(2 * Mp + M) - 0.00042 * s(3 * Mp) + 0.00042 * E * s(M + 2 * F) + 0.00038 * E * s(M - 2 * F)
             - 0.00024 * E * s(2 * Mp - M) - 0.00017 * s(Om) - 0.00007 * s(Mp + 2 * M) + 0.00004 * s(2 * Mp - 2 * F)
             + 0.00004 * s(3 * M) + 0.00003 * s(Mp + M - 2 * F) + 0.00003 * s(2 * Mp + 2 * F) - 0.00003 * s(Mp + M + 2 * F)
             + 0.00003 * s(Mp - M + 2 * F) - 0.00002 * s(Mp - M - 2 * F) - 0.00002 * s(3 * Mp + M) + 0.00002 * s(4 * Mp))
    # the fourteen planetary arguments
    A = [299.77 + 0.107408 * k - 0.009173 * T * T, 251.88 + 0.016321 * k, 251.83 + 26.651886 * k, 349.42 + 36.412478 * k, 84.66 + 18.206239 * k,
         141.74 + 53.303771 * k, 207.14 + 2.453732 * k, 154.84 + 7.306860 * k, 34.52 + 27.261239 * k, 207.19 + 0.121824 * k,
         291.34 + 1.844379 * k, 161.72 + 24.198154 * k, 239.56 + 25.513099 * k, 331.55 + 3.592518 * k]
    W = [0.000325, 0.000165, 0.000164, 0.000126, 0.000110, 0.000062, 0.000060, 0.000056, 0.000047, 0.000042, 0.000040, 0.000037, 0.000035, 0.000023]
    return JDE + c + sum(w * s(R(a)) for w, a in zip(W, A))


if __name__ == '__main__':
    # test against JPL: usage phases.py DATADIR   (the Sun and Moon tables of the Antikythera study; run with -I through runpy)
    import sys, os
    sys.path.insert(0, '/home/agent3/antikythera'); sys.path.insert(0, '/home/agent3/antikythera/dial')
    import numpy as np, mech, dial
    for w in ('then', 'now'):
        moon = mech.read(os.path.join(sys.argv[1], f'moon_{w}.txt')); sun = mech.read(os.path.join(sys.argv[1], f'sun_{w}.txt'))
        sz = dial.syzygies(moon, sun)
        for kind, off in (('new', 0.0), ('full', 0.5)):
            t = sz[kind][0]
            k0 = round((t[0] - 2451550.09766) / 29.530588861 - off) + off
            d = np.array([(true_phase(k0 + i) - t[i]) * 24 * 60 for i in range(len(t))])
            assert np.all(np.abs(d) < 12 * 60), 'lunations out of step'
            print(f'{w} {kind} moons: {len(t)}; Meeus minus JPL table (minutes): mean {d.mean():+.1f}, rms {np.sqrt((d ** 2).mean()):.1f}, largest {np.abs(d).max():.1f}')
