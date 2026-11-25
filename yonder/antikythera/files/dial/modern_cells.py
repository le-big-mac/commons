"""Which cells of the dial today's eclipses fall in (catalogue lunation numbers; lunar + 27257, solar + 27256).
usage: modern_cells.py CATDIR     (the folder holding LE2001-2100.html and SE2001-2100.html; under -I through runpy)"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import dial
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)')
lunar, solar = dial.glyph_months()
for pre, add, marked in (('LE', 27257, sorted(lunar)), ('SE', 27256, sorted(solar))):
    out = []
    for line in open(os.path.join(sys.argv[1], pre + '2001-2100.html'), encoding='utf-8', errors='replace'):
        m = pat.match(re.sub(r'<[^>]*>', '', line))
        if m and 2024 <= int(m.group(2)) <= 2026:
            n = int(m.group(9)) + add; cell = (n - 1) % 223 + 1
            near = min(marked, key=lambda c: abs(c - cell))
            out.append(f'{m.group(2)} {m.group(3)} {m.group(4)} ({m.group(11)[0]}): month {n}, cell {cell}, nearest marked cell {near}')
    print(pre, *out, sep='\n  ')
