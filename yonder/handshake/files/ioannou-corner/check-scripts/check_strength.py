"""Reader's side run (not sealed, checked by nobody): the corner as corner.py runs it (a third of the whole population
mutated every generation, 30 machines, 500 generations, random start, errors of both kinds) with the study's selection
made stronger, to see whether strength of selection alone undoes the all-defect outcome.
usage: python -I -B check_strength.py OUT.json [PROCESSES]"""
import sys, json, time
from multiprocessing import Pool
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner
if __name__ == '__main__':
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    J = []
    for beta in (3.0, 10.0, 30.0):
        for r in (0.0, 0.02):
            for s in range(30): J.append((r, r, 0.995, 9000000 + 1000 * len(J) + s, 500, 30, 1 / 3, beta, 'random'))
    t = time.time()
    with Pool(procs) as p: res = p.map(corner.run, J, chunksize=1)
    json.dump(res, open(sys.argv[1], 'w')); print(len(res), 'runs in', round(time.time() - t), 's')
    print('selection strength; error rate: all-defect commonest (of 30); led by an open-loop machine; mean cooperation; mean all-defect share')
    k = 0
    for beta in (3.0, 10.0, 30.0):
        for r in (0.0, 0.02):
            c = res[k:k + 30]; k += 30
            print(f'  {beta:4.0f}; {r:.2f}: {sum(x["top_is_alld"] for x in c):2d};  {sum(x["top_open_loop"] for x in c):2d};  {sum(x["coop"] for x in c) / 30:.3f};  {sum(x["alld_share"] for x in c) / 30:.3f}')
