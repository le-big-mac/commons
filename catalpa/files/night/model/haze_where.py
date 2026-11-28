# Where the twice-scattered light is first scattered (the sunlit point B), with and without the Hunga layer: the share
# of it that comes from heights of 16 to 26 km, at two wavelengths and three depths. A description of the model.
import importlib.util, numpy as np
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
M = RH.M
for lam in (575, 675):
    A = RH.atms(lam, 21.0, 5.0); hz, base = A[1], A[3]; tabs = (M.sun_table(hz), M.sun_table(base))
    for dep in (4.0, 6.0, 9.0):
        out = []
        for at, tab in ((hz, tabs[0]), (base, tabs[1])):
            tot, zA, prof, byh = M.second(at, dep, tab, nel=64, naz=24, ns=100, detail=True)
            lay = byh[(M.ZC >= 16) & (M.ZC < 26)].sum() / byh.sum(); med = M.ZC[np.searchsorted(np.cumsum(byh), 0.5 * byh.sum())]; medA = zA[np.searchsorted(np.cumsum(prof), 0.5 * prof.sum())]
            out.append((tot, lay, med, medA, byh))
        add = out[0][4] - out[1][4]
        print(f'{lam} nm, {dep:g} degrees: twice-scattered light, with the layer {out[0][0]:.3e}, without {out[1][0]:.3e} (x{out[0][0] / out[1][0]:.2f}); share first scattered at 16 to 26 km: with {out[0][1]:.2f}, without {out[1][1]:.2f}; middle height of the first scattering: with {out[0][2]:.0f} km, without {out[1][2]:.0f} km; middle height of the second scattering, on the line of sight: {out[0][3]:.0f} km and {out[1][3]:.0f} km; of the light the layer adds, the share first scattered at 16 to 26 km: {add[(M.ZC >= 16) & (M.ZC < 26)].sum() / add.sum():.2f}')
