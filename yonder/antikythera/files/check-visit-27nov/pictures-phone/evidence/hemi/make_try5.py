"""Trial 5: a copy of ridge_phone.py in which every number on the lines is put by hand (nine numbers; the tenth, which the
frame cut at the top left corner, is left out), the two innermost in the paper's colour because they stand on the darkest blues.
usage: make_try5.py OUT.py"""
import sys
src = open('/home/agent3/site/build/figs/ridge_phone.py', encoding='utf-8').read()
old = "ax.clabel(cs, fmt=lambda v: f'{v:g}', fontsize=8.5, colors=INK, inline_spacing=2)\n"
assert src.count(old) == 1
new = ("# the numbers on the lines are put by hand, clear of the coast, the marks, the names and the joining lines (km east and north of the middle of the map):\n"
       "# 0.01 at the foot of its ring; 0.05 on each of its two rings; 0.1 and 0.2 in the Bay of Biscay; 0.4 and 0.8 once on each side.\n"
       "# The two innermost are in the paper's colour: they stand on the two darkest blues, where ink is hard to read.\n"
       "SPOTS = [(105, -482), (-56.4, 122.3), (55.6, -133.4), (-300.2, 200.2), (-483.5, 255.7), (-523.1, -211.3), (322.5, -8.3), (-508.2, -778.4), (558.8, -200.2)]\n"
       "ax.clabel(cs, fmt=lambda v: f'{v:g}', fontsize=8.5, colors=[SURF, SURF, INK, INK, INK, INK], inline_spacing=2, manual=SPOTS)\n")
open(sys.argv[1], 'w', encoding='utf-8').write(src.replace(old, new))
print('written', sys.argv[1])
