# The two model runs made after the fifteenth sheet was scored (model/after_years.md says what was run and what I
# guessed before): a layer like Raikoke's (model/haze_raikoke.pkl) and one like Ruang's (model/haze_ruang.pkl),
# summed over the colours with the first make's response as its makers print it (the checker's blind reading).
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('run_haze', B + 'model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
RESP = {425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768}
def tot(R, d, i): return sum(RH.RC.SUN[l] * RESP[l] * (R[(l, d)]['L1'][i] + R[(l, d)]['L2'][i] + R[(l, d)]['L3'][:, i].mean()) for l in RH.LAMS)
def err(R, d, i):          # the Monte Carlo's own error on the change, from its batches (the higher orders only)
    b = np.array([sum(RH.RC.SUN[l] * RESP[l] * R[(l, d)]['L3'][k, i] for l in RH.LAMS) for k in range(R[(RH.LAMS[0], d)]['L3'].shape[0])])
    b0 = np.array([sum(RH.RC.SUN[l] * RESP[l] * R[(l, d)]['L3'][k, 3] for l in RH.LAMS) for k in range(R[(RH.LAMS[0], d)]['L3'].shape[0])])
    return 2.5 / np.log(10) * float(np.std(b - b0 * (tot(R, d, i) / tot(R, d, 3)), ddof=1) / np.sqrt(len(b)) / tot(R, d, i))
D = [d for d in RH.DEPTHS if 3 <= d <= 9]
for name, fn in (("a layer like Raikoke's", 'model/haze_raikoke.pkl'), ("a layer like Ruang's", 'model/haze_ruang.pkl')):
    X = pickle.load(open(B + fn, 'rb')); R = X['R']; kw = X['kw']
    print(f"{name}: centred at {kw['z0']:g} km, {kw['fwhm']:g} km wide; droplets {kw['PLUME']}; the comparison years' haze {kw['BG']}; {X['N']} paths a case")
    print('   amount at 550 nm   ' + ''.join(f'{d:7g}°' for d in D) + '    | the same counted from 3 degrees, at 7, 8 and 9 degrees')
    for i in range(3):
        v = {d: -2.5 * np.log10(tot(R, d, i) / tot(R, d, 3)) for d in D}
        print(f"   {kw['TAUS'][i]:<18g}" + ''.join(f'{v[d]:+8.2f}' for d in D) + '    | ' + ', '.join(f'{v[d] - v[3]:+.2f}' for d in (7, 8, 9)) + f'   (Monte Carlo error at 7 degrees about {err(R, 7, i):.3f})')
