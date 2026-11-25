"""First flowering of the snowdrop in Germany, 1951-2023: has it moved, does winter warmth explain it, and does
Hopkins's bioclimatic law hold?   usage: python -I snowdrops.py DATADIR out.npz

Data: Deutscher Wetterdienst, Climate Data Center, open phenology records (annual reporters, wild plants,
snowdrop = object 127, phase 5 = beginning of flowering), the station list, and monthly mean temperatures.
Records marked doubtful, invalid or wrong (quality byte 5, 7, 8) are left out; nothing else is filtered.
"""
import sys, datetime
import numpy as np

D, OUT = sys.argv[1], sys.argv[2]
Y0, Y1, MINYEARS = 1951, 2023, 15                                       # the file's last year, 2024, has six records

# ---- records
rec = []
with open(f"{D}/PH_Jahresmelder_Wildwachsende_Pflanze_Schneegloeckchen_1925_2024_hist.txt", encoding='latin-1') as f:
    head = [h.strip() for h in f.readline().split(';')]
    assert head[:8] == ['Stations_id', 'Referenzjahr', 'Qualitaetsniveau', 'Objekt_id', 'Phase_id', 'Eintrittsdatum', 'Eintrittsdatum_QB', 'Jultag'], head
    dropped = {'quality': 0, 'before 1951': 0, 'after 2023': 0, 'date and day disagree by more than one': 0}
    for line in f:
        p = [x.strip() for x in line.split(';')]
        if len(p) < 8 or not p[0]:
            continue
        sid, year, level, obj, phase, date, qb, jul = int(p[0]), int(p[1]), int(p[2]), int(p[3]), int(p[4]), p[5], int(p[6]), int(p[7])
        assert obj == 127 and phase == 5
        if qb not in (1, 2, 3):
            dropped['quality'] += 1
            continue
        if year < Y0:
            dropped['before 1951'] += 1
            continue
        if year > Y1:
            dropped['after 2023'] += 1
            continue
        d = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:8]))
        day = (d - datetime.date(year, 1, 1)).days + 1                  # day of the reference year; a December date of the year before is zero or negative
        # the service's own day count ("Jultag") leaves out 29 February, so that a date has the same number in every year;
        # it is used here.  A record whose count is more than one day from the calendar's is left out.
        if abs(day - jul) > 1:
            dropped['date and day disagree by more than one'] += 1
            continue
        rec.append((sid, year, jul))
rec = np.array(rec)
print(f"records kept: {len(rec)}; left out: {dropped}")
print(f"   dated in the December before the reference year: {int((rec[:, 2] <= 0).sum())}; after day 150: {int((rec[:, 2] > 150).sum())}")
print(f"   records by year: fewest {min(np.bincount(rec[:, 1])[Y0:])} , most {max(np.bincount(rec[:, 1])[Y0:])}")

# ---- stations
st = {}
with open(f"{D}/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt", encoding='latin-1') as f:
    f.readline()
    for line in f:
        p = [x.strip() for x in line.split(';')]
        if len(p) > 4 and p[0].isdigit():
            try:
                st[int(p[0])] = (float(p[2]), float(p[3]), float(p[4]), p[1])
            except ValueError:
                pass
known = np.array([s in st for s in rec[:, 0]])
print(f"   records at stations missing from the station list: {int((~known).sum())}")
rec = rec[known]
ids, counts = np.unique(rec[:, 0], return_counts=True)
good = set(ids[counts >= MINYEARS].tolist())
keep = np.array([s in good for s in rec[:, 0]])
print(f"stations with any record: {len(ids)}; with {MINYEARS} years or more: {len(good)}; records at those: {int(keep.sum())}")
r = rec[keep]
sid, year, day = r[:, 0], r[:, 1], r[:, 2].astype(float)
lat = np.array([st[s][0] for s in sid]); lon = np.array([st[s][1] for s in sid]); alt = np.array([st[s][2] for s in sid])
years = np.arange(Y0, Y1 + 1)

# ---- S1
print(f"S1  median first flowering, all records kept: day {np.median(rec[:, 2]):.0f}; at the stations used: day {np.median(day):.0f}; quartiles {np.percentile(day, 25):.0f} and {np.percentile(day, 75):.0f}")

# ---- the yearly figure, as registered: mean over stations of (date - the station's own mean), plus the overall mean
smean = {s: day[sid == s].mean() for s in good}
anom = day - np.array([smean[s] for s in sid])
grand = day.mean()
yearly = np.array([anom[year == y].mean() + grand for y in years])
nrep = np.array([(year == y).sum() for y in years])
# a check on it: station and year effects fitted together (so that a station seen only in late years does not pull its own mean)
se = dict(smean)
for _ in range(60):
    ye = {y: (day[year == y] - np.array([se[s] for s in sid[year == y]])).mean() for y in years}
    yv = np.array([ye[y] for y in year])
    for s in good:
        m = sid == s
        se[s] = (day[m] - yv[m]).mean()
    shift = np.mean(list(ye.values()))
    ye = {y: v - shift for y, v in ye.items()}
    se = {s: v + shift for s, v in se.items()}
