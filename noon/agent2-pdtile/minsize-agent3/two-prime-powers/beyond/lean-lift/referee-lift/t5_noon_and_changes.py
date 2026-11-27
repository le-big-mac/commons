"""(1) Were the three texts changed only in the passages about Noon's rebuild?  Put the old wording back (as I read it before) and compare
the byte counts with those of the files as first listed (61213, 32741, 23843 bytes).
(2) Noon's trial of exists_lift, redone with my own code: every multiset of 1..4 elements on Z_N, N = 1..8, r = 3, and of 1..3 elements on
Z_N, N = 1..6, r = 5: is there a lift with no new divisor (search over all lifts)?   usage: python -I t5_noon_and_changes.py"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift')
import itertools, hashlib
from cyc import divisors, pattern
def rd(p): return open(p, encoding='utf-8').read()
A = rd('/home/agent3/paper/minsize.tex')
newA = ", and Noon did the same in a copy of its own, with the same count of jobs, the three check files printing $95$ lines that each name only the three axioms. Noon also tried \\lean{exists\\_lift} by brute force, with nothing from the proof, on $1{,}481$ small multisets for $r=3$ and $r=5$: each had a lift."
print('A: new passage occurs', A.count(newA), 'time(s); bytes with the old wording put back:', len(A.replace(newA, '.').encode()), '(first listed: 61213)')
B = rd('/home/agent3/pq2/rule/beyond-up-sets.candidate.md')
newB = ", and Noon did the same in a copy of its own (18,459 jobs; 95 lines from the three check files, each with the standard three axioms; `../../../lean-lift-rebuild-26nov-agent2.log`). Noon also tried the lemma by brute force, with nothing from the proof, on 1,481 small multisets for r = 3 and r = 5, and found a lift for each (`../../../lean-lift-try-26nov-agent2.out`)."
print('B: new passage occurs', B.count(newB), 'time(s); bytes with the old wording put back:', len(B.replace(newB, '.').encode()), '(first listed: 32741)')
C = rd('/home/agent3/door/README.candidate.md')
newC = "Noon read the seven statements before the files were put with the others. After that Noon and I each ran the checking program on the whole library again, from nothing, in copies of our own; and Noon tried the lemma by plain search on 1,481 small markings for r = 3 and r = 5, and found a copy for each."
oldC = "Noon read the seven statements before the files were put with the others, and I then ran the checking program on the whole library again, from nothing, with them in it."
print('C: new passage occurs', C.count(newC), 'time(s); bytes with the old wording put back:', len(C.replace(newC, oldC).encode()), '(first listed: 23843)')
for name, t in (('minsize.tex', A), ('beyond-up-sets.candidate.md', B), ('README.candidate.md', C)):
    print('   sha256 as read now:', hashlib.sha256(t.encode()).hexdigest(), name)
print("(2) Noon's trial redone")
tot = 0; nolift = 0
for r, Ns, S in ((3, range(1, 9), 4), (5, range(1, 7), 3)):
    for N in Ns:
        M = N * r; new = [d for d in divisors(M) if N % d]; cnt = 0; bad = 0
        for s in range(1, S + 1):
            for w in itertools.combinations_with_replacement(range(N), s):
                cnt += 1; found = False
                for js in itertools.product(range(r), repeat=s):
                    P = pattern([x + j * N for x, j in zip(w, js)], M, with_one=True)
                    if not any(d in P for d in new): found = True; break
                bad += not found
        tot += cnt; nolift += bad
        print(f'   r = {r}, N = {N}: {cnt} multisets of 1 to {S} elements; without a lift free of new divisors: {bad}')
print(f'   total {tot} multisets (Noon: 1,481); without a lift: {nolift}')
