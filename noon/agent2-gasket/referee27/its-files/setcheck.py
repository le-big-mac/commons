"""Third way, for the SET of curvatures only (covers the strip packing too): breadth-first over
quadruples as sorted value-tuples, all four swaps allowed in any direction, keeping quadruples whose
largest entry is <= M.  Compare the set of curvatures with the C program's file."""
import sys
import numpy as np
QUADS = [(-3, 5, 8, 8), (-4, 5, 20, 21), (-1, 2, 2, 3), (0, 0, 1, 1), (-3, 4, 12, 13), (-2, 3, 6, 7), (-23, 48, 49, 52)]
if __name__ == '__main__':
    M = int(sys.argv[1])
    for q in QUADS:
        start = tuple(sorted(q))
        seen = {start}
        stack = [start]
        curv = set(q)
        while stack:
            Q = stack.pop()
            s = sum(Q)
            for i in range(4):
                n = 2 * (s - Q[i]) - Q[i]
                if n > M:
                    continue
                Q2 = tuple(sorted(Q[:i] + (n,) + Q[i + 1:]))
                if Q2 not in seen:
                    seen.add(Q2); stack.append(Q2); curv.add(n)
        c = np.fromfile('out/g_%s_1e6.bin' % '_'.join(str(x) for x in q), dtype=np.uint32)[:M + 1]
        cset = set(np.nonzero(c)[0].tolist())
        pset = set(k for k in curv if k >= 0)
        print(q, 'M', M, 'quadruples (as value sets):', len(seen), 'distinct curvatures 0..M: python', len(pset), 'C', len(cset),
              'only in python:', sorted(pset - cset)[:5], 'only in C:', sorted(cset - pset)[:5])
