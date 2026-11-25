"""What the author's own hours_after.py section C would print with cell 72 read as Iversen and Jones's edition has it (Sun, n[ighttime],
2nd hour), using the author's hours.py unchanged (so the numbers are those the mended script will give). Also 120M at one longitude."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, hours
SIXTEEN = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
OUT4 = ('13S', '120M', '125M', '184M')
g22 = hours.glyphs_real(); g18 = hours.glyphs_real(drop=OUT4)
conv = lambda n, dn: (6 + n) % 24 if dn == 'd' else (18 + n) % 24
def variant(extra, changed):
    g = [(m, kind, conv(*changed[f'{m}{kind}']) if f'{m}{kind}' in changed else h) for m, kind, h in g22]
    return g + [(m, kind, conv(n, dn)) for (m, kind, n, dn) in extra]
CH = {'120M': (12, 'd'), '119S': (12, 'n')}
for name, extra in (('26 hours, 72S 2n, 8S 1d', [(8, 'M', 2, 'd'), (8, 'S', 1, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'n')]),
                    ('26 hours, 72S 2n, 8S 4d', [(8, 'M', 2, 'd'), (8, 'S', 4, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'n')])):
    g = variant(extra, CH)
    row = {bc: hours.score(k, g) for bc, k in SIXTEEN.items() if bc in (223, 205, 187, 169)}
    rest = min(hours.score(k, g)[0] for bc, k in SIXTEEN.items() if bc not in (223, 205, 187, 169))
    print(f'{name}: ' + '; '.join(f'{bc} BC {v[0]:.2f} h at {v[1]:+.0f}' for bc, v in row.items()) + f'; best of the other twelve {rest:.2f} h; 259 BC {hours.score(-669, g)[0]:.2f} at {hours.score(-669, g)[1]:+.0f}')
    s0, lon = hours.score(0, g)
    for m, kind, h in g:
        if f'{m}{kind}' in ('120M', '119S', '8M', '8S', '67M', '72S'):
            ut = ((hours.syzygy_ut_hours(0, m, kind) + 0.5) % 1.0) * 24.0
            print(f'     at 205 BC ({lon:+.2f} E), {m}{kind}: engraved {h} h, difference {float(hours.wrap(h - ut - lon / 15)):+.2f}')
# at the longitude of the 18 (26.25 E): the six, as Carman and Evans read them and as Iversen and Jones do
s, lon = hours.score(0, g18)
print(f'\nat the longitude of the 18 ({lon} E):')
for c, m, kind, n, dn in (('120M as 6d (C&E)', 120, 'M', 6, 'd'), ('120M as 12d (I-J, queried)', 120, 'M', 12, 'd'), ('119S as 11n (C&E)', 119, 'S', 11, 'n'), ('119S as 12n (I-J)', 119, 'S', 12, 'n'),
                          ('8M 2d', 8, 'M', 2, 'd'), ('8S 1d', 8, 'S', 1, 'd'), ('8S 4d', 8, 'S', 4, 'd'), ('67M 8n', 67, 'M', 8, 'n'), ('72S 2n (I-J)', 72, 'S', 2, 'n'), ('72S 2d (as the README has it)', 72, 'S', 2, 'd'), ('72S 5n (Jones 2020)', 72, 'S', 5, 'n')):
    ut = ((hours.syzygy_ut_hours(0, m, kind) + 0.5) % 1.0) * 24.0
    print(f'     {c}: {float(hours.wrap(conv(n, dn) - ut - lon / 15)):+.2f}')
# whole cycles -3, 0, +3 at fixed 26.25 E with the author's ruler
for k, b in ((-669, 259), (0, 205), (669, 151)):
    print(f'{b} BC at 26.25 E exactly: 18 hours {hours.score(k, g18, lon_range=(26.25, 26.25))[0]:.2f}; 22 hours {hours.score(k, g22, lon_range=(26.25, 26.25))[0]:.2f}; free: 18 {hours.score(k, g18)}, 22 {hours.score(k, g22)}')
# Exeligmos settings, author's ruler, longitude free
for b, k in ((223, -223), (205, 0), (187, 223), (169, 446)):
    r = []
    for add in (0, 8, 16):
        g = [(m, kind, (h + add) % 24) for m, kind, h in g18]; v = hours.score(k, g); r.append(f'+{add} h: {v[0]:.2f} at {v[1]:+.1f}')
    print(f'{b} BC, engraved hours with the Exeligmos dial\'s hours added: ' + '; '.join(r))
