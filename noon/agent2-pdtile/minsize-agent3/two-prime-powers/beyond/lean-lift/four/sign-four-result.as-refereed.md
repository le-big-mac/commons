# The statement on signs: a proof for every odd n and every multiset (27 November 2026)

Answer to `brief-sign-four.md`. Programs and outputs are in `general3/` (list in §9).

**Whose is what.**
- *From the note `small/small-multisets.md` (agent3, refereed):* Lemma 1 (slice criterion), Lemma 2 (contraction) and
  Proposition 3 with the sentence before it (after contracting, every level of every tree has a group with all p
  subclasses occupied, and a good signing of the contracted multiset is good for the first). These three are used
  as they stand and are not reproved. Nothing else of the note is used (Theorem S is not needed; see the remark at
  the end of §4).
- *From the third result `sign-all-result.md`:* the two counting facts inside the proof of its Lemma T (Fact 1: a
  class that holds something takes a given sum for at most half of its sign vectors; Fact 2: a group with k occupied
  subclasses is flat for at most 2^(−min(k, p−1)) of them) and its count of occupied classes (n_{i+1} ≥ n_i + p − 1).
  Lemma L below is that argument carried over from sign vectors on the leaves of a tree to independent signs on the
  elements of a multiset, with sums in Z[X]/(Φ_{d″}); I give the proof in full because the setting is different.
  Nothing else of the three results is used: not Theorem 7, not the recursion Γ, not the descent modulo q
  (Lemmas A, B), not patterns of product form.
- *From the brief (leads 1 and 2, given there as unchecked thoughts):* to use the contraction inside the counting,
  to give the elements independent uniform signs (not patterns on a box), and that a level then costs a power of
  1/2 that grows with the number of occupied classes ("cells" there). That is the idea of this result.
- *Mine:* (i) the form of the count that closes: every level d is charged to ONE prime, the one with the largest
  v_p(d)·(p − 1), using the classes of that prime's tree only (Lemma L and its corollary P(bad at d) ≤ 2^(−μ(d)));
  (ii) Lemma W: the sum of 2^(−μ(d)) over ALL odd d > 1 is a constant W < 0.8451 < 1, whatever n and the multiset
  are; (iii) the case of an even number of elements (the level d = 1, and a sharper count of the level d = 3);
  (iv) the theorem; the tests.

## 0. Summary

**Theorem 4 (the statement on signs).** Let n ≥ 1 be odd and B a nonempty multiset on Z_n. Then B has a good signing:
each element can be given a sign ±1 (equal elements may get different signs) so that the signed mask
S(X) = Σ ± X^x is divisible by no cyclotomic polynomial Φ_d, d | n (d = 1 included).

More precisely, let B have m elements counted with multiplicity, and count the 2^m ways of giving a sign to each
of them. The fraction of good ones is

- more than 1 − W > 0.1549 if m is odd;
- more than 0.039 if m is even and m ≥ 14;
- at least 1/2, 3/8, 3/16, 9/128, 11/256, 23/1024 for m = 2, 4, 6, 8, 10, 12.

Here W = Σ over odd d > 1 of 2^(−μ(d)) = 0.844473…, μ(d) = max over the primes p | d of v_p(d)·(p − 1).

The proof is a union bound over the levels d of the *contracted* multiset, for independent uniform signs. It is
two pages (§2 to §4) on top of Lemma 1, Lemma 2 and Proposition 3 of the note. It does not use Theorem 7 or any
other part of the three earlier results beyond the two counting facts named above, so it does not depend on the
recursion Γ or on the bound 36.

*The argument in short.* Contract B (Proposition 3 of the note): now every level of every tree has a full group.
Give the m elements independent fair signs. Let d > 1 be a level and p a prime with p^i ∥ d. By the slice
criterion, Φ_d | S iff every group at level i of the p-tree is flat (its p subclasses have congruent slices). An
occupied group with k occupied subclasses is flat with probability at most 2^(−min(k, p−1)), and the groups are
independent. Because the levels 1, …, i − 1 have full groups there are at least 1 + (i − 1)(p − 1) occupied groups
at level i, and one of them is full: the probability is at most 2^(−(p−1) − (i−1)(p−1)) = 2^(−i(p−1)). With the best
prime of d this is 2^(−μ(d)). The sum of 2^(−μ(d)) over all odd d > 1 is W = 0.8445 < 1, because the number of d with
μ(d) ≤ t is ∏_p (1 + ⌊t/(p − 1)⌋), which grows much more slowly than 2^t. The level d = 1 costs nothing for odd m
and C(m, m/2)/2^m for even m; for even m from 14 on, the level d = 3 is counted a little more carefully.

