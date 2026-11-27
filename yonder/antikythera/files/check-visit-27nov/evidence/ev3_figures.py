"""Evidence reading, part 2: the figures in the changed sentences, against the saved outputs and against standard values.
usage: python ev3_figures.py RECORDS_DIR      (the folder of the three working notes; read only)
Prints; writes nothing."""
import json
import math
import os
import sys

R = sys.argv[1]
S = json.load(open(os.path.join(R, 'results-S.json')))
T = json.load(open(os.path.join(R, 'results-T.json')))
today = json.load(open(os.path.join(R, 'today.json')))
cat = json.load(open(os.path.join(R, 'dial', 'catalogue_all.json')))
two = json.load(open(os.path.join(R, 'dial', 'two_lists.json')))

print('=== THE MOON ===')
d = S['drift']['moon']
print(f'drift against the stars over the span: {d:.2f} deg = {abs(d) / 360:.3f} of a turn behind; the same place on the dial is {d % 360:.2f} deg ahead')
p, s = today['moon']
print(f'today.json: pointer {p:.2f}, Moon {s:.2f}; pointer minus Moon = {((p - s + 180) % 360) - 180:+.2f} deg (positive = further on in longitude = ahead); as a share of a turn {((p - s) % 360) / 360:.3f}')
print(f'results-S.json today: {S["today"]["moon"]:+.2f}; part of the 105 that is not the mean slow running: {S["today"]["moon"] - d % 360:+.2f} deg')
print(f'what a reader gets who subtracts: 360 - 105.3 = {360 - S["today"]["moon"]:.1f} deg "behind", against the 262.2 of the long account')
rate = d / S['years']
print(f'rate {rate:.4f} deg a year; years for one degree: {1 / abs(rate):.1f}; in nine years: {9 * abs(rate):.2f} deg; floor of the Moon theory (run.out) 1.035 deg rms: {1.035 / abs(rate):.1f} years')
moon_per_year = 360 * 254 / 19
print(f'the pointer turns {moon_per_year:.0f} deg a year; slow by one part in {moon_per_year / abs(rate):.0f}')

print('\n=== THE KEEPER\'S YEAR ===')
span_days = S['years'] * 365.25
ys, yt = span_days / S['dn'], span_days / T['dn']
print(f'span {span_days:.1f} days; turns by the stars {S["dn"]:.5f}, by the seasons {T["dn"]:.5f}; difference {(T["dn"] - S["dn"]) * 360:.2f} deg')
print(f'so the run\'s own two years: by the stars {ys:.5f} d, by the seasons {yt:.5f} d; difference {(ys - yt) * 1440:.2f} minutes')
SID, TROP = 365.256363, 365.242190          # standard values for J2000 (days): sidereal year, mean tropical year
print(f'standard values (J2000): sidereal {SID}, tropical {TROP}: difference {(SID - TROP) * 1440:.2f} minutes')
print(f'from the page\'s 31 deg over the span: 31.0 / {S["years"]:.1f} = {31.0 / S["years"] * 3600:.2f} arcsec a year; the Sun moves 360 deg in {SID} d, so {31.0 / S["years"] / 360 * SID * 1440:.2f} minutes a year')
print(f'twenty minutes a year over {S["years"]:.0f} years = {20 * S["years"] / 1440:.1f} days = {20 * S["years"] / 1440 / SID * 360:.1f} deg of the Sun\'s round')

print('\n=== THE PLANETS, typical error over the 76 years to today (rms; run.out) ===')
rms_S = dict(mercury=4.690, venus=10.437, mars=11.669, jupiter=4.418, saturn=9.260)      # copied from run.out, frame S
rms_T = dict(mercury=22.761, venus=22.837, mars=14.146, jupiter=30.347, saturn=37.972)    # frame T
floor = dict(mercury=4.2271, venus=1.4818, mars=9.5623, jupiter=3.6651, saturn=4.9654)
print('against the stars: %.1f to %.1f' % (min(rms_S.values()), max(rms_S.values())), '| against the seasons: %.1f to %.1f' % (min(rms_T.values()), max(rms_T.values())))
print('on the day, against the seasons:', {k: round(T['today'][k], 1) for k in rms_T}, '-> %.0f to %.0f' % (min(abs(T['today'][k]) for k in rms_T), max(abs(T['today'][k]) for k in rms_T)))
print('growth of typical error against the stars:', {k: f'{rms_S[k] / floor[k]:.2f}' for k in rms_S})
print('Mars on the day:', round(S['today']['mars'], 2))

