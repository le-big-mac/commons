"""After the reading (25 November): the reader's new numbers recomputed with this folder's own code before they went into the note.
usage: after_check.py   (under -I)"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hours as H
st = H.starts()                       # every lunation 300 BC to 1 BC as a start
run = json.load(open(os.path.join(HERE, 'hours_run.json')))
print('keys of hours_run.json:', list(run)[:12])
g18 = H.glyphs_real(drop=('13S', '120M', '125M', '184M')); g22 = H.glyphs_real()
allk = [s[0] if isinstance(s, (list, tuple)) else s for s in st]
sc = [H.score(k, g18)[0] for k in allk]
print('starts:', len(sc), ' under 3.0 h:', sum(1 for x in sc if x < 3.0), ' one in', round(len(sc) / sum(1 for x in sc if x < 3.0), 1))
print('median %.2f' % sorted(sc)[len(sc) // 2])
for name, k in (('259 BC', -669), ('205 BC', 0), ('151 BC', 669)):
    a = H.score(k, g18); b = H.score(k, g22); c = H.score(k, g18, lon_range=(26.25, 26.25)); d = H.score(k, g22, lon_range=(26.25, 26.25))
    print(f'{name} (k={k}): 18 free {a[0]:.2f} h at {a[1]:+.2f}; 22 free {b[0]:.2f} h at {b[1]:+.2f}; at 26.25 E: 18 {c[0]:.2f}, 22 {d[0]:.2f}')
for name, k in (('223 BC', -223), ('205 BC', 0), ('187 BC', 223), ('169 BC', 446)):
    a = H.score(k, g18)
    print(f'{name}: {a[0]:.3f} h at {a[1]:+.2f}; with 8 h added the longitude is {((a[1] + 120 + 180) % 360) - 180:+.2f}, with 16 h {((a[1] + 240 + 180) % 360) - 180:+.2f}')

# Voulgaris, Mouratidis and Vossinakis: 22 or 23 December 178 BC, with the cells numbered one lower. The lunations about that date as starts.
import phases as P
def greg(jd):   # Julian-calendar date from a Julian day number
    z = int(jd + 0.5); f = jd + 0.5 - z; a = z; b = a + 1524; c = int((b - 122.1) / 365.25); d = int(365.25 * c); e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e) + f; mon = e - 1 if e < 14 else e - 13; yr = c - 4716 if mon > 2 else c - 4715
    return yr, mon, day
print('\nStarts about 22 December 178 BC (astronomical year -177):')
for k in allk:
    jd_full = P.true_phase(H.K0_FULL + k + 1)            # the full moon of month 1
    jd_new_before = P.true_phase(H.K0_FULL + k + 0.5)    # the new moon that begins month 1
    y, m, d = greg(jd_new_before)
    if (y, m) in ((-177, 11), (-177, 12)) or (y, m) == (-176, 1) or (y, m) == (-177, 10):
        a = H.score(k, g18); b = H.score(k, g22); c = H.score(k, g18, lon_range=(10, 40))
        y2, m2, d2 = greg(jd_full)
        print(f'  k={k}: month 1 begins at the new moon of {y}-{m:02d}-{d:05.2f}, full moon {y2}-{m2:02d}-{d2:05.2f}: 18 hours {a[0]:.2f} h at {a[1]:+.1f}; 22 hours {b[0]:.2f} h at {b[1]:+.1f}; 18 hours with 10 to 40 E {c[0]:.2f} h at {c[1]:+.1f}')
