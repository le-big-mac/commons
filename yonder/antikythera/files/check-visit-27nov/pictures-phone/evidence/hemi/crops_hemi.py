"""Enlarged crops of places in the two phone pictures (and the same places in the wide ones) for my eye; and all four at 350 wide."""
import os
from PIL import Image
SRC = '/home/agent3/site/build/img'
HERE = '/home/agent3/site/check-pictures-phone/hemi'
os.makedirs(f'{HERE}/crops', exist_ok=True); os.makedirs(f'{HERE}/scaled', exist_ok=True)
def crop(n, box, tag, zoom):
    im = Image.open(f'{SRC}/{n}.png').convert('RGB').crop(box)
    im.resize((im.width * zoom, im.height * zoom), Image.LANCZOS).save(f'{HERE}/crops/{n}-{tag}.png')
crop('hemi-ridge-phone', (470, 880, 730, 1110), 'south', 4)
crop('hemi-ridge-phone', (330, 500, 500, 640), 'north-marks', 5)
crop('hemi-ridge-phone', (20, 245, 330, 545), 'topleft', 3)
crop('hemi-ridge-phone', (390, 400, 700, 520), 'numbers-north', 3)
crop('hemi-ridge-phone', (680, 880, 1040, 1270), 'sardinia', 2)
crop('hemi-ridge-phone', (20, 980, 400, 1270), 'bottomleft', 2)
crop('hemi-ridge', (560, 900, 760, 1060), 'south', 4)
crop('hemi-ridge', (400, 460, 540, 560), 'north-marks', 5)
crop('second-map-phone', (0, 0, 1058, 420), 'top', 1)
crop('second-map-phone', (680, 420, 1058, 860), 'right', 2)
crop('second-map-phone', (180, 1090, 1058, 1310), 'foot', 1)
for n in ['hemi-ridge-phone', 'second-map-phone', 'hemi-ridge', 'second-map']:
    im = Image.open(f'{SRC}/{n}.png').convert('RGB')
    im.resize((350, round(im.height * 350 / im.width)), Image.LANCZOS).save(f'{HERE}/scaled/{n}-350.png')
    print(n, im.size, '-> 350 x', round(im.height * 350 / im.width))
