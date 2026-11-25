# The four-layer search ended with two radii equal to four places; my mesh then has near-zero cells, so re-evaluate it cleanly (merged) and by the author's code.
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/drum/referee'); sys.path.insert(1, '/home/agent2/drum')
import numpy as np
from mem import *
import helpers
a4 = [18.207, 37.439, 18.009, 34.322]; k4 = [0.4611, 0.2498, 0.4498, 0.4611]
rho = lambda r: 1.0 + sum(a * (r < k) for a, k in zip(a4, k4))
print('four-layer search answer, author code N=3000: %.5f ; N=6000: %.5f' % (helpers.tied(helpers.fd_modes(rho, N=3000)), helpers.tied(helpers.fd_modes(rho, N=6000))))
am = [18.207 + 34.322, 18.009, 37.439]; km = [0.4611, 0.4498, 0.2498]
for N in (2000, 4000):
    print('  merged to three radii, referee code N=%d: %.5f' % (N, miss(ratios(layers(am, km), km, N))))
print('  added mass %.2f skins' % sum(a * k * k for a, k in zip(am, km)))
a3 = [35.97, 39.103, 39.994]; k3 = [0.4580, 0.4587, 0.2499]
rho3 = lambda r: 1.0 + sum(a * (r < k) for a, k in zip(a3, k3))
print('three-layer search answer, author code N=3000: %.5f ; N=6000 %.5f ; referee N=4000: %.5f ; added mass %.2f' % (helpers.tied(helpers.fd_modes(rho3, N=3000)), helpers.tied(helpers.fd_modes(rho3, N=6000)), miss(ratios(layers(a3, k3), k3, 4000)), sum(a * k * k for a, k in zip(a3, k3))))
a2 = [39.9809, 20.9575]; k2 = [0.4558, 0.2489]
rho2 = lambda r: 1.0 + sum(a * (r < k) for a, k in zip(a2, k2))
print('two-layer answer, author code N=3000: %.5f ; N=6000: %.5f ; N=12000: %.5f' % tuple(helpers.tied(helpers.fd_modes(rho2, N=n)) for n in (3000, 6000, 12000)))
