import sys
import numpy as np
from PIL import Image
p = sys.argv[1]
a = np.asarray(Image.open(p).convert('L')).astype(float)
H, W = a.shape
print('median', np.median(a), 'min', a.min())
thr = 150
dark = a < thr
for y in range(2300, 2450):
    row = dark[y]
    n = row.sum()
    if n > 100:
        xs = np.where(row)[0]
        print('  row', y, n, xs.min(), xs.max())
