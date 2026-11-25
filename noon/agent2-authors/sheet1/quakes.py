"""Verdicts for the author's twelve expectations, by the letter of readers/sheet.md.   usage: python -I quakes.py catalogue.csv results.json
Readings where the sheet leaves a choice (settled before running, none changes with the catalogue's values in view):
 - "rounded to one decimal place" and "to two decimal places" use ordinary rounding of the decimal text (half away from zero);
 - a share's denominator is the events that have the needed column, as the sheet says;
 - "one in the year 2004 and one in the year 2011" means the two events of magnitude 9.0 or more fall one in each of those years."""
import sys, csv, json, collections
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone
SRC, OUT = sys.argv[1], sys.argv[2]
raw = list(csv.DictReader(open(SRC, encoding='utf-8')))
seen, rows = set(), []
for r in raw:
    if r['id'] in seen:
        continue
    seen.add(r['id']); rows.append(r)
if any(r['type'].strip() for r in rows):
    rows = [r for r in rows if r['type'].strip().lower() == 'earthquake']
def dec(s):
    try:
        return Decimal(s.strip())
    except Exception:
        return None
t0 = datetime(2000, 1, 1, tzinfo=timezone.utc); t1 = datetime(2025, 12, 31, 23, 59, 59, 999000, tzinfo=timezone.utc)
ev = []
for r in rows:
    m = dec(r['mag'])
    try:
        t = datetime.fromisoformat(r['time'].replace('Z', '+00:00'))
    except Exception:
        continue
    if m is None or m < Decimal('5.5') or not (t0 <= t <= t1):
        continue
    q2 = lambda x: None if x is None else x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    d = dec(r['depth'])
    ev.append(dict(t=t, year=t.year, mag=q2(m), depth=d, dval=None if d is None else d.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP), lat=dec(r['latitude']), lon=dec(r['longitude']), place=r['place']))
N = len(ev)
print(f"{len(raw)} rows in the file; {len(rows)} after removing repeated ids and other types; N = {N} events")
res = {}
def say(tag, text, ok):
    res[tag] = bool(ok)
    print(f"{tag:4s} {text}  ->  {'held' if ok else 'failed'}")
def median(v):
    v = sorted(v); n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
s6 = sum(e['mag'] >= 6 for e in ev) / N; s7 = sum(e['mag'] >= 7 for e in ev) / N
say('A1', f"share with magnitude 6.0 or more {s6:.4f} ({sum(e['mag'] >= 6 for e in ev)}); 7.0 or more {s7:.4f} ({sum(e['mag'] >= 7 for e in ev)})", 0.26 <= s6 <= 0.35 and 0.024 <= s7 <= 0.036)
big = [e for e in ev if e['mag'] >= 9]; mx = max(e['mag'] for e in ev)
say('A2', f"largest magnitude {mx}; magnitude 9.0 or more: " + "; ".join(f"{e['mag']} in {e['year']} ({e['place']})" for e in big), mx == Decimal('9.1') and len(big) == 2 and sorted(e['year'] for e in big) == [2004, 2011])
lo = [e for e in ev if e['lon'] is not None]; east = sum(e['lon'] > 0 for e in lo) / len(lo)
say('A3', f"share with longitude above 0: {east:.4f} of {len(lo)}", 0.58 <= east <= 0.72)
dp = [e for e in ev if e['dval'] is not None]; cnt = collections.Counter(e['dval'] for e in dp).most_common(3)
say('A4', f"most frequent depth values: " + ", ".join(f"{v} km {c} ({100 * c / len(dp):.1f}%)" for v, c in cnt), cnt[0][0] == Decimal('10.0') and cnt[0][1] > cnt[1][1] and cnt[0][1] / len(dp) >= 0.15)
n8 = sum(e['mag'] >= 8 for e in ev); say('A5', f"events of magnitude 8.0 or more: {n8}", 26 <= n8 <= 30)
sh = sum(e['depth'] < 70 for e in dp) / len(dp); deep = sum(e['depth'] >= 300 for e in dp) / len(dp)
say('A6', f"share shallower than 70 km {sh:.4f}; share at 300 km or deeper {deep:.4f}", sh >= 0.72 and 0.035 <= deep <= 0.075)
by = collections.Counter(e['year'] for e in ev); top = by.most_common(3)
say('A7', f"busiest years: " + ", ".join(f"{y} {c}" for y, c in top), top[0][0] == 2011 and top[0][1] > top[1][1])
ts = sorted(e['t'] for e in ev); gaps = [(b - a).total_seconds() for a, b in zip(ts[:-1], ts[1:])]; short = sum(g < 3600 for g in gaps) / len(gaps)
say('A8', f"gaps shorter than one hour: {sum(g < 3600 for g in gaps)} of {len(gaps)} = {100 * short:.2f}%", short >= 0.08)
y7 = {y: sum(e['mag'] >= 7 and e['year'] == y for e in ev) for y in range(2000, 2026)}
srt = sorted(y7.items(), key=lambda kv: -kv[1])
say('A9', "magnitude 7.0 or more by year: " + ", ".join(f"{y}:{c}" for y, c in sorted(y7.items())), srt[0][0] == 2010 and srt[0][1] > srt[1][1] and srt[-1][0] == 2017 and srt[-1][1] < srt[-2][1])
mm = median([e['mag'] for e in ev]); mmr = Decimal(mm).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
cum = {str(v): sum(e['mag'] <= Decimal(v) for e in ev) / N for v in ('5.5', '5.6', '5.7', '5.8')}
say('A10', f"median magnitude {mmr}; share at or below 5.6: {cum['5.6']:.4f}, at or below 5.7: {cum['5.7']:.4f}", mmr == Decimal('5.70'))
la = [e for e in ev if e['lat'] is not None]; south = sum(e['lat'] < 0 for e in la); north = sum(e['lat'] > 0 for e in la)
say('A11', f"latitude below 0: {south}; above 0: {north}", south > north)
m7 = median([e['depth'] for e in dp if e['mag'] >= 7]); mall = median([e['depth'] for e in dp])
say('A12', f"median depth, magnitude 7.0 or more: {m7} km ({sum(e['mag'] >= 7 for e in dp)} events); all events: {mall} km", m7 > mall)
json.dump(dict(verdicts=res, N=N), open(OUT, 'w'), indent=1)
