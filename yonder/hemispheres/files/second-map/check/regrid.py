"""Independent re-gridding of one 30-arc-second population GeoTIFF onto a 0.05-degree grid, a census of its
special values, a comparison with the author's grid, and hard-edged halves counted on the native pixels.

usage: python -I regrid.py NAME IN.tif AUTHOR_GRID.npy MY_GRID_OUT.npy OUT.json

Written by the checker; does not use popgrid.py, popgrid2.py or hemilib.
Method (differs from the author's bincount of pixel centres): the georeferencing is read from the tags
(ModelPixelScale, ModelTiepoint, raster type); the output cell of every input row and column is worked out with
the exact pixel size 1/120 degree anchored at the tie point; then the raster is summed with np.add.reduceat over
runs of rows and of columns that share a cell. Values counted as people: finite, > 0, and not equal to the
file's no-data value; everything else is censused and reported.
"""
import sys, json, re
import numpy as np
import tifffile

name, path, author_path, my_out, json_out = sys.argv[1:6]
CELL = 0.05
H, W = 3600, 7200
res = {'name': name}

with tifffile.TiffFile(path) as t:
    p = t.pages[0]
    raw = {tag.code: tag.value for tag in p.tags.values() if tag.code in (33550, 33922, 34735, 42113)}
    sx, sy, _ = raw[33550]
    tp = raw[33922]
    gk = raw[34735]
    # GeoKey 1025 = GTRasterTypeGeoKey: 1 = PixelIsArea (tie point is the outer corner of pixel 0,0), 2 = PixelIsPoint
    rtype = None
    for k in range(4, len(gk), 4):
        if gk[k] == 1025:
            rtype = gk[k + 3]
    nd_raw = raw.get(42113)
    nd_txt = nd_raw if isinstance(nd_raw, str) else repr(nd_raw)
    nd_txt = re.sub(r'[^0-9eE+\-.]', '', nd_txt)
    nodata64 = float(nd_txt)
    with np.errstate(over='ignore'):
        nodata32 = np.float32(nodata64)      # may round to +-FLT_MAX or to inf
    a = p.asarray()
print(name, 'shape', a.shape, a.dtype, 'pixel', sx, sy, 'tiepoint', tp, 'raster type key', rtype, 'nodata text', nd_txt, 'as float32', repr(nodata32), flush=True)
assert a.dtype == np.float32 and a.ndim == 2
assert tp[0] == 0 and tp[1] == 0 and tp[2] == 0
assert rtype == 1, 'not PixelIsArea'
nr, nc = a.shape
lon0, lat0 = tp[3], tp[4]
res.update(shape=[nr, nc], pixel=[sx, sy], origin=[lon0, lat0], raster_type=rtype, nodata_text=nd_txt)

# ---------- census of values ----------
FLT_MAX = np.finfo(np.float32).max
cen = dict(nan=0, posinf=0, neginf=0, neg=0, zero=0, pos_lt_1e30=0, ge_1e30=0, eq_nodata=0,
           neg_not_nodata=0, big_not_nodata=0)
neg_min, neg_max = np.inf, -np.inf
pos_max = 0.0
big_min, big_max = np.inf, -np.inf
bins = [0, 1e-6, 1e-3, 1, 1e3, 1e4, 1e5, 2e5, 5e5, 1e6, 1e7, 1e10, 1e20, 1e30]
hist = np.zeros(len(bins) - 1, dtype=np.int64)
tot_pos = 0.0
step = 1024
for r0 in range(0, nr, step):
    b = a[r0:r0 + step]
    n_nan = int(np.isnan(b).sum())
    cen['nan'] += n_nan
    cen['posinf'] += int(np.isposinf(b).sum())
    cen['neginf'] += int(np.isneginf(b).sum())
    m_neg = b < 0
    cen['neg'] += int(m_neg.sum())
    cen['zero'] += int((b == 0).sum())
    m_big = b >= 1e30
    cen['ge_1e30'] += int(m_big.sum())
    m_pos = (b > 0) & ~m_big
    cen['pos_lt_1e30'] += int(m_pos.sum())
    cen['eq_nodata'] += int((b == nodata32).sum())
    if m_neg.any():
        v = b[m_neg]
        neg_min = min(neg_min, float(v.min())); neg_max = max(neg_max, float(v.max()))
        cen['neg_not_nodata'] += int((v != nodata32).sum())
    if m_big.any():
        v = b[m_big]
        big_min = min(big_min, float(v.min())); big_max = max(big_max, float(v.max()))
        cen['big_not_nodata'] += int((v != nodata32).sum())
    if m_pos.any():
        v = b[m_pos]
        pos_max = max(pos_max, float(v.max()))
        hist += np.histogram(v, bins=bins)[0]
        tot_pos += float(v.sum(dtype=np.float64))
