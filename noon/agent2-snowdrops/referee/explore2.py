import collections, datetime
import numpy as np
from load import *

hdr, R, bad = read_records()
sid, yr, qn, obj, ph, date, qb, jul = R.T
td = np.array([true_doy(int(y), int(d)) for y, d in zip(yr, date)])
dy = date // 10000
mm = (date // 100) % 100
dd = date % 100
leap = np.array([(y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) for y in yr])
diff = jul - td

print('--- leap-year reference years: Jultag - trueDOY by year, for dates on/after 29 Feb (same calendar year)')
for y in sorted(set(yr[leap].tolist())):
    m = (yr == y) & (dy == yr) & ((mm >= 3) | ((mm == 2) & (dd == 29)))
    print(y, sorted(collections.Counter(diff[m].tolist()).items()))
print('--- leap-year reference years: dates up to 28 Feb')
m = leap & (dy == yr) & ((mm == 1) | ((mm == 2) & (dd <= 28)))
print(sorted(collections.Counter(diff[m].tolist()).items()))
print('--- non-leap reference years, same-calendar-year dates')
m = (~leap) & (dy == yr)
print(sorted(collections.Counter(diff[m].tolist()).items()))
print('--- previous-December dates: Jultag - trueDOY, split by whether the PREVIOUS year is leap')
m = dy < yr
print(sorted(collections.Counter(diff[m].tolist()).items()))
for i in np.where(m)[0]:
    pass
print('   all prev-year records month counts:', collections.Counter(mm[m].tolist()))

print('--- anomalies: records where Jultag matches none of {trueDOY, trueDOY-1 for leap after-Feb, trueDOY-1 for December}')
ok = (diff == 0) | (leap & (dy == yr) & (td >= 60) & (diff == -1)) | ((dy < yr) & (diff == -1))
for i in np.where(~ok)[0]:
    print('   ', R[i].tolist(), 'trueDOY', td[i], 'diff', diff[i])
print('--- leap-year after-Feb records where Jultag == trueDOY (i.e. 29 Feb counted): quality fields')
m = leap & (dy == yr) & (td >= 60) & (diff == 0)
print(m.sum(), 'QB', collections.Counter(qb[m].tolist()), 'QN', collections.Counter(qn[m].tolist()))
print('   by year', sorted(collections.Counter(yr[m].tolist()).items()))
print('   QN overall by year for QN!=10:', sorted(collections.Counter(yr[qn != 10].tolist()).items()))
m2 = leap & (dy == yr) & (td >= 60)
print('   leap after-feb by QN: ', {q: (int(((qn == q) & m2).sum()), int(((qn == q) & m2 & (diff == 0)).sum())) for q in (1, 7, 10)})

print('--- QB==5 breakdown: pre-1951', ((qb == 5) & (yr < 1951)).sum(), ' 2024', ((qb == 5) & (yr == 2024)).sum())
print('--- pre-1951 & qb!=5:', ((yr < 1951) & (qb != 5)).sum(), '; 2024 & qb!=5:', ((yr == 2024) & (qb != 5)).sum())
print('--- pre-1951 total', (yr < 1951).sum(), '2024 total', (yr == 2024).sum())
base = (qb != 5) & (yr >= 1951) & (yr <= 2023)
print('after doubtful/pre-1951/2024 removal:', base.sum(), 'stations', len(set(sid[base].tolist())))
print('   of which anomalies (not ok):', (base & ~ok).sum())
print('   of which Dec-before:', (base & (dy < yr)).sum())
print('   jul range', jul[base].min(), jul[base].max(), ' td range', td[base].min(), td[base].max())
# extremes
o = np.argsort(td[base])
B = R[base]
print('   earliest 12:', [(r[0], r[1], r[5], r[7], r[6]) for r in B[o[:12]].tolist()])
print('   latest 25:', [(r[0], r[1], r[5], r[7], r[6]) for r in B[o[-25:]].tolist()])
# histogram by month of kept
print('   month counts:', sorted(collections.Counter(mm[base].tolist()).items()))
