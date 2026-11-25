"""Referee's own loader. Data files are parsed as text only (csv module); nothing is executed."""
import csv, re, os
from collections import OrderedDict, Counter

DATE = re.compile(r'^(-?\d+)-(\d\d)-(\d\d)T')
MALE, FEMALE = 'Q6581097', 'Q6581072'
DIM = [31, 28.2425, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def read_rows(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            m = DATE.match(row.get('d') or '')
            if not m:
                rows.append((row['p'], None, row.get('sex') or ''))
                continue
            y, mo, da = int(m.group(1)), int(m.group(2)), int(m.group(3))
            rows.append((row['p'], (y, mo, da), row.get('sex') or ''))
    return rows


def people(path, rule='first', y0=1900, y1=2005, drop_jan1=True, drop_first_of_month=False):
    """One record per person.
    rule: 'first' (first row's date), 'min' (earliest date), 'max', 'unique' (drop people with >1 distinct date).
    Returns list of (p, (y,m,d), sex) and a dict of diagnostics."""
    rows = read_rows(path)
    dates = OrderedDict()
    sexes = {}
    bad = 0
    for p, d, s in rows:
        if d is None:
            bad += 1
            continue
        dates.setdefault(p, [])
        if d not in dates[p]:
            dates[p].append(d)
        sexes.setdefault(p, set())
        if s:
            sexes[p].add(s.rsplit('/', 1)[-1])
    diag = dict(rows=len(rows), bad_dates=bad, persons=len(dates),
                multi_date=sum(1 for v in dates.values() if len(v) > 1),
                multi_sex=sum(1 for v in sexes.values() if len(v) > 1))
    out = []
    n_jan1 = 0
    n_out_years = 0
    for p, ds in dates.items():
        if rule == 'unique' and len(ds) > 1:
            continue
        if rule == 'first' or rule == 'unique':
            d = ds[0]
        elif rule == 'min':
            d = min(ds)
        elif rule == 'max':
            d = max(ds)
        else:
            raise ValueError(rule)
        if not (y0 <= d[0] <= y1):
            n_out_years += 1
            continue
        if d[1] == 1 and d[2] == 1:
            n_jan1 += 1
            if drop_jan1:
                continue
        if drop_first_of_month and d[2] == 1:
            continue
        sx = sexes[p]
        if sx == {MALE}:
            s = 'M'
        elif sx == {FEMALE}:
            s = 'F'
        elif not sx:
            s = ''
        else:
            s = '?'
        out.append((p, d, s))
    diag.update(jan1=n_jan1, out_of_years=n_out_years, counted=len(out))
    return out, diag


def month_counts(recs):
    c = [0] * 12
    for _, d, _ in recs:
        c[d[1] - 1] += 1
    return c


def share(c, months):
    """months: iterable of 1..12"""
    n = sum(c)
    return 100.0 * sum(c[m - 1] for m in months) / n if n else float('nan')


def window(start, k=3):
    return [((start - 1 + i) % 12) + 1 for i in range(k)]


def even_share(months, jan1_out=True):
    tot = 365.2425 - (1 if jan1_out else 0)
    s = sum(DIM[m - 1] for m in months) - (1 if (jan1_out and 1 in months) else 0)
    return 100.0 * s / tot


def per_day(c, jan1_out=True):
    out = []
    for i in range(12):
        days = DIM[i] - (1 if (i == 0 and jan1_out) else 0)
        out.append(c[i] / days)
    return out


MN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def wname(start):
    w = window(start)
    return MN[w[0] - 1] + '-' + MN[w[2] - 1]