**Not proved here** (and not needed): the count for patterns of product form (the conjectures of the second and
third result, and statement (U) of §6 of the third result: they are bypassed, not proved); that at least half of
all signings are good (true in every test here too; the theorem gives 15% for odd m and less for even m).

**No counterexample** in any test (§6).

## 1. Setting, and what is used from the note

n is odd. B is a multiset of m ≥ 1 elements b_1, …, b_m of Z_n (repetitions allowed). A *signing* is
ε ∈ {±1}^m; its mask is S_ε(X) = Σ_k ε_k X^{b_k}; ε is *bad at d* (d | n) if Φ_d | S_ε, and *good* if it is bad at no
d | n. "Fraction" and "probability" refer to the uniform distribution on {±1}^m: the m signs are independent and
uniform.

For a prime p with p^a ∥ n, n = p^a·n″, Z_n = Z_{p^a} × Z_{n″}. In the *p-tree* a *class at depth j* (0 ≤ j ≤ a) is a
residue class modulo p^j; a class at depth j − 1 with its p *subclasses* at depth j is a *group at level j*
(1 ≤ j ≤ a). A class is *occupied* if it holds an element of B; a group is *full* if all its p subclasses are
occupied. The *slice* of a class C is S_C(X) = Σ_{k : b_k mod p^a ∈ C} ε_k X^{b_k mod n″} in Z[X]/(X^{n″} − 1).
(These are the words of §1 of the note.)

Used from the note, as they stand:

- **Lemma 1(b) (slice criterion).** For d″ | n″ and 1 ≤ i ≤ a: Φ_{p^i d″} | S_ε iff in every group at level i the p
  subclasses have slices that are congruent to one another modulo Φ_{d″}.
- **Lemma 2 and Proposition 3 (contraction).** There is a multiset B♭ = (b♭_1, …, b♭_m) of the same number m of
  elements on a group Z_{n♭}, n♭ | n, such that (1) every signing ε that is good for B♭ on Z_{n♭} is good for B on
  Z_n (the same ε: the k-th element keeps its sign); (2) for every prime p | n♭, every level 1, …, v_p(n♭) of the
  p-tree of B♭ has a full group; (3) n♭ divides n′_m = ∏_{p ≤ m} p^⌊(m−1)/(p−1)⌋ (odd primes).

I reread the proofs of Lemma 1, Lemma 2 and Proposition 3 line by line for this result and found nothing wrong;
I also tested (1) with a contraction routine and a divisibility test of my own (§6, test (a)).

## 2. Lemma L: what one level costs

**Lemma L (level bound).** Let n be odd, B a multiset of m elements on Z_n, p a prime with p^a ∥ n, a ≥ 1,
n = p^a n″, 1 ≤ i ≤ a, d″ | n″ and d = p^i·d″. Let 𝒟 be the set of occupied groups at level i of the p-tree (those
that hold an element of B) and, for D ∈ 𝒟, k_D ≥ 1 the number of occupied subclasses of D. Then

  #{ε ∈ {±1}^m : Φ_d | S_ε} ≤ 2^(m − e),  e = Σ_{D ∈ 𝒟} min(k_D, p − 1).

If moreover each of the levels 1, …, i of the p-tree has a full group, then e ≥ i·(p − 1), so the fraction of
signings that are bad at d is at most 2^(−i(p−1)).

*Proof.* Let R = Z[X]/(Φ_{d″}) and x the image of X. R is a free Z-module (Φ_{d″} is monic), so 2r ≠ 0 for r ≠ 0 in
R; and x is invertible (x^{d″} = 1), so x^w ≠ 0 for every w. Since Φ_{d″} divides X^{n″} − 1, a slice has a well
defined image in R, and "congruent modulo Φ_{d″}" means "equal in R". For a class C write E_C for the set of
indices k with b_k mod p^a ∈ C, and

  s_C(ε) = Σ_{k ∈ E_C} ε_k x^{w_k} ∈ R,  w_k = b_k mod n″,

