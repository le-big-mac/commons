# What the Hunga layer changes in the model, part by part: light scattered once, twice, three times and more, at each
# depth (the band's weighted sums), the central case against the comparison years. And by wavelength.
import sys, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
X = pickle.load(open(sys.argv[1], 'rb')); R = X['R']; LAMS = RH.LAMS; DEPTHS = RH.DEPTHS
print(f"layer {X['kw']}; central case (plume 0.018 at 550 nm) against no plume")
print('depth   once: ratio   twice: ratio   three times and more: ratio   |  share of the comparison-year light: once, twice, more  |  of the added light: once, twice, more')
for d in DEPTHS:
    b = [RH.band(R, d, 3, p) for p in ('L1', 'L2', 'L3')]; h = [RH.band(R, d, 1, p) for p in ('L1', 'L2', 'L3')]; tb = sum(b); add = [h[i] - b[i] for i in range(3)]; ta = sum(add)
    print(f'  {d:2d}°    {h[0] / b[0]:6.3f}        {h[1] / b[1]:6.3f}          {h[2] / b[2]:6.3f}                |  {b[0] / tb:.2f} {b[1] / tb:.2f} {b[2] / tb:.2f}   |  ' + (f'{add[0] / ta:+.2f} {add[1] / ta:+.2f} {add[2] / ta:+.2f}' if abs(ta) > 0.02 * tb else '(no change to speak of)'))
print('\nthe brightening by wavelength, central case (magnitudes)')
print('        ' + ''.join(f'{l:8d}' for l in LAMS))
for d in DEPTHS:
    row = []
    for l in LAMS:
        r = R[(l, d)]; t1 = r['L1'][1] + r['L2'][1] + r['L3'][:, 1].mean(); t0 = r['L1'][3] + r['L2'][3] + r['L3'][:, 3].mean(); row.append(-2.5 * np.log10(t1 / t0))
    print(f'  {d:2d}°   ' + ''.join(f'{v:+8.2f}' for v in row))
print('\nthe twice-scattered light with the plume, central case: direct sums against the Monte Carlo on the same atmosphere (band sums)')
for d in DEPTHS: print(f'  {d:2d}°   {RH.band(R, d, 1, "L2"):.3e}   {RH.band(R, d, 1, "L2mc"):.3e}   ratio {RH.band(R, d, 1, "L2mc") / RH.band(R, d, 1, "L2"):.3f}')
print('\nthe ordinary twilight in this run (no plume): magnitudes below 3 degrees, beside the meters')
OBS = {3: 9.28, 4: 10.40, 5: 11.72, 6: 13.08, 7: 14.39, 8: 15.62, 9: 16.58, 10: 17.54, 11: 18.46}; base = None
for d in DEPTHS:
    t = sum(RH.band(R, d, 3, p) for p in ('L1', 'L2', 'L3')); m = -2.5 * np.log10(t); base = m if base is None else base
    print(f'  {d:2d}°   model {m - base:5.2f}   meters {OBS[d] - OBS[3]:5.2f}')
