"""The mechanism's own eclipse dial (the eclipse year model of Freeth 2014, eym.py) against the real sky.
usage: dial.py trial            a made-up sky with a planted offset and drift
       dial.py DATADIR          the real Sun and Moon tables (76 years from 1 May 205 BC, and the 76 years to today)

Months are numbered as on the dial: month n holds the n-th full moon and then the n-th new moon, the first
full moon being the first after 1 May 205 BC (12 May). Cycle j is months 223 j + 1 to 223 j + 223.
A syzygy's latitude is the Moon's latitude of date at the instant of full or new moon.
The dial's limits, 20 and 7 units of 446 to the eclipse year, are turned into latitudes with the mean
inclination 5.145 deg: 20 units = 16.14 deg from the node = 1.43 deg of latitude; 7 units = 5.65 deg = 0.51 deg."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import eym

INC = 5.145
LIM_N = INC * np.sin(np.radians(20 * 360.0 / 446))      # 1.43
LIM_S = INC * np.sin(np.radians(7 * 360.0 / 446))       # 0.51
wrap = lambda x: (np.asarray(x) + 180.0) % 360.0 - 180.0


def glyph_months():
    lunar, solar = eym.glyphs()
    for n in sorted(lunar):                      # the consecutive-month rule: the second of two goes
        if n in lunar and n + 1 in lunar: del lunar[n + 1]
    assert len(lunar) == 38 and len(solar) == 28 and len(set(lunar) | set(solar)) == 51
    return lunar, solar


def syzygies(moon, sun):
    """Times and latitudes of full and new moons from the tables (longitude of date)."""
    sunT = np.interp(moon['jd'], sun['jd'], np.unwrap(np.radians(sun['T'])) * 180 / np.pi)
    D = wrap(moon['T'] - sunT)
    out = {}
    for kind, off in (('new', 0.0), ('full', 180.0)):
        d = wrap(D - off)
        i = np.where((d[:-1] < 0) & (d[1:] >= 0) & (d[1:] - d[:-1] < 90))[0]
        f = -d[i] / (d[i + 1] - d[i])
        out[kind] = (moon['jd'][i] + f * (moon['jd'][i + 1] - moon['jd'][i]), moon['lat'][i] + f * (moon['lat'][i + 1] - moon['lat'][i]))
    return out


def number(sz, first_full_index=1):
    """Dial month numbers: the first full moon is FM of month `first_full_index`; each new moon takes the number
    of the full moon before it. Returns dicts month -> latitude."""
    ft, fb = sz['full']; nt, nb = sz['new']
    FM = {first_full_index + k: float(fb[k]) for k in range(len(ft))}
    NM = {}
    for t, b in zip(nt, nb):
        k = np.searchsorted(ft, t) - 1           # the full moon before this new moon
        if k >= 0: NM[first_full_index + int(k)] = float(b)
    return FM, NM


def model_lat(n, kind, shift=0.0):
    """The latitude the model implies for month n's syzygy, with the node points moved by `shift` units."""
    p = (38 * (n - 1) + (17 if kind == 'full' else 36)) % 446
    th = np.radians((p - eym.DNP - shift) * 360.0 / 446)        # the Sun's distance past the descending node point
    b = -INC * np.sin(th)                                       # new moon: north before the descending node
    return -b if kind == 'full' else b                          # a full moon is at the other node


def fit_shift(FM, NM, months):
    """The shift of the node points (units of 446) that best fits the true latitudes of these months."""
    best = None
    for s in np.arange(-30, 30.01, 0.05):
        r = [FM[n] - model_lat(n, 'full', s) for n in months if n in FM] + [NM[n] - model_lat(n, 'new', s) for n in months if n in NM]
        c = float(np.mean(np.square(r)))
        if best is None or c < best[0]: best = (c, s)
    return best[1], np.sqrt(best[0])


def tally(FM, NM, lunar, solar, j):
    base = 223 * j
    L = [n for n in lunar if base + n in FM]
    S = [n for n in solar if base + n in NM]
    lun_ok = sum(abs(FM[base + n]) <= LIM_N for n in L)
    sol_ok = sum(-LIM_S <= NM[base + n] <= LIM_N for n in S)
    umb = [n for n in range(1, 224) if base + n in FM and abs(FM[base + n]) < 1.0]
    umb_hit = sum(n in lunar for n in umb)
    sol_any = [n for n in range(1, 224) if base + n in NM and abs(NM[base + n]) < 1.5]
    sol_dial = [n for n in range(1, 224) if base + n in NM and -LIM_S <= NM[base + n] <= LIM_N]
    return dict(L=len(L), lun_ok=lun_ok, S=len(S), sol_ok=sol_ok, umb=len(umb), umb_hit=umb_hit,
                umb_missed=[n for n in umb if n not in lunar], sol_any=len(sol_any), sol_any_hit=sum(n in solar for n in sol_any),
                sol_dial=len(sol_dial), sol_dial_hit=sum(n in solar for n in sol_dial))


