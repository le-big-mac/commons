# The lines of the sixth sheet (expectations-twilight.md): have these photometers themselves changed, by the twilight?
# Reads a file of monthly reductions made by twilight.py's reduce() ({(station, year, month): reduction}).
# Usage: twsheet.py FILE.pkl [six]      "six": use only January, March, May, July, September and November
# Run on cache2/twilight16.pkl six it prints the reference figures for the sixteen photometers of the dawn page.
import sys, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
DIM, STEADY = 0.04, 0.025
def chip(r): return (r.get('mac') or '')[-8:]          # the last three bytes: the chip's own number
def table(R, SIX):
    """one row for each station: its instrument's twilight drift (all, evening alone, morning alone) and night drift"""
    stations = sorted({k[0] for k in R}, key=lambda s: int(s.replace('stars', ''))); rows = {}
    for st in stations:
        chips = {}                                     # the instrument: the chip with the most months at this station
        for (s, y, m), r in R.items():
            if s == st and r is not None and (SIX is None or m in SIX) and TW.month_value(r): chips.setdefault(chip(r), []).append((y, m))
        if not chips: rows[st] = None; continue
        ch = max(chips, key=lambda c: len(chips[c])); V = {}; E = {}; Mo = {}; sl = []; nights = []
        for (s, y, m), r in R.items():
            if s != st or r is None or chip(r) != ch or (SIX is not None and m not in SIX): continue
            mv = TW.month_value(r)
            if mv: V[(y, m)] = mv[0]; E[(y, m)] = mv[1]; Mo[(y, m)] = mv[2]; sl += r['sl']
            nights += [(y, m) + tuple(n) for n in r.get('nights', [])]
        slope = float(np.median(sl)); ok = len(V) >= 20 and (max(y for y, m in V) - min(y for y, m in V)) >= 3
        d = TW.drift(V, slope) if ok else None; de = TW.drift(E, slope) if ok else None; dm = TW.drift(Mo, slope) if ok else None
        nd = None; nm = 0
        if nights:
            floor = np.percentile([n[5] for n in nights], 20); g = {}
            for (y, m, dd, L, lev, sp) in nights:
                if sp <= 2 * floor: g.setdefault((y, m), []).append(lev)
            NM = {k: float(np.median(v)) for k, v in g.items()}; nm = len(NM); nd = TW.drift(NM, 1.0) if len(NM) >= 15 else None
        rows[st] = dict(d=d, de=de, dm=dm, nd=nd, months=len(V), years=(min(y for y, m in V), max(y for y, m in V)), slope=slope, mid=float(np.median(list(V.values()))), nm=nm, chips=len(chips),
                        name=next((r['name'] for k, r in R.items() if k[0] == st and r and r.get('name')), ''), yearly={y: float(np.mean([v for (yy, m), v in V.items() if yy == y])) for y in sorted({y for y, m in V})})
    return rows
