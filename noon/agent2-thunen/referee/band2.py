# Plate II: the forest band beside the river where the river runs near vertical. Near-vertical thick lines in a band of rows.
import sys
import numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
PX = 20.04; cx, cy = 773.5, 1342.0
for mi in (17, 18, 19, 20, 24, 25, 26):
    y = int(round(cy + mi * PX))
    x0 = int(cx - 14 * PX); x1 = int(cx - 1 * PX)
    band = (255 - a[y - 6:y + 7, x0:x1]).min(axis=0)      # ink present in all 13 rows: a near-vertical line
    xs = np.where(band > 90)[0]
    groups = []
    for x in xs:
        if groups and x - groups[-1][-1] <= 2: groups[-1].append(x)
        else: groups.append([x])
    print('%2d mi down: near-vertical lines at' % mi, ' '.join('%.2f' % ((x0 + np.mean(g) - cx) / PX) for g in groups))
