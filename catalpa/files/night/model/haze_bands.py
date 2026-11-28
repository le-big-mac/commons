# The sealed run again with other weights across the colours. No new run: the stored results by wavelength are summed
# with (a) the weights of the sealed sheet (the sensor's response as I had it from memory), (b) the TESS-W's response
# as its makers print it (Zamorano and others 2016, Figure 3, panel 3: read from the figure by eye, good to about
# 0.03), (c) the response of the other make of sky meter, the SQM, from the same figure.
# The readings from the figure, by 50 nm bins centred on 425 ... 725 nm, relative:
import sys, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
RC = RH.RC; LAMS = RH.LAMS; DEPTHS = RH.DEPTHS
SETS = {'sealed (from memory)': RC.RESP,
        'TESS-W as printed, my reading by eye': {425: 0.58, 475: 0.68, 525: 0.77, 575: 0.82, 625: 0.90, 675: 0.96, 725: 0.75},
        'SQM as printed, my reading by eye': {425: 0.47, 475: 0.61, 525: 0.67, 575: 0.52, 625: 0.25, 675: 0.04, 725: 0.0},
        # the same figure read by program from the PDF's own bitmap by the checker, before it had seen my readings (check/fig3_blind.txt)
        'TESS-W as printed, the checker\'s blind reading': {425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768},
        'SQM as printed, the checker\'s blind reading': {425: 0.472, 475: 0.597, 525: 0.673, 575: 0.479, 625: 0.120, 675: 0.009, 725: 0.006}}
OBS = {3: -0.034, 4: -0.157, 5: -0.214, 6: -0.302, 7: -0.454, 8: -0.654, 9: -0.801, 10: -0.824, 11: -0.834}
ORD = {3: 9.28, 4: 10.40, 5: 11.72, 6: 13.08, 7: 14.39, 8: 15.62, 9: 16.58, 10: 17.54, 11: 18.46}
def tot(R, d, i, resp):
    return sum(RC.SUN[l] * resp[l] * (R[(l, d)]['L1'][i] + R[(l, d)]['L2'][i] + R[(l, d)]['L3'][:, i].mean()) for l in LAMS)
for fn in sys.argv[1:]:
    X = pickle.load(open(fn, 'rb')); R = X['R']; print(f"run {fn.split('/')[-1]}: layer {X['kw']}")
    for name, resp in SETS.items():
        print(f'  weights: {name}')
        print('     depth   plume 0.022  0.018  0.014   meters   |  the ordinary twilight below 3 degrees: model, meters')
        base = None; n15 = 0
        for d in DEPTHS:
            t = [tot(R, d, i, resp) for i in range(4)]; dm = [-2.5 * np.log10(t[i] / t[3]) for i in range(3)]; m = -2.5 * np.log10(t[3]); base = m if base is None else base
            n15 += (4 <= d <= 10) and abs(dm[1] - OBS[d]) <= 0.15
            print(f'     {d:2d}°     {dm[0]:+.2f}  {dm[1]:+.2f}  {dm[2]:+.2f}    {OBS[d]:+.2f}    |   {m - base:5.2f}  {ORD[d] - ORD[3]:5.2f}')
        print(f'     the central case within 0.15 of the meters at {n15} of the seven depths from 4 to 10 degrees')
