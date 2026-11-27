"""Small arithmetic behind the new sentences, from the saved outputs (nothing is recomputed from the map files).
usage: python figures.py /srv/commons/hemispheres-agent3"""
import sys, re, math, json, os

root = sys.argv[1]
R = 6371.0088


def km(a, b):
    (la1, lo1), (la2, lo2) = [(math.radians(x), math.radians(y)) for x, y in (a, b)]
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


south, north = (40.82, 1.72), (47.42, -2.36)
nantes = (47 + 13 / 60, -(1 + 32 / 60))            # the study's own Nantes (hemi_run.py)
dumet = (47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600))
print('== the opening sentence')
print(f'  northern summit 47.42 N, 2.36 W to Nantes (47.217 N, 1.533 W): {km(north, nantes):.0f} km; to Ile Dumet: {km(north, dumet):.0f} km; southern summit to Nantes: {km(south, nantes):.0f} km; summit to summit: {km(south, north):.0f} km')
s = open(os.path.join(root, 'out/summits.out')).read()
m = re.search(r'land ([\d,]+) km2 \| Catalan summit ([\d.]+)% .*?Breton summit ([\d.]+)% .*?= \+([\d.]+) points = \+([\d,]+) km2', s)
land = int(m.group(1).replace(',', '')); cs, bs, dp, dk = float(m.group(2)), float(m.group(3)), float(m.group(4)), int(m.group(5).replace(',', ''))
print(f'  scored run (out/summits.out, first row): land {land:,} km2; southern summit {cs}%, northern {bs}%; difference {dp} points = {dk:,} km2')
shares = re.findall(r'Catalan summit ([\d.]+)% .*?Breton summit ([\d.]+)%', s)
print(f'  the ten variants of out/summits.out: southern {min(float(a) for a, b in shares):.2f} to {max(float(a) for a, b in shares):.2f}%, northern {min(float(b) for a, b in shares):.2f} to {max(float(b) for a, b in shares):.2f}%  (README adds two OpenStreetMap rows at 80.3%)')
est = 45339  # km2, Estonia, from memory (no network); some sources give 45,227
print(f'  46,120 km2 is {dk / est:.2f} of Estonia taken as {est:,} km2 (from memory)')
a = open(os.path.join(root, 'out/after_review.out')).read()
for name, d in re.findall(r'^\s+(map latitude[^:]*|equal-area sphere|plane through[^:]*): best [\d.]+%; best - Nantes ([\d.]+)', a, re.M):
    print(f'  best minus the half centred on Nantes itself, {name[:45]}: {d} points = {float(d) / 100 * land:,.0f} km2 = {float(d) / 100 * land / est:.2f} Estonias  (summit against summit: {dk / est:.2f})')

print('== the people')
sc = open(os.path.join(root, 'second-map/out/score.out')).read()
rows = []
for line in sc.splitlines():
    p = [x.strip() for x in line.split('|')]
    if len(p) == 10 and p[1][:1].isdigit():
        mm = re.match(r'([\d.]+)% at ([\d.]+) N, ([\d.]+) E', p[2])
        rows.append(dict(name=p[0], total=float(p[1]), best=float(mm.group(1)), lat=float(mm.group(2)), lon=float(mm.group(3)), valais=float(p[3]), pal=float(p[4]), berlin=float(p[5]), diff=float(p[9])))
berlin_mid = (52.52, 13.405)  # middle of Berlin, from memory
for r in rows:
    yr = int(r['name'].split()[-1]); r['year'] = yr; r['set'] = r['name'].rsplit(' ', 1)[0]
    where = 'Alps' if r['lat'] < 47.5 else ('near Berlin' if r['lat'] > 51 else 'Palatinate')
    r['where'] = where
    print(f"  {r['set']:22s} {yr}: best {r['best']:.3f}% at {r['lat']:.2f} N, {r['lon']:.2f} E = {where:11s} ({km((r['lat'], r['lon']), berlin_mid):4.0f} km from the middle of Berlin); Berlin half minus Alpine half {r['diff']:+5.1f} million of {r['total'] * 1000:,.0f} million = {abs(r['diff']) / (r['total'] * 1000) * 100:.3f}%; best minus Palatinate {r['best'] - r['pal']:+.3f} points")
print('  "in the western Alps in every year I tried up to 2010, and near Berlin from 2020 on":')
for st in sorted(set(r['set'] for r in rows)):
    up = [(r['year'], r['where']) for r in rows if r['set'] == st and r['year'] <= 2010]
    on = [(r['year'], r['where']) for r in rows if r['set'] == st and r['year'] >= 2020]
    mid = [(r['year'], r['where'], round(r['best'] - r['pal'], 3)) for r in rows if r['set'] == st and 2010 < r['year'] < 2020]
    print(f'    {st}: up to 2010 {up} all Alps: {all(w == "Alps" for y, w in up)}; from 2020 {on} all near Berlin: {all(w == "near Berlin" for y, w in on)}; between: {mid}')
d2020 = [r['diff'] for r in rows if r['year'] == 2020]
print(f'  the lead in 2020 on the three sets: {sorted(d2020)} million; totals {[r["total"] for r in rows if r["year"] == 2020]} thousand million')
b2020 = [r['best'] for r in rows if r['year'] == 2020]
print(f'  best share in 2020 on the three sets: {b2020} -> all round to 92.7: {all(round(x, 1) == 92.7 for x in b2020)}')
print(f'  centre of the people\'s half 52.37 N, 12.68 E to the middle of Berlin (52.52 N, 13.405 E, from memory): {km((52.37, 12.68), berlin_mid):.0f} km; Rankin\'s point 46.5 N, 7 E to it: {km((46.5, 7), (52.37, 12.68)):.0f} km')

print('== the woodpeckers')
w = open(os.path.join(root, 'out/woodpeckers_clean.out')).read()
print('  ' + w.splitlines()[1])
print(f'  43.0 N, 0.9 W to Auch (43.65 N, 0.59 E, from memory): {km((43.0, -0.9), (43.65, 0.59)):.0f} km; to Pau (43.30 N, 0.37 W): {km((43.0, -0.9), (43.30, -0.37)):.0f} km')

print('== the search')
logp = os.path.join(root, 'prior-art-tools/fetch-log.txt')
if os.path.exists(logp):
    L = open(logp).read().splitlines()
    print(f'  prior-art-tools/fetch-log.txt: {sum(1 for x in L if "| SEARCH |" in x)} lines SEARCH, {sum(1 for x in L if "| FETCH |" in x)} lines FETCH')