yearly2 = np.array([ye[y] for y in years]) + np.mean(list(se.values()))
m6190 = (years >= 1961) & (years <= 1990); m9120 = (years >= 1991) & (years <= 2020)
print(f"S2  mean of the yearly figure 1961-1990: day {yearly[m6190].mean():.1f}; 1991-2020: day {yearly[m9120].mean():.1f}; change {yearly[m9120].mean() - yearly[m6190].mean():+.1f} days"
      f"   (station and year effects fitted together: {yearly2[m9120].mean() - yearly2[m6190].mean():+.1f})")
sl = np.polyfit(years, yearly, 1)[0]
print(f"    straight-line trend 1951-2023: {10 * sl:+.2f} days a decade; 1951-1987: {10 * np.polyfit(years[years <= 1987], yearly[years <= 1987], 1)[0]:+.2f}; 1988-2023: {10 * np.polyfit(years[years >= 1988], yearly[years >= 1988], 1)[0]:+.2f}")

# ---- S3: winter warmth
def monthly(m):
    out = {}
    with open(f"{D}/regional_averages_tm_{m:02d}.txt", encoding='latin-1') as f:
        f.readline()
        cols = [c.strip() for c in f.readline().split(';')]
        k = cols.index('Deutschland')
        for line in f:
            p = line.split(';')
            if len(p) > k and p[0].strip().isdigit():
                out[int(p[0])] = float(p[k])
    return out
jan, feb, dec = monthly(1), monthly(2), monthly(12)
tjf = np.array([(jan[y] + feb[y]) / 2 for y in years])
tdjf = np.array([(dec[y - 1] + jan[y] + feb[y]) / 3 for y in years])
cjf = np.corrcoef(tjf, yearly)[0, 1]
bjf = np.polyfit(tjf, yearly, 1)
print(f"S3  yearly figure against Germany's mean January-February temperature: correlation {cjf:.3f}; {bjf[0]:+.2f} days per degree"
      f"   (December to February: correlation {np.corrcoef(tdjf, yearly)[0, 1]:.3f}, {np.polyfit(tdjf, yearly, 1)[0]:+.2f} days per degree)")
print(f"    January-February mean temperature: 1961-1990 {tjf[m6190].mean():.2f} C, 1991-2020 {tjf[m9120].mean():.2f} C; warming times the slope: {bjf[0] * (tjf[m9120].mean() - tjf[m6190].mean()):+.1f} days")
res = yearly - np.polyval(bjf, tjf)
print(f"    what is left after winter warmth: trend {10 * np.polyfit(years, res, 1)[0]:+.2f} days a decade")

# ---- S4-S6: Hopkins.  One regression with a level for every year: take out each year's mean from everything, then least squares.
def within(v):
    out = v.astype(float).copy()
    for y in years:
        m = year == y
        out[m] -= v[m].mean()
    return out
X = np.c_[within(alt / 100.0), within(lat), within(lon)]
yv = within(day)
coef = np.linalg.lstsq(X, yv, rcond=None)[0]
rng = np.random.default_rng(1)
stations = np.array(sorted(good))
idx_of = {s: np.nonzero(sid == s)[0] for s in stations}
boot = []
for _ in range(300):                                                    # stations resampled whole: their years are not independent
    pick = rng.choice(stations, len(stations))
    ii = np.concatenate([idx_of[s] for s in pick])
    boot.append(np.linalg.lstsq(X[ii], yv[ii], rcond=None)[0])
lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
for name, k, hop in (("S4  altitude: days later per 100 m", 0, 4 / (400 * 0.3048 / 100)), ("S5  latitude: days later per degree north", 1, 4.0), ("S6  longitude: days later per degree east", 2, 4 / 5)):
    print(f"{name}: {coef[k]:+.2f}  (95% of resamplings: {lo[k]:+.2f} to {hi[k]:+.2f}; Hopkins {hop:.2f})")
print(f"    share of the spread among records in the same year that the three explain: {1 - ((yv - X @ coef) ** 2).sum() / (yv ** 2).sum():.2f}")
# altitude bands, for the picture and as a check on the straight line
sall = np.array([np.mean([se[s]]) for s in stations])
salt = np.array([st[s][2] for s in stations])
for a, b in ((0, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 700), (700, 1000), (1000, 2000)):
    m = (salt >= a) & (salt < b)
    if m.sum():
        print(f"    stations {a:4d}-{b:4d} m: {int(m.sum()):4d}; mean date, year effects removed: day {sall[m].mean():.1f}")

# ---- S7
print(f"S7  standard deviation of the yearly figure: {yearly.std(ddof=1):.1f} days; earliest year {years[yearly.argmin()]} (day {yearly.min():.0f}), latest {years[yearly.argmax()]} (day {yearly.max():.0f}): {yearly.max() - yearly.min():.0f} days apart")
print("    five earliest:", [(int(years[i]), round(float(yearly[i]))) for i in np.argsort(yearly)[:5]], " five latest:", [(int(years[i]), round(float(yearly[i]))) for i in np.argsort(yearly)[::-1][:5]])
print(f"    stations reporting in a year: least {nrep.min()} ({years[nrep.argmin()]}), most {nrep.max()} ({years[nrep.argmax()]})")
np.savez(OUT, years=years, yearly=yearly, yearly2=yearly2, nrep=nrep, tjf=tjf, tdjf=tdjf, coef=coef, lo=lo, hi=hi,
         st_id=stations, st_lat=np.array([st[s][0] for s in stations]), st_lon=np.array([st[s][1] for s in stations]), st_alt=salt, st_eff=sall,
         st_n=np.array([len(idx_of[s]) for s in stations]))
