import re
chk = open('/home/agent3/antikythera/check.md').read()
sec = chk.split('## Changes I would make')[1].split('## Could not check')[0]
mended = open('/home/agent3/antikythera-check2/mended.txt').read()
first = open('/home/agent3/antikythera-check2/first.txt').read()
items = re.findall(r'^(\d+)\. (.*)$', sec, flags=re.M)
for n, body in items:
    quoted = re.findall(r'"((?:[^"]|"(?=[a-z]))*?)"(?=[ ,.;:)]|$)', body)
    print(f'--- {n}: {len(quoted)} quoted strings')
    for q in quoted:
        q2 = q.replace("'Theory'", '"Theory"').replace("'phase'", '"phase"')
        print(f'    in first: {q in first!s:5}  in mended: {q2 in mended!s:5}  | {q[:70]}{"..." if len(q)>70 else ""}')
print('=== the four with a difference: strip my attributions and test again')
m2 = mended.replace("; the reader's figures.)", ".)").replace(" (the reader's reckoning)", "").replace(" (the reader's figures, `check-scripts/check5.out`)", "").replace(" (the reader's figures)", "")
for n, body in items:
    if n in ('10', '12', '21', '23'):
        q = re.findall(r'→ "(.*)"$', body)[0]
        q2 = q.replace("'Theory'", '"Theory"').replace("'phase'", '"phase"')
        print(n, q2 in m2)
