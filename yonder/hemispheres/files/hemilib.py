"""Shares of a quantity on the sphere (land area, people) lying within a cap, and the cap that holds most.

Everything works on a "weight grid": a regular longitude-latitude grid (row 0 = southernmost band, column 0 starts at
longitude -180) whose entries are amounts (km2 of land, people) in each cell. A cell is represented by its centre.
The Earth is a sphere and the grid's latitude is used as the latitude on that sphere unless `latmap` says otherwise.

share(): a cell at angular distance t from the centre c counts fully if t < r - e/2, not at all if t > r + e/2 and
linearly in between, where e is the cell height. So the share is a continuous function of c.
"""
import numpy as np

R_KM = 6371.0088


def unit(lat, lon):
    lat = np.radians(np.asarray(lat, dtype=np.float64))
    lon = np.radians(np.asarray(lon, dtype=np.float64))
    return np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], axis=-1)


def latlon(v):
    v = np.asarray(v, dtype=np.float64)
    return np.degrees(np.arcsin(np.clip(v[..., 2], -1, 1))), np.degrees(np.arctan2(v[..., 1], v[..., 0]))


def angle_deg(u, v):
    """Angle between unit vectors, accurate for small angles."""
    u = np.asarray(u, dtype=np.float64); v = np.asarray(v, dtype=np.float64)
    return np.degrees(2 * np.arcsin(np.clip(np.linalg.norm(u - v, axis=-1) / 2, 0, 1)))


def authalic(lat_deg):
    """Authalic latitude of a geodetic latitude on WGS84 (series in e^2; Snyder 1987, eq. 3-18)."""
    e2 = 0.00669437999014
    p = np.radians(np.asarray(lat_deg, dtype=np.float64))
    x = (p - (e2 / 3 + 31 * e2 ** 2 / 180 + 59 * e2 ** 3 / 560) * np.sin(2 * p)
         + (17 * e2 ** 2 / 360 + 61 * e2 ** 3 / 1260) * np.sin(4 * p) - (383 * e2 ** 3 / 45360) * np.sin(6 * p))
    return np.degrees(x)


def area_weights(cover, latmap=None):
    """Coverage fractions -> km2 per cell on the sphere (latmap: grid latitude -> latitude on the sphere)."""
    H, W = cover.shape
    lat = -90 + (np.arange(H) + 0.5) * (180 / H)
    top = lat + 90 / H; bot = lat - 90 / H
    if latmap is not None:
        top = latmap(top); bot = latmap(bot)
    # exact area of a latitude band cell: R^2 * dlon * (sin(top) - sin(bottom))
    cell = R_KM ** 2 * (2 * np.pi / W) * (np.sin(np.radians(top)) - np.sin(np.radians(bot)))
    return cover.astype(np.float64) * cell[:, None]


