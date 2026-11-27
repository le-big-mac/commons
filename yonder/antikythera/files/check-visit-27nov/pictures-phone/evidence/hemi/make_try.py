"""Write a trial copy of ridge_phone.py into my own folder with one line changed: where the numbers stand on the lines.
The numbers of the lines 0.1, 0.4 and 0.8 are left to matplotlib as before; those of 0.01, 0.05 and 0.2 are put at spots given by hand.
usage: make_try.py OUT.py "x,y;x,y;..."     (the spots, in km east and north of the middle of the map)"""
import sys
src = open('/home/agent3/site/build/figs/ridge_phone.py', encoding='utf-8').read()
old = "ax.clabel(cs, fmt=lambda v: f'{v:g}', fontsize=8.5, colors=INK, inline_spacing=2)\n"
assert src.count(old) == 1
spots = [tuple(float(v) for v in p.split(',')) for p in sys.argv[2].split(';')]
COLS = '[SURF, SURF, INK]' if len(sys.argv) > 3 and sys.argv[3] == 'pale' else 'INK'      # pale: the numbers of the two innermost lines in the paper's colour, since they stand on the darkest blues
new = ("ax.clabel(cs, levels=[0.1, 0.4, 0.8], fmt=lambda v: f'{v:g}', fontsize=8.5, colors=INK, inline_spacing=2)\n"
       "# the numbers of the three inner lines are put by hand, clear of the coast, the marks and the names (km east and north of the middle of the map):\n"
       "# 0.01 at the foot of its ring, 0.05 once on each of its two rings, 0.2 in the Bay of Biscay\n"
       f"ax.clabel(cs, levels=[0.01, 0.05, 0.2], fmt=lambda v: f'{{v:g}}', fontsize=8.5, colors={COLS}, inline_spacing=2, manual={spots!r})\n")
open(sys.argv[1], 'w', encoding='utf-8').write(src.replace(old, new))
print('written', sys.argv[1], 'with spots', spots)
