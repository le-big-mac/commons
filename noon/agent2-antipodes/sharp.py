"""The same count on a sharp fine analysis: GFS 0.25 degree (721 x 1440), 72 times of 2025.

Same zero finder as pairs.py (imported).  Strides 1, 2, 4, 8, 10, 20, 40, 120 = 0.25, 0.5, 1, 2, 2.5, 5, 10, 30 degrees.
usage: python -I sharp.py GFSDIR out.npz [nproc]
"""
import sys, os, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eccodes
from multiprocessing import Pool
import pairs

STRIDES = (1, 2, 4, 8, 10, 20, 40, 120)
KEEP = (1, 10)                                                          # strides whose zeros are kept
SEED, EPS = 20261121, 1e-6


def read(path, want_name=None, want_when=None):
    """one GRIB message -> (721, 1440) array, north to south, from Greenwich eastwards; with checks on what it is"""
    with open(path, 'rb') as f:
        gid = eccodes.codes_grib_new_from_file(f)
        assert gid is not None
        g = lambda k: eccodes.codes_get(gid, k)
        assert (g('Ni'), g('Nj')) == (1440, 721), (g('Ni'), g('Nj'))
        assert abs(g('latitudeOfFirstGridPointInDegrees') - 90) < 1e-9 and abs(g('longitudeOfFirstGridPointInDegrees')) < 1e-9
        assert abs(g('latitudeOfLastGridPointInDegrees') + 90) < 1e-9 and abs(g('longitudeOfLastGridPointInDegrees') - 359.75) < 1e-9
        assert g('iScansNegatively') == 0 and g('jScansPositively') == 0
        if want_name:
            assert g('shortName') == want_name, (path, g('shortName'))
        if want_when:
            assert (g('dataDate'), g('dataTime')) == (int(want_when.strftime('%Y%m%d')), want_when.hour * 100), (path, g('dataDate'), g('dataTime'))
        meta = (g('shortName'), g('typeOfLevel'), g('level'), g('units'))
        v = eccodes.codes_get_values(gid).reshape(721, 1440)
        assert eccodes.codes_grib_new_from_file(f) is None              # exactly one message in the file
        eccodes.codes_release(gid)
    return v, meta


def noise():
    rng = np.random.default_rng(SEED)
    out = []
    for _ in range(2):
        n = rng.uniform(-EPS, EPS, size=(721, 1440))
        n[0, :] = n[0, 0]
        n[-1, :] = n[-1, 0]
        out.append(n)
    return out


def work(args):
    gfsdir, stamp = args
    when = datetime.datetime.strptime(stamp, '%Y%m%d%H')
    T, mT = read(f"{gfsdir}/gfs.{stamp}.tmp.grib2", 't', when)
    P, mP = read(f"{gfsdir}/gfs.{stamp}.prmsl.grib2", 'prmsl', when)
    P = P / 100.0
    assert np.isfinite(T).all() and np.isfinite(P).all() and T.min() > 150 and T.max() < 340 and P.min() > 850 and P.max() < 1100
    polar = max(np.ptp(T[0]), np.ptp(T[-1]), np.ptp(P[0]), np.ptp(P[-1]))  # do the rows at the poles hold one value?
    for F in (T, P):
        F[0, :] = F[0].mean()
        F[-1, :] = F[-1].mean()
    nT, nP = noise()
    T, P = T + nT, P + nP
    counts, kept = [], {}
    for k in STRIDES:
        a, b = T[::k, ::k], P[::k, ::k]
        g1, g2 = a - pairs.anti(a), b - pairs.anti(b)
        assert np.abs(g1 + pairs.anti(g1)).max() < 1e-9
        la, lo = pairs.zeros(g1, g2)
        assert len(la) % 2 == 0, (stamp, k, len(la))
        counts.append(len(la) // 2)
        if k in KEEP:
            kept[k] = np.c_[la, lo]
    return stamp, counts, kept, polar, (mT, mP)


if __name__ == '__main__':
    gfsdir, out = sys.argv[1], sys.argv[2]
    nproc = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    stamps = sorted(os.path.basename(p).split('.')[1] for p in glob.glob(f"{gfsdir}/gfs.*.tmp.grib2"))
    with Pool(nproc) as pool:
        res = pool.map(work, [(gfsdir, s) for s in stamps])
    counts = np.array([r[1] for r in res])
    land, mL = read(f"{gfsdir}/land.grib2")
    save = dict(counts=counts, strides=np.array(STRIDES), stamps=np.array(stamps), land=land)
    for k in KEEP:
        save[f"recs{k}"] = np.concatenate([np.c_[np.full(len(r[2][k]), i), r[2][k]] for i, r in enumerate(res)])
    np.savez(out, **save)
    print("fields:", res[0][4], " land:", mL, " land values:", np.unique(land).tolist())
    print("times:", len(stamps), stamps[0], "to", stamps[-1], "; largest spread of values along a polar row before averaging:", max(r[3] for r in res))
    for j, k in enumerate(STRIDES):
        c = counts[:, j]
        print(f"stride {k:3d} ({0.25 * k:5.2f} degrees): even counts {int((c % 2 == 0).sum())}; mean {c.mean():7.2f}; median {np.median(c):5.0f}; min {c.min()}, max {c.max()}")