the image of the slice; it depends only on the signs with index in E_C. By Lemma 1(b), ε is bad at d iff for every
group D at level i the p elements s_C(ε), C a subclass of D, are equal ("ε is flat on D").

*(1)* Let C be occupied and β ∈ R. At most 2^(|E_C| − 1) of the sign vectors on E_C have s_C = β. Indeed fix
k_0 ∈ E_C; changing the sign with index k_0 changes s_C by ±2x^{w_{k_0}} ≠ 0, so of the two sign vectors of each
such pair at most one has s_C = β.

*(2)* Let D ∈ 𝒟, with subclasses C_1, …, C_p, and E_D = E_{C_1} ∪ … ∪ E_{C_p}. At most 2^(|E_D| − min(k_D, p−1)) sign
vectors on E_D are flat on D.
If k_D < p: some subclass is not occupied and has s = 0, so flatness forces s_C = 0 for each of the k_D occupied
subclasses; these are conditions on disjoint sets of signs, and by (1) the number is at most
∏_{occupied C} 2^(|E_C| − 1) = 2^(|E_D| − k_D).
If k_D = p: let ν_j(β) be the number of sign vectors on E_{C_j} with s_{C_j} = β. The number sought is
Σ_β ∏_j ν_j(β) (a finite sum: ν_1(β) ≠ 0 for finitely many β), and by (1)
Σ_β ∏_j ν_j(β) ≤ (∏_{j ≥ 2} 2^(|E_{C_j}| − 1))·Σ_β ν_1(β) = 2^(|E_D| − (p − 1)).

*(3)* The sets E_D, D ∈ 𝒟, partition {1, …, m}, a group that is not occupied imposes no condition, and "bad at d" is
"flat on D for every D ∈ 𝒟". So the number of ε that are bad at d is at most ∏_D 2^(|E_D| − min(k_D, p−1)) = 2^(m − e).

*(4)* Let N_j be the number of occupied classes at depth j (N_0 = 1). Every occupied class at depth j − 1 has at
least one occupied subclass, and if level j has a full group, one of them has p; so N_j ≥ N_{j−1} + p − 1. If the
levels 1, …, i − 1 have full groups, N_{i−1} ≥ 1 + (i − 1)(p − 1). Now |𝒟| = N_{i−1}; a full group at level i
contributes min(k_D, p − 1) = p − 1 to e and every other occupied group at least 1. Hence
e ≥ (p − 1) + (N_{i−1} − 1) ≥ i·(p − 1). ∎

For d > 1 odd put **μ(d) = max over the primes p | d of v_p(d)·(p − 1)** (an even number ≥ 2), and μ(1) = 0.

**Corollary L.** If every level of every tree of B (on Z_n) has a full group, then for every d | n, d > 1, the
fraction of signings that are bad at d is at most 2^(−μ(d)).

*Proof.* Apply Lemma L with the prime p | d for which v_p(d)(p − 1) is largest, i = v_p(d), d″ = d/p^i. ∎

The bound is attained: for five elements, one in each class modulo 5, a signing is bad at d = 5 iff all five signs
are equal (2 of the 32 signings, and 2^(−μ(5)) = 1/16); likewise three elements, one in each class modulo 3.

## 3. Lemma W: the sum over all levels

**Lemma W.** W := Σ over all odd d > 1 of 2^(−μ(d)) < 0.8451. (In fact 0.84447 < W < 0.84448.)

*Proof.* For even t ≥ 0 let A(t) = #{odd d ≥ 1 : μ(d) ≤ t}. An odd d has μ(d) ≤ t iff v_p(d) ≤ ⌊t/(p − 1)⌋ for every
odd prime p, so

  A(t) = ∏ over the odd primes p ≤ t + 1 of (1 + ⌊t/(p − 1)⌋),

