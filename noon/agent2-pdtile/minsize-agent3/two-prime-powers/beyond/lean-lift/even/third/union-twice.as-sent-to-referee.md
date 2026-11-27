# "Twice" for the whole of Z_n: a multiset has at most twice as many bad signings on Z_n as its reduction has modulo the odd part of n; and the shares for few elements (agent3 "Yonder", 27 November 2026)

**Status.** Written at about 20:30 UTC on 27 November, after the statement on signs for every n (`theorem-twice.md`)
had been refereed, posted and formalised. STATUS-HERE On paper only; no person has read it.

**What it adds.** Theorem T′ of `theorem-twice.md` bounds, for ONE system of values (one odd divisor e), the signings
that are bad somewhere on the ladder e, 2e, 4e, …, 2^k·e by twice those bad at e. Corollary 3 there then adds the
ladders up. The remark of this note is that the proof of Theorem T′ does not need the adding: its four steps hold
word for word for the events "bad at this level for SOME e", because the map τ_j that it uses does not depend on e.
The result is a statement about the whole of Z_n with no sum in it.

## 1. Statements

Notation of `theorem-twice.md`, §1: k ≥ 0; a finite family of elements y, each with a position u_y ∈ Z_(2^k); classes
at depth d, their halves, "level j is bad", the events F_d; signs independent and uniform.

> **Theorem U (several systems of values).** Let E be any set, and for each e ∈ E let V_e be an abelian group and
> let each element y have a value v_y^(e) ∈ V_e (0 allowed). The positions are the same for every e. For 0 ≤ j ≤ k
> let B_j be the event "level j is bad for the values of some e ∈ E", and for 0 ≤ d ≤ k let G_d be the event "for
> some e ∈ E, every class at depth d has σ = 0 in V_e" (the union over e of the events F_d of Theorem T′; G_0 = B_0).
> Then P(B_j) = P(G_(j−1)) for 1 ≤ j ≤ k, and
>
>   P(B_0 or B_1 or … or B_k) ≤ 2·P(B_0) − P(G_k).

For a single e this is Theorem T′. For the empty set E every event is empty and the inequality reads 0 ≤ 0.

> **Corollary U (the whole of Z_n).** Let n = 2^k·n′ with n′ odd, B a multiset of m ≥ 0 elements of Z_n, and B′
> its reduction modulo n′, a multiset of m elements of Z_(n′); a signing of B is a signing of B′, element by
> element. Call a signing bad on Z_n if its signed mask is divisible by Φ_d for some d | n, and bad on Z_(n′)
> likewise for B′ and the d | n′. Then
>
>   #{signings of B bad on Z_n} ≤ 2·#{signings of B′ bad on Z_(n′)} − #G,
>
> where G is the set of signings for which, for some e | n′, the signed mask of each class of B modulo 2^k
> vanishes at the roots of unity of order e. In particular **the share of bad signings of B on Z_n is at most
> twice the share of bad signings of B′ on Z_(n′).**

## 2. Proofs

*Proof of Theorem U.* For each e ∈ E write F_d^(e) for the event F_d of Theorem T′ for the values of e, and "level
j is bad for e" likewise. Steps (a), (b), (c) of `theorem-twice.md`, §2, hold for each e separately; they use
nothing of V or of the values. The map τ_j of step (b) negates the sign of every element whose position has
remainder ≥ 2^(j−1) modulo 2^j: it is defined by the positions alone, so it is the same map for every e.

(a′) G_0 ⊇ G_1 ⊇ … ⊇ G_k: by (a), F_d^(e) ⊆ F_(d−1)^(e) for each e; take the union over e.

(b′) A signing ε lies in B_j iff τ_j(ε) lies in G_(j−1), for 1 ≤ j ≤ k: by (b), for each e, ε is bad at level j for
e iff τ_j(ε) ∈ F_(j−1)^(e); so ε is bad at level j for some e iff τ_j(ε) ∈ F_(j−1)^(e) for some e. As τ_j is a
bijection of the set of signings, P(B_j) = P(G_(j−1)).

(c′) G_j ⊆ B_j ∩ B_0 for 1 ≤ j ≤ k: by (c), F_j^(e) ⊆ {level j is bad for e} ∩ {level 0 is bad for e} ⊆ B_j ∩ B_0
for each e.

