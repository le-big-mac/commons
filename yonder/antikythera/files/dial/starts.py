"""After the fact (not sealed): is the fit to the sky particular to the start of 205 BC?
For every lunation as a possible month 1, from 300 BC to 1 BC, the same catalogue count over the 223 months that follow:
A = lunar glyph months with a lunar eclipse of any kind, S = solar glyph months with a solar eclipse,
U = partial or total lunar eclipses in months without a lunar glyph, N = solar eclipses whose shadow passed north of
the Earth's centre (gamma > 0) in months without a solar glyph. k = 0 is the full moon of 12 May 205 BC.
usage: starts.py CATDIR [CATDIR ...]     (run under -I through runpy)"""
import sys, os, re, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import dial, ij2019
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)\s+\S+\s+(-?\d+\.\d+)')


def read_cat(prefix, add):
    rows = {}
    for f in sorted(f for d in sys.argv[1:] for f in glob.glob(os.path.join(d, prefix + '*.html'))):
        for line in open(f, encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if m: rows[int(m.group(9)) + add] = (m.group(11)[0], float(m.group(12)))
    return rows


def year_of(k):                      # the year (BC) of the full moon k lunations from 12 May 205 BC, by the mean month
    jd = 1646679.21 + 29.530589 * k
    y = -4712 + (jd + 0.5) / 365.25  # Julian years from 1 January 4713 BC
    return 1 - math.floor(y)


LE, SE = read_cat('LE', 27257), read_cat('SE', 27256)
fl, fs = dial.glyph_months()
K = [k for k in range(-1250, 2700) if 1 <= year_of(k) <= 300]
print(f'{len(K)} possible starts, {year_of(K[0])} BC to {year_of(K[-1])} BC')
for name, L, S in (('Freeth 2014', sorted(fl), sorted(fs)), ('Iversen and Jones 2019', ij2019.LUNAR, ij2019.SOLAR)):
    sc = {}
    for k in K:
        A = sum(k + n in LE for n in L); Sn = sum(k + n in SE for n in S)
        U = sum(1 for n in range(1, 224) if k + n in LE and LE[k + n][0] in 'PT' and n not in L)
        N = sum(1 for n in range(1, 224) if k + n in SE and SE[k + n][1] > 0 and n not in S)
        sc[k] = (A, Sn, U, N)
    a0, s0, u0, n0 = sc[0]
    good3 = [k for k in K if sc[k][0] >= a0 and sc[k][1] >= s0 and sc[k][2] <= u0]
    good = [k for k in good3 if sc[k][3] <= n0]
    best = max(sc[k][0] + sc[k][1] for k in K)
    print(f'\n{name}: the start of 205 BC scores A {a0} of {len(L)}, S {s0} of {len(S)}, U {u0}, N {n0}')
    print(f'  starts that score at least as well on A, S and U: {len(good3)} of {len(K)}; on all four: {len(good)}')
    print('    k (year BC; whole Saros cycles and months over):', ', '.join(f'{k} ({year_of(k)}; {k // 223 if k >= 0 else -((-k) // 223)} and {k - 223 * (k // 223 if k >= 0 else -((-k) // 223))})' for k in good))
    print(f'  best A + S anywhere: {best} at k =', [(k, year_of(k), sc[k][3]) for k in K if sc[k][0] + sc[k][1] == best], '(k, year BC, N)')
    whole = [k for k in K if k % 223 == 0]
    print('  whole Saros cycles from 205 BC, k/223: A, S, U, N:', '; '.join(f'{k // 223}: {sc[k][0]}, {sc[k][1]}, {sc[k][2]}, {sc[k][3]}' for k in whole))
    med = sorted(sc[k][0] + sc[k][1] for k in K)[len(K) // 2]
    print(f'  a typical start (the median of A + S over all {len(K)}): {med} of {len(L) + len(S)}; starts with A + S of at least {a0 + s0}: {sum(sc[k][0] + sc[k][1] >= a0 + s0 for k in K)}')
