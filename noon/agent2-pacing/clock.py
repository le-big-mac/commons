"""The same rule on newer clocks, and three smaller checks.   Added 26 November 2026, after a reader's report.
usage: python -I clock.py DATADIR AICCTABLE WORKDIR > clock.out        (numpy; pacing.py beside it; about a minute)
DATADIR holds the two files pacing.py reads (the Dome C record on the EDC3 time scale and the orbital solution).
AICCTABLE is the table of Bouchet and others (2023), https://doi.pangaea.de/10.1594/PANGAEA.990377?format=textfile
(depth; ice age on AICC2012; ice age on AICC2023; ...). WORKDIR is an empty folder for the re-dated copies.
1. Each sample of the record keeps its depth and temperature and gets the age its depth has on AICC2012 or on
   AICC2023; pacing.py is then run on the copy, unchanged.
2. On the EDC3 dates: the terminations younger than 440 thousand years (six) and the older ones (four) apart; and
   the four that fall where the EDC3 clock was tied to minima of the tilt and to nothing radiometric (219, 247, 339,
   428) against the other six. The clock's ten such markers run from 71 to 431 thousand years ago (Parrenin and
   others 2007, Table 1); the youngest termination is pinned by layer counts and the one at 134 by a cave-dated marker.
3. On the EDC3 dates: the event my rule dates at 507 thousand years ago moved to 530, where the papers put
   Termination VI.
4. Where the record crosses my upper line near 507 and 530 thousand years ago.
5. On each clock, by how much the cold before that event passes my lower line: the rule counts a termination only
   if the record has first been below that line."""
import os, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def read_table(tab):
    z, a12, a23 = [], [], []; body = 0
    for line in open(tab, encoding='utf-8'):
        if body == 0:
            if line.startswith('*/'): body = 1
            continue
        if body == 1: body = 2; continue
        p = line.rstrip('\n').split('\t')
        if p[1] == '' or p[2] == '': continue
        z.append(float(p[0])); a12.append(float(p[1]) * 1000); a23.append(float(p[2]) * 1000)
    z, a12, a23 = map(np.array, (z, a12, a23))
    assert np.all(np.diff(z) > 0) and np.all(np.diff(a12) > 0) and np.all(np.diff(a23) > 0)
    return z, a12, a23

def redate(src, z, a, out):
    n = 0; big = 0.0; started = False
    with open(out, 'w', encoding='latin-1') as f:
        for line in open(src, encoding='latin-1'):
            p = line.split()
            if not started:
                f.write(line); started = len(p) >= 5 and p[0] == 'Bag' and p[2] == 'Age'; continue
            if len(p) == 5 and float(p[1]) <= z.max():
                new = float(np.interp(float(p[1]), z, a)); big = max(big, abs(new - float(p[2])))
                f.write(f"{p[0]} {p[1]} {new:.5f} {p[3]} {p[4]}\n"); n += 1
    return n, big / 1000

def run(datadir, workdir, tag):
    out = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'pacing.py'), datadir, os.path.join(workdir, tag + '.npz')],
                         capture_output=True, text=True, check=True).stdout
    return out

def events(out):
    return [(float(a), float(b), float(c)) for a, b, c in re.findall(r'^\s+([\d.]+) thousand years ago: tilt [\d.]+ deg, tilt phase\s+(\d+), precession phase\s+(\d+)', out, re.M)]

R = lambda ph: float(np.abs(np.exp(1j * np.radians(ph)).mean()))
mean = lambda ph: float(np.degrees(np.angle(np.exp(1j * np.radians(ph)).mean())) % 360)
rising = lambda ph: int(sum(180 <= p < 360 for p in ph))

def chance(r, n, rng, draws=200000):
    sim = np.abs(np.exp(1j * rng.uniform(0, 2 * np.pi, (draws, n))).mean(1)); return float((sim >= r).mean())

def headline(out):
    keep = [l for l in out.splitlines() if l.startswith(('I1', 'I2', 'I3', 'I4', 'I5')) or 'within 12 of' in l or 'eccentricity phases' in l]
    return "\n".join("   " + l.strip() for l in keep)

