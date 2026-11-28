# The fourteenth sheet: the thirteenth sheet's seven lines again, by a measure that a meter's ageing cannot touch.
# The measure: a month's reading with the Sun 7 degrees down LESS the same month's reading with the Sun 3 degrees
# down (how much the twilight has faded between the two), and that set against the same month of 2021 and 2024,
# whichever the station has. A meter that reads darker by the same amount at every brightness drops out of it.
# Reads the reductions the thirteenth sheet's program stored (cache2/sqm_months.pkl); nothing is fetched.
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('sqm_depth', B + 'src/sqm_depth.py'); SD = importlib.util.module_from_spec(spec); spec.loader.exec_module(SD)
ST = SD.ST; YEARS = (2021, 2022, 2023, 2024, 2025); REF = 3.0
if __name__ == '__main__':
    R = pickle.load(open(B + 'cache2/sqm_months.pkl', 'rb'))
    def steep(c, y, m, dp):
        a, b = SD.fig(R[(c, y, m)], dp), SD.fig(R[(c, y, m)], REF); return (a - b) if a is not None and b is not None else None
    def anom(c, y, m, dp, f=steep):
        v = f(c, y, m, dp); base = [b for b in (f(c, yy, m, dp) for yy in (2021, 2024)) if b is not None]
        return (v - float(np.mean(base))) if v is not None and base else None
    direct = lambda c, y, m, dp: SD.fig(R[(c, y, m)], dp)
    A = {(c, y, m, dp): anom(c, y, m, dp) for c in ST for y in YEARS for m in range(1, 13) for dp in (7.0, 8.0)}
    for dp in (7.0, 8.0):
        print(f'the fading from 3 to {dp:g} degrees, each station, every month of 2022 and 2023, less the same month of 2021 and 2024 (hundredths of a magnitude; negative: a brighter twilight at {dp:g} degrees for the same twilight at 3; . no figure)')
        for c, (name, lat, lon) in ST.items():
            print(f"   {name.split(',')[0]:<14} {lat:+6.1f}  " + ' | '.join(' '.join(f"{100 * A[(c, y, m, dp)]:+4.0f}" if A[(c, y, m, dp)] is not None else '   .' for m in range(1, 13)) for y in (2022, 2023)))
        mids = {(y, m): [A[(c, y, m, dp)] for c in ST if A[(c, y, m, dp)] is not None] for y in (2022, 2023) for m in range(1, 13)}
        print('   the middle             ' + ' | '.join(' '.join(f"{100 * np.median(mids[(y, m)]):+4.0f}" if mids[(y, m)] else '   .' for m in range(1, 13)) for y in (2022, 2023)))
        print('   stations               ' + ' | '.join(' '.join(f"{len(mids[(y, m)]):4d}" for m in range(1, 13)) for y in (2022, 2023)))
    print('\nthe reading at 3 degrees itself, each station, every month of 2022 and 2023, less the same month of 2021 and 2024 (hundredths)')
    for c, (name, lat, lon) in ST.items():
        print(f"   {name.split(',')[0]:<14} {lat:+6.1f}  " + ' | '.join(' '.join((lambda v: f"{100 * v:+4.0f}" if v is not None else '   .')(anom(c, y, m, 3.0, direct)) for m in range(1, 13)) for y in (2022, 2023)))
    print('\nhow each meter\'s reading at 3 degrees changes from year to year (the mean over the months both years have, and how many; magnitudes; positive: reads darker)')
    for c, (name, lat, lon) in ST.items():
        row = []
        for y0, y1 in ((2021, 2022), (2022, 2023), (2023, 2024), (2024, 2025), (2021, 2024), (2021, 2025)):
            d = [direct(c, y1, m, 3.0) - direct(c, y0, m, 3.0) for m in range(1, 13) if direct(c, y1, m, 3.0) is not None and direct(c, y0, m, 3.0) is not None]
            row.append(f"{y0}-{y1 % 100}: {np.mean(d):+.2f} ({len(d)})" if d else f"{y0}-{y1 % 100}: none")
        print(f"   {name.split(',')[0]:<14} " + '; '.join(row))
    print('   and the same for the fading from 3 to 7 degrees:')
    for c, (name, lat, lon) in ST.items():
        row = []
        for y0, y1 in ((2021, 2024), (2024, 2025), (2021, 2025)):
            d = [steep(c, y1, m, 7.0) - steep(c, y0, m, 7.0) for m in range(1, 13) if steep(c, y1, m, 7.0) is not None and steep(c, y0, m, 7.0) is not None]
            row.append(f"{y0}-{y1 % 100}: {np.mean(d):+.2f} ({len(d)})" if d else f"{y0}-{y1 % 100}: none")
        print(f"   {name.split(',')[0]:<14} " + '; '.join(row))
    a7 = lambda c, y, m: A[(c, y, m, 7.0)]
    def stretch(c, months, need, dp=7.0):
        v = [A[(c, y, m, dp)] for y, m in months if A[(c, y, m, dp)] is not None]; return float(np.mean(v)) if len(v) >= need else None
    def middle(vals): v = [x for x in vals if x is not None]; return (float(np.median(v)), len(v)) if v else (None, 0)
    f = lambda v: 'none' if v is None else f'{v:+.3f}'
    print('\nThe lines of the fourteenth sheet (the fading from 3 to 7 degrees; unrounded figures; marks included)')
    m1, n1 = middle([a7(c, 2022, 1) for c in ST]); print(f"U1. January 2022: the middle of the stations within 0.10 of nothing (two or more stations): {f(m1)} ({n1}): {'void' if n1 < 2 else ('held' if abs(m1) <= 0.10 else 'failed')}")
    p = [a7('PAOF', 2022, m) for m in (3, 4)]; pv = [x for x in p if x is not None]; print(f"U2. Ouro Fino at -0.10 or below in March or April 2022: {f(p[0])}, {f(p[1])}: {'void' if not pv else ('held' if min(pv) <= -0.10 else 'failed')}")
    o = [a7('Oam', 2022, m) for m in (2, 3, 4)]; ov = [x for x in o if x is not None]; print(f"U3. Oamaru above -0.10 in each of February, March and April 2022: {', '.join(f(x) for x in o)}: {'void' if len(ov) < 2 else ('held' if min(ov) > -0.10 else 'failed')}")
    m4, n4 = middle([stretch(c, [(2023, 9), (2023, 10), (2023, 11)], 2) for c in ST]); print(f"U4. September to November 2023: the middle within 0.08 of nothing: {f(m4)} ({n4}): {'void' if n4 < 2 else ('held' if abs(m4) <= 0.08 else 'failed')}")
    m5, n5 = middle([stretch(c, [(2023, m) for m in range(1, 7)], 4) for c in ST]); print(f"U5. January to June 2023: the middle between -0.03 and -0.20: {f(m5)} ({n5}): {'void' if n5 < 2 else ('held' if -0.20 <= m5 <= -0.03 else 'failed')}")
    def first2(c):
        ks = [(y, m) for y in (2022, 2023) for m in range(1, 13)]
        for i in range(len(ks) - 1):
            a, b = a7(c, *ks[i]), a7(c, *ks[i + 1])
            if a is not None and b is not None and a <= -0.10 and b <= -0.10: return ks[i]
        return None
    fp, fo = first2('PAOF'), first2('Oam'); print(f"U6. Oamaru has no two months in a row at -0.10 or below before April 2022: {fo}: {'held' if fo is None or fo >= (2022, 4) else 'failed'}   (Ouro Fino's first: {fp})")
    m7, n7 = middle([stretch(c, [(2025, 6), (2025, 7), (2025, 8)], 2) for c in ST]); print(f"U7. June to August 2025: the middle within 0.08 of nothing: {f(m7)} ({n7}): {'void' if n7 < 2 else ('held' if abs(m7) <= 0.08 else 'failed')}")
    m8, n8 = middle([stretch(c, [(2022, 6), (2022, 7), (2022, 8)], 2) for c in ST]); print(f"U8. June to August 2022: the middle at -0.15 or below: {f(m8)} ({n8}): {'void' if n8 < 2 else ('held' if m8 <= -0.15 else 'failed')}")
    print('\nfor the record, each station by stretch, the fading from 3 to 7 degrees and (after the bar) from 3 to 8:')
    for c in ST:
        print(f"   {ST[c][0].split(',')[0]:<14} " + ' | '.join('; '.join(f"{lab} {f(stretch(c, mo, need, dp))}" for lab, mo, need in (('Jun-Aug 2022', [(2022, 6), (2022, 7), (2022, 8)], 2), ('Sep-Dec 2022', [(2022, m) for m in (9, 10, 11, 12)], 3), ('Jan-Jun 2023', [(2023, m) for m in range(1, 7)], 4), ('Sep-Nov 2023', [(2023, 9), (2023, 10), (2023, 11)], 2), ('Jun-Aug 2025', [(2025, 6), (2025, 7), (2025, 8)], 2))) for dp in (7.0, 8.0)))
