"""Trial 4: trial 3 (the numbers of the three inner lines put by hand, the two innermost in the paper's colour) and, besides,
the two summits' dots drawn after the other three marks, so that the white dot of the northern summit lies whole over the
corner of Ile Dumet's triangle (as drawn now, the triangle lies over the dot).
usage: make_try4.py TRY3.py OUT.py"""
import sys
src = open(sys.argv[1], encoding='utf-8').read()
lines = src.split('\n')
i_s = next(i for i, l in enumerate(lines) if l.startswith("mark(south,"))
i_n = next(i for i, l in enumerate(lines) if l.startswith("mark(northp,"))
i_t = next(i for i, l in enumerate(lines) if l.startswith("mark(") and "'Tarragona'" in l)
assert i_n == i_s + 1 and i_t == i_s + 4
block = lines[i_s:i_s + 2]
new = lines[:i_s] + lines[i_s + 2:i_t + 1] + ['# the two summits last, so that their dots lie over the other marks'] + block + lines[i_t + 1:]
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(new))
print('written', sys.argv[2])
