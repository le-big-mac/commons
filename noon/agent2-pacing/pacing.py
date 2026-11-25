"""Are the terminations of the ice ages paced by the Earth's tilt?   usage: python -I pacing.py DATADIR out.npz

Data: EPICA Dome C temperature on the EDC3 time scale (Jouzel et al. 2007); the orbital solution La2004
(Laskar et al. 2004): time in thousands of years (negative = past), eccentricity, obliquity (rad), longitude of
perihelion from the moving equinox (rad).  The rules for terminations and phases were fixed in expectations.md.
"""
import sys
import numpy as np

D, OUT = sys.argv[1], sys.argv[2]
rng = np.random.default_rng(4)

# ---- the ice core
age, temp = [], []
started = False
for line in open(f"{D}/edc3deuttemp2007.txt", encoding='latin-1'):
    p = line.split()
    if not started:
        started = len(p) >= 5 and p[0] == 'Bag' and p[2] == 'Age'
        continue
    if len(p) == 5:
        age.append(float(p[2]) / 1000.0)
        temp.append(float(p[4]))
age, temp = np.array(age), np.array(temp)
assert np.all(np.diff(age) > 0) and age.max() > 790
print(f"ice core: {len(age)} samples with a temperature, from {age.min():.2f} to {age.max():.1f} thousand years ago")


