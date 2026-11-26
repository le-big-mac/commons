"""Exact fixation probability of a single mutant in a Moran process with payoff-dependent fitness exp(beta*payoff).
Reported relative to a neutral mutant (rho*N): >1 favoured, <1 opposed. log10 shown when tiny."""
import numpy as np, sys
from ipd import M, payoff
D, BETA = 0.99, 1.0
K = lambda k: M(k, 0, [(s[0], int(s[1]), int(s[2])) for s in k.split(" ")])
SP = {"all-defect": "D00", "tit-for-tat": "C01 D01", "grim": "C01 D11", "echo-once": "D10 C00", "handshake": "D01 D02 C20", "wooer": "C01 D12 D10"}
def log10_rhoN(inv, res, eps, N):
    a = payoff(inv, inv, eps, D)[0]; b, c = payoff(inv, res, eps, D); d = payoff(res, res, eps, D)[0]
    # with j mutants: payoffs (self-interaction included, as in the simulations)
    j = np.arange(1, N)
    fi = (a * j + b * (N - j)) / N; fr = (c * j + d * (N - j)) / N
    lg = np.cumsum(BETA * (fr - fi))                 # log of prod_{k<=j} (f_res/f_inv)
    m = lg.max(); logsum = m + np.log(np.exp(-m) + np.exp(lg - m).sum())   # log(1 + sum exp(lg))
    return (-logsum + np.log(N)) / np.log(10)
def fmt(x): return f"{10**x:6.2f}" if x > -2 else f"1e{x:+.0f}"
for eps in (0.0, 0.01, 0.02, 0.05):
    print(f"\nnoise {eps}:  fixation probability of ONE mutant, relative to neutral drift (rows: population)")
    cols = [("handshake", "all-defect"), ("wooer", "all-defect"), ("tit-for-tat", "all-defect"), ("grim", "all-defect"), ("echo-once", "all-defect"), ("handshake", "echo-once"), ("all-defect", "handshake"), ("all-defect", "tit-for-tat")]
    print("   N   " + "  ".join(f"{i[:9]}>{r[:9]}".rjust(20) for i, r in cols))
    for N in (50, 100, 200, 400, 1000):
        print(f"{N:5d}  " + "  ".join(fmt(log10_rhoN(K(SP[i]), K(SP[r]), eps, N)).rjust(20) for i, r in cols))
