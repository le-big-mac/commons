*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

# The statement on signs for even n, second result: Conjecture E proved for every n ≡ 2 (mod 4), for n = 2^k·3^a, for at most nine elements, and in two more families; on an odd modulus more than half of the signings are good; open only for 4 | n (27 November 2026)

Answer to `brief-even-2.md`. Programs and outputs are in `prover2/` (list in §9). Nothing here is refereed or
formalised. It was found and written in about an hour and a quarter; Theorem J and Corollary K came last.

**An error in the first result?** I found none. I read `even-result.md` whole. I redid line by line Lemma N with
Remark 3 and Corollary N (the valuation argument is correct as written), Lemma Q, and the count in Lemma V. I read
Theorem A, Theorem B and the step-down and (β) of Proposition P and saw nothing wrong, without redoing every line.
I did not recheck Lemma S, part (2) of Proposition P (the 3/4), the proof of Theorem D (iii) beyond its arithmetic,
or the numbers W(…) other than W(no 3), which I recomputed. Its list of what is proved and what is open is right as
far as I can see. **But see the next paragraph: its list was not sharp, and I did not notice.** One caution on its
§6, not an error:
"Missing statement 1 … first order would do" may well be true of the sum, but §5.4 below gives explicit supports on
which the natural bounds that treat the levels e one at a time, through their live levels, fail (one has three
live dangerous levels 25, 75, 225 of the same rank); I think a proof has to add over the levels jointly.

**The first result was refereed and revised while I worked.** I worked from `even-result.md` as it was at the start
(the text kept as `even-result.as-returned.md`). After everything below was written I saw that the folder held a
referee's reports and two lists of changes (`even-revision-1.md`, `even-revision-2.md`); I read the beginning of
each list, their headings, and the revised head of `even-result.md`; nothing in `referee/`, and not the reports. What bears on this text: (a) the referee found that
**five elements, every n**, already follow from the first result (its sharpening (α) and the count of
Theorem D (iii): with five elements only 3 and 5 can be live), and that for odd m the count of Theorem D (iii)
closes further sets of primes, so that the family (II) is narrower than the brief and I had it: m odd, m ≥ 7, with
7 | n or 11 | n, or 13 | n together with 17 | n or 19 | n. I had noticed neither; so for m = 5 Corollary K below is
a second route, not a first proof. (b) The referee gave a shorter proof of Corollary N, and by its report found no
error in the mathematics. As far as I read the lists of changes (their headings and the first items, not every
line), the statements I cite (Corollary N, the step-down and (β) of Proposition P, Lemma V, Lemma Q) are unchanged;
a few lines of the proof of Lemma V were reworded. §0 and §4 below state what is not proved with the revised first
result taken into account.

**Whose is what.**
- *From the first result:* used as they stand, not reproved: for Proposition K and Corollary K only — Corollary N
  (a signing bad at some 2^j·e has λ_e(N) in a set of two values), the step-down and (β) of Proposition P (for odd m
  the share of bad signings is at most the sum R of 2^(1−D_e) over the live dangerous odd e > 1), Lemma V
  (D_e ≥ max_p l_p·(p − 1)), Lemma Q for p = 3. Theorems F and G and Proposition H use **nothing** of the first
  result except the shape of Theorem A's induction (Lemma F is that induction with "sum of signs ≠ 0" replaced by
  conditions modulo 3) and the count of occupied classes in Lemma V. They do use the number
  W(no 3) < 0.119134, whose tail bound is Lemma W of `sign-four-result.md` (refereed); the partial sum I recomputed.
- *From the brief's leads.* Lead 3 as given: "on an odd modulus more than half of the signings of every multiset of
  at least three elements are good; then the good signings with and without the twist must meet" — this is
  Proposition H (now proved) and the proof of Theorem G. The brief said Theorem 4's union bound is not sharp and
  that the level 3 is the costly one; the way out here (do not count the levels divisible by 3 at all) is mine.
  Lead 1: I took from it the two-prime picture (parities r_s + ρ_t, the "diagonal" caution) and changed it: the
  fibre formula of Lemma X is the general form, and the caution turned out to hold in a stronger form (§5.4).
  Lead 4 (small sizes exactly): reached for 5, 7, 9 elements by Proposition K and for 6 and 8 elements by Theorem J,
  not by lists of vanishing sums. Lead 2 (second order for even m): not used; (I) is closed for n ≡ 2 (mod 4), for
  n = 2^k·3^a and for m = 6, 8 by other means and stays open for 4 | n, m ≥ 10. Lead 5 (what cannot work): respected; §6 adds to it.
- *Mine.* Lemma M (the prime 3 can be peeled: nonvanishing modulo 3 at d′ gives nonvanishing at 3^i·d′ for all
  i); "3-good"; Lemma S3 and Lemma L3 (slice criterion, level bound and step-down, all modulo 3); Lemma F and
  Theorem F; Proposition H; Theorem G in the form with two residues modulo 2^k; Theorem J; Lemma X (fibre formula for D_e),
  Lemma A, Lemma Y, Proposition K and Corollary K (five elements: also, by another route, the first result's
  referee); the examples of §5.4; the tests.

## 0. Summary

n = 2^k·n′, n′ odd; B a nonempty multiset of m elements of Z_n; *exceptional pair*: B = {a, b}, 2^k ∤ a − b.
**Conjecture E**: B has a good signing unless it is an exceptional pair. Write n = 3^a·n_3 with 3 ∤ n_3, and
n_3 = 2^k·n″ (so gcd(n″, 6) = 1). "Live", "group", "full", the p-tree: as in the first result §1.

**Proved here, completely:**

- **Theorem F.** Let n be arbitrary and suppose that for no prime q ≥ 5 a level of the q-tree of B is live (for
  instance: n = 2^k·3^a; or B meets at most four classes modulo every prime q ≥ 5 that divides n). Then Conjecture E
  holds for B, with an explicit signing that depends only on the residues modulo 2^k. In particular
  **Conjecture E holds for n = 2^k·3^a** (every k, a, m).
- **Proposition H.** Let n be odd and m ≥ 3. Then more than half of the signings of B are good: at least 3/4 for
  m = 3, at least 5/8 for m = 4, more than 0.537 for m ≥ 5. (m = 1: all; m = 2: exactly half.)
- **Theorem G.** Let n be even and suppose the elements of B take at most two values modulo 2^k (always so if
  k = 1). Then Conjecture E holds for B. In particular **Conjecture E holds for every n ≡ 2 (mod 4)**. Share of good
  signings: at least 1/2 (m = 3), 1/4 (m = 4), more than 0.074 (m ≥ 5).
- **Theorem J.** For **every n**, every multiset of **6 or 8** elements has a good signing (at least 3/16, 9/64 of the
  signings are 3-good). (One step is a finite exact computation: the least share of signings good "on the 2-part"
  over all 2-trees with six, eight elements is 5/16, 21/64.) With Theorem B and Corollary K: **Conjecture E holds
  for every multiset of at most nine elements, for every n.**
