"""In the phone picture of the dial: for each grey joining line, which pair of marks does it end at, and how near does it pass
to every other mark? Distances in the file's pixels and at 350 pixels wide. Marks are found by colour (as in marks.py);
each line is a connected stroke of the grey of the lines. Reads only."""
import json, math
import numpy as np
from PIL import Image
from scipy import ndimage
today = json.load(open('/srv/commons/antikythera-agent3/today.json'))
ORDER = ['moon', 'mercury', 'venus', 'sun', 'mars', 'jupiter', 'saturn']
a = np.asarray(Image.open('/home/agent3/site/build/img/dial-today-phone.png').convert('RGB')).astype(int)
H, W = a.shape[:2]
def near(hexcol, tol):
    c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)]); return np.abs(a - c).sum(axis=2) < tol
cx, cy, step = 529.0, 765.0, 64.53            # centre and ring step as marks.py found them in this picture
def where(b, k):                               # where the file puts a mark: k = 0 the pointer (blue dot), 1 the body (orange ring)
    r = (ORDER.index(b) + 1.4) * step; t = math.radians(today[b][k])
    return cx + r * math.cos(t), cy - r * math.sin(t)
marks = {b: (where(b, 0), where(b, 1)) for b in ORDER}
grey = near('#8f8e88', 45)
lab, k = ndimage.label(grey, structure=np.ones((3, 3)))
s = 350 / W
print(f'picture {W} x {H}; one pixel at 350 wide = {1 / s:.2f} of the file\'s pixels')
for i in range(1, k + 1):
    ys, xs = np.where(lab == i)
    if max(ys.max() - ys.min(), xs.max() - xs.min()) < 80: continue          # the Earth dot and specks
    top = (xs[ys.argmin()], ys.min()); bot = (xs[ys.argmax()], ys.max())
    # the end nearer the centre of the rings is the marks' end
    endm = min((top, bot), key=lambda p: math.hypot(p[0] - cx, p[1] - cy)); endn = top if endm is bot else bot
    dist = {}
    for b in ORDER:
        d = min(min(np.hypot(xs - mx, ys - my).min() for mx, my in marks[b]), 1e9)
        dist[b] = d
    own = min(ORDER, key=lambda b: min(math.hypot(endm[0] - mx, endm[1] - my) for mx, my in marks[b]))
    others = sorted((d, b) for b, d in dist.items() if b != own)
    print(f'  line from the name end at ({endn[0]}, {endn[1]}) to ({endm[0]}, {endm[1]}): ends {dist[own]:.0f} px ({dist[own] * s:.0f} at 350) from the nearer mark of {own.upper()}; '
          f'nearest other mark: {others[0][1]} at {others[0][0]:.0f} px ({others[0][0] * s:.0f} at 350), then {others[1][1]} at {others[1][0]:.0f} px ({others[1][0] * s:.0f} at 350)')
