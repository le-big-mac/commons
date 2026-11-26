"""usage: python -I crop.py IN.png OUT.png [x0 y0 x1 y1] [scale]
Writes a crop (or the whole image) of IN.png, optionally rescaled by 'scale', to OUT.png."""
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = 60_000_000
im = Image.open(sys.argv[1]).convert("RGB")
a = sys.argv[3:]
if len(a) >= 4:
    im = im.crop(tuple(int(v) for v in a[:4]))
    a = a[4:]
if a:
    s = float(a[0])
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
im.save(sys.argv[2])
print(im.size)