def terminations(step=0.5, window=5.0, ql=25, qu=80):
    grid = np.arange(np.ceil(age.min() / step) * step, age.max(), step)
    raw = np.interp(grid, age, temp)
    k = int(round(window / step)) + 1
    pad = np.r_[raw[k // 2:0:-1], raw, raw[-2:-k // 2 - 1:-1]]
    sm = np.convolve(pad, np.ones(k) / k, mode='valid')
    assert len(sm) == len(grid)
    L, U = np.percentile(sm, ql), np.percentile(sm, qu)
    mid = (L + U) / 2
    out = []
    armed = False
    for i in range(len(grid) - 1, -1, -1):                              # forward in time: from the oldest sample to the youngest
        if sm[i] < L:
            armed = True
        elif armed and sm[i] > U:
            j = i
            while sm[j] > mid:                                          # walk back (older) to where the rise crossed halfway
                j += 1
            t = grid[j] + (grid[j - 1] - grid[j]) * (mid - sm[j]) / (sm[j - 1] - sm[j])
            out.append(t)
            armed = False
    return np.array(out[::-1]), grid, raw, sm, L, U                     # youngest first


# ---- the orbit
orb = np.array([[float(x.replace('D', 'E')) for x in line.split()] for line in open(f"{D}/INSOLN.LA2004.BTL.ASC") if line.strip()])
orb = orb[(orb[:, 0] <= 0) & (orb[:, 0] >= -1000)]
oage = -orb[:, 0]                                                       # thousands of years ago, increasing into the past
ecc, obl, peri = orb[:, 1], np.degrees(orb[:, 2]), orb[:, 3]
prec = ecc * np.sin(peri)                                               # least when northern midsummer is at perihelion
print(f"orbit today: tilt {obl[0]:.3f} deg, eccentricity {ecc[0]:.5f}, precession index {prec[0]:+.4f} (positive: northern summer far from the Sun)")


def extrema(y, sign):
    """ages of the local maxima (sign=+1) or minima (-1) of y, refined by a parabola through three points"""
    z = sign * y
    idx = [i for i in range(1, len(z) - 1) if z[i] > z[i - 1] and z[i] >= z[i + 1]]
    out = []
    for i in idx:
        a, b, c = z[i - 1], z[i], z[i + 1]
        out.append(oage[i] + 0.5 * (a - c) / (a - 2 * b + c) * (oage[1] - oage[0]))
    return np.array(out)


def phase(t, marks):
    """0 at each mark, rising evenly with time to 360 at the next (younger) mark"""
    older = marks[marks >= t].min()
    y = marks[marks < t]
    younger = y.max() if len(y) else marks.min() - np.diff(marks[:6]).mean()      # a date shaken to after the latest mark: the next mark is put one mean cycle on
    return 360.0 * (older - t) / (older - younger)


def rayleigh(ph):
    return float(np.abs(np.exp(1j * np.radians(ph)).mean()))


def chance(R, n, draws=200000):
    sim = np.abs(np.exp(1j * rng.uniform(0, 2 * np.pi, (draws, n))).mean(1))
    return float((sim >= R).mean())


def mean_phase(ph):
    return float(np.degrees(np.angle(np.exp(1j * np.radians(ph)).mean())) % 360)


tilt_max = extrema(obl, +1)
prec_min = extrema(prec, -1)
ecc_max = extrema(ecc, +1)
print(f"tilt maxima in the last 800,000 years: {int((tilt_max < 800).sum())}, mean spacing {np.diff(tilt_max[tilt_max < 850]).mean():.1f} thousand years; the latest {tilt_max[0]:.1f} thousand years ago")
print(f"precession: northern midsummer at perihelion {int((prec_min < 800).sum())} times, mean spacing {np.diff(prec_min[prec_min < 850]).mean():.1f}; the latest {prec_min[0]:.1f} thousand years ago")

T, grid, raw, sm, L, U = terminations()
n = len(T)
pt = np.array([phase(t, tilt_max) for t in T])
pp = np.array([phase(t, prec_min) for t in T])
pe = np.array([phase(t, ecc_max) for t in T])
print(f"I1  terminations found: {n}  (L = {L:.2f}, U = {U:.2f} degrees relative to the last thousand years)")
for t, a, b in zip(T, pt, pp):
    i = np.argmin(np.abs(oage - t))
    print(f"      {t:6.1f} thousand years ago: tilt {obl[i]:.2f} deg, tilt phase {a:5.0f}, precession phase {b:5.0f}")
Rt, Rp, Re = rayleigh(pt), rayleigh(pp), rayleigh(pe)
print(f"I2  tilt phases: R = {Rt:.3f}; evenly spread phases do as well with probability {chance(Rt, n):.4f}")
print(f"I3  mean tilt phase: {mean_phase(pt):.0f} degrees  (0 = tilt at its maximum; 270 = a quarter cycle before it)")
print(f"I4  precession phases: R = {Rp:.3f} (probability {chance(Rp, n):.4f}); mean phase {mean_phase(pp):.0f}")
print(f"    eccentricity phases, for the record: R = {Re:.3f} (probability {chance(Re, n):.4f}); mean phase {mean_phase(pe):.0f}")
gaps = np.diff(T)
near = [(abs(g - 82) <= 12) or (abs(g - 123) <= 12) for g in gaps]
print(f"I5  intervals between successive terminations (thousand years, youngest first): {[round(float(g), 1) for g in gaps]}")
print(f"    within 12 of 82 or 123: {int(sum(near))} of {len(gaps)}; in tilt cycles of 41: {[round(float(g) / 41.0, 2) for g in gaps]}")

# ---- afterwards: how much depends on the rule, and on the dating
print("afterwards, not registered: other choices of the rule")
for window in (3.0, 5.0, 7.0):
    for ql, qu in ((20, 80), (25, 80), (30, 80), (25, 70), (25, 85), (35, 75)):
        TT = terminations(window=window, ql=ql, qu=qu)[0]
        ph = np.array([phase(t, tilt_max) for t in TT])
        ph2 = np.array([phase(t, prec_min) for t in TT])
        print(f"   smoothing {window:.0f}, percentiles {ql}/{qu}: {len(TT):2d} terminations; tilt R {rayleigh(ph):.2f} (p {chance(rayleigh(ph), len(TT), 50000):.3f}), mean {mean_phase(ph):3.0f};"
              f" precession R {rayleigh(ph2):.2f} (p {chance(rayleigh(ph2), len(TT), 50000):.3f})")
print("afterwards: the dates shaken by a dating error (standard deviation in thousand years), 20,000 times each")
for sd in (2.0, 4.0, 6.0):
    Rs, Rps = [], []
    for _ in range(20000):
        TT = T + rng.normal(0, sd, n)
        TT = np.clip(TT, 0.5, 799)
        Rs.append(rayleigh([phase(t, tilt_max) for t in TT]))
        Rps.append(rayleigh([phase(t, prec_min) for t in TT]))
    Rs, Rps = np.array(Rs), np.array(Rps)
    crit = np.quantile(np.abs(np.exp(1j * rng.uniform(0, 2 * np.pi, (100000, n))).mean(1)), 0.95)
    print(f"   error {sd:.0f}: tilt R median {np.median(Rs):.2f} (5th to 95th pct {np.percentile(Rs, 5):.2f} to {np.percentile(Rs, 95):.2f}); still beyond the 5% level in {100 * (Rs > crit).mean():.0f}% of shakes;"
          f" precession R median {np.median(Rps):.2f}")
np.savez(OUT, T=T, grid=grid, raw=raw, sm=sm, L=L, U=U, oage=oage, obl=obl, prec=prec, ecc=ecc, tilt_max=tilt_max, prec_min=prec_min, pt=pt, pp=pp)
