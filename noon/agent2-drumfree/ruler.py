"""The ruler, before the search: three cases whose answers I already had from other code.   usage: python -u ruler.py > ruler.out"""
import json
import numpy as np
import libfree as F
L = F.L
N = 2000; r = (np.arange(N) + 0.5) / N; smooth = (2.57 ** 2 - 1) / 2 * (1 - np.tanh((r - 0.492) / 0.091)); sk = F.FreeSkin(N, F.FIVE, per=1)
print(f"the paper's smooth step (sigma 2.57, k 0.492, xi 0.091): overtone miss {100 * sk.miss(smooth):.2f}%, the lowest mode's place {F.place(smooth, per=1):.4f} (known from ../drum12/smooth.out: within 1.92%, and 1.0995)")
m, pl = F.disc_miss(3.125 ** 2, 0.4, F.FIVE); print(f"the 1954 disc (9.77 times over 0.4), exact: overtone miss {100 * m:.2f}%, place {pl:.4f} (known from ../drum12/composite.out: (2,2) at 5.3128, that is 6.26%; place 1.0326)")
a = np.array(json.load(open("../drum/rings2-free-1.43.json"))['rings']['40']['a']); s40 = F.FreeSkin(40, F.FIVE); ex, pe = F.exact(a, F.FIVE)
print(f"the nine-mode ring load of 1.43 skins: overtone miss {100 * s40.miss(a):.3f}% by finite differences, {100 * ex:.3f}% exact; place {F.place(a):.4f} and {pe:.4f} (its ratios to the lowest were 1.9847, 3.0231, 3.0016, 4.0247, 3.9695, 4.9618, 5.0385, 4.9618: to half the second that is a place of {2 / 1.9847:.4f} and a largest miss of {100 * max(abs(2 * x / 1.9847 / t - 1) for x, t in zip((3.0231, 3.0016, 4.0247, 3.9695, 4.9618, 5.0385, 4.9618), (3, 3, 4, 4, 5, 5, 5))):.3f}%)")
c, J = s40.solve(a); e = np.zeros(40); e[6] = 1e-4; c2 = s40.solve(a + e, grad=False); print(f"derivative of the seven misses with respect to ring 7's load against a finite difference: largest difference {np.abs((c2 - c) / 1e-4 - J[:, 6]).max():.1e}")
