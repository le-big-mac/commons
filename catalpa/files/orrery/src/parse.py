#!/usr/bin/env python3
# Turn Horizons vector tables into simple text: ic.txt (JD0 state per body) and ref.txt (jd body x y z vx vy vz)
import re, sys, os
D = sys.argv[1]
ids = ['10','199','299','399','301','4','5','6','7','8','9']
num = r'([-+]?\d\.\d+E[-+]\d+)'
def rows(path):
    t = open(path).read()
    body = t.split('$$SOE')[1].split('$$EOE')[0]
    out = []
    for m in re.finditer(r'(\d+\.\d+) = A\.D\..*?\n\s*X\s*=\s*'+num+r'\s*Y\s*=\s*'+num+r'\s*Z\s*=\s*'+num+r'\s*\n\s*VX=\s*'+num+r'\s*VY=\s*'+num+r'\s*VZ=\s*'+num, body):
        out.append(m.groups())
    return out
with open(os.path.join(D,'ic.txt'),'w') as f:
    for i in ids:
        r = rows(os.path.join(D,f'h_{i}.txt'))[0]
        f.write(' '.join(r[1:])+'\n')
with open(os.path.join(D,'ref.txt'),'w') as f:
    for k,i in enumerate(ids):
        for r in rows(os.path.join(D,f'ref_{i}.txt')):
            f.write(f'{r[0]} {k} '+' '.join(r[1:])+'\n')
