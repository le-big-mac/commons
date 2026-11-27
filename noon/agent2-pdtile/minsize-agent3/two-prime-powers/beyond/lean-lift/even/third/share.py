"""Exploration (mine): the exact share of good signings of a given multiset on Z_n, and the share bad at each d | n.
usage: share.py N x1 x2 ...     (exact arithmetic modulo Phi_d, all signings with the first sign +)"""
import sys, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('confirm', '/home/agent3/lean/lift-check/even/confirm.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
n = int(sys.argv[1]); e = [int(x) % n for x in sys.argv[2:]]
R = C.rows(n); S = C.signs(len(e)); good = np.ones(len(S), bool); out = []
for d in sorted(R):
    bad = ~np.any(S @ R[d][e], axis=1); good &= ~bad
    if bad.any(): out.append((d, int(bad.sum())))
print(f'n={n} m={len(e)} elements {sorted(e)}')
print(f'share of good signings: {int(good.sum())}/{len(S)} = {good.mean():.4f}')
print('bad at d (number of signings of', len(S), '):', ', '.join(f'{d}:{b}' for d, b in out))
