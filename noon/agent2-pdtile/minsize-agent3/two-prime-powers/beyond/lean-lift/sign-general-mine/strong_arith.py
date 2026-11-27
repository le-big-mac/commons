"""My own check of the arithmetic of the counterexample to the strong form (section 5.2 of sign-general-result.md), in exact
integers, from the text: the two products, e, the weights, that none is negative, the class counts for each of the nine primes
(counted from the weights and the numbers of points with a given zero set), the number of elements for m = 1 and m = 3, their
divisibility by 103 and by 7735396963941761, both n, and how often an hour of the clock is marked when r = 103."""
from math import prod
from itertools import combinations
P = [3, 5, 7, 11, 13, 17, 19, 23, 29]; q = [p - 1 for p in P]
Pi = prod(P); Q = prod(q); e = sum(Pi // p for p in P) - Pi
print('Pi =', Pi, ' Q =', Q, ' e =', e, ' (e > 0:', e > 0, '; without 29:', sum((Pi // 29) // p for p in P[:-1]) - Pi // 29, ')')
def weights(m):
    w = {}
    for i in range(1, 8): w[(i,)] = m * q[i] * (Pi // P[i])
    w[(0,)] = m * q[0] * (Pi // P[0] - e); w[(8,)] = m * q[8] * (Pi // P[8] - e); w[(0, 8)] = m * q[0] * q[8] * e
    return w                                    # weight of each point whose zero set is the key; the point 0 has weight 2
for m in (1, 3):
    w = weights(m); assert all(v > 0 for v in w.values())
    npoints = {Z: prod(q[j] for j in range(9) if j not in Z) for Z in w}          # points with zero set exactly Z
    N = 2 + sum(w[Z] * npoints[Z] for Z in w)
    ok = True
    for i in range(9):
        u = m * Q * Pi // P[i]
        zero = 2 + sum(w[Z] * npoints[Z] for Z in w if i in Z)
        other = sum(w[Z] * npoints[Z] // q[i] for Z in w if i not in Z)            # elements with x_i = one given nonzero value
        ok &= (zero == u + 2 and other == u)
    print(f'm = {m}: number of elements N = {N} = 2 + m Q Pi: {N == 2 + m * Q * Pi}; for every one of the nine primes the class 0 holds u + 2 and every other class u: {ok}; largest weight {max(w.values())}, smallest {min(w.values())}')
    for r in (103, 641, 7735396963941761): print(f'    N mod {r} = {N % r}')
w = weights(1); N1 = 2 + 1 * Q * Pi
print('r = 103: n =', Pi * 103, '; N/103 =', N1 // 103, 'elements in each class modulo 103; a point of weight w is spread over the 103 classes, so an hour of the clock is marked about w/103 times: from about', min(w.values()) // 103, 'to about', max(w.values()) // 103, '(and the two elements over the point 0 once each)')
print('m = 3, r = 7735396963941761: n =', Pi * 7735396963941761, '; largest weight', max(weights(3).values()), '< r:', max(weights(3).values()) < 7735396963941761)
