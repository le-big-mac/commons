"""For my eye: an enlarged crop of the southern summit in a trial picture, and the picture as drawn beside the trial at 350 wide.
usage: view_try.py TRIAL.png TAG"""
import sys
from PIL import Image
HERE = '/home/agent3/site/check-pictures-phone/hemi/tryfix'
trial, tag = sys.argv[1], sys.argv[2]
im = Image.open(trial).convert('RGB')
c = im.crop((470, 880, 730, 1110)); c.resize((c.width * 4, c.height * 4), Image.LANCZOS).save(f'{HERE}/south-{tag}.png')
old = Image.open('/home/agent3/site/build/img/hemi-ridge-phone.png').convert('RGB')
h = round(im.height * 350 / im.width)
both = Image.new('RGB', (720, h), (255, 255, 255)); both.paste(old.resize((350, h), Image.LANCZOS), (0, 0)); both.paste(im.resize((350, h), Image.LANCZOS), (370, 0)); both.save(f'{HERE}/both-350-{tag}.png')
print('written', f'{HERE}/south-{tag}.png', f'{HERE}/both-350-{tag}.png')
