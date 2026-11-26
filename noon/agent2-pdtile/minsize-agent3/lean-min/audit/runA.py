"""Driver for enumA: plain enumeration of all multisets of size <= S on Z_M, at most 8 processes.

After the run: (1) the number of multisets of each size s must be C(M+s-1, s); (2) the witness kept for each
pattern is divided again here, by long division in Python, and must have exactly that pattern and that size.
Writes outA/group<M>.json.
"""
import json
import os
import subprocess
import sys
import time
from math import comb

from cyc import pattern
from tables import divs, write_group_table

HERE = os.path.dirname(os.path.abspath(__file__))
NW = 8


def max_entry(path):
    mx = 0
    with open(path) as f:
        M, nd = map(int, f.readline().split())
        for _ in range(nd):
            d, ph = map(int, f.readline().split())
            for _ in range(M):
                for v in f.readline().split():
                    mx = max(mx, abs(int(v)))
    return mx


def run(M, S):
    tab = os.path.join(HERE, 'tab', f'group{M}.txt')
    write_group_table(M, tab)
    assert max_entry(tab) * S < 30000
    env = dict(os.environ, OMP_NUM_THREADS='1')
    t0 = time.time()
    procs = []
    outs = []
    for w in range(NW):
        out = os.path.join(HERE, 'outA', f'group{M}.S{S}.w{w}.txt')
        outs.append(out)
        procs.append(subprocess.Popen([os.path.join(HERE, 'enumA'), tab, str(S), str(w), str(NW), out], env=env))
    for p in procs:
        if p.wait() != 0:
            raise SystemExit(f"enumA failed for M={M}")
    dt = time.time() - t0
    ds = divs(M)
    merged = {}
    for out in outs:
        with open(out) as f:
            head = f.readline().split()
            assert int(head[1]) == M and int(head[3]) == S
            for ln in f:
                t = ln.split()
                mask = int(t[1])
                best = int(t[3])
                i = t.index('counts')
                wit = [int(x) for x in t[5:i]]
                counts = [int(x) for x in t[i + 1:]]
                assert len(counts) == S + 1
                if mask not in merged:
                    merged[mask] = {'best': best, 'wit': wit, 'counts': counts}
                else:
                    m = merged[mask]
                    m['counts'] = [a + b for a, b in zip(m['counts'], counts)]
                    if best < m['best']:
                        m['best'], m['wit'] = best, wit
        os.remove(out)
    # (1) every multiset was visited once
    for s in range(S + 1):
        tot = sum(m['counts'][s] for m in merged.values())
        assert tot == comb(M + s - 1, s), (M, s, tot)
    # (2) witnesses, by long division
    for mask, m in merged.items():
        assert m['best'] == min(s for s in range(S + 1) if m['counts'][s])
        assert len(m['wit']) == m['best']
        w = [0] * M
        for a in m['wit']:
            w[a] += 1
        pat = pattern(M, w)
        assert pat == frozenset(d for i, d in enumerate(ds) if (mask >> i) & 1), (M, mask, m['wit'])
    total = sum(comb(M + s - 1, s) for s in range(S + 1))
    res = {'M': M, 'S': S, 'divisors': ds, 'multisets': total, 'seconds': round(dt, 1),
           'patterns': {str(k): v for k, v in sorted(merged.items())}}
    with open(os.path.join(HERE, 'outA', f'group{M}.json'), 'w') as f:
        json.dump(res, f)
    nonempty = sum(1 for k, v in merged.items() if v['best'] > 0)
    print(f"Z_{M}: every multiset of size <= {S} ({total} multisets, sizes 0..{S}; count for each size is "
          f"C(M+s-1,s)); {len(merged)} patterns met, {dt:.1f} s; witnesses confirmed by long division", flush=True)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        M, S = map(int, arg.split(':'))
        run(M, S)
