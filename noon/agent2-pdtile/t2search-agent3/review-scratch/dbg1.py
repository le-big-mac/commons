import numpy as np, sys
from fractions import Fraction
from scipy.optimize import linprog
import wt
M=36; A=[0, 1, 2, 3, 4, 5, 6, 8, 21]
B = np.zeros((M + 1, M))
for y in range(M):
    for x in A: B[y, (y - x) % M] += 1
B[M, 0] = 1
r = linprog(-np.ones(M + 1), A_ub=B.T, b_ub=np.zeros(M), bounds=[(-1, 1)] * (M + 1), method="highs")
print(r.status, r.fun); print(np.round(r.x, 6))
for D in (12, 360, 10**4, 10**6):
    wr=[Fraction(float(t)).limit_denominator(D) for t in r.x]
    w, w0 = wr[:M], wr[M]
    viol=[(t, float(sum(w[(t + x) % M] for x in A) + (w0 if t == 0 else 0))) for t in range(M) if sum(w[(t + x) % M] for x in A) + (w0 if t == 0 else 0) > 0]
    print(D, viol[:5], float(sum(w)+w0))