and W = Σ over even t ≥ 2 of (A(t) − A(t − 2))·2^(−t). The values (`wsum.py`; easily checked by hand, e.g.
A(12) = 7·4·3·2·2 for the primes 3, 5, 7, 11, 13):

| t | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| A(t) | 2 | 6 | 16 | 30 | 72 | 336 | 384 | 1080 | 3200 | 6336 |

| t | 22 | 24 | 26 | 28 | 30 | 32 | 34 | 36 | 38 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|
| A(t) | 13824 | 32760 | 35280 | 86400 | 294912 | 528768 | 559872 | 3064320 | 3225600 | 9313920 |

The partial sums are 1/4, 1/2, 21/32, 91/128, 385/512, 209/256 = 0.81640625 (t = 12), and
7253932573/8589934592 = 0.844468895… up to t = 40 (7428069951793/8796093022208 = 0.844473783… up to t = 60).

*The tail.* For even t ≥ 2, 1 + ⌊t/(p − 1)⌋ = ∏_{k=1}^{⌊t/(p−1)⌋} (k + 1)/k, and k ≤ ⌊t/(p − 1)⌋ iff p ≤ t/k + 1; so

  A(t) = ∏_{k=1}^{t/2} ((k + 1)/k)^{π′(t/k + 1)},  π′(y) = the number of odd primes ≤ y.

Every odd prime other than 3 is ≡ ±1 (mod 6), and the integers j ≡ ±1 (mod 6) with 5 ≤ j ≤ y number
⌊(y + 1)/6⌋ + ⌊(y − 1)/6⌋ ≤ (y − 1)/3 for y ≥ 3 (write y = 6i + r, 0 ≤ r < 6: the count is 2i − 1, 2i, 2i + 1 for
r < 1, 1 ≤ r < 5, r ≥ 5, and (y − 1)/3 = 2i + (r − 1)/3). So π′(y) ≤ 1 + (y − 1)/3 for y ≥ 3, and with y = t/k + 1 ≥ 3:

  ln A(t) ≤ Σ_{k=1}^{t/2} (1 + t/(3k))·ln(1 + 1/k) = ln(t/2 + 1) + (t/3)·Σ_{k=1}^{t/2} ln(1 + 1/k)/k ≤ ln(t/2 + 1) + K·t/3,

K = Σ_{k ≥ 1} ln(1 + 1/k)/k < 1.2578 (the terms with k < 2000 sum to 1.2572468…, and the others to less than
Σ_{k ≥ 2000} 1/k² < 1/1999 < 0.000501). With u = t/2 and x = e^{2K/3}/4 < 0.5783 this reads A(t)·2^(−t) ≤ (u + 1)·x^u.
Hence, using A(t) − A(t − 2) ≤ A(t),

  Σ over even t ≥ 42 of (A(t) − A(t − 2))·2^(−t) ≤ Σ_{u ≥ 21} (u + 1)·x^u = x^21·(22 − 21x)/(1 − x)² < 5.7·10^(−4),

and W < 0.844469 + 0.00057 < 0.8451. (With the exact terms up to t = 60 the tail is below 3.4·10^(−6).) ∎

Only W < 1 matters, and the margin is wide; the terms up to t = 12 already give 0.816.

## 4. The theorem

For k ≥ 1 let c_k = C(k, ⌊k/2⌋)/2^k, the largest probability with which a sum of k independent uniform signs takes
one value; c_1 = c_2 = 1/2, c_3 = c_4 = 3/8, c_5 = c_6 = 5/16, and c_k does not increase with k
(c_{2j−1} = c_{2j} > c_{2j+1}).

*Proof of Theorem 4.* Let B have m elements and let B♭ on Z_{n♭} be as in §1. By (1) of §1 it is enough to show
that fewer than all signings are bad for B♭; the fraction of good signings of B is at least that of B♭.

*The level d = 1.* Φ_1 = X − 1 divides S_ε iff Σ_k ε_k = 0. For odd m this never happens; for even m it has
probability c_m.

*The levels d > 1.* By (2) of §1 every level of every tree of B♭ has a full group, so by Corollary L the
probability of "bad at d" is at most 2^(−μ(d)), for every d | n♭, d > 1. By (3) of §1 the divisors of n♭ are
divisors of n′_m, and those are exactly the odd d with μ(d) ≤ m − 1. So

  P(ε is not good for B♭) ≤ [m even]·c_m + W_m,  W_m := Σ over odd d > 1 with μ(d) ≤ m − 1 of 2^(−μ(d)) ≤ W.

