"""Reader's attempt to reproduce the dry run of the scorer that the sealed sheet describes ("eight runs of 30
generations"). The dry run's own files are not in the folder; this guesses that it was corner.jobs(1, 30) kept at
rates 0 and 2%, which is eight runs, and that the scorer then put them in four cells of two.  usage: python -I -B dryrun_guess.py"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner
from collections import defaultdict
J = [j for j in corner.jobs(1, 30) if j[0] in (0.0, 0.02)]
print(len(J), 'runs')
cell = defaultdict(list)
for j in J:
    r = corner.run(j); cell[(r['start'], r['e_move'])].append(r)
for k in sorted(cell):
    c = cell[k]; print(k, len(c), 'all-defect commonest in', sum(x['top_is_alld'] for x in c), 'cooperation %.2f' % (sum(x['coop'] for x in c) / len(c)), [x['top'] for x in c])
