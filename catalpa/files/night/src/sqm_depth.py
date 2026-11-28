# The eleventh sheet scored: the other make of meter (SQM) by the depth of the Sun, with the measure of the ninth sheet
# as the eleventh sheet words it for these files:
#   the reading (the file's own magnitude, column nsb; 0 is the file's mark for "saturated" and is left out) when the Sun
#   passes a depth, by straight-line interpolation in the Sun's altitude between two readings up to 11 minutes apart;
#   evenings and mornings apart; the middle of each over a month (five or more of each), the two averaged; a month's
#   figure less the mean of the same month of 2021 and 2024, whichever the station has; P the mean of June, July and
#   August 2022 (two of the three or more). From 8 degrees down only twilights with the Moon below the horizon.
#   A station gives a depth only if its ordinary reading there (the middle of its comparison-year months) is 2.0
#   magnitudes or more brighter than its own moonless night (the middle of its readings with the Sun 18 degrees down
#   or more and the Moon down) and 0.3 or more fainter than the brightest reading its files hold.
import os, glob, csv, pickle, importlib.util, datetime as dt
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('twilight', B + 'src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
ST = {'PAOF': ('Ouro Fino, Brazil', -22.35, -46.2), 'Nrnr': ('NamibRand, Namibia', -24.94899, 16.03956), 'AHO': ('Buenos Aires, Argentina', -34.58868, -58.41320), 'Oam': ('Oamaru, New Zealand', -45.077068, 170.980597)}
DEPTHS = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]; GAP = 660.0
def moon_up(ts, lat, lon): return TW.sky.moon_alt(TW.T2000 + dt.timedelta(seconds=float(ts)), lat, lon) > 0
def load(code, y, m):
    fn = B + f'data/sqm/{code}_{y}-{m:02d}.csv'
    if not os.path.exists(fn): return None
    T, M = [], []
    for row in csv.DictReader(open(fn, encoding='utf-8')):
        try: v = float(row['nsb']); t = dt.datetime.strptime(row['received_utc'][:19], '%Y-%m-%d %H:%M:%S')
        except (ValueError, KeyError): continue
        if v > 0: T.append((t - TW.T2000).total_seconds()); M.append(v)
    if len(T) < 50: return None
    o = np.argsort(T); return np.array(T)[o], np.array(M)[o]
