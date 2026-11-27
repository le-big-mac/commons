# The lines of the fifth sheet (expectations-sun.md): does the darkness of a dark sky follow the Sun's eleven-year cycle,
# or do the photometers only read darker as they age?  Reads cache2/nights<YEAR>.pkl (dawnlib2.py) and the monthly
# 10.7 cm radio flux of the Sun (data/sun/solar-cycle.json, from NOAA's Space Weather Prediction Center).
# Usage: sunsheet.py YEAR[,YEAR...]            the lines on those years
#        sunsheet.py madeup                    the method on made-up levels of known kinds
#
# The measure. For each cleaned night, lev40: the middle reading, as 20.5 - 2.5 log10(frequency), over the minutes at
# which the point overhead is 40 degrees or more from the Milky Way's plane (60 minutes or more of them). For each
# instrument (a station; a change of the photometer's own address in the headers starts a new instrument) and each
# month with two such nights or more, the month's level is the middle of its nights. Each calendar month of each
# instrument that has three years or more is then taken about its own mean over the years, and so are that month's solar
# flux and date. What is fitted, by least squares over all such months, is
#       level = b x (flux, in hundreds of units) + c x (years) + scatter
# b is the Sun's part (negative: a brighter sky when the Sun is active), c the drift with time (positive: darker year by year).
import sys, json, pickle
import numpy as np
SUN = {r['time-tag']: r['f10.7'] for r in json.load(open('/home/agent1/night/data/sun/solar-cycle.json')) if r.get('f10.7') not in (None, -1)}
DARK = ['stars289', 'stars62', 'stars477', 'stars35', 'stars426']; TOWNS = ['stars33', 'stars76', 'stars1', 'stars52', 'stars7']; BETW = ['stars36', 'stars19', 'stars9', 'stars225', 'stars4', 'stars24']
def months(N, key='lev40'):
    """{(instrument, year, month): level} from nights; an instrument is (station, address)"""
    g = {}
    for c in N:
        if c.get(key) is None: continue
        g.setdefault(((c['st'], c.get('mac')), c['dusk'].year, c['dusk'].month), []).append(c[key])
    return {k: float(np.median(v)) for k, v in g.items() if len(v) >= 2}
def rows(M):
    """the fitted rows: (instrument, year, month, level anomaly, flux anomaly in hundreds, time anomaly in years)"""
    out = []; byim = {}
    for (ins, y, m), v in M.items():
        if f'{y}-{m:02d}' in SUN: byim.setdefault((ins, m), []).append((y, v))
    for (ins, m), L in byim.items():
        if len(L) < 3: continue
        ys = np.array([y for y, v in L], float); vs = np.array([v for y, v in L]); fs = np.array([SUN[f'{int(y)}-{m:02d}'] for y in ys]) / 100.0
        for y, v, fl in zip(ys, vs, fs): out.append((ins, int(y), m, v - vs.mean(), fl - fs.mean(), y - ys.mean()))
    return out
def fit(R):
    if len(R) < 12: return None
    A = np.array([[r[4], r[5]] for r in R]); yv = np.array([r[3] for r in R]); co, res, rk, sv = np.linalg.lstsq(A, yv, rcond=None)
    e = yv - A @ co; s2 = float(e @ e) / (len(R) - 2); cov = s2 * np.linalg.inv(A.T @ A)
    return float(co[0]), float(co[1]), float(np.sqrt(cov[0, 0])), float(np.sqrt(cov[1, 1])), len(R), float(np.sqrt(s2))
def ff(r): return f'b {r[0]:+.2f} per 100 units of flux (plain error {r[2]:.2f}); c {r[1]:+.3f} a year ({r[3]:.3f}); {r[4]} months; scatter {r[5]:.2f}' if r else 'fewer than 12 months'
def shuffled(R, rng):
    """the years of each instrument's record dealt out afresh among themselves (each year's months kept together): what b comes out when the Sun's record is paired with the wrong years"""
    out = []; ins_set = sorted({r[0] for r in R}, key=str)
    for ins in ins_set:
        S = [r for r in R if r[0] == ins]; ys = sorted({r[1] for r in S}); perm = dict(zip(ys, rng.permutation(ys)))
        lev = {(r[1], r[2]): r[3] for r in S}
        for r in S:
            v = lev.get((perm[r[1]], r[2]))
            if v is not None: out.append((r[0], r[1], r[2], v, r[4], r[5]))
    return out
