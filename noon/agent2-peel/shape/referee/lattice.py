# last step: what counting in whole layers does to the variance: Y = round(X), X normal with the count's own mean
import math
def mom(mu, s2):
    s = math.sqrt(s2); ks = range(int(mu) - 12, int(mu) + 13)
    p = [0.5 * (math.erf((k + 0.5 - mu) / (s * math.sqrt(2))) - math.erf((k - 0.5 - mu) / (s * math.sqrt(2)))) for k in ks]
    m = sum(k * q for k, q in zip(ks, p)); v = sum((k - m) ** 2 * q for k, q in zip(ks, p)); m3 = sum((k - m) ** 3 * q for k, q in zip(ks, p)); m4 = sum((k - m) ** 4 * q for k, q in zip(ks, p))
    return m, v, m3 / v ** 1.5, m4 / v ** 2 - 3
def solve(mean, var):
    mu, s2 = mean, max(var - 1 / 12, 0.01)
    for it in range(200):
        m, v, sk, ku = mom(mu, s2); mu += mean - m; s2 = max(s2 + (var - v), 1e-4)
    return mu, s2, mom(mu, s2)
print('size  count mean  count var   latent var   var - latent - 1/12 (the lattice term)   skew, kurtosis of the rounded normal   measured skew')
for N, mean, var, sk in ((16, 3.1148, 0.13494, None), (25, 4.1464, 0.18428, None), (40, 5.6175, 0.27207, None), (64, 7.6024, 0.30910, None), (100, 10.1648, 0.33863, 0.122), (300, 20.9360, 0.51067, 0.036),
                         (1000, 46.4980, 0.77769, 0.034), (3000, 96.5521, 1.13945, 0.027), (10000, 215.2815, 1.72297, 0.018)):
    mu, s2, (m, v, s, k) = solve(mean, var)
    print('%6d  %9.4f  %.5f    %.5f      %+.5f                                   %+.3f, %+.3f                       %s' % (N, mean, var, s2, var - s2 - 1 / 12, s, k, sk))
