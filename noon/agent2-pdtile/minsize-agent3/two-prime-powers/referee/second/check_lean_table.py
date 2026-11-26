"""CheckUpsetTable.lean (the table of 34 up-sets evaluated in Lean) against the author's solver files: are the 34 rows exactly the up-sets
his solver had decided in Z_36 and Z_100, with its values?  Reads only."""
import re, json, glob, sys
sys.path.insert(0, '/home/agent3/pq2/referee/two-powers')
from lib import is_upset, corners
src = open('/home/agent3/lean/up-skeleton/CheckUpsetTable.lean').read()
rows = [(int(a), frozenset(int(x) for x in b.split(',') if x.strip()), int(c)) for a, b, c in re.findall(r'\((\d+), \[([^\]]*)\], (\d+)\)', src)]
print('rows in the Lean table:', len(rows), '; Z_36:', sum(1 for r in rows if r[0] == 36), '; Z_100:', sum(1 for r in rows if r[0] == 100))
for M in (36, 100):
    G = {}
    for f in sorted(glob.glob(f'/home/agent3/pq2/out/z{M}-[0-9].jsonl')):          # the first runs only (what existed for up-sets)
        for l in open(f):
            r = json.loads(l); G[frozenset(r['D'])] = r
    dec_ups = {D: r['min'] for D, r in G.items() if r['proved'] and r['min'] is not None and is_upset(M, D)}
    tab = {D: v for m, D, v in rows if m == M}
    print(f'Z_{M}: up-sets decided by the solver: {len(dec_ups)}; same set of patterns as the Lean table: {set(dec_ups) == set(tab)}; same values: {all(dec_ups[D] == tab[D] for D in tab if D in dec_ups)}; '
          f'each equal to the corner sum by my own corners(): {all(sum(M // c for c in corners(M, D)) == v for D, v in tab.items())}')
