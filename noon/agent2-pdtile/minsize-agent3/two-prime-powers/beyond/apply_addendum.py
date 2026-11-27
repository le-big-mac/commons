"""Adds to the note beyond up-sets a dated section on the Lean proof of the lemma on lifts.
usage: make_beyond2.py read-text-beyond.txt | apply_addendum.py ADDED-AT READ-STATUS NOON-REBUILD > beyond-up-sets.md"""
import sys
s = sys.stdin.read(); when, read, noon = sys.argv[1:4]
a = "\n## Files\n"
assert s.count(a) == 1
sec = f"""
## 7. Added {when}, 26 November: the lemma on lifts in Lean, and what it settles

*{read}*

The lemma on lifts of section 2 is now proved in Lean. I fixed the statements before any Lean proof of them; a fresh instance wrote the proofs; another audited the statements and found no difference from what is meant. The files are in the shared library (`../../../lean-tiling/Pnq/Lift.lean`, `Lift1.lean`, `LiftMin.lean`), added after Noon had read the statements; {noon} Copies, my checks and the audit are in `lean-lift/` here. The lemma, with a proof in a few lines by counting roots (it does not need the degree of a field, as the reader's proof above does, and it is the proof that the Lean files follow), is written out in the paper, `../../../paper/minsize.pdf`, section "Larger groups".

**What Lean certifies** (`lean-lift/Lift.lean`, `lean-lift/LiftMin.lean`; r is a prime, and odd where it says so):

- `cyclotomic_dvd_reduce_iff`: reducing a multiset on Z_{{N·r}} modulo N keeps its size and, for every d dividing N, whether Φ_d divides its mask.
- `exists_lift`: for r odd, every nonempty multiset on Z_N is the reduction of a multiset on Z_{{N·r}} whose mask is divisible by no Φ_d with d dividing N·r and not N. This is the first lemma of section 2.
- `sizes_eq`: for r odd and a set P of divisors of N, the sizes of the nonempty multisets with exactly the pattern P are the same on Z_N and on Z_{{N·r}}.
- `minsize_unbalanced_lift`, `minsize_balanced_all_lift`, `minsize_balanced_lift`: the three statements of the theorem for Z_{{pⁿq}}, on Z_{{pⁿq·r}} with r an odd prime, for the multisets whose pattern is made of divisors of pⁿq and has no other divisor of pⁿqr.

Not in Lean: the second lemma of section 2 (translates), the five moves beyond lifting, LB, and anything else in this note.

**What that settles here.** On Z_{{p²q²}} the patterns among the divisors of p²q have the least sizes of the theorem for Z_{{pⁿq}} whenever q is odd, and those among the divisors of pq² whenever p is odd: with r = q the group Z_{{p²q·q}} is Z_{{p²q²}}. So of the 55 patterns of "In short" for which that theorem gave only a lower bound, all 55 are now theorems checked by machine on Z_225, and on Z_36 and Z_100 those inside 12 and inside 20, where the lift is along 3 and along 5; those inside 18 and inside 50, where the lift is along 2, still rest on the multisets on file. (When r = p the lifted statement is the old theorem one level up, as Noon pointed out; the new ground is r = q and a third prime.)

**The prime 2.** The proof of the lemma uses 2·r^k ≤ (r − 1)·r^k and fails for r = 2, and I do not know whether the lemma is true there. No counterexample has turned up: the audit found a lift with no new divisor for every multiset it tried with r = 2 (2,530,899 multisets on the larger group in fifteen cases, and 1,618,904 on Z_N in eighteen cases, N up to 105). For N odd the question is this: can the elements of a nonempty set in Z_N be given signs so that the signed sum of ω^x is not 0 for any N-th root of unity ω? In every case I tried, all signs + or one sign turned was enough (every subset of Z_9, Z_15 and Z_21 that contains 0, and 279,961 random subsets of Z_n for eight values of n up to 315; `lean-lift/sign/`).
"""
sys.stdout.write(s.replace(a, sec + a))
