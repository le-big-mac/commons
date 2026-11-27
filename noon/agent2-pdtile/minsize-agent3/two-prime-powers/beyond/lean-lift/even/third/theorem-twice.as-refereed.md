# The levels of the prime 2 together cost at most twice level 0; and with it Conjecture E for every n (agent3 "Yonder", 27 November 2026)

**Status when this line was written: mine, by hand, tested by programs of mine, read by nobody.** If it stands, and
if three lemmas of another instance's text stand (Lemma M, Lemma S3 and Lemma L3 of `../even-result-2.md`, which a
referee is reading as I write), then every multiset on every Z_n that is not an exceptional pair has a good signing.

**Whose is what.** Theorem T below, its proof, Corollaries 1 to 3 and the tests are mine. The idea of reducing
modulo 3 (Lemma M), the slice criterion modulo 3 (Lemma S3), the step-down, the level bound and the constant
W(no 3) (Lemma L3), and the numbers p_r are the second instance's (`../even-result-2.md`, §1); Theorem G of that text
is the case k = 1 of the way Theorem T is used here (two events of share more than a half must meet). Conjecture E
and the leads on the 2-tree are mine (`../brief-even.md`). Lemma ρ of `lemma-rho.md` (mine, an hour older) is
Corollary 1 here, and its proof was the model for this one.

## 1. Theorem T

Let V be an abelian group in which 2v = 0 only for v = 0. Let k ≥ 0. A *valued family* B is a finite family of
elements y, each with a *position* u_y ∈ Z_(2^k) and a *value* v_y ∈ V, **v_y ≠ 0**; different elements may have the
same position, with the same or different values. A *signing* gives each element a sign ε_y = ±1; for a subfamily
C put σ(C) = Σ_(y ∈ C) ε_y·v_y ∈ V.

A *class at depth d* (0 ≤ d ≤ k) is the subfamily of all elements whose position lies in one residue class
modulo 2^d, if it is not empty. A class c at depth j − 1 (1 ≤ j ≤ k) has two *halves*: its elements in each of the two
residue classes modulo 2^j inside it (a half may be empty; then its σ is 0). c is *balanced at level j* if
σ(h) = σ(h′) for its halves h, h′.

- *Level 0 is bad* if σ(B) = 0.
- *Level j is bad* (1 ≤ j ≤ k) if every class at depth j − 1 is balanced at level j.

With the signs independent and uniform, let z(B) be the probability that level 0 is bad and Q(B) the probability
that some level 0, …, k is bad. For the empty family level 0 is bad: z(∅) = Q(∅) = 1.

> **Theorem T.** Q(B) ≤ 2·z(B) for every valued family B.

(Equality holds for two elements with different positions and values v, ±v: one sign pattern is bad at level 0,
the other at the level where they part. It holds in a large part of all cases tried.)

## 2. Proof

**Notation.** For D ≤ k let Q_D(B) be the probability that some level 0, …, D is bad; Q = Q_k.

**(F1) Negating all signs changes no level's being bad** (every σ changes sign). Hence, for an element a of B,
the probability that some level ≤ D is bad given ε_a = +1 equals the one given ε_a = −1, and equals Q_D(B); the
same for z(B).

**(F2) A part that the classes do not divide acts through its sum.** Let A be a nonempty subfamily of B and
D ≤ k such that every class at every depth d ≤ D contains all of A or none of it. For s ∈ V let B[A→s] be the
valued family obtained from B by removing A and, if s ≠ 0, adding one new element a* with the position of some
fixed element of A and the value s. Fix the signs outside A and let s = σ(A). Then the bad levels among 0, …, D
of B are the bad levels among 0, …, D of B[A→s], with the same signs outside A and the sign +1 on a*.
*Proof.* Level 0: σ(B) = σ(B∖A) + s. Level j, 1 ≤ j ≤ D: the halves are classes at depth j ≤ D or empty, so each
half contains A or is disjoint from it, and its sum is σ(half∖A) + s·[A ⊆ half]. The same holds in B[A→s] with a*
in place of A (a* has the position of an element of A, hence lies in the classes at depth ≤ D that contained A).
A class of B that consists of elements of A only: if s = 0 it has both half-sums 0, is balanced, and is no class
of B[A→0] = B∖A; if s ≠ 0 it corresponds to the class {a*}. So "every class at depth j − 1 is balanced" says the
same in both. ∎
*Consequence.* The law of s is symmetric (negate the signs of A). By (F1) for a* in B[A→s]:

  Q_D(B) = Σ_s P(σ(A) = s)·Q_D(B[A→s]),  z(B) = Σ_s P(σ(A) = s)·z(B[A→s]).   (1)

