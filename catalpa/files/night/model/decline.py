# The lines of the twelfth sheet: the model with the haze of 2023 (as the print gives it) against the meters of 2023.
# Reads the two model runs (model/haze_2023a.pkl: January to June 2023; model/haze_2023b.pkl: September to November 2023),
# summed over the colours with the meter's response as its makers print it (the checker's blind reading), and the
# meters' stretches (cache2/depth_stretch.pkl, written by src/depth_stretch.py).
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('run_haze', B + 'model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
RESP = {425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768}
def tot(R, d, i): return sum(RH.RC.SUN[l] * RESP[l] * (R[(l, d)]['L1'][i] + R[(l, d)]['L2'][i] + R[(l, d)]['L3'][:, i].mean()) for l in RH.LAMS)
def rows(fn):
    X = pickle.load(open(B + fn, 'rb')); R = X['R']; return X['kw'], {i: {d: -2.5 * np.log10(tot(R, d, i) / tot(R, d, 3)) for d in RH.DEPTHS} for i in range(3)}
M = pickle.load(open(B + 'cache2/depth_stretch.pkl', 'rb')); D = [4, 5, 6, 7, 8, 9]
CHK = {4: -0.06, 5: -0.09, 6: -0.15, 7: -0.28, 8: -0.39, 9: -0.46}       # the checker's figures for January to June 2023 (its seventh report), ten places
kwa, A = rows('model/haze_2023a.pkl'); kwb, Bm = rows('model/haze_2023b.pkl')
ma = M['January to June 2023']; mb = M['September to November 2023']
print(f"January to June 2023. Model: the layer {kwa['z0']} km, plume {kwa['TAUS']} (the middle one is the sheet's)")
print('   depth    model: high, central, low     meters (mine; places)    meters (the checker\'s)')
for d in D: print(f"   {d}°      {A[0][d]:+.2f}  {A[1][d]:+.2f}  {A[2][d]:+.2f}          {ma[float(d)][0]:+.2f} ({ma[float(d)][1]})              {CHK[d]:+.2f}")
print(f"September to November 2023. Model: the layer {kwb['z0']} km, plume {kwb['TAUS']}")
for d in D: print(f"   {d}°      {Bm[0][d]:+.2f}  {Bm[1][d]:+.2f}  {Bm[2][d]:+.2f}          {mb[float(d)][0]:+.2f} ({mb[float(d)][1]})")
print('\nThe lines of the twelfth sheet (unrounded figures; marks included)')
print(f"D1. the model for January to June 2023 at 8 degrees between -0.20 and -0.45: {A[1][8]:+.3f}: {'held' if -0.45 <= A[1][8] <= -0.20 else 'failed'}")
n = sum(1 for d in D if abs(A[1][d] - ma[float(d)][0]) <= 0.12); print(f"D2. that model within 0.12 of the meters at four or more of the six depths from 4 to 9 degrees: {n} of 6: {'held' if n >= 4 else 'failed'}")
ok = all(abs(mb[float(d)][0]) <= 0.10 for d in (4, 5, 6, 7, 8)); print(f"D3. the meters of September to November 2023 within 0.10 of nothing at every depth from 4 to 8 degrees: {', '.join(f'{mb[float(d)][0]:+.2f}' for d in (4, 5, 6, 7, 8))}: {'held' if ok else 'failed'}")
print(f"D4. the meters of September to November 2023 at 9 degrees at -0.15 or above: {mb[9.0][0]:+.3f}: {'held' if mb[9.0][0] >= -0.15 else 'failed'}")
print(f"D5. the model for September to November 2023 at -0.10 or above at 7 degrees and at -0.20 or above at 9: {Bm[1][7]:+.3f}, {Bm[1][9]:+.3f}: {'held' if Bm[1][7] >= -0.10 and Bm[1][9] >= -0.20 else 'failed'}")
n = sum(1 for d in D if abs(Bm[1][d] - mb[float(d)][0]) <= 0.12); print(f"D6. that model within 0.12 of the meters at four or more of the six depths: {n} of 6: {'held' if n >= 4 else 'failed'}")
