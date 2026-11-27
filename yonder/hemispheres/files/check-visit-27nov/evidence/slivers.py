"""The two slivers by set of maps, from the saved table (second-map/out/score.out): which set the page's 41, 30, 92 and 87 million are from,
and on which sets "Alps up to 2010, near Berlin from 2020 on" is a move.
usage: python slivers.py /srv/commons/hemispheres-agent3"""
import sys, os, re
sc = open(os.path.join(sys.argv[1], 'second-map/out/score.out')).read()
rows = []
for line in sc.splitlines():
    p = [x.strip() for x in line.split('|')]
    if len(p) == 10 and p[1][:1].isdigit():
        lat = float(re.search(r'at ([\d.]+) N', p[2]).group(1))
        rows.append((p[0].rsplit(' ', 1)[0], int(p[0].split()[-1]), float(p[7]), float(p[8]), float(p[9]), 'Alps' if lat < 47.5 else 'near Berlin'))
print('set | year | only in the Berlin half (Asian sliver), millions | only in the Alpine half (South American sliver) | difference | best centre')
for s, y, b, v, d, w in rows:
    print(f'{s:22s} {y} | {b:5.1f} -> {round(b):3d} | {v:5.1f} -> {round(v):3d} | {d:+5.1f} (from the rounded pair: {round(b) - round(v):+d}) | {w}')
for s in dict.fromkeys(r[0] for r in rows):
    ws = [(y, w) for ss, y, b, v, d, w in rows if ss == s]
    moved = any(w == 'Alps' for y, w in ws) and any(w == 'near Berlin' for y, w in ws)
    print(f'{s}: {"the centre moves" if moved else "no move seen"}: {ws}')
g = {(s, y): (b, v, d) for s, y, b, v, d, w in rows}
print('the page: "In 1975 ... 41 million against 30 million. By 2020 ... 92 million against 87 million."')
print('   1975 exists only on', sorted(set(s for s, y in g if y == 1975)), '->', g[('GHS-POP R2023A', 1975)])
print('   2020 on the three sets:', {s: g[(s, 2020)] for s, y in g if y == 2020})