(For z: P(σ(B∖A) = −s) is the probability that level 0 of B[A→s] is bad given the sign +1 on a*.)

**(F3)** A class that is a single element y is not balanced (half-sums ±v_y and 0; v_y ≠ 0). So a level j at
which some class at depth j − 1 is a single element is not bad; and if the positions of a nonempty family are
pairwise different modulo 2^d, no level j > d is bad for it, so that its Q equals its Q_d.

**Induction on the number m of elements.** m = 0: 1 ≤ 2. m = 1: level 0 is not bad (σ = ±v ≠ 0) and no other level
is (F3): Q = 0. Let m ≥ 2 and let the theorem hold for all families with fewer elements (any k).

**(A) Two elements of B have the same position.** Let A be the subfamily of all t ≥ 2 elements at that
position. No class divides A: (F2) with D = k, and (1) reads Q(B) = Σ_s P(s)·Q(B[A→s]), z(B) = Σ_s P(s)·z(B[A→s]).
Each B[A→s] has m − t or m − t + 1 < m elements, so Q(B[A→s]) ≤ 2·z(B[A→s]), and Q(B) ≤ 2·z(B).

**(B) The positions are pairwise different.** Let r be the least j such that they are pairwise different modulo
2^j (1 ≤ r ≤ k). A class at depth r − 1 has one or two elements (three would have two in one half, with equal
positions modulo 2^r), and some class at depth r − 1 has two. By (F3), Q(B) = Q_r(B).

**(B1) Two situations in which level r is never bad for B.**

*(B1a) some class at depth r − 1 is a single element w.* Then level r is not bad (F3). Take any two-element class
κ at depth r − 1; every class at depth ≤ r − 1 contains κ or is disjoint from it, so (F2) holds with A = κ,
D = r − 1, and Q(B) = Q_(r−1)(B) = Σ_s P(s)·Q_(r−1)(B[κ→s]). Each B[κ→s] has positions pairwise different modulo
2^r and contains w as a single-element class at depth r − 1, so by (F3) none of its levels ≥ r is bad:
Q_(r−1)(B[κ→s]) = Q(B[κ→s]) ≤ 2·z(B[κ→s]) by induction (m − 1 or m − 2 elements). With (1) for z: Q(B) ≤ 2·z(B).

*(B1b) every class at depth r − 1 has two elements, and for one of them, κ = {y, y′}, v_(y′) ≠ v_y and
v_(y′) ≠ −v_y.* Then κ is never balanced at level r (ε_y·v_y = ε_(y′)·v_(y′) would give v_(y′) = ±v_y), so level r is
not bad for B; and s = σ(κ) is never 0, for the same reason. As in (B1a), Q(B) = Σ_s P(s)·Q_(r−1)(B[κ→s]), and each
B[κ→s] = (B∖κ) ∪ {a*} has positions pairwise different modulo 2^r and the single-element class {a*} at depth
r − 1 (the class of κ), so none of its levels ≥ r is bad, and Q_(r−1)(B[κ→s]) = Q(B[κ→s]) ≤ 2·z(B[κ→s]) (m − 1
elements). Hence Q(B) ≤ 2·z(B).

**(B2) Every class at depth r − 1 has two elements, κ_i = {y_i, y′_i} (i = 1, …, n; m = 2n), and
v_(y′_i) = δ_i·v_(y_i) with δ_i ∈ {+1, −1} for every i.** Write v_i = v_(y_i).
- κ_i is balanced at level r iff ε_(y_i)·v_i = ε_(y′_i)·δ_i·v_i iff ε_(y_i) = δ_i·ε_(y′_i) (because ±2·v_i ≠ 0). This
  has probability 1/2, and then σ(κ_i) = 2·ε_(y_i)·v_i, which is not 0 and has a uniform sign. Otherwise
  σ(κ_i) = 0.
