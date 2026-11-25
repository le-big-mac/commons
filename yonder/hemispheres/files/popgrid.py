"""Aggregate a global population-count GeoTIFF in WGS84 (GHS-POP, 30 arc-seconds) to a regular grid.

usage: popgrid.py IN.tif OUT.npy [CELL_DEG=0.05]

Each input pixel's count is added to the output cell containing the pixel's centre (longitude wrapped into
[-180, 180)). Negative values (no-data) and NaN count as zero. Row 0 of the output is the southernmost band;
column 0 starts at longitude -180. Prints the total, which must equal the sum of the input.
"""
import sys
import numpy as np
import tifffile


def main():
    path, outp = sys.argv[1], sys.argv[2]
    cell = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
    H = round(180 / cell)
    W = round(360 / cell)
    with tifffile.TiffFile(path) as t:
        p = t.pages[0]
        sx, sy, _ = p.tags['ModelPixelScaleTag'].value
        tp = p.tags['ModelTiepointTag'].value
        assert tp[0] == 0 and tp[1] == 0
        lon0, lat0 = tp[3], tp[4]
        nodata = p.tags.get('GDAL_NODATA')
        print('shape', p.shape, 'pixel', sx, sy, 'origin', lon0, lat0, 'nodata', nodata.value if nodata is not None else None)
        a = p.asarray()
    nr, nc = a.shape
    lat = lat0 - (np.arange(nr) + 0.5) * sy
    lon = lon0 + (np.arange(nc) + 0.5) * sx
    lon = (lon + 180) % 360 - 180
    rb = np.clip(np.floor((lat + 90) / cell).astype(np.int64), 0, H - 1)
    cb = np.clip(np.floor((lon + 180) / cell).astype(np.int64), 0, W - 1)
    print('latitude of pixel centres', lat[-1], 'to', lat[0], '; longitude', lon.min(), 'to', lon.max())
    out = np.zeros(H * W, dtype=np.float64)
    total = 0.0
    nneg = nnan = npos = 0
    step = 512
    for r0 in range(0, nr, step):
        blk = a[r0:r0 + step]
        nnan += int(np.isnan(blk).sum())
        nneg += int((blk < 0).sum())
        i, j = np.nonzero(blk > 0)
        v = blk[i, j]
        npos += len(v)
        total += float(v.sum())
        out += np.bincount(rb[r0 + i] * W + cb[j], weights=v, minlength=H * W)
    out = out.reshape(H, W)
    np.save(outp, out)
    print(f'positive pixels {npos:,}; negative {nneg:,}; NaN {nnan:,}')
    print(f'total of input {total:,.0f}; total of output {out.sum():,.0f}; non-empty output cells {int((out > 0).sum()):,}')


if __name__ == '__main__':
    main()
