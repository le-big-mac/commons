"""The wide eclipse chart has two scales. Read the tick marks of its upper (calendar) scale off the picture and turn their
columns into years after 205 BC with the lower scale's own tick marks (0, 200, ... 1600). They should stand at
0, 205, 454, 704, 954, 1204, 1454 (205 BC, AD 1, 250, 500, 750, 1000, 1250), as AD Y at Y + 204. Reads only."""
import numpy as np
from PIL import Image
a = np.asarray(Image.open('/home/agent3/site/build/img/dial-kept-page.png').convert('RGB')).astype(int)
def runs(v):
    out = []; s = None
    for i, x in enumerate(list(v) + [False]):
        if x and s is None: s = i
        if not x and s is not None: out.append((s, i - 1)); s = None
    return out
bg = np.array([252, 252, 251])
notbg = np.abs(a - bg).sum(axis=2) > 20
# lower scale: tick marks just under the foot (row 651.5 found by steps.py)
low = [(s + e) / 2 for s, e in runs(notbg[656:659].all(axis=0)) if e - s < 12]
k = np.polyfit(low, [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600], 1)
print('lower tick marks at columns', low)
# upper scale: short strokes in the rows between the upper labels and the top grid line (row 77.5 is the line at 40; the top of the chart is at 41)
for r0 in range(52, 70):
    cols = [(s + e) / 2 for s, e in runs(notbg[r0:r0 + 3].all(axis=0)) if e - s < 12]
    if len(cols) == 7:
        print(f'upper tick marks (rows {r0}..{r0 + 2}) at columns', cols)
        print('  in years after 205 BC by the lower scale:', [round(float(np.polyval(k, c)), 1) for c in cols], ' expected 0, 205, 454, 704, 954, 1204, 1454')
        break
else:
    print('upper tick marks not found as seven strokes')