cen.update(neg_min=neg_min, neg_max=neg_max, pos_max=pos_max, big_min=big_min, big_max=big_max,
           pixels=int(nr) * int(nc), total_pos_lt_1e30=tot_pos)
assert cen['nan'] + cen['neg'] + cen['zero'] + cen['pos_lt_1e30'] + cen['ge_1e30'] == nr * nc
res['census'] = {k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in cen.items()}
res['hist_bins'] = bins
res['hist_counts'] = hist.tolist()
print(name, 'census', res['census'], flush=True)
print(name, 'positive values by size:', list(zip(bins[:-1], hist.tolist())), flush=True)

# ---------- zero out everything that is not a count of people ----------
# people = finite, > 0, below 1e30.  (Any value >= 1e30 or < 0 or NaN is set to 0; the census above says what they were.)
for r0 in range(0, nr, step):
    b = a[r0:r0 + step]
    bad = ~((b > 0) & (b < 1e30))
    b[bad] = 0

# ---------- my own re-gridding ----------
PIX = 1.0 / 120.0                               # exact 30 arc-seconds; the tag says 0.0083333333
i = np.arange(nr); j = np.arange(nc)
lat_c = lat0 - (i + 0.5) * PIX                  # centre latitude of each row, north to south
lon_c = lon0 + (j + 0.5) * PIX
lon_c = np.where(lon_c >= 180, lon_c - 360, lon_c); lon_c = np.where(lon_c < -180, lon_c + 360, lon_c)
row_cell = np.floor((lat_c + 90) / CELL + 1e-9).astype(np.int64)     # 0 = southernmost band
col_cell = np.floor((lon_c + 180) / CELL + 1e-9).astype(np.int64)
# the same with the tag's own pixel size, to see whether the rounding in the tag moves any row or column
lat_t = lat0 - (i + 0.5) * sy; lon_t = lon0 + (j + 0.5) * sx
row_cell_t = np.floor((lat_t + 90) / CELL).astype(np.int64); col_cell_t = np.floor((lon_t + 180) / CELL).astype(np.int64)
res['rows_moved_by_tag_rounding'] = int((row_cell != row_cell_t).sum())
res['cols_moved_by_tag_rounding'] = int((col_cell != col_cell_t).sum())
# distance of pixel centres from the nearest cell boundary, in pixels (0.5 = centred between boundaries of the 30" lattice)
fr = (lat_c + 90) / CELL; fc = (lon_c + 180) / CELL
res['min_dist_centre_to_cell_boundary_deg'] = float(min(np.abs(fr - np.round(fr)).min(), np.abs(fc - np.round(fc)).min()) * CELL)
assert row_cell.min() >= 0 and row_cell.max() < H and col_cell.min() >= 0 and col_cell.max() < W
assert (np.diff(row_cell) <= 0).all() and (np.diff(col_cell) >= 0).all(), 'cells not monotone (wrap?)'
res['lat_centres'] = [float(lat_c[-1]), float(lat_c[0])]; res['lon_centres'] = [float(lon_c[0]), float(lon_c[-1])]
res['row_cells'] = [int(row_cell.min()), int(row_cell.max())]; res['col_cells'] = [int(col_cell.min()), int(col_cell.max())]
# runs of rows / columns sharing a cell
rstart = np.flatnonzero(np.r_[True, np.diff(row_cell) != 0]); cstart = np.flatnonzero(np.r_[True, np.diff(col_cell) != 0])
res['row_run_lengths'] = sorted(set(np.diff(np.r_[rstart, nr]).tolist())); res['col_run_lengths'] = sorted(set(np.diff(np.r_[cstart, nc]).tolist()))
mine = np.zeros((H, W), dtype=np.float64)
# sum columns first (float64), in chunks of whole row-runs
chunk_runs = 64
for k0 in range(0, len(rstart), chunk_runs):
    rs = rstart[k0:k0 + chunk_runs]
    r_lo = rs[0]; r_hi = rstart[k0 + chunk_runs] if k0 + chunk_runs < len(rstart) else nr
    blk = a[r_lo:r_hi].astype(np.float64)
    cs = np.add.reduceat(blk, cstart, axis=1)
    rr = np.add.reduceat(cs, rs - r_lo, axis=0)
    mine[row_cell[rs][:, None], col_cell[cstart][None, :]] += rr
