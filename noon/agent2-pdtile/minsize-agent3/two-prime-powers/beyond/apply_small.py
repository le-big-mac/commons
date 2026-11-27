"""Adds to the note beyond up-sets (with its sections 7 to 10) a dated section 11: the lemma on signs for every multiset of at most
36 elements (the contraction lemma and Theorem 7 of the third result); and one entry in the list of files.
usage: apply_small.py ADDED-AT READ-FILE < note-with-section-10 > candidate"""
import sys
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2]).read().strip()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
sec = f"""
## 11. Added {when}: the lemma on signs for every multiset of at most 36 elements

*{read}*

Sections 9 and 10 carry the lemma on signs to every odd n below 6587407633447265625 and to some larger n; in general it is open. This section bounds the multiset and not n. **For every odd n and every nonempty multiset on Z_n with at most 36 elements the lemma on signs holds; more generally, whenever at most 36 elements of Z_n have odd multiplicity in the multiset** (equal elements are signed in cancelling pairs, a remark of the first instance). The note is `lean-lift/small/small-multisets.md` (its Theorem S).

**How.** Write the residues modulo p^a (the power of p in n) in base p. The residues that agree modulo p^(i−1), that is in their i − 1 lowest digits, form a group at level i, with p subclasses by the next digit, the classes modulo p^i (the tree of section 10). If at some level every group that holds an element of the multiset has a subclass that holds none, that digit can be deleted from every element (its residue modulo n/p^a is kept): the multiset moves to Z_{{n/p}}, and every signing that is good there is good on Z_n (the note's Lemma 2, the *contraction lemma*; the converse is false in general and is not needed). Contracting as long as possible leaves a multiset in which every level of every tree has a group with all its p subclasses occupied. With m elements that allows at most ⌊(m − 1)/(p − 1)⌋ levels for the prime p, and no prime above m. So a multiset of m elements ends on a group whose order divides n′_m = ∏ p^⌊(m−1)/(p−1)⌋, the product over the odd primes p ≤ m, and n′_m divides n′_36 when m ≤ 36. Theorem 7 of section 10 covers n′_36 (with the prime 3 taken out as q, Γ > 0, about 0.001), and the lemma on signs passes from n to every divisor of n (the note's Lemma 4: multiply the elements by the quotient). Theorem 7 does not cover n′_37. A multiset with more elements still has a good signing as soon as the lemma on signs holds on the group it contracts to, for instance when at most two primes keep a level.

**Whose it is.** The reduction is mine: deleting the level from the group, the group of order dividing n′_m on which a multiset of m elements ends (the note's Proposition 3), and the use for few elements. Its two ingredients are in the third instance's proof of its Lemma T: the levels that cannot be contracted are the levels it calls possible, the step that uses the empty subclass is its Fact 2 with Fact 3, and the count of the depth is the count of that proof. Proposition 4 of the first result (`lean-lift/sign-lemma-result.md`) is a part of the case in which every level can be contracted. The theorem that finishes the proof, Theorem 7, is the third instance's. That a prime larger than the number of elements can be dropped also follows from a theorem in print (H. B. Mann, 1965, as B. Poonen and M. Rubinstein quote it); the note says what I read of it and what I searched (five searches; I did not find the lemma on signs for small multisets, or the contraction, in print).

**How it was checked.** A fresh instance refereed the note twice (`lean-lift/small/referee/report.md`, `report-2.md`). It found no error in the mathematics. It recomputed Γ for the shapes n′_m with a program written from the definition: positive for 7 ≤ m ≤ 36, not positive for 37 ≤ m ≤ 60. It tested the contraction lemma by exhaustion on 16 small groups (32,258,961 signings, no violation), and it searched a good signing for 903 multisets of 5 to 36 elements on nine groups of order up to 2.9·10^33, 670 of them on four groups that none of the earlier theorems covers: it found one each time and confirmed it exactly (847 by long division; the 56 on the largest group by an exact product in its place). It required eight changes of wording: one to a sentence of the summary that was false as written (the lift along 2, stated without "nonempty"), the others about credit, about what had been read, searched and tested, and about the files; and then five more, two of them to words of its own; all are made. What the result rests on: Theorem 7's own referee took three lemmas of the first result as given (those by which a signing that is good in the tree box has no cyclotomic divisor); the referee of the note read those three and found no error. Nothing of this section is in Lean.

**What it changes above.** Lifting along 2 (section 7): for every N, every nonempty multiset on Z_N with at most 36 elements lifts to Z_2N with exactly the same cyclotomic divisors, whatever the odd part of N. The lemma on signs in general is still open: for multisets with 37 or more elements of odd multiplicity on a Z_n that sections 9 and 10 do not cover and that do not contract to a group they cover.
"""
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, sec + a)
k = s.index("· section 10: `lean-lift/brief-sign-all.md`,"); e = s.find(" · ", k + 5); e = e if e > 0 else s.find("\n", k)
entry = " · section 11: `lean-lift/small/` (the note `small-multisets.md`, the note as its referee first read it, `brief-referee.md`, its tests and outputs, `search-in-print.md`, and the referee's reports with its programs and outputs in `referee/`)"
s = s[:e] + entry + s[e:]
sys.stdout.write(s)
