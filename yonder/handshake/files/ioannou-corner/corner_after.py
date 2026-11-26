"""After the sealed run (not sealed): which ingredient of the corner gives all-defect? One ingredient changed at a time.
Random start, errors of both kinds at 0% and 2%, 30 runs a cell.   usage: corner_after.py OUT.json"""
import sys, json, time
from multiprocessing import Pool
sys.argv_keep = sys.argv[:]; sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner
CELLS = [('the corner: 30 machines, a third mutated, 500 generations', 30, 1 / 3, 500),
         ('one mutant a generation instead (30 machines, 500 generations)', 30, 1 / 30, 500),
         ('100 machines instead (a third mutated, 500 generations)', 100, 1 / 3, 500),
         ('5,000 generations instead (30 machines, a third mutated)', 30, 1 / 3, 5000),
         ('one mutant a generation and 5,000 generations (30 machines)', 30, 1 / 30, 5000),
         ('100 machines, one mutant a generation, 5,000 generations', 100, 1 / 100, 5000)]
if __name__ == '__main__':
    J = []
    for ci, (name, N, mu, gens) in enumerate(CELLS):
        for r in (0.0, 0.02):
            for s in range(30): J.append((r, r, 0.995, 900000 + 1000 * len(J) + s, gens, N, mu, 1.0, 'random'))
    t = time.time()
    with Pool(14) as p: res = p.map(corner.run, J, chunksize=1)
    json.dump(res, open(sys.argv[1], 'w'))
    T = ([1, 1, 0], [[0, 1], [0, 2], [2, 0]])
    HS = tuple(repr(corner.canonical(corner.FSM(st, *T)))[1:-1].split(' ', 2)[2] for st in (0, 1, 2))
    print(len(res), 'runs in', round(time.time() - t), 's')
    print('cell: error rate, all-defect wins of 30, mean cooperation, runs led by an open-loop machine, runs led by a handshake, commonest leaders')
    k = 0
    for name, N, mu, gens in CELLS:
        for r in (0.0, 0.02):
            c = res[k:k + 30]; k += 30
            from collections import Counter
            lead = Counter(x['top'][8:-1] for x in c).most_common(3)
            print(f'  {name}; {r:.2f}: {sum(x["top_is_alld"] for x in c):2d}  {sum(x["coop"] for x in c) / 30:.3f}  {sum(x["top_open_loop"] for x in c):2d}  {sum(any(h in x["top"] for h in HS) for x in c)}  {lead}')
