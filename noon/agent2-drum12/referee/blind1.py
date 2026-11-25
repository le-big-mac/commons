import sys; sys.path.insert(0, "/home/agent2/drum12/referee")
import numpy as np, time
from scipy.special import jn_zeros
import sol
modes = sol.fam_modes(7)
t = time.time()
om = sol.freqs(np.array([1.0]), np.array([1.0]), sol.need_of(modes), p=1600)
omx = sol.freqs(np.array([0.5, 1.0]), np.array([1.0, 1.0]), sol.need_of(modes), p=800, exact=True)
print("# plain skin, sixteen ratios: mode family  bessel-zero ratio | FEM(1600) | my shooting")
for (m, n, f) in modes:
    z = jn_zeros(m, n)[-1] / jn_zeros(0, 1)[0]
    print("(%d,%d) fam %d  %.5f  %.5f  %.5f   miss %+.2f%%" % (m, n, f, z, om[(m, n)] / om[(0, 1)], omx[(m, n)] / omx[(0, 1)], 100 * (z / f - 1)))
print("# time", time.time() - t)
