"""Bullard's fit, again: the rigid rotation that best closes the South Atlantic, on the ETOPO1 depth grid.
usage: python -I fit.py ETOPO1_Ice_g_gmt4.grd out.npz

The margin of a continent at depth z is the longest contour of that depth in a window round the South Atlantic,
cut to the stretch facing that ocean and resampled every 20 km.  A rotation of South America is scored by the
root-mean-square distance from each margin point to the nearest point of the other margin, leaving out points
whose nearest neighbour is an end of the other margin (the two stretches need not be equally long).
"""
import sys
import numpy as np
from scipy.io import netcdf_file
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from skimage.measure import find_contours

R = 6371.0
BULLARD = (44.0, -30.6, 57.0)                                           # pole latitude, longitude, angle: as I remember the 1965 paper
NIGER = (4.5, 6.0)
DEPTHS = [0, 200, 500, 900, 2000, 3000]
LAT0, LAT1, LON0, LON1, STEP = -60.0, 20.0, -80.0, 30.0, 2              # the window; every second cell of the one-minute grid


def unit(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], axis=-1)


def latlon(v):
    return np.degrees(np.arcsin(np.clip(v[..., 2], -1, 1))), np.degrees(np.arctan2(v[..., 1], v[..., 0]))


def rotmat(w):
    """rotation by |w| radians about the axis w (right-handed)"""
    th = np.linalg.norm(w)
    if th < 1e-12:
        return np.eye(3)
    k = w / th
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K


def w_of(plat, plon, angle):
    return unit(plat, plon) * np.radians(angle)


def pole_of(w):
    th = np.linalg.norm(w)
    la, lo = latlon(w / th)
    return float(la), float(lo), float(np.degrees(th))


def gc(a, b):
    """great-circle distance in km between unit vectors"""
    return R * 2 * np.arcsin(np.clip(np.linalg.norm(a - b, axis=-1) / 2, 0, 1))


def load(path):
    f = netcdf_file(path, 'r', mmap=False)
    x, y = f.variables['x'][:], f.variables['y'][:]
    i0, i1 = np.searchsorted(y, LAT0), np.searchsorted(y, LAT1) + 1
    j0, j1 = np.searchsorted(x, LON0), np.searchsorted(x, LON1) + 1
    z = np.array(f.variables['z'][i0:i1:STEP, j0:j1:STEP], dtype=np.float32)
    return y[i0:i1:STEP].copy(), x[j0:j1:STEP].copy(), z


def resample(lat, lon, step_km=20.0):
    v = unit(lat, lon)
    s = np.concatenate([[0], np.cumsum(gc(v[1:], v[:-1]))])
    t = np.arange(0, s[-1], step_km)
    out = np.stack([np.interp(t, s, v[:, k]) for k in range(3)], axis=1)
    return out / np.linalg.norm(out, axis=1)[:, None]


def margins(lats, lons, z, depth, afr_north=8.0, afr_east=20.0):
    """-> (South America's margin, Africa's margin) as unit vectors every 20 km"""
    cs = find_contours(z, -float(depth) + 0.5)                          # half a metre off the integer, so that the coastline is not a plateau
    def ll(c):
        return np.interp(c[:, 0], np.arange(len(lats)), lats), np.interp(c[:, 1], np.arange(len(lons)), lons)
    best = {}
    for c in cs:
        if len(c) < 200:
            continue
        la, lo = ll(c)
        for name, keep in (('sam', (lo > -68) & (lo < -25) & (la > -45) & (la < 8)), ('afr', (lo > -25) & (lo < afr_east) & (la < afr_north) & (la > -40))):
            if keep.sum() < 100:
                continue
            # the longest unbroken run of kept points on this contour
            idx = np.nonzero(keep)[0]
            runs = np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1)
            run = max(runs, key=len)
            v = resample(la[run], lo[run])
            if name not in best or len(v) > len(best[name]):
                best[name] = v
    return best['sam'], best['afr']


def misfit(w, sam, afr, tree_afr=None, detail=False):
    rs = sam @ rotmat(w).T
    ta = tree_afr if tree_afr is not None else cKDTree(afr)
    d1, i1 = ta.query(rs)
    ts = cKDTree(rs)
    d2, i2 = ts.query(afr)
    k1 = (i1 > 0) & (i1 < len(afr) - 1)
    k2 = (i2 > 0) & (i2 < len(rs) - 1)
    g1 = R * 2 * np.arcsin(np.clip(d1 / 2, 0, 1))
    g2 = R * 2 * np.arcsin(np.clip(d2 / 2, 0, 1))
    used = np.concatenate([g1[k1], g2[k2]])
    if k1.mean() < 0.6 or k2.mean() < 0.6 or len(used) == 0:           # a rotation that slides the margins past each other is no fit
        rms = 1e4 + 1e4 * (2 - k1.mean() - k2.mean())
    else:
        rms = float(np.sqrt((used ** 2).mean()))
    if detail:
        return rms, rs, g1, k1, g2, k2
    return rms


def best_rotation(sam, afr):
    tree = cKDTree(afr)
    results = []
    for plat in (15, 40, 65):
        for plon in (-70, -35, 0):
            for ang in (35, 55, 75):
                r = minimize(misfit, w_of(plat, plon, ang), args=(sam, afr, tree), method='Nelder-Mead',
                             options=dict(xatol=1e-5, fatol=1e-3, maxiter=4000))
                results.append((r.fun, r.x))
    results.sort(key=lambda t: t[0])
    return results


