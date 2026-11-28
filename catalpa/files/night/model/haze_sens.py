# The runs made after the sealed one, each with one input changed: the brightening by depth, summed over the colours with
# the meter's response as its makers print it (the checker's blind reading of their figure). Magnitudes, negative for
# a brighter twilight. Beyond 9 degrees the higher orders come from a Monte Carlo that is not to be trusted.
import sys, os, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
RESP = {425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768}
OBS = {3: -0.034, 4: -0.157, 5: -0.214, 6: -0.302, 7: -0.454, 8: -0.654, 9: -0.801, 10: -0.824, 11: -0.834}
def tot(R, d, i): return sum(RH.RC.SUN[l] * RESP[l] * (R[(l, d)]['L1'][i] + R[(l, d)]['L2'][i] + R[(l, d)]['L3'][:, i].mean()) for l in RH.LAMS)
def row(R, i): return [-2.5 * np.log10(tot(R, d, i) / tot(R, d, 3)) for d in RH.DEPTHS]
B = '/home/agent1/night/model/'
CASES = [('haze_central.pkl', 1, 'the sealed inputs (plume 0.018 at 21 km, median radius 0.35)'), ('haze_central.pkl', 2, 'plume 0.014'), ('haze_central.pkl', 0, 'plume 0.022'),
         ('haze_tau.pkl', 1, 'plume 0.010'), ('haze_tau.pkl', 2, 'plume 0.007'), ('haze_tau.pkl', 0, 'plume 0.028'),
         ('haze_z195.pkl', 1, 'the layer at 19.5 km'), ('haze_z225.pkl', 1, 'the layer at 22.5 km'),
         ('haze_r030.pkl', 1, 'droplets of median radius 0.30'), ('haze_r040.pkl', 1, 'droplets of median radius 0.40'),
         ('haze_bg17.pkl', 1, 'the comparison years\' haze centred at 17 km'), ('haze_bg21.pkl', 1, 'the comparison years\' haze centred at 21 km')]
rows = ['<tr><th>the Sun below the horizon, degrees</th>' + ''.join(f'<th class="n">{d}</th>' for d in RH.DEPTHS if d <= 9) + '</tr>', '<tr><td>the meters, June to August 2022</td>' + ''.join(f'<td class="n">{OBS[d]:+.2f}</td>'.replace('-', '−') for d in RH.DEPTHS if d <= 9) + '</tr>']
print('                                                              ' + ''.join(f'{d:6d}°' for d in RH.DEPTHS) + '   largest difference from the meters, 4 to 9 degrees')
print(f"{'the meters (ninth sheet)':<62}" + ''.join(f'{OBS[d]:+7.2f}' for d in RH.DEPTHS))
for fn, i, name in CASES:
    if not os.path.exists(B + fn): print(f'{name:<62}  (not run yet)'); continue
    X = pickle.load(open(B + fn, 'rb')); r = row(X['R'], i); dif = max(abs(r[k] - OBS[d]) for k, d in enumerate(RH.DEPTHS) if 4 <= d <= 9)
    print(f'{name:<62}' + ''.join(f'{v:+7.2f}' for v in r) + f'   {dif:.2f}   ({X["N"]} photons)')
    rows.append(f'<tr><td>the model: {name}</td>' + ''.join(f'<td class="n">{v:+.2f}</td>'.replace('-', '−') for v, d in zip(r, RH.DEPTHS) if d <= 9) + '</tr>')
open('/home/agent1/night/t_model_sens.html', 'w', encoding='utf-8').write('<div class="tablewrap"><table>\n' + '\n'.join(rows) + '\n</table></div>\n')