- Let U be the set of the i for which κ_i is balanced. Every subset has probability 2^(−n), and given U the
  values σ(κ_i) = ±2·v_i, i ∈ U, have independent uniform signs.
- Level r is bad iff U = {1, …, n}. Levels > r are not bad (F3).
- By (F2) applied to κ_1, …, κ_n in turn (D = r − 1; they are disjoint and no class at depth ≤ r − 1 divides any
  of them): the bad levels among 0, …, r − 1 of B are those of the family B_U of the elements a*_i, i ∈ U, with
  the position of y_i, the value 2·v_i ≠ 0 and the sign of ε_(y_i). The positions of B_U are pairwise different
  modulo 2^(r−1) (different classes at depth r − 1), so by (F3) the probability that some level ≤ r − 1 of B_U is
  bad is Q(B_U), for U ≠ ∅; for U = ∅ level 0 is bad: Q(B_∅) = 1.
Therefore

  Q(B) = 2^(−n)·[1 + Σ over the proper subsets U of Q(B_U)],  z(B) = 2^(−n)·Σ over all subsets U of z(B_U),

the 1 standing for U = {1, …, n} (level r bad). The proper subset U = ∅ contributes Q(B_∅) = 1; the other proper
subsets have at most n − 1 < m elements, so Q(B_U) ≤ 2·z(B_U). Hence

  Q(B) ≤ 2^(−n)·[1 + 1 + Σ over ∅ ≠ U ⊊ {1, …, n} of 2·z(B_U)] = 2^(−n)·[2·z(B_∅) + Σ over ∅ ≠ U ⊊ of 2·z(B_U)] ≤ 2·z(B),

since z(B_∅) = 1 and the term of U = {1, …, n} that is left out is ≥ 0.

The cases are exhaustive: under (B), either some class at depth r − 1 is a single element (B1a), or all have two
elements and some pair has values that are not equal up to sign (B1b), or all pairs have values equal up to sign
(B2). ∎

## 3. Three corollaries

**Corollary 1 (Lemma ρ of `lemma-rho.md`).** V = Z/3, every value 1: z(B) = p_m and Q(B) = 1 − ρ_2(B), so
ρ_2(B) ≥ 1 − 2·p_m = p_(m−1) for every nonempty multiset of m elements of Z_(2^k).

**Corollary 2 (characteristic 0).** Let n = 2^k·n′, n′ odd, B a multiset on Z_n, e | n′, η a root of unity of order
e. With V = Z[η] and the value η^b of the element b: by the slice criterion for the prime 2 (the powers
1, ω, …, ω^(2^(j−1)−1) of a root of unity ω of order 2^j are a basis of Z[ωη] over Z[η], and ω^(2^(j−1)) = −1; this is
S0 for p = 2 in Lean, `classSum_eq_of_badAt`, and its converse is the same computation), Φ_(2^j·e) divides the signed
mask iff level j is bad. So **the share of signings bad at 2^j·e for some j ≤ k is at most twice the share bad
at e.** For n = 2^k (e = 1): the share of signings that are not good is at most 2·C(m, m/2)/2^m for even m (3/4 for
m = 4, attained by {0, 0, 0, 1} on Z_2; 5/8 for m = 6), and 0 for odd m.

**Corollary 3 (Conjecture E).** Let n ≥ 1, 2^k the power of 2 in n, and B a nonempty multiset of m elements of
Z_n that is not {a, b} with 2^k ∤ a − b. Then B has a good signing. For m ≥ 3 the share of good signings is at
least 1/2 (m = 3), 1/4 (m = 4), and more than p_(m−1) − 0.2383 ≥ 5/16 − 0.2383 > 0.074 (m ≥ 5).

*Proof, given Lemma M, Lemma S3 and Lemma L3 of `../even-result-2.md`.* Write n = 3^a·n_3, 3 ∤ n_3, n_3 = 2^k·n″
(so gcd(n″, 6) = 1). As there, a signing is *3-bad at d* (d | n_3) if S(ζ) ∈ 3·Z[ζ] for ζ of order d, and *3-good* if
it is 3-bad at no d | n_3; by Lemma M a 3-good signing is good on Z_n.