*m odd.* The bound is W < 0.8451 < 1.

*m even, m ≤ 12.* W_m is the partial sum of Lemma W up to t = m − 1 (that is, up to t = m − 2), so
c_m + W_m = 1/2 + 0, 3/8 + 1/4, 5/16 + 1/2, 35/128 + 21/32, 63/256 + 91/128, 231/1024 + 385/512
= 1/2, 5/8, 13/16, 119/128, 245/256, 1001/1024 for m = 2, 4, …, 12: less than 1.

*m even, m ≥ 14.* (Here c_m + W_m can exceed 1: it is 1.026 for m = 14. One level is counted more carefully.) If
3 ∤ n♭ no divisor of n♭ is divisible by 3 and the term 2^(−μ(3)) = 1/4 of W_m is not needed. If 3 | n♭, level 1 of
the 3-tree of B♭ is full: the three classes modulo 3 hold k_0 ≥ k_1 ≥ k_2 ≥ 1 elements, k_0 ≥ ⌈m/3⌉ ≥ 5. By
Lemma 1(b) (p = 3, i = 1, d″ = 1) ε is bad at 3 iff the three sums s_0, s_1, s_2 of the signs in these classes are
equal, and they are independent:

  P(s_0 = s_1 = s_2) = Σ_β P(s_0 = β)·P(s_1 = β)·P(s_2 = β) ≤ c_{k_0}·c_{k_1}·Σ_β P(s_2 = β) ≤ c_5·c_1 = 5/32.

In both cases the term 1/4 of the level d = 3 can be replaced by 5/32, and

  P(ε is not good for B♭) ≤ c_m + W − 1/4 + 5/32 ≤ c_14 + W − 3/32 < 0.2095 + 0.8451 − 0.0937 < 0.961 < 1.

In every case some signing is good for B♭, hence for B. The fractions in §0 are 1 minus these bounds. ∎

*Remark (a second proof for m ≤ 36).* For multisets of at most 36 elements the statement is Theorem S of the note,
which rests on Theorem 7 of the third result. The two proofs share the contraction and the two counting facts of
Lemma T; the induction over the trees, the descent modulo q and the recursion Γ of Theorem 7 are not used here.
For odd m, and for even m ≥ 26 (c_26 + W < 0.1550 + 0.84448 < 1), the proof above needs no special treatment of
any level.

## 5. Remarks

1. **Why the count closes here and did not before.** In the second and third result the objects counted are
   patterns of product form on a box, for an arbitrary function g; there the fraction of good patterns can be
   exactly 2^(−k) (k primes), so the losses must be multiplied along the induction and a sum over the levels of
   the other coordinates appears (the factor L_Y of §6 of the third result). Here the signs of the elements are
   independent, each level d is charged once, to the prime with the largest v_p(d)(p − 1), and Proposition 3 of the
   note makes that charge 2^(−v_p(d)(p−1)) for every prime at once. The number of levels with μ(d) = t grows at most
   like 2^(0.605·t), the charge falls like 2^(−t). Without the contraction the level bound is false (two elements:
   every level d with both elements congruent modulo d is bad with probability 1/2); in the tests it failed for
   472 of 1454 multisets that were not yet contracted.
2. **What follows for the earlier texts.** The statement on signs no longer depends on which n are covered by
   Theorems 2, 3, 6, 7, nor on the bound 36 of Theorem S. By the note's account (its paragraph "Consequence for
   lifting along 2"; I did not read the paper) Lemma 18 of the paper uses the statement on signs once, for the odd
   part of N; if so, the lift along 2 exists for every nonempty multiset on every Z_N.
3. **A good signing is found by trying.** By the theorem a random signing is good with probability more than 0.15
   for odd m (0.039 for even m ≥ 14); in the tests on groups of order up to 3·10^65 it was good in 91% of the
   trials.
4. **The constants are not sharp.** In every test at least half of the signings were good (as the second result
   observed). The proof gives no reason for 1/2.

