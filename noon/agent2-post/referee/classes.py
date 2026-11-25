"""Are the referee's own lag-3 witnesses (found by annealing, q2.c) inside Noon's 14 classes?  A test that the 72/14 enumeration misses nothing."""
import itertools, glob, numpy as np
codes = [''.join(p) for p in itertools.product('123456', repeat=4)]; idx = {c: i for i, c in enumerate(codes)}
D = np.array([[int(ch) - 1 for ch in c] for c in codes]); w = 6 ** np.arange(3, -1, -1)
G = [(np.array(cp)[D[:, list(pp)]] * w).sum(1) for pp in itertools.permutations(range(4)) for cp in itertools.permutations(range(6))]
def canon(g): return min((int(im[g[0]]),) + tuple(sorted(int(im[x]) for x in g[1:])) for im in G)
noon = set(canon([idx[x] for x in l.split()[1:]]) for l in open('/home/agent2/post/out/K-d3-Q5-all.out') if l.startswith('yes'))
print('Noon classes:', len(noon))
mine = {}
for f in sorted(glob.glob('q2_seed*.out')):
    for l in open(f):
        if l.startswith('WITNESS'):
            g = [int(x) for x in l.split(';')[0].split('=')[1].split()]; c = canon(g)
            mine[f] = c; print(f, ' '.join(codes[x] for x in g), '-> in Noon\'s 14 classes:', c in noon)
print('referee witnesses:', len(mine), '; distinct classes among them:', len(set(mine.values())), '; all inside Noon\'s:', all(c in noon for c in mine.values()))
