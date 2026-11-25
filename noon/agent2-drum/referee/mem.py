# Referee's own solver: linear finite elements in r, lumped mass, mesh nodes on every density jump.
# Weak form for mode m:  int r u'v' + m^2 int uv/r = w^2 int sigma(r) r u v   on (0,1), u(1)=0.
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.special import jv, yv, jvp, yvp, jn_zeros
from scipy.optimize import brentq

GX = np.array([-np.sqrt(0.6), 0.0, np.sqrt(0.6)])
GW = np.array([5 / 9, 8 / 9, 5 / 9])
MODES = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
TARGET = np.array([1, 2, 3, 3, 4, 4, 5, 5, 5.0])
EXTRA = [(5, 1), (3, 2), (1, 3)]


def mesh(breaks, N):
    pts = [0.0] + sorted(b for b in breaks if 1e-6 < b < 1 - 1e-6) + [1.0]
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        if b - a < 1e-7:
            continue
        n = max(4, int(np.ceil(N * (b - a))))
        segs.append(np.linspace(a, b, n + 1)[:-1])
    return np.append(np.concatenate(segs), 1.0)


def freqs(sigma, breaks, m, nmax, N):
    r = mesh(breaks, N)
    a, b = r[:-1], r[1:]
    h = b - a
    mid = 0.5 * (a + b)
    x = mid[:, None] + 0.5 * h[:, None] * GX[None, :]
    f = sigma(x) * x * (0.5 * h[:, None] * GW[None, :])
    pR = (x - a[:, None]) / h[:, None]
    n = len(r)
    M = np.zeros(n)
    M[:-1] += (f * (1 - pR)).sum(1)
    M[1:] += (f * pR).sum(1)
    kel = mid / h
    K = np.zeros(n)
    K[:-1] += kel
    K[1:] += kel
    lo = 0
    if m > 0:
        lg = np.log1p(h[1:] / a[1:])
        cR = np.ones(len(h))
        cL = np.zeros(len(h))
        cR[1:] = 1 - a[1:] / h[1:] * lg
        cL[1:] = b[1:] / h[1:] * lg - 1
        K[:-1] += m * m * cL
        K[1:] += m * m * cR
        lo = 1
    d = K[lo:n - 1] / M[lo:n - 1]
    e = -kel[lo:n - 2] / np.sqrt(M[lo:n - 2] * M[lo + 1:n - 1])
    ev = eigh_tridiagonal(d, e, eigvals_only=True, select='i', select_range=(0, nmax - 1))
    return np.sqrt(ev)


def ratios(sigma, breaks, N, modes=MODES, rich=False):
    if rich:  # Richardson on h^2
        r1 = ratios(sigma, breaks, N, modes)
        r2 = ratios(sigma, breaks, 2 * N, modes)
        return (4 * r2 - r1) / 3
    need = {0: 1}
    for m, nn in modes:
        need[m] = max(need.get(m, 0), nn)
    fr = {m: freqs(sigma, breaks, m, nm, N) for m, nm in need.items()}
    return np.array([fr[m][nn - 1] / fr[0][0] for m, nn in modes])


def miss(rat):
    return float(np.max(np.abs(rat[1:] / TARGET[1:] - 1)))


def step(s, k):
    return lambda x: np.where(x < k, s, 1.0)


def graded(s, k):
    return lambda x: np.where(x < k, 1 + (s - 1) * (1 - (x / k) ** 2), 1.0)


def layers(loads, radii):
    def sg(x):
        out = np.ones_like(x)
        for a_, k_ in zip(loads, radii):
            out = out + a_ * (x < k_)
        return out
    return sg


# independent check for the step skin: Bessel matching at r = k
def bessel_step(s, k, m, nmax, wmax=40.0, npts=8000):
    q = np.sqrt(s)

    def F(w):
        g = jv(m, w * k) * yv(m, w) - yv(m, w * k) * jv(m, w)
        gp = jvp(m, w * k) * yv(m, w) - yvp(m, w * k) * jv(m, w)
        return q * jvp(m, w * q * k) * g - jv(m, w * q * k) * gp
    ws = np.linspace(0.05, wmax, npts)
    v = F(ws)
    out = []
    for i in np.nonzero(np.sign(v[:-1]) != np.sign(v[1:]))[0]:
        out.append(brentq(F, ws[i], ws[i + 1], xtol=1e-13))
        if len(out) == nmax:
            break
    return np.array(out)
