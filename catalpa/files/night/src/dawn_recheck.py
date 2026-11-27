# After the independent check (check/check-dawn.md): my own recomputation of its points. Not sealed.
#  A. Ties: how long the smoothed curve sits at its maximum, and what first, last and middle tied minute give;
#     two measures with no ties (a running mean; the darkest tenth of the night by mean reading); and the sealed
#     method on made-up nights rounded to 0.01 as the real readings are.
#  B. Nights that are not the sky (a reading more than 1 magnitude from the station's own level), and each
#     station's magnitude column against the formula in its own header.
#  C. The infrared sky temperature as a second test of "clear".
#  D. The towns: by the clock, or three quarters through the night?
#  E. Before dawn against after dusk, station by station.
#  F. The middle night (median, not mean), hours before dawn.
#  G. The Milky Way: how far the zenith is from its plane at the darkest moment.
#  H. The eight lines under each choice.
# Run: ~/ipd/.venv/bin/python -I src/dawn_recheck.py > dawn_recheck.out
import sys, io, contextlib, importlib.util, glob, re, math, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('dawn', '/home/agent1/night/src/dawn.py'); D = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(D)
sky = D.sky; t0 = dt.datetime(2024, 1, 1)
def read_full(st):
    T, M, TE, TS, FQ, ZP, lat, lon, place, zph = [], [], [], [], [], [], None, None, '', None
    for fn in sorted(glob.glob(D.IDA + st + '_2024-??.dat')):
        txt = open(fn, encoding='utf-8', errors='replace').read()
        if '# END OF HEADER' not in txt: continue
        head, body = txt.split('# END OF HEADER', 1)
        m = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head)
        if m: lat, lon = float(m.group(1)), float(m.group(2))
        m = re.search(r'# Location name: (.*)', head)
        if m: place = m.group(1).split('/')[0].strip()
        m = re.search(r'# TESS zero point: ([-\d.]+)', head)
        if m: zph = float(m.group(1))
        for line in body.splitlines():
            p = line.split(';')
            if len(p) < 7: continue
            try: v = float(p[5]); te = float(p[2]); ts = float(p[3]); fq = float(p[4]); zp = float(p[6]); t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
            except ValueError: continue
            T.append((t - t0).total_seconds()); M.append(v); TE.append(te); TS.append(ts); FQ.append(fq); ZP.append(zp)
    o = np.argsort(T); g = lambda x: np.array(x)[o]
    return g(T), g(M), g(TE), g(TS), g(FQ), g(ZP), lat, lon, place, zph
