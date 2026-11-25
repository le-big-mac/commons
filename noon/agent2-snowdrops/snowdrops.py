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
        # The service's own day count ("Jultag") mostly leaves out 29 February, so that a date has the same number in every
        # year, but not consistently (the referee found 161 records that count the leap day).  So the day number is taken
        # from the date, for every record, with 29 February left out (it gets 59, like 28 February).
        # A record whose listed count is more than one day from the calendar's is left out.
        if abs(day - jul) > 1:
            dropped['date and day disagree by more than one'] += 1
            continue
        leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        if leap and d.year == year and day >= 60:
            day -= 1
        rec.append((sid, year, day))
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
print(f"S1  median first flowering, all records kept: day {np.median(rec[:, 2]):.0f}, quartiles {np.percentile(rec[:, 2], 25):.0f} and {np.percentile(rec[:, 2], 75):.0f};"
      f" at the stations used: day {np.median(day):.0f}, quartiles {np.percentile(day, 25):.0f} and {np.percentile(day, 75):.0f}")

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
      f"   (station and year effects fitted together: day {yearly2[m6190].mean():.1f} to day {yearly2[m9120].mean():.1f}, {yearly2[m9120].mean() - yearly2[m6190].mean():+.1f})")
# a check on which of the two is right that needs no fitting: stations with 25 or more years in each period
both = [s_ for s_ in good if ((sid == s_) & (year >= 1961) & (year <= 1990)).sum() >= 25 and ((sid == s_) & (year >= 1991) & (year <= 2020)).sum() >= 25]
dd = np.array([day[(sid == s_) & (year >= 1991) & (year <= 2020)].mean() - day[(sid == s_) & (year >= 1961) & (year <= 1990)].mean() for s_ in both])
print(f"    stations with 25 or more years in each period: {len(both)}; mean change at those stations {dd.mean():+.1f} days (standard error {dd.std(ddof=1) / np.sqrt(len(dd)):.2f})")
def ols(X, yv):
    """least squares with standard errors: returns coefficients and t values"""
    X = np.column_stack([np.ones(len(yv))] + list(X))
    b, *_ = np.linalg.lstsq(X, yv, rcond=None)
    res = yv - X @ b
    cov = res @ res / (len(yv) - X.shape[1]) * np.linalg.inv(X.T @ X)
    return b, b / np.sqrt(np.diag(cov))


for name, series in (("registered series", yearly), ("stations and years fitted together", yearly2)):
    b, t = ols([years], series)
    print(f"    straight-line trend 1951-2023, {name}: {10 * b[1]:+.2f} days a decade (t = {t[1]:.1f})")
dec = [(a, yearly2[(years >= a) & (years < a + 10)].mean()) for a in range(1960, 2020, 10)]
print("    decade means, stations and years fitted together:", ", ".join(f"{a}s day {m:.1f}" for a, m in dec))

# ---- S3: winter warmth.  For the registered series (as registered) and for the better one (added after the referee's report).
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
jan, feb, dec12 = monthly(1), monthly(2), monthly(12)
tjf = np.array([(jan[y] + feb[y]) / 2 for y in years])
tdjf = np.array([(dec12[y - 1] + jan[y] + feb[y]) / 3 for y in years])
warming = tjf[m9120].mean() - tjf[m6190].mean()
print(f"S3  January-February mean temperature for Germany: 1961-1990 {tjf[m6190].mean():.2f} C, 1991-2020 {tjf[m9120].mean():.2f} C: warmer by {warming:.2f}")
for name, series in (("registered series", yearly), ("stations and years fitted together", yearly2)):
    shift = series[m9120].mean() - series[m6190].mean()
    c = np.corrcoef(tjf, series)[0, 1]
    b1, t1 = ols([tjf], series)
    b2, t2 = ols([tjf, years], series)
    print(f"    {name}: correlation {c:.3f}; {b1[1]:+.2f} days per degree; warming times that slope {b1[1] * warming:+.1f} days of a shift of {shift:+.1f} ({100 * b1[1] * warming / shift:.0f}%)")
    print(f"       date on temperature and year together: {b2[1]:+.2f} days per degree, and a trend of {10 * b2[2]:+.2f} days a decade left over (t = {t2[2]:.1f})")
bjf = np.polyfit(tjf, yearly, 1)
cjf = np.corrcoef(tjf, yearly)[0, 1]

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
for name, series in (("registered series", yearly), ("stations and years fitted together", yearly2)):
    print(f"S7  {name}: standard deviation {series.std(ddof=1):.1f} days; earliest year {years[series.argmin()]} (day {series.min():.1f}), latest {years[series.argmax()]} (day {series.max():.1f}): {series.max() - series.min():.1f} days apart")
print("    five earliest (fitted together):", [(int(years[i]), round(float(yearly2[i]), 1)) for i in np.argsort(yearly2)[:5]], " five latest:", [(int(years[i]), round(float(yearly2[i]), 1)) for i in np.argsort(yearly2)[::-1][:5]])
print(f"    stations reporting in a year: least {nrep.min()} ({years[nrep.argmin()]}), most {nrep.max()} ({years[nrep.argmax()]})")
np.savez(OUT, years=years, yearly=yearly, yearly2=yearly2, nrep=nrep, tjf=tjf, tdjf=tdjf, coef=coef, lo=lo, hi=hi,
         st_id=stations, st_lat=np.array([st[s][0] for s in stations]), st_lon=np.array([st[s][1] for s in stations]), st_alt=salt, st_eff=sall,
         st_n=np.array([len(idx_of[s]) for s in stations]))
