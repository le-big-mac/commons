"""Second evidence reading, figures: the new numbers of the second candidate against the saved outputs and the catalogue.
usage: python ev8_second_figures.py RECORDS_DIR CATDIR [CATDIR ...]
The catalogue pages are data: run under -I, read only. Prints; writes nothing."""
import glob
import html
import json
import math
import os
import re
import sys

R, CATS = sys.argv[1], sys.argv[2:]
S = json.load(open(os.path.join(R, 'results-S.json')))
T = json.load(open(os.path.join(R, 'results-T.json')))

print('=== THE MOON: "most of one turn lost in nearly thirty thousand" ===')
turns_main = S['dn']
moon_turns = 254 / 19 * turns_main
lost = -S['drift']['moon'] / 360
print(f'turns of the main wheel by the stars: {turns_main:.2f}; the Moon\'s pointer: 254/19 x that = {moon_turns:,.1f} turns (with 2,230.5: {254 / 19 * 2230.5:,.1f})')
print(f'lost by the slow running alone: {-S["drift"]["moon"]:.1f} deg = {lost:.3f} of a turn; read from where the pointer stands on the day (360 - 105.3): {(360 - S["today"]["moon"]) / 360:.3f} of a turn')
print(f'one turn lost in {moon_turns / lost:,.0f}; "most of one turn in nearly thirty thousand" = {lost:.2f} in {moon_turns:,.0f}')

print('\n=== "In short": the Sun, Venus and Saturn (run.out) ===')
print(f'Sun on the day, against the stars: {S["today"]["sun"]:+.2f} deg (rms over the 76 years 0.18, from run.out); with the keeper by the seasons, against the seasons: {T["today"]["sun"]:+.2f} (rms 0.88)')
print('typical error then -> now (run.out, frame S): Venus 1.48 -> 10.44 (x%.1f); Saturn 4.97 -> 9.26 (x%.2f); Mercury x%.2f, Mars x%.2f, Jupiter x%.2f'
      % (10.437 / 1.4818, 9.260 / 4.9654, 4.690 / 4.2271, 11.669 / 9.5623, 4.418 / 3.6651))
print('typical error today: Mercury 4.7, Venus 10.4, Mars 11.7, Jupiter 4.4, Saturn 9.3 (so Venus and Saturn have "got worse" than they were, and are not worse than Mars is)')

# ---------------- the marks, two lists ---------------------------------------------------------------------------------
YEAR, NODES = 446, ((66, 'D'), (289, 'A'))


