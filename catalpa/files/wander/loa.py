# The Lunar Occultation Archive (Herald & Gault, VizieR VI/132C): timings from 1623 on, reduced by its authors with the DE440 Moon, measured limb heights (LRO) and Gaia star places,
# using the published spline for the clock correction before 1961.  For each record: OC = computed height of the star above the limb at the reported time (arcsec); dOC = its change per +1 s.
# Seconds by which the event was seen before (-) or after (+) the computed time = OC / dOC.
import numpy as np, sys
def recs(y0, y1, path='/home/agent1/wander/loa/lunarocc.dat'):
    out = []
    with open(path, 'r', errors='replace') as f:
        for line in f:
            try: y = int(line[0:4])
            except ValueError: continue
            if y < y0: continue
            if y > y1: break
            def fl(a, b):
                try: return float(line[a - 1:b])
                except ValueError: return np.nan
            out.append(dict(y=y, mo=int(line[4:6] or 0), d=int(line[6:8] or 0), h=int(line[8:10] or 0), mi=int(line[10:12] or 0), s=fl(13, 18), cat=line[18], num=line[19:25].strip(), phen=line[26], limb=line[27], peapp=line[33], meth1=line[34], tmeth=line[62],
                            graze=line[28], srce=line[71], dup=line[72], valid=line[73], town=line[127:177].strip(), name=line[188:213].strip(), limbh=fl(297, 303), oc=fl(304, 313), pa=fl(314, 320), doc=fl(321, 327),
                            dmoon=fl(328, 333), ref=line[340:347].strip()))
    return out
def secs(R, phen='D', limb='D', extra=lambda r: True):
    v = np.array([r['oc'] / r['doc'] for r in R if r['phen'] == phen and r['limb'] == limb and r['graze'] != 'G' and np.isfinite(r['oc']) and abs(r['doc']) > 0.15 and extra(r)])
    return v[np.abs(v) < 30]
if __name__ == '__main__':
    if sys.argv[1] == 'tables':
        # Everything quoted on the eclipse page from this archive.  The seconds are two of the archive's columns divided (OC / dOC); the cuts (no grazes, closing rate above 0.15"/s,
        # under 30 s) and the medians are mine.
        print('Dark-limb disappearances, median seconds seen-minus-computed, by span (n):')
        for y0, y1 in ((1840, 1849), (1850, 1859), (1860, 1869), (1870, 1879), (1880, 1889), (1890, 1899), (1900, 1909), (1910, 1919), (1920, 1929), (1930, 1939), (1940, 1949), (1950, 1959), (1961, 1975), (1970, 1974), (2010, 2014)):
            v = secs(recs(y0, y1)); print(f'  {y0}-{y1}: {np.median(v):+.2f} ({len(v)})')
        R = recs(1860, 1869); v = secs(R); print(f'1860s pooled: median {np.median(v):+.2f}, n={len(v)}; dark-limb reappearances: median {np.median(secs(R, "R", "D")):+.2f}, n={len(secs(R, "R", "D"))}')
        allD = [r for r in R if r['phen'] == 'D' and r['limb'] == 'D' and r['graze'] != 'G']
        print('1860s dark-limb disappearances by reaction-time code (S, A, B = taken off by the observer or compiler; U = not taken off; E = not relevant; X = not known):', {c: sum(1 for r in allD if r['peapp'] == c) for c in sorted(set(r['peapp'] for r in allD))})
        print('1860s by source of star position:', {c: sum(1 for r in allD if r['ref'] == c) for c in sorted(set(r['ref'] for r in allD))})
        v = secs(recs(1868, 1868)); print(f'1868 alone: median {np.median(v):+.2f}, n={len(v)}')
        R = recs(1961, 1975)
        for label, f in (('reaction-time code X (not known whether taken off)', lambda r: r['peapp'] == 'X'), ('code X and eye-and-ear timing (RGO method 2 or 7)', lambda r: r['peapp'] == 'X' and r['tmeth'] in '27'),
                         ('reaction time taken off by the observer (code S)', lambda r: r['peapp'] == 'S'), ('code U (not taken off)', lambda r: r['peapp'] == 'U')):
            v = secs(R, extra=f); print(f'1961-1975, when the clock correction is known exactly; {label}: median {np.median(v) if len(v) else float("nan"):+.2f}, n={len(v)}')
        ee = [r for r in R if r['phen'] == 'D' and r['limb'] == 'D' and r['graze'] != 'G' and r['peapp'] == 'X' and r['tmeth'] in '27' and np.isfinite(r['oc']) and abs(r['doc']) > 0.15 and abs(r['oc'] / r['doc']) < 30]
        towns = {}
        for r in ee: towns.setdefault(r['town'][:28], []).append(r['oc'] / r['doc'])
        print('   of those eye-and-ear timings, by station (n, median):', sorted(((len(v), k, round(float(np.median(v)), 2)) for k, v in towns.items()), reverse=True)[:8])
        allD60 = [r for r in recs(1860, 1869) if r['phen'] == 'D' and r['limb'] == 'D' and r['graze'] != 'G']
        print('1860s dark-limb disappearances with a timing method recorded (RGO code; 2 = eye-and-ear, 7 = eye-and-ear with sidereal chronometer, 3 = chronograph):', {c: sum(1 for r in allD60 if r['tmeth'] == c) for c in sorted(set(r['tmeth'] for r in allD60))})
        print('Aldebaran (ZC 692), 9 September 1868:')
        for r in recs(1868, 1868):
            if r['mo'] == 9 and r['d'] == 9 and r['cat'] == 'R' and r['num'] == '692':
                print(f"  {r['h']:02d}:{r['mi']:02d}:{r['s']:04.1f} {'disappearance' if r['phen'] == 'D' else 'reappearance'} at the {'bright' if r['limb'] == 'B' else 'dark'} limb: {r['oc'] / r['doc']:+.1f} s | {r['town'][:30]}")
        sys.exit()
    y0, y1 = int(sys.argv[1]), int(sys.argv[2]); R = recs(y0, y1)
    if len(sys.argv) > 3 and sys.argv[3] == 'list':
        pat = sys.argv[4].lower()
        for r in R:
            if pat in r['town'].lower():
                dt = r['oc'] / r['doc'] if r['doc'] else np.nan
                print(f"{r['y']} {r['mo']:2d}/{r['d']:02d} {r['h']:02d}:{r['mi']:02d}:{r['s']:06.3f} {r['cat']}{r['num']:>6s} {r['phen']}{r['limb']}{r['graze']} valid={r['valid']} dup={r['dup']} OC {r['oc']:+8.3f}\" dOC {r['doc']:+6.2f} limb {r['limbh']:+6.3f} -> seen {dt:+6.1f} s from computed | {r['town'][:28]} | {r['name']}")
    else:
        print('year   n   median seconds (seen minus computed)   mean   sd    [dark-limb disappearances, not grazes, |dOC|>0.15, |seconds|<30]')
        for y in range(y0, y1 + 1):
            v = [r['oc'] / r['doc'] for r in R if r['y'] == y and r['phen'] == 'D' and r['limb'] == 'D' and r['graze'] != 'G' and np.isfinite(r['oc']) and abs(r['doc']) > 0.15]
            v = np.array([x for x in v if abs(x) < 30])
            if len(v): print(f'{y}  {len(v):4d}   {np.median(v):+6.2f}   {v.mean():+6.2f}   {v.std():5.2f}   (standard error {v.std() / np.sqrt(len(v)):.2f})')
