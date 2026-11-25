"""Item 2: the ruler by the checker's own route. Full and new moons from the JPL tables (own spline root finder),
Delta T interpolated from the catalogue rows, own scoring. Starts the 'then' tables reach."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, own

full, new = own.syz('then')
print(f'full moons {len(full)}, new moons {len(new)}; first full moon JD(TT) {full[0]:.4f} (12 May 205 BC = JD 1646678.5 to 1646679.5); first new {new[0]:.4f}')
cat = own.catalogue(-299, 0)
cj = np.array([r['jd'] for r in cat]); cd = np.array([r['dt'] for r in cat])
print(f'catalogue rows {len(cat)} from year {cat[0]["y"]} to {cat[-1]["y"]}; Delta T {cd[0]:.0f} to {cd[-1]:.0f} s')
dT = lambda jd: np.interp(jd, cj, cd)

def ut_hours(k, month, kind):
    """UT (hours of the day) of the full moon of dial month `month` at start k, or of the new moon after it."""
    t = full[k + month - 1]
    if kind == 'S':
        t = new[np.searchsorted(new, t)]          # the new moon after that full moon
    ut = t - dT(t) / 86400.0
    return ((ut + 0.5) % 1.0) * 24.0, t

def score(k, g, lons=None):
    ut = [ut_hours(k, m, kind)[0] for m, kind, h in g]
    return own.best([h for m, kind, h in g], ut, lons)

g22 = own.glyphs(); g18 = own.glyphs(drop=own.OUT4)
README = {0: (2.56, 26, 3.91, 36), 223: (2.52, -89, 4.18, -79), 270: (6.31, -145, 6.21, -147), 446: (2.63, 156, 4.38, 150), 493: (6.44, 101, 6.34, 98), 716: (6.56, -33, 6.43, -34)}
print('\nstart: my 18 (rms h, longitude E) | README 18 || my 22 | README 22')
res = {}
for k, bc in ((0, 205), (223, 187), (270, 183), (446, 169), (493, 165), (716, 147)):
    a = score(k, g18); b = score(k, g22); r = README[k]
    res[k] = (a, b)
    print(f'  {bc} BC k={k:4d}: {a[0]:.3f} h at {a[1]:+7.2f} | {r[0]:.2f} at {r[1]:+d} || {b[0]:.3f} h at {b[1]:+7.2f} | {r[2]:.2f} at {r[3]:+d}')

# the Greek-world range for these six
print('\nlongitude kept to 10..40 E, the 18:')
for k, bc in ((0, 205), (223, 187), (270, 183), (446, 169), (493, 165), (716, 147)):
    a = score(k, g18, np.arange(10, 40.0001, 0.05)); print(f'  {bc} BC: {a[0]:.2f} h at {a[1]:+.1f}')

# glyph by glyph at 205 BC at 26.2 E (the README's longitude) and at my own best longitude
s, lon = res[0][0]
print(f'\n205 BC glyph by glyph: engraved, UT of the syzygy (h), difference at my best longitude {lon:+.2f} E, and at 26.25 E')
rows = {}
for m, kind, h in g22:
    ut, t = ut_hours(0, m, kind)
    d = float(own.wrap12(h - ut - lon / 15)); d2 = float(own.wrap12(h - ut - 26.25 / 15))
    rows[f'{m}{kind}'] = (h, ut, d, d2, t)
    print(f'  {m:3d}{kind} {h:2d} h  UT {ut:6.2f}  {d:+6.2f}  {d2:+6.2f}' + ('  (set aside)' if f'{m}{kind}' in own.OUT4 else ''))
d18 = [rows[c][3] for c in rows if c not in own.OUT4]
print(f'  the 18 at 26.25 E: from {min(d18):+.2f} to {max(d18):+.2f}')

# lunar and solar apart
for name, kk in (('9 lunar', 'M'), ('9 solar', 'S')):
    g = [x for x in g18 if x[1] == kk]; v = score(0, g); print(f'205 BC {name}: {len(g)} hours, {v[0]:.2f} h at {v[1]:+.1f}')
# lunar and solar at the joint best longitude
for name, kk in (('9 lunar', 'M'), ('9 solar', 'S')):
    d = [rows[f'{m}{kind}'][2] for m, kind, h in g18 if kind == kk]; print(f'   at the joint longitude {lon:+.2f}: {name} rms {np.sqrt(np.mean(np.square(d))):.2f} h')

# Table 16 of Carman and Evans: typed by the checker from paper.txt lines 2994-3021: cell, AM time, lunation, TD, DeltaT, UT, AM-UT
T16 = [('20M', 0, -27237, '2:18:04', 12758, -1.24, 1.24), ('26M', 13, -27231, '14:18:45', 12752, 10.77, 2.23), ('79M', 16, -27178, '18:01:27', 12700, 14.50, 1.50),
       ('114M', 18, -27143, '18:56:57', 12666, 15.43, 2.57), ('131M', 20, -27126, '0:22:07', 12649, 20.86, -0.86), ('137M', 11, -27120, '12:40:18', 12643, 9.16, 1.84),
       ('172M', 24, -27085, '0:44:45', 12609, 21.24, 2.76), ('178M', 3, -27079, '2:28:11', 12604, -1.03, 4.03), ('190M', 15, -27067, '17:49:16', 12592, 14.32, 0.68),
       ('25S', 12, -27231, '16:47:22', 12752, 13.25, -1.25), ('78S', 7, -27178, '5:59:42', 12700, 2.47, 4.53), ('119S', 5, -27137, '1:33:19', 12660, -1.96, 6.96),
       ('125S', 9, -27131, '11:04:05', 12655, 7.55, 1.45), ('131S', 3, -27125, '2:10:48', 12649, -1.33, 4.33), ('137S', 18, -27119, '1:16:17', 12643, 21.76, -3.76),
       ('172S', 18, -27084, '23:07:08', 12609, 19.62, -1.62), ('178S', 15, -27078, '14:44:22', 12603, 11.24, 3.76), ('184S', 7, -27072, '10:29:38', 12597, 6.99, 0.01)]
x = np.array([r[6] for r in T16])
print(f'\nTable 16, column AM-UT, 18 rows: mean {x.mean():.3f} h = {x.mean() * 15:.1f} deg E; sd about the mean (n) {x.std():.3f} h, (n-1) {x.std(ddof=1):.3f} h; rms about zero {np.sqrt((x ** 2).mean()):.3f}')
print('   their own statements: L = 1.69 h = 25.3 deg; RMS discrepancy 2.52 h (paper.txt 3043, 3062, 2402)')
# their rows against the catalogue rows and against my syzygies
bykey = {(r['kind'], r['luna']): r for r in cat}
print('   cell: their UT | UT from the catalogue row | UT of my JPL syzygy | (greatest eclipse - syzygy, min) | their AM-UT | my difference at L=0 | mine - theirs')
dd = []
for c, am, luna, td, dt, ut, amut in T16:
    r = bykey.get(('LE' if c.endswith('M') else 'SE', luna))
    h = r['td_h'] - r['dt'] / 3600 if r else float('nan')
    mine_ut = rows[c][1]
    m0 = float(own.wrap12(am - mine_ut))
    dd.append(m0 - amut)
    tcat = (r['jd'] - rows[c][4]) * 1440 if r else float('nan')
    print(f'   {c:5s} {ut:6.2f} | {h % 24 if h>12 else h:6.2f} (dT cat {r["dt"] if r else 0:.0f}, theirs {dt}) | {mine_ut:6.2f} | {tcat:+6.1f} | {amut:+5.2f} | {m0:+5.2f} | {m0 - amut:+5.2f}')
dd = np.array(dd)
print(f'   mine - theirs over the 18: mean {dd.mean():+.3f} h, rms {np.sqrt((dd**2).mean()):.3f} h, largest {np.abs(dd).max():.2f} h')
json.dump({str(k): v for k, v in res.items()}, open(os.path.join(HERE, 'c2_ruler.json'), 'w'))
