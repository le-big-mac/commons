"""dtheory.py: what the equation of the addition (far/) says about a disc, with nothing fitted.   python -I dtheory.py
A disc of radius 1 holding n points, density rho = n / pi. At radius r the cell problem's units are a = (r / rho)^(1/3) along the
front and b = a^2 / r across it. Write T(r, theta) for the depth. The equation dT/dy = (1/3) T_xx + noise of strength D, in those
units and with the distance in from the rim for the height, becomes
        dT / d(-r) = (1 / (3 r)) d^2 T / d theta^2 + noise of strength D rho^(1/3) r^(-1/3) (for each unit of angle and of radius).
So the part of T that goes as cos(m theta) or sin(m theta) falls as r^(m^2 / 3) on the way in (m = 1 is the front shifted bodily,
m = 2 the front squeezed to an ellipse: both are exact symmetries of the flow, and this is what they give), and gathers noise:
        mean square of the m-th part  =  (D rho^(1/3) / (2 pi)) x g_m(r),   g_m(r) = (3/2) (r^(2/3) - r^(2 m^2 / 3)) / (m^2 - 1),
        g_1(r) = r^(2/3) ln(1/r),   g_0(r) = (3/2) (1 - r^(2/3)).
m = 0 is the mean depth round the ring; the variance of depth round a ring about its own mean is twice the sum over m >= 1.
For clouds whose number of points is left to chance that is all. For clouds of exactly n points, the part of D that is the count
of points, (4/9) alpha^2, is changed in the ring's mean only: a point at radius s adds c s^(-2/3) to the depth of every ring inside
it, and n such points, independent but for their number, give the covariance n c^2 [3 (1 - s^(2/3)) - (9/4) u(r1) u(r2)], where s
is the larger of r1 and r2 and u(r) = 1 - r^(4/3), in place of n c^2 x 3 (1 - s^(2/3)); and n c^2 = D_count rho^(1/3) / (4 pi)."""
import math
ALPHA = 1.3259; D = 1.081; DC = 4 / 9.0 * ALPHA ** 2; DR = D - DC       # the noise (far/after.out, with its two corrections), its part that is the count of points, the rest
HALF = 0.008                                                            # an annulus is r - HALF to r + HALF
def tau(r): return 1 - r ** (2 / 3.0)
def u(r): return 1 - r ** (4 / 3.0)
def S(n): return 3 / (4 * math.pi) * math.pi ** (-1 / 3.0) * n ** (1 / 3.0)            # (3 / (4 pi)) rho^(1/3)
def cov_chance(r1, r2, n, d=D): return S(n) * d * tau(max(r1, r2))
def cov_fixed(r1, r2, n, d=D, dc=DC): return S(n) * ((d - dc) * tau(max(r1, r2)) + dc * (tau(max(r1, r2)) - 0.75 * u(r1) * u(r2)))
def annulus(cov, r1, r2, n, half=HALF, k=40, **kw):
    """the covariance of the means over two annuli (points uniform in area: weight r)"""
    def grid(r): xs = [r - half + (i + 0.5) * 2 * half / k for i in range(k)]; w = [x for x in xs]; t = sum(w); return xs, [x / t for x in w]
    x1, w1 = grid(r1); x2, w2 = grid(r2)
    return sum(a * b * cov(p, q, n, **kw) for p, a in zip(x1, w1) for q, b in zip(x2, w2))
def g(m, r):
    if m == 0: return 1.5 * (1 - r ** (2 / 3.0))
    if m == 1: return r ** (2 / 3.0) * math.log(1 / r)
    return 1.5 * (r ** (2 / 3.0) - r ** (2 * m * m / 3.0)) / (m * m - 1)
def mode(m, r, n, d=D): return d * (n / math.pi) ** (1 / 3.0) / (2 * math.pi) * g(m, r)
def local(r, n, d=D, mmax=4000):
    s = sum(g(m, r) for m in range(1, mmax + 1)); s += 1.5 * r ** (2 / 3.0) * (1.0 / mmax)       # the tail: sum of 1/(m^2 - 1) beyond mmax is about 1/mmax
    return 2 * d * (n / math.pi) ** (1 / 3.0) / (2 * math.pi) * s
if __name__ == '__main__':
    print('D = %.3f, of which the count of points %.3f and the rest %.3f; (3 / (4 pi)) pi^(-1/3) = %.4f' % (D, DC, DR, S(1)))
    n = 10 ** 6
    print('n = 10^6. The variance, from cloud to cloud, of the mean depth of the annulus r +- %.3f:' % HALF)
    print('   r      number left to chance    exactly n     the second over the first      (at a single radius, without the annulus: chance %s)' % ', '.join('%.3f' % cov_chance(r, r, n) for r in (0.2, 0.5, 0.8)))
    for r in (0.2, 0.35, 0.5, 0.65, 0.8, 0.9):
        a = annulus(cov_chance, r, r, n); b = annulus(cov_fixed, r, r, n); print('   %.2f        %7.3f             %7.3f           %.3f' % (r, a, b, b / a))
    print('the correlation between the mean depths at r = 0.8 and r = 0.3, number left to chance: %.3f (sqrt of the ratio of 1 - r^(2/3): %.3f); exactly n: %.3f' % (
        annulus(cov_chance, 0.8, 0.3, n) / math.sqrt(annulus(cov_chance, 0.8, 0.8, n) * annulus(cov_chance, 0.3, 0.3, n)), math.sqrt(tau(0.8) / tau(0.3)),
        annulus(cov_fixed, 0.8, 0.3, n) / math.sqrt(annulus(cov_fixed, 0.8, 0.8, n) * annulus(cov_fixed, 0.3, 0.3, n))))
    print('the count of layers (the ring shrunk to nothing): variance %.4f n^(1/3) with the number left to chance, %.4f n^(1/3) with exactly n' % (S(1) * D, S(1) * (D - 0.75 * DC)))
    print('the variance of depth round a ring about its own mean, and the mean squares of its first parts (n = 10^6):')
    print('   r      variance     m = 1      m = 2      m = 3      m = 4      (the level cell problem would have 0.65 x sqrt(depth) = %s)' % ', '.join('%.1f' % (0.65 * math.sqrt(0.75 * ALPHA * (n / math.pi) ** (2 / 3.0) * u(r))) for r in (0.3, 0.5, 0.7, 0.9)))
    for r in (0.1, 0.3, 0.5, 0.7, 0.9): print('   %.2f    %7.2f    %7.3f    %7.3f    %7.3f    %7.3f' % ((r, local(r, n)) + tuple(mode(m, r, n) for m in (1, 2, 3, 4))))
    print('check near the rim: at r = 0.999 the sum gives %.3f and the level formula D rho^(1/3) sqrt(3 (1 - r) / (2 pi)) gives %.3f' % (local(0.999, n), D * (n / math.pi) ** (1 / 3.0) * math.sqrt(3 * 0.001 / (2 * math.pi))))
