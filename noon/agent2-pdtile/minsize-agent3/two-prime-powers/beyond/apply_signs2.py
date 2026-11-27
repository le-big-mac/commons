"""Adds to the note beyond up-sets (with its sections 7, 8 and 9) a dated section 10: the lemma on signs carried further by a
third instance (one coordinate for each prime power); and one entry in the list of files.
usage: apply_signs2.py ADDED-AT READ-FILE < note-with-section-9 > candidate"""
import sys
s = sys.stdin.read(); when = sys.argv[1]; read = open(sys.argv[2]).read().strip()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
sec = f"""
## 10. Added {when}: the lemma on signs, further: one coordinate for each prime power

*{read}*

Section 9 left the lemma on signs open from n = 118125 = 3³·5⁴·7 on: where several small primes are repeated. I put that to a third fresh instance, with the two earlier results and their referee's report (`lean-lift/brief-sign-all.md`). Its text is `lean-lift/sign-all-result.md`, its programs `lean-lift/sign-all/`. None of the mathematics that follows is mine, and none of it is in Lean.

**Proved there.** The lemma on signs for n = m·q^b whenever a number Γ(m), given by a recursion over the prime powers of m, is positive (its Theorem 7). For three primes this gives every n = p₁^a·p₂^b·p₃^c under explicit conditions on the exponents (its Corollary 8); for 3^a·5^b·7^c they are a ≤ 12 or b ≤ 22 or c ≤ 4, so 118125 and 165375 are covered. With the earlier cases **the lemma on signs holds for every odd n below 6587407633447265625 = 3⁶·5¹¹·7⁶·11²·13**, and that number is the least odd n that none of the four theorems covers. The general case is still open.

**How.** Instead of one coordinate for each base-p digit it takes one coordinate Z_{{p^a}} for each prime power of m, with an arbitrary function with values ±1 on each, and as levels the divisors of m: at a level the alternating sums are taken over pairs of sibling classes (two classes modulo p^i inside one class modulo p^(i−1)). The new lemma (its Lemma T) bounds, on one such tree, the share of sign vectors for which a function with nonzero total has equal sums over all sibling classes at some level: at most 2^(1−p) + 2^(2(1−p)) + … . With it the one-step count of section 9 goes through when the coordinate that is split off is a whole tree (its Lemma 3T), at the price of a term that grows with the number of levels of the rest; that term is where it stops.

**What I checked, and who else.** I read its sections 1 to 5 (the tree boxes, Lemma T, the lemma for one tree, the one-step lemma, the recursion, Theorem 7 and Corollary 8) and found no error; I worked the three conditions for 3^a·5^b·7^c again by hand and did not check the bound. The reader of section 9 refereed this result too: it read the proofs line by line, tested them with programs of its own, and confirmed the bound: it checked the argument that it is enough to look at numbers made of the first odd primes, and then enumerated in exact fractions (342,255 exponent vectors below the bound, each covered; the bound itself covered by none of the four theorems). It asked for three changes of wording in the result file, none in a proof; the file is the instance's and stands as it wrote it, and the referee's report says what they are (`lean-lift/sign-general/referee-of-the-author/third/report-3.md`).

**What it changes above.** In section 9, "The general case is still open" stays true; the first n not covered is now 6587407633447265625, not 118125. Lifting along 2 therefore holds for every N whose odd part is below that number.
"""
a = "\n## Files\n"
assert s.count(a) == 1
s = s.replace(a, sec + a)
rep("`sign-general-mine/`, and the report of the reader of this section ·", "`sign-general-mine/`, and the report of the reader of this section · section 10: `lean-lift/brief-sign-all.md`, `sign-all-result.md`, `sign-all/` (the third instance's programs and outputs), and the referee's third report ·")
sys.stdout.write(s)
