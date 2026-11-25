"""Antipodal pairs with equal temperature and equal pressure, from reanalysis fields.  (Noon = agent2, 21 November 2026)

For each time: g = (T, P) - (T, P) at the antipode, on the 2.5-degree grid, which the antipodal map sends to itself
(latitude row i -> row 72 - i, longitude column j -> column j + 72).  With bilinear interpolation on the grid cells g
is a continuous odd map from the sphere to the plane, so it has a zero (Borsuk-Ulam), and generically an odd number
of antipodal pairs of zeros.  The zeros are found cell by cell: two bilinear equations in (u, v), solved exactly.
A tiny fixed perturbation of the data breaks exact ties (the data are rounded to 0.1 K and 10 Pa); it keeps g odd.
Reads the downloaded files with nothing but h5py and numpy.

--stride k keeps every k-th row and column (k = 2, 3, 4, 6, 8, 12 give grids of 5, 7.5, 10, 15, 20, 30 degrees, each
again carried to itself by the antipodal map): the same question asked of a coarser picture of the same weather.

usage: python -I pairs.py DATADIR out.npz [--pressure slp|pres] [--seed N] [--eps X] [--swap] [--stride k] [--year Y]
"""
import sys, argparse
import numpy as np
import h5py

PFILE = {'slp': ('slp.%d.nc', 'slp'), 'pres': ('pres.sfc.%d.nc', 'pres')}


