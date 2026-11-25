"""Item 3: phases.py (the subject) against (a) the checker's own JPL syzygies in both windows, (b) the catalogue's instants of greatest
eclipse from -299 to 0, by half-century; and hours.delta_t against the catalogue's Delta T column."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, own
import phases, hours          # the subjects under test

for w in ('then', 'now'):
    full, new = own.syz(w)
    for name, t, off in (('new', new, 0.0), ('full', full, 0.5)):
        k0 = round((t[0] - 2451550.09766) / 29.530588861 - off) + off
        d = np.array([(phases.true_phase(k0 + i) - t[i]) * 1440 for i in range(len(t))])
        n = len(d); x = np.arange(n)
        slope = np.polyfit(x, d, 1)[0] * n
        print(f'{w} {name}: {n} syzygies, first k {k0}; Meeus - JPL (min): mean {d.mean():+.2f}, sd {d.std():.2f}, min {d.min():+.2f}, max {d.max():+.2f}; first quarter mean {d[:n//4].mean():+.2f}, last quarter {d[-n//4:].mean():+.2f}; trend over the window {slope:+.2f}')

cat = own.catalogue(-299, 0)
print(f'\ncatalogue rows -299..0: {len(cat)} (lunar {sum(r["kind"]=="LE" for r in cat)}, solar {sum(r["kind"]=="SE" for r in cat)})')
d = []; yr = []; kd = []
for r in cat:
    k = r['luna'] + (0.5 if r['kind'] == 'LE' else 0.0)
    t = phases.true_phase(k)
    d.append((t - r['jd']) * 1440); yr.append(r['y']); kd.append(r['kind'])
d = np.array(d); yr = np.array(yr); kd = np.array(kd)
print(f'all: Meeus syzygy - greatest eclipse (min): mean {d.mean():+.2f}, sd {d.std():.2f}, min {d.min():+.1f}, max {d.max():+.1f}; |d| > 20: {int((np.abs(d) > 20).sum())}; > 30: {int((np.abs(d) > 30).sum())}; > 720: {int((np.abs(d) > 720).sum())}')
for kind in ('LE', 'SE'):
    for lo in range(-300, 0, 50):
        m = (kd == kind) & (yr >= lo) & (yr < lo + 50)
        print(f'   {kind} {lo:5d}..{lo + 49:5d}: n {int(m.sum()):3d}  mean {d[m].mean():+6.2f}  sd {d[m].std():5.2f}  min {d[m].min():+6.1f}  max {d[m].max():+6.1f}')
for kind in ('LE', 'SE'):
    m = kd == kind
    p = np.polyfit(yr[m], d[m], 1)
    print(f'   {kind}: linear trend {p[0] * 300:+.2f} min over 300 years (se of mean per half-century about {d[m].std() / np.sqrt(m.sum() / 6):.2f})')
# the same for the JPL window, as a ruler for what the catalogue differences look like where JPL confirms Meeus
m = (yr >= -204) & (yr <= -129)
print(f'   inside the JPL window (-204..-129): n {int(m.sum())}, mean {d[m].mean():+.2f}, sd {d[m].std():.2f}, min {d[m].min():+.1f}, max {d[m].max():+.1f}')
m = ~m
print(f'   outside it: n {int(m.sum())}, mean {d[m].mean():+.2f}, sd {d[m].std():.2f}, min {d[m].min():+.1f}, max {d[m].max():+.1f}')

# Delta T
print('\nDelta T: hours.delta_t(year) - catalogue column (s), by half-century')
e = np.array([hours.delta_t(hours.year_of(r['jd'])) - r['dt'] for r in cat])
for lo in range(-300, 0, 50):
    m = (yr >= lo) & (yr < lo + 50)
    print(f'   {lo:5d}..{lo + 49:5d}: mean {e[m].mean():+6.1f}  min {e[m].min():+6.1f}  max {e[m].max():+6.1f}   (catalogue Delta T {np.array([r["dt"] for r in cat])[m].min():.0f} to {np.array([r["dt"] for r in cat])[m].max():.0f})')
print(f'   all: mean {e.mean():+.1f} s, min {e.min():+.1f}, max {e.max():+.1f}; in degrees of longitude: {e.min() / 240:+.2f} to {e.max() / 240:+.2f}')
print('   year_of check: JD 1646679.2 ->', hours.year_of(1646679.2), ' (12 May -204 is year -204 + 0.36 = -203.64)')