def off(p):
    best = None
    for node, name in NODES:
        d = (p - node + YEAR // 2) % YEAR - YEAR // 2
        if best is None or abs(d) < abs(best[0]):
            best = (d, name)
    return best


lunarF, solarF = set(), set()
for n in range(1, 224):
    d, name = off((38 * (n - 1) + 17) % YEAR)
    if abs(d) <= 20:
        lunarF.add(n)
    d, name = off((38 * (n - 1) + 36) % YEAR)
    northside = (d < 0) if name == 'D' else (d > 0)
    if abs(d) <= (20 if (northside or d == 0) else 7):
        solarF.add(n)
for n in sorted(lunarF):
    if n in lunarF and n + 1 in lunarF:
        lunarF.discard(n + 1)
# Iversen and Jones (2019), as the dial note gives the difference: the lunar mark of month 214 is in 213, the solar mark of month 207 is in 196
lunarI = (lunarF - {214}) | {213}
solarI = (solarF - {207}) | {196}
assert 214 in lunarF and 207 in solarF and 213 not in lunarF and 196 not in solarF
LISTS = {'Freeth': (lunarF, solarF), 'Iversen and Jones': (lunarI, solarI)}

row = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+\d{2}:\d{2}:\d{2}\s+-?\d+\s+(-?\d+)\s+-?\d+\s+([A-Za-z])\S*\s+\S+\s+(-?\d+\.\d+)')


def read(prefix, add):
    out = {}
    for f in sorted(f for d in CATS for f in glob.glob(os.path.join(d, prefix + '*.html'))):
        for line in open(f, encoding='utf-8', errors='replace'):
            m = row.match(html.unescape(re.sub(r'<[^>]*>', '', line)))
            if m:
                out[int(m.group(5)) + add] = (int(m.group(2)), m.group(3), int(m.group(4)), m.group(6), float(m.group(7)))
    return out


LE, SE = read('LE', 27257), read('SE', 27256)
print(f'\ncatalogue: {len(LE)} lunar and {len(SE)} solar eclipses read (the dial note: 5,776 and 5,674)')
two = json.load(open(os.path.join(R, 'dial', 'two_lists.json')))
date = lambda e: f'{e[2]} {e[1]} {"AD " + str(e[0]) if e[0] > 0 else str(1 - e[0]) + " BC"}'
cell = lambda n: (n - 1) % 223 + 1
cyc = lambda n: (n - 1) // 223

print('\n=== THE ECLIPSE DIAL by each published list, kind for kind (my recount from the catalogue pages) ===')
for name, (L, Sset) in LISTS.items():
    A = [sum(1 for n in range(223 * j + 1, 223 * j + 224) if n in LE and cell(n) in L) for j in range(123)]
    Sc = [sum(1 for n in range(223 * j + 1, 223 * j + 224) if n in SE and cell(n) in Sset) for j in range(123)]
    key = 'F' if name == 'Freeth' else 'IJ'
    same = all(A[j] == two[key][j]['A'] and Sc[j] == two[key][j]['S'] for j in range(123))
    a0 = next(j for j in range(123) if A[j] == 0); s0 = next(j for j in range(123) if Sc[j] == 0)
    lastL = max(n for n in LE if cell(n) in L and cyc(n) < 123)
    lastS = max(n for n in SE if cell(n) in Sset and cyc(n) < 123)
    lastL_all = max(n for n in LE if cell(n) in L); lastS_all = max(n for n in SE if cell(n) in Sset)
    print(f'{name}: my counts agree with two_lists.json in all 123 cycles: {same}')
    print(f'   months marked for the Moon: none with a lunar eclipse from cycle {a0} (and never again: {all(x == 0 for x in A[a0:])}); {a0} x 18.03 = {a0 * 18.03:.1f} years on -> AD {round(a0 * 18.03) - 204}')
    print(f'   months marked for the Sun:  none with a solar eclipse from cycle {s0} (and never again: {all(x == 0 for x in Sc[s0:])}); {s0} x 18.03 = {s0 * 18.03:.1f} years on -> AD {round(s0 * 18.03) - 204}')
    print(f'   the last lunar eclipse in a month marked for the Moon: {date(LE[lastL])} (cell {cell(lastL)}, cycle {cyc(lastL)}); the last solar eclipse in a month marked for the Sun: {date(SE[lastS])} (cell {cell(lastS)}, cycle {cyc(lastS)})')
    print(f'   (to the end of the catalogue pages, AD 2100, nothing later: {lastL_all == lastL and lastS_all == lastS})')
    print(f'   so no month has held the eclipse it is marked for in the {2026 - max(LE[lastL][0], SE[lastS][0])} years since {max(LE[lastL][0], SE[lastS][0])}; counted from the page\'s date for the cycle, {2026 - (round(max(a0, s0) * 18.03) - 204)} years')
    moon_only = L - Sset
    lastX = max(n for n in SE if cell(n) in moon_only)
    cntX = sum(1 for n in SE if cell(n) in moon_only and cyc(n) >= s0)
    print(f'   months marked only for the Moon ({len(moon_only)}) holding eclipses of the SUN: the last {date(SE[lastX])} (cell {cell(lastX)}); {cntX} of them from cycle {s0} on')
    sun_only = Sset - L
    print(f'   months marked only for the Sun holding eclipses of the MOON: from the dial\'s first month on (cycles 0 to 122 and the one now running): {sum(1 for n in LE if n >= 1 and cell(n) in sun_only)}; '
          f'in the catalogue\'s years before the dial\'s first month (300 to 205 BC, not the page\'s span): {sum(1 for n in LE if n < 1 and cell(n) in sun_only)}')

print('\n=== "Today they fall two cells after its marks" (Freeth\'s marks for the Moon; the same by the other list but for 213/214) ===')
def after_mark(c, L):
    # how many cells after the nearest mark at or before it, going round the spiral
    k = 0
    while cell(c - k) not in L:
        k += 1
    return k
from collections import Counter
for label, lo, hi in (('the eighteen years to 23 November 2026', 2008.9, 2026.9), ('2024 to 2026', 2024, 2026.99), ('2000 to 2100', 2000, 2100.99)):
    for kinds, kn in (('PT', 'partial or total'), ('NPT', 'of any kind')):
        offs = Counter()
        for n, e in LE.items():
            y = e[0] + ('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split().index(e[1]) + 0.5) / 12
            if lo <= y <= hi and e[3] in kinds:
                offs[after_mark(cell(n), lunarF)] += 1
        print(f'   lunar eclipses {kn}, {label}: cells after the nearest mark before them: {dict(sorted(offs.items()))}')
for n, e in sorted(LE.items()):
    if 2008 <= e[0] <= 2026 and e[3] in 'PT' and after_mark(cell(n), lunarF) != 2:
        print(f'   the exception: {date(e)} (kind {e[3]}), cell {cell(n)}, {after_mark(cell(n), lunarF)} cell after the mark in cell {cell(n) - after_mark(cell(n), lunarF)}')
n26 = next(n for n, e in LE.items() if e[:3] == (2026, 'Mar', 3))
print(f'   3 March 2026: kind {LE[n26][3]}, cell {cell(n26)}; cell 149 marked for the Moon: {149 in lunarF} (Freeth), {149 in lunarI} (Iversen and Jones); cell 151 marked: {151 in (lunarF | solarF)}; cell 150 marked: {150 in (lunarF | solarF)}')

print('\n=== THE LONG ACCOUNT: "the 13 in months without a solar glyph all passed south of the Earth\'s centre" ===')
se0 = {n: SE[n] for n in range(1, 224) if n in SE}
out = sorted(n for n in se0 if n not in solarF)
print(f'first cycle: {len(se0)} solar eclipses; in months without a solar mark: {len(out)}')
for n in out:
    e = se0[n]
    print(f'   month {n:3d}: {date(e):>14s}  kind {e[3]}  gamma {e[4]:+.4f}  {"SOUTH" if e[4] < 0 else "NORTH"}  month marked for the Moon: {n in lunarF}')
print(f'   all thirteen south (gamma below 0): {all(se0[n][4] < 0 for n in out)}; gamma from {min(se0[n][4] for n in out):+.2f} to {max(se0[n][4] for n in out):+.2f} (the dial note: -1.49 to -0.43); in months marked for the Moon: {sum(n in lunarF for n in out)}')
inn = sorted(n for n in se0 if n in solarF)
print(f'   the 28 in months WITH a solar mark: gamma from {min(se0[n][4] for n in inn):+.2f} to {max(se0[n][4] for n in inn):+.2f}; of them south: {sum(se0[n][4] < 0 for n in inn)} (so "the side the rule leaves out" is left out in part, not wholly)')
print(f'   by Iversen and Jones\'s list: in months without a solar mark: {sum(1 for n in se0 if n not in solarI)}, all south: {all(se0[n][4] < 0 for n in se0 if n not in solarI)}')

print('\n=== A FIST AT ARM\'S LENGTH ===')
for w, a in ((8, 60), (9, 65), (10, 60), (10, 70), (11, 62)):
    print(f'   a fist {w} cm wide at {a} cm: {2 * math.degrees(math.atan(w / 2 / a)):.1f} deg')
