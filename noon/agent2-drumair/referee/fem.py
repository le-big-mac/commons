# Referee's own solver: linear finite elements in the radius, density constant per element.
# weak form (divided by 2 pi):  int (u'v' + m^2 u v / r^2) r dr + [m=0] 2 pi B (int u r dr)(int v r dr) = lam int rho u v r dr
import numpy as np, scipy.linalg as sl

CREF = 1.2 * 343.0**2 * 0.065**2 / (np.pi * 0.06**2 * 0.125 * 0.25 * (2 * np.pi * 440.0) ** 2)  # B = CREF * w11^2


class Fem:
    def __init__(self, N):
        self.N = N
        h = 1.0 / N
        re = np.arange(N) * h
        self.m00 = h * (re / 3 + h / 12)
        self.m11 = h * (re / 3 + h / 4)
        self.m01 = h * (re / 6 + h / 12)
        self.k = (re + h / 2) / h
        g, wg = np.polynomial.legendre.leggauss(8)
        s = (g + 1) / 2
        ws = wg / 2
        r = re[:, None] + s[None, :] * h
        self.c00 = (((1 - s) ** 2) / r) @ ws * h
        self.c11 = ((s**2) / r) @ ws * h
        self.c01 = (((1 - s) * s) / r) @ ws * h
        v = np.zeros(N + 1)
        v[:-1] += h * (re / 2 + h / 6)
        v[1:] += h * (re / 2 + h / 3)
        self.v = v

    def modes(self, rho, m, n, B=0.0):
        """rho: density per element. returns lam[n], U[N+1,n] (M-orthonormal), and unit-density element energies E[N,n]"""
        N = self.N
        d = np.zeros(N + 1)
        d[:-1] += self.k + m * m * self.c00
        d[1:] += self.k + m * m * self.c11
        o = -self.k + m * m * self.c01
        K = np.diag(d) + np.diag(o, 1) + np.diag(o, -1)
        dm = np.zeros(N + 1)
        dm[:-1] += rho * self.m00
        dm[1:] += rho * self.m11
        om = rho * self.m01
        M = np.diag(dm) + np.diag(om, 1) + np.diag(om, -1)
        lo = 0 if m == 0 else 1
        K = K[lo:N, lo:N]
        M = M[lo:N, lo:N]
        if m == 0 and B != 0.0:
            vv = self.v[lo:N]
            K = K + 2 * np.pi * B * np.outer(vv, vv)
        lam, U = sl.eigh(K, M, subset_by_index=[0, n - 1])
        Uf = np.zeros((N + 1, n))
        Uf[lo:N] = U
        E = (Uf[:-1] ** 2) * self.m00[:, None] + 2 * Uf[:-1] * Uf[1:] * self.m01[:, None] + (Uf[1:] ** 2) * self.m11[:, None]
        return lam, Uf, E


def freqs(fem, rho, B=None, cref=CREF, grads=False):
    """returns dict of w for the nine modes; B=None means reference drum (B = cref*w11^2). If grads, also dw/drho_e."""
    out = {}
    G = {}
    need = {1: 2, 2: 2, 3: 1, 4: 1}
    for m, n in need.items():
        lam, U, E = fem.modes(rho, m, n)
        for j in range(n):
            out[(m, j + 1)] = np.sqrt(lam[j])
            if grads:
                G[(m, j + 1)] = -lam[j] * E[:, j] / (2 * np.sqrt(lam[j]))
    w11 = out[(1, 1)]
    Bv = cref * w11**2 if B is None else B
    lam, U, E = fem.modes(rho, 0, 3, Bv)
    for j in range(3):
        w = np.sqrt(lam[j])
        out[(0, j + 1)] = w
        if grads:
            dl = -lam[j] * E[:, j]
            if B is None:
                dB = cref * 2 * w11 * G[(1, 1)]
                dl = dl + 2 * np.pi * (fem.v @ U[:, j]) ** 2 * dB
            G[(0, j + 1)] = dl / (2 * w)
    out["B"] = Bv
    return (out, G) if grads else out


def rich(Ns, rho_fn, B=None, cref=CREF):
    """Richardson from two grids N, 2N. rho_fn(N) -> density per element."""
    a = freqs(Fem(Ns), rho_fn(Ns), B, cref)
    b = freqs(Fem(2 * Ns), rho_fn(2 * Ns), B, cref)
    if B is None:
        # B depends on w11: use extrapolated w11 for B, then redo
        w11 = (4 * b[(1, 1)] - a[(1, 1)]) / 3
        Bx = cref * w11**2
        a = freqs(Fem(Ns), rho_fn(Ns), Bx, cref)
        b = freqs(Fem(2 * Ns), rho_fn(2 * Ns), Bx, cref)
    return {k: (4 * b[k] - a[k]) / 3 if k != "B" else b[k] for k in a}


def ring_rho(a):
    a = np.asarray(a, float)

    def f(N):
        assert N % len(a) == 0
        return 1.0 + np.repeat(a, N // len(a))

    return f


def disc_rho(mu, r0):
    def f(N):
        mid = (np.arange(N) + 0.5) / N
        return 1.0 + mu * (mid < r0)

    return f


OVER = [(2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
KOVER = [3, 3, 4, 4, 5, 5, 5]


def report(w):
    note = w[(1, 1)] / 2
    ra = [w[q] / (k * note) - 1 for q, k in zip(OVER, KOVER)]
    low = w[(0, 1)]
    rb = [w[(1, 1)] / (2 * low) - 1] + [w[q] / (k * low) - 1 for q, k in zip(OVER, KOVER)]
    return dict(place=low / note, missA=max(abs(x) for x in ra), missB=max(abs(x) for x in rb), ra=ra, rb=rb, B=w["B"], w11=w[(1, 1)])
