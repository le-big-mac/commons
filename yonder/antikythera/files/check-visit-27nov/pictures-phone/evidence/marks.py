"""Read the marks back out of the pictures themselves (not out of the programs) and compare with today.json.
For each picture of the dial: find the blue dots and the orange rings by colour, take the centre of the grey Earth dot as the
centre, and give each mark's ring (distance from the centre in ring steps) and its angle, anticlockwise from the right.
Then compare the phone picture with the wide picture and with the file. Reads only."""
import json, sys, math
import numpy as np
from PIL import Image
from scipy import ndimage
SRC = '/home/agent3/site/build/img'
today = json.load(open('/srv/commons/antikythera-agent3/today.json'))
ORDER = ['moon', 'mercury', 'venus', 'sun', 'mars', 'jupiter', 'saturn']
def near(a, hexcol, tol):
    c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)])
    return (np.abs(a - c).sum(axis=2) < tol)
def blobs(mask, minpix):
    lab, n = ndimage.label(mask)
    out = []
    for k in range(1, n + 1):
        ys, xs = np.where(lab == k)
        if len(ys) >= minpix: out.append((xs.mean(), ys.mean(), len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
    return out
res = {}
for n in ['dial-today-phone', 'dial-today-page']:
    a = np.asarray(Image.open(f'{SRC}/{n}.png').convert('RGB')).astype(int)
    H, Wd = a.shape[:2]
    blue = blobs(near(a, '#2a78d6', 60), 60)
    orange = blobs(near(a, '#eb6834', 60), 60)
    grey = [b for b in blobs(near(a, '#8f8e88', 30), 60) if (b[4] - b[3]) < 40 and (b[6] - b[5]) < 40 and abs((b[4] - b[3]) - (b[6] - b[5])) <= 2]
    # the legend's two marks are the lowest blobs; the Earth dot is the round grey blob
    blue = sorted(blue, key=lambda b: b[1])[:-1]; orange = sorted(orange, key=lambda b: b[1])[:-1]
    assert len(grey) == 1, grey
    cx, cy = grey[0][0], grey[0][1]
    print(f'\n{n}: {Wd} x {H}; centre (Earth dot) at {cx:.1f}, {cy:.1f}; blue dots found {len(blue)}, orange rings found {len(orange)}')
    def polar(b): return math.hypot(b[0] - cx, b[1] - cy), math.degrees(math.atan2(-(b[1] - cy), b[0] - cx)) % 360
    # the ring step in pixels: from the outermost marks (Saturn, ring radius 7.4 in the program) -- instead I estimate it from all marks by least squares against whole rings 1.4 .. 7.4
    pol_b = [polar(b) for b in blue]; pol_o = [polar(b) for b in orange]
    rs = sorted(r for r, _ in pol_b)
    step = sum(r * (i + 1.4) for i, r in enumerate(rs)) / sum((i + 1.4) ** 2 for i in range(7))
    print(f'  ring step {step:.2f} px (from the seven blue dots, taking them as on rings 1.4, 2.4 ... 7.4 in order of distance)')
    got = {}
    for name, pol in (('blue', pol_b), ('orange', pol_o)):
        for r, ang in pol:
            ring = r / step; i = round(ring - 1.4)
            got.setdefault(ORDER[i], {})[name] = (ring, ang)
    for i, b in enumerate(ORDER):
        ptr, sky = today[b]
        rb, ab = got[b]['blue']; ro, ao = got[b]['orange']
        dp = (ab - ptr + 180) % 360 - 180; ds = (ao - sky + 180) % 360 - 180
        sep = (ab - ao + 180) % 360 - 180
        print(f'  ring {i + 1} {b:8s} blue dot: ring {rb:5.2f} (should be {i + 1.4}), angle {ab:7.2f} (file: pointer {ptr:7.2f}, off by {dp:+5.2f});  orange ring: ring {ro:5.2f}, angle {ao:7.2f} (file: sky {sky:7.2f}, off by {ds:+5.2f});  blue minus orange {sep:+7.2f}')
    res[n] = got
print('\nphone picture against wide picture, mark by mark (angles in degrees):')
for b in ORDER:
    p, w = res['dial-today-phone'][b], res['dial-today-page'][b]
    print(f'  {b:8s} blue {p["blue"][1]:7.2f} / {w["blue"][1]:7.2f}   orange {p["orange"][1]:7.2f} / {w["orange"][1]:7.2f}   ring {p["blue"][0]:.2f} / {w["blue"][0]:.2f}')