- **Corollary K.** For **every n**, every multiset of **5, 7 or 9** elements has a good signing. (This one rests on
  the first result's Lemma N; margins 0.19 for 5 and 7 elements, 0.011 for 9. Five elements are also in the revised
  first result, by its referee; 7 and 9 are new.)
- Tools: Lemma M (peeling 3), Lemma L3 (levels modulo 3), Lemma X (fibre formula for the ranks D_e), Lemma A,
  Proposition K (for odd m: R < 0.8012 + R_fib, where R_fib is the part of the first-order sum that comes from
  "fibrewise dangerous" levels).

**What is not proved now** (with the first result as revised): only multisets with **4 | n**, **at least three
residues modulo 2^k** and **a live level at some prime q ≥ 5**, in the two families
(I′) 3 | n, m even, m ≥ 10;  (II′) 15 | n, m odd, m ≥ 11, and 7 | n or 11 | n, or 13 | n together with 17 | n or 19 | n
(the sets of primes are the revised first result's; before its revision: "n with a further odd prime factor").
No counterexample in any test. §4 says why the method of Theorems F, G stops at 4 | n; §5 what is missing for (II′).

## 1. Peeling the prime 3

Throughout, for a primitive d-th root of unity ζ and p^i ∥ d, d = p^i·d″, write ζ = y·x with y of order p^i and x
of order d″ (unique). Standard fact, used in the first result's Lemma V as well: Z[ζ] = R[Y]/(Φ_{p^i}(Y)) with
R = Z[x], Y ↦ y (Φ_{p^i} is irreducible over Q(x) since φ(d) = φ(p^i)φ(d″), and both sides are free over Z of rank
φ(d)). So Z[ζ] is a free R-module with basis Y^r·Z^t, 0 ≤ r < p^(i−1), 0 ≤ t ≤ p − 2, where Z = Y^{p^(i−1)} and
Z^(p−1) = −(1 + Z + … + Z^(p−2)).

**Definition.** A signing ε is *3-bad at d* (d | n_3) if S_ε(ζ) ∈ 3·Z[ζ] for ζ of order d (equivalently: the remainder
of S_ε modulo Φ_d has all coefficients divisible by 3; it does not depend on the choice of ζ). ε is *3-good* if it is
3-bad at no d | n_3. This depends only on the residues of B modulo n_3. If 3 ∤ n, 3-good implies good (0 ∈ 3Z[ζ]).

**Lemma M (peeling).** If ε is not 3-bad at d′ | n_3, then ε is not bad at 3^i·d′ for every 0 ≤ i ≤ a. Hence a
3-good signing is good on Z_n.
*Proof.* i = 0 is clear. Let i ≥ 1, ζ of order 3^i·d′, ζ = y·x, R = Z[x]. The ring homomorphism R[Y] → R/3R, Y ↦ 1,
kills Φ_{3^i}(Y) because Φ_{3^i}(1) = 3. So there is a ring homomorphism ρ : Z[ζ] → R/3R with ρ(x) = x, ρ(y) = 1, and
ρ(S_ε(ζ)) = Σ_b ε_b x^b mod 3 = S_ε(x) mod 3R. If S_ε(ζ) = 0 then S_ε(x) ∈ 3R: ε is 3-bad at d′. ∎

**Lemma S3 (slice criterion modulo 3).** Let p ≠ 3 be a prime (p = 2 allowed), d | n_3, p^i ∥ d, i ≥ 1, d = p^i·d″,
x of order d″, R = Z[x]. For a class C of the p-tree put s_C = Σ_{b ∈ C} ε_b x^b ∈ R (its *slice*). Then ε is 3-bad at
d iff in every group at level i (a class r modulo p^(i−1) with its p subclasses (r, t)) the p slices s_{r,t} are
congruent to one another modulo 3R.
*Proof.* With ζ = y·x: y^b = Y^r Z^t for b ≡ r + t·p^(i−1) (mod p^i), so S_ε(ζ) = Σ_r Σ_{t=0}^{p−1} s_{r,t} Y^r Z^t
= Σ_r Σ_{t ≤ p−2} (s_{r,t} − s_{r,p−1})·Y^r Z^t, and 3Z[ζ] = ⊕ 3R·Y^r Z^t. ∎
For p = 2: ε is 3-bad at 2^j·e″ (j ≥ 1) iff every class C modulo 2^(j−1) has s_{C′} ≡ s_{C″} (mod 3) for its two
children. For d″ = 1 the slices are the sums σ_C of the signs in C: ε is 3-bad at 1 iff σ_B ≡ 0 (mod 3), and at
2^j iff σ_{C′} ≡ σ_{C″} (mod 3) for every class C modulo 2^(j−1).

**Lemma L3 (levels modulo 3).** Let q ≥ 5 be prime (or q = 2), d | n_3, q^i ∥ d, i ≥ 1.
(a) *Step-down.* If level i of the q-tree is not live, every signing that is 3-bad at d is 3-bad at d/q.
(b) *Level bound.* The share of signings 3-bad at d is at most 2^(−Σ_D min(k_D, q−1)), the sum over the occupied
groups D at level i, k_D the number of occupied subclasses of D. If level i is the l-th live level of q, the share
is at most 2^(−l(q−1)).
(c) Let c be a power of 2 dividing n_3. Every signing that is 3-bad at c·e″ for some e″ | n″ is 3-bad at c, or
3-bad at c·e′ for some *live* e′ > 1, e′ | n″ (every q^i ∥ e′ a live level); and the signings of the second kind
have share at most W(no 3) := Σ over the integers e* > 1 with all prime factors ≥ 5 of 2^(−μ(e*)),
μ(e*) = max_q v_q(e*)·(q − 1). **W(no 3) < 0.119134.**
*Proof.* (a) Every occupied group has an empty subclass, whose slice is 0; if all groups are flat (Lemma S3), all
slices of the classes modulo q^i are ≡ 0 (mod 3R), hence so are their sums over the classes modulo q^(i−1) and
modulo q^(i−2): by Lemma S3 again (same x, same R) ε is 3-bad at q^(i−1)·d″ if i ≥ 2, and S_ε(x) = Σ of all slices
≡ 0 if i = 1. (b) *Fact:* for an occupied class C and β ∈ R, at most half of the sign vectors on C have
s_C ≡ β (mod 3R): flipping one sign ε_b changes s_C by ±2x^b, and 2x^b ∉ 3R (x^b is a unit, and R/3R ≠ 0 has
characteristic 3). The groups have disjoint sets of signs. A group with k < q occupied subclasses is flat only if
each of them has slice ≡ 0: share ≤ 2^(−k). A full group: fix the signs of one subclass; each of the other q − 1 must
hit its slice: share ≤ 2^(−(q−1)). For the count: let N_j be the number of occupied classes modulo q^j; N_0 = 1,
N_j ≥ N_(j−1), and N_j ≥ N_(j−1) + q − 1 if level j is live. So N_(i−1) ≥ 1 + (l − 1)(q − 1), and the sum is at least
(q − 1) + (N_(i−1) − 1) ≥ l(q − 1). (c) Apply (a) as long as some q^i ∥ e″ is not live. For a live e′ let
l_q be the number of live levels of q up to v_q(e′) and e′* = ∏ q^{l_q}; e′ ↦ e′* is injective on the live e′, and by
(b) with the best prime the share of 3-bad at c·e′ is at most 2^(−μ(e′*)). The number: `wsum2.py` (partial sum up to
t = 40: 0.118564492, by the product formula A(t) = ∏_{5 ≤ p ≤ t+1} (1 + ⌊t/(p − 1)⌋), checked by enumeration for
t ≤ 12) plus the tail bound 5.7·10^(−4) of Lemma W of `sign-four-result.md`, which applies because the terms are
sums over subsets of those of W. ∎

**The numbers p_r.** p_r := P(a sum of r independent signs is ≡ 0 mod 3). p_0 = 1, p_(r+1) = (1 − p_r)/2 (the sum
of r signs must be ≢ 0 and the new sign must be the right one): 1, 0, 1/2, 1/4, 3/8, 5/16, 11/32, 21/64, …;
p_r − 1/3 = (2/3)(−1/2)^r. So 1/4 ≤ p_r ≤ 1/2 for r ≥ 2, p_r ≤ 3/8 for r ≥ 3, p_r ≤ 11/32 for r ≥ 5.

## 2. Theorem F: a construction on the 2-tree, modulo 3

**Lemma F.** Let K ≥ 0 and let B be a nonempty multiset on Z_{2^K} that is not {a, b} with a ≠ b. Then B has a
signing with (0) σ_B ≢ 0 (mod 3) and (j), for j = 1, …, K: some class C modulo 2^(j−1) has σ_{C′} ≢ σ_{C″} (mod 3).
By Lemma S3 this signing is 3-bad at no 2^j, j ≤ K.

*Proof.* Induction on K (the program `sign3` in `thmF.py`). A set of r ≥ 2 elements has a signing with sum ≡ 0
(mod 3) (t minus signs, t ≡ −r mod 3, t ∈ {0, 1, 2}, t ≤ r), and a set of r ≥ 1 elements one with sum ≢ 0 (all +,
or one − if 3 | r). K = 0: sum ≢ 0. Let K ≥ 1, E and D the even and the odd elements, as multisets on Z_{2^(K−1)}
(x ↦ ⌊x/2⌋); the classes of B modulo 2^(j−1), j ≥ 2, are the classes of E and of D modulo 2^(j−2).
 - D = ∅ (or E = ∅): E is not a pair of distinct elements; sign it by induction. (0): σ_B = σ_E. (1): σ_E ≢ 0 = σ_∅.
   (j), j ≥ 2: property (j − 1) of E.
 - One half, C, has exactly one element (then the other, A, has at least two, since B is not an exceptional pair):
   sign A with σ_A ≡ 0, C anyhow. (0): σ_B ≡ ±1. (1): σ_A ≡ 0 ≢ ±1. (j), j ≥ 2: the class modulo 2^(j−1) that
   holds the element of C has one child with sum ±1 and the other with sum 0.
 - Both halves have at least two elements and one of them, A, is not a pair of distinct elements; C the other:
   sign A by induction and C with σ_C ≡ 0. (0), (1): σ_A ≢ 0 ≡ σ_C. (j), j ≥ 2: property (j − 1) of A.
 - E = {x, y}, D = {z, w}, x ≠ y, z ≠ w in Z_{2^(K−1)}; v_E = v_2(x − y), v_D = v_2(z − w). For a pair with signs
   (+, −): at level j of B the class holding both (if j − 2 ≤ v) is a witness iff j − 2 = v, and for j − 2 > v each
   of the two is alone in its class, a witness; so (+, −) fails to give a witness exactly for j − 2 < v. For signs
   (+, +): the class holding both is a witness iff j − 2 < v (children 2, 0); for j − 2 > v again a witness; so
   (+, +) fails exactly for j − 2 = v. If v_D ≥ v_E take E: (+, −), D: (+, +): both fail only if v_D < v_E. If
   v_D < v_E take E: (+, +), D: (+, −): both fail only if v_E < v_D. (0): σ_B = ±2. (1): the two sums are 0 and ±2. ∎

**Theorem F.** Let B be a multiset on Z_n, not an exceptional pair, such that no level of the q-tree of B is live
for any prime q ≥ 5. Then the signing of Lemma F for the residues of B modulo 2^k is good on Z_n.
*Proof.* B mod 2^k is not a pair of distinct elements. Let ε be the signing of Lemma F; it is 3-bad at no 2^j. If
ε were 3-bad at 2^j·e″ with e″ > 1, e″ | n″, Lemma L3 (a), applied to the primes of e″ one level at a time (no level
is live), would make it 3-bad at 2^j. So ε is 3-good, and good by Lemma M. ∎

Remarks. (1) For m ≤ 4 the hypothesis always holds (a live level of q ≥ 5 needs five elements): this is a second
proof of the existence part of Theorem B. (2) The construction is not the only choice; in the third case C is
free up to σ_C ≡ 0 (mod 3), about a third of its signings.

## 3. Proposition H and Theorem G

**Proposition H.** Let n be odd, B a multiset of m ≥ 3 elements on Z_n. The share of 3-good signings (for B mod
n_3 = n″), hence of good signings, is at least 1 − p_m − [m ≥ 5]·W(no 3): at least 3/4 for m = 3, 5/8 for m = 4, and
more than 1 − 11/32 − 0.119134 > 0.537 for m ≥ 5.
*Proof.* By Lemma L3 (c) with c = 1, a signing that is not 3-good is 3-bad at 1 (share p_m exactly, Lemma S3) or at
a live e′ > 1 (share ≤ W(no 3); there is no live e′ if m ≤ 4). Lemma M. ∎
(On Z_3, where there is no e″, the share of 3-good signings is exactly 1 − p_m; the least share of good signings
found in the tests is 3/4, 5/8, 3/4, 21/32 for m = 3, 4, 5, 6, equal to 1 − p_m for m = 3, 4, 6.)

**Theorem G.** Let n be even and let the elements of B take at most two values u_1, u_2 modulo 2^k. If B is not an
exceptional pair, it has a good signing; for m ≥ 3 the share of good signings is at least 2h − 1, h the bound of
Proposition H: at least 1/2, 1/4 for m = 3, 4 and more than 0.074 for m ≥ 5.
*Proof.* Let Q_1, Q_2 be the elements with residue u_1, u_2 (Q_2 may be empty), v = v_2(u_1 − u_2) < k, and
B° = B mod n′ on the odd Z_{n′}, with the same signs. For ζ = ξη, ξ of order 2^j, η of odd order e | n′, put
s_i = Σ_{b ∈ Q_i} ε_b η^b. Then S_ε(ζ) = ξ^{u_1}·(s_1 + ξ^{u_2−u_1}·s_2), and ξ^{u_2−u_1} is 1 for j ≤ v, −1 for
j = v + 1, and of order 2^(j−v) ≥ 4 for j ≥ v + 2; in the last case 1 and ξ^{u_2−u_1} are independent over Q(η), so
S_ε(ζ) = 0 forces s_1 = s_2 = 0. Hence ε is good for B iff s_1 + s_2 ≠ 0 and s_1 − s_2 ≠ 0 at every η of odd order
dividing n′, i.e. iff ε and ε·τ (τ = −1 on Q_2, +1 on Q_1) are both good for B° on Z_{n′}. ε ↦ ε·τ is a bijection
of the signings. For m ≥ 3 each of the two events has share ≥ h > 1/2 (Proposition H), so they meet, in a share
≥ 2h − 1. m = 1: clear. m = 2, not exceptional: both elements are in Q_1; X^a + X^b is good on the odd Z_{n′}
(ζ^{a−b} = −1 is impossible for ζ of odd order) and τ = 1. ∎

**Remark (the count that `thmG.py` tests).** For k = 1 one can also count directly: with E, D the even and odd
elements, a signing is 3-bad at neither 1 nor 2 iff exactly one of σ_E, σ_D is ≡ 0 (mod 3), which has share
p_E + p_D − 2p_E p_D (p_E = p_{|E|}); this is ≥ 1/4 unless |E| = |D| = 1 (least value 1/4 at sizes (1, 3)); and by
Lemma L3 (c) with c = 1, 2 the other levels cost at most 2·W(no 3) < 0.238269. So the share of 3-good signings on
Z_{2n″} is at least 1/4 − 0.238269 > 0.0117. In every test it was at least 1/4.

## 4. What is open, and why Theorems F and G stop at 4 | n

After the first result (as revised), Theorem F, Theorem G, Theorem J (below) and Corollary K (§5), Conjecture E is
not proved only when 4 | n, B has at least three residues modulo 2^k, some prime q ≥ 5 has a live level for B, and
(I′) 3 | n (and, by the first result's sharpening (α), the 3-tree of B has a live level) and m is even, m ≥ 10; or
(II′) 15 | n, m is odd, m ≥ 11, and 7 | n or 11 | n, or 13 | n together with 17 | n or 19 | n (the revised first
result, end of its §5, which I did not recheck; more exactly, by (α), the primes with a live level for B are not
3, 5 and primes ≥ 17, nor 3, 5, 13 and primes ≥ 23).

Lemma M reduces everything with 3 | n to: *every multiset on Z_{2^k·n″}, gcd(n″, 6) = 1, that is not an exceptional
pair has a 3-good signing* (call it E3; it would prove Conjecture E for every n with 3 | n). E3 is proved above for
n″ without live levels (Theorem F) and for k ≤ 1 or two residues (Theorem G, Remark). For general k the count
does not close: modulo 3 the levels 2^j·e″, j = 0, …, k, are **not nested** (the group algebra of Z_{2^k} over
Z[η]/3 is semisimple; Lemma N has no analogue), each live level of the 2-tree costs up to 2^(−μ(e″*)) again, and
against (L + 1)·W(no 3) for L live levels of the 2-tree stands a share of signings 3-good on the 2-part that is at
most about 1/2 and can be 1/4. For L = 1 this is 0.2383 < 1/4 (the Remark); for L = 2 already 0.357. A proof of E3
needs a construction on the 2-tree that leaves enough freedom for the primes ≥ 5 (Lemma F leaves the "other half"
free at every step, but I could not make the count conditional on it), or an idea of another kind.

**Six and eight elements: where the count does close for every k.** Let ρ_2(B) be the share of signings that
are 3-bad at no 2^j, j ≤ k. It depends only on the 2-tree of B with the levels that are not live removed (Lemma L3 (a) for q = 2: a
signing 3-bad at 2^j with level j not live is 3-bad at 2^(j−1)), a tree with at most m − 1 levels.

**Lemma ρ (computed).** For six elements ρ_2(B) ≥ 5/16; for eight elements ρ_2(B) ≥ 21/64. (`rho2.py`: a recursion
over all 507 trees with six elements and at most five levels, and all 36,680 trees with eight elements and at most
seven levels; exact fractions; the recursion was compared with all signings on 1,200 random multisets on Z_4, Z_8,
Z_16. The least values for m = 3, …, 8 are 1/2, 1/4, 3/8, 5/16, 11/32, 21/64, each at "m − 1 equal elements and one
other", where ρ_2 = p_(m−1).)

**Theorem J.** Every multiset B of six or of eight elements on Z_n, every n, has a good signing; at least 3/16
(six) and 9/64 (eight) of the signings are 3-good.
*Proof for six elements.* If no level of a q-tree, q ≥ 5, is live: Theorem F. Otherwise q = 5 (a live level needs q elements) and
exactly one level i of the 5-tree is live (two live levels need 5 + 4 occupied classes); the only live e′ > 1 is
e = 5^i. By Lemma L3 (c) a signing that is not 3-good is 3-bad at some 2^j or at some 2^j·e. *Claim: the signings
3-bad at 2^j·e for some j have share at most 1/8.* Then the share of 3-good signings is at least 5/16 − 1/8, and
Lemma M ends the proof. Proof of the claim: let η have order e, R = Z[η]; R/3R has the basis Y^r Z^t (t ≤ 3) of §1,
and a signed sum Σ_{b ∈ T} ±η^b lies in 3R iff in every group r the five signed counts c_{r,t} of T in the
subclasses (r, t) are congruent modulo 3. Let b_0, …, b_4 be elements in the five subclasses of a full group r_0;
the sixth element shares a subclass with at most one of them, so at least four of them are alone in their
subclass. If a class C of the 2-tree with twisted signs has sum in 3R ("is flat") and holds one of these four,
that subclass has c = ±1, so all five subclasses of r_0 meet C: C has at least five elements. A class of one
element is never flat. Hence, if every nonempty class modulo 2^(j−1) is flat (Lemma S3 for p = 2, j ≥ 1), B lies in
one class modulo 2^(j−1). Let j_0 be the least j ≥ 1 with B not in one class modulo 2^j. For 1 ≤ j < j_0 the class
has an empty child and "3-bad at 2^j·e" is "3-bad at e"; for j = j_0 it says that ε·τ is 3-bad at e, τ = −1 on one
child of the class; for j > j_0 it is impossible. Each of the two events has share at most 2^(−4) (Lemma L3 (b),
q = 5, l = 1). ∎
*Proof for eight elements.* At most one level i of the 5-tree and one level i′ of the 7-tree are live (two live
levels of 5 need nine occupied classes; 11 needs eleven elements), so the live e′ > 1 are among 5^i, 7^{i′},
5^i·7^{i′}. "Flat" is as above. I show that the signings 3-bad at 2^j·e′ for some j and some live e′ have share at
most 5/32 + 1/32 + 0; with ρ_2 ≥ 21/64 this leaves 9/64.
(α) e = 7^{i′}. At least six of the seven subclasses of a full group hold one element of B; a flat class holding
one of these has at least seven elements, and the eighth element is not flat alone. So, as for six elements, the
share is at most 2·2^(−6).
(β) e = 5^i·7^{i′}, both live: no signing is 3-bad at 2^j·e. Use Lemma S3 with p = 7, d″ = 2^j·5^i, x of order d″,
R = Z[x]. In a full 7-group at least six subclasses hold exactly one element, with slices ±x^b. If two of them are
congruent modulo 3R, then 1 − ω ∈ 3R for the root of unity ω = ±x^{b−b′}, whose order is prime to 3; the norm of
1 − ω from Q(x) to Q is 0, 1 or a power of a prime other than 3, and a nonzero element of 3R has a norm divisible
by 3; so ω = 1, x^{b−b′} = ±1 and 5^i | b − b′. Six elements congruent modulo 5^i leave at most three occupied
classes modulo 5^i: level i of 5 is not live, a contradiction.
(γ) e = 5^i, r_0 a full group. Call an element a *single* if it is alone in its subclass of r_0; there are at least
two (five subclasses, three further elements). Let j ≥ 1 and let every nonempty class modulo 2^(j−1) be flat. A flat
class holding a single meets all five subclasses of r_0, so it has at least five elements: one class, C_N, holds
all the singles, and the other classes hold at most three elements together. In such a class C′ the signed counts
in the subclasses of the singles are 0, so all five counts in r_0 are ≡ 0, and so are the counts in every other
group (it holds at most three elements, so it has an empty subclass). So every subclass that meets C′ meets it in
two elements of opposite twisted signs or in three of equal twisted signs: there is at most one class C′, a pair
or a triple inside one subclass, and it is flat for at most half of its signings whatever the twist. Now let j_0
be the least j ≥ 1 with B not in one class modulo 2^j. The levels 1 ≤ j < j_0 give the event E_0: ε is 3-bad at e.
Level j_0 gives E_1: ε·τ is 3-bad at e (τ the twist of that level). For j > j_0 the nonempty classes modulo 2^(j−1)
must be C_N and C′, the two children at level j_0, undivided. Let j_1 > j_0 be the least level at which C_N or C′
is divided. For j_0 < j < j_1 level j is not live, and the event lies in that of level j − 1 (Lemma L3 (a), q = 2),
hence in E_1. Level j_1 gives E_2: C_N flat and C′ flat for the twists of that level; the two have disjoint signs,
C_N meets all five subclasses of r_0 (Lemma L3 (b) for the multiset C_N: share ≤ 2^(−4)), C′ costs ≤ 1/2. For
j > j_1 there are at least three nonempty classes: impossible. So the share is at most 2^(−4) + 2^(−4) + 2^(−5). ∎
(For ten elements the same case analysis grows: two live levels of 5, the prime 11, and more kinds of flat
classes. Not done.)

## 5. Odd m: the first-order sum, the fibre formula, and 5, 7, 9 elements

Frame (first result, Proposition P with (β)): for odd m the share of bad signings is at most
R := Σ over the odd e > 1 that are live for W and dangerous for f of 2^(1−D_e(W)), where F = B mod n′, W its
support, f ∈ F_2[Z_{n′}] the parities of the multiplicities (odd weight), π_e : F_2[Z_{n′}] → A_e := Z[η_e]/2 the map
δ_w ↦ η_e^w, "e dangerous" means π_e(f) = 0, and D_e(W) = dim span{π_e(δ_w) : w ∈ W}.

### 5.1 Lemma X (fibre formula)

Let p be an odd prime, p^i ∥ e, i ≥ 1, e = p^i·e_2. For a class c of the p-tree let W_c = W ∩ c, f_c = f restricted
to c, V_c = span{π_{e_2}(δ_w) : w ∈ W_c} ⊆ A_{e_2}, Φ(c) = π_{e_2}(f_c) ∈ V_c. (Φ(c) is the sum of Φ over the children
of c; V_c is the sum of the V of the children.) Call c *active* if Φ(c) ≠ 0.

**Lemma X.** (i) D_e(W) = Σ over the classes r modulo p^(i−1) of [Σ_t dim V_{r,t} − dim ∩_t V_{r,t}] (t ∈ Z_p, the
children of r). (ii) e is dangerous iff for every r the p elements Φ(r, t) are equal; then they equal Φ(r).
(iii) Σ_t dim V_{r,t} − dim ∩_t V_{r,t} ≥ dim V_r + (p − 2)·dim ∩_t V_{r,t}. So D_e(W) ≥ Σ_r dim V_r ≥ D_{e_2}(W).
*Proof.* Z[η_e] = Z[η_{p^i}] ⊗ Z[η_{e_2}] with η_e = η_{p^i}·η_{e_2} (coprime orders), so
A_e = F_2[Y]/(Φ_{p^i}(Y)) ⊗ A_{e_2}, π_e(δ_w) = Y^w ⊗ π_{e_2}(δ_w), and Y^w = Y^r Z^t for w ≡ r + t·p^(i−1). With the
basis Y^r Z^t (t ≤ p − 2) and Z^(p−1) = 1 + Z + … + Z^(p−2) (characteristic 2), A_e = ⊕_r (block r), and the map
(v_t)_{t ∈ Z_p} ↦ Σ_t Y^r Z^t ⊗ v_t = Σ_{t ≤ p−2} Y^r Z^t ⊗ (v_t + v_{p−1}) from (A_{e_2})^p onto block r has kernel the
diagonal. The span of the π_e(δ_w), w in the class r, is the image of ⊕_t V_{r,t}: dimension Σ_t dim V_{r,t} minus
the dimension of the diagonal vectors in it, which is dim ∩_t V_{r,t}. (ii) π_e(f) = Σ_r Σ_t Y^r Z^t ⊗ Φ(r, t) is 0
iff every (Φ(r, t))_t is diagonal; and Σ_t Φ(r, t) = p·Φ(r, 0) = Φ(r, 0). (iii) With c = dim ∩_t V_{r,t}: the spaces
V_{r,t}/∩ span V_r/∩, so Σ_t (dim V_{r,t} − c) ≥ dim V_r − c. ∎
(Tested exactly: for p = 3 on 43,000 pairs (W, e) in `ranks2.py`, and for p = 3, 5, 7, 11 on 164,400 triples (W, e, p), prime
powers e included, in `lemmaXY.py`.)

**Lemma Y.** Let g ∈ F_2[Z_{n′}] have odd weight and π_e(g) = 0, e > 1 odd. Then the support of g has at least q
points, q the least prime factor of e.
*Proof.* Induction on the number of primes of e. Take p | e, e = p^i e_2. By Lemma X (ii) either some Φ(r) ≠ 0, and
then the p restrictions g_{r,t} are all nonzero (p ≥ q points); or every restriction g_c to a class modulo p^i has
π_{e_2}(g_c) = 0. One of them has odd weight; e_2 = 1 is impossible (π_1 is the parity of the weight), so e_2 > 1 and
the induction applies to g_c. ∎

### 5.2 Lemma A and Proposition K

Now p = 3, e_2 > 1 prime to 3, e = 3^i·e_2, i ≥ 1.

**Lemma A.** (a) Suppose e_2 is **not** dangerous and e is dangerous; let l′ be the number of i′ ∈ {1, …, i} with
3^{i′}·e_2 dangerous. Then D_e(W) ≥ D_{e_2}(W) + 3^(l′−1) (and D_e(W) ≥ 2·3^(l′−1)).
(b) Suppose e_2 and e are dangerous and some class modulo 3^(i−1) is active; let i_1 be the least depth with an
active class and l″ the number of i′ with i_1 < i′ ≤ i and 3^{i′}·e_2 dangerous. Then l″ ≥ 1 and
D_e(W) ≥ D_{e_2}(W) + 1 + 2·3^(l″−1).
*Proof.* Let o_j be the number of active classes modulo 3^j. An active class has an active child, so o_j ≥ o_(j−1);
if 3^j·e_2 is dangerous, the three children of every class c have Φ = Φ(c) (Lemma X (ii)), so o_j = 3·o_(j−1).
For an active class r modulo 3^(i−1), 0 ≠ Φ(r) ∈ ∩_t V_{r,t}. By Lemma X (i), (iii):
D_e(W) ≥ Σ_r dim V_r + o_(i−1). (a) o_0 = 1, so o_(i−1) ≥ 3^(l′−1); and Σ_r dim V_r ≥ D_{e_2}(W) (also ≥ o_(i−1)).
(b) Φ(root) = 0. If i ≤ i_1, no class modulo 3^(i−1) is active; so i > i_1. o_{i_1} ≥ 2 (the Φ of the classes
modulo 3^{i_1} sum to 0 and one is not 0), so o_(i−1) ≥ 2·3^(l″−1). The nonzero Φ(r) ∈ V_r, r modulo 3^(i−1), sum to
0, so the sum of the V_r is not direct: Σ_r dim V_r ≥ D_{e_2}(W) + 1. ∎

Call a pair (e_2, i) *fibrewise dangerous* if e_2 > 1 is prime to 3, i ≥ 1, and **every** class modulo 3^i has
Φ = 0 (then e_2 and all 3^{i′}·e_2, i′ ≤ i, are dangerous). Let
R_fib := Σ over the fibrewise dangerous pairs with 3^i·e_2 live of 2^(1−D_{3^i e_2}(W)).

**Proposition K.** For odd m (every n): R < 0.80118 + R_fib.
*Proof.* Split the e of R as e = 3^i·e_2. (1) e_2 = 1: at most δ_3 = Σ_{l ≥ 1} 2^(1−2·3^(l−1)) < 0.531258 (first
result, Lemma Q). (2) For a live e_2 > 1 let c(e_2) be the sum of 2^(1−D_e) over e_2 itself (if dangerous) and the
live dangerous 3^i·e_2, i ≥ 1, that are not fibrewise. If e_2 is not dangerous, the dangerous levels i have
different l′, and by Lemma A (a) c(e_2) ≤ 2^(1−D_{e_2}(W))·Σ_{l′ ≥ 1} 2^(−3^(l′−1)) < 0.62696·2^(1−D_{e_2}(W)). If e_2 is
dangerous, a dangerous level i is fibrewise (i < i_1) or as in Lemma A (b) (i > i_1; i = i_1 cannot be dangerous: at
a dangerous level the children of an inactive class are inactive),
with different l″: c(e_2) ≤ 2^(1−D_{e_2}(W))·(1 + Σ_{l″ ≥ 1} 2^(−1−2·3^(l″−1))) < 1.13282·2^(1−D_{e_2}(W)). By Lemma V and
the injection e_2 ↦ e_2*, Σ over the live e_2 > 1 of 2^(1−D_{e_2}(W)) ≤ 2·W(no 3) < 0.238269. Together:
0.531258 + 1.13282·0.238269 + R_fib < 0.80118 + R_fib. ∎

**Corollary K.** Let m ∈ {5, 7, 9}. Every multiset of m elements on Z_n, every n, has a good signing; the share of
bad signings is less than 0.8012 for m = 5, 7 and less than 0.9887 for m = 9.
*Proof.* Let (e_2, i) be fibrewise dangerous with 3^i·e_2 live. f has odd weight, so some class c* modulo 3^i has
f_{c*} of odd weight, and π_{e_2}(f_{c*}) = 0: by Lemma Y, c* holds at least 5 points of odd multiplicity. Every
other occupied class c modulo 3^i holds at least 2 elements of B: either f_c = 0 (all multiplicities even) or f_c ≠ 0
with π_{e_2}(f_c) = 0, and a single point is not dangerous. Level i of 3 is live: three occupied classes in one
group. So m ≥ 5 + 2 + 2 = 9: for m = 5, 7, R_fib = 0 and R < 0.8012. For m = 9 there is equality: B is five points
of multiplicity 1 in c* and two elements in each of the two sister classes of c*, nothing else; so i is the only
live level of the 3-tree (three occupied classes modulo 3^i, one modulo 3^(i−1)); the two elements of a sister
class are equal or congruent modulo e_2 (f_c = 0, or two points with π_{e_2}(δ_w + δ_{w′}) = 0), so W has at most 7
points modulo e_2, one relation among them (π_{e_2}(f_{c*}) = 0), D_{e_2}(W) ≤ 6, μ(e_2*) ≤ 6, e_2* ∈ {5, 7, 35}. With
D_{3^i e_2}(W) ≥ D_{e_2}(W) ≥ μ(e_2*): R_fib ≤ 2^(−3) + 2^(−5) + 2^(−5) = 3/16 and R < 0.80118 + 0.1875 < 0.9887. ∎

(For m = 11 a count of the same kind, which I did not write out, gives about 13/64 for R_fib and so about 1.004: not
enough as it stands.)

### 5.3 What is missing for (II′)

> **Missing statement 1′.** For every multiset with an odd number of elements on an odd Z_{n′}: R_fib < 0.198, where
> R_fib is the sum of 2^(1−D_{3^i e_2}(W)) over the pairs (e_2, i) with e_2 > 1 prime to 3, 3^i·e_2 live, and every
> class modulo 3^i carrying an e_2-dangerous restriction of the multiset.

With Proposition K this gives a good signing for every multiset with an odd number of elements on every Z_n. In
the tests R − R_fib was at most 21/32 and R at most 5377/8192 ≈ 0.6564. What is known about a fibrewise pair: one
class modulo 3^i holds an odd e_2-dangerous restriction, at least 5 points (Lemma Y); D_{3^i e_2} ≥ max(D_{e_2}(W),
number of occupied classes modulo 3^(i−1) plus 1).

### 5.4 Why one level at a time cannot do it: five supports (`examples5.py`, exact)

1. Z_45: W_2 = {0, 15, 30} (a coset of order 3), W = W_2 ∪ {1, 2, 28, 29}. 45 is live and dangerous with D_45 = 6,
   while the levels 1, 2 of 3 and 1 of 5 are live: "D_e ≥ 1 + Σ_p (l_p(p − 1) − 1)" (= 7) is **false**.
2. Z_105: W_2 = {0, 35, 70}, W = W_2 ∪ {1, 2, 3, 4, 69, 89} (six points that make 5 and 7 live, on a diagonal of
   Z_5 × Z_7 as far as that goes). D_105 = 8, not 1 + 1 + 3 + 5 = 10:
   the primes that do not carry the danger behave like the brief's diagonal.
3. Z_225: W_2 = {0, 45, 90, 135, 180} (a coset of order 5), W = W_2 ∪ {1, 2, 3, 204}. The levels 25, 75, 225 are all
   live and dangerous with the **same** rank 8 = μ(25): for e_2 = 25 each of the two mixed levels costs as much as
   e_2 itself. So for a dangerous e_2 no bound "mixed levels ≤ ρ·2^(1−μ(e_2*))" with ρ < 2 holds, while a sum over
   all e_2* of such bounds needs ρ below about 0.96 (`wsum2.py`: total 0.926 for ρ = 2/3, 0.982 for ρ = 0.9, 1.006 for
   ρ = 1). The pairs (25, 1), (25, 2) are fibrewise.
4. Z_225: W = W_2 = three cosets of order 5 in the three classes modulo 3: D_75 = D_25(W) = 12 exactly; equality
   D_e = D_{e_2}(W) in Lemma X (iii) is possible for a dangerous e_2 (the fibres are independent).
5. Z_15: the cross W_2 = {0, 3, 6, 9, 12}, W = W_2 ∪ {5, 10}: D_15 = 5 = D_5(W) + 1 (in every test a live dangerous 15
   had D_15 ≥ 5).

So a proof of Missing statement 1 or 1′ must add over the e jointly (the same few points make many e live at
once only on a "diagonal", and a diagonal carries no danger), not bound each e by its live levels.

## 6. Roads that failed

1. *E3 for general k by counting* (§4): the levels of 2 are not nested modulo 3; (L + 1)·W(no 3) against a share
   ≤ 1/2. Using Lemma N for the levels 2^j·e″ and peeling only for 3 | d does not help: the mixed levels 3^i·e″
   then cost Σ 2^(1−max(2l, μ)) ≈ 0.78 by Lemma V.
2. *Peeling two primes.* "p-good and q-good on Z_{n/(p^a q^b)}" does not give good on Z_n: the reduction modulo
   1 − ζ_p says nothing about divisibility by q afterwards. Only one prime can be peeled, and the prime 2 cannot
   (modulo 2 the signs disappear).
3. *E3 by induction on k as in Lemma F with the other half random.* For a fixed signing of the half A the other
   half must avoid ±(the slice of A) at every e″, a target that is not 0, so the step-down is lost and a small half
   (two elements) can be blocked; this is road 1 of the first result again, modulo 3.
4. *"More than half" for more than two events.* Proposition H gives two events that must meet (k = 1). For k = 2
   three are needed (S(η), S(−η) and a witness at depth 1), each of share > 1/2 only; with the flip of one half as
   a symmetry it would suffice that the deep levels hold with share > 0.905 or are independent of the level 0, and
   neither is true in general.
5. *Rank bounds one level at a time* (§5.4): the multiplicative bound, the bound D_{3^i e_2} ≥ μ(e_2*) + 2l − 1 (false:
   support 3), and D_{3^i e_2} ≥ D_{e_2}(W) + l (false: support 4) were each tested and refuted.
6. A second-order form of Lemma N for even m (lead 2) and lists of vanishing sums for m = 6 (lead 4): not tried.

## 7. Tests

Exact integer arithmetic; programs of my own (`lib2.py`: remainders modulo Φ_d; compared with complex evaluation
on 7,650 (signed multiset, level) pairs, 687 of them bad: `selfcheck.py`). "All signings" means all 2^m.

- **Lemma F, Theorem F for n = 2^k·3^a** (`thmF.py`): the construction is 3-good on Z_{2^k} and good on Z_n for all
  multisets with 0 up to 9, 8, 6, 5 elements on Z_2, Z_4, Z_8, Z_16 and up to 3 to 8 elements on n = 6, 12, 18, 24, 36,
  48, 54, 72, 96, 108, 144, 162 (1,796,304 multisets; the 620 exceptional pairs were confirmed to have no good
  signing); every nonempty subset of Z_8, Z_12, Z_16 (69,683 good, 202 exceptional pairs); 4,800 random and
  structured multisets of 2 to about 48 elements on 12 moduli 2^k·3^a up to 2592 (closed under x ↦ x + n/2, unions of
  cosets, all three classes modulo 3 of even size, few residues modulo 2^k).
- **Theorem F in general** (`more_tests.py F`): all multisets with 0 up to 3 to 6 elements on n = 10, 20, 30, 40, 60,
  84, 120, 140, 210 without a live level at a prime ≥ 5 (553,561, plus 493 exceptional pairs; 1,696 with a live
  level skipped), and 2,700 random multisets of 3 to 30 elements with at most four residues modulo each prime ≥ 5
  on n = 60, …, 9240: the construction's signing is good every time.
- **Lemmas M, S3, L3 and the Remark of §3** (`thmG.py`, all signings): 377,362 multisets (all with 0 up to 4 to 8
  elements on n = 6, 10, 18, 30, 42, 54, 66, 70, 90) and 2,018 random and structured ones of 3 to 12 elements on 13
  moduli up to 2310 (closed under +n/2, unions of cosets, even classes modulo 3, a full level of a prime ≥ 5, few
  values modulo n′): bad at 3^i·d′ implies 3-bad at d′; the step-down modulo 3; the level bound 2^(−μ) (attained);
  the share p_E + p_D − 2p_E p_D exactly; share of 3-good ≥ that minus the sum; every 3-good signing good; least
  share of 3-good signings 1/4.
- **Theorem G with two residues** (`more_tests.py G2`): 1,320 multisets of 3 to 11 elements with two residues modulo
  4 or 8 on 11 moduli up to 1320: least share of 3-good signings 1/4.
- **Proposition H** (`more_tests.py H`, all signings): all multisets with 0 up to 4 to 9 elements on n = 3, 9, 15, 21,
  27, 35, 45, 75, 105, and 900 random and structured ones of 3 to 13 elements on n up to 1155: more than half good
  for m ≥ 3 every time (least 5/8).
- **Lemma X, Lemma A, the bound of Lemma A (b)** (`ranks2.py`; ranks over F_2 exactly): see the counts in
  `ranks2_a.out`, `ranks2_b.out`, `ranks2_c.out` (31,000 supports on Z_15, …, Z_1575, built to be dangerous at several
  e at once: unions of cosets, full groups with a repeated pattern, one point in every class modulo q); the fibre
  formula holds exactly; Lemma A (a) held in every case (about 4,200, slack 0 attained); Lemma A (b) in every case
  with an active class, but those were few (46): **(b) is the least tested statement here.**
- **Lemma X for p = 3, 5, 7, 11 and Lemma Y** (`lemmaXY.py`): 13,200 supports on 11 odd moduli from 15 to 1155: the
  fibre formula exactly for every e and every prime of e; Lemma Y on 14,146 pairs (odd W_2, dangerous e).
- **Proposition K, Corollary K** (`propK.py`, `corK.py`): R − R_fib ≤ 0.801174 (largest value found 21/32) on 13,500
  multisets of 5 and 7 elements (R_fib = 0 and R ≤ 5/8 for all of them) and 13,500 larger structured ones on nine odd moduli (1,736 with a
  fibrewise pair); and directly, all signings, 1,920 multisets of 5, 7, 9 elements on n = 60, 120, 180, 420, 660, 840,
  1260, 2100: share of bad signings ≤ R < 1 (largest share 1/2).
- **Theorem J, eight elements** (`thmJ8.py`, all 256 signings): 6,000 random and structured multisets of eight
  elements on n_3 = 20, 40, 80, 100, 140, 280, 400, 560, 700, 1120 (among them the shape of the proof: a class with all
  five subclasses and a pair or a triple apart in the 2-tree; seven classes modulo 7 and five modulo 5 at once):
  ρ_2 ≥ 21/64 (attained); share of signings 3-bad off the 2-part and not on it ≤ 3/16 (largest found 5/64); share of
  3-good ≥ 9/64 (least found 1/4). Note: this test measures the signings 3-bad off the 2-part *and not on it*, which
  is at most the quantity bounded in the proof.
- **Lemma ρ and Theorem J, six elements** (`rho2.py`, `thmJ.py`, all 64 signings): every multiset of six elements with 0 on Z_20
  (42,504) and 4,000 random and structured ones on each of n_3 = 40, 80, 100, 140, 200, 280, 400, 560, 700, 1120, 3080
  (one element in every class modulo 5 inside one class modulo 2^j; a coset of order 5 shifted in the 2-tree; two
  residues modulo 2^k): ρ_2 ≥ 5/16 (attained), share of signings 3-bad only off the 2-part ≤ 1/8 (largest found
  1/16), share of 3-good ≥ 3/16 (least found 1/4).
- **Numbers** (`wsum2.py`): W(no 3), p_r, the least value of p_E + p_D − 2p_E p_D, δ_3, the sums of §5.

Not tested: Lemma X (ii), (iii) by themselves (only through Lemma A and Lemma Y); anything beyond about 48
elements; the shares of Theorem G and Proposition H for m ≥ 5 beyond 13 elements. Nothing formalised.

## 8. What I am least sure of

1. **Corollary K for m = 9**: margin 0.011, and it stands on the whole chain (first result's Corollary N, Lemma Q,
   Lemma V; Lemma X, Lemma A (b), Lemma Y; the number 0.238269). m = 5 and 7 have margin 0.19 but the same chain.
2. **Lemma A (b)** (46 test cases only).
3. **Theorem G for m = 3, 4, 5** rests on Proposition H's exact shares (3/4, 5/8) and for m ≥ 5 on
   1 − 11/32 − W(no 3) > 1/2, i.e. on W(no 3) < 0.156; the margin is comfortable. The identification
   Z[ζ] = Z[x][Y]/(Φ_{p^i}) is used everywhere (Lemma M, S3, X).
4. **Lemma F**, the case of two pairs (the bookkeeping of levels j − 2 against v_E, v_D); it is exactly what
   `thmF.py` runs, and every subset of Z_16 passed.
5. **Theorem J** rests on Lemma ρ, a computation over 507 and 36,680 trees (the recursion was compared with brute
   force, but the claim that m − 1 levels are enough rests on the step-down for the 2-tree), and on the bookkeeping
   of the flat classes; the case of eight elements, (γ), was written last and fast, and its test is a sample.
6. The statement of what is not proved (§0, §4) combines this result with the first result's Theorem D and with
   the sets of primes of its revision, neither of which I rechecked in full; and I missed, as the referee of the
   first result did not, that five elements were already within its reach.

## 9. Housekeeping and files

Every program ran through `~/bin/cap2g.sh`, at most three at a time, the longest about three minutes (`thmJ.py`). Nothing
outside `prover2/` and this file was written; no file beginning with `expect` and nothing in `referee/` was opened;
no network; nothing posted; nothing left running.

`prover2/`: `lib2.py` (Φ_d, remainders, bad and 3-bad at d), `selfcheck.py`, `selfcheck.out`;
`thmF.py` (the construction `sign3`; modes exhaust, subsets, random) with `thmF_exhaust.out`, `thmF_subsets.out`,
`thmF_random.out`; `thmG.py` with `thmG_exhaust.out`, `thmG_random.out`; `more_tests.py` (modes F, G2, H) with
`more_F.out`, `more_G2.out`, `more_H.out`; `wsum2.py`, `wsum2.out` (the numbers);
`ranks.py`, `ranks.out` (first rank test; it also holds the helpers), `ranks2.py`, `ranks2_a.out`, `ranks2_b.out`,
`ranks2_c.out` (Lemma X, Lemma A), `examples5.py`, `examples5.out` (the five supports of §5.4), `propK.py`,
`propK.out`, `corK.py`, `corK.out` (Proposition K, Corollary K), `lemmaXY.py`, `lemmaXY.out` (Lemma X for other primes,
Lemma Y), `rho2.py`, `rho2.out`, `thmJ.py`, `thmJ.out`, `thmJ8.py`, `thmJ8.out` (Lemma ρ, Theorem J).