N = []; noon = {}; formula = {}
for st in D.STATIONS:
    tsec, M, TE, TS, FQ, ZP, lat, lon, place, zph = read_full(st)
    ok = (M > 0) & (FQ > 0)
    # the magnitude column against the header's formula, month by month
    dev = M[ok] - (ZP[ok] - 2.5 * np.log10(FQ[ok])); mon = (np.array([t0 + dt.timedelta(seconds=float(x)) for x in tsec[ok][::200]]))
    formula[st] = (float(np.median(dev[: len(dev) // 6])), float(np.median(dev[-len(dev) // 6:])), zph, float(np.median(ZP[ok])))
    cand = []
    for d, dusk, dawn, moon in D.nights(lat, lon):
        if moon >= 0: continue
        a = (dusk - t0).total_seconds(); b = (dawn - t0).total_seconds(); i0, i1 = np.searchsorted(tsec, a), np.searchsorted(tsec, b)
        sel = slice(i0, i1); good = M[sel] > 0
        if good.sum() < 10: continue
        mins = np.floor((tsec[sel][good] - a) / 60).astype(int); nmin = int((b - a) // 60); um = np.unique(mins)
        if len(um) < 0.9 * nmin: continue
        med = lambda x: np.array([np.median(x[sel][good][mins == k]) for k in um])
        fq = FQ[sel][good]; pos = fq > 0; off = float(np.median(M[sel][good][pos] - (ZP[sel][good][pos] - 2.5 * np.log10(fq[pos])))) if pos.sum() > 10 else 0.0
        m = med(M); cand.append(dict(st=st, place=place, d=d, L=(b - a) / 3600, t=(um + 0.5) / 60, m=m, ts=med(TS), te=med(TE), s=D.spread(m), dusk=dusk, dawn=dawn, lon=lon, lat=lat, off=off))
    if not cand: continue
    floor = float(np.percentile([c['s'] for c in cand], 20))
    for c in cand: c['floor'] = floor; c['clear'] = c['s'] <= 2 * floor; c['sm'] = D.runmed(c['m'], 31); N.append(c)
clear = [c for c in N if c['clear']]
print(f"moonless covered nights {len(N)}; clear by the sealed rule {len(clear)}")
# ---------------- A
def ties(c):
    mx = c['sm'].max(); idx = np.where(np.isclose(c['sm'], mx, atol=1e-9))[0]; return idx
def f_of(c, how):
    idx = ties(c)
    if how == 'first': return c['t'][idx[0]] / c['L']
    if how == 'last': return c['t'][idx[-1]] / c['L']
    if how == 'middle': return 0.5 * (c['t'][idx[0]] + c['t'][idx[-1]]) / c['L']
    if how == 'mean':
        k = np.convolve(c['m'], np.ones(31) / 31, 'valid'); return c['t'][15 + int(np.argmax(k))] / c['L']
def tenth(c):
    b = np.minimum((c['t'] / c['L'] * 10).astype(int), 9); mt = np.array([c['m'][b == k].mean() if np.any(b == k) else -np.inf for k in range(10)]); return int(np.argmax(mt)), mt
print("\nA. TIES")
pl = [len(ties(c)) for c in clear]; span = [(c['t'][ties(c)[-1]] - c['t'][ties(c)[0]]) / c['L'] for c in clear]
print(f"   minutes at which the 31-minute running median equals its maximum: middle {np.median(pl):.0f} (quarter marks {np.percentile(pl, 25):.0f} to {np.percentile(pl, 75):.0f}); nights with one such minute: {sum(1 for x in pl if x == 1)}; first and last tied minute more than a tenth of the night apart on {sum(1 for x in span if x > 0.1)} nights, more than a quarter on {sum(1 for x in span if x > 0.25)}")
def shares(sel, how):
    f = np.array([f_of(c, how) for c in sel]); return 100 * np.mean(f >= 0.9), 100 * np.mean(f > 0.5), float(np.median(f))
for how in ('first', 'last', 'middle', 'mean'):
    a, b, m = shares(clear, how); mxst = max((np.mean([f_of(c, how) >= 0.9 for c in clear if c['st'] == st]), st) for st in D.STATIONS if sum(1 for c in clear if c['st'] == st) >= 5)
    print(f"   darkest moment by the {how:<6} {'tied minute' if how != 'mean' else 'running mean (no ties)':<22}: last tenth {a:4.1f} in 100; second half {b:4.1f} in 100; middle f {m:.2f}; largest share in the last tenth at any station {100 * mxst[0]:.0f} in 100 ({mxst[1]})")
tt = [tenth(c)[0] for c in clear]
print(f"   the darkest tenth of the night by mean reading: the last on {100 * np.mean(np.array(tt) == 9):.1f} in 100 nights, the ninth {100 * np.mean(np.array(tt) == 8):.1f}, the eighth {100 * np.mean(np.array(tt) == 7):.1f}; one of the first five {100 * np.mean(np.array(tt) < 5):.1f}; by tenth: " + ", ".join(str(int(np.sum(np.array(tt) == k))) for k in range(10)))
near = [tenth(c)[1].max() - tenth(c)[1][9] <= 0.02 for c in clear]; print(f"   the last tenth within 0.02 magnitude of the darkest tenth on {100 * np.mean(near):.0f} in 100 nights")
rng = np.random.default_rng(1650); tg = np.arange(0.5 / 60, 8, 1 / 60)
def made(shape, rnd, n=400):
    out = {h: [] for h in ('first', 'last', 'middle', 'mean')}; tn = []
    for _ in range(n):
        m = shape(tg) + rng.normal(0, 0.02, len(tg))
        if rnd: m = np.round(m, 2)
        c = dict(t=tg, m=m, L=8.0, sm=D.runmed(m, 31))
        for h in out: out[h].append(f_of(c, h))
        tn.append(tenth(c)[0])
    return {h: (100 * np.mean(np.array(v) >= 0.9), float(np.median(v))) for h, v in out.items()}, 100 * np.mean(np.array(tn) == 9)
for name, shape in (("flat", lambda t: 21.0 + 0 * t), ("darkening 0.05 an hour", lambda t: 18.0 + 0.05 * t), ("darkening ever more slowly to its last minute", lambda t: 18.0 + 0.5 * (1 - np.exp(-t / 1.5)))):
    for rnd in (False, True):
        r, tn = made(shape, rnd)
        print(f"   made-up, {name}, {'rounded to 0.01' if rnd else 'not rounded'}: last tenth by first tie {r['first'][0]:.0f} in 100 (middle f {r['first'][1]:.2f}); last tie {r['last'][0]:.0f}; middle tie {r['middle'][0]:.0f}; running mean {r['mean'][0]:.0f}; darkest tenth is the last {tn:.0f}")
# ---------------- B
print("\nB. NIGHTS THAT ARE NOT THE SKY, AND THE MAGNITUDE COLUMN")
lev0 = {st: float(np.median([np.median(c['m']) for c in clear if c['st'] == st])) for st in D.STATIONS if any(c['st'] == st for c in clear)}
for c in N: c['sky'] = abs(np.median(c['m']) - lev0[c['st']]) <= 1.0
bad = [c for c in clear if not c['sky']]
print(f"   clear nights whose middle reading is more than 1 magnitude from the station's level: {len(bad)} of {len(clear)}")
for st in D.STATIONS:
    b = [c for c in bad if c['st'] == st]
    if b: print(f"      {st} ({b[0]['place']}): {len(b)} of {sum(1 for c in clear if c['st'] == st)}; dates {b[0]['d']} to {b[-1]['d']}; middle reading {np.median([np.median(c['m']) for c in b]):.2f} against a level of {lev0[st]:.2f}; enclosure {np.median([np.median(c['te']) for c in b]):.0f} C, enclosure less sky {np.median([np.median(c['te'] - c['ts']) for c in b]):.0f} C (on the station's other clear nights {np.median([np.median(c['te'] - c['ts']) for c in clear if c['st'] == st and c['sky']]):.0f} C)")
print("   magnitude column less (zero point column - 2.5 log10 frequency): first sixth of the year, last sixth; header zero point; column zero point")
for st in D.STATIONS:
    a, b, zph, zpc = formula[st]
    if abs(a) > 0.02 or abs(b) > 0.02 or (zph is not None and abs(zph - zpc) > 0.02): print(f"      {st}: {a:+.2f}, {b:+.2f}; header {zph}; column {zpc:.2f}")
good = [c for c in clear if c['sky']]
lev = {st: float(np.median([np.median(c['m']) for c in good if c['st'] == st])) for st in lev0}
cls0 = lambda st: 'lit' if lev0[st] < 19.5 else ('dark' if lev0[st] >= 21.0 else 'between'); cls1 = lambda st: 'lit' if lev[st] < 19.5 else ('dark' if lev[st] >= 21.0 else 'between')
print("   levels with those nights out (and the class, where it changes): " + "; ".join(f"{st} {lev[st]:.2f}" + (f" ({cls0(st)} -> {cls1(st)})" if cls0(st) != cls1(st) else "") for st in sorted(lev, key=lambda s: lev[s])))
# ---------------- C
print("\nC. THE INFRARED SKY TEMPERATURE AS A SECOND TEST OF CLEAR (criteria after the reader's: sky temperature within 1.5 C of its own hour-long running median for 95 in 100 of the night, and enclosure less sky at least half the station's best tenth)")
best = {}
for st in lev0:
    v = [np.median(c['te'] - c['ts']) for c in N if c['st'] == st]; best[st] = float(np.percentile(v, 90)) if v else 0.0
def ir(c):
    if np.all(c['ts'] == 0) or best[c['st']] <= 1: return None
    r = np.abs(c['ts'] - D.runmed(c['ts'], 61)); return bool(np.percentile(r, 95) <= 1.5 and np.median(c['te'] - c['ts']) >= 0.5 * best[c['st']])
for c in N: c['ir'] = ir(c)
print("   stations with no usable temperatures: " + ", ".join(st for st in lev0 if all(c['ir'] is None for c in N if c['st'] == st)))
t1 = [c for c in clear if c['ir'] is not None]; print(f"   of {len(t1)} rule-clear nights that can be tested, {sum(1 for c in t1 if not c['ir'])} fail the infrared test; of {sum(1 for c in N if not c['clear'] and c['ir'] is not None)} rejected nights, {sum(1 for c in N if not c['clear'] and c['ir'])} pass it")
clean = [c for c in clear if c['sky'] and c['ir'] is not False]
print(f"   the cleaned set (rule-clear, the sky, and not failing the infrared test): {len(clean)} nights")
for tag, sel in (("sealed set", clear), ("cleaned set", clean), ("infrared-clear whatever the rule says", [c for c in N if c['ir'] and c['sky']])):
    print(f"   {tag} ({len(sel)} nights): last tenth by first / last / middle tie / running mean: " + " / ".join(f"{shares(sel, h)[0]:.0f}" for h in ('first', 'last', 'middle', 'mean')) + " in 100; second half: " + " / ".join(f"{shares(sel, h)[1]:.0f}" for h in ('first', 'last', 'middle', 'mean')) + f"; darkest tenth is the last on {100 * np.mean([tenth(c)[0] == 9 for c in sel]):.0f}, in the second half on {100 * np.mean([tenth(c)[0] >= 5 for c in sel]):.0f}")
# ---------------- D
print("\nD. THE FIVE SPANISH TOWNS: by the clock, or a fixed share of the night? (cleaned set; middle tie)")
towns = ('stars1', 'stars7', 'stars52', 'stars76', 'stars33')
def clock(u): off = 2 if dt.datetime(2024, 3, 31, 1) <= u < dt.datetime(2024, 10, 27, 1) else 1; x = u + dt.timedelta(hours=off); h = x.hour + x.minute / 60 + x.second / 3600; return h if h < 12 else h - 24
hm = lambda x: f"{int(x):02d}:{int((x - int(x)) * 60):02d}"
for tag, months in (("November to February", (11, 12, 1, 2)), ("March, April, September, October", (3, 4, 9, 10)), ("May to August", (5, 6, 7, 8))):
    v = [c for c in clean if c['st'] in towns and c['d'].month in months]
    if not v: continue
    for how in ('first', 'middle', 'last'):
        ck = [clock(c['dusk'] + dt.timedelta(hours=f_of(c, how) * c['L'])) for c in v]
        if how == 'first': head = f"   {tag:<34} {len(v):3d} nights; dawn begins {hm(np.median([clock(c['dawn']) for c in v]))}; three quarters through the night falls at {hm(np.median([clock(c['dusk'] + dt.timedelta(hours=0.75 * c['L'])) for c in v]))};"
        else: head = " " * 6
        print(f"{head} darkest by {how} tie {hm(np.median(ck))} (middle f {np.median([f_of(c, how) for c in v]):.2f})")
v = [c for c in clean if c['st'] in towns]; ck = np.array([clock(c['dusk'] + dt.timedelta(hours=f_of(c, 'middle') * c['L'])) for c in v]); hb = np.array([(1 - f_of(c, 'middle')) * c['L'] for c in v]); ff = np.array([f_of(c, 'middle') for c in v]); LL = np.array([c['L'] for c in v])
print(f"   spread (standard deviation) of the darkest moment over the {len(v)} nights: {np.std(ck):.2f} h by the clock; {np.std(hb):.2f} h counted back from dawn; {np.std(ff * np.mean(LL)):.2f} h as a share of the night (scaled to the mean night)")
# ---------------- E
print("\nE. BEFORE DAWN AGAINST AFTER DUSK: the last half hour of the night against the first (cleaned set)")
def dd(c): return np.median(c['m'][c['t'] >= c['L'] - 0.5]) - np.median(c['m'][c['t'] <= 0.5])
for st in sorted(lev, key=lambda s: lev[s]):
    v = [dd(c) for c in clean if c['st'] == st and np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)]
    if len(v) >= 5: print(f"   {st:<9} {cls1(st):<8} level {lev[st]:.2f}  {len(v):3d} nights: darker before dawn on {100 * np.mean(np.array(v) > 0):3.0f} in 100; middle difference {np.median(v):+.2f} mag")
for k in ('lit', 'between', 'dark', 'all'):
    v = np.array([dd(c) for c in clean if (k == 'all' or cls1(c['st']) == k) and np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)])
    print(f"   {k:<8} {len(v):3d} nights: darker before dawn on {100 * np.mean(v > 0):.0f} in 100; middle difference {np.median(v):+.2f} mag: the evening {100 * (10 ** (0.4 * np.median(v)) - 1):.0f} in 100 brighter, which is the hour before dawn {100 * (1 - 10 ** (-0.4 * np.median(v))):.0f} in 100 darker")
# ---------------- F
print("\nF. THE MIDDLE NIGHT: brighter than its own darkest moment, hundredths of a magnitude, by half hours before dawn (3.25 ... 0.25); median over nights of 7 hours or more (cleaned set), and the mean beside it")
for k in ('lit', 'between', 'dark'):
    v = [c for c in clean if cls1(c['st']) == k and c['L'] >= 7]; md = []; mn = []
    for h in np.arange(3.25, 0, -0.5):
        x = [c['sm'].max() - np.interp(c['L'] - h, c['t'], c['sm']) for c in v]; md.append(np.median(x)); mn.append(np.mean(x))
    print(f"   {k:<8} {len(v):3d} nights: median " + " ".join(f"{100 * x:3.0f}" for x in md) + "   mean " + " ".join(f"{100 * x:3.0f}" for x in mn))
# ---------------- G
print("\nG. THE MILKY WAY: at the darkest moment (middle tie), the share of the night's minutes at which the zenith is nearer the plane of the Milky Way (50 in 100 if unrelated)")
def gal_b(tu, lat, lon):
    lst = (sky.gmst_deg(sky.jd(tu)) + lon) % 360; a = math.radians(lst); d = math.radians(lat); an, dn = math.radians(192.85948), math.radians(27.12825)
    return abs(math.degrees(math.asin(math.sin(d) * math.sin(dn) + math.cos(d) * math.cos(dn) * math.cos(a - an))))
for st in sorted(lev, key=lambda s: -lev[s])[:6]:
    v = [c for c in clean if c['st'] == st]; pct = []
    for c in v:
        b = np.array([gal_b(c['dusk'] + dt.timedelta(hours=float(x)), c['lat'], c['lon']) for x in c['t'][::5]]); bm = gal_b(c['dusk'] + dt.timedelta(hours=float(f_of(c, 'middle') * c['L'])), c['lat'], c['lon']); pct.append(100 * np.mean(b < bm))
    if v: print(f"   {st:<9} level {lev[st]:.2f}  {len(v):3d} nights: middle {np.median(pct):.0f} in 100")
# ---------------- H
print("\nH. THE EIGHT LINES UNDER EACH CHOICE (H held, F failed, - void); sets: sealed, cleaned; ties: first, middle, last")
def lines(sel, how, cl):
    F = np.array([f_of(c, how) for c in sel]); out = ['H' if np.mean(F >= 0.9) < 0.5 else 'F', 'H' if np.mean(F > 0.5) > 0.6 else 'F']
    S = {}
    for st in set(c['st'] for c in sel):
        v = [c for c in sel if c['st'] == st]
        if len(v) < 10: continue
        f = np.array([f_of(c, how) for c in v]); south = v[0]['lat'] < 0
        su = [f_of(c, how) >= 0.9 for c in v if (c['d'].month in (5, 6, 7, 8)) != south and c['d'].month in (5, 6, 7, 8, 11, 12, 1, 2)]; wi = [f_of(c, how) >= 0.9 for c in v if (c['d'].month in (11, 12, 1, 2)) != south and c['d'].month in (5, 6, 7, 8, 11, 12, 1, 2)]
        S[st] = dict(med=np.median(f), late=np.mean(f >= 0.9), slope=np.median([D.slope(c['t'], c['m']) for c in v]), su=su, wi=wi)
    lit = [S[s] for s in S if cl(s) == 'lit']; dark = [S[s] for s in S if cl(s) == 'dark']
    def frac(c, test, need): return '-' if not c else ('H' if sum(1 for s in c if test(s)) / len(c) >= need - 1e-9 else 'F')
    out += [frac(lit, lambda s: s['med'] >= 0.7, 2 / 3), frac(lit, lambda s: s['late'] > 0.25, 0.5), frac(dark, lambda s: 0.3 <= s['med'] <= 0.7, 2 / 3), frac(lit, lambda s: 0.02 <= s['slope'] <= 0.10, 2 / 3), frac(dark, lambda s: abs(s['slope']) <= 0.02, 2 / 3)]
    out.append('-' if not lit else ('H' if sum(1 for s in lit if s['su'] and s['wi'] and np.mean(s['su']) > np.mean(s['wi'])) > len(lit) / 2 else 'F'))
    return out, len(lit), len(dark)
allr = []
skyonly = [c for c in clear if c['sky']]
for tag, sel, cl in (("sealed set, sealed classes", clear, cls0), ("the sky only, classes from it", skyonly, cls1), ("cleaned set, classes from it", clean, cls1)):
    for how in ('first', 'middle', 'last'):
        o, nl, nd = lines(sel, how, cl); allr.append(o); print(f"   {tag:<30} {how:<6} tie: L1..L8 = {' '.join(o)}   (lit stations {nl}, dark {nd})")
print("   hold under all nine: " + ", ".join(f"L{i + 1}" for i in range(8) if all(r[i] == 'H' for r in allr)) + "; fail under all nine: " + (", ".join(f"L{i + 1}" for i in range(8) if all(r[i] == 'F' for r in allr)) or "none"))
# ---------------- after the checker's second report (check/check-dawn-2.md)
print("\nI. LEVELS BY THE FILES' OWN FORMULA (the magnitude column less its departure from zero point - 2.5 log10 frequency, night by night), cleaned set")
levc = {st: float(np.median([np.median(c['m']) - (c['off'] if abs(c['off']) > 0.1 else 0.0) for c in clean if c['st'] == st])) for st in lev if any(c['st'] == st for c in clean)}
cls2 = lambda st: 'lit' if levc[st] < 19.5 else ('dark' if levc[st] >= 21.0 else 'between')
for st in sorted(levc, key=lambda q: levc[q]):
    v = [c for c in clean if c['st'] == st]; nb = sum(1 for c in v if abs(c['off']) > 0.1)
    if nb: print(f"   {st}: level {lev[st]:.2f} as printed, {levc[st]:.2f} by the formula; {nb} of {len(v)} nights printed {np.median([c['off'] for c in v if abs(c['off']) > 0.1]):+.2f} from it")
print("   order from the brightest: " + ", ".join(f"{st} {levc[st]:.2f} ({cls2(st)})" for st in sorted(levc, key=lambda q: levc[q])))
print("\nJ. HOW MUCH THE SKY CHANGES IN A NIGHT: the darkest tenth less the brightest tenth, middle night, magnitudes (and the middle nightly trend an hour)")
def rng10(c): mt = tenth(c)[1]; mt = mt[np.isfinite(mt)]; return float(mt.max() - mt.min())
for st in sorted(levc, key=lambda q: levc[q]):
    v = [c for c in clean if c['st'] == st]
    print(f"   {st:<9} {cls2(st):<8} {len(v):3d} nights: {np.median([rng10(c) for c in v]):.2f} ({100 * (10 ** (0.4 * np.median([rng10(c) for c in v])) - 1):.0f} in 100 of light); trend {np.median([D.slope(c['t'], c['m']) for c in v]):+.3f}")
for k in ('lit', 'between', 'dark'):
    v = [c for c in clean if cls2(c['st']) == k]; print(f"   all {k}: {np.median([rng10(c) for c in v]):.2f} mag")
print("\nK. THE FIVE TOWNS THROUGH THE NIGHT, by season (cleaned set): each tenth of the night, brighter than that night's darkest tenth, hundredths of a magnitude, middle night")
towns = ('stars1', 'stars7', 'stars52', 'stars76', 'stars33')
for tag, months in (("November to February", (11, 12, 1, 2)), ("March, April, September, October", (3, 4, 9, 10)), ("May to August", (5, 6, 7, 8)), ("all year", tuple(range(1, 13)))):
    v = [c for c in clean if c['st'] in towns and c['d'].month in months]
    if not v: continue
    prof = np.median(np.array([tenth(c)[1].max() - tenth(c)[1] for c in v]), axis=0); tn = np.array([tenth(c)[0] for c in v]); nearl = np.array([tenth(c)[1].max() - tenth(c)[1][9] <= 0.02 for c in v])
    h1 = [D.slope(c['t'][c['t'] <= c['L'] / 2], c['m'][c['t'] <= c['L'] / 2]) for c in v]; h2 = [D.slope(c['t'][c['t'] > c['L'] / 2], c['m'][c['t'] > c['L'] / 2]) for c in v]
    print(f"   {tag:<34} {len(v):3d} nights: " + " ".join(f"{100 * x:3.0f}" for x in prof) + f"; the last tenth the darkest on {int(tn.sum() * 0 + np.sum(tn == 9))} ({100 * np.mean(tn == 9):.0f} in 100); the last tenth within 0.02 of the darkest on {100 * np.mean(nearl):.0f} in 100; darkening {np.median(h1):+.3f} mag an hour over the first half of the night and {np.median(h2):+.3f} over the second; night {np.median([c['L'] for c in v]):.1f} h")
print("\nL. BEFORE DAWN AGAINST AFTER DUSK, by the classes from the corrected levels (cleaned set)")
for k in ('lit', 'between', 'dark'):
    v = np.array([dd(c) for c in clean if cls2(c['st']) == k and np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)]); sts = sorted(set(c['st'] for c in clean if cls2(c['st']) == k), key=lambda q: levc[q])
    print(f"   {k:<8} {len(sts)} places, {len(v):3d} nights: darker before dawn on {100 * np.mean(v > 0):.0f} in 100; places: " + ", ".join(f"{st} {100 * np.mean([dd(c) > 0 for c in clean if c['st'] == st and np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)]):.0f}" for st in sts))
for st in towns:
    v = [dd(c) for c in clean if c['st'] == st and np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)]
    if v: print(f"   {st}: the evening brighter by {100 * (10 ** (0.4 * np.median(v)) - 1):.0f} in 100 in the middle night ({len(v)} nights)")
print("   the last tenth the darkest, place by place (cleaned set / sealed set): " + "; ".join(f"{st} {int(np.sum([tenth(c)[0] == 9 for c in clean if c['st'] == st]))} of {sum(1 for c in clean if c['st'] == st)} / {int(np.sum([tenth(c)[0] == 9 for c in clear if c['st'] == st]))} of {sum(1 for c in clear if c['st'] == st)}" for st in sorted(levc, key=lambda q: levc[q])))
print(f"   pooled, the darkest tenth is the last: cleaned {100 * np.mean([tenth(c)[0] == 9 for c in clean]):.1f}, sealed set {100 * np.mean([tenth(c)[0] == 9 for c in clear]):.1f}; in the second half: cleaned {100 * np.mean([tenth(c)[0] >= 5 for c in clean]):.1f}, sealed {100 * np.mean([tenth(c)[0] >= 5 for c in clear]):.1f}; second half at stars477 {100 * np.mean([tenth(c)[0] >= 5 for c in clean if c['st'] == 'stars477']):.0f}, stars289 {100 * np.mean([tenth(c)[0] >= 5 for c in clean if c['st'] == 'stars289']):.0f}")
# ---------------- the page's table and pictures (cleaned set; levels by the files' own formula)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'
NAME = {'stars33': "Madrid, by the ring road", 'stars76': "Valencia", 'stars1': "Coslada, beside Madrid", 'stars52': "Huércal de Almería", 'stars7': "Pamplona", 'stars36': "Northampton, Massachusetts", 'stars4': "Santa Cruz de La Palma", 'stars19': "Tucson, Arizona", 'stars9': "Añora, a village in Andalusia", 'stars225': "Morata de Jalón, a village in Aragon", 'stars24': "Temisas, Gran Canaria", 'stars426': "Teide Observatory, Tenerife", 'stars62': "Àger, Catalonia", 'stars35': "Otlica, Slovenia", 'stars477': "Arkaroola, South Australia", 'stars289': "Nerpio, in the mountains of Albacete"}
rows = ['<tr><th>place</th><th class="n">level</th><th class="n">nights</th><th class="n">the last tenth the darkest</th><th class="n">darkest tenth in the second half</th><th class="n">darker before dawn than after dusk</th></tr>']
tab = []
for st in sorted(levc, key=lambda q: levc[q]):
    v = [c for c in clean if c['st'] == st]; tn = np.array([tenth(c)[0] for c in v]); w = [dd(c) for c in v if np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)]
    tab.append((st, levc[st], len(v), int(np.sum(tn == 9)), int(np.sum(tn >= 5)), 100 * np.mean(np.array(w) > 0), int(np.sum(np.array(w) > 0)), len(w)))
    rows.append(f'<tr><td>{NAME[st]}</td><td class="n">{levc[st]:.1f}</td><td class="n">{len(v)}</td><td class="n">{tab[-1][3]}</td><td class="n">{tab[-1][4]}</td><td class="n">{tab[-1][6]} of {tab[-1][7]}</td></tr>')
