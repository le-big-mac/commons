# The thirteenth sheet scored: the four southern SQM stations month by month, 2022 and 2023 (and June to August 2025),
# by the measure of the eleventh sheet (src/sqm_depth.py, unchanged; here its files are read from data/sqm2/).
# A month's figure at a depth is the station's reading there less the mean of the same month of 2021 and 2024,
# whichever it has: magnitudes, negative for a brighter twilight. The lines use 7 degrees, where all four stations
# give a figure; 8 degrees is printed beside it.
import os, pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('sqm_depth', B + 'src/sqm_depth.py'); SD = importlib.util.module_from_spec(spec); spec.loader.exec_module(SD)
_load = SD.load
def load2(code, y, m):
    import csv, datetime as dt
    fn = B + f'data/sqm2/{code}_{y}-{m:02d}.csv'
    if not os.path.exists(fn): return None
    T, M = [], []
    for row in csv.DictReader(open(fn, encoding='utf-8')):
        try: v = float(row['nsb']); t = dt.datetime.strptime(row['received_utc'][:19], '%Y-%m-%d %H:%M:%S')
        except (ValueError, KeyError): continue
        if v > 0: T.append((t - SD.TW.T2000).total_seconds()); M.append(v)
    if len(T) < 50: return None
    o = np.argsort(T); return np.array(T)[o], np.array(M)[o]
