"""Evidence reading: the sentence of "In short", "no month that it marks has held one since about AD 1058", read literally.
The page's counts ask whether a month marked for the Moon held an eclipse of the Moon, and a month marked for the Sun an
eclipse of the Sun. Read literally the sentence also covers a marked month that held an eclipse of the OTHER kind.
This recounts from NASA's catalogue pages with a parser of its own (the pages are data: run under -I, read only).
usage: python ev6_literal.py RECORDS_DIR CATDIR [CATDIR ...]
Prints; writes nothing."""
import glob
import html
import json
import os
import re
import sys

R, CATS = sys.argv[1], sys.argv[2:]

# --- Freeth's model of the marks (as the dial note describes it; written again here) --------------------------------
YEAR, NODES = 446, ((66, 'D'), (289, 'A'))


def off(p):
    best = None
    for node, name in NODES:
        d = (p - node + YEAR // 2) % YEAR - YEAR // 2
        if best is None or abs(d) < abs(best[0]):
            best = (d, name)
    return best


lunar, solar = set(), set()
for n in range(1, 224):
    d, name = off((38 * (n - 1) + 17) % YEAR)
    if abs(d) <= 20:
        lunar.add(n)
    d, name = off((38 * (n - 1) + 36) % YEAR)
    northside = (d < 0) if name == 'D' else (d > 0)
    if abs(d) <= (20 if (northside or d == 0) else 7):
        solar.add(n)
for n in sorted(lunar):
    if n in lunar and n + 1 in lunar:
        lunar.discard(n + 1)
print(f'marks: {len(lunar)} lunar, {len(solar)} solar, {len(lunar | solar)} cells; cells with both: {len(lunar & solar)}')

# --- the catalogue ----------------------------------------------------------------------------------------------------
row = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+\d{2}:\d{2}:\d{2}\s+-?\d+\s+(-?\d+)\s+-?\d+\s+([A-Za-z])')


def read(prefix, add):
    out = {}
    files = sorted(f for d in CATS for f in glob.glob(os.path.join(d, prefix + '*.html')))
    for f in files:
        for line in open(f, encoding='utf-8', errors='replace'):
            m = row.match(html.unescape(re.sub(r'<[^>]*>', '', line)))
            if not m:
                continue
            month = int(m.group(5)) + add
            assert month not in out, (f, month)
            out[month] = (f'{int(m.group(2))} {m.group(3)} {m.group(4)}', m.group(6))
    return out, len(files)


LE, nl = read('LE', 27257)
SE, ns = read('SE', 27256)
print(f'{nl} lunar pages, {len(LE)} lunar eclipses; {ns} solar pages, {len(SE)} solar eclipses (the dial note: 24 and 5,776; 24 and 5,674)')

# --- the page's own counts, made again, as a test of this parser ---------------------------------------------------------
cat = json.load(open(os.path.join(R, 'dial', 'catalogue_all.json')))
bad = 0
rows = []
for j in range(123):
    b = 223 * j
    le = {n - b: LE[n] for n in range(b + 1, b + 224) if n in LE}
    se = {n - b: SE[n] for n in range(b + 1, b + 224) if n in SE}
    um = {n for n in le if le[n][1] in 'PT'}
    r = dict(cycle=j, A=len(lunar & set(le)), Aum=len(lunar & um), S=len(solar & set(se)), U=len(um - lunar),
             L_in_solar_only=sorted((set(le) & solar) - lunar), Lum_in_solar_only=sorted((um & solar) - lunar),
             S_in_lunar_only=sorted((set(se) & lunar) - solar),
             any_in_marked=sorted((set(le) | set(se)) & (lunar | solar)),
             first=min([LE[n][0] for n in range(b + 1, b + 224) if n in LE][:1] + ['?']))
    rows.append(r)
    c = cat[j]
    if (r['A'], r['Aum'], r['S'], r['U']) != (c['A'], c['Aum'], c['S'], c['U']):
        bad += 1
print('cycles where this recount differs from catalogue_all.json in A, Aum, S or U:', bad, 'of 123')

yr = lambda j: round(j * 18.03) - 204
print('\ncycle (begins AD): marked-for-Moon with a lunar eclipse | marked-for-Sun with a solar eclipse | cells marked for the Sun only that held a LUNAR eclipse (partial or total) | cells marked for the Moon only that held a SOLAR eclipse | marked cells holding an eclipse of either kind')
for r in rows:
    j = r['cycle']
    if j in (0, 1, 30, 50, 55, 60, 63, 64, 65, 68, 69, 70, 71, 72, 75, 80, 90, 100, 110, 120, 121, 122):
        print(f"  {j:3d} ({yr(j):5d}): {r['A']:2d} | {r['S']:2d} | {len(r['L_in_solar_only']):2d} ({len(r['Lum_in_solar_only'])}) | {len(r['S_in_lunar_only']):2d} | {len(r['any_in_marked']):2d}")
after = [r for r in rows if r['cycle'] >= 70]
print('\nfrom cycle 70 (AD 1058) on:')
print('  cycles in which some marked cell held an eclipse of either kind:', sum(bool(r['any_in_marked']) for r in after), 'of', len(after))
print('  marked cells holding an eclipse, per cycle, least and most:', min(len(r['any_in_marked']) for r in after), max(len(r['any_in_marked']) for r in after))
print('  the last whole cycle (122, ended January 2014): marked cells that held an eclipse:', rows[122]['any_in_marked'])
print('     of those, lunar eclipses in cells marked for the Sun only:', rows[122]['L_in_solar_only'], '; solar eclipses in cells marked for the Moon only:', rows[122]['S_in_lunar_only'])
last_zero = [r['cycle'] for r in rows if not r['any_in_marked']]
print('  cycles in which NO marked cell held an eclipse of either kind:', last_zero)
# since the last whole cycle
b = 223 * 123
tail_le = {n - b: LE[n] for n in range(b + 1, b + 224) if n in LE}
tail_se = {n - b: SE[n] for n in range(b + 1, b + 224) if n in SE}
print('\nthe cycle now running (123, from January 2014): eclipses to the end of the catalogue pages that fall in a marked cell:')
for n in sorted(set(tail_le) | set(tail_se)):
    if n in (lunar | solar):
        kinds = []
        if n in tail_le: kinds.append('lunar eclipse ' + tail_le[n][0] + ' (' + tail_le[n][1] + ')')
        if n in tail_se: kinds.append('solar eclipse ' + tail_se[n][0] + ' (' + tail_se[n][1] + ')')
        print(f'   cell {n}: marked for {"the Moon" if n in lunar else ""}{" and " if n in lunar and n in solar else ""}{"the Sun" if n in solar else ""}; held: {"; ".join(kinds)}')

# --- examples, so that the finding can be checked by eye against the catalogue ------------------------------------------
print('\nexamples: solar eclipses in cells marked for the Moon only')
for j in (70, 80, 90, 95, 96):
    b = 223 * j
    ex = [(n - b, SE[n][0], SE[n][1]) for n in range(b + 1, b + 224) if n in SE and (n - b) in lunar and (n - b) not in solar]
    print(f'  cycle {j} (begins AD {yr(j)}): {len(ex)}', ex[:4], '...' if len(ex) > 4 else '')
allhits = [(n, SE[n][0]) for n in sorted(SE) if ((n - 1) % 223 + 1) in (lunar | solar) and n > 223 * 70]
allhits += [(n, LE[n][0]) for n in sorted(LE) if ((n - 1) % 223 + 1) in (lunar | solar) and n > 223 * 70]
last = max(allhits)
print('the last eclipse of either kind in a marked cell:', last[1], 'cell', (last[0] - 1) % 223 + 1, 'cycle', (last[0] - 1) // 223,
      '| number of such eclipses from cycle 70 on:', len(allhits))
print('per cycle from 70:', [len(rows[j]['any_in_marked']) for j in range(70, 97)])

# --- "months without a mark" read literally (no mark of either kind) ------------------------------------------------------
print('\n"months without a mark", read as months with no mark of either kind:')
print('  lunar eclipses of any kind in cells marked for the Sun only, all 123 cycles:', sum(len(r['L_in_solar_only']) for r in rows))
b = 0
se0 = {n: SE[n] for n in range(1, 224) if n in SE}
out = sorted(n for n in se0 if n not in solar)
print(f'  first cycle: {len(se0)} solar eclipses; {len(out)} in months not marked for the Sun: {out}')
print(f'     of those, in months marked for the Moon: {[n for n in out if n in lunar]} ({sum(n in lunar for n in out)}); in months with no mark at all: {[n for n in out if n not in lunar]} ({sum(n not in lunar for n in out)})')
le0 = {n: LE[n] for n in range(1, 224) if n in LE}
print(f'  first cycle: {len(le0)} lunar eclipses, {sum(v[1] in "PT" for v in le0.values())} partial or total; lunar eclipses in months not marked for the Moon: {sorted(n for n in le0 if n not in lunar)}; of those in months marked for the Sun: {sorted(n for n in le0 if n not in lunar and n in solar)}')
