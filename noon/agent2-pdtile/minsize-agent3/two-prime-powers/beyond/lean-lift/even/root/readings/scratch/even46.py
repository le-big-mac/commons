# even m <= 46: the first text's B_E(m) (its own output) against last night's tables min(b, T2)
import re
from fractions import Fraction as F
E = '/home/agent3/lean/lift-check/even/'
b = {}
for ln in open(E + 'quarter/one/table.out', encoding='utf-8'):
    mo = re.match(r'\s*m =\s*(\d+)\s+tbar =.*\sb =\s*(\d+)/(\d+) =', ln)
    if mo: b[int(mo.group(1))] = float(F(int(mo.group(2)), int(mo.group(3))))
T2 = {}
txt = open(E + 'quarter/two/result.md', encoding='utf-8').read()
i = txt.index('| m | level 0 | Σ_p U_p | COMP | T2(m) |')
for ln in txt[i:].split('\n')[2:17]:
    cells = [x.strip() for x in ln.strip().strip('|').split('|')]
    if cells[0]: T2[int(cells[0])] = float(F(cells[4]))
    for k in (6, 9):
        if cells[k]: T2[int(cells[k])] = float(F(cells[k + 1]))
BE = {}
for ln in open(E + 'root/one/even_3000.out', encoding='utf-8'):
    mo = re.match(r'm =\s*(\d+)\s+level 0.*B_E\(m\) = ([0-9.]+)\s', ln)
    if mo: BE[int(mo.group(1))] = float(mo.group(2))
print('even m <= 46 where B_E(m) < min(b, T2)(m):', [m for m in range(4, 47, 2) if BE[m] < min(b.get(m, 9), T2[m])])
print('last m in table.out:', max(b))