SD.load = load2
ST = SD.ST; YEARS = (2021, 2022, 2023, 2024, 2025)
if __name__ == '__main__':
    R = {(c, y, m): SD.reduce(c, y, m) for c in ST for y in YEARS for m in range(1, 13)}
    pickle.dump(R, open(B + 'cache2/sqm_months.pkl', 'wb'))
    def anom(c, y, m, dp):
        v = SD.fig(R[(c, y, m)], dp); base = [b for b in (SD.fig(R[(c, yy, m)], dp) for yy in (2021, 2024)) if b is not None]
        return (v - float(np.mean(base))) if v is not None and base else None
    A = {(c, y, m, dp): anom(c, y, m, dp) for c in ST for y in YEARS for m in range(1, 13) for dp in (7.0, 8.0)}
    for dp in (7.0, 8.0):
        print(f'each station, every month of 2022 and 2023 at {dp:g} degrees (hundredths of a magnitude; negative: a brighter twilight; . no figure)')
        for c, (name, lat, lon) in ST.items():
            print(f"   {name.split(',')[0]:<14} {lat:+6.1f}  " + ' | '.join(' '.join(f"{100 * A[(c, y, m, dp)]:+4.0f}" if A[(c, y, m, dp)] is not None else '   .' for m in range(1, 13)) for y in (2022, 2023)))
        mids = {(y, m): [A[(c, y, m, dp)] for c in ST if A[(c, y, m, dp)] is not None] for y in (2022, 2023) for m in range(1, 13)}
        print('   the middle             ' + ' | '.join(' '.join(f"{100 * np.median(mids[(y, m)]):+4.0f}" if mids[(y, m)] else '   .' for m in range(1, 13)) for y in (2022, 2023)))
        print('   stations               ' + ' | '.join(' '.join(f"{len(mids[(y, m)]):4d}" for m in range(1, 13)) for y in (2022, 2023)))
    print('   which comparison years each station has, month by month (1 = 2021 alone, 4 = 2024 alone, b = both, . = neither):')
    for c, (name, lat, lon) in ST.items():
        print(f"   {name.split(',')[0]:<14} " + ' '.join(('b' if all(SD.fig(R[(c, yy, m)], 7.0) is not None for yy in (2021, 2024)) else '1' if SD.fig(R[(c, 2021, m)], 7.0) is not None else '4' if SD.fig(R[(c, 2024, m)], 7.0) is not None else '.') for m in range(1, 13)))
    a7 = lambda c, y, m: A[(c, y, m, 7.0)]
    def stretch(c, months, need):
        v = [a7(c, y, m) for y, m in months if a7(c, y, m) is not None]; return float(np.mean(v)) if len(v) >= need else None
    def middle(vals): v = [x for x in vals if x is not None]; return (float(np.median(v)), len(v)) if v else (None, 0)
    f = lambda v: 'none' if v is None else f'{v:+.3f}'
    print('\nThe lines of the thirteenth sheet (7 degrees; unrounded figures; marks included)')
    m1, n1 = middle([a7(c, 2022, 1) for c in ST]); print(f"T1. January 2022: the middle of the stations within 0.10 of nothing (two or more stations): {f(m1)} ({n1}): {'void' if n1 < 2 else ('held' if abs(m1) <= 0.10 else 'failed')}")
    p = [a7('PAOF', 2022, m) for m in (3, 4)]; pv = [x for x in p if x is not None]; print(f"T2. Ouro Fino at -0.10 or below in March or April 2022: {f(p[0])}, {f(p[1])}: {'void' if not pv else ('held' if min(pv) <= -0.10 else 'failed')}")
    o = [a7('Oam', 2022, m) for m in (2, 3, 4)]; ov = [x for x in o if x is not None]; print(f"T3. Oamaru above -0.10 in each of February, March and April 2022: {', '.join(f(x) for x in o)}: {'void' if len(ov) < 2 else ('held' if min(ov) > -0.10 else 'failed')}")
    m4, n4 = middle([stretch(c, [(2023, 9), (2023, 10), (2023, 11)], 2) for c in ST]); print(f"T4. September to November 2023: the middle within 0.08 of nothing: {f(m4)} ({n4}): {'void' if n4 < 2 else ('held' if abs(m4) <= 0.08 else 'failed')}")
    m5, n5 = middle([stretch(c, [(2023, m) for m in range(1, 7)], 4) for c in ST]); print(f"T5. January to June 2023: the middle between -0.03 and -0.20: {f(m5)} ({n5}): {'void' if n5 < 2 else ('held' if -0.20 <= m5 <= -0.03 else 'failed')}")
    def first2(c):
        ks = [(y, m) for y in (2022, 2023) for m in range(1, 13)]
        for i in range(len(ks) - 1):
            a, b = a7(c, *ks[i]), a7(c, *ks[i + 1])
            if a is not None and b is not None and a <= -0.10 and b <= -0.10: return ks[i]
        return None
    fp, fo = first2('PAOF'), first2('Oam'); print(f"T6. the first of two months in a row at -0.10 or below comes earlier at Ouro Fino than at Oamaru: {fp}, {fo}: {'void' if fp is None or fo is None else ('held' if fp < fo else 'failed')}")
    m7, n7 = middle([stretch(c, [(2025, 6), (2025, 7), (2025, 8)], 2) for c in ST]); print(f"T7. June to August 2025: the middle within 0.08 of nothing: {f(m7)} ({n7}): {'void' if n7 < 2 else ('held' if abs(m7) <= 0.08 else 'failed')}")
    print('\nfor the record, each station\'s first of two months in a row at -0.10 or below at 7 degrees: ' + '; '.join(f"{ST[c][0].split(',')[0]} {first2(c)}" for c in ST))
    print('for the record, each station by stretch at 7 degrees: ' + '; '.join(f"{ST[c][0].split(',')[0]}: June to August 2022 {f(stretch(c, [(2022, 6), (2022, 7), (2022, 8)], 2))}, September to December 2022 {f(stretch(c, [(2022, m) for m in (9, 10, 11, 12)], 3))}, January to June 2023 {f(stretch(c, [(2023, m) for m in range(1, 7)], 4))}, September to November 2023 {f(stretch(c, [(2023, 9), (2023, 10), (2023, 11)], 2))}, June to August 2025 {f(stretch(c, [(2025, 6), (2025, 7), (2025, 8)], 2))}" for c in ST))
