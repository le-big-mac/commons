"""Second reader's own glyph lists.
freeth(): from the words of Freeth 2014 (38 units a month, 446 an eclipse year, FM at 17, NM at 36 into the month,
node points at 66 (descending) and 289 (ascending), lunar within 20, solar within 20 north / 7 south, second of two
consecutive lunar months dropped). Written without looking at eym.py's arithmetic beyond the README's description.
ij_table5(path): Table 5 of Iversen & Jones 2019, parsed from the paper text itself."""
import re


def freeth(drop='second'):
    lunar, solar, info = [], [], {}
    for n in range(1, 224):
        for kind, off in (('L', 17), ('S', 36)):
            p = (38 * (n - 1) + off) % 446
            # signed distance to each node point
            dD = ((p - 66 + 223) % 446) - 223
            dA = ((p - 289 + 223) % 446) - 223
            if abs(dD) <= abs(dA): d, node = dD, 'D'
            else: d, node = dA, 'A'
            # Sun before the descending node point: for a NEW moon (Moon with the Sun) the Moon is still north; after it, south.
            # at the ascending node the other way round.  d == 0 counts as north (it is inside either limit anyway).
            north_new = (d <= 0) if node == 'D' else (d >= 0)
            if kind == 'L':
                if abs(d) <= 20: lunar.append(n); info[('L', n)] = (d, node)
            else:
                if abs(d) <= (20 if north_new else 7): solar.append(n); info[('S', n)] = (d, node, 'N' if north_new else 'S')
    cons = [(a, a + 1) for a in lunar if a + 1 in lunar]
    for a, b in cons:
        lunar.remove(b if drop == 'second' else a)
    return lunar, solar, info, cons


def ij_table5(path):
    """rows: (cell, lunar 'Y'/'N', lunar bracketed?, solar 'Y'/'N', solar bracketed?, solar queried?)"""
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    starts = [i for i, l in enumerate(lines) if l.startswith('Table 5')]
    rows = []
    pat = re.compile(r'^\s*(\d{1,3})\s+(\[?)(Yes|No)(\??)(\]?)\s+(\[?)(Yes|No)(\??)(\]?)\s+\S')
    for s in starts:
        for l in lines[s:s + 60]:
            if l.startswith('Table 5') and l is not lines[s]: break
            m = pat.match(l)
            if m:
                rows.append((int(m.group(1)), m.group(3)[0], bool(m.group(2)), m.group(7)[0], bool(m.group(6)), bool(m.group(8))))
            elif rows and (l.strip().startswith('a solar EP') or l.strip().startswith('We can now')):
                break
    return rows