if __name__ == '__main__':
    lats, lons, z = load(sys.argv[1])
    print(f"window {LAT0}..{LAT1} N, {LON0}..{LON1} E; grid {z.shape}; depths from {z.min():.0f} to {z.max():.0f} m")
    out = {}
    wb = w_of(*BULLARD)
    for depth in DEPTHS:
        sam, afr = margins(lats, lons, z, depth)
        res = best_rotation(sam, afr)
        f, w = res[0]
        plat, plon, ang = pole_of(w)
        sep = float(gc(unit(plat, plon), unit(BULLARD[0], BULLARD[1])) / R * 180 / np.pi)
        fb = misfit(wb, sam, afr)
        near = sum(1 for g, _ in res if g < f * 1.02)
        second = next((g for g, _ in res if g > f * 1.02), np.nan)
        print(f"depth {depth:4d} m: margins {len(sam) * 20} km (South America) and {len(afr) * 20} km (Africa); best rotation {ang:.2f} deg about {plat:.2f} N, {plon:.2f} E;"
              f" misfit {f:.1f} km; pole {sep:.1f} deg from Bullard's, angle {ang - BULLARD[2]:+.2f}; Bullard's rotation on these margins: {fb:.1f} km"
              f"; starts reaching the best: {near} of {len(res)}, next best {second:.0f} km")
        out[f"w{depth}"] = w
        out[f"f{depth}"] = f
        out[f"fb{depth}"] = fb
        out[f"sam{depth}"] = sam
        out[f"afr{depth}"] = afr
    # overlaps and gaps at 900 m: is the rotated South American margin on Africa's side of Africa's margin?
    depth = 900
    sam, afr, w = out['sam900'], out['afr900'], out['w900']
    rms, rs, g1, k1, g2, k2 = misfit(w, sam, afr, detail=True)
    la, lo = latlon(rs)
    ii = np.clip(np.interp(la, lats, np.arange(len(lats))), 0, len(lats) - 1.001)
    jj = np.clip(np.interp(lo, lons, np.arange(len(lons))), 0, len(lons) - 1.001)
    i0, j0 = ii.astype(int), jj.astype(int)
    fi, fj = ii - i0, jj - j0
    elev = (1 - fi) * ((1 - fj) * z[i0, j0] + fj * z[i0, j0 + 1]) + fi * ((1 - fj) * z[i0 + 1, j0] + fj * z[i0 + 1, j0 + 1])
    signed = np.where(elev > -depth, g1, -g1)                           # positive: South America's edge lies on Africa's shelf (overlap)
    signed[~k1] = np.nan
    k = int(np.nanargmax(signed))
    dn = float(gc(rs[k], unit(*NIGER)))
    print(f"at 900 m: largest overlap {signed[k]:.0f} km at {la[k]:.1f} N, {lo[k]:.1f} E in Africa's frame, {dn:.0f} km from the Niger delta;"
          f" largest gap {-np.nanmin(signed):.0f} km at {la[int(np.nanargmin(signed))]:.1f} N, {lo[int(np.nanargmin(signed))]:.1f} E")
    print(f"   share of South America's margin overlapping Africa's shelf: {100 * np.nanmean(signed > 0):.0f}%; median gap or overlap {np.nanmedian(np.abs(signed)):.0f} km")
    out['signed900'] = signed
    out['rs900'] = rs
    np.savez(sys.argv[2], lats=lats[::2], lons=lons[::2], z=z[::2, ::2], **out)

    # ---- a second look, decided after seeing where the misfit lies: the stretches fixed beforehand do not face each other
    # at either end (South America's reaches the Guianas and 45 S; Africa's stopped short of the Guinea plateau and of the
    # tip of the Agulhas bank).  Africa's stretch is extended to 12 N and 24 E; nothing else changes.
    print("second look, Africa's stretch extended to 12 N and to 24 E:")
    for depth in (500, 900, 2000):
        sam, afr = margins(lats, lons, z, depth, afr_north=12.0, afr_east=24.0)
        res = best_rotation(sam, afr)
        f, w = res[0]
        plat, plon, ang = pole_of(w)
        sep = float(gc(unit(plat, plon), unit(BULLARD[0], BULLARD[1])) / R * 180 / np.pi)
        rms, rs, g1, k1, g2, k2 = misfit(w, sam, afr, detail=True)
        used = np.concatenate([g1[k1], g2[k2]])
        print(f"   depth {depth:4d} m: Africa's margin {len(afr) * 20} km; best rotation {ang:.2f} deg about {plat:.2f} N, {plon:.2f} E; misfit {f:.1f} km (median distance {np.median(used):.0f} km);"
              f" pole {sep:.1f} deg from Bullard's, angle {ang - BULLARD[2]:+.2f}; Bullard's rotation on these margins: {misfit(wb, sam, afr):.1f} km")
        out[f"x_w{depth}"] = w
        out[f"x_sam{depth}"] = sam
        out[f"x_afr{depth}"] = afr
        out[f"x_f{depth}"] = f
    np.savez(sys.argv[2], lats=lats[::2], lons=lons[::2], z=z[::2, ::2], **out)
