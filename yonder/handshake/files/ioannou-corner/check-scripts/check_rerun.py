"""Reader's rerun with the same seeds. usage: python -I -B check_rerun.py sealed|after [PROCESSES]
sealed: all 480 runs of corner.jobs(30, 500), compared field by field with corner_run.json.
after:  all 360 runs of corner_after.py (its job list rebuilt here from its CELLS), compared with corner_after.json,
        and the table of all-defect wins and handshake leaders worked out again from the file by the reader's own count."""
import sys, json, time
from multiprocessing import Pool
from collections import Counter
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner, corner_after

def same(a, b):
    bad = []
    for k in b:
        if isinstance(b[k], float):
            if abs(a[k] - b[k]) > 1e-12: bad.append(k)
        elif a[k] != b[k]: bad.append(k)
    return bad

if __name__ == '__main__':
    which = sys.argv[1]; procs = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    if which == 'sealed':
        J = corner.jobs(30, 500); old = json.load(open('/home/agent3/welch-prior/corner/corner_run.json'))
    else:
        J = []
        for ci, (name, N, mu, gens) in enumerate(corner_after.CELLS):
            for r in (0.0, 0.02):
                for s in range(30): J.append((r, r, 0.995, 900000 + 1000 * len(J) + s, gens, N, mu, 1.0, 'random'))
        old = json.load(open('/home/agent3/welch-prior/corner/corner_after.json'))
    assert len(J) == len(old) and [j[3] for j in J] == [o['seed'] for o in old]
    t = time.time()
    with Pool(procs) as p: new = p.map(corner.run, J, chunksize=1)
    diff = [(i, same(n, o)) for i, (n, o) in enumerate(zip(new, old)) if same(n, o)]
    print(f'{which}: {len(new)} runs again in {round(time.time() - t)} s on {procs} processes; records differing from the file in any field: {len(diff)}', diff[:5])
    if which == 'after':
        HS = {'<fsm s0 0:D[0,1] 1:D[0,2] 2:C[2,0]>', '<fsm s0 0:D[1,2] 1:D[1,0] 2:C[2,1]>', '<fsm s0 0:C[0,1] 1:D[1,2] 2:D[1,0]>'}
        for ci, (name, N, mu, gens) in enumerate(corner_after.CELLS):
            for ri, r in enumerate((0.0, 0.02)):
                c = old[(2 * ci + ri) * 30:(2 * ci + ri + 1) * 30]
                assert all(x['N'] == N and x['gens'] == gens and abs(x['mu'] - mu) < 1e-15 and x['e_move'] == r and x['e_read'] == r and x['start'] == 'random' for x in c)
                print(f'  N {N:3d}, mutated share {mu:.4f} ({N * mu:.0f} a generation), {gens} generations, both errors {r:.2f}: '
                      f'all-defect commonest {sum(x["top"] == "<fsm s0 0:D[0,0]>" for x in c):2d}, handshake commonest {sum(x["top"] in HS for x in c)}, '
                      f'mean cooperation {sum(x["coop"] for x in c) / 30:.3f}, states of the other leaders {sorted(x["top"].count(":") for x in c if x["top"] != "<fsm s0 0:D[0,0]>")}')
