import collections, datetime
import numpy as np
from load import *

hdr, R, bad = read_records()
print('header:', repr(hdr[:120]))
print('records parsed:', len(R), ' unparsed lines:', len(bad))
for b in bad[:5]:
    print('  bad', b[0], repr(b[1][:100]))
sid, yr, qn, obj, ph, date, qb, jul = R.T
print('Objekt_id:', collections.Counter(obj.tolist()))
print('Phase_id:', collections.Counter(ph.tolist()))
print('Qualitaetsniveau:', collections.Counter(qn.tolist()))
print('Eintrittsdatum_QB:', sorted(collections.Counter(qb.tolist()).items()))
print('year range', yr.min(), yr.max())
print('pre-1951:', (yr < 1951).sum(), ' 2024:', (yr == 2024).sum(), ' >2024:', (yr > 2024).sum())
print('Jultag range', jul.min(), jul.max())

# duplicates of (station, year)
keys = sid * 10000 + yr
u, c = np.unique(keys, return_counts=True)
print('duplicate station-years:', (c > 1).sum())

# date-year vs Referenzjahr
dy = date // 10000
print('date year - refyear:', sorted(collections.Counter((dy - yr).tolist()).items()))

# true day-of-year vs Jultag
td = np.array([(-9999 if true_doy(int(y), int(d)) is None else true_doy(int(y), int(d))) for y, d in zip(yr, date)])
print('invalid dates:', (td == -9999).sum())
diff = jul - td
print('Jultag - trueDOY (relative to 1 Jan of ref year):', sorted(collections.Counter(diff.tolist()).items()))

leap = np.array([(y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) for y in dy])
mm = (date // 100) % 100
dd = date % 100
after_feb = leap & (mm >= 3) & (dy == yr)
print('leap-year records dated March or later (same year):', after_feb.sum())
print('  of which Jultag - trueDOY:', sorted(collections.Counter(diff[after_feb].tolist()).items()))
feb29 = (mm == 2) & (dd == 29)
print('records dated 29 Feb:', feb29.sum(), ' their Jultag:', sorted(collections.Counter(jul[feb29].tolist()).items()))
mar1leap = leap & (mm == 3) & (dd == 1)
print('records dated 1 Mar in leap years:', mar1leap.sum(), ' Jultag:', sorted(collections.Counter(jul[mar1leap].tolist()).items()))
mar1non = (~leap) & (mm == 3) & (dd == 1)
print('records dated 1 Mar in non-leap years:', mar1non.sum(), ' Jultag:', sorted(collections.Counter(jul[mar1non].tolist()).items()))
feb28leap = leap & (mm == 2) & (dd == 28)
print('records dated 28 Feb in leap years:', feb28leap.sum(), ' Jultag:', sorted(collections.Counter(jul[feb28leap].tolist()).items()))
dec31 = (mm == 12) & (dd == 31)
print('records dated 31 Dec:', dec31.sum(), list(zip(yr[dec31].tolist(), date[dec31].tolist(), jul[dec31].tolist()))[:10])

# December-before records
prev = dy < yr
print('dated in a previous calendar year:', prev.sum())
print('  examples:', list(zip(yr[prev].tolist(), date[prev].tolist(), jul[prev].tolist(), qb[prev].tolist()))[:12])
later = dy > yr
print('dated in a later calendar year:', later.sum(), list(zip(yr[later].tolist(), date[later].tolist(), jul[later].tolist(), qb[later].tolist()))[:12])

# "naive" Jultag hypotheses
cum = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
naive = np.array([cum[m - 1] + d for m, d in zip(mm, dd)])  # non-leap day-of-year
print('Jultag - nonleapDOY (all recs):', sorted(collections.Counter((jul - naive).tolist()).items())[:20])

# the records where date and Jultag disagree under either hypothesis
odd = (diff != 0) & ~(after_feb & (diff == -1))
print('records disagreeing with BOTH true DOY and no-29-Feb DOY:', odd.sum())
for i in np.where(odd)[0][:60]:
    print('   ', R[i].tolist(), 'trueDOY', td[i])
