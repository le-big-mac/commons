"""Scale each picture to 350 pixels wide (what a phone shows) and measure lettering. Reads only; writes into this folder."""
import sys, os
from PIL import Image
import numpy as np
src = '/home/agent3/site/build/img'
os.makedirs('scaled', exist_ok=True)
for n in ['dial-today-phone', 'dial-kept-phone', 'handshake-popsize-phone', 'dial-today-page', 'dial-kept-page', 'handshake-popsize']:
    im = Image.open(f'{src}/{n}.png').convert('RGB')
    w, h = im.size
    s = im.resize((350, round(h * 350 / w)), Image.LANCZOS)
    s.save(f'scaled/{n}-350.png')
    # the same, shown at twice the size (as a phone with two device pixels to one would show it, roughly): for my eye only
    im.resize((700, round(h * 700 / w)), Image.LANCZOS).save(f'scaled/{n}-700.png')
    print(n, 'full size', w, 'x', h, '-> 350 x', round(h * 350 / w), ' scale', round(350 / w, 4))
