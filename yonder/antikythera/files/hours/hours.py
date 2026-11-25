"""The hours engraved on the eclipse dial's glyphs against the real times of full and new moon, for any start of the dial.
usage: hours.py trial          a made-up dial: glyph hours taken from a known start, with noise, then looked for
       hours.py real           the 22 hours of Carman and Evans (2014), Table 11, for every start from 300 BC to 1 BC

For a start k (lunations from the full moon of 12 May 205 BC; k = 0 is that start), month n of the dial holds full moon
number k + n and then the new moon after it. A glyph's hour is set against the local time of that full moon (lunar glyph) or
new moon (solar glyph): UT + longitude/15, with UT = TT - DeltaT. One number is free for each start, the longitude, since the
dial does not say where it was made for; the score is the root-mean-square difference (hours, each wrapped to +-12) at the
longitude that makes it least. Syzygy times are Meeus's (phases.py, within 2.5 minutes of JPL's tables in 205-129 BC)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from phases import true_phase

K0_FULL = -27257 + 0.5        # Meeus's k of the full moon of month 1 at start k = 0 is K0_FULL + 1 (checked in main against 12 May 205 BC)


def delta_t(year):
    """TT - UT in seconds, Espenak and Meeus's polynomial for years -500 to +500 (typed from memory; tested in main against the catalogue's column)."""
    u = year / 100.0
    return 10583.6 - 1014.41 * u + 33.78311 * u ** 2 - 5.952053 * u ** 3 - 0.1798452 * u ** 4 + 0.022174192 * u ** 5 + 0.0090316521 * u ** 6


def year_of(jd):
    return -4712 + (jd + 0.5) / 365.25


def syzygy_ut_hours(k, month, kind):
    """UT of the full (kind 'M') or following new (kind 'S') moon of dial month `month` at start k, as a Julian date."""
    kk = K0_FULL + k + month + (0.5 if kind == 'S' else 0.0)
    jde = true_phase(kk)
    return jde - delta_t(year_of(jde)) / 86400.0


def wrap(x): return (np.asarray(x) + 12.0) % 24.0 - 12.0


def score(k, glyphs, lon_range=None, step=0.25):
    """glyphs: list of (month, kind, hour on a 24-hour clock). Returns (rms hours, best longitude east in degrees)."""
    ut = np.array([((syzygy_ut_hours(k, m, kind) + 0.5) % 1.0) * 24.0 for m, kind, h in glyphs])
    am = np.array([h for m, kind, h in glyphs], dtype=float)
    lons = np.arange(-180, 180, step) if lon_range is None else np.arange(lon_range[0], lon_range[1] + 1e-9, step)
    r = wrap(am[None, :] - ut[None, :] - lons[:, None] / 15.0)
    rms = np.sqrt((r ** 2).mean(axis=1)); i = int(np.argmin(rms))
    return float(rms[i]), float(lons[i])


# Carman and Evans 2014, Table 11: month, Moon or Sun, hour as engraved (d = of the day, n = of the night)
TABLE11 = """13S 1d; 20M 6n; 25S 6d; 26M 7d; 78S 1d; 79M 10d; 114M 12d; 119S 11n; 120M 6d; 125M 8d; 125S 3d; 131M 2n; 131S 9n;
137M 5d; 137S 12d; 172M 6n; 172S 12d; 178M 9n; 178S 9d; 184M 4d; 184S 1d; 190M 9d"""


def glyphs_real(drop=()):
    out = []
    for item in TABLE11.replace('\n', ' ').split(';'):
        a, b = item.split(); month, kind = int(a[:-1]), a[-1]; n, dn = int(b[:-1]), b[-1]
        if a in drop: continue
        out.append((month, kind, (6 + n) % 24 if dn == 'd' else (18 + n) % 24))        # their rule: 1st hour of day = 7h, 1st of night = 19h
    return out


def starts(first_bc=300, last_bc=1):
    ks = []
    for k in range(-1300, 2800):
        y = 1 - math.floor(year_of(true_phase(K0_FULL + k + 1)))
        if last_bc <= y <= first_bc: ks.append(k)
    return ks


if __name__ == '__main__':
    jd1 = true_phase(K0_FULL + 1)
    print(f'full moon of month 1 at k = 0: JDE {jd1:.3f} (12 May 205 BC is JD 1646678.5 to 1646679.5); DeltaT there {delta_t(year_of(jd1)):.0f} s (the catalogue has 12775 s for June 205 BC, 12592 for August 190 BC: {delta_t(-189.4):.0f})')
    if sys.argv[1] == 'trial':
        rng = np.random.default_rng(7)
        K = starts()
        for ktrue, lon, noise in ((0, 25.0, 0.0), (0, 25.0, 2.5), (716, 25.0, 2.5), (-223, 140.0, 2.5)):
            months = [(m, kind) for m, kind, h in glyphs_real()]
            g = []
            for m, kind in months:
                t = ((syzygy_ut_hours(ktrue, m, kind) + 0.5) % 1.0) * 24.0 + lon / 15.0 + rng.normal(0, noise)
                g.append((m, kind, round(t) % 24))                                    # engraved to the whole hour
            sc = sorted((score(k, g)[0], k) for k in K)
            mine = score(ktrue, g)
            print(f'TRIAL planted start k = {ktrue}, longitude {lon}, noise {noise} h: its rms {mine[0]:.2f} h at longitude {mine[1]:+.1f}; rank {1 + [k for _, k in sc].index(ktrue)} of {len(K)}; '
                  f'best five (rms, k): {[(round(a, 2), b) for a, b in sc[:5]]}; median rms over all starts {np.median([a for a, _ in sc]):.2f}')