if __name__ == '__main__':
    R = pickle.load(open(sys.argv[1], 'rb')); META = R.pop('meta', None); SIX = (1, 3, 5, 7, 9, 11) if len(sys.argv) > 2 and sys.argv[2] == 'six' else None
    rows = table(R, SIX)
    print(f"{sys.argv[1]}{' (six months a year)' if SIX else ''}: {len(rows)} stations")
    print('station     months  years       Sun at the level   slope    twilight drift (plain error)   evening   morning   night drift (months)   chips  place')
    for st, x in rows.items():
        if x is None: print(f'{st:<10}  no month with five evening and five morning crossings'); continue
        print(f"{st:<10} {x['months']:>5}   {x['years'][0]}-{x['years'][1]}   {x['mid']:+6.2f}          {x['slope']:+5.2f}   " + (f"{x['d'][0]:+.3f} ({x['d'][1]:.3f})            {x['de'][0]:+.3f}    {x['dm'][0]:+.3f}" if x['d'] else 'too few months or years                    ') + '    ' + (f"{x['nd'][0]:+.3f} ({x['nm']})" if x['nd'] else f"   -   ({x['nm']})") + f"        {x['chips']}     {x['name'][:60]}")
    D = [(st, x) for st, x in rows.items() if x and x['d'] and (META is None or st in META['chosen'])]
    if META: print(f"\nthe twenty of the sample: {' '.join(META['chosen'])}; companions only: {' '.join(META['companions']) or 'none'}")
    t = np.array([x['d'][0] for st, x in D]); e = np.array([x['de'][0] for st, x in D]); mo = np.array([x['dm'][0] for st, x in D])
    print(f'\ninstruments with a drift: {len(D)}')
    if len(D) >= 2:
        print(f'T1. reading darker in twilight by {DIM} magnitude a year or more: {int(np.sum(t >= DIM))} of {len(t)} ({100 * np.mean(t >= DIM):.0f} in 100)')
        print(f'T2. steady within {STEADY}: {int(np.sum(np.abs(t) < STEADY))} of {len(t)} ({100 * np.mean(np.abs(t) < STEADY):.0f} in 100)')
        print(f'T3. reading brighter by {DIM} or more: {int(np.sum(t <= -DIM))} of {len(t)}')
        print(f'T4. evening alone against morning alone: correlation {np.corrcoef(e, mo)[0, 1]:+.3f}; middle difference in size {np.median(np.abs(e - mo)):.3f}; largest {np.max(np.abs(e - mo)):.3f}')
        B = [(x['d'][0], x['nd'][0]) for st, x in D if x['nd']]
        if len(B) >= 3:
            bt = np.array([b[0] for b in B]); bn = np.array([b[1] for b in B]); print(f'T5. the night against the twilight, {len(B)} instruments with both: correlation {np.corrcoef(bt, bn)[0, 1]:+.2f}; slope {np.polyfit(bt, bn, 1)[0]:.2f}; night less twilight, middle {np.median(bn - bt):+.3f}')
        else: print(f'T5. the night against the twilight: only {len(B)} instruments with both')
        print(f'T6. the middle twilight drift of all instruments: {np.median(t):+.3f}; from {t.min():+.3f} to {t.max():+.3f}')
        print('for the record: the drifts in order: ' + ' '.join(f'{x:+.3f}' for x in sorted(t)))
    if META:
        # T7: pairs under one sky. Each companion against the photometer of the dawn page that stands beside it, whose
        # figures are made here from cache2/twilight16.pkl by the same function and the same months.
        mine = table(pickle.load(open('/home/agent1/night/cache2/twilight16.pkl', 'rb')), SIX)
        print('T7. pairs under one sky: the newly fetched photometer less the one beside it, twilight drift and night drift')
        good = n = 0
        for c, m in META['pairs'].items():
            a, b = rows.get(c), mine.get(m)
            if not a or not b or not a['d'] or not b['d']: print(f'   {c} and {m}: no twilight drift for one of them'); continue
            dt_ = a['d'][0] - b['d'][0]
            if not a['nd'] or not b['nd']: print(f'   {c} and {m}: twilight {dt_:+.3f} ({a["d"][0]:+.3f} and {b["d"][0]:+.3f}); no night drift for one of them'); continue
            dn = a['nd'][0] - b['nd'][0]; ok = abs(dn - dt_) <= 0.03; n += 1; good += ok
            print(f'   {c} and {m}: twilight {dt_:+.3f} ({a["d"][0]:+.3f} and {b["d"][0]:+.3f}); night {dn:+.3f} ({a["nd"][0]:+.3f} and {b["nd"][0]:+.3f}); apart {abs(dn - dt_):.3f}' + ('' if ok else '  (more than 0.03)'))
        print(f'   pairs with both: {n}; of them with the night difference within 0.03 of the twilight difference: {good}')
    print('\nyear by year, each instrument: the twilight figure in hundredths of a magnitude from its own mean (positive: reading darker)')
    for st, x in rows.items():
        if x is None: continue
        mean = np.mean(list(x['yearly'].values())); print(f"{st:<10}" + ' '.join(f"{y}:{100 * abs(x['slope']) * (v - mean):+4.0f}" for y, v in x['yearly'].items()))