tot_mine = float(mine.sum())
res['total_mine'] = tot_mine
np.save(my_out, mine)
print(name, f'my total {tot_mine:,.1f}; total of positive values below 1e30 {tot_pos:,.1f}', flush=True)

# ---------- comparison with the author's grid ----------
theirs = np.load(author_path)
assert theirs.shape == (H, W)
d = mine - theirs
res['total_author'] = float(theirs.sum())
res['max_abs_cell_diff'] = float(np.abs(d).max())
nzm = mine > 0; nzt = theirs > 0
res['nonempty_mine'] = int(nzm.sum()); res['nonempty_author'] = int(nzt.sum()); res['nonempty_mismatch'] = int((nzm != nzt).sum())
both = nzm & nzt
rel = np.abs(d[both]) / theirs[both]
res['max_rel_cell_diff'] = float(rel.max()); res['cells_rel_diff_gt_1e-4'] = int((rel > 1e-4).sum())
print(name, f"author's total {res['total_author']:,.1f}; difference {tot_mine - res['total_author']:+.3f}; largest cell difference {res['max_abs_cell_diff']:.4f} people; "
      f"largest relative {res['max_rel_cell_diff']:.2e}; cells differing by more than 1 in 10,000: {res['cells_rel_diff_gt_1e-4']}; emptiness mismatches {res['nonempty_mismatch']}", flush=True)
# a sample of cells: twelve named places, read straight from the raster with independent indexing
PLACES = [('Berlin', 52.52, 13.40), ('Paris', 48.86, 2.35), ('Manila', 14.60, 120.98), ('Sao Paulo', -23.55, -46.63), ('Singapore', 1.35, 103.82),
          ('Lagos', 6.50, 3.35), ('Tokyo', 35.68, 139.75), ('Auckland', -36.85, 174.76), ('Anchorage', 61.20, -149.90), ('Suva', -18.14, 178.44),
          ('Honolulu', 21.31, -157.86), ('Reykjavik', 64.14, -21.93), ('Ushuaia', -54.80, -68.30), ('Tromso', 69.65, 18.96)]
samp = []
for nm, la, lo in PLACES:
    ci = int(np.floor((la + 90) / CELL)); cj = int(np.floor((lo + 180) / CELL))
    lat_s, lat_n = -90 + ci * CELL, -90 + (ci + 1) * CELL; lon_w, lon_e = -180 + cj * CELL, -180 + (cj + 1) * CELL
    # rows whose centre lies in [lat_s, lat_n): solve directly instead of using row_cell
    rows = np.flatnonzero((lat_c >= lat_s - 1e-9) & (lat_c < lat_n - 1e-9)); cols = np.flatnonzero((lon_c >= lon_w - 1e-9) & (lon_c < lon_e - 1e-9))
    direct = float(a[rows.min():rows.max() + 1, cols.min():cols.max() + 1].sum(dtype=np.float64)) if len(rows) and len(cols) else 0.0
    samp.append(dict(place=nm, lat=la, lon=lo, cell=[ci, cj], pixels=[len(rows), len(cols)], direct=direct, mine=float(mine[ci, cj]), author=float(theirs[ci, cj])))
    print(f"   {nm:10s} cell ({ci},{cj}) {len(rows)}x{len(cols)} px: direct {direct:12.2f}  mine {mine[ci, cj]:12.2f}  author {theirs[ci, cj]:12.2f}")
