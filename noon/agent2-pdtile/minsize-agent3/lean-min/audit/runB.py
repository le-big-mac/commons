"""Driver for enumB: for every pattern P of a group Z_M = Z_{p^n q}, list EVERY multiset of at most S(P)
elements whose mask polynomial is divisible by Phi_d for all d in P, where S(P) is Lean's value for P plus
`extra`; each such multiset gets its full pattern by remainders modulo every Phi_d.  So for each P the least
size of a multiset with pattern exactly P is found if it is at most S(P), and otherwise is shown to exceed S(P).

Checks after each run: the witness of the least size is divided again in Python (long division) and must
have exactly the pattern claimed; every multiset listed has a pattern that contains P.
Writes outB/<p>_<q>_<n>.json.

usage: runB.py p:q:n[:extra] ...
"""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from math import comb

from cyc import pattern, phi
from rule_note import levels_of, read_lean
from tables import divs, write_group_table, write_target_table

HERE = os.path.dirname(os.path.abspath(__file__))
NW = 8
BIG = 3e8          # above this many nodes a job is split over 8 processes and run alone
FULLMAX = 4e10     # above this many nodes the window bound HMAX = floor(S (M-D) / M) is used (see enumB.c)
CAP = None         # if set: a pattern whose enumeration (with the window bound) would exceed this is not attempted


def max_entry_target(path):
    mx = 0
    with open(path) as f:
        f.readline()
        for ln in f:
            for v in ln.split():
                mx = max(mx, abs(int(v)))
    return mx


def divisor_set(p, q, n, bal, E, F):
    P = set()
    if bal:
        P.add(q)
    for l in E:
        P.add(p ** l)
    for l in F:
        P.add(p ** l * q)
    return P


def run_job(tab, tgt, S, hmax, nworkers, tag):
    env = dict(os.environ, OMP_NUM_THREADS='1')
    outs = [os.path.join(HERE, 'outB', f'{tag}.w{w}.txt') for w in range(nworkers)]
    procs = [subprocess.Popen([os.path.join(HERE, 'enumB'), tab, tgt, str(S), str(hmax), str(w), str(nworkers), outs[w]],
                              env=env)
             for w in range(nworkers)]
    for pr in procs:
        if pr.wait() != 0:
            raise SystemExit(f"enumB failed: {tag}")
    merged = {}
    nodes = 0
    for out in outs:
        with open(out) as f:
            head = f.readline().split()
            nodes += int(head[head.index('nodes') + 1])
            for ln in f:
                t = ln.split()
                mask = int(t[1])
                best = int(t[3])
                i = t.index('counts')
                wit = [int(x) for x in t[5:i]]
                counts = [int(x) for x in t[i + 1:]]
                if mask not in merged:
                    merged[mask] = {'best': best, 'wit': wit, 'counts': counts}
                else:
                    m = merged[mask]
                    m['counts'] = [a + b for a, b in zip(m['counts'], counts)]
                    if best < m['best']:
                        m['best'], m['wit'] = best, wit
        os.remove(out)
    os.remove(tgt)
    return merged, nodes