if __name__ == '__main__':
    datadir, tab, work = sys.argv[1:4]
    rng = np.random.default_rng(26)
    z, a12, a23 = read_table(tab)
    print(f"the table: {len(z)} depths from {z.min():.2f} to {z.max():.2f} m; AICC2012 to {a12.max() / 1000:.1f}, AICC2023 to {a23.max() / 1000:.1f} thousand years")
    base = run(datadir, work, 'edc3'); ev = {'EDC3 (2007)': events(base)}
    print("1. the rule on three clocks\nEDC3 (2007), as on the page:\n" + headline(base))
    for tag, a, name in (('aicc2012', a12, 'AICC2012'), ('aicc2023', a23, 'AICC2023')):
        d = os.path.join(work, tag); os.makedirs(d, exist_ok=True)
        shutil.copy(os.path.join(datadir, 'INSOLN.LA2004.BTL.ASC'), d)
        n, big = redate(os.path.join(datadir, 'edc3deuttemp2007.txt'), z, a, os.path.join(d, 'edc3deuttemp2007.txt'))
        out = run(d, work, tag); ev[name] = events(out)
        print(f"{name}: {n} samples re-dated, the largest change of age {big:.2f} thousand years\n" + headline(out))
        var = re.findall(r'smoothing \d, percentiles \d+/\d+:\s+(\d+) terminations; tilt R ([\d.]+) \(p ([\d.]+)\), mean (\d+)', out)
        rs = [float(v[1]) for v in var]; ps = [float(v[2]) for v in var]; ns = [int(v[0]) for v in var]
        print(f"   the 18 other choices of the rule: {min(ns)} to {max(ns)} terminations; tilt R {min(rs):.2f} to {max(rs):.2f}; p {min(ps):.3f} to {max(ps):.3f}, below 0.03 in {sum(p < 0.03 for p in ps)} of 18")
    print("   on each clock: number of events, tilt R, mean tilt phase, how many on a rising tilt (phase 180 to 360), precession R")
    for name, e in ev.items():
        t = [x[1] for x in e]; pr = [x[2] for x in e]
        print(f"   {name}: {len(e)}; {R(t):.3f}; {mean(t):.0f}; {rising(t)} of {len(e)}; {R(pr):.3f}")
    e = ev['EDC3 (2007)']
    print("2. the EDC3 dates in two halves (the clock was tied to the tilt's minima in the younger half, to precession in the older)")
    for name, part in (("younger than 440 thousand years", [x for x in e if x[0] < 440]), ("older", [x for x in e if x[0] >= 440])):
        t = [x[1] for x in part]; pr = [x[2] for x in part]
        print(f"   {name}: {len(part)} events; tilt R {R(t):.2f} (uniform phases do as well with chance {chance(R(t), len(t), rng):.3f}), mean phase {mean(t):.0f}, {rising(t)} rising; precession R {R(pr):.2f} (chance {chance(R(pr), len(pr), rng):.3f})")
    for name, part in (("the four at 219, 247, 339 and 428", [x for x in e if 200 < x[0] < 440]), ("the other six", [x for x in e if not 200 < x[0] < 440])):
        t = [x[1] for x in part]
        print(f"   {name}: tilt R {R(t):.2f} (chance {chance(R(t), len(t), rng):.3f}), mean phase {mean(t):.0f}, {rising(t)} of {len(t)} rising")
    for name, part in (("the three at 219, 247 and 339, where only tilt markers hold the clock", [x for x in e if 200 < x[0] < 400]),
                       ("the three at 219, 339 and 428 (the four without 247)", [x for x in e if 200 < x[0] < 440 and abs(x[0] - 247.0) > 1]),
                       ("all but the 507 event", [x for x in e if abs(x[0] - 507.4) > 1])):
        t = [x[1] for x in part]
        print(f"   {name}: tilt R {R(t):.2f}, mean phase {mean(t):.0f}, {rising(t)} of {len(t)} rising")
    near = [x[1] for x in e if min(x[1], 360 - x[1]) <= 90]
    print(f"   within 90 degrees of a maximum of the tilt: {len(near)} of {len(e)}")
    print("3. the 507 event moved to 530 thousand years ago")
    orb = np.array([[float(x.replace('D', 'E')) for x in line.split()] for line in open(os.path.join(datadir, 'INSOLN.LA2004.BTL.ASC')) if line.strip()])
    orb = orb[(orb[:, 0] <= 0) & (orb[:, 0] >= -1000)]; oage = -orb[:, 0]; obl = np.degrees(orb[:, 2])
    idx = [i for i in range(1, len(obl) - 1) if obl[i] > obl[i - 1] and obl[i] >= obl[i + 1]]
    marks = np.array([oage[i] + 0.5 * (obl[i - 1] - obl[i + 1]) / (obl[i - 1] - 2 * obl[i] + obl[i + 1]) * (oage[1] - oage[0]) for i in idx])
    def phase(t):
        older = marks[marks >= t].min(); younger = marks[marks < t].max(); return 360.0 * (older - t) / (older - younger)
    assert all(abs(((phase(x[0]) - x[1] + 180) % 360) - 180) < 1.0 for x in e), "my phases do not match pacing.py's"
    t2 = [x[1] if abs(x[0] - 507.4) > 1 else phase(530.0) for x in e]
    print(f"   tilt phase at 530: {phase(530.0):.0f}; with it in place of the 507 event: R {R(t2):.2f} (chance {chance(R(t2), len(t2), rng):.3f}), mean phase {mean(t2):.0f}, {rising(t2)} of {len(t2)} rising")
    print("4. the smoothed record between 480 and 540 thousand years ago, on EDC3 (see results.npz from pacing.py)")
    d = np.load(os.path.join(work, 'edc3.npz'), allow_pickle=True)
    grid, sm, L, U = d['grid'], d['sm'], float(d['L']), float(d['U'])
    print(f"   my lower and upper lines: {L:.2f} and {U:.2f}; halfway {(L + U) / 2:.2f}")
    print("   age, smoothed temperature: " + ", ".join(f"{a:.0f}: {np.interp(a, grid, sm):+.2f}" for a in range(545, 479, -5)))
    m = (grid >= 480) & (grid <= 545); up = [float(g) for g, x, y in zip(grid[m][:-1], sm[m][:-1], sm[m][1:]) if (x - U) * (y - U) < 0]
    half = [float(g) for g, x, y in zip(grid[m][:-1], sm[m][:-1], sm[m][1:]) if (x - (L + U) / 2) * (y - (L + U) / 2) < 0]
    print(f"   it crosses the upper line at about {', '.join(f'{u:.1f}' for u in up)}; the halfway line at about {', '.join(f'{u:.1f}' for u in half)}; its highest between 480 and 545 is {sm[m].max():+.2f} at {grid[m][sm[m].argmax()]:.1f}")
    print("5. the coldest smoothed value between 535 and 560 thousand years ago, less my lower line (negative: the rule is armed)")
    for tag in ('edc3', 'aicc2012', 'aicc2023'):
        d = np.load(os.path.join(work, tag + '.npz'), allow_pickle=True); g, x, Lq = d['grid'], d['sm'], float(d['L'])
        mm = (g >= 535) & (g <= 560)
        print(f"   {tag}: {x[mm].min() - Lq:+.3f} degrees, at {g[mm][x[mm].argmin()]:.1f} thousand years ago")
