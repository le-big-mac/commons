"""After the fact: the eight possible start dates of Freeth 2014's Table S5 (supplement), scored by my catalogue count.
usage: freeth_starts.py CATDIR [CATDIR ...]   (under -I through runpy)"""
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
def jd_julian(y, m, d):
    if m <= 2: y -= 1; m += 12
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d - 1524.5
LE, SE = read_cat('LE', 27257), read_cat('SE', 27256)
fl, fs = dial.glyph_months(); L, S = sorted(fl), sorted(fs)
TABLE_S5 = [(-240, 5, 5, 15, 53), (-222, 5, 16, 23, 23), (-204, 5, 12, 13, 21), (-186, 5, 23, 19, 45), (-168, 6, 3, 2, 8), (-48, 1, 1, 2, 48), (-30, 1, 11, 10, 43), (-12, 1, 22, 18, 32)]
print('Freeth 2014, Table S5: date of the first full moon; lunations from 12 May 205 BC (and the remainder of the division); A, S, U, N for his list')
for y, mo, d, h, mi in TABLE_S5:
    jd = jd_julian(y, mo, d) + (h + mi / 60) / 24
    x = (jd - 1646679.21) / 29.530589; k = round(x)
    A = sum(k + n in LE for n in L); Sn = sum(k + n in SE for n in S)
    U = sum(1 for n in range(1, 224) if k + n in LE and LE[k + n][0] in 'PT' and n not in L)
    N = sum(1 for n in range(1, 224) if k + n in SE and SE[k + n][1] > 0 and n not in S)
    print(f'  {1 - y} BC ({y}-{mo:02d}-{d:02d}): k = {k} ({x - k:+.3f}); {k // 223 if k >= 0 else -((-k) // 223)} cycles and {k - 223 * (k // 223 if k >= 0 else -((-k) // 223))} months; A {A}, S {Sn}, U {U}, N {N}')
