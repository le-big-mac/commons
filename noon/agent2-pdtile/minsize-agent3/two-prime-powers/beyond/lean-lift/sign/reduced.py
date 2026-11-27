"""The reduced problem (R).  Types A subset of [r]; counts n_A >= 0 (not all 0), n_A <= prod_{i not in A} q_i;  q_i = p_i - 1 >= 2.
Choose integers m_A = n_A mod 2, |m_A| <= n_A, with for every D subset of [r]:
     Psi_D = sum_A m_A * prod_{i in D} (q_i if i in A else -1)   != 0.
(Psi_D is, up to a positive factor, the value at the base point x* of the D-component of the signed mask, when n_A counts the points
of E agreeing with x* exactly on the coordinates in A.)   Exhaustive over all admissible n.   usage: reduced.py q1 q2 ..."""
import sys, itertools
q = [int(t) for t in sys.argv[1:]]; r = len(q)
types = list(itertools.product((0, 1), repeat=r))
cap = []
for A in types:
    c = 1
    for i in range(r):
        if not A[i]: c *= q[i]
    cap.append(c)
W = [[1] * len(types) for _ in types]
for di, D in enumerate(types):
    for ai, A in enumerate(types):
        w = 1
        for i in range(r):
            if D[i]: w *= (q[i] if A[i] else -1)
        W[di][ai] = w
fails = []; total = 0
for n in itertools.product(*[range(c + 1) for c in cap]):
    if not any(n): continue
    total += 1
    ok = False
    for m in itertools.product(*[range(-k, k + 1, 2) for k in n]):
        if all(sum(w * mm for w, mm in zip(Wd, m)) != 0 for Wd in W): ok = True; break
    if not ok: fails.append(n)
print(f'q = {q}: admissible count vectors {total}; with no solution: {len(fails)}; first: {fails[:8]}  (type order {types})')
