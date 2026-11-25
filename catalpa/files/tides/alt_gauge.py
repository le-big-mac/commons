# How well does the altimetry cell nearest a gauge follow the gauge, October by October?  (A look after alt.py; not sealed.)  Run with python -I.
import numpy as np, csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
def october(y, pts):
    acc = {p: [] for p in pts}
    for line in open(f'{HERE}/alt/sla_{y}10.csv'):
        w = line.strip().split(',')
        if not w[0].startswith(f'{y}-10') or w[3] in ('NaN', ''): continue
        k = (float(w[1]), float(w[2]))
        if k in acc: acc[k].append(float(w[3]))
    return {p: 100 * np.mean(v) for p, v in acc.items()}
def gauge(st):
    M = {}
    for r in csv.reader(open(f'{HERE}/data/{st}_monthly_mean.csv')):
        if r and r[0].strip().isdigit() and int(r[1]) == 10 and r[5].strip() not in ('', 'NaN'): M[int(r[0])] = 100 * float(r[5])
    return M
SETS = (('San Diego', '9410170', [(32.625, -117.125), (32.625, -117.375), (32.625, -117.875), (32.625, -118.875)]), ('San Francisco', '9414290', [(37.625, -122.625), (37.625, -122.875), (37.625, -123.375), (37.625, -124.375)]))
for name, st, pts in SETS:
    M = gauge(st); A = {y: october(y, pts) for y in range(2017, 2027)}; gm = np.mean([M[y] for y in range(2017, 2026)])
    print(f'{name}: each October minus the mean of Octobers 2017-2025, cm.  Columns: gauge; then altimetry cells going seaward along one parallel: ' + ', '.join(f'{-p[1]:.3f}W' for p in pts))
    for y in range(2017, 2027):
        print(f'   {y}   {M[y] - gm:+6.1f}   ' + '   '.join(f'{A[y][p] - np.mean([A[z][p] for z in range(2017, 2026)]):+6.1f}' for p in pts) + f'      gauge minus nearest cell {M[y] - gm - (A[y][pts[0]] - np.mean([A[z][pts[0]] for z in range(2017, 2026)])):+6.1f}')
    d = np.array([M[y] - gm - (A[y][pts[0]] - np.mean([A[z][pts[0]] for z in range(2017, 2026)])) for y in range(2017, 2026)]); gg = np.array([M[y] - gm for y in range(2017, 2026)]); cc = np.array([A[y][pts[0]] - np.mean([A[z][pts[0]] for z in range(2017, 2026)]) for y in range(2017, 2026)])
    print(f'   2017-2025: sd of (gauge minus nearest cell) {d.std():.1f} cm; correlation of gauge with nearest cell {np.corrcoef(gg, cc)[0, 1]:+.2f}; slope of cell on gauge {np.polyfit(gg, cc, 1)[0]:.2f}')
