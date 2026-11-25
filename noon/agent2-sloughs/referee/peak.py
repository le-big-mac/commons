# first peak of S(t) by two readings, on the referee's own base-case runs (S every 0.1 time, and thinned to every 1.0 as Noon samples)
import sys, numpy as np
for fn in sys.argv[1:]:
    a = np.loadtxt(fn, comments="#"); t, S = a[:, 0], a[:, 1]
    T = t[-1]; Sbar = S[t > T / 2].mean()
    for step, lab in ((1, "every 0.1"), (10, "every 1.0")):
        tt, SS = t[step - 1::step], S[step - 1::step]
        run = np.maximum.accumulate(SS); below = np.nonzero(SS < 0.95 * run)[0]
        pk = run[below[0]] if len(below) else run[-1]
        # first local maximum of S (first time S falls at all)
        d = np.nonzero(np.diff(SS) < 0)[0]; first_local = SS[d[0]] if len(d) else SS[-1]
        print("%s %s: S-bar %.3f; peak before first 5%% fall %.3f (x%.2f) at t=%.1f; first local max %.3f (x%.2f) at t=%.1f; max in first tenth %.3f (x%.2f); max in first 100 units %.3f (x%.2f)" % (
            fn, lab, Sbar, pk, pk / Sbar, tt[below[0] - 1] if len(below) else -1, first_local, first_local / Sbar, tt[d[0]] if len(d) else -1,
            SS[tt <= T / 10].max(), SS[tt <= T / 10].max() / Sbar, SS[tt <= 100].max(), SS[tt <= 100].max() / Sbar))