*m ≥ 3.* Let e″ | n″, x a root of unity of order e″, R = Z[x], V = R/3R. 2v = 0 in V gives v = 4v − 3v = 0. Give
the element b the position b mod 2^k and the value x^b mod 3R, which is not 0 (x^b is a unit of R and R ≠ 3R). By
Lemma S3 for p = 2 and d = 2^j·e″ (d″ = e″; the slices are the σ of the classes, read in R), a signing is 3-bad at
2^j·e″, j ≥ 1, iff level j is bad; and it is 3-bad at e″ iff σ(B) = 0 in V, level 0. By Theorem T:

  the share of signings 3-bad at 2^j·e″ for some j ≤ k is at most twice the share 3-bad at e″.   (2)

By Lemma L3 (c), used with c = 2^j for each j, a signing that is 3-bad at some 2^j·e″ is 3-bad at 2^j, or at 2^j·e′
for some e′ > 1 that is live for B. So a signing that is not 3-good is 3-bad at 2^j·e′ for some j and some e′ in
L = {1} ∪ {the live e′ > 1}, and by (2) their share is at most 2·Σ_(e′ ∈ L) (share 3-bad at e′). The share 3-bad at
1 is p_m. The shares 3-bad at the live e′ > 1 add up to at most W(no 3) < 0.119134: this is what the proof of
Lemma L3 (c) shows for c = 1 (by (b) the share 3-bad at a live e′ is at most 2^(−μ(e′*)), the map e′ ↦ e′* is
injective on the live e′, and W(no 3) is the sum of 2^(−μ(e*)) over all e* > 1 with prime factors ≥ 5). And there is no live e′ > 1 unless B has at least five elements (a full group of a prime
q ≥ 5 has q occupied subclasses). So the share of signings that are not 3-good is at most
2·p_3 = 1/2 for m = 3, 2·p_4 = 3/4 for m = 4, and 2·p_m + 2·W(no 3) < 2·(11/32) + 0.2383 < 0.926 for m ≥ 5
(p_m ≤ 11/32 for m ≥ 5); in general it is at most 1 − p_(m−1) + 0.2383, since 2·p_m = 1 − p_(m−1).

*m = 1.* ±X^b has no root of unity as a zero. *m = 2, B = {a, b} with 2^k | a − b.* X^a + X^b vanishes at an n-th
root of unity ζ only if ζ^(a−b) = −1; but ζ^(a−b) is a power of ζ^(2^k), whose order divides n/2^k, an odd number. ∎

*What Corollary 3 does not use:* the first result (`../even-result.md`), Theorem 4 for odd n (it proves it again:
k = 0), the rest of the second result (Theorems F, G, J, Lemma ρ as computed, §5). It uses the reduction modulo 3
for every n, also when 3 ∤ n (a = 0), where Lemma M is the remark that 0 ∈ 3·Z[ζ].

## 4. Tests (programs of mine, beside this file; exact integer arithmetic, all signings)

- `twice_abstract.py`: Theorem T as stated, for random valued families of up to 9 elements with positions in Z_8
  and Z_32 and values in Z², (Z/3)², Z/9, Z/5 and Z: 9,000 families, no failure; the largest ratio Q/z is exactly
  2, in about four cases of ten (`twice-abstract.out`).
- `twice_test.py`: inequality (2) in the form used, "3-bad" computed from remainders modulo Φ_d with integer
  coefficients: every multiset containing 0 of up to 5 elements on Z_20 (`twice-exh-20.out`) and on Z_28
  (`twice-exh-28.out`), up to 4 on Z_40 (`twice-exh-40.out`); 1,500 random and structured multisets of 3 to 11
  elements on each of Z_40, Z_80, Z_56, Z_140, Z_280, Z_100 (`twice-rand-*.out`: random; few residues modulo the
  power of 2; pairs congruent modulo the odd part; a full set of residues modulo a prime; all congruent modulo
  the odd part). No failure; largest ratio exactly 2. The least share of 3-good signings seen: 1/2 for m = 3,
  1/4 for m = 4 and 5, and 9/32 or more for m = 8 to 11 in the random families.
- `rho_identities.py`, `rho_min.py` (Corollary 1; see `lemma-rho.md`).
- Before any of this: the confirming search of `../confirm.py` (6,002,729 multisets of 3 to 5 elements on eleven
  even groups and 20,000 structured ones up to Z_2000) found no multiset of three or more elements without a good
  signing.
