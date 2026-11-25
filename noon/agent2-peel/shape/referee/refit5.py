# fifth sheet: the fits of (c) again without the 100-point file, and with the term's size left free
import numpy as np, math
six = [(83, 0.31302, 0.00110, -0.00992), (90, 0.34100, 0.00094, 0.00833), (98, 0.33325, 0.00114, -0.00732), (105, 0.35723, 0.00102, 0.00621), (113, 0.35693, 0.00119, -0.00525), (120, 0.37302, 0.00109, 0.00415)]
e8 = [(100, 0.33863, 0.00079, -0.00345), (300, 0.51067, 0.00114, -0.00036), (1000, 0.77769, 0.00174, 0), (3000, 1.13945, 0.00254, 0), (10000, 1.72297, 0.00385, 0), (30000, 2.51300, 0.00561, 0), (100000, 3.76588, 0.00974, 0), (300000, 5.46366, 0.01990, 0)]
def run(data, name):
    N = np.array([d[0] for d in data], float); V = np.array([d[1] - d[3] for d in data]); E = np.array([d[2] for d in data]); W = 1 / E ** 2
    def fit(cols):
        X = np.column_stack([c(N) for c in cols]); C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * V)); return b, np.sqrt(np.diag(C)), (W * (V - X @ b) ** 2).sum()
    b, sb, chi = fit([lambda n: n ** (1 / 3), lambda n: np.ones(len(n))])
    ps = [p for p in np.arange(-0.4, 0.3001, 0.005) if abs(p - 1 / 3) > 0.03]; ch = np.array([fit([lambda n: n ** (1 / 3), lambda n, p=p: n ** p])[2] for p in ps]); i = ch.argmin(); ok4 = [p for p, c in zip(ps, ch) if c <= ch[i] + 4]
    b3, sb3, chi3 = fit([lambda n: n ** (1 / 3), lambda n: np.ones(len(n)), lambda n: n ** (-1 / 3)])
    print('%-34s constant: c %.5f (%.5f) b %+.4f (%.4f) chi2 %.1f on %d | free power %.2f (within 4: %.2f to %.2f) chi2 %.1f on %d | with e n^(-1/3): c %.5f b %+.4f (%.4f) e %+.3f (%.3f) chi2 %.1f on %d' % (
        name, b[0], sb[0], b[1], sb[1], chi, len(N) - 2, ps[i] - 1 / 3, min(ok4) - 1 / 3, max(ok4) - 1 / 3, ch[i], len(N) - 3, b3[0], b3[1], sb3[1], b3[2], sb3[2], chi3, len(N) - 3))
run(six + e8, 'fourteen sizes'); run(six + e8[1:], 'thirteen, without the 100 file'); run(six + e8[1:5], '83 to 10,000 without the 100 file'); run(six + e8[1:3], '83 to 1,000 without the 100 file')
