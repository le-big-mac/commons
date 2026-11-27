"""For my eye: the three northern marks, enlarged, as drawn (left) and in a trial (right); and the whole trial at 350 wide.
usage: view_north.py TRIAL.png TAG"""
import sys
from PIL import Image
HERE = '/home/agent3/site/check-pictures-phone/hemi/tryfix'
box = (330, 500, 500, 640)
a = Image.open('/home/agent3/site/build/img/hemi-ridge-phone.png').convert('RGB').crop(box); b = Image.open(sys.argv[1]).convert('RGB').crop(box)
z = 4
both = Image.new('RGB', (a.width * z * 2 + 20, a.height * z), (255, 255, 255))
both.paste(a.resize((a.width * z, a.height * z), Image.LANCZOS), (0, 0)); both.paste(b.resize((b.width * z, b.height * z), Image.LANCZOS), (a.width * z + 20, 0))
both.save(f'{HERE}/north-{sys.argv[2]}.png')
im = Image.open(sys.argv[1]).convert('RGB'); im.resize((350, round(im.height * 350 / im.width)), Image.LANCZOS).save(f'{HERE}/whole-350-{sys.argv[2]}.png')
print('written')
