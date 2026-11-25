"""Second reader's own parser for the NASA Five Millennium catalogue pages (HTML), and own placement in dial months.
Not derived from agent3's regex: uses html.parser to pull the text of <pre> blocks, then whitespace tokens.
usage (as a module): rows = cat2.load(kind, dirs)   kind 'LE' or 'SE'
"""
import os, re, glob, math
from html.parser import HTMLParser

MON = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)


class Pre(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag == 'pre': self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'pre' and self.depth > 0: self.depth -= 1

    def handle_data(self, data):
        if self.depth > 0: self.buf.append(data)


def jd_from_date(y, m, d, gregorian):
    """Julian day number at 0h of a calendar date; astronomical year numbering (year 0 = 1 BC).
    Integer arithmetic (Fliegel-Van Flandern style for Gregorian; plain for Julian)."""
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    if gregorian:
        jdn = d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045
    else:
        jdn = d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083
    return jdn - 0.5


def summary(raw):
    """The page's own count table: {'All Eclipses': n, 'Penumbral': n, ...}"""
    out = {}
    for name, num in re.findall(r'<td>\s*([A-Za-z ]+?)\s*</td>\s*<td>[^<]*</td>\s*<td>\s*(\d+)\s*</td>\s*<td>\s*[\d.]+%', raw):
        if name not in out: out[name] = int(num)
    return out


def parse_page(path, kind):
    raw = open(path, encoding='utf-8', errors='replace').read()
    p = Pre(); p.feed(raw)
    text = ''.join(p.buf)
    rows = []
    for line in text.split('\n'):
        t = line.split()
        if len(t) < 12: continue
        if not (len(t[0]) == 5 and t[0].isdigit()): continue
        if t[2] not in MON: continue
        y = int(t[1]); mo = MON[t[2]]; d = int(t[3])
        hh, mi, ss = (int(x) for x in t[4].split(':'))
        dT = int(t[5]); luna = int(t[6]); saros = int(t[7]); typ = t[8]; q = t[9]
        gamma = float(t[10])
        r = dict(cat=int(t[0]), y=y, mo=mo, d=d, date=f'{y} {t[2]} {d:02d}', hms=t[4], dT=dT, luna=luna, saros=saros, typ=typ, q=q, gamma=gamma,
                 page=os.path.basename(path))
        if kind == 'LE':
            r['pmag'] = float(t[11]); r['umag'] = float(t[12])
        else:
            r['mag'] = float(t[11])
        greg = (y, mo, d) >= (1582, 10, 15)
        r['jd'] = jd_from_date(y, mo, d, greg) + (hh + mi / 60 + ss / 3600) / 24     # TD
        rows.append(r)
    return rows, summary(raw)


def load(kind, dirs, verbose=True):
    files = sorted(f for d in dirs for f in glob.glob(os.path.join(d, kind + '*.html')))
    allrows = []; problems = []
    for f in files:
        rows, summ = parse_page(f, kind)
        n_all = summ.get('All Eclipses')
        if n_all != len(rows): problems.append((os.path.basename(f), 'row count', len(rows), 'page says', n_all))
        if kind == 'LE':
            want = dict(N=summ.get('Penumbral'), P=summ.get('Partial'), T=summ.get('Total'))
        else:
            want = dict(P=summ.get('Partial'), A=summ.get('Annular'), T=summ.get('Total'), H=summ.get('Hybrid'))
        got = {}
        for r in rows: got[r['typ'][0]] = got.get(r['typ'][0], 0) + 1
        for k, v in want.items():
            if (got.get(k, 0)) != (v or 0): problems.append((os.path.basename(f), 'type', k, got.get(k, 0), 'page says', v))
        for k in got:
            if k not in want: problems.append((os.path.basename(f), 'unexpected type letter', k, got[k]))
        allrows += rows
    allrows.sort(key=lambda r: r['jd'])
    if verbose:
        print(f'{kind}: {len(files)} pages, {len(allrows)} rows; mismatches against the pages\' own count tables: {problems if problems else "none"}')
    return allrows, files, problems


# ---- Meeus, Astronomical Algorithms ch. 49: mean phases. k integer = new moon, k + 0.5 = full moon; k = 0 is the new moon of 6 Jan 2000.
def mean_phase_jde(k):
    T = k / 1236.85
    return 2451550.09766 + 29.530588861 * k + 0.00015437 * T * T - 0.000000150 * T ** 3 + 0.00000000073 * T ** 4


def k_of(jde):
    k = (jde - 2451550.09766) / 29.530588861
    for _ in range(6):
        k -= (mean_phase_jde(k) - jde) / 29.530588861
    return k
