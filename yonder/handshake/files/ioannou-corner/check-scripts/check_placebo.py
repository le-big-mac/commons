"""Reader's side runs (not sealed, checked by nobody). usage: python -I -B check_placebo.py OUT.json [PROCESSES]

A. Placebo: the corner with selection switched off (strength 0: every machine equally likely to leave offspring, so
   the game and the error rate play no part). If a one-state machine is still the commonest, then that much of the
   corner's outcome is the mutation scheme's doing and not the game's.
B. The cell "one mutant a generation, 30 machines, 500 generations" again from the all-defect start, to see whether
   the eleven runs of thirty not led by all-defect belong to the random start.
"""
import sys, json, time
from multiprocessing import Pool
from collections import Counter
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner

CELLS = [('A placebo: the corner, selection off, random start', 30, 1 / 3, 500, 0.0, 'random'),
         ('A placebo: the corner, selection off, all-defect start', 30, 1 / 3, 500, 0.0, 'alld'),
         ('A placebo: one mutant a generation, 30 machines, 5,000 generations, selection off, random start', 30, 1 / 30, 5000, 0.0, 'random'),
         ('B: one mutant a generation, 30 machines, 500 generations, selection on, all-defect start', 30, 1 / 30, 500, 1.0, 'alld'),
         ('B: one mutant a generation, 30 machines, 500 generations, selection on, random start (new seeds)', 30, 1 / 30, 500, 1.0, 'random')]
if __name__ == '__main__':
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    J = []
    for name, N, mu, gens, beta, start in CELLS:
        for r in (0.0, 0.02):
            for s in range(30): J.append((r, r, 0.995, 7000000 + 1000 * len(J) + s, gens, N, mu, beta, start))
    t = time.time()
    with Pool(procs) as p: res = p.map(corner.run, J, chunksize=1)
    json.dump(res, open(sys.argv[1], 'w'))
    print(len(res), 'runs in', round(time.time() - t), 's')
    print('cell; error rate: commonest machine all-defect / all-cooperate / other (of 30); led by an open-loop machine; mean cooperation; mean all-defect share; states of other leaders')
    k = 0
    for name, N, mu, gens, beta, start in CELLS:
        for r in (0.0, 0.02):
            c = res[k:k + 30]; k += 30
            d = sum(x['top'] == '<fsm s0 0:D[0,0]>' for x in c); a = sum(x['top'] == '<fsm s0 0:C[0,0]>' for x in c)
            print(f'  {name}; {r:.2f}: {d} / {a} / {30 - d - a};  {sum(x["top_open_loop"] for x in c)};  {sum(x["coop"] for x in c) / 30:.3f};  {sum(x["alld_share"] for x in c) / 30:.3f};  '
                  f'{sorted(x["top"].count(":") for x in c if x["top"] not in ("<fsm s0 0:D[0,0]>", "<fsm s0 0:C[0,0]>"))}')