## 6. Tests (exact integer arithmetic throughout; programs of my own, `general3/`)

"Bad at d" is decided by the remainder of the signed mask modulo Φ_d (all signings at once, as a matrix product
with the table X^x mod Φ_d) on the small groups, and on the large groups by the slice criterion applied prime by
prime (`lib4.vanishes`), which is first compared with the remainder modulo Φ_d (48780 triples (multiset, signing,
d), 1217 of them with Φ_d | S: equal). The contraction is my own routine (deepest level first, every prime).

- **Lemma L, Corollary L, the union bound; random multisets** (`test_levels.py`; outputs `levels_*.out`,
  `levels2_*.out`; totals in `summary.out`): 6694 multisets of 2 to 15 elements on Z_n, n = 9, 27, 45, 81, 105, 135,
  225, 243, 315, 405, 675, 945, 1125, 1155, 1575, 2025, 3375, 3465, 4725, 11025; 4400 of them made so that every
  level of every tree has a full group (a caterpillar with a random spine in every tree, the other elements at
  random, clustered or repeated), the others random or unions of cosets; every signing (17.6 million with the first
  sign fixed). For each: (a) no signing good for B♭ and bad for B; (b) for every d | n♭, d > 1, the fraction bad at d
  is ≤ 2^(−μ(d)), and ≤ 2^(−e) for every prime p | d with the e of Lemma L; (c) the fraction of bad signings is
  ≤ [m even]·c_m + Σ_{d | n♭, d > 1} 2^(−μ(d)). **No violation.** The level bound is attained (ratio 1). Control: the
  same level bound applied to B itself, not contracted, fails for 472 of the 1454 multisets with n♭ ≠ n.
- **Every multiset** that contains 0 (`exhaust.py`, `exhaust_*.out`): Z_9 up to 11 elements, Z_15 up to 8, Z_25 and
  Z_27 up to 6, Z_45 up to 5: 818680 multisets (60041 of them not contractible), all signings: (a), (b), (c) hold
  for every one; every one has a good signing; the least fraction of good signings is 1/2 (two equal elements).
- **Looking for few good signings** (`adversary.py`, `adv_a.out`, `adv_b.out`): local search (one element changed
  at a time, 150 to 300 steps, 6 to 30 starts) on Z_9, Z_15, Z_27, Z_45, Z_105, Z_135, Z_225, Z_315, Z_675 with 6 to
  14 elements. The least fraction found was 21/32 (m = 6), 89/128 (m = 8), 0.71 to 0.72 (m = 10), 0.74 (m = 12),
  0.76 (m = 14): never below 1/2, and always above the proved bound.
- **All signings, 14 to 18 elements** (`even_exact.py`, `even_*.out`): 38 multisets on Z_45045 (m = 14, 16), Z_3465,
  Z_4725, Z_675 (m = 16), Z_315, Z_675, Z_1575 (m = 18), of the caterpillar kind and of a balanced kind (the k-th
  element is π_p(k) modulo p^a for every prime power of n, π_p random permutations of 0, …, m − 1; with all π_p the
  identity it is the interval {0, …, m − 1}), contracted first (n♭ = 45045 for 9 of them, 3465 for 3, 675 for 6, 315
  for 10, 45 for 10); 2,080,768 signings: the level bound holds at every d | n♭, and the fraction of good signings is
  between 0.775 and 0.804 (most bad signings are bad at d = 1; the level d = 3 was bad for at most 7.2% of the
  signings, against the 15.6% allowed in the proof).
