"""Reduced problem (R) again, splitting by whether the base point x* is in E (n_[r] = 1) or not (n_[r] = 0).
usage: reduced2.py q1 q2 ..."""
import sys, itertools
q = [int(t) for t in sys.argv[1:]]; r = len(q)
types = list(itertools.product((0, 1), repeat=r))
cap = []
for A in types:
    c = 1
    for i in range(r):
        if not A[i]: c *= q[i]
    cap.append(min(c, 3) if sum(A) < r else 1)     # counts capped at 3 to keep the search small (parity and 'at least 2' is what matters)
W = []
for D in types:
    row = []
    for A in types:
        w = 1
        for i in range(r):
            if D[i]: w *= (q[i] if A[i] else -1)
        row.append(w)
    W.append(row)
res = {0: [0, []], 1: [0, []]}
for n in itertools.product(*[range(c + 1) for c in cap]):
    if not any(n): continue
    top = n[-1]; res[top][0] += 1
    ok = False
    for m in itertools.product(*[range(-k, k + 1, 2) for k in n]):
        if all(sum(w * mm for w, mm in zip(Wd, m)) != 0 for Wd in W): ok = True; break
    if not ok: res[top][1].append(n)
for top in (0, 1):
    print(f'q = {q}, base point {"in" if top else "not in"} E: count vectors {res[top][0]}, with no solution {len(res[top][1])}; first: {res[top][1][:5]}')
print('   type order', types)