def report(N, label):
    print(f'\n== {label} ==')
    M = months(N); R = rows(M); byst = lambda sts: [r for r in R if r[0][0] in sts]
    yrs = sorted({r[1] for r in R}); print(f'months fitted: {len(R)}, of years {yrs[0] if yrs else "-"} to {yrs[-1] if yrs else "-"}; instruments: {len({r[0] for r in R})}')
    rd = fit(byst(DARK)); rt = fit(byst(TOWNS)); rb = fit(byst(BETW))
    print('Q1 and Q2. the five dark places together: ' + ff(rd))
    n_neg = n_have = 0
    for st in DARK:
        S = byst([st]); r = fit(S) if len(S) >= 24 else None
        if r: n_have += 1; n_neg += r[0] < 0
        print(f'      {NAMES.get(st, st):<20}' + (ff(r) if r else f'fewer than 24 months ({len(S)})') + f"; years {sorted({x[1] for x in S})[0] if S else '-'} to {sorted({x[1] for x in S})[-1] if S else '-'}; instruments {len({x[0] for x in S})}")
    print(f'Q3. places with 24 months or more: {n_have}; of them with b below nothing: {n_neg}')
    print('Q4. the five towns together: ' + ff(rt)); print('      the six places between, for the record: ' + ff(rb))
    if rd:
        rng = np.random.default_rng(20261127); S = byst(DARK); bs = np.array([fit(shuffled(S, rng))[0] for _ in range(400) ])
        print(f'Q5. the years dealt out afresh 400 times: b comes out as low as the real one in {100 * np.mean(bs <= rd[0]):.1f} draws of 100 (middle {np.median(bs):+.2f}, 5th to 95th in 100: {np.percentile(bs, 5):+.2f} to {np.percentile(bs, 95):+.2f})')
        for st in DARK:
            S2 = [r for r in S if r[0][0] != st]; r2 = fit(S2); print(f'      without {NAMES.get(st, st):<18}' + ff(r2))
    print('Q6. quiet years against active years, the same calendar months, level in 2018 to 2020 less level in 2023 and 2024:')
    alld = []
    for st in ('stars62', 'stars35', 'stars289', 'stars426', 'stars477'):
        q = {}; a = {}
        for (ins, y, m), v in M.items():
            if ins[0] != st: continue
            if y in (2018, 2019, 2020): q.setdefault(m, []).append(v)
            if y in (2023, 2024): a.setdefault(m, []).append(v)
        d = [np.mean(q[m]) - np.mean(a[m]) for m in q if m in a]
        print(f'      {NAMES.get(st, st):<20}' + (f'{np.mean(d):+.2f} over {len(d)} calendar months' if d else 'no month in both'))
        if d: alld.append(float(np.mean(d)))
    print(f'      averaged over the {len(alld)} places that have months in both: ' + (f'{np.mean(alld):+.2f}' if alld else '-'))
    print('for the record: the yearly middle of the monthly levels, place by place (months in brackets), and the Sun')
    for st in DARK + ['stars24', 'stars9']:
        print(f'   {NAMES.get(st, st):<20}' + ' '.join(f"{y}:{np.median([v for (ins, yy, m), v in M.items() if ins[0] == st and yy == y]):.2f}({sum(1 for (ins, yy, m), v in M.items() if ins[0] == st and yy == y)})" for y in sorted({k[1] for k in M if k[0][0] == st})))
    print('   the Sun, yearly mean flux: ' + ' '.join(f"{y}:{np.mean([SUN[f'{y}-{m:02d}'] for m in range(1, 13) if f'{y}-{m:02d}' in SUN]):.0f}" for y in range(2016, 2027)))
    ch = {}
    for (ins, y, m) in M: ch.setdefault(ins[0], set()).add(ins[1])
    print('   stations whose photometer changed (more than one address): ' + (', '.join(f'{NAMES.get(s, s)} ({len(v)})' for s, v in ch.items() if len(v) > 1) or 'none'))
