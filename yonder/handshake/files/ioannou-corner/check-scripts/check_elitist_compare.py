"""Reader's comparison of the two writings of the elitist side run at zero error, 120 fresh seeds each, to see whether
their difference in the first batches (6 and 8 of 30 against 1 of 30) is chance. usage: python -I -B check_elitist_compare.py [PROCESSES]"""
import sys
from multiprocessing import Pool
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner/check-scripts')
import check_elitist, check_elitist_again
if __name__ == '__main__':
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    with Pool(procs) as p:
        a = p.map(check_elitist.run, [(0.0, 8100000 + 1000 * i, 500, 1.0) for i in range(120)], chunksize=1)
        b = p.map(check_elitist_again.run, [(0.0, 8200000 + 1000 * i) for i in range(120)], chunksize=1)
    for lo in range(0, 120, 30):
        print('batch', lo // 30, ': first writing', sum(x['top_is_alld'] for x in a[lo:lo + 30]), 'of 30; second writing', sum(x[1] == '<fsm s0 0:D[0,0]>' for x in b[lo:lo + 30]), 'of 30')
    print('zero error, all ten newcomers mutated: first writing all-defect commonest in', sum(x['top_is_alld'] for x in a), 'of 120, mean cooperation %.3f;' % (sum(x['coop'] for x in a) / 120),
          'second writing', sum(x[1] == '<fsm s0 0:D[0,0]>' for x in b), 'of 120, mean cooperation %.3f' % (sum(x[2] for x in b) / 120))