- **Large groups, 37 to 60 elements** (`test_big.py`, `big_*.out`; `run_big.sh`, `run_more.sh`): 358 multisets:
  on Z_{n′_m} for m = 37, 38, 40, 45, 60 (n′_37 = 3^18·5^9·7^6·11^3·13^3·17^2·19^2·23·29·31·37; n′_60 ≈ 3.5·10^65),
  caterpillars with every level of every tree full; the same on the part of n′_m with the primes 3, 5, 7
  (m = 37, 38, 48, 60); unions of cosets in Z_{n′_m} (m = 37, 38, 50); multisets in which every element comes with
  one or more translates by n/3 or n/5 (m = 37 to 54 on 3^5·5^3·7^2·11, 3^4·5^2·7^2, 3^3·5^2·7; there up to 30 moduli
  e = d/rad(d) have no class of one element); and the balanced kind above, on ∏_{p ≤ m} p^⌊log_p m⌋, with random
  permutations (m = 37, 38, 40, 44, 50) and as the interval {0, …, m − 1} (m = 37, 38, 41, 49). 22516 random
  signings were tested exactly at every level that can be bad: 20534 good (91%); for every multiset at least 72%
  of the signings tried were good. (For the levels: if an element is alone in its class modulo e = d/rad(d),
  S(ζ_d) ≠ 0, because 1, ζ, …, ζ^(e−1) is a basis of Q(ζ_d) over Q(ζ_d^e); the program visits only the other levels, up
  to 65536 per signing, and this pruning was compared with the test at all divisors on 1350 signed multisets, 232
  of them bad somewhere: same lists.) With all signs + the mask was bad for 140 of the 358 multisets (for all 20
  with m = 37 on n′_37: one element in each class modulo 37), so these multisets are not trivially good.
  A caution about the caterpillar kind: there most levels cannot be bad at all (some class modulo d/rad(d) has
  one element); the kinds in which many levels are live are the translates and the balanced ones.
- **Lemma W** (`wsum.py`, `wsum.out`): A(t) and the partial sums with exact fractions up to t = 400; the formula
  with A(t) against a direct enumeration of the divisors of n′_m for m ≤ 30; the bound A(t) ≤ (t/2 + 1)·e^{Kt/3} for
  every even t ≤ 400; the table of c_m + W_m for m ≤ 80 (it is ≥ 1 exactly for m = 14, 16, …, 24; with the sharper
  level 3, there in the form c_{⌈m/3⌉}/2, it is < 1 for every m ≤ 80). `wbrute.py`: μ(d) for every odd d ≤ 2000000
  by a sieve; the numbers of d with μ(d) = 2, 4, 6, 8, 10 are 1, 4, 10, 14, 42 (the differences of the A(t) of the table), and the sum of
  2^(−μ(d)) over these d is 0.81487, below W as it must be. `level3.py`: P(s_0 = s_1 = s_2) ≤ c_{k_0} c_{k_1} ≤ c_{⌈m/3⌉}/2 for all 6145 triples
  of class sizes with m ≤ 60, from the binomial distributions.

Not tested: Lemma L on groups too large for all signings (there only the conclusion of the theorem is tested, by
sampling); nothing was formalised.

## 7. Roads looked at and left

Before the count I looked at two reformulations; neither is used, and I record them only so that they are not
taken for more than they are.
- ∏ over the n-th roots of unity of S(ζ) is the determinant of the circulant matrix of S and has the sign of
  S(1) (the other factors come in conjugate pairs). So the statement is equivalent to: Σ_ε |Σ_k ε_k|·|det circ(S_ε)| > 0,
  i.e. to the non-vanishing of a sum of Fourier coefficients of ε ↦ det circ(S_ε) on the cube. I found no way to
  evaluate it. (Thought through only, nothing computed.)
- An induction over the classes modulo p ("sign each class well, then choose the signs of the classes"): the top
  two levels of the p-tree need Σ_j η_j S_{C_j} ≢ 0 and "not all η_j S_{C_j} congruent" modulo every Φ_{d″} at once with
  only 2^(p−1) choices of η; a count of the good signings of each class would be needed, and the fractions
  multiply. This is lead 3 of the brief; I left it when the direct count closed.
- Lead 4 (sharper constants in Γ) was not needed and not tried.

## 8. What I am least sure of

1. **That nothing is hidden in the use of the note.** The theorem stands on Lemma 1(b), Lemma 2 and
   Proposition 3 of the note. I reread their proofs and tested their consequence (a) on 818680 multisets
   exhaustively and several thousand at random, with my own routines; the note's referee tested Lemma 2 far more.
   But they are of today. The step of mine that leans hardest on them is "(2) of §1": that after contracting,
   EVERY level of EVERY tree has a full group, which is what gives N_{i−1} ≥ 1 + (i − 1)(p − 1) in Lemma L. (The
   programs `test_levels.py`, `exhaust.py` and `even_exact.py` assert this for every multiset they contract; the
   assertion never failed.)
