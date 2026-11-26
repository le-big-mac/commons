"""Does check/recount-at-0435.out reproduce the table of section 5, cell by cell?   usage: table_vs_recount.py README RECOUNT"""
import sys, re
readme = open(sys.argv[1]).read().split('\n'); rec = open(sys.argv[2]).read().split('\n')
T = {}
for l in readme:
    m = re.match(r'\| (\d) \| (\d), (\d) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+ of \d+) \| (\d+ of \d+) \| (\d+ of \d+) \| (\d+ of \d+) \| (\d+) of (\d+)[^|]*\| (\d+ of \d+) \|', l)
    if m: T[int(m[4])] = (m[1], m[2], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[12], m[13], m[14])
R = {}
for l in rec:
    m = re.match(r'(\d) (\d) (\d) (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+ of \d+) \| (\d+ of \d+) \| (\d+ of \d+) \| (\d+ of \d+) \| (\d+) \| (\d+) \(none[^)]*\) \| (\d+ of \d+)', l)
    if m: R[int(m[4])] = (m[1], m[2], m[3], m[5], m[6], m[7], m[8], m[9], m[10], m[11], m[13], m[12], m[14])
print('rows in the note\'s table:', len(T), '| rows in the recount:', len(R))
bad = 0
for order in sorted(T):
    same = T[order] == R.get(order)
    bad += not same
    print(order, 'same in all 13 cells' if same else f'DIFFERENT: note {T[order]} recount {R.get(order)}')
print('rows that differ:', bad)
