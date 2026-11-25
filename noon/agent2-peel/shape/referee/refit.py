# last step: the eight-size fits again with the whole-number lattice term taken off the 100- and 300-point variances
import numpy as np, math
N = np.array([100, 300, 1000, 3000, 10000, 30000, 100000, 300000.])
V = np.array([0.33863, 0.51067, 0.77769, 1.13945, 1.72297, 2.51300, 3.76588, 5.46366]); E = np.array([0.00079, 0.00114, 0.00174, 0.00254, 0.00385, 0.00561, 0.00974, 0.01990])
def fit(V, sel, cols):
    X = np.column_stack([c(N[sel]) for c in cols]); W = 1 / E[sel] ** 2; C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * V[sel])); return b, np.sqrt(np.diag(C)), (W * (V[sel] - X @ b) ** 2).sum()
c13 = lambda n: n ** (1 / 3); one = lambda n: np.ones(len(n))
for nm, VV in (('as measured', V), ('lattice term off (+0.00345 at 100, +0.00036 at 300)', V + np.array([0.00345, 0.00036, 0, 0, 0, 0, 0, 0]))):
    sel = list(range(8)); b, sb, chi = fit(VV, sel, [c13, one])
    ps = [p for p in np.arange(-0.4, 0.3001, 0.005) if abs(p - 1 / 3) > 0.03]; ch = np.array([fit(VV, sel, [c13, lambda n, p=p: n ** p])[2] for p in ps]); i = ch.argmin()
    ok = [p for p, c in zip(ps, ch) if c <= ch[i] + 1]; ok4 = [p for p, c in zip(ps, ch) if c <= ch[i] + 4]; bb = fit(VV, sel, [c13, lambda n: n ** ps[i]])
    print('%s:\n   c n^(1/3) + b: c = %.5f (%.5f), b = %+.4f (%.4f), chi2 %.1f on 6; B(100) - B(1000) = %+.4f\n   power free: lean as n^(%.2f) (within 1: %.2f to %.2f; within 4: %.2f to %.2f), chi2 %.1f on 5; a constant is %.1f above the least; c at best %.5f = %.4f of the theory' % (
        nm, b[0], sb[0], b[1], sb[1], chi, (VV[0] - 0.08227 * 100 ** (1 / 3)) - (VV[2] - 0.08227 * 10), ps[i] - 1 / 3, min(ok) - 1 / 3, max(ok) - 1 / 3, min(ok4) - 1 / 3, max(ok4) - 1 / 3, ch[i], chi - ch[i], bb[0][0], bb[0][0] / 0.08068))