res['sample'] = samp

# ---------- north-south check: is row 0 the north? ----------
# people north of 45 N and south of 45 S, and in four boxes, under the reading "row 0 = north" (the tags' reading)
def box(lat_s, lat_n, lon_w, lon_e):
    rows = np.flatnonzero((lat_c >= lat_s) & (lat_c < lat_n)); cols = np.flatnonzero((lon_c >= lon_w) & (lon_c < lon_e))
    if not len(rows) or not len(cols): return 0.0
    return float(a[rows.min():rows.max() + 1, cols.min():cols.max() + 1].sum(dtype=np.float64))
res['boxes'] = dict(iceland=box(63, 67, -25, -13), new_zealand=box(-48, -34, 166, 179), madagascar=box(-26, -11.5, 43, 51),
                    sri_lanka=box(5.8, 9.9, 79.5, 82), japan_main=box(30, 46, 129, 146), great_britain_ireland=box(49.8, 59, -11, 2),
                    north_of_60N=box(60, 90, -180, 180), south_of_40S=box(-90, -40, -180, 180))
print(name, 'boxes (people):', {k: round(v / 1e6, 3) for k, v in res['boxes'].items()}, 'million', flush=True)

# ---------- hard-edged halves on the native 30" pixels ----------
def unit(la, lo):
    la, lo = np.radians(la), np.radians(lo)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])
CENTRES = dict(berlin=(52.37, 12.68), valais=(46.0, 7.18), palatinate=(49.4, 12.4), rankin=(46.5, 7.0))
la_r = np.radians(lat_c); lo_r = np.radians(lon_c)
native = {}
masks_u = {}
for k, (la, lo) in CENTRES.items():
    c = unit(la, lo)
    u = np.cos(lo_r) * c[0] + np.sin(lo_r) * c[1]           # per column
    thr = -np.sin(la_r) * c[2] / np.cos(la_r)               # per row: inside iff u > thr
    masks_u[k] = (u, thr)
sums = {k: 0.0 for k in CENTRES}; only_b = 0.0; only_v = 0.0
for r0 in range(0, nr, step):
    b = a[r0:r0 + step]
    if not b.any(): continue
    ins = {}
    for k in ('berlin', 'valais', 'palatinate', 'rankin'):
        u, thr = masks_u[k]
        ins[k] = u[None, :] > thr[r0:r0 + step, None]
        sums[k] += float(b.sum(where=ins[k], dtype=np.float64))
    only_b += float(b.sum(where=ins['berlin'] & ~ins['valais'], dtype=np.float64))
    only_v += float(b.sum(where=ins['valais'] & ~ins['berlin'], dtype=np.float64))
tot_native = float(sum(float(a[r0:r0 + step].sum(dtype=np.float64)) for r0 in range(0, nr, step)))
res['native'] = dict(total=tot_native, **{k: v / tot_native for k, v in sums.items()}, only_berlin=only_b, only_valais=only_v,
                     L=100 * (sums['berlin'] - sums['valais']) / tot_native)
print(name, f"native 30\" pixels: total {tot_native:,.0f}; Berlin half {100 * sums['berlin'] / tot_native:.4f}%; Valais half {100 * sums['valais'] / tot_native:.4f}%; "
      f"Palatinate {100 * sums['palatinate'] / tot_native:.4f}%; L {res['native']['L']:+.4f} points; only Berlin {only_b / 1e6:.2f} M; only Valais {only_v / 1e6:.2f} M; "
      f"difference {(only_b - only_v) / 1e6:+.2f} M", flush=True)
json.dump(res, open(json_out, 'w'), indent=1)
print(name, 'done', flush=True)