def report(FM, NM, lunar, solar, cycles, label):
    print(f'\n{label}')
    print('cycle: lunar glyph months that are true possibilities | solar glyph months inside the dial\'s own limits | '
          'umbral full moons on a lunar glyph | new moons inside the dial\'s limits on a solar glyph | fitted shift of the node points (units; deg), rms (deg)')
    out = {}
    for j in cycles:
        t = tally(FM, NM, lunar, solar, j)
        months = [223 * j + n for n in range(1, 224)]
        s, r = fit_shift({k - 223 * j: v for k, v in FM.items() if k in months}, {k - 223 * j: v for k, v in NM.items() if k in months}, range(1, 224))
        out[j] = dict(t, shift=s)
        print(f'  {j:3d}: {t["lun_ok"]:2d} of {t["L"]:2d} | {t["sol_ok"]:2d} of {t["S"]:2d} | {t["umb_hit"]:2d} of {t["umb"]:2d} (missed: {t["umb_missed"]}) | '
              f'{t["sol_dial_hit"]:2d} of {t["sol_dial"]:2d} | {s:+6.2f} units = {s * 360 / 446:+6.2f} deg, rms {r:.2f}')
    return out


def survival(shift0, rate, lunar, solar, upto=140):
    """By the model's own latitudes with the node points moved: how many glyph months stay inside the limits."""
    rows = []
    for j in range(0, upto + 1):
        s = shift0 + rate * j
        lun = sum(abs(model_lat(n, 'full', s)) <= LIM_N for n in lunar)
        sol = sum(-LIM_S <= model_lat(n, 'new', s) <= LIM_N for n in solar)
        rows.append((j, lun, sol))
    return rows


if __name__ == '__main__':
    lunar, solar = glyph_months()
    if sys.argv[1] == 'trial':
        rng = np.random.default_rng(1)
        SH, RATE = 3.0, -0.6                              # planted: node points 3 units late at the start, 0.6 a cycle
        FM, NM = {}, {}
        for n in range(1, 223 * 4 + 1):
            j = (n - 1) // 223; m = (n - 1) % 223 + 1
            s = SH + RATE * (j + (m - 1) / 223.0)
            FM[n] = float(model_lat(m, 'full', s) + rng.normal(0, 0.15))
            NM[n] = float(model_lat(m, 'new', s) + rng.normal(0, 0.15))
        out = report(FM, NM, lunar, solar, range(4), f'TRIAL: planted shift {SH} units at the start, {RATE} a cycle, noise 0.15 deg')
        print('  recovered shifts should be near', [round(SH + RATE * (j + 0.5), 2) for j in range(4)])
    else:
        import mech
        DATA = sys.argv[1]
        res = {}
        for w in ('then', 'now'):
            moon = mech.read(os.path.join(DATA, f'moon_{w}.txt')); sun = mech.read(os.path.join(DATA, f'sun_{w}.txt'))
            res[w] = syzygies(moon, sun)
        ft = res['then']['full'][0]
        print(f'first full moon in the table: JD {ft[0]:.2f} (1 May 205 BC is JD 1646667.5; 12 May is 1646678.5)')
        FM, NM = number(res['then'])
        out = report(FM, NM, lunar, solar, range(4), 'From 205 BC: the dial\'s first four cycles')
        shifts = [out[j]['shift'] for j in range(4)]
        rate = float(np.polyfit(np.arange(4), shifts, 1)[0])
        print(f'drift of the fitted shift over cycles 0 to 3: {rate:+.3f} units a cycle = {rate * 360 / 446:+.3f} deg a cycle')
        # the count of lunations across the gap, by the two windows' mean months
        syn = 0.5 * (np.polyfit(np.arange(len(ft)), ft, 1)[0] + np.polyfit(np.arange(len(res['now']['full'][0])), res['now']['full'][0], 1)[0])
        gap = (res['now']['full'][0][0] - ft[0]) / syn
        print(f'lunations from the first full moon then to the first now: {gap:.3f}')
        FM2, NM2 = number(res['now'], first_full_index=1 + int(round(gap)))
        last = max(FM2)
        jlast = (last - 1) // 223 - 1
        report(FM2, NM2, lunar, solar, [jlast], f'To today: the last whole cycle, cycle {jlast} of the dial (months {223 * jlast + 1} to {223 * jlast + 223}; the tables end in month {last})')
        # and the 223 months that end with the tables, each in its own cell of the dial
        FMr = {(n - 1) % 223 + 1: FM2[n] for n in range(last - 222, last + 1) if n in FM2}
        NMr = {(n - 1) % 223 + 1: NM2[n] for n in range(last - 222, last + 1) if n in NM2}
        report(FMr, NMr, lunar, solar, [0], f'To today: the 223 months ending with the tables (months {last - 222} to {last}), each in its own cell')
        print('\nSurvival by the model\'s own geometry, the node points moved by the fitted shift and drift:')
        rows = survival(shifts[0] - 0.5 * rate, rate, lunar, solar)
        print('  cycle (years after 205 BC): lunar glyph months inside the limit, solar glyph months inside the limits')
        for j, lun, sol in rows:
            if j <= 40 or j % 10 == 0: print(f'  {j:3d} ({j * 18.03:6.0f}): {lun:2d} of 38, {sol:2d} of 28')
