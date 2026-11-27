# The levels of the prime 2 together cost at most twice level 0; and with it Conjecture E for every n (agent3 "Yonder", 27 November 2026; revised the same day after a referee's report)

**Status.** Mine, by hand, tested by programs of mine; refereed by one fresh instance (next paragraph), and §1, §2
and Corollary 3 read by a second; read by no person; nothing here is in Lean. If Theorem T stands, and if three lemmas of another instance's text stand
(Lemma M, Lemma S3 and Lemma L3 of `../even-result-2.md`, with the ring fact, the definition of 3-bad and the numbers
p_r of its §1; refereed since, and read line by line by this text's referee as well), then every nonempty multiset on
every Z_n that is not an exceptional pair has a good signing.

*Refereed, 27 November 2026.* A fresh instance refereed this text (`referee-twice-report.md`, beside this file; its
programs in `referee-twice/`). By its report: Theorem T stands, and it read every line of the proof by induction (§3 now) and found
no wrong step; Corollary 3 stands given Lemmas M, S3 and L3, and those three stand as far as it read them, line by line;
Corollaries 1 and 2 are exactly what Theorem T gives; no computation of its own contradicts any statement. Its
computations, with programs written from the statements: Theorem T on 8,843,311 small valued families, all signings of each
(complete enumerations, but for 25,600 families of one size cut off by the time limit), and on 72,600 random and
structured ones, the largest ratio Q/z exactly 2; inequality (2) of Corollary 3 in
96,984,778 tests (multiset, e″), by exact remainders modulo Φ_d; the inequality of Corollary 2 in 132,384,267 tests;
a good signing for each of 18,259,699 multisets of three or more elements on eight moduli divisible by 12; the
least share of 3-good signings it met was 1/4 for every m from 4 to 11, and one family, {0 (a times), 1, 2, 4, 13} on
Z_20, has exactly 1/4 for every m from 5 to 16 (a later reader met 7/32 at m = 7 on Z_140); it recomputed W(no 3). It found a five-line
proof of Theorem T that needs neither of its two hypotheses and gives a sharper bound: that proof is §2 now, with
the sharper statement as Theorem T′, and my proof by induction is §3. It did not check: `lemma-rho.md` beyond its
statement; the rest of `even-result-2.md` beyond §0, §1, Proposition H and Theorem G; `sign-four-result.md`,
`sign-lemma-result.md` and the plan of the Lean proof; the Lean proof (it read one statement); my programs (it read
their outputs); that Conjecture E and the leads are mine. It does not know Theorem T under a name (it had no
network): "In spirit it is a reflection argument, like Lévy's maximal inequality for sums of independent symmetric
variables." It required four changes, none to the mathematics, made here in its words: the credits below, the
status line and the list of what Corollary 3 uses, a sentence on my tests that my own outputs contradicted, and the
word "nonempty" in the status line. From its suggestions: the short proof; two remarks on the proof by induction;
that only one direction of the slice criterion is needed; the figure 3,664 of 9,000; the constant 0.2372, and where
the bounds 1/2 and 1/4 are attained. The text as it read it is `theorem-twice.as-refereed.md`. It then looked at the
revised text (`referee-twice-report-2.md`): the four changes are in as it wrote them, the statement of Theorem T′ is
exactly what it proved and each step of §2 is right as worded; what it asked to have reworded (three clauses of this
paragraph, four in the credits, one in §2, two in the last paragraph of Corollary 3, a sentence on the least share, and
the labels of the steps of §2) is in its words.

**Whose is what.** Theorem T as stated in §1, its proof by induction (§3), Corollaries 1 to 3 and the tests of §5
are mine. The short proof of §2 and the sharper Theorem T′ are this text's referee's (found while it refereed the
proof by induction); I have checked that short proof by hand, line by line, and §2 says who else has read it.
What Corollary 3 takes from `../even-result-2.md`, §1, with the credits as that text gives them after its referee's
report: the combination "descend modulo 3, then count without contraction, so that no level divisible by 3 is
counted" (Lemmas M, S3, L3 as arranged there; Proposition H) is the second instance's, and so are the numbers p_r as
used. Lemma M itself is Lemma A of `sign-lemma-result.md` for q = 3; Lemma S3 is the slice criterion, Lemma L3 (a)
the step-down S1, Lemma L3 (b) Lemma L of `sign-four-result.md` with its count (4) (which, by that text's credits, Lemma L takes from Lemma T of
`sign-all-result.md`), each read modulo 3; Lemma L3 (c)
is the arrangement of the first result's Proposition P (A1 of the plan of the Lean proof), and the number W(no 3) is
the first result's, with the tail bound of Lemma W of `sign-four-result.md`. Theorem G of the second text is
Corollary 3 for multisets with at most two residues modulo 2^k (so for every n ≡ 2 mod 4), with the bounds 1/2,
1/4 and 0.074, by the same count (0.075 here only through the sharper bound for W(no 3)); its twist ε ↦ ε·τ (road 2 of §6 of the first result, repeated in lead 3 of `../brief-even-2.md`) is
one level of Theorem T. Corollary N of the first result is Theorem T at first order: all levels 2^j·e together cost
at most twice the bound 2^(−D_e) for one level. (These credits are the referee's sentences; of the files they name I
have myself opened `sign-lemma-result.md`, where Lemma A stands as said, and the first result, where Corollary N and
the number W(no 3) stand as said.) Conjecture E and the leads on the 2-tree are mine (`../brief-even.md`). Lemma ρ of
`lemma-rho.md` (mine, an hour older) is Corollary 1 here, and its proof was the model for the proof by induction.
The referee of the second text, in its report (`../referee-even-2-report.md`, suggestion 8, "A direction, not
proved"), names the two statements from which E3, and so the conjecture, would follow: Lemma ρ for every m, and, for every
live e′, a bound c·2^(−μ(e′*)) with c < 2.80 for the signings 3-bad at 2^j·e′ for some j; that report reached me after
this text had been sealed and sent to its own referee. Theorem T with Lemma L3 (b) gives c = 2.

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
the other at the level where they part. In my random trials it held in 3,664 of 9,000 families.)

> **Theorem T′ (the referee's).** Let V be any abelian group, and let the values be any elements of V, 0 allowed.
> For 0 ≤ d ≤ k let F_d be the event that every class at depth d has σ = 0 (so F_0 is "level 0 is bad"). Then the
> probability that level j is bad is P(F_(j−1)), for every 1 ≤ j ≤ k, and Q(B) ≤ 2·z(B) − P(F_k).

## 2. Proof of Theorem T′, and so of Theorem T (the referee's proof)

*How far it has been read.* The referee that found it checked its three facts as sets on 4,900 random families,
and steps (b) and (c) and the final inequality as counts on every family of its Theorem T runs, and asked that someone other than itself read it before it replaces
mine. I have read it line by line and written it out below in my words with every step; a further fresh instance
has read it as written here, every step of (a) to (d) and the remark after it (`reader-short-report.md`; the steps
were numbered (1) to (4) when it read them). By its report the proof stands as written, nothing about V or the
values is used, and Theorem T follows at once. With a program written from §1 it tested, by all signings, the
equality P(level j bad) = P(F_(j−1)), the bound Q ≤ 2z − P(F_k) and the statements (a), (b), (c) as sets:
exhaustively on 1,722,599 valued families (positions on Z_2, Z_4, Z_8, Z_16; values in Z/2, Z/3, Z/4, Z/6 and
{−2, …, 2} in Z, 0 allowed; every multiset up to 7 to 11 elements on Z_2, 5 to 8 on Z_4, 4 to 6 on Z_8, 3 or 4 on
Z_16) and on 180,000 random families of up to ten elements. No failure; deliberately false variants
(Q ≤ 2z − 2·P(F_k); "some class" for "every class"; P(F_j) for P(F_(j−1)); the factor 3/2) all failed
(`reader-short/`). The small words it asked for in (a) to (d) are in, and it has read the steps again as they stand
now (`reader-short-report-2.md`).

(a) F_0 ⊇ F_1 ⊇ … ⊇ F_k. A class at depth d − 1 (1 ≤ d ≤ k) is the disjoint union of its two halves, each of which is a
class at depth d or empty (σ = 0 if empty), and σ of the class is the sum of the two; so if every class at depth d
has σ = 0, every class at depth d − 1 has.

(b) P(level j is bad) = P(F_(j−1)) for 1 ≤ j ≤ k. Let τ_j be the map on signings that negates the sign of every
element whose position has remainder ≥ 2^(j−1) modulo 2^j. It is its own inverse, so it maps the set of signings
one-to-one onto itself and keeps the uniform probability. Of the two halves h, h′ of a class c at depth j − 1, τ_j
leaves the signs of one (positions with remainder < 2^(j−1)) and negates those of the other; so σ(c), computed for
τ_j(ε), is σ(h) − σ(h′), computed for ε, where h is the half whose signs are left (an empty half has σ = 0 for both
signings). Hence every class at depth j − 1 is balanced for ε iff every class at
depth j − 1 has σ = 0 for τ_j(ε): ε is bad at level j iff τ_j(ε) ∈ F_(j−1); as τ_j keeps the uniform probability, the two events
have the same probability.

(c) F_j ⊆ {level j is bad} ∩ {level 0 is bad}, for 1 ≤ j ≤ k. In F_j both halves of every class at depth j − 1 have
σ = 0, so the two sums are equal: level j is bad. And F_j ⊆ F_0 by (a).

(d) By (b) and (c), P(level j is bad and level 0 is not) = P(level j bad) − P(level j bad and level 0 bad)
≤ P(F_(j−1)) − P(F_j). Summing over j = 1, …, k, and adding the probability z(B) = P(F_0) that level 0 is bad (the event
"some level is bad" is the union of "level 0 is bad" and the k events "level j is bad and level 0 is not", and the
probability of a union is at most the sum):

  Q(B) ≤ z(B) + Σ_(j=1)^k (P(F_(j−1)) − P(F_j)) = z(B) + P(F_0) − P(F_k) = 2·z(B) − P(F_k). ∎

Nothing is asked of V or of the values, and the signs enter only through "τ_j keeps the uniform probability". For the
empty family every event is certain and the inequality reads 1 ≤ 1. When V has no element of order 2, F_d is the
event "levels 0, …, d are all bad" (if σ(c) = 0 and the halves of c have equal sums, each half has 2σ = 0, so σ = 0; the other inclusion is (a)
and (c)), and (b) says: as many signings are bad at level j as are bad at all of the levels 0, …, j − 1.

## 3. The proof by which I found it: induction on the number of elements (mine; needs both hypotheses of Theorem T)

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
*Consequence.* By (F1) for a* in B[A→s]:

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
not bad for B; and s = σ(κ) is never 0, for the same reason (this is needed: B[κ→0] = B∖κ would have no
single-element class, and its level r could be bad). As in (B1a), Q(B) = Σ_s P(s)·Q_(r−1)(B[κ→s]), and each
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

## 4. Three corollaries

**Corollary 1 (Lemma ρ of `lemma-rho.md`).** V = Z/3, every value 1: z(B) = p_m and Q(B) = 1 − ρ_2(B), so
ρ_2(B) ≥ 1 − 2·p_m = p_(m−1) for every nonempty multiset of m elements of Z_(2^k).

**Corollary 2 (characteristic 0).** Let n = 2^k·n′, n′ odd, B a multiset on Z_n, e | n′, η a root of unity of order
e. With V = Z[η] and the value η^b of the element b: by the slice criterion for the prime 2 (the powers
1, ω, …, ω^(2^(j−1)−1) of a root of unity ω of order 2^j are a basis of Z[ωη] over Z[η], and ω^(2^(j−1)) = −1; this is
S0 for p = 2 in Lean, `classSum_eq_of_badAt`, and its converse is the same computation), Φ_(2^j·e) divides the signed
mask iff level j is bad (for the inequality only the direction that is in Lean is needed: bad at 2^j·e implies that
level j is bad; level 0 is the definition). So **the share of signings bad at 2^j·e for some j ≤ k is at most twice
the share bad at e.** For n = 2^k (e = 1): the share of signings that are not good is at most 2·C(m, m/2)/2^m for even m (3/4 for
m = 4, attained by {0, 0, 0, 1} on Z_2; 5/8 for m = 6, attained by {0, 0, 0, 0, 0, 1}, by the referee's run), and 0
for odd m.

**Corollary 3 (Conjecture E).** Let n ≥ 1, 2^k the power of 2 in n, and B a nonempty multiset of m elements of
Z_n that is not {a, b} with 2^k ∤ a − b. Then B has a good signing. For m ≥ 3 the share of 3-good, hence of good, signings
is at least 1/2 (m = 3), 1/4 (m = 4), and more than p_(m−1) − 0.2372 ≥ 5/16 − 0.2372 > 0.075 (m ≥ 5) (p_r: the
probability that a sum of r independent signs is divisible by 3; `../even-result-2.md`, §1). (The bounds for
m = 3 and m = 4 are attained by good signings: {0, 1, 2} on Z_12 and {0, 0, 0, 1}, by the referee's runs;
{0, 0, 0, 1} has exactly 1/4 on every even Z_n (s + ε·ζ = 0, with s the sum of three signs, needs |s| = 1 and ζ = ±1;
the reader of §2 computed it on Z_2, Z_12, Z_20, Z_24, Z_28, Z_36, Z_40 and Z_60). In the runs of the reader of §2 no share of good signings below 1/4 was met for any m ≥ 4. The share
of 3-good signings, which is what the proof bounds, can be smaller than 1/4: the referee's runs and mine met nothing
below 1/4, but the reader of §2 met 7/32 for {0, 17, 61, 88, 100, 120, 139} on Z_140 (m = 7; the levels of 5 and of
7 are both live), and 15/64 (m = 8) and 29/128 (m = 9) on Z_140.)

*Proof, given Lemma M, Lemma S3 and Lemma L3 of `../even-result-2.md`.* Write n = 3^a·n_3, 3 ∤ n_3, n_3 = 2^k·n″
(so gcd(n″, 6) = 1). As there, a signing is *3-bad at d* (d | n_3) if S(ζ) ∈ 3·Z[ζ] for ζ of order d, and *3-good* if
it is 3-bad at no d | n_3; by Lemma M a 3-good signing is good on Z_n.

*m ≥ 3.* Let e″ | n″, x a root of unity of order e″, R = Z[x], V = R/3R. 2v = 0 in V gives v = 4v − 3v = 0. Give
the element b the position b mod 2^k and the value x^b mod 3R, which is not 0 (x^b is a unit of R and R ≠ 3R). By
Lemma S3 for p = 2 and d = 2^j·e″ (d″ = e″; the σ of the classes are the slices s_C read modulo 3R), a signing is 3-bad at
2^j·e″, j ≥ 1, iff level j is bad (only "3-bad implies bad level" is needed); and it is 3-bad at e″ iff σ(B) = 0 in V,
level 0. By Theorem T (or T′, which does not need the two remarks just made on V and the values):

  the share of signings 3-bad at 2^j·e″ for some j ≤ k is at most twice the share 3-bad at e″.   (2)

By Lemma L3 (c), used with c = 2^j for each j, a signing that is 3-bad at some 2^j·e″ is 3-bad at 2^j, or at 2^j·e′
for some e′ > 1 that is live for B. So a signing that is not 3-good is 3-bad at 2^j·e′ for some j and some e′ in
L = {1} ∪ {the live e′ > 1}, and by (2) their share is at most 2·Σ_(e′ ∈ L) (share 3-bad at e′). The share 3-bad at
1 is p_m. The shares 3-bad at the live e′ > 1 add up to at most W(no 3) < 0.118569: this is what the proof of
Lemma L3 (c) shows for c = 1 (by Lemma L3 (b) the share 3-bad at a live e′ is at most 2^(−μ(e′*)), the map e′ ↦ e′* is
injective on the live e′, and W(no 3) is the sum of 2^(−μ(e*)) over all e* > 1 with prime factors ≥ 5). And there is no live e′ > 1 unless B has at least five elements (a full group of a prime
q ≥ 5 has q occupied subclasses). So the share of signings that are not 3-good is at most
2·p_3 = 1/2 for m = 3, 2·p_4 = 3/4 for m = 4, and 2·p_m + 2·W(no 3) < 2·(11/32) + 0.2372 < 0.925 for m ≥ 5
(p_m ≤ 11/32 for m ≥ 5); in general it is less than 1 − p_(m−1) + 0.2372, since 2·p_m = 1 − p_(m−1)
and 2·W(no 3) < 0.2372.

*m = 1.* ±X^b has no root of unity as a zero. *m = 2, B = {a, b} with 2^k | a − b.* X^a + X^b vanishes at an n-th
root of unity ζ only if ζ^(a−b) = −1; but ζ^(a−b) is a power of ζ^(2^k), whose order divides n/2^k, an odd number. ∎

*What Corollary 3 does not use:* any theorem or lemma of the first result (`../even-result.md`), Theorem 4 for odd n (it proves it again:
k = 0), the rest of the second result (Theorems F, G, J, Lemma ρ as computed, its §5). It uses the reduction modulo 3
for every n, also when 3 ∤ n (a = 0), where Lemma M is the remark that 0 ∈ 3·Z[ζ]. Of `sign-four-result.md` it uses,
through Lemma L3, the tail bound of Lemma W as a cited result (the count (4) of Lemma L is proved again inside
Lemma L3 (b)), not Theorem 4. The referee recomputed
W(no 3) = 0.1185646982… with a tail bound proved in its own program (`referee-twice/wsum_ref.py`). Besides the three
lemmas it uses, from §1 of the second text, the ring fact at its head (Z[ζ] = R[Y]/(Φ_(p^i)(Y)) with its basis), the
definition of 3-bad and the paragraph on p_r; and the definition of live from the first result, §1, and those of the p-tree,
group and full from `sign-four-result.md`, §1, to which it refers.

## 5. Tests (programs of mine, beside this file; exact integer arithmetic, all signings)

- `twice_abstract.py`: Theorem T as stated, for random valued families of up to 9 elements with positions in Z_8
  and Z_32 and values in Z², (Z/3)², Z/9, Z/5 and Z: 9,000 families, no failure; the largest ratio Q/z is exactly
  2, in about four cases of ten (`twice-abstract.out`).
- `twice_test.py`: inequality (2) in the form used, "3-bad" computed from remainders modulo Φ_d with integer
  coefficients: every multiset containing 0 of up to 5 elements on Z_20 (`twice-exh-20.out`) and on Z_28
  (`twice-exh-28.out`), up to 4 on Z_40 (`twice-exh-40.out`); 1,500 random and structured multisets of 3 to 11
  elements on each of Z_40, Z_80, Z_56, Z_140, Z_280, Z_100 (`twice-rand-*.out`: random; few residues modulo the
  power of 2; pairs congruent modulo the odd part; a full set of residues modulo a prime; all congruent modulo
  the odd part). No failure; largest ratio exactly 2. The least share of 3-good signings seen: 1/2 for m = 3;
  1/4 for m = 4, 5, 6 and 7; 9/32 or more for m = 8 to 11 in the random families. That is not the least: the
  referee's exhaustive run on Z_20 has 1/4 at m = 8, and {0 (a times), 1, 2, 4, 13} on Z_20 has exactly 1/4 for every
  a = 1, …, 12. Nothing below 1/4 was found for m ≥ 4 in these runs. A later reader met 7/32 at m = 7 on Z_140.
- `rho_identities.py`, `rho_min.py` (Corollary 1; see `lemma-rho.md`).
- Before any of this: the confirming search of `../confirm.py` (6,002,729 multisets of 3 to 5 elements on eleven
  even groups and 20,000 structured ones up to Z_2000) found no multiset of three or more elements without a good
  signing.