def reduce(code, y, m):
    d = load(code, y, m)
    if d is None: return None
    T, M = d; name, lat, lon = ST[code]; alt = TW.sun_alt_vec(T, lat, lon); ok = (np.diff(T) <= GAP) & (np.diff(T) > 0); out = dict(d={}, bright=float(M.min()), n=len(T))
    for dp in DEPTHS:
        a0 = alt[:-1] + dp; a1 = alt[1:] + dp; ev, mo = [], []
        for k in np.where(ok & (a0 * a1 < 0))[0]:
            fr = a0[k] / (a0[k] - a1[k]); val = float(M[k] + fr * (M[k + 1] - M[k])); tc = T[k] + fr * (T[k + 1] - T[k])
            if dp >= 8.0 and moon_up(tc, lat, lon): continue
            (ev if alt[k + 1] < alt[k] else mo).append(val)
        out['d'][dp] = (ev, mo)
    deep = np.where(alt < -18.0)[0]; night = []
    for k in deep[::max(1, len(deep) // 400)]:
        if not moon_up(T[k], lat, lon): night.append(M[k])
    out['night'] = night; return out
def fig(r, dp, which=None):
    if r is None: return None
    ev, mo = r['d'][dp]
    if which == 'ev': return float(np.median(ev)) if len(ev) >= 5 else None
    if which == 'mo': return float(np.median(mo)) if len(mo) >= 5 else None
    return 0.5 * (float(np.median(ev)) + float(np.median(mo))) if len(ev) >= 5 and len(mo) >= 5 else None
if __name__ == '__main__':
    R = {(c, y, m): reduce(c, y, m) for c in ST for y in (2021, 2022, 2024) for m in (6, 7, 8)}
    pickle.dump(R, open(B + 'cache2/sqm_depth.pkl', 'wb'))
    print('the four stations: the months that give readings (rows), and each station\'s moonless night and brightest reading')
    P = {}; info = {}
    for c, (name, lat, lon) in ST.items():
        have = {k[1:]: R[k]['n'] for k in R if k[0] == c and R[k] is not None}; night = [v for k in R if k[0] == c and R[k] for v in R[k]['night']]; bright = min(R[k]['bright'] for k in R if k[0] == c and R[k])
        nl = float(np.median(night)) if night else None; info[c] = (nl, bright)
        print(f"   {name:<26} {lat:+6.1f}: " + ', '.join(f'{y}-{m:02d} ({n})' for (y, m), n in sorted(have.items())) + f'; night {nl if nl is None else round(nl, 2)}; brightest {bright:.2f}')
    print('\nP: June to August 2022 less the same months of 2021 and 2024 (magnitudes; negative: a brighter twilight; . no figure), by the depth of the Sun')
    print('   ' + ' ' * 26 + ''.join(f'{d:7g}°' for d in DEPTHS) + '    months of 2022 used; comparison years')
    for c, (name, lat, lon) in ST.items():
        row = []; used = set(); fl = set()
        for dp in DEPTHS:
            flank = [fig(R[(c, y, m)], dp) for y in (2021, 2024) for m in (6, 7, 8)]; flank = [v for v in flank if v is not None]; nl, bright = info[c]
            okd = bool(flank) and (nl is None or np.median(flank) <= nl - 2.0) and np.median(flank) >= bright + 0.3; an = []
            for m in (6, 7, 8):
                v = fig(R[(c, 2022, m)], dp); base = [(y, fig(R[(c, y, m)], dp)) for y in (2021, 2024)]; base = [(y, b) for y, b in base if b is not None]
                if okd and v is not None and base: an.append(v - float(np.mean([b for y, b in base]))); used.add(m); fl.update(y for y, b in base)
            p = float(np.mean(an)) if len(an) >= 2 else None; P[(c, dp)] = p; row.append(f'{p:+8.2f}' if p is not None else '       .')
        print(f'   {name:<26}' + ''.join(row) + f'    {sorted(used)}; {sorted(fl)}')
    mid = {dp: [P[(c, dp)] for c in ST if P[(c, dp)] is not None] for dp in DEPTHS}
    print('   ' + f"{'the middle':<26}" + ''.join(f'{np.median(mid[dp]):+8.2f}' if mid[dp] else '       .' for dp in DEPTHS)); print('   ' + f"{'stations':<26}" + ''.join(f'{len(mid[dp]):8d}' for dp in DEPTHS))
    print('   ' + f"{'the TESS-W meters (ninth)':<26}" + ''.join(f'{v:+8.2f}' for v in (-0.03, -0.16, -0.21, -0.30, -0.45, -0.65, -0.80)))
    print('   the ordinary reading at each depth, each station (the middle of its comparison months): ' + '; '.join(f"{ST[c][0].split(',')[0]} " + ' '.join(f"{np.median([v for v in (fig(R[(c, y, m)], dp) for y in (2021, 2024) for m in (6, 7, 8)) if v is not None]):.1f}" if any(fig(R[(c, y, m)], dp) is not None for y in (2021, 2024) for m in (6, 7, 8)) else '.' for dp in DEPTHS) for c in ST))
    g = lambda dp: float(np.median(mid[dp])) if mid[dp] else None
    def verdict(dp, test): return 'void (no station)' if g(dp) is None else ('held' if test(g(dp)) else 'failed')
    f = lambda v: 'none' if v is None else f'{v:+.3f}'
    print('\nThe lines of the eleventh sheet (unrounded figures; marks included)')
    print(f"S1. at 8 degrees the middle between -0.30 and +0.05: {f(g(8.0))}: {verdict(8.0, lambda v: -0.30 <= v <= 0.05)}")
    print(f"S2. at 8 degrees the middle above -0.33: {f(g(8.0))}: {verdict(8.0, lambda v: v > -0.33)}")
    print(f"S3. at 4 degrees the middle at 0.00 or above: {f(g(4.0))}: {verdict(4.0, lambda v: v >= 0.0)}")
    s4 = [v for v in (g(3.0), g(4.0)) if v is not None]; print(f"S4. a dimming: the middle at 3 or at 4 degrees at +0.05 or above: {f(g(3.0))}, {f(g(4.0))}: {'void (no station)' if not s4 else ('held' if max(s4) >= 0.05 else 'failed')}")
    print(f"S5. at 6 degrees the middle within 0.12 of nothing: {f(g(6.0))}: {verdict(6.0, lambda v: abs(v) <= 0.12)}")
    print(f"S6. at 7 degrees the middle less negative than -0.30: {f(g(7.0))}: {verdict(7.0, lambda v: v > -0.30)}")
    print('\nfor the record: evening alone and morning alone (the same rules), each station')
    for w in ('ev', 'mo'):
        for c, (name, lat, lon) in ST.items():
            row = []
            for dp in DEPTHS:
                an = []
                for m in (6, 7, 8):
                    v = fig(R[(c, 2022, m)], dp, w); base = [b for b in (fig(R[(c, y, m)], dp, w) for y in (2021, 2024)) if b is not None]
                    if v is not None and base and P[(c, dp)] is not None: an.append(v - float(np.mean(base)))
                row.append(f'{np.mean(an):+8.2f}' if len(an) >= 2 else '       .')
            print(f"   {'evening' if w == 'ev' else 'morning'} {name:<22}" + ''.join(row))