print('\n=== THE ECLIPSE DIAL: the counts ===')
first = lambda rows, cond: next((r['cycle'] for r in rows if cond(r)), None)
for name, rows in (('Freeth (catalogue_all.json)', cat), ('Freeth (two_lists.json)', two['F']), ('Iversen and Jones (two_lists.json)', two['IJ'])):
    a0 = first(rows, lambda r: r['A'] == 0); um0 = first(rows, lambda r: r['Aum'] == 0); s0 = first(rows, lambda r: r['S'] == 0)
    half = first(rows, lambda r: r['A'] <= 19)
    allmiss = first(rows, lambda r: r['U'] == r['umbral'])
    print(f'{name}: cycle 0: A {rows[0]["A"]}, partial or total {rows[0]["Aum"]}, S {rows[0]["S"]}; lunar at half or under from cycle {half}; lunar none from {a0}; '
          f'partial-or-total none from {um0} (stays none after: {all(r["Aum"] == 0 for r in rows if r["cycle"] >= um0)}); '
          f'every partial or total lunar eclipse in an unmarked month from {allmiss} (stays so: {all(r["U"] == r["umbral"] for r in rows if r["cycle"] >= allmiss)}); solar none from {s0} '
          f'(stays: {all(r["S"] == 0 for r in rows if r["cycle"] >= s0)})')
    print('    A never rises:', all(a['A'] >= b['A'] for a, b in zip(rows, rows[1:])), '| S never rises:', all(a['S'] >= b['S'] for a, b in zip(rows, rows[1:])),
          '| partial-or-total in marked months rises at cycles:', [b['cycle'] for a, b in zip(rows, rows[1:]) if b['Aum'] > a['Aum']])
r0 = cat[0]
print(f'first cycle: {r0["umbral"]} partial or total lunar eclipses, {r0["U"]} in unmarked months; {r0["A"] - r0["Aum"]} of the {r0["A"]} penumbral only; {r0["solar_all"]} solar eclipses, {r0["solar_all"] - r0["solar_on_glyph"]} in months without a mark')
print('unmarked partial or total lunar eclipses at cycle 8 (144 years on):', cat[8]['U'], '; at cycle 7:', cat[7]['U'])


# --- the dates: the first full moon of cycle j is 223 j mean lunations after that of 12 May 205 BC -------------------
def mean_full_moon_jde(k):
    """Meeus, Astronomical Algorithms ch. 49, mean phase only; k whole = new moon, k + 0.5 = full moon."""
    Tc = k / 1236.85
    return 2451550.09766 + 29.530588861 * k + 0.00015437 * Tc ** 2 - 0.000000150 * Tc ** 3 + 0.00000000073 * Tc ** 4


def julian_calendar(jd):
    """JD -> (year, month, day with fraction) in the Julian calendar (astronomical year numbering)."""
    z = math.floor(jd + 0.5); f = jd + 0.5 - z
    a = z
    b = a + 1524; c = math.floor((b - 122.1) / 365.25); dd = math.floor(365.25 * c); e = math.floor((b - dd) / 30.6001)
    day = b - dd - math.floor(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return year, month, day


def gregorian(jd):
    z = math.floor(jd + 0.5); f = jd + 0.5 - z
    al = math.floor((z - 1867216.25) / 36524.25); a = z + 1 + al - math.floor(al / 4)
    b = a + 1524; c = math.floor((b - 122.1) / 365.25); dd = math.floor(365.25 * c); e = math.floor((b - dd) / 30.6001)
    day = b - dd - math.floor(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return year, month, day


def jd_julian(y, m, dday):
    if m <= 2:
        y -= 1; m += 12
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + dday - 1524.5


jd0 = jd_julian(-204, 5, 12.5)
k0 = round((jd0 - 2451550.09766) / 29.530588861 - 0.5) + 0.5
print('\n=== THE ECLIPSE DIAL: "years on" turned into years AD ===')
y, m, dday = julian_calendar(mean_full_moon_jde(k0))
print(f'mean full moon nearest 12 May 205 BC: k = {k0}, {y} {m:02d} {dday:05.2f} (Julian calendar; year {y} is {1 - y} BC); a true full moon lies within about 0.6 day of the mean one')
# a test of the reckoning on a date the dial note gives: cycle 122 "ended with the new moon of 1 January 2014"
jd_end = mean_full_moon_jde(k0 + 223 * 122 + 222 + 0.5)
print('test: the last new moon of cycle 122 by this reckoning (Gregorian): %d %02d %05.2f (the dial note: 1 January 2014)' % gregorian(jd_end))
MON = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
for j, what in ((31, 'lunar months at half or under (the page: about 560 years, around AD 355)'),
                (55, 'no marked month with a partial or total lunar eclipse (the page, NEW: 992 years on, around AD 788)'),
                (56, 'the cycle after'),
                (62, 'Iversen and Jones: lunar none'),
                (64, 'lunar none (the page: AD 950)'),
                (70, 'solar none (the page: AD 1058)'),
                (73, 'Iversen and Jones: solar none')):
    jd = mean_full_moon_jde(k0 + 223 * j)
    y, m, dday = julian_calendar(jd)
    yrs = (jd - mean_full_moon_jde(k0)) / 365.25
    print(f'cycle {j:3d}: begins {yrs:8.2f} Julian years on ({j} x 18.03 = {j * 18.03:7.1f}); first full moon {int(dday):2d} {MON[m - 1]} AD {y} (Julian calendar), give or take a day; plain subtraction {round(j * 18.03)} - 204 = {round(j * 18.03) - 204}  | {what}')
jd = mean_full_moon_jde(k0 + 223 * 55)
print(f'cycle 55: its first full moon is {jd_julian(788, 1, 1.0) - jd:.1f} days before 1 January AD 788; the cycle runs to', '%d %02d' % julian_calendar(mean_full_moon_jde(k0 + 223 * 56))[:2])
