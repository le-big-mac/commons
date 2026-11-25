"""Two more things recomputed before using the second reader's words. usage: after_check2b.py CATDIR [CATDIR ...]"""
import sys, os, re, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import dial
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)\s+\S+\s+(-?\d+\.\d+)')
def read_cat(prefix, add):
    rows = {}
    for f in sorted(f for d in sys.argv[1:] for f in glob.glob(os.path.join(d, prefix + '*.html'))):
        for line in open(f, encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if m: rows[int(m.group(9)) + add] = (m.group(11)[0], f'{int(m.group(2))} {m.group(3)} {m.group(4)}', int(m.group(10)), int(m.group(2)))
    return rows
LE, SE = read_cat('LE', 27257), read_cat('SE', 27256)
# month 126 and month 214: the cycles in which each has a lunar eclipse
for m in (126, 214, 125, 213):
    js = [j for j in range(-5, 123) if 223 * j + m in LE]
    print(f'month {m}: lunar eclipse in cycles {js[0]} to {js[-1]} ({len(js)} cycles, unbroken: {js == list(range(js[0], js[-1] + 1))}); first {LE[223 * js[0] + m][1]}, last {LE[223 * js[-1] + m][1]}')
for m in (207, 196, 2):
    js = [j for j in range(-5, 123) if 223 * j + m in SE]
    print(f'month {m}: solar eclipse in cycles {js[0]} to {js[-1]} ({len(js)} cycles, unbroken: {js == list(range(js[0], js[-1] + 1))}); first {SE[223 * js[0] + m][1]}, last {SE[223 * js[-1] + m][1]}')
# the solar eclipse each of the 16 starts puts in month 13, with its Saros series
for k, yr in ((-1162, 299), (-223, 223), (0, 205), (223, 187), (270, 183), (446, 169), (493, 165), (716, 147), (939, 129), (1162, 111), (1385, 93), (1432, 89), (1655, 71), (1878, 53), (2101, 35), (2324, 17)):
    e = SE.get(k + 13)
    print(f'start {yr} BC (k = {k}): month 13 solar eclipse {e[1] if e else None}, Saros series {e[2] if e else None}')
