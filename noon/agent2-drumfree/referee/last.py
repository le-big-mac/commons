import sys, json
sys.path.insert(0, "/home/agent2/drumfree/referee")
import numpy as np
from sol import *
B = json.load(open('/home/agent2/drumfree/best.json'))
a = np.array(B['five|4|40']['a'])
fem = Fem(1600); rng = np.random.default_rng(1)
def miss(a):
    return np.abs(misses(fem_freqs(fem, np.repeat(1 + a, 40)))[0]).max()
v = [miss(a * (1 + 0.01 * rng.standard_normal(40))) for _ in range(200)]
print('five|4|40 with each ring load off by 1%% (sd), 200 draws, FEM 1600: median %.3f%%, as found %.3f%%' % (100 * np.median(v), 100 * miss(a)))
# Raman fit point
ram = {(0,1):1.03,(2,1):3.00,(0,2):3.00,(3,1):4.00,(1,2):4.00,(0,3):5.04,(4,1):5.03,(2,2):5.08}
for nm_, s, k in [('6.426 over 0.4413', 6.426, 0.4413), ('9.77 over 0.4', 9.77, 0.4)]:
    f = exact_freqs([k, 1.0], [s, 1.0]); note = f[(1, 1)] / 2
    print(nm_, 'largest relative difference from Raman\'s eight: %.3f%%' % (100 * max(abs(f[m] / note / r - 1) for m, r in ram.items())))
# ratios as printed
t5 = [5.67,4.21,2.89,1.73,0.77,0.71,0.64,0.61,0.58,0.55,0.53]; f5 = [0.757,0.464,0.295,0.170,0.104,0.102,0.091,0.079,0.071,0.064,0.058]
f80 = [0.753,0.461,0.271,0.129,0.099,0.098,0.086,0.076,0.067,0.061,0.056]
print('five, 40 rings, tuned/free from printed digits:', ' '.join('%.2f' % (x / y) for x, y in zip(t5, f5)))
print('five, 80 rings free:', ' '.join('%.2f' % (x / y) for x, y in zip(t5, f80)))
print('cents for 0.071%%: %.3f' % (1200 * np.log2(1.00071)))
print('two discs: mean density over the patch %.2f; inner disc area share %.3f; outer %.3f; sigma of outer %.4f' % ((8.120 * 0.2768**2 + 6.304 * (0.4933**2 - 0.2768**2)) / 0.4933**2, 0.2768**2, 0.4933**2, 6.304**0.5))
