"""speech.py: each book's cells split between what stands inside double quotation marks and what stands outside them.
    /usr/bin/python3 -I speech.py ~/braille-data/texts OUT.json [WORKERS] [story]
A paragraph is translated whole, as in cells.py. Every character's uncontracted cells, and every group of contracted cells,
go to the bin of the character (for a group: of its first character): 'in' between a quotation mark and the next one in the
paragraph, 'out' otherwise, 'mark' for the marks themselves. A paragraph begins outside; one that ends inside (a speech
carried on into the next paragraph) leaves its last stretch inside."""
import json, os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import louis, cells, run, story

def split(par, table=cells.UEB, g1=cells.G1):
    """{'in': [U, C, letters], 'out': [...], 'mark': [...]} for one paragraph"""
    b1, _, r1, _ = louis.translate([g1], par); b2, _, r2, _ = louis.translate([table], par); n = len(par)
    bins = []; inside = False
    for ch in par:
        if ch == '"': bins.append('mark'); inside = not inside
        else: bins.append('in' if inside else 'out')
    out = {k: [0, 0, 0] for k in ('in', 'out', 'mark')}
    for i in range(n):
        out[bins[i]][0] += (r1[i + 1] if i + 1 < n else len(b1)) - r1[i]; out[bins[i]][2] += par[i].isalpha()
    i = 0
    while i < n:
        j = i + 1
        while j < n and r2[j] == r2[i]: j += 1
        out[bins[i]][1] += (r2[j] if j < n else len(b2)) - r2[i]; i = j
    return out, len(b1), len(b2)

def one(job):
    root, (era, folder, title, year), only = job
    d = os.path.join(root, folder); path = os.path.join(d, [f for f in os.listdir(d) if f.endswith('.txt')][0])
    tot = {k: [0, 0, 0] for k in ('in', 'out', 'mark')}; U = C = 0
    for par in (story.trim(folder)(cells.clean(path)) if only else cells.clean(path)):
        o, u, c = split(par); U += u; C += c
        for k in tot:
            for t in range(3): tot[k][t] += o[k][t]
    return dict(era=era, folder=folder, title=title, year=year, U=U, C=C, **tot)

if __name__ == '__main__':
    root, outp = os.path.expanduser(sys.argv[1]), sys.argv[2]; workers = int(sys.argv[3]) if len(sys.argv) > 3 else 6; only = len(sys.argv) > 4 and sys.argv[4] == 'story'
    with Pool(workers) as pool: recs = pool.map(one, [(root, b, only) for b in run.BOOKS])
    json.dump(recs, open(outp, 'w'), indent=1)
    for r in recs: print('%-36s inside %.2f%%  outside %.2f%%  letters inside %.1f%%' % (r['title'], 100 * (1 - r['in'][1] / max(1, r['in'][0])), 100 * (1 - r['out'][1] / max(1, r['out'][0])), 100 * r['in'][2] / (r['in'][2] + r['out'][2])))
