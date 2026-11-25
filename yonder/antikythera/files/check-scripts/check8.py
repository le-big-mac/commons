"""Circle-fit deferent phase beside the mean heliocentric longitude from conjunction/opposition samples (check1.out), frame S,
at window centre and at the outer edge. Numbers from check1.out typed in."""
import numpy as np, os
Z = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fits-S.npz'))
H = {'mars': {'then': (206.5052, 0.524033015), 'now': (29.7025, 0.524032912)},
     'jupiter': {'then': (189.6458, 0.083095173), 'now': (57.3622, 0.083084166)},
     'saturn': {'then': (222.9218, 0.033450205), 'now': (274.1795, 0.033479770)}}
wrap = lambda x: (x + 180) % 360 - 180
DR = {'mars': 4.720, 'jupiter': -1.438, 'saturn': -9.888}
for p in H:
    b = {}
    for w, half in (('then', -13879.5), ('now', 13879.5)):
        p0, r = float(Z[f'{w}_{p}_p0']), float(Z[f'{w}_{p}_r']); L0, rr = H[p][w]
        b[w] = (wrap(p0 - L0), wrap(p0 + r * half - (L0 + rr * half)))
        print(f'{p:8s} {w:5s} circle fit minus mean longitude: centre {b[w][0]:+.3f}, outer edge {b[w][1]:+.3f}')
    print(f'{p:8s} drift {DR[p]:+.2f} + bias then (edge) {b["then"][1]:+.2f} - bias now (edge) {b["now"][1]:+.2f} = {DR[p] + b["then"][1] - b["now"][1]:+.2f}  (after2.out "phase": mars +4.32, jupiter -1.69, saturn -7.74)')