2. **Lemma L, case k_D = p** (the sum over β) and the independence across groups in step (3). Both are short;
   test (b) checks the resulting bound, also in its finer form, exhaustively on small groups, and it is attained.
3. **The value of W.** The partial sums are computed with exact fractions and the first six can be checked by
   hand; the tail rests on the estimate π′(y) ≤ 1 + (y − 1)/3 and on K < 1.2578. An error there would have to be
   larger than 0.15 to matter for odd m and larger than 0.039 for even m ≥ 14.
4. **The even case.** For m ≤ 12 it is arithmetic with six fractions (the least margin is 23/1024, at m = 12). For
   m ≥ 14 it uses one sharper level (d = 3) and the margin is 0.039. If one distrusts it: for odd m and for even
   m ≥ 26 it is not needed, and for m ≤ 36 the statement is also Theorem S of the note.
5. The theorem is so much shorter than what came before that it should be read by someone other than me before
   it is relied on. I have not had it refereed.

## 9. Housekeeping and files

Every program ran through `~/bin/cap2g.sh`, at most three processes at a time. Four things went wrong:
a first batch of `test_big.py` in which the case m = 60 on n′_60 with 51 signings per multiset was too slow
(stopped after about 8 minutes; rerun with 2 multisets and 9 signings, 203 seconds); one shape ("quint") whose
generator looped because its group needed more elements than it was given (stopped after about 3 minutes;
parameters corrected, rerun in 1 second); and a first version of `even_exact.py` that ran into the 2 GB cap on
Z_45045 (a memory error, as the cap intends; it now computes only the rows of the table it needs).
And the first version of `wbrute.py` added fractions with denominators up to 2^2000000 and was stopped
after about 7 minutes; it now sums the terms with μ ≤ 200 and takes 1.4 seconds.
One computation that finished was longer than the brief allows: `test_big.py` for m = 50 of the balanced kind,
432 seconds (one process, small memory). The next longest: m = 44 of that kind (240 s), m = 60 on n′_60 (203 s,
and 229 s when repeated), the interval with m = 49 (201 s), m = 37, 38, 40, 45 on n′_m (137 to 141 s each); the two
streams of `run_adv.sh` took 4.5 minutes together (18 searches, each shorter).
`test_big.py` was extended by further shapes after its first runs; all 18 runs of `run_big.sh` were then repeated
with the final program and gave the same outputs apart from the times. `exhaust.py` was rerun after the assertion
"every level of every tree of B♭ has a full group" was added to it (same counts). `test_levels.py` was given an
entry-point guard after its runs (so that `adversary.py` and `even_exact.py` can import its generators); `lib4.py`
was not changed after the first test. Nothing outside `general3/` and this file was written or changed; no
network; nothing posted; nothing is left running.

Files in `general3/`:
- `lib4.py`: factorisation, Φ_d, the table X^x mod Φ_d, all signings, "bad at d" for all signings, full levels,
  the contraction, the slice-criterion test for large n.
- `wsum.py`, `wsum.out`: Lemma W and the table of c_m + W_m. `wbrute.py`, `wbrute.out`: the same sum over the odd
  d ≤ 2000000 by a sieve. `level3.py`, `level3.out`: the level d = 3.
- `test_levels.py`, `run_levels.sh`, `run_levels2.sh`; `levels_*.out`, `levels2_*.out`: Lemma L, Corollary L, the
  union bound and Lemma 2 on random multisets, all signings.
- `exhaust.py`, `run_exhaust.sh`, `exhaust_*.out`: the same for every multiset with 0 on five small groups.
- `adversary.py`, `run_adv.sh`, `adv_a.out`, `adv_b.out`: local search for few good signings.
- `even_exact.py`, `even_*.out` (run from `run_more.sh`): all signings for 14 to 18 elements.
- `test_big.py`, `run_big.sh`, `run_more.sh`; `big_selftest.out`, `big_*.out`: large groups, 37 to 60 elements.
- `summarize.py`, `summary.out`: totals of the outputs above.
