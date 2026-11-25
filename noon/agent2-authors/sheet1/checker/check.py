#!/usr/bin/env python
"""Independent check of expectations A1..A12 on the USGS catalogue.

Run as:  python -I check.py /path/to/catalogue.csv
The catalogue is read as data only (csv module, text mode).
Writes verdicts.json and verdicts.out next to this script.
"""
import csv
import json
import math
import os
import re
import sys
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, ROUND_HALF_UP
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]

# ---------------------------------------------------------------- helpers

NUM_RE = re.compile(r'^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$')


def num(s):
    """Decimal if s is a plain finite number, else None (missing / non-numeric)."""
    if s is None:
        return None
    t = s.strip()
    if t == '' or not NUM_RE.match(t):
        return None
    try:
        d = Decimal(t)
    except InvalidOperation:
        return None
    if not d.is_finite():
        return None
    return d


TIME_RE = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:?\d{2})?$')


def parse_time(s):
    """Return (microseconds since epoch UTC as int, year UTC) or None."""
    if s is None:
        return None
    t = s.strip()
    m = TIME_RE.match(t)
    if not m:
        return None
    y, mo, d, h, mi, se, frac, tz = m.groups()
    try:
        dt = datetime(int(y), int(mo), int(d), int(h), int(mi), int(se),
                      tzinfo=timezone.utc)
    except ValueError:
        return None
    off = 0
    if tz and tz != 'Z':
        sign = 1 if tz[0] == '+' else -1
        digits = tz[1:].replace(':', '')
        off = sign * (int(digits[:2]) * 3600 + int(digits[2:]) * 60)
    secs = int((dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()) - off
    frac = (frac or '')
    # keep full sub-second precision as a Fraction of a second, in microseconds
    us = Fraction(int(frac), 10 ** len(frac)) * 1000000 if frac else Fraction(0)
    total_us = Fraction(secs) * 1000000 + us
    year = datetime.fromtimestamp(secs, tz=timezone.utc).year
    return total_us, year


def epoch_us(y, mo, d, h, mi, s, ms):
    dt = datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc)
    return Fraction(int((dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds())) * 1000000 + ms * 1000


T_LO = epoch_us(2000, 1, 1, 0, 0, 0, 0)
T_HI = epoch_us(2025, 12, 31, 23, 59, 59, 999)


def q(d, places, mode):
    return d.quantize(Decimal(1).scaleb(-places), rounding=mode)


def median(vals):
    v = sorted(vals)
    n = len(v)
    if n == 0:
        return None
    if n % 2 == 1:
        return v[n // 2]
    return (v[n // 2 - 1] + v[n // 2]) / 2


def between(x, a, b):
    return Fraction(a) <= x <= Fraction(b)


def fr(x):
    return Fraction(x)


def f6(x):
    return '%.6f' % float(x)


# ---------------------------------------------------------------- read

with open(SRC, newline='', encoding='utf-8') as fh:
    rdr = csv.reader(fh)
    header = next(rdr)
    raw = [r for r in rdr]

col = {name: i for i, name in enumerate(header)}
diag = []
diag.append('header columns: %d ; data rows: %d' % (len(header), len(raw)))
badlen = [i for i, r in enumerate(raw) if len(r) != len(header)]
diag.append('rows with wrong field count: %d' % len(badlen))
rows = [r for r in raw if len(r) == len(header)]  # (none dropped if badlen == 0)
if badlen:
    # keep them anyway, padded, so "every row of the file" is honoured
    rows = [(r + [''] * len(header))[:len(header)] for r in raw]


def g(r, name):
    return r[col[name]]


# ---------------------------------------------------------------- step 1: id
seen = set()
step1 = []
ndup = 0
nemptyid = sum(1 for r in rows if g(r, 'id') == '')
for r in rows:
    i = g(r, 'id')
    if i in seen:
        ndup += 1
        continue
    seen.add(i)
    step1.append(r)
diag.append('step1: duplicate-id rows dropped: %d ; rows with empty id: %d ; kept %d'
            % (ndup, nemptyid, len(step1)))
# sensitivity: would trimming ids change anything?
ndup_trim = len(rows) - len(set(g(r, 'id').strip() for r in rows))
diag.append('step1 sensitivity: dups if ids were trimmed: %d' % ndup_trim)

# ---------------------------------------------------------------- step 2: type
types_all = Counter(g(r, 'type') for r in rows)
diag.append('type values (whole file, raw): %s' % dict(types_all))
all_empty_literal = all(g(r, 'type') == '' for r in rows)
all_empty_trim = all(g(r, 'type').strip() == '' for r in rows)
diag.append('type empty in every row: literal=%s trimmed=%s' % (all_empty_literal, all_empty_trim))
if all_empty_literal:
    step2 = step1
else:
    step2 = [r for r in step1 if g(r, 'type').strip(' ').lower() == 'earthquake']
diag.append('step2: kept %d (dropped %d)' % (len(step2), len(step1) - len(step2)))
step2_alt = [r for r in step1 if g(r, 'type').strip().lower() == 'earthquake']
diag.append('step2 sensitivity (strip all whitespace instead of spaces): kept %d' % len(step2_alt))

# ---------------------------------------------------------------- step 3: mag, time
events = []
drop_mag_missing = drop_mag_low = drop_time_missing = drop_time_range = 0
mag_round_diff = 0          # raw mag differs from 2dp-rounded mag
mag_mode_diff = 0           # half-even vs half-up differ
mag_border = 0              # raw < 5.5 but rounded >= 5.5 (or the reverse)
time_formats = Counter()
for r in step2:
    m = num(g(r, 'mag'))
    if m is None:
        drop_mag_missing += 1
        continue
    m_he = q(m, 2, ROUND_HALF_EVEN)
    m_hu = q(m, 2, ROUND_HALF_UP)
    if (m >= Decimal('5.5')) != (m_he >= Decimal('5.5')) or (m >= Decimal('5.5')) != (m_hu >= Decimal('5.5')):
        mag_border += 1
    if not (m >= Decimal('5.5')):      # literal: "the number in mag ... at least 5.5"
        drop_mag_low += 1
        continue
    t = parse_time(g(r, 'time'))
    if t is None:
        drop_time_missing += 1
        continue
    tus, year = t
    if not (T_LO <= tus <= T_HI):
        drop_time_range += 1
        continue
    time_formats[re.sub(r'\d', '9', g(r, 'time'))] += 1
    if m_he != m:
        mag_round_diff += 1
    if m_he != m_hu:
        mag_mode_diff += 1
    ev = {
        'id': g(r, 'id'),
        'mag': m_he,
        'mag_raw': m,
        't': tus,
        'year': year,
        'depth': num(g(r, 'depth')),
        'lat': num(g(r, 'latitude')),
        'lon': num(g(r, 'longitude')),
        'raw_depth': g(r, 'depth'),
    }
    events.append(ev)

N = len(events)
diag.append('step3: dropped mag missing/non-numeric %d, mag<5.5 %d, time missing/unparseable %d, '
            'time out of range %d ; N = %d'
            % (drop_mag_missing, drop_mag_low, drop_time_missing, drop_time_range, N))
diag.append('step3 sensitivity: rows where raw-vs-rounded mag disagree on >=5.5: %d' % mag_border)
diag.append('mag: events whose raw mag != mag rounded to 2dp: %d ; half-even vs half-up differ: %d'
            % (mag_round_diff, mag_mode_diff))
diag.append('mag decimal places (raw): %s' % dict(Counter(
    max(0, -e['mag_raw'].as_tuple().exponent) for e in events)))
diag.append('time string patterns among events: %s' % dict(time_formats))
diag.append('events with missing depth: %d ; missing lat: %d ; missing lon: %d ; lat==0: %d ; lon==0: %d'
            % (sum(e['depth'] is None for e in events),
               sum(e['lat'] is None for e in events),
               sum(e['lon'] is None for e in events),
               sum(e['lat'] is not None and e['lat'] == 0 for e in events),
               sum(e['lon'] is not None and e['lon'] == 0 for e in events)))
lons = [e['lon'] for e in events if e['lon'] is not None]
lats = [e['lat'] for e in events if e['lat'] is not None]
deps = [e['depth'] for e in events if e['depth'] is not None]
diag.append('lat range [%s, %s] ; lon range [%s, %s] ; depth range [%s, %s] ; negative depths: %d'
            % (min(lats), max(lats), min(lons), max(lons), min(deps), max(deps),
               sum(d < 0 for d in deps)))
yrs = Counter(e['year'] for e in events)
diag.append('year range of events: %d..%d' % (min(yrs), max(yrs)))

# ---------------------------------------------------------------- expectations
verd = OrderedDict()
out = OrderedDict()
D = Decimal

# A1
n6 = sum(e['mag'] >= D('6.0') for e in events)
n7 = sum(e['mag'] >= D('7.0') for e in events)
s6 = Fraction(n6, N)
s7 = Fraction(n7, N)
a1a = between(s6, '0.26', '0.35')
a1b = between(s7, '0.024', '0.036')
verd['A1'] = a1a and a1b
out['A1'] = ('N=%d; mag>=6.0: %d/%d = %s (in [0.26,0.35]: %s); mag>=7.0: %d/%d = %s (in [0.024,0.036]: %s)'
             % (N, n6, N, f6(s6), a1a, n7, N, f6(s7), a1b))

# A2
maxmag = max(e['mag'] for e in events)
ge9 = sorted([e for e in events if e['mag'] >= D('9.0')], key=lambda e: e['t'])
ge9_years = sorted(e['year'] for e in ge9)
a2a = (maxmag == D('9.1'))
a2b = (len(ge9) == 2 and ge9_years == [2004, 2011])
verd['A2'] = a2a and a2b
out['A2'] = ('largest mag = %s (==9.1: %s); events with mag>=9.0: %d, (year, mag) = %s (exactly two, 2004 and 2011: %s)'
             % (maxmag, a2a, len(ge9), [(e['year'], str(e['mag'])) for e in ge9], a2b))

# A3
nlon = len(lons)
npos = sum(x > 0 for x in lons)
sl = Fraction(npos, nlon)
verd['A3'] = between(sl, '0.58', '0.72')
out['A3'] = ('longitude>0: %d/%d = %s (in [0.58,0.72]: %s); longitude<0: %d; longitude==0: %d'
             % (npos, nlon, f6(sl), verd['A3'], sum(x < 0 for x in lons), sum(x == 0 for x in lons)))

# A4
dv_he = Counter(q(d, 1, ROUND_HALF_EVEN) for d in deps)
dv_hu = Counter(q(d, 1, ROUND_HALF_UP) for d in deps)
dv_fl = Counter(round(float(d), 1) for d in deps)
nd = len(deps)


def a4(counter):
    top = counter.most_common()
    best_val, best_n = top[0]
    strict = len(top) == 1 or top[1][1] < best_n
    is10 = strict and (D(str(best_val)) == D('10.0'))
    share10 = Fraction(counter.get(best_val.__class__('10.0') if isinstance(best_val, Decimal) else 10.0, 0), nd)
    return top[:3], is10, share10


top_he, is10_he, sh10_he = a4(dv_he)
top_hu, is10_hu, sh10_hu = a4(dv_hu)
top_fl, is10_fl, sh10_fl = a4(dv_fl)
a4a = is10_he
a4b = sh10_he >= Fraction('0.15')
verd['A4'] = a4a and a4b
out['A4'] = ('most frequent depth value = %s km with %d events (strictly first: %s; runners-up %s); '
             'share at 10.0 km = %d/%d = %s (>=0.15: %s)'
             % (top_he[0][0], top_he[0][1], is10_he,
                ', '.join('%s km x%d' % (v, c) for v, c in top_he[1:3]),
                dv_he.get(D('10.0'), 0), nd, f6(sh10_he), a4b))
diag.append('A4 rounding sensitivity: half-even top3 %s ; half-up top3 %s ; float-round top3 %s'
            % ([(str(v), c) for v, c in top_he], [(str(v), c) for v, c in top_hu], top_fl))
diag.append('A4: depths whose 1dp value differs between half-even and half-up: %d ; depths with >1 decimal place: %d'
            % (sum(q(d, 1, ROUND_HALF_EVEN) != q(d, 1, ROUND_HALF_UP) for d in deps),
               sum(-d.as_tuple().exponent > 1 for d in deps)))
diag.append('A4: raw depth strings mapping to value 10.0: %s'
            % dict(Counter(e['raw_depth'] for e in events
                           if e['depth'] is not None and q(e['depth'], 1, ROUND_HALF_EVEN) == D('10.0'))))

# A5
n8 = sum(e['mag'] >= D('8.0') for e in events)
verd['A5'] = 26 <= n8 <= 30
out['A5'] = 'events with mag>=8.0: %d (in [26,30]: %s)' % (n8, verd['A5'])
diag.append('A5: mag>=8.0 events by raw mag: %s ; events with 7.9<=raw mag<8.0: %s'
            % (dict(sorted(Counter(str(e['mag_raw']) for e in events if e['mag'] >= D('8.0')).items())),
               dict(sorted(Counter(str(e['mag_raw']) for e in events
                                   if D('7.9') <= e['mag_raw'] < D('8.0')).items()))))

# A6
nsh = sum(d < 70 for d in deps)
ndeep = sum(d >= 300 for d in deps)
ssh = Fraction(nsh, nd)
sdeep = Fraction(ndeep, nd)
a6a = ssh >= Fraction('0.72')
a6b = between(sdeep, '0.035', '0.075')
verd['A6'] = a6a and a6b
out['A6'] = ('depth<70: %d/%d = %s (>=0.72: %s); depth>=300: %d/%d = %s (in [0.035,0.075]: %s)'
             % (nsh, nd, f6(ssh), a6a, ndeep, nd, f6(sdeep), a6b))
# sensitivity: depth value (1dp) instead of depth as given
nsh_v = sum(q(d, 1, ROUND_HALF_EVEN) < 70 for d in deps)
ndeep_v = sum(q(d, 1, ROUND_HALF_EVEN) >= 300 for d in deps)
diag.append('A6 sensitivity (using 1dp depth value): depth<70 %d ; depth>=300 %d' % (nsh_v, ndeep_v))

# A7
per_year = OrderedDict((y, 0) for y in range(2000, 2026))
for e in events:
    per_year[e['year']] += 1
ranked = sorted(per_year.items(), key=lambda kv: (-kv[1], kv[0]))
a7 = ranked[0][0] == 2011 and ranked[0][1] > ranked[1][1]
verd['A7'] = a7
out['A7'] = ('year with most events: %d (%d events); next: %d (%d), %d (%d); strict first and ==2011: %s'
             % (ranked[0][0], ranked[0][1], ranked[1][0], ranked[1][1], ranked[2][0], ranked[2][1], a7))
diag.append('A7 counts per year: %s' % dict(per_year))

# A8
ts = sorted(e['t'] for e in events)
gaps = [ts[i + 1] - ts[i] for i in range(len(ts) - 1)]
HOUR = Fraction(3600) * 1000000
nshort = sum(gp < HOUR for gp in gaps)
sg = Fraction(nshort, len(gaps))
verd['A8'] = sg >= Fraction('0.08')
span_s = float(ts[-1] - ts[0]) / 1e6
mean_gap = span_s / len(gaps)
pois = 1 - math.exp(-3600.0 / mean_gap)
out['A8'] = ('gaps<3600 s: %d/%d = %s (>=0.08: %s); zero gaps: %d; mean gap %.1f s; '
             'independent-arrival reference 1-exp(-3600/mean) = %.4f'
             % (nshort, len(gaps), f6(sg), verd['A8'], sum(gp == 0 for gp in gaps), mean_gap, pois))
diag.append('A8: gaps exactly 3600 s: %d ; gaps within 1 s of 3600 s: %d'
            % (sum(gp == HOUR for gp in gaps), sum(abs(gp - HOUR) < 1000000 for gp in gaps)))

# A9
per_year7 = OrderedDict((y, 0) for y in range(2000, 2026))
for e in events:
    if e['mag'] >= D('7.0'):
        per_year7[e['year']] += 1
hi = sorted(per_year7.items(), key=lambda kv: (-kv[1], kv[0]))
lo = sorted(per_year7.items(), key=lambda kv: (kv[1], kv[0]))
a9a = hi[0][0] == 2010 and hi[0][1] > hi[1][1]
a9b = lo[0][0] == 2017 and lo[0][1] < lo[1][1]
verd['A9'] = a9a and a9b
maxc = hi[0][1]
minc = lo[0][1]
out['A9'] = ('mag>=7.0 per year: max %d in %s (2010 has %d; strictly most: %s); min %d in %s (2017 has %d; strictly fewest: %s)'
             % (maxc, [y for y, c in per_year7.items() if c == maxc], per_year7[2010], a9a,
                minc, [y for y, c in per_year7.items() if c == minc], per_year7[2017], a9b))
diag.append('A9 mag>=7.0 counts per year: %s' % dict(per_year7))

# A10
mm = median([e['mag'] for e in events])
mm2_he = q(D(mm) if not isinstance(mm, Decimal) else mm, 2, ROUND_HALF_EVEN)
mm2_hu = q(mm, 2, ROUND_HALF_UP)
verd['A10'] = (mm2_he == D('5.7'))
out['A10'] = ('median mag = %s (N=%d; rounded to 2dp %s; ==5.7: %s); events with mag<5.7: %d, ==5.7: %d, >5.7: %d'
              % (mm, N, mm2_he, verd['A10'],
                 sum(e['mag'] < D('5.7') for e in events),
                 sum(e['mag'] == D('5.7') for e in events),
                 sum(e['mag'] > D('5.7') for e in events)))
diag.append('A10: median of raw (unrounded) mags = %s ; half-up 2dp of median = %s'
            % (median([e['mag_raw'] for e in events]), mm2_hu))

# A11
nsouth = sum(x < 0 for x in lats)
nnorth = sum(x > 0 for x in lats)
verd['A11'] = nsouth > nnorth
out['A11'] = ('latitude<0: %d; latitude>0: %d; latitude==0: %d; of %d with latitude (south>north: %s)'
              % (nsouth, nnorth, sum(x == 0 for x in lats), len(lats), verd['A11']))

# A12
d7 = [e['depth'] for e in events if e['mag'] >= D('7.0') and e['depth'] is not None]
med7 = median(d7)
medall = median(deps)
verd['A12'] = med7 > medall
out['A12'] = ('median depth of mag>=7.0 events = %s km (n=%d); median depth of all events = %s km (n=%d); greater: %s'
              % (med7, len(d7), medall, len(deps), verd['A12']))
dlt7 = [e['depth'] for e in events if e['mag'] < D('7.0') and e['depth'] is not None]
diag.append('A12 sensitivity: median depth of mag<7.0 events only = %s (n=%d)' % (median(dlt7), len(dlt7)))

# ---------------------------------------------------------------- write
verd = OrderedDict((k, bool(v)) for k, v in verd.items())
with open(os.path.join(HERE, 'verdicts.json'), 'w') as fh:
    json.dump(verd, fh, indent=1)
    fh.write('\n')
with open(os.path.join(HERE, 'verdicts.out'), 'w') as fh:
    for k in verd:
        fh.write('%s: %s | %s\n' % (k, 'HELD' if verd[k] else 'FAILED', out[k]))

print('--- diagnostics')
for line in diag:
    print(line)
print('--- results')
for k in verd:
    print('%s: %s | %s' % (k, 'HELD' if verd[k] else 'FAILED', out[k]))