NAMES = {'stars33': "Madrid ring road", 'stars76': "Valencia", 'stars1': "Coslada", 'stars52': "Almería", 'stars7': "Pamplona", 'stars36': "Northampton, USA", 'stars4': "La Palma, a town", 'stars19': "Tucson, USA",
         'stars9': "Añora", 'stars225': "Morata de Jalón", 'stars24': "Temisas", 'stars426': "Teide Observatory", 'stars62': "Àger", 'stars35': "Otlica", 'stars477': "Arkaroola", 'stars289': "Nerpio"}
if sys.argv[1] == 'madeup':
    # made-up monthly levels on a likely frame: the months January to June of each year a place has on the share (the months
    # in which the northern sky overhead is far from the Milky Way), for the five dark places; scatter 0.08 a month and 0.04 a year
    span = {'stars289': (2019, 2026), 'stars62': (2017, 2025), 'stars477': (2021, 2026), 'stars35': (2018, 2026), 'stars426': (2020, 2026)}
    rng = np.random.default_rng(7)
    for kind, bb, cc in (('nothing', 0.0, 0.0), ('ageing only, 0.05 a year', 0.0, 0.05), ('the Sun only, -0.25 per 100', -0.25, 0.0), ('both', -0.25, 0.05), ('both, small Sun -0.10', -0.10, 0.05)):
        res = []
        for _ in range(200):
            M = {}
            for st, (y0, y1) in span.items():
                for y in range(y0, y1 + 1):
                    ye = rng.normal(0, 0.04)
                    for m in ((1, 2, 3, 4, 5, 6) if st != 'stars477' else (7, 8, 9, 10, 11, 12)):
                        if f'{y}-{m:02d}' not in SUN or rng.random() < 0.3: continue
                        M[((st, 'x'), y, m)] = 21.5 + bb * SUN[f'{y}-{m:02d}'] / 100 + cc * (y - 2020) + ye + rng.normal(0, 0.08)
            r = fit(rows(M)); res.append((r[0], r[1], r[2], r[3]))
        res = np.array(res)
        print(f'{kind:<30} b: middle {np.median(res[:, 0]):+.2f}, 5th to 95th {np.percentile(res[:, 0], 5):+.2f} to {np.percentile(res[:, 0], 95):+.2f} (plain error says {np.median(res[:, 2]):.2f}); c: middle {np.median(res[:, 1]):+.3f}, {np.percentile(res[:, 1], 5):+.3f} to {np.percentile(res[:, 1], 95):+.3f}; b in -0.05 to -0.60 on {100 * np.mean((res[:, 0] <= -0.05) & (res[:, 0] >= -0.60)):.0f} draws in 100; c in +0.005 to +0.10 on {100 * np.mean((res[:, 1] >= 0.005) & (res[:, 1] <= 0.10)):.0f}')
else:
    years = [int(y) for y in sys.argv[1].split(',')]; N = []
    for y in years:
        try: N += pickle.load(open(f'/home/agent1/night/cache2/nights{y}.pkl', 'rb'))
        except FileNotFoundError: print(f'{y}: no file of nights')
    print(f"years {sys.argv[1]}: {len(N)} cleaned nights, {sum(1 for c in N if c.get('lev40') is not None)} of them with an hour or more far from the Milky Way")
    report(N, 'the level far from the Milky Way (lev40)')
    for c in N: c['alt'] = c['levdark']
    M2 = months(N, 'alt'); R2 = rows(M2); print('\nfor the record, the same fit with each night\'s darkest tenth for its level: the five dark places ' + ff(fit([r for r in R2 if r[0][0] in DARK])) + '; the five towns ' + ff(fit([r for r in R2 if r[0][0] in TOWNS])))
