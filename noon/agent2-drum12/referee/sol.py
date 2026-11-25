# Referee's own solver: radial linear FEM (lumped mass) + exact Bessel shooting to polish roots.
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.special import jv, yv, jvp, yvp
from scipy.optimize import brentq, linprog


def fam_modes(F):
    out = []
    for f in range(1, F + 1):
        for m in range(f - 1, -1, -2):
            out.append((m, (f + 1 - m) // 2, f))
    return out


def fem(nodes, rho_e, m, nev, grad=False):
    a = nodes[:-1]; b = nodes[1:]; h = b - a
    s1 = (a + b) / (2 * h)
    n = len(nodes)
    d = np.zeros(n); e = -s1.copy()
    d[:-1] += s1; d[1:] += s1
    if m > 0:
        L = np.zeros_like(a); L[1:] = np.log(b[1:] / a[1:])
        Ia = (b * b * L - 2 * b * h + (b * b - a * a) / 2) / h**2
        Ib = (a * a * L - 2 * a * h + (b * b - a * a) / 2) / h**2
        Iab = ((b * b - a * a) / 2 - a * b * L) / h**2
        d[:-1] += m * m * Ia; d[1:] += m * m * Ib; e += m * m * Iab
    ca = h * (2 * a + b) / 6; cb = h * (a + 2 * b) / 6
    M = np.zeros(n); M[:-1] += rho_e * ca; M[1:] += rho_e * cb
    lo = 1 if m > 0 else 0
    sl = slice(lo, n - 1)
    sq = np.sqrt(M[sl])
    dd = d[sl] / M[sl]; ee = e[lo:n - 2] / (sq[:-1] * sq[1:])
    if not grad:
        return eigh_tridiagonal(dd, ee, eigvals_only=True, select='i', select_range=(0, nev - 1))
    w, v = eigh_tridiagonal(dd, ee, select='i', select_range=(0, nev - 1))
    u = np.zeros((n, nev)); u[sl] = v / sq[:, None]
    G = -(u[:-1]**2 * ca[:, None] + u[1:]**2 * cb[:, None]) * w[None, :]
    return w, G


def fem_vec(nodes, rho_e, m, nev):
    """eigenvalues and nodal mode shapes, normalised to int rho u^2 r dr = 1"""
    a = nodes[:-1]; b = nodes[1:]; h = b - a
    s1 = (a + b) / (2 * h); n = len(nodes)
    d = np.zeros(n); e = -s1.copy(); d[:-1] += s1; d[1:] += s1
    if m > 0:
        L = np.zeros_like(a); L[1:] = np.log(b[1:] / a[1:])
        d[:-1] += m * m * (b * b * L - 2 * b * h + (b * b - a * a) / 2) / h**2
        d[1:] += m * m * (a * a * L - 2 * a * h + (b * b - a * a) / 2) / h**2
        e += m * m * ((b * b - a * a) / 2 - a * b * L) / h**2
    M = np.zeros(n); M[:-1] += rho_e * h * (2 * a + b) / 6; M[1:] += rho_e * h * (a + 2 * b) / 6
    lo = 1 if m > 0 else 0; sl = slice(lo, n - 1); sq = np.sqrt(M[sl])
    w, v = eigh_tridiagonal(d[sl] / M[sl], e[lo:n - 2] / (sq[:-1] * sq[1:]), select='i', select_range=(0, nev - 1))
    u = np.zeros((n, nev)); u[sl] = v / sq[:, None]
    return w, u


def spectrum(a, mmax=30, nmax=10, p=None):
    """all modes (ratio to (0,1), m, n) of a ring load, by FEM"""
    R = len(a); p = p or max(10, 1600 // R)
    nodes, rho_e = mesh(ring_edges(R), 1 + np.asarray(a), p); out = []; w0 = None
    for m in range(mmax + 1):
        w = np.sqrt(fem(nodes, rho_e, m, nmax))
        if m == 0: w0 = w[0]
        out += [(w[j] / w0, m, j + 1) for j in range(nmax)]
    return sorted(out)


def myD(edges, rho, top=6.6, strike=0.5, c0=0.5, rolloff=True, p=40, parts=False):
    """my reading of the author's D: struck at `strike`, modes up to `top`, energy in 0.6 s, cents from nearest whole multiple"""
    nodes, rho_e = mesh(np.asarray(edges), np.asarray(rho), p); w0 = None; num = den = 0.0; lst = []
    for m in range(0, 12):
        w, u = fem_vec(nodes, rho_e, m, 8); w = np.sqrt(w)
        if m == 0: w0 = w[0]
        for j in range(8):
            r = w[j] / w0
            if r > top: break
            amp = abs(np.interp(strike, nodes, u[:, j])) * (c0 if m == 0 else 1.0)
            s = amp / np.sqrt(r) * (np.exp(-(r / 7.0)**2) if rolloff else 1.0)
            t = 1.3 * r**-0.8; e = s * s * t * (1 - np.exp(-1.2 / t)); k = max(1, round(r))
            c = abs(1200 * np.log2(r / k)); num += e * c; den += e; lst.append((r, m, j + 1, e, c))
    if parts:
        return num / den, [(r, m, n, e / den, c) for r, m, n, e, c in sorted(lst)]
    return num / den


def shoot(om, edges, rho, m):
    A, B = 1.0, 0.0
    u = du = 0.0
    for i in range(len(rho)):
        k = om * np.sqrt(rho[i])
        if i > 0:
            x = k * edges[i - 1]
            A, B = ((np.pi * x / 2) * (u * yvp(m, x) - (du / k) * yv(m, x)),
                    (np.pi * x / 2) * ((du / k) * jv(m, x) - u * jvp(m, x)))
            s = abs(A) + abs(B); A /= s; B /= s
        x = k * edges[i]
        u = A * jv(m, x) + B * yv(m, x); du = k * (A * jvp(m, x) + B * yvp(m, x))
    return u


def exact_root(om0, edges, rho, m):
    for dlt in (1e-3, 3e-3, 1e-2, 2e-2):
        lo, hi = om0 * (1 - dlt), om0 * (1 + dlt)
        if shoot(lo, edges, rho, m) * shoot(hi, edges, rho, m) < 0:
            return brentq(shoot, lo, hi, args=(edges, rho, m), xtol=1e-13, rtol=1e-13)
    raise RuntimeError("no bracket m=%d om0=%g" % (m, om0))


def mesh(edges, rho, p):
    """edges: outer radii of regions; p elements per region."""
    r0 = 0.0; nodes = [np.array([0.0])]
    for e in edges:
        nodes.append(np.linspace(r0, e, p + 1)[1:]); r0 = e
    return np.concatenate(nodes), np.repeat(rho, p)


def freqs(edges, rho, need, p=40, exact=False, grad=False):
    """need: dict m -> nmax. returns dict (m,n)->omega (and grads wrt region rho)."""
    nodes, rho_e = mesh(edges, rho, p)
    om = {}; gr = {}
    for m, nmax in need.items():
        if grad:
            w, G = fem(nodes, rho_e, m, nmax, True)
            Gr = G.reshape(len(rho), p, nmax).sum(1)
        else:
            w = fem(nodes, rho_e, m, nmax)
        for n in range(1, nmax + 1):
            o = np.sqrt(w[n - 1])
            if grad:
                gr[(m, n)] = Gr[:, n - 1] / w[n - 1]   # dlam/lam
            om[(m, n)] = exact_root(o, edges, rho, m) if exact else o
    return (om, gr) if grad else om


def need_of(modes):
    need = {}
    for (m, n, f) in modes:
        need[m] = max(need.get(m, 0), n)
    return need


def misses(edges, rho, modes, p=40, exact=False, grad=False):
    need = need_of(modes)
    if grad:
        om, gr = freqs(edges, rho, need, p, exact, True)
    else:
        om = freqs(edges, rho, need, p, exact)
    o0 = om[(0, 1)]
    c = np.array([om[(m, n)] / o0 / f - 1 for (m, n, f) in modes if (m, n) != (0, 1)])
    if not grad:
        return c
    J = np.array([0.5 * (om[(m, n)] / o0 / f) * (gr[(m, n)] - gr[(0, 1)]) for (m, n, f) in modes if (m, n) != (0, 1)])
    return c, J


def ring_edges(R):
    return np.arange(1, R + 1) / R


def ring_w(R):
    e = np.concatenate([[0], ring_edges(R)])
    return e[1:]**2 - e[:-1]**2


def slp(a0, modes, Mmax, p=20, iters=400, exact=False, tr0=1.0, trmin=1e-6, verbose=False):
    R = len(a0); edges = ring_edges(R); w = ring_w(R)
    a = np.array(a0, float)
    c, J = misses(edges, 1 + a, modes, p, exact, True)
    f = np.abs(c).max(); tr = tr0; nc = len(c)
    for it in range(iters):
        cost = np.zeros(R + 1); cost[-1] = 1
        Aub = np.zeros((2 * nc + 1, R + 1)); bub = np.zeros(2 * nc + 1)
        Aub[:nc, :R] = J; Aub[:nc, -1] = -1; bub[:nc] = -c
        Aub[nc:2 * nc, :R] = -J; Aub[nc:2 * nc, -1] = -1; bub[nc:2 * nc] = c
        Aub[-1, :R] = w; bub[-1] = Mmax - w @ a
        bnds = [(max(-ai, -tr), tr) for ai in a] + [(0, None)]
        res = linprog(cost, A_ub=Aub, b_ub=bub, bounds=bnds, method='highs')
        if res.status != 0:
            tr *= 0.5
            if tr < trmin: break
            continue
        an = np.maximum(a + res.x[:R], 0)
        cn, Jn = misses(edges, 1 + an, modes, p, exact, True)
        fn = np.abs(cn).max()
        if fn < f:
            a, c, J, f = an, cn, Jn, fn; tr = min(tr * 1.5, 5.0)
        else:
            tr *= 0.5
            if tr < trmin: break
        if verbose and it % 20 == 0:
            print(it, f, tr, flush=True)
    return a, f
