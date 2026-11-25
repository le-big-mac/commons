"""Checker's own tools (no phases.py, no hours.py, no mech.py, no dial.py).
 - read_h: parse a Horizons table (JD TT, apparent ecliptic longitude of date)
 - syz: full and new moons from the Moon and Sun tables by a cubic spline of the elongation and a root finder
 - catalogue: rows of NASA's eclipse catalogue pages (JD of greatest eclipse in TD, Delta T, lunation number, kind)
 - G22: the 22 hours typed by the checker from Carman and Evans's Table 11 (paper.txt lines 1868-1889), with their column "Time of day (h)"
"""
import re, os, math, glob
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

HZ = '/home/agent3/downloads/horizons-antikythera'
CAT = ['/home/agent3/downloads/nasa-eclipse-catalog', '/home/agent3/downloads/nasa-eclipse-catalog-2']


def read_h(path):
    jd, lon = [], []
    on = False
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            p = line.split(',')
            jd.append(float(p[0])); lon.append(float(p[5]))
    return np.array(jd), np.array(lon)


def syz(window='then'):
    jm, lm = read_h(os.path.join(HZ, f'moon_{window}.txt'))
    js, ls = read_h(os.path.join(HZ, f'sun_{window}.txt'))
    sun = CubicSpline(js, np.degrees(np.unwrap(np.radians(ls))))
    D = np.degrees(np.unwrap(np.radians(lm - sun(jm))))        # elongation, unwrapped, increasing
    f = CubicSpline(jm, D)
    full, new = [], []
    n0 = math.floor(D[0] / 180.0) + 1
    n1 = math.floor(D[-1] / 180.0)
    for n in range(n0, n1 + 1):
        target = 180.0 * n
        i = int(np.searchsorted(D, target))
        t = brentq(lambda x: f(x) - target, jm[i - 1], jm[i], xtol=1e-9)
        (new if n % 2 == 0 else full).append(t)
    return np.array(full), np.array(new)


MON = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)


def jd_julian(y, m, d):
    """Julian date at 0h of a Julian-calendar date (astronomical year numbering)."""
    if m <= 2: y -= 1; m += 12
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d - 1524.5


def catalogue(first=-299, last=0):
    rows = []
    for d in CAT:
        for path in sorted(glob.glob(os.path.join(d, '*.html'))):
            kind = os.path.basename(path)[:2]          # LE or SE
            m = re.match(r'(LE|SE)(-?\d{4})-(-?\d{4})', os.path.basename(path))
            lo, hi = int(m.group(2)), int(m.group(3))
            if hi < first or lo > last: continue
            for line in open(path, encoding='utf-8', errors='replace'):
                s = re.sub(r'<[^>]+>', '', line)
                mm = re.match(r'\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)', s)
                if not mm: continue
                y, mo, dd = int(mm.group(2)), MON[mm.group(3)], int(mm.group(4))
                h = int(mm.group(5)) + int(mm.group(6)) / 60 + int(mm.group(7)) / 3600
                rows.append(dict(kind=kind, y=y, mo=mo, d=dd, jd=jd_julian(y, mo, dd) + h / 24, dt=float(mm.group(8)), luna=int(mm.group(9)), saros=int(mm.group(10)), type=mm.group(11), td_h=h))
    rows.sort(key=lambda r: r['jd'])
    return rows


# Carman and Evans 2014, Table 11, typed by the checker from paper.txt lines 1868-1889:
# (cell, hour as engraved, d/n, their column "Time of day (h)")
T11 = [('13S', 1, 'd', 7), ('20M', 6, 'n', 0), ('25S', 6, 'd', 12), ('26M', 7, 'd', 13), ('78S', 1, 'd', 7), ('79M', 10, 'd', 16),
       ('114M', 12, 'd', 18), ('119S', 11, 'n', 5), ('120M', 6, 'd', 12), ('125M', 8, 'd', 14), ('125S', 3, 'd', 9), ('131M', 2, 'n', 20),
       ('131S', 9, 'n', 3), ('137M', 5, 'd', 11), ('137S', 12, 'd', 18), ('172M', 6, 'n', 24), ('172S', 12, 'd', 18), ('178M', 9, 'n', 3),
       ('178S', 9, 'd', 15), ('184M', 4, 'd', 10), ('184S', 1, 'd', 7), ('190M', 9, 'd', 15)]
OUT4 = ('13S', '120M', '125M', '184M')


def rule(n, dn):
    """Carman and Evans's rule (paper.txt 1775-1785): 1st hour of day 7h, 6th 12, 12th 18; 1st of night 19, 6th 24 or 0, 7th 1, 12th 6."""
    return (6 + n) % 24 if dn == 'd' else (18 + n) % 24


def glyphs(drop=()):
    return [(int(c[:-1]), c[-1], col % 24) for c, n, dn, col in T11 if c not in drop]


def wrap12(x): return (np.asarray(x) + 12.0) % 24.0 - 12.0


def best(am, ut, lons=None):
    """rms of wrap(am - ut - L/15) minimised over the longitude L (degrees east); grid of 0.05 deg."""
    if lons is None: lons = np.arange(-180, 180, 0.05)
    r = wrap12(np.asarray(am, float)[None, :] - np.asarray(ut, float)[None, :] - lons[:, None] / 15.0)
    rms = np.sqrt((r ** 2).mean(axis=1)); i = int(np.argmin(rms))
    return float(rms[i]), float(lons[i])
