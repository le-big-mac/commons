# The meters' profile by the Sun's depth for other stretches of months, by the measure of the ninth sheet (depth.py):
# the mean over a stretch of each month's figure less the same month of 2021 and 2024, at each southern place, and the
# middle over the places. A stretch needs two thirds of its months at a place.
# usage: depth_stretch.py            (prints January to June 2023 and September to November 2023)
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
R = pickle.load(open(B + 'cache2/depth.pkl', 'rb'))
STRETCH = {'January to June 2023': [(2023, m) for m in (1, 2, 3, 4, 5, 6)], 'September to November 2023': [(2023, m) for m in (9, 10, 11)], 'June to August 2022 (the ninth sheet)': [(2022, m) for m in (6, 7, 8)]}
DEPTHS = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
out = {}
for name, months in STRETCH.items():
    print(f'{name}: each southern place, then the middle and how many places (magnitudes; negative: brighter)')
    print('   ' + ' ' * 16 + ''.join(f'{d:7g}°' for d in DEPTHS)); mids = []
    cols = {d: [] for d in DEPTHS}
    for st, pl in DP.SOUTH.items():
        row = []
        for d in DEPTHS:
            a = DP.series(R, st, d)[0]; v = [a[k] for k in months if k in a]; p = float(np.mean(v)) if len(v) >= (2 * len(months) + 2) // 3 else None
            row.append(f'{p:+8.2f}' if p is not None else '       .')
            if p is not None: cols[d].append(p)
        print(f'   {pl:<16}' + ''.join(row))
    print('   the middle      ' + ''.join(f'{np.median(cols[d]):+8.2f}' if cols[d] else '       .' for d in DEPTHS)); print('   places          ' + ''.join(f'{len(cols[d]):8d}' for d in DEPTHS))
    out[name] = {d: (float(np.median(cols[d])) if cols[d] else None, len(cols[d])) for d in DEPTHS}
pickle.dump(out, open(B + 'cache2/depth_stretch.pkl', 'wb'))
