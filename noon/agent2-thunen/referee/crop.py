import sys
from PIL import Image
p, out, x0, y0, x1, y1, s = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:8])
im = Image.open(p)
c = im.crop((int(x0), int(y0), int(x1), int(y1)))
c = c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)
c.save(out)
print(c.size)
