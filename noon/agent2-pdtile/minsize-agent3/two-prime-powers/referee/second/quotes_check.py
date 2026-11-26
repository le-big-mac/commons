"""Every sentence the second report quotes from the note 'as it stands': is it in note/README.md (and the table headers) word for word?  Reads only."""
note = open('/home/agent3/pq2/note/README.md').read()
t36 = open('/home/agent3/pq2/note/table-36.md').read(); t100 = open('/home/agent3/pq2/note/table-100.md').read()
Q = [
 "the least size by theorem where a theorem gives it (Theorem S for the 19 up-sets, the theorem for Z_{pⁿq} for 55 more patterns that use only the divisors of p²q or only those of pq²)",
 "For one of them the theorem for Z_{pⁿq} gives the least size, and the smallest multiset found has that size.",
 "from statements I had fixed before any proof of them existed",
 "before any proof was begun",
 "My solver decided 248 and 172 of them in a minute each;",
 "So the \"least\" column of the table as I first made it was not least in nine of the rows it did not mark proved",
 "It stays in the one group Z_M, and uses neither Lemma A nor a second modulus.",
 "which are the only definitions of this file that a reader has to trust",
 "Not in Lean: Corollaries T and P, the statement on minimisers, the proposition on sets, the three-prime statements, and everything about patterns that are not up-sets.",
 "collect the summands by corner. ∎",
 "a function A ≥ 0 that is N_k-periodic and has Â = 0 at every character whose order is in D is a sum of functions ≥ 0, each periodic under some divisor of M that is not in D",
 "for two other primes p, p′ of M",
 "After they were added a fresh copy of the 85 files of the shared folder was rebuilt from nothing: 18,453 jobs, no error",
 "and `#print axioms` gives `[propext, Classical.choice, Quot.sound]` for each of the three theorems (`lean/lean-upset-private-build.log`)",
 "I had also checked by evaluation in Lean that the sum of M/c over `corners` equals the least size my solver had proved on the 34 up-sets it had decided in Z_36 and Z_100 (`lean/CheckUpsetTable.lean`)",
 "and tested the three statements, translated from the Lean text, by exhaustive search in 22 small groups",
 "Its remarks: the hypothesis p ≠ q is not needed",
 "For Z_36 and Z_100 the least size is now known for 256 and 240 of the 256 patterns.",
 "which gives the 248 of sections 3 and 4.) (The parenthesis before this one is the referee's wording; the 248 it speaks of is now in \"In short\" and in section 4.",
 "and is dated 26 November 2026",
 "(each below one term of the corner sum)",
 "added with Noon's word after Noon had read the statements (my board, 15:51 UTC)",
 "It says it read S1 to S3 line by line, and it reports on each step of S4 and S5.",
 "since for a prime p in which s has a higher exponent than c, (X^s − 1)/(X^{s/p} − 1) is the product of the Φ_e with e | s, e ∤ s/p, none of which divides c. ∎",
 "I also ran this induction as a program, apart from Lean (`proofrun/run_proof.py`): on 1,036 multisets in thirteen groups, each a random sum of cosets of cZ_M with c outside D",
 "Theorem S and the least size for up-sets are also proved in Lean, from statements I had fixed beforehand (section 6).",
 "in the referee's files the paths under `/home/agent3/pq2/` are this folder",
 "that decided seven more",
 "16 patterns are not decided by any programme; their rows give the smallest size found, which in four of them is the referee's programme's and smaller than my solver's (or my solver had none).",
 "of the 2014 pairs of patterns with equal least size on Z_36, 1901 have equal least size on Z_100 too (94.4%, among the 240 patterns decided on both)",
 "(Six of the 24 were being solved during twelve minutes in which another job of mine had all my processes short of memory and slowed, so they had less than their time; none of the six was decided.)",
 "Noon read the statements and three cases by hand before the files went in, and afterwards rebuilt a clean copy of the shared folder on its own account: 18,453 jobs, and 88 lines from the three check files, every one with the standard three axioms (`../../lean-upset-rebuild-26nov-agent2.log`; Noon's post on my board at 17:13 UTC).",
 "`Upset1.lean` (263 lines of lemmas: F1, F2, F3 and sums)",
 "Proposition 5.1 and, under (T2), Theorem 9.4 (far below it, in the search report's words)",
]
for q in Q: print(('in the note   : ' if q in note else 'NOT IN NOTE   : ') + q[:120])
H = "'by theorem' gives the least size where a theorem gives it: (S) Theorem S of the note, for an up-set; (N) the theorem for Z_{pⁿq} of `minsize.pdf`, for a pattern that uses only the divisors of"
print('table headers have the "by theorem" sentence:', H in t36, H in t100)
print('Z_36 table header says R had 60 seconds a pattern:', "solved by HiGHS, whose proofs of optimality are in floating point; 60 seconds a pattern, run by the referee" in t36)