def coarsen(wgrid, f):
    H, W = wgrid.shape
    return wgrid.reshape(H // f, f, W // f, f).sum(axis=(1, 3))


def cells(wgrid, latmap=None):
    """Non-empty cells of a weight grid: unit vectors (float32), weights (float64), cell height in radians."""
    H, W = wgrid.shape
    lat = -90 + (np.arange(H) + 0.5) * (180 / H)
    lon = -180 + (np.arange(W) + 0.5) * (360 / W)
    if latmap is not None:
        lat = latmap(lat)
    i, j = np.nonzero(wgrid > 0)
    X = unit(lat[i], lon[j]).astype(np.float32)
    return X, wgrid[i, j].astype(np.float64), np.radians(180 / H)


def share(X, w, c, eps, r_deg=90.0, total=None):
    """Share of the total weight within r_deg of the unit vector c (soft edge of width eps radians)."""
    c = np.asarray(c, dtype=np.float32)
    d = X @ c
    r = np.radians(r_deg)
    f = np.clip(0.5 + (d - np.float32(np.cos(r))) / np.float32(eps * np.sin(r)), 0, 1)
    return float(w @ f.astype(np.float64)) / (w.sum() if total is None else total)


def share_map(X, w, eps, step, r_deg=90.0, chunk=400):
    """share() for centres on a grid of `step` degrees: lat -90+step/2 .. , lon -180+step/2 .. ; returns (lats, lons, S)."""
    lats = np.arange(-90 + step / 2, 90, step)
    lons = np.arange(-180 + step / 2, 180, step)
    LA, LO = np.meshgrid(lats, lons, indexing='ij')
    C = unit(LA.ravel(), LO.ravel()).astype(np.float32)
    r = np.radians(r_deg)
    out = np.empty(len(C))
    tot = w.sum()
    for a in range(0, len(C), chunk):
        D = X @ C[a:a + chunk].T
        F = np.clip(0.5 + (D - np.float32(np.cos(r))) / np.float32(eps * np.sin(r)), 0, 1)
        out[a:a + chunk] = (w @ F.astype(np.float64)) / tot
    return lats, lons, out.reshape(len(lats), len(lons))


class Local:
    """Fast share() for centres within `reach_deg` of c0: cells that are always in or always out are summed once."""

    def __init__(self, X, w, eps, c0, reach_deg, r_deg=90.0):
        c0 = np.asarray(c0, dtype=np.float64)
        d0 = X.astype(np.float64) @ c0
        t0 = np.degrees(np.arccos(np.clip(d0, -1, 1)))
        margin = reach_deg + np.degrees(eps) + 0.05
        always = t0 < r_deg - margin
        band = np.abs(t0 - r_deg) <= margin
        self.base = float(w[always].sum())
        self.X = X[band]; self.w = w[band]
        self.eps = eps; self.r = r_deg; self.total = float(w.sum())
        self.c0 = c0; self.reach = reach_deg

    def share(self, c):
        assert angle_deg(np.asarray(c, dtype=np.float64), self.c0) <= self.reach + 1e-9
        c32 = np.asarray(c, dtype=np.float32)
        d = self.X @ c32
        r = np.radians(self.r)
        f = np.clip(0.5 + (d - np.float32(np.cos(r))) / np.float32(self.eps * np.sin(r)), 0, 1)
        return (self.base + float(self.w @ f.astype(np.float64))) / self.total

    def grid(self, half_deg, step_deg):
        """Shares on a square grid of centres around c0 (tangent-plane offsets north/east, in degrees of arc)."""
        la0, lo0 = latlon(self.c0)
        north = unit(la0 + 90, lo0) if la0 <= 0 else -unit(la0 - 90, lo0)
        east = np.cross(north, self.c0)
        n = int(round(half_deg / step_deg))
        offs = np.arange(-n, n + 1) * step_deg
        S = np.full((len(offs), len(offs)), np.nan)
        for a, dn in enumerate(offs):
            for b, de in enumerate(offs):
                t = np.hypot(dn, de)
                if t > self.reach:
                    continue
                if t == 0:
                    c = self.c0
                else:
                    dirv = (dn * north + de * east) / t
                    c = np.cos(np.radians(t)) * self.c0 + np.sin(np.radians(t)) * dirv
                S[a, b] = self.share(c)
        return offs, S, north, east

    def point(self, dn, de, north, east):
        t = np.hypot(dn, de)
        if t == 0:
            return self.c0
        dirv = (dn * north + de * east) / t
        return np.cos(np.radians(t)) * self.c0 + np.sin(np.radians(t)) * dirv


def best_cap(wgrid, r_deg=90.0, coarse=10, step=1.0, latmap=None, verbose=True, levels=((4.0, 0.25), (0.6, 0.05), (0.12, 0.01))):
    """Global search for the centre holding the largest share within r_deg; returns a dict."""
    Xc, wc, ec = cells(coarsen(wgrid, coarse), latmap)
    lats, lons, S = share_map(Xc, wc, ec, step, r_deg)
    a, b = np.unravel_index(np.argmax(S), S.shape)
    c = unit(lats[a], lons[b])
    if verbose:
        print(f'  coarse: best {S[a, b]:.5f} at {lats[a]:.2f}, {lons[b]:.2f}')
    X, w, e = cells(wgrid, latmap)
    best = None
    for half, st in levels:
        loc = Local(X, w, e, c, half * 1.5, r_deg)
        offs, G, north, east = loc.grid(half, st)
        a2, b2 = np.unravel_index(np.nanargmax(G), G.shape)
        c = loc.point(offs[a2], offs[b2], north, east)
        best = G[a2, b2]
        if verbose:
            la, lo = latlon(c)
            edge = a2 in (0, len(offs) - 1) or b2 in (0, len(offs) - 1)
            print(f'  level +-{half} step {st}: best {best:.6f} at {la:.3f}, {lo:.3f}' + ('  (ON THE EDGE OF THE SEARCH BOX)' if edge else ''))
    la, lo = latlon(c)
    return dict(lat=float(la), lon=float(lo), share=float(best), c=c, coarse=(lats, lons, S), X=X, w=w, eps=e)


# ---------------------------------------------------------------------------------------------------------------
# Added after the review of 21 November (nothing above this line was changed). The reviewer showed that best_cap()
# refines only the single best point of the coarse map and so can return the lower of two distant, nearly equal
# maxima. summits() refines every local maximum of the coarse map that is within `tol` of the coarse best.
def summits(wgrid, r_deg=90.0, tol=0.003, coarse=10, step=1.0, latmap=None, levels=((4.0, 0.25), (0.6, 0.05), (0.12, 0.01)), merge_deg=1.0):
    """All refined local maxima within `tol` (as a share) of the best; a list of dicts, best first."""
    Xc, wc, ec = cells(coarsen(wgrid, coarse), latmap)
    lats, lons, S = share_map(Xc, wc, ec, step, r_deg)
    # local maxima of the coarse map: not smaller than any of the 8 neighbours (longitude wraps)
    P = np.pad(S, ((1, 1), (0, 0)), mode='edge')
    P = np.concatenate([P[:, -1:], P, P[:, :1]], axis=1)
    core = P[1:-1, 1:-1]
    ismax = np.ones_like(core, dtype=bool)
    for da in (-1, 0, 1):
        for db in (-1, 0, 1):
            if da or db:
                ismax &= core >= P[1 + da:P.shape[0] - 1 + da, 1 + db:P.shape[1] - 1 + db]
    cand = [(S[i, j], lats[i], lons[j]) for i, j in np.argwhere(ismax & (S >= S.max() - tol))]
    cand.sort(reverse=True)
    X, w, e = cells(wgrid, latmap)
    found = []
    for s0, la0, lo0 in cand:
        c = unit(la0, lo0)
        edge = False
        for half, st in levels:
            loc = Local(X, w, e, c, half * 1.5, r_deg)
            offs, G, north, east = loc.grid(half, st)
            a2, b2 = np.unravel_index(np.nanargmax(G), G.shape)
            edge = a2 in (0, len(offs) - 1) or b2 in (0, len(offs) - 1)
            c = loc.point(offs[a2], offs[b2], north, east)
            best = float(G[a2, b2])
        if any(angle_deg(c, f['c']) < merge_deg for f in found):
            continue
        la, lo = latlon(c)
        found.append(dict(lat=float(la), lon=float(lo), share=best, c=c, coarse_share=float(s0), on_edge_of_last_box=bool(edge)))
    found.sort(key=lambda f: -f['share'])
    return found
