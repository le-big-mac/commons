"""The checker's own small library (not the author's hemilib): people in a half of the Earth, two ways.

A grid is 3600 x 7200, row 0 = southernmost band, column 0 starts at 180 W, people per cell; a cell is represented
by its centre, and it is inside the half centred at c when the dot product of the two unit vectors is > 0 (hard edge).

  half_dot(P, lat, lon)       direct: a mask from dot products in float64
  Cum(P).shares(lats, lons)   by rows: in row i the cells inside are those whose longitude is within
                              h_i = arccos(-tan(lat_i) tan(lat_c)) of the centre's, so the count is a difference of
                              two entries of the row's cumulative sum.  Exact, and fast enough for a lattice of
                              centres over the whole sphere.
"""
import numpy as np

H, W, CELL = 3600, 7200, 0.05
LAT = -90 + (np.arange(H) + 0.5) * CELL
LON = -180 + (np.arange(W) + 0.5) * CELL
R_KM = 6371.0088


def unit(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def km(lat1, lon1, lat2, lon2):
    a = unit(lat1, lon1); b = unit(lat2, lon2)
    return float(R_KM * 2 * np.arcsin(min(1.0, np.linalg.norm(a - b) / 2)))


def mask_dot(lat, lon):
    c = unit(lat, lon)
    la = np.radians(LAT)[:, None]; lo = np.radians(LON)[None, :]
    d = np.cos(la) * np.cos(lo) * c[0] + np.cos(la) * np.sin(lo) * c[1] + np.sin(la) * c[2]
    return d > 0


def half_dot(P, lat, lon):
    return float(P[mask_dot(lat, lon)].sum())


class Cum:
    def __init__(self, P):
        assert P.shape == (H, W)
        self.total = float(P.sum())
        rows = np.flatnonzero(P.sum(axis=1) > 0)
        self.rows = rows
        self.C = np.zeros((len(rows), W + 1), dtype=np.float64)
        np.cumsum(P[rows], axis=1, out=self.C[:, 1:])
        self.T = self.C[:, -1].copy()
        self.tanlat = np.tan(np.radians(LAT[rows]))
        self.ri = np.arange(len(rows))[:, None]

    def _cw(self, k):
        """periodic cumulative sum at integer positions k (array n_rows x L)"""
        q, r = np.divmod(k, W)
        return self.C[self.ri, r] + q * self.T[:, None]

    def at_lat(self, latc, lons):
        """people in the halves centred at (latc, lon) for every lon in lons"""
        lons = np.asarray(lons, dtype=np.float64)
        q = -self.tanlat * np.tan(np.radians(latc))
        full = q <= -1; empty = q >= 1
        h = np.degrees(np.arccos(np.clip(q, -1, 1)))          # half-width in degrees of longitude, per row
        hw = h / CELL
        uc = (lons + 180.0) / CELL
        lo = np.floor(uc[None, :] - hw[:, None] - 0.5).astype(np.int64) + 1
        hi = np.ceil(uc[None, :] + hw[:, None] - 0.5).astype(np.int64) - 1
        n = hi - lo + 1
        S = self._cw(hi + 1) - self._cw(lo)
        S = np.where(n <= 0, 0.0, S)
        S = np.where(n >= W, self.T[:, None], S)
        S[full] = self.T[full, None]
        S[empty] = 0.0
        return S.sum(axis=0)

    def shares(self, lats, lons):
        """array len(lats) x len(lons) of shares"""
        out = np.empty((len(lats), len(lons)))
        for a, la in enumerate(lats):
            out[a] = self.at_lat(float(la), lons)
        return out / self.total

    def share(self, lat, lon):
        return float(self.at_lat(float(lat), [float(lon)])[0] / self.total)