def run(p, q, n, extra, lean, force_window=False):
    M = p ** n * q
    ds = divs(M)
    idx = {d: i for i, d in enumerate(ds)}
    tab = os.path.join(HERE, 'tab', f'groupB{M}.txt')
    write_group_table(M, tab)
    jobs = []
    for bal in (0, 1):
        for em in range(2 ** n):
            for fm in range(2 ** n):
                kind, a0, kp, x, val, ok = lean[(p, q, n, bal, em, fm)]
                assert ok == 1
                E, F = levels_of(em, n), levels_of(fm, n)
                P = sorted(divisor_set(p, q, n, bal, E, F))
                pmask = sum(1 << idx[d] for d in P)
                S = val + extra
                D = sum(phi(d) for d in P)
                R = M - D
                cost = comb(R + S, S)
                hmax = S
                if cost > FULLMAX or force_window:
                    hmax = (S * R) // M
                    cost = comb(R + hmax, hmax)
                jobs.append(dict(bal=bal, em=em, fm=fm, E=sorted(E), F=sorted(F), P=P, pmask=pmask, S=S, D=D,
                                 hmax=hmax, window=(hmax < S), cost=cost, lean=val, kind=kind, a0=a0))
    assert len(set(j['pmask'] for j in jobs)) == len(jobs) == 2 ** len(ds)   # every set of divisors, once

    for j in jobs:
        j['skipped'] = bool(CAP is not None and j['cost'] > CAP)
        if j['skipped']:
            j['found'] = None
            j['nodes'] = 0

    def do(j, nworkers):
        tag = f"{p}_{q}_{n}.P{j['pmask']}"
        tgt = os.path.join(HERE, 'outB', tag + '.target.txt')
        D = write_target_table(M, j['P'], tgt)
        assert D == j['D']
        assert max(1, max_entry_target(tgt)) * j['S'] < 30000
        t0 = time.time()
        merged, nodes = run_job(tab, tgt, j['S'], j['hmax'], nworkers, tag)
        j['seconds'] = round(time.time() - t0, 1)
        j['nodes'] = nodes
        assert nodes == sum(comb(M - j['D'] + s - 1, s) for s in range(j['hmax'] + 1)), (tag, nodes)
        # every multiset listed has all of P in its pattern
        for mask in merged:
            assert mask & j['pmask'] == j['pmask'], (tag, mask)
        me = merged.get(j['pmask'])
        j['found'] = None
        if me is not None:
            j['found'] = me['best']
            j['wit'] = me['wit']
            assert sum(me['wit']) == me['best']
            assert pattern(M, me['wit']) == frozenset(j['P']), (tag, me['wit'])
            j['count_at_least'] = me['counts'][me['best']]
        # numbers of multisets with pattern containing P, by size (for the cross-check with enumA)
        j['sup_counts'] = [sum(m['counts'][s] for m in merged.values()) for s in range(j['S'] + 1)]
        return j

    t0 = time.time()
    small = [j for j in jobs if j['cost'] <= BIG and not j['skipped']]
    big = sorted([j for j in jobs if j['cost'] > BIG and not j['skipped']], key=lambda j: j['cost'])
    with ThreadPoolExecutor(max_workers=NW) as ex:
        list(ex.map(lambda j: do(j, 1), small))
    for j in big:
        do(j, NW)
    dt = time.time() - t0
    res = {'p': p, 'q': q, 'n': n, 'M': M, 'divisors': ds, 'extra': extra, 'seconds': round(dt, 1), 'jobs': jobs}
    with open(os.path.join(HERE, 'outB', f'{p}_{q}_{n}{"_window" if force_window else ""}.json'), 'w') as f:
        json.dump(res, f)
    eq = sum(1 for j in jobs if j['found'] == j['lean'])
    less = [j for j in jobs if j['found'] is not None and j['found'] < j['lean']]
    none = [j for j in jobs if j['found'] is None and not j['skipped']]
    skipped = [j for j in jobs if j['skipped']]
    more = [j for j in jobs if j['found'] is not None and j['found'] > j['lean']]
    print(f"Z_{M} (p={p}, q={q}, n={n}): {len(jobs)} patterns; not attempted (too large): {len(skipped)}; "
          f"least size found = Lean's value: {eq}; "
          f"smaller than Lean's: {len(less)}; none of size <= Lean's value: {len(none)}; "
          f"found only above Lean's value: {len(more)}; "
          f"largest Lean value {max(j['lean'] for j in jobs)}; patterns done with the window bound: "
          f"{sum(1 for j in jobs if j['window'])}; nodes {sum(j['nodes'] for j in jobs)}; {dt:.1f} s",
          flush=True)
    for j in less + none + more:
        print("   MISMATCH", {k: j[k] for k in ('bal', 'E', 'F', 'P', 'lean', 'found', 'S')}, flush=True)


if __name__ == '__main__':
    lean = read_lean(os.path.join(HERE, 'lean-values.txt'))
    force = '--window' in sys.argv
    for arg in sys.argv[1:]:
        if arg.startswith('--fullmax='):
            FULLMAX = float(arg.split('=')[1])
        if arg.startswith('--cap='):
            CAP = float(arg.split('=')[1])
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            continue
        t = list(map(int, arg.split(':')))
        p, q, n = t[:3]
        extra = t[3] if len(t) > 3 else 0
        run(p, q, n, extra, lean, force_window=force)
