"""Does the catalogue's own lunation number give the dial month? Checked on the two centuries where the JPL tables give the month.
usage: luna_check.py DATADIR CATDIR   (under -I through runpy)"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, dial, mech
DATA, CAT = sys.argv[1], sys.argv[2]
MON = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
def jd_julian(y, m, d):
    if m <= 2: y -= 1; m += 12
    return np.floor(365.25 * (y + 4716)) + np.floor(30.6001 * (m + 1)) + d - 1524.5
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)')
moon = mech.read(os.path.join(DATA, 'moon_then.txt')); sun = mech.read(os.path.join(DATA, 'sun_then.txt'))
sz = dial.syzygies(moon, sun); ft, nt = sz['full'][0], sz['new'][0]
for pre, times, isnew in (('LE', ft, False), ('SE', nt, True)):
    diffs = {}
    for name in (f'{pre}-0299--0200.html', f'{pre}-0199--0100.html'):
        for line in open(os.path.join(CAT, name), encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if not m: continue
            t = jd_julian(int(m.group(2)), MON[m.group(3)], int(m.group(4))) + (int(m.group(5)) + int(m.group(6)) / 60 + int(m.group(7)) / 3600) / 24
            if not (ft[0] - 1 <= t <= ft[-1] - 30): continue
            k = int(np.argmin(np.abs(times - t)))
            n = int(np.searchsorted(ft, times[k])) if isnew else k + 1
            diffs[n - int(m.group(9))] = diffs.get(n - int(m.group(9)), 0) + 1
    print(pre, 'dial month minus the catalogue\'s lunation number, and how many eclipses give it:', diffs)
