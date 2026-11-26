"""Which months, and is the leftover a drift or a step?   Added 26 November 2026, after a reader's report.
usage: python -I months.py results.npz TEMPDIR > months.out        (numpy)
results.npz is this study's own (the yearly dates, 1951 to 2023, stations and years fitted together). TEMPDIR holds
the weather service's monthly mean temperatures for Germany, regional_averages_tm_MM.txt for MM = 01, 02, 03, 11, 12
(https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly/air_temperature_mean/).
1. The page took January and February. For other choices of months: days per degree, the share of the shift between
   1961-1990 and 1991-2020 that the warming of those months accounts for, and the trend left over.
2. The leftover within 1951-1990 and within 1991-2023.
3. Temperature and a straight drift, against temperature and one step: which leaves less unexplained?"""
import sys
sys.dont_write_bytecode = True
import numpy as np

def monthly(D, m):
    out = {}
    with open(f"{D}/regional_averages_tm_{m:02d}.txt", encoding='latin-1') as f:
        f.readline(); cols = [c.strip() for c in f.readline().split(';')]; k = cols.index('Deutschland')
        for line in f:
            p = line.split(';')
            if len(p) > k and p[0].strip().isdigit(): out[int(p[0])] = float(p[k])
    return out

def ols(X, y):
    X = np.column_stack([np.ones(len(y))] + list(X)); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b; cov = res @ res / (len(y) - X.shape[1]) * np.linalg.inv(X.T @ X)
    return b, b / np.sqrt(np.diag(cov)), float(res @ res)

if __name__ == '__main__':
    r = np.load(sys.argv[1], allow_pickle=True); D = sys.argv[2]
    years, date = r['years'].astype(int), r['yearly2'].astype(float)
    T = {m: monthly(D, m) for m in (1, 2, 3, 11, 12)}
    def window(months):
        """months as (month, year offset): (12, -1) is the December before"""
        return np.array([np.mean([T[m][y + off] for m, off in months]) for y in years])
    W = {'January-February (the page)': [(1, 0), (2, 0)], 'December-February': [(12, -1), (1, 0), (2, 0)], 'January-March': [(1, 0), (2, 0), (3, 0)],
         'December-March': [(12, -1), (1, 0), (2, 0), (3, 0)], 'November-March': [(11, -1), (12, -1), (1, 0), (2, 0), (3, 0)], 'February alone': [(2, 0)]}
    a, b = (years >= 1961) & (years <= 1990), (years >= 1991) & (years <= 2020)
    shift = date[b].mean() - date[a].mean()
    print(f"the yearly date, stations and years fitted together: day {date[a].mean():.1f} in 1961-1990, day {date[b].mean():.1f} in 1991-2020, shift {shift:+.1f} days")
    print("1. by choice of months: correlation; days per degree; warming between the periods; share of the shift; trend left over in days a decade (t)")
    for name, months in W.items():
        t = window(months); warm = t[b].mean() - t[a].mean()
        b1, _, _ = ols([t], date); b2, t2, _ = ols([t, years], date)
        print(f"   {name}: {np.corrcoef(t, date)[0, 1]:+.2f}; {b1[1]:+.2f}; {warm:+.2f} C; {100 * b1[1] * warm / shift:.0f}%; {10 * b2[2]:+.2f} ({t2[2]:.1f})")
    print("   (March is after the typical date, 27 February, so a window that holds it counts warmth that came after most of the flowers)")
    tjf = window(W['January-February (the page)'])
    print("2. January-February temperature and year together, within parts of the record: trend left over in days a decade (t)")
    for lo, hi in ((1951, 2023), (1951, 1990), (1991, 2023), (1951, 1988), (1989, 2023)):
        m = (years >= lo) & (years <= hi); b2, t2, _ = ols([tjf[m], years[m]], date[m])
        print(f"   {lo}-{hi}: {10 * b2[2]:+.2f} ({t2[2]:.1f}), {int(m.sum())} years")
    print("3. what is left unexplained (sum of squared residuals, days squared), January-February temperature with:")
    _, _, r0 = ols([tjf], date); bt, tt, r1 = ols([tjf, years], date)
    print(f"   nothing else {r0:.0f}; a straight drift {r1:.0f} (drift {10 * bt[2]:+.2f} days a decade, t {tt[2]:.1f})")
    best = min(((ols([tjf, (years >= s).astype(float)], date), s) for s in range(1960, 2015)), key=lambda z: z[0][2])
    (bs, ts, rs), s = best
    print(f"   one step, at the best year of 1960 to 2014: {rs:.0f}, a step of {bs[2]:+.1f} days from {s} on (t {ts[2]:.1f}); steps at 1987 to 1991 leave "
          + ", ".join(f"{ols([tjf, (years >= y).astype(float)], date)[2]:.0f}" for y in range(1987, 1992)))
    bb, tb, rb = ols([tjf, years, (years >= s).astype(float)], date)
    print(f"   a drift and that step together: {rb:.0f}; drift {10 * bb[2]:+.2f} (t {tb[2]:.1f}), step {bb[3]:+.1f} (t {tb[3]:.1f})")
    # added after the reader's check of the first corrections (26 November)
    print("4. the months entered separately, each with its own days per degree (a mean of months gives every month the same weight)")
    for name, months in (('December, January, February', [(12, -1), (1, 0), (2, 0)]), ('November to February', [(11, -1), (12, -1), (1, 0), (2, 0)]),
                         ('December to March', [(12, -1), (1, 0), (2, 0), (3, 0)]), ('November to March', [(11, -1), (12, -1), (1, 0), (2, 0), (3, 0)])):
        cols = [window([mo]) for mo in months]
        b1, t1, _ = ols(cols, date); b2, t2, _ = ols(cols + [years], date)
        expl = sum(b1[1 + i] * (c[b].mean() - c[a].mean()) for i, c in enumerate(cols))
        print(f"   {name}: days per degree {', '.join(f'{x:+.2f} (t {tt:.1f})' for x, tt in zip(b1[1:], t1[1:]))}; share of the shift {100 * expl / shift:.0f}%; trend left over {10 * b2[-1]:+.2f} ({t2[-1]:.1f})")
    print("5. would a steady drift look like a step? 1,000 made-up records: the fitted temperature effect and drift, with noise of the size of the residuals")
    rng = np.random.default_rng(1989)
    bt, _, r1 = ols([tjf, years], date); sd = (r1 / (len(date) - 3)) ** 0.5; fit = bt[0] + bt[1] * tjf + bt[2] * years
    gain_here = r1 - min(ols([tjf, (years >= s).astype(float)], date)[2] for s in range(1960, 2015))
    beats = asmuch = 0; where = []
    for _ in range(1000):
        y = fit + rng.normal(0, sd, len(date))
        rd = ols([tjf, years], y)[2]; rs_, s_ = min((ols([tjf, (years >= s).astype(float)], y)[2], s) for s in range(1960, 2015))
        beats += rs_ < rd; asmuch += (rd - rs_) >= gain_here; where.append(s_)
    print(f"   here the best step leaves {gain_here:.0f} days squared less than the drift; in the made-up records the best step beats the drift in {beats / 10:.0f}% and by as much as here in {asmuch / 10:.0f}%")
