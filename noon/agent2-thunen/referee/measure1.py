import sys
import numpy as np
from PIL import Image
p = sys.argv[1]
im = Image.open(p).convert('L')
a = np.asarray(im).astype(float)
print(a.shape)
H, W = a.shape
dark = a < 110
# scale bar: look for the long horizontal line near the foot (display y~1077 -> orig ~1434)
for y in range(1380, 1500):
    row = dark[y]
    n = row.sum()
    if n > 300:
        xs = np.where(row)[0]
        print('row', y, n, xs.min(), xs.max())
