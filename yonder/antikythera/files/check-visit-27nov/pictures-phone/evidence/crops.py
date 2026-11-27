"""Enlarged crops of the places I want to look at closely (full-size pixels, then enlarged). Reads only."""
import os
from PIL import Image
src = '/home/agent3/site/build/img'
os.makedirs('crops', exist_ok=True)
def crop(n, box, tag, zoom=2):
    im = Image.open(f'{src}/{n}.png').convert('RGB').crop(box)
    im = im.resize((im.width * zoom, im.height * zoom), Image.LANCZOS)
    im.save(f'crops/{n}-{tag}.png'); print(n, tag, im.size)
crop('dial-kept-phone', (640, 440, 1058, 960), 'zeros', 2)
crop('dial-kept-phone', (0, 0, 720, 300), 'topleft', 2)
crop('dial-kept-phone', (100, 620, 560, 800), 'sunlabel', 2)
crop('handshake-popsize-phone', (200, 120, 720, 460), 'left', 2)
crop('handshake-popsize-phone', (740, 110, 1058, 330), 'right', 3)
crop('dial-today-phone', (0, 30, 480, 640), 'topleft', 2)
crop('dial-today-phone', (240, 760, 800, 1460), 'bottom', 1)