(d′) By (b′) and (c′), P(B_j and not B_0) = P(B_j) − P(B_j and B_0) ≤ P(G_(j−1)) − P(G_j). The event "B_0 or … or
B_k" is the union of B_0 and the k events "B_j and not B_0"; so its probability is at most
P(B_0) + Σ_(j=1)^k (P(G_(j−1)) − P(G_j)) = P(B_0) + P(G_0) − P(G_k) = 2·P(B_0) − P(G_k). ∎

*Proof of Corollary U.* Let E be the set of divisors of n′. For e ∈ E fix a root of unity η_e of order e, let
V_e = Z[η_e], and give the element b of B the position b mod 2^k and the value η_e^b; η_e^b depends only on b mod e,
so only on b mod n′. Every divisor d of n is 2^j·e for exactly one pair 0 ≤ j ≤ k, e | n′.

- Level 0: the signed mask S of B has S(η_e) = Σ ± η_e^b = σ(B) in V_e, and Φ_e divides S iff S(η_e) = 0. The
  signed mask S′ of B′ has S′(η_e) = S(η_e). So B_0 is the event "S′ is divisible by Φ_e for some e | n′": the
  signing is bad on Z_(n′).
- Level j ≥ 1: if Φ_(2^j·e) divides S, then level j is bad for e. This is the slice criterion for the prime 2, as in
  Corollary 2 of `theorem-twice.md` (S0 for p = 2 in the Lean library, `classSum_eq_of_badAt`). So a signing bad
  on Z_n lies in B_0 or … or B_k. (The converse holds too, by the same computation, but is not needed.)
- G_k: every class at depth k is the set of the elements of B in one residue class modulo 2^k, and σ of it in V_e
  is the value at η_e of the signed mask of that class.

Theorem U gives P(bad on Z_n) ≤ P(B_0 or … or B_k) ≤ 2·P(B_0) − P(G_k) = 2·P(bad on Z_(n′)) − P(G). Multiply by
2^m. ∎

## 3. What follows, and what does not

1. **No bad signing on the odd part, none at all.** If every signing of B′ is good on Z_(n′), every signing of B is
   good on Z_n.
2. **The exceptional pairs are the case of equality with everything bad.** For two elements a, b the reduction B′
   has exactly the two signings with different signs bad (X^a − X^b vanishes at 1; X^a + X^b vanishes at no root of
   unity of odd order, since −1 is not a power of one). So Corollary U allows all four signings of {a, b} to be
   bad on Z_n, and for an exceptional pair they are.
3. **The least share of good signings is a question about odd n.** Let β(m) be the supremum, over all odd n′ and
   all multisets of m elements of Z_(n′), of the share of bad signings. Then on every Z_n a multiset of m elements
   has a share of good signings of at least 1 − 2·β(m). What is proved about β(m): Proposition H of
   `../even-result-2.md` (on odd n the share of signings that are not 3-good, hence of bad signings, is at most
   p_m + [m ≥ 5]·W(no 3)) gives β(3) ≤ 1/4 and β(4) ≤ 3/8, both attained ({0, 1, 2} on Z_3; any four elements,
   since the signings whose signs add up to 0 are 3/8 of all), and with the sum cut off as in 5 below
   β(5) ≤ 3/8 and β(m) < 0.452 for every m ≥ 5. What is seen in the cases tried (§4) is nothing above 11/32 for
   m = 5 to 8. If β(m) ≤ 3/8 held for every m ≥ 3, every multiset of three or more elements on every Z_n would
   have a share of good signings of at least 1/4. **That is not proved for m ≥ 6.**
4. **The same modulo 3.** With V_e = Z[η_e]/3 for the divisors e of n′ that are prime to 3, Theorem U says: the
   share of signings of B that are 3-bad at some d | n with 3 ∤ d is at most twice the share that are 3-bad at some
   odd such d. Corollary 3 of `theorem-twice.md` bounds the latter by the sum p_m + W(no 3); so the numbers of
   Corollary 3 are the same by this road.
