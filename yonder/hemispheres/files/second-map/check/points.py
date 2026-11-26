"""What value does each mosaic hold at a few places that are sea, lake, or land with nobody on it?
(To see what the no-data marker stands for: sea only, or sea and empty land.)
usage: python -I points.py NAME=FILE.tif ..."""
import sys
import numpy as np
import tifffile

PTS = [('mid-Atlantic', 0.0, -30.0), ('mid-Pacific', 0.0, -150.0), ('Caspian Sea', 40.0, 51.0), ('Lake Victoria', -1.0, 33.0), ('Lake Superior', 47.7, -87.5),
       ('Sahara (Tenere)', 18.0, 11.0), ('Sahara (Libyan desert)', 25.0, 25.0), ("Rub' al Khali", 20.0, 50.0), ('central Greenland', 72.0, -40.0),
       ('central Australia', -24.0, 127.0), ('Amazon forest', -5.0, -65.0), ('Taklamakan', 39.0, 83.0), ('north Siberia (Taymyr)', 74.0, 100.0),
       ('Antarctic Peninsula', -65.0, -62.0), ('a field in Brandenburg', 52.37, 12.68), ('Val de Bagnes', 46.0, 7.18)]
for spec in sys.argv[1:]:
    name, path = spec.split('=')
    with tifffile.TiffFile(path) as t:
        p = t.pages[0]
        sx, sy, _ = p.tags['ModelPixelScaleTag'].value; tp = p.tags['ModelTiepointTag'].value
        a = p.asarray()
    lon0, lat0 = tp[3], tp[4]
    print(f'== {name}: shape {a.shape}')
    for nm, la, lo in PTS:
        i = int(np.floor((lat0 - la) / sy)); j = int(np.floor((lo - lon0) / sx))
        if not (0 <= i < a.shape[0] and 0 <= j < a.shape[1]):
            print(f'   {nm:26s} outside the raster'); continue
        blk = a[max(i - 30, 0):i + 31, max(j - 30, 0):j + 31]         # about half a degree square around the point
        n_nd = int(((blk < 0) | (blk >= 1e30)).sum()); n_zero = int((blk == 0).sum()); n_pos = int(((blk > 0) & (blk < 1e30)).sum())
        print(f'   {nm:26s} value at the point {a[i, j]!r:>14}; in the 61 x 61 pixels around it: {n_nd} no-data, {n_zero} zero, {n_pos} positive')
