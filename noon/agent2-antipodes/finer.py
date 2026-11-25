"""The same count on a finer grid: 20CRv3, 1980, 1 degree (181 x 360), three-hourly.

Same zero finder as pairs.py (imported), at strides 1, 2, 3, 5, 10, 15, 30 (grids of 1 to 30 degrees).
usage: python -I finer.py DATADIR out.npz [nproc]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import h5py
from multiprocessing import Pool
import pairs

STRIDES = (1, 2, 3, 5, 10, 15, 30)
SEED, EPS = 20261121, 1e-6


def noise():
    rng = np.random.default_rng(SEED)
    out = []
    for _ in range(2):
        n = rng.uniform(-EPS, EPS, size=(181, 360))
        n[0, :] = n[0, 0]
        n[-1, :] = n[-1, 0]                                             # one value at each pole
        out.append(n)
    return out


def work(args):
    datadir, t0, t1 = args
    nT, nP = noise()
    with h5py.File(datadir + '/air.sig995.1980.nc', 'r') as fa, h5py.File(datadir + '/prmsl.1980.nc', 'r') as fp:
        T = fa['air'][t0:t1].astype(np.float64)[:, ::-1, :]            # the files run south to north; turn them round
        P = fp['prmsl'][t0:t1].astype(np.float64)[:, ::-1, :] / 100.0   # hPa
    assert np.isfinite(T).all() and np.isfinite(P).all() and T.min() > 150 and T.max() < 340 and P.min() > 850 and P.max() < 1100
    assert np.ptp(T[:, 0, :], axis=1).max() == 0 and np.ptp(T[:, -1, :], axis=1).max() == 0
    assert np.ptp(P[:, 0, :], axis=1).max() == 0 and np.ptp(P[:, -1, :], axis=1).max() == 0      # one value at each pole
    T, P = T + nT, P + nP
    counts = np.zeros((t1 - t0, len(STRIDES)), int)
    recs = []
    for i in range(t1 - t0):
        for j, k in enumerate(STRIDES):
            a, b = T[i, ::k, ::k], P[i, ::k, ::k]
            g1, g2 = a - pairs.anti(a), b - pairs.anti(b)
            assert np.abs(g1 + pairs.anti(g1)).max() < 1e-9
            la, lo = pairs.zeros(g1, g2)
            assert len(la) % 2 == 0, (t0 + i, k, len(la))               # zeros come in antipodal pairs
            counts[i, j] = len(la) // 2
            if k == 1:
                recs += [(t0 + i, x, y) for x, y in zip(la, lo)]
    return t0, counts, np.array(recs).reshape(-1, 3)


if __name__ == '__main__':
    datadir, out = sys.argv[1], sys.argv[2]
    nproc = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    with h5py.File(datadir + '/air.sig995.1980.nc', 'r') as fa, h5py.File(datadir + '/prmsl.1980.nc', 'r') as fp:
        lat, lon, time = fa['lat'][...], fa['lon'][...], fa['time'][...]
        assert np.array_equal(time, fp['time'][...]) and np.array_equal(lat, fp['lat'][...]) and np.array_equal(lon, fp['lon'][...])
        assert fa['air'].shape == fp['prmsl'].shape == (len(time), 181, 360)
    assert np.allclose(lat, np.linspace(-90, 90, 181)) and np.allclose(lon, np.arange(360.0))
    step = 48
    jobs = [(datadir, t, min(t + step, len(time))) for t in range(0, len(time), step)]
    with Pool(nproc) as pool:
        res = sorted(pool.map(work, jobs), key=lambda r: r[0])
    counts = np.concatenate([r[1] for r in res])
    recs = np.concatenate([r[2] for r in res])
    np.savez(out, counts=counts, recs=recs, time=time, strides=np.array(STRIDES))
    print("times:", len(time))
    for j, k in enumerate(STRIDES):
        c = counts[:, j]
        print(f"stride {k:2d} ({k:2d} degrees): even counts {int((c % 2 == 0).sum())}; mean {c.mean():7.2f}; median {np.median(c):5.0f}; min {c.min()}, max {c.max()}")