open('/home/agent1/night/t_stations.html', 'w', encoding='utf-8').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
print("\nTHE PAGE'S TABLE (cleaned set): station, level by the formula, nights, last tenth darkest, second half, darker before dawn")
for r in tab: print(f"   {r[0]:<9} {r[1]:5.2f} {r[2]:4d} {r[3]:4d} {r[4]:4d}   {r[6]} of {r[7]} ({r[5]:.0f} in 100)")
tn = np.array([tenth(c)[0] for c in clean]); share = [100 * np.mean(tn == k) for k in range(10)]
print("picture 1 (cleaned set), nights in 100 on which each tenth of the night was the darkest: " + ", ".join(f"{x:.1f}" for x in share) + f"; last three tenths together {sum(share[7:]):.0f}; first half {sum(share[:5]):.0f}")
fig = plt.figure(figsize=(5.0, 3.7), facecolor=SURF); ax = fig.add_axes([0.115, 0.135, 0.865, 0.745]); ax.set_facecolor(SURF)
ax.bar(np.arange(10) + 0.5, share, width=0.86, color=BLUE, zorder=3)
ax.text(9.5, share[9] + 0.6, f'{share[9]:.0f}', fontsize=14, color=INK, ha='center', va='bottom', fontweight='bold')
ax.set_xlim(0, 10); ax.set_ylim(0, 24); ax.set_yticks([0, 5, 10, 15, 20]); ax.set_xticks([0, 5, 10]); ax.set_xticklabels(['end of dusk', 'middle of the night', 'start of dawn'], fontsize=13)
for lab, ha in zip(ax.get_xticklabels(), ('left', 'center', 'right')): lab.set_ha(ha)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0, labelsize=13)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.975, 'nights in 100 on which each tenth was the darkest', fontsize=12.5, color=INK2, va='top')
fig.savefig('/home/agent1/night/img/dawn-tenths.png', dpi=140, facecolor=SURF)
short = {'stars33': "Madrid ring road", 'stars76': "Valencia", 'stars1': "Coslada", 'stars52': "Almería", 'stars7': "Pamplona", 'stars36': "Northampton, USA", 'stars4': "La Palma, a town", 'stars19': "Tucson, USA", 'stars9': "Añora, a village", 'stars225': "Morata, a village", 'stars24': "Temisas, Canaries", 'stars426': "Teide Observatory", 'stars62': "Àger, Catalonia", 'stars35': "Otlica, Slovenia", 'stars477': "Arkaroola, Australia", 'stars289': "Nerpio, Spain"}
groups = [("five Spanish towns", [r for r in tab if cls2(r[0]) == 'lit']), ("seven places in between", [r for r in tab if cls2(r[0]) == 'between']), ("the four darkest skies", [r for r in tab if cls2(r[0]) == 'dark'])]
fig = plt.figure(figsize=(5.0, 7.3), facecolor=SURF); ax = fig.add_axes([0.50, 0.075, 0.47, 0.875]); ax.set_facecolor(SURF)
y = 0.0; ticks = []; labs = []
for gname, g in groups:
    fig_y = None; ax.text(34.0, -y, gname, fontsize=12, color=INK2, style='italic', ha='right', va='center', clip_on=False); y += 1.0
    for r in g:
        ax.plot([50, r[5]], [-y, -y], color=BLUE, lw=2.4, alpha=0.35, solid_capstyle='round', zorder=3); ax.plot([r[5]], [-y], 'o', ms=10, color=BLUE, mec=SURF, mew=1.4, zorder=4); ticks.append(-y); labs.append(short[r[0]]); y += 1.0
    y += 0.6
ax.axvline(50, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=2); ax.text(51.0, 0.75, 'a coin toss', fontsize=11.5, color=INK2, va='center', ha='left')
ax.set_yticks(ticks); ax.set_yticklabels(labs, fontsize=12.5, color=INK); ax.set_ylim(-y + 0.9, 1.2); ax.set_xlim(35, 104); ax.set_xticks([50, 75, 100]); ax.set_xticklabels(['50', '75', '100'], fontsize=13)
ax.grid(True, axis='x', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.99, 'nights in 100 darker before dawn than after dusk', fontsize=12.5, color=INK2, va='top')
fig.savefig('/home/agent1/night/img/dawn-places.png', dpi=140, facecolor=SURF)