5. **The shares of Corollary 3, with the sum cut off at the number of elements.** This is independent of Theorem U.
   In Lemma L3 (c) of `../even-result-2.md` a live e′ is sent to e′* = ∏ q^(l_q), l_q the number of live levels
   of q up to v_q(e′), and the share 3-bad at c·e′ is at most 2^(−μ(e′*)), μ(e*) = max_q v_q(e*)·(q − 1). For a
   multiset of m elements μ(e′*) ≤ m − 1: by the count in the proof of Lemma L3 (b), l live levels of a prime q
   need at least 1 + l·(q − 1) occupied classes, and there are at most m. So in Lemma L3 (c), and with it in
   Corollary 3 of `theorem-twice.md`, W(no 3) can be replaced by

     W_m := Σ of 2^(−μ(e*)) over the e* > 1 with all prime factors ≥ 5 and μ(e*) ≤ m − 1   (W_5 = W_6 = 1/16),

   and the share of 3-good, hence of good, signings of a multiset of m ≥ 5 elements on any Z_n that Corollary 3
   gives becomes 1 − 2·p_m − 2·W_m: **at least 1/4 for m = 5**, 3/16 for m = 6, 5/32, 9/64, 17/128, 33/256, 61/512,
   121/1024 for m = 7, …, 12, and more than 0.0961 for every m ≥ 5 (`../shares/refined.py`, `refined.out`: exact
   fractions for m ≤ 60; for m > 60 from p_m ≤ 1/3 + (2/3)/2^61 and W_m < 0.118569). Corollary 3 as written has
   "more than 0.075" for every m ≥ 5. The cut-off is that of `sign-four-result.md`, whose W_m is the same sum
   over all odd d > 1 with μ(d) ≤ m − 1; I have only carried it to the sum without the prime 3.

## 4. Tests (mine; exact integer arithmetic)

`../shares/union_twice.py` (it imports `../shares/minshare.py`): for a modulus n and a size m, every multiset of m
elements of Z_n that contains 0, every signing with the first sign +; a signing is bad if its signed mask has
remainder 0 modulo Φ_d for some d | n; the same for the reduction modulo the odd part. Checked: bad on Z_n ≤ twice
bad on the odd part. Outputs `../shares/union-2to5.out` (m = 2 to 5 on n = 2, 4, 6, 12, 20, 24, 30, 36),
`union-5-more.out` (m = 5 on 40, 42, 48, 60), `union-6.out` (m = 6 on 2, 4, 6, 8, 10, 12, 18, 20, 24, 30),
`union-7.out` (m = 7 on 6, 10, 12, 18, 20, 24), `union-8.out` (m = 8 on 6, 10, 12): 55 lines, 2,556,760 multisets in all, no failure;
the ratio 2 is attained in each of the 50 lines in which some multiset has a bad signing on the odd part (in the
other five, with m odd and n = 2, 4 or 20, none has); no multiset has a bad signing on Z_n and none on its odd part. The term #G was not tested.

`../shares/minshare.py`: the least share of good signings by exhaustion, same conventions. On odd n (outputs
`../shares/odd-3to6.out`, `odd-7.out`, `odd-8.out`; n = 3, 5, 9, 15, 21, 27, 45 for m = 3 to 6; 3, 9, 15, 21, 27 for
m = 7; 3, 9, 15 for m = 8) the largest share of bad signings seen is 1/4, 3/8, 1/4, 11/32, 13/64, 39/128 for
m = 3, …, 8 (m = 4: every multiset has exactly 3/8, the signings whose signs add up to 0). On even n (outputs
`m5.out` to `m8.out`, `m5-more.out`, `m6-more.out`, `m7-more.out`) the least share of good signings seen is 1/2,
1/4, 1/2, 5/16, 19/32, 25/64 for m = 3, …, 8, which is 1 − 2·(the largest bad share seen on odd n) in each case.
These are searches on small moduli and prove nothing about β(m).

## 5. Whose it is

The four steps are the referee's proof of Theorem T′ (`theorem-twice.md`, §2), used unchanged; Theorem T is mine.
The cut-off of §3, 5 is the fourth instance's (`sign-four-result.md`), carried over by me; Lemma L3 and Proposition H
are the second afternoon instance's (`../even-result-2.md`), with the credits for their parts given in
`theorem-twice.md`.
What is added here, that the steps hold for the events "for some e" because τ_j does not depend on e, is mine.
For multisets with at most two residues modulo 2^k (so for every n ≡ 2 mod 4) the statement of Corollary U without
the term #G is in the proof of Theorem G of the second of the afternoon's results (`../even-result-2.md`, §3):
there a signing is good for B iff it and its twist ε·τ are both good for the reduction on Z_(n′). I have not
searched in print for Corollary U; the two searches made for Theorem T and for the statement on signs
(`../scout-even-report.md`, `../scout-twice-report.md`) did not look for it.
