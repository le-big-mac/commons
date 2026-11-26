"""Second reader: is the study's canonical() a true test of 'the same machine'? For pairs of eight-state strings (a string and a
mutated copy, and unrelated strings) compare 'same canonical key' with 'same behaviour', the latter worked out directly: walk the
two machines side by side over every sequence of the other's moves and look for a state pair that plays differently.
usage: python -I -B canon_check.py"""
import sys
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner'); sys.path.insert(0, '/srv/commons/welch/src')
import elite
def same_behaviour(A, B):
    seen = set(); todo = [(A[2], B[2])]
    while todo:
        a, b = todo.pop()
        if (a, b) in seen: continue
        seen.add((a, b))
        if A[0][a] != B[0][b]: return False
        for x in (0, 1): todo.append((int(A[1][a][x]), int(B[1][b][x])))
    return True
rng = np.random.default_rng(21); n = agree = same = 0; alld = alld_ok = 0
for trial in range(6000):
    A = elite.rand_string(rng)
    if trial % 3 == 0: A[0][:] = rng.integers(0, 2)                       # some machines of one move only, to make all-defect and all-cooperate common
    if trial % 2: B = elite.mutate_string(A, rng)
    else:
        B = elite.rand_string(rng)
        if trial % 3 == 0: B[0][:] = A[0][0]
    k = elite.canon(A).key() == elite.canon(B).key(); s = same_behaviour(A, B)
    n += 1; agree += k == s; same += s
    if all(v == 1 for v in A[0]):
        alld += 1; alld_ok += elite.canon(A).key() == elite.ALLD.key()
print(f'{n} pairs, {same} of them the same in behaviour: canonical key and direct test agree in {agree}')
print(f'{alld} strings whose every state defects: canonical form is the one-state all-defect in {alld_ok}')