def anti(F):
    """The field seen from the antipode, for arrays (..., rows from pole to pole, an even number of columns)."""
    return np.roll(F[..., ::-1, :], F.shape[-1] // 2, axis=-1)


def load(datadir, pressure='slp', seed=20261121, eps=1e-6, stride=1, year=2025):
    """Returns time, lat, lon, g1 (K), g2 (hPa): the odd parts times two, tie-broken."""
    fa = h5py.File(datadir + '/air.sig995.%d.nc' % year, 'r')
    fs = h5py.File(datadir + '/' + PFILE[pressure][0] % year, 'r')
    lat, lon, time = fa['lat'][...], fa['lon'][...], fa['time'][...]
    assert np.allclose(lat, np.linspace(90, -90, 73)) and np.allclose(lon, np.arange(0, 360, 2.5))
    assert np.array_equal(time, fs['time'][...])
    T = fa['air'][...].astype(np.float64)                               # K
    P = fs[PFILE[pressure][1]][...].astype(np.float64) / 100.0          # hPa
    assert T.shape == P.shape == (len(time), 73, 144) and len(time) in (1460, 1464) and np.isfinite(T).all() and np.isfinite(P).all()
    assert T.min() > 150 and T.max() < 340 and P.min() > 400 and P.max() < 1150
    assert np.ptp(T[:, 0, :], axis=1).max() == 0 and np.ptp(P[:, -1, :], axis=1).max() == 0      # one value at each pole
    assert 72 % stride == 0
    T, P, lat, lon = T[:, ::stride, ::stride], P[:, ::stride, ::stride], lat[::stride], lon[::stride]
    rng = np.random.default_rng(seed)

    def perturb(F):
        n = rng.uniform(-eps, eps, size=F.shape[1:])
        n[0, :] = n[0, 0]
        n[-1, :] = n[-1, 0]                                             # one value at each pole
        return F + n
    T, P = perturb(T), perturb(P)
    g1, g2 = T - anti(T), P - anti(P)
    assert np.abs(g1 + anti(g1)).max() < 1e-9 and np.abs(g2 + anti(g2)).max() < 1e-9             # odd
    assert np.abs(g1[:, 0, :] - g1[:, 0, :1]).max() < 1e-9                                       # single-valued at the poles
    return time, lat, lon, g1, g2


def zeros_in_cells(a1, b1, c1, d1, a2, b2, c2, d2):
    """corners: a = (u=0,v=0), b = (1,0), c = (0,1), d = (1,1); f = A + B u + C v + E u v for each component.
    Returns arrays (cell index, u, v) of the common zeros with 0 <= u, v < 1."""
    A1, B1, C1, E1 = a1, b1 - a1, c1 - a1, a1 - b1 - c1 + d1
    A2, B2, C2, E2 = a2, b2 - a2, c2 - a2, a2 - b2 - c2 + d2
    # eliminate uv: E2 * f1 - E1 * f2 = L0 + Lu u + Lv v = 0  ->  v = -(L0 + Lu u) / Lv ; substitute into f1 (times Lv)
    L0, Lu, Lv = E2 * A1 - E1 * A2, E2 * B1 - E1 * B2, E2 * C1 - E1 * C2
    # Lv f1 = Lv A1 + Lv B1 u - C1 (L0 + Lu u) - E1 u (L0 + Lu u) = q0 + q1 u + q2 u^2
    q0 = Lv * A1 - C1 * L0
    q1 = Lv * B1 - C1 * Lu - E1 * L0
    q2 = -E1 * Lu
    disc = q1 * q1 - 4 * q2 * q0
    ok = disc >= 0
    sq = np.sqrt(np.where(ok, disc, 0))
    out_i, out_u, out_v = [], [], []
    for sgn in (1, -1):
        with np.errstate(divide='ignore', invalid='ignore'):
            u = np.where(np.abs(q2) > 1e-300, (-q1 + sgn * sq) / (2 * q2), np.where(sgn == 1, -q0 / q1, np.nan))
            v = -(L0 + Lu * u) / Lv
        good = ok & np.isfinite(u) & np.isfinite(v) & (u >= 0) & (u < 1) & (v >= 0) & (v < 1)
        idx = np.nonzero(good)[0]
        out_i.append(idx), out_u.append(u[idx]), out_v.append(v[idx])
    return np.concatenate(out_i), np.concatenate(out_u), np.concatenate(out_v)


def zeros(G1, G2, swap=False):
    """All common zeros of the two piecewise bilinear fields (rows from pole to pole) -> latitude, longitude in degrees.
    swap=True eliminates the other variable first (the same zeros by a different route; a check)."""
    ncol = G1.shape[1]
    step = 360.0 / ncol
    assert (G1.shape[0] - 1) * step == 180
    G1 = np.concatenate([G1, G1[:, :1]], axis=1)
    G2 = np.concatenate([G2, G2[:, :1]], axis=1)                        # close the circle of longitudes
    # cell (i, j): rows i, i+1 (latitude going south), columns j, j+1 (longitude going east); u along longitude, v along latitude
    corners = lambda G: (G[:-1, :-1].ravel(), G[:-1, 1:].ravel(), G[1:, :-1].ravel(), G[1:, 1:].ravel())
    a1, b1, c1, d1 = corners(G1)
    a2, b2, c2, d2 = corners(G2)
    mixed = lambda a, b, c, d: (np.minimum(np.minimum(a, b), np.minimum(c, d)) < 0) & (np.maximum(np.maximum(a, b), np.maximum(c, d)) > 0)
    cand = np.nonzero(mixed(a1, b1, c1, d1) & mixed(a2, b2, c2, d2))[0]
    k = lambda x: x[cand]
    if swap:
        i, v, u = zeros_in_cells(k(a1), k(c1), k(b1), k(d1), k(a2), k(c2), k(b2), k(d2))
    else:
        i, u, v = zeros_in_cells(k(a1), k(b1), k(c1), k(d1), k(a2), k(b2), k(c2), k(d2))
    cell = cand[i]
    row, col = cell // ncol, cell % ncol
    return 90 - step * (row + v), (step * (col + u)) % 360


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('datadir'), ap.add_argument('out')
    ap.add_argument('--pressure', default='slp', choices=list(PFILE))
    ap.add_argument('--seed', type=int, default=20261121), ap.add_argument('--eps', type=float, default=1e-6)
    ap.add_argument('--swap', action='store_true'), ap.add_argument('--stride', type=int, default=1)
    ap.add_argument('--year', type=int, default=2025)
    a = ap.parse_args()
    time, lat, lon, g1, g2 = load(a.datadir, a.pressure, a.seed, a.eps, a.stride, a.year)
    counts = np.zeros(len(time), int)
    recs = []
    for t in range(len(time)):
        la, lo = zeros(g1[t], g2[t], a.swap)
        assert len(la) % 2 == 0, (t, len(la))                           # zeros come in antipodal pairs
        counts[t] = len(la) // 2
        recs += [(t, x, y) for x, y in zip(la, lo)]
    np.savez(a.out, counts=counts, recs=np.array(recs), time=time, lat=lat, lon=lon)
    vals, freq = np.unique(counts, return_counts=True)
    print("times:", len(time), " pairs per time:", dict(zip(vals.tolist(), freq.tolist())))
    print("even counts:", int((counts % 2 == 0).sum()), " median", np.median(counts), " mean %.2f" % counts.mean(),
          " 5th and 95th percentile", np.percentile(counts, [5, 95]))
