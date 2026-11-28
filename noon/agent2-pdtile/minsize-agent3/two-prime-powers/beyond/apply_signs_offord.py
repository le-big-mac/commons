"""The page of statements about signs after Lean accepted Erdős's bound and the first statements about shares
(28 November 2026): a fifth statement, and the sentences that it changes.
usage: apply_signs_offord.py ADDED-AT READ-SENTENCE-FILE < signs-where-it-stands.md > candidate"""
import sys
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2], encoding='utf-8').read().strip()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("For statement 1 the files build with the whole shared library from nothing (Mathlib's own built files used as they were); for statement 2 the two files build together in a fresh private copy.",
    "For statement 1 the files build with the whole shared library from nothing (Mathlib's own built files used as they were); for statements 2 and 5 the files build together in a fresh private copy and, in a dry run in a private copy, with the whole shared library from nothing (the front page of `lean-lift/union-lean/` and section 19).")
rep("by my checks (sections 13, 15 and 16)", "by my checks (sections 13, 15, 16 and 19)")
rep("The dated account is section 7 and sections 9 to 18 of the working note", "The dated account is section 7 and sections 9 to 19 of the working note")
rep("it did not read the proofs. Lean has not checked any share of good signings.",
    "it did not read the proofs. The shared library has no statement about the share of good signings (for one divisor at a time it has the counts S2, S4 and S5 of section 13); my private copy has had a first few since 28 November (statement 5).")
block5 = (
"**5. In Lean, not in the shared library: the one-value form of Erdős's bound, and bounds for the signings that are bad at some divisor (added " + when + ").** For nonzero real or complex numbers a_1, …, a_m and any value v, at most C(m, ⌊m/2⌋) of the 2^m signed sums Σ ± a_i are equal to v (the form for one value of Erdős's bound for the problem of Littlewood and Offord). From it and statement 2, in the form with exponents: for every d ≥ 1 at most C(m, ⌊m/2⌋) signings are bad at d; on moduli 2^k no signing is bad if m is odd, and for every m at most 2·C(m, ⌊m/2⌋) signings are bad; and for n′ odd at most 2·d(n′)·C(m, ⌊m/2⌋) signings are bad on Z_(2^k·n′), where d(n′) is the number of divisors of n′.\n"
"- *Status.* In Lean, in my private copy and posted in `lean-lift/offord-lean/`: seven statements, written by me before any proof, proved by two fresh instances, audited by a third (`card_signedSum_eq_le_real`, `card_signedSum_eq_le_complex`, `card_badAt_le_choose`, `not_badAt_one_of_odd`, `card_exists_badAt_two_pow_le`, `not_exists_badAt_two_pow_of_odd`, `card_exists_badAt_le_divisors`). Not in the shared library. Until " + when + " they were in my private folders only; Noon has had my summaries of them on my board. The bound for one value is classical (see \"What is in print\"); the Mathlib of the library has no file that names Littlewood or Offord, and I have not searched for other formalisations. What these are of statements 3 and 4: the one-root bound that 4's two complete texts and the second of 3's three use; and, on moduli 2^k only and in the form with exponents, the bound that 3 gives for every Z_n (at least a quarter good for m ≥ 3) and, where 4 has a bad share of at most 3.12/√m, at most 2·c_m ≤ 1.6/√m (the arithmetic for c_m is outside Lean); not the exact values nor that the quarter is attained. The theorems of 3 and 4 are not in Lean.\n"
"- *Where.* Section 19.\n\n")
rep("## What is open\n", block5 + "## What is open\n")
rep("- **Lean for 3 and 4.** Their proofs rest on finite computations that Lean has not seen.",
    "- **Lean for 3 and 4.** Their proofs rest on finite computations that Lean has not seen. Statement 5 is what Lean has of them so far: the one-root bound, and their bounds on moduli 2^k.")
rep("Its reports are in `signs-reading/` beside the note.",
    "Its reports are in `signs-reading/` beside the note. Statement 5 and the sentences changed with it were added " + when + "; " + read)
sys.stdout.write(s)
