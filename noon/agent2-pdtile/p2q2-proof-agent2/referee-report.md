*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# Referee report on `p2q2-agent2.md` (weak tiles of Z_{p²q²} are tiles)

*20 November 2026. Adversarial reading plus independent computation. My scripts are in `/tmp/referee-p2q2/`
and nothing else was written anywhere except this file — with one slip: importing `check_p2q2.py` for the
attack of 4.7 left a `__pycache__` directory in this folder from 13:11 to 14:08 UTC, when I removed it. I
took (P1)–(P4) as given, as instructed, and checked only that the note uses them for what they say.*

*Version read: §§1–5 below are about the note as it stood at 12:36 UTC (14,896 bytes, "Status: claimed, not
established") and `check_p2q2.py` of the same time (SHA-256 ade2e975…), with `certificates_p2q2.json`
(SHA-256 adbbbba4…, unchanged since). A first draft of this report was in the folder from about 13:27; the
note and the checker were revised at 13:33–13:38 in response to it. §6 is about that revision. The numbers
in this final version supersede those of the draft (the note's §6 quotes the draft: "about 1.6 million"
linear programmes is now about 3 million, and "1,159 prime pairs" was a miscount of mine: 1,112 distinct
pairs).*

## 1. Verdict

I found no error: Lemmas 1–3, Proposition 4, Lemma 5, the five-category argument of §5, the certificate
file and the checker survived every attack I made, by hand and by independent computation (own code; exact
arithmetic for the certificates; about 3 million linear programmes on actual sets). What I found are gaps
of citation and exposition, none of which changes a statement, and one looseness in `check_p2q2.py` that
the shipped certificate file does not exercise.

## 2. Errors that break the proof

None found.

For the record, the places where I expected a break and why there is none:

- **Lemma 2.** The subgroup sums σ/p, σ/q are right (the annihilator of pZ_M is the p frequencies of order
  dividing p); "f > 0 on one unit ⇒ on all units" needs the step complement of (P2), which is used; the
  three-line argument "a ∉ pZ, b ∉ qZ ⇒ a − b is a unit" needs 0 ∈ A, which is assumed. The reduction is
  right for both subgroups (Z_{M/p} = Z_{q²·p} and Z_{M/q} = Z_{p²·q} are both instances of Theorem A).
- **Lemma 3, Claim.** I re-derived it: equal sizes plus (T1) force S_c, S_c′ to differ exactly by q ↔ q²;
  the sum of g over q²Z_{M/p} is Σg/q²; n = q, Σg = pq; then ĝ vanishes at all five non-trivial orders
  p, q, q², pq, pq² of Z_{pq²}, so g ≡ 1 and Σg = pq². Each of the five is justified. The q-version is the
  same proof with the primes exchanged and nothing in it uses p < q. The assembly A ⊕ pB′ is right; it uses
  that B′ depends on S only (Proposition CM (2)).
- **Λ formula.** c_p(1,·) = (−p, p−1, 1) and c_p(2,·) = (0, −1, 1) are right (derived by hand, confirmed
  numerically, §4.1).
- **Proposition 4.** (1) and (2) are (P1) and its converse; (2) does not even need A to be a weak tile.
  (3) is weak duality; it divides by y₀, which is positive wherever it is used.
- **§5.** "k divides |A|" is Proposition CM (1) with k = ∏_{s∈S_A} p_s and is used correctly in b and H.
  "No orphan" is literally the hypothesis of Proposition CM (3). "p < q without loss of generality" is
  legitimate *because* the file certifies all 192 patterns in the asymmetric coordinates (not orbits under
  exchanging the primes), Lemma 3 is proved for both primes, and Lemma 5 is invoked only with p as the prime
  that is a zero (it is true in either orientation, §4.9). Every one of the 192 patterns has an entry in
  each regime (no missing, no duplicate, no extra entry). Regimes A and B are exhaustive: q ≠ p² for primes.
- **Category N.** gcd(p²(q−1)+q²(p−1), pq) = 1 and p²(q−1)+q²(p−1) ≥ p²+q² > pq−1. Right.
- **Sign test.** Regime B: (s,t) ↦ (2+s, p²+1+t) is onto {p ≥ 2, q ≥ p²+1}. Regime A:
  q = ((p+1)+(p²−1)z)/(1+z) runs over [p+1, p²−1) for z ∈ [0,∞); a prime q with p < q < p² satisfies
  p+1 ≤ q ≤ p²−1 and q = p²−1 only for (2,3), which is s = 0 (any z). So every prime pair is covered,
  including p = 2, (2,3) and (2,5). Multiplying by (1+z)^deg does not change a sign.
- **The checker checks what §3 says.** It requires y to have exactly the rows of LP(Z), loops over all nine
  classes for the reduced costs, tests γ*₂₂ = 1, γ* ≥ 0, Λ(γ*) = 0 on every row, σ(γ*) = y₀ and the support
  for RP/RQ/N, uses the strict test in category b, and fails on a missing entry. Category H has no primal
  point and needs none. The one soft spot is G4.

## 3. Gaps that do not break the proof

**G1. Lemma 5 and the Claim of Lemma 3 use facts that are not among (P1)–(P4).** §1 lists what is imported
from the paper; the following are used and are not in that list:

- (a) in Z_{p²q²}: Φ_{p²q²} | A ⇔ A is additive in every box (Lemma 5, first step, direction ⇒);
- (b) in Z_{p²q²}: Φ_{pq²} | A ⇔ for every t the p×q array (c,t′) ↦ #{a : u ≡ c (p), w = t+qt′} is additive
  (Lemma 5, last step, direction ⇐);
- (c) in Z_{pq²}: Φ_{pq²} | A ⇔ for every class t mod q the array (u,t′) is additive, and Φ_{pq} | A ⇔ the
  p×q array of counts is additive (Claim of Lemma 3, direction ⇒ twice).

(c) is the lemma on the level conditions (E_ℓ), (F_ℓ) in Part I of the paper (label `Y:lem:cyclo`), with
the primes exchanged; the paper states it without a written proof ("standard") and says it is formalised.
(b) follows from it applied to the image of A in Z_{pq²}, which is a multiset, while the lemma is stated
for sets. (a) is not in the paper at all: the paper only treats Z_{pⁿq}. All three are true
(kernel of evaluation at a primitive root of unity of order p^a q^b, by linear disjointness of the two
cyclotomic fields) and I tested them on 7,934 random instances without a disagreement (§4.11), but the note
must state them and prove or cite them; as written Lemma 5 rests on an unstated lemma.

**G2. (P4) is not what Theorem A says.** Theorem A, and the headline Lean theorem
`Pnq.weak_tiling_iff_tiling_pnq`, say "every weak tile of Z_{pⁿq} is a tile". Lemma 3 needs more: each piece
satisfies (T1) and (T2) relative to pq², and the digit set T_{𝒫∖S} is a complement. That is what the *proof*
of Theorem A shows (paper, "Proof of Theorem A"; in Lean the composition of `exists_stepTiling_tree`,
`step_structure`, `T2_of_tree` and the (T1) conversion inside `tiling_of_tree_T1_T2`, with
`Pqr.tiling_of_T1_T2_digitSet` for the complement), but no single named statement says it. Either cite the
proof, or add the one-line corollary. (Lemma 2 only needs the weak form.)

**G3. Lemma 3, one clause missing.** "Every A^c is a weak tile" needs A^c ≠ ∅; it follows from the identity
just derived (an empty sum is not 1) but is not said, and the equal size n is used right after.

**G4. `check_p2q2.py` accepts expressions that are undefined on the boundary of a regime.** `sign()` returns
`'+0'` when a *denominator* factor is only weakly signed, and `nonneg()` accepts `'+0'`. I ran it:
`sign(1/(p-2),'A') = '+0'`, `sign(1/(p-2),'B') = '+0'`, `sign(1/(q-p-1),'A') = '+0'`,
`sign(1/(q-p**2-1),'B') = '+0'`, all accepted as non-negative, although they are undefined at p = 2, at
(2,3), at (2,5), which are prime pairs of the regime. So the test "r_c ≥ 0" or "γ*_c ≥ 0" passes for an
expression with a pole exactly at p = 2. I could not build a complete wrong certificate that gets through
(since Σ_c r_c = M − y₀, a pole in a reduced cost drives y₀ to −∞ near the boundary, which the tests on y₀
then reject), but the soundness of the checker should not rest on such an argument. The shipped file does
not exercise the hole: every denominator that occurs in it (raw or after reduction) is a product of p, p±1,
q, q±1, pq−1 and p²−2pq+q, and each of these is strictly signed on both regimes (§4.6); and all entries
evaluate without a division by zero at (2,3), (2,5) and 1,110 other prime pairs. Fix: require a strict
sign for every denominator factor.

**G5. The note's description of the sign test is weaker than the code.** "accepting a polynomial factor as
positive when … all its coefficients are positive" is not enough for the strict inequality of category b
(s·t has positive coefficients and vanishes at p = 2). The code does the right thing (it also requires a
non-zero constant term for a strict sign, and category b demands strict); the sentence in §3 should say so.

**G6. Smaller points about the checker.** (i) It feeds strings from the JSON to `sympy.sympify`, which
evaluates them: the file has to be trusted (I parsed it with a whitelist parser instead). (ii) An unknown
key in `gamma` (e.g. `"7,7"`) is silently ignored — harmless, tested. (iii) The lookup is sensitive to the
order of the pairs in `F` — conservative (a reordered entry is reported as a failure).

**G7. Proposition 4 (3)** should say y₀ > 0 before "so |A| ≤ M/y₀" (true in every use: y₀ > M/k, y₀ = pq,
y₀ = σ(γ*) ≥ 1).

**G8. Bookkeeping.** (i) Z_36 has 64 zero patterns of tiles, not 63: the note's count leaves out A = Z_36
itself (category a); so 54 + 10. (ii) `sands/consist36.py` reads the certificates from
`/home/agent2/p2q2/final/certificates_p2q2.json`, not from the shipped folder (today the two files have the
same SHA-256).

**G9. A remark, not a gap: the R branch cannot be tested on examples.** No tile in any of my samples (all
383,806 tiles of Z_36; 36,473 of Z_100; 46,003 of Z_225; 73,793 of Z_196) has a pattern of category RP or
RQ, so "γ* is a weak complement of the tile" was never exercised on a set. The R certificates are verified
only as statements about the linear programme (4.5, 4.6, 4.10), and Lemma 3 only on tiles with a-patterns
(4.8). This agrees with Remark 7.1 and with the proof, which never claims that such sets exist. Of the 50 R
patterns of regime A, at all 858 pairs tested: 5 have M/y₀ not a multiple of k (no weak tile, by
divisibility alone); 32 have M/y₀ a proper multiple of k, and 11 have M/y₀ = k but violate (T2) (a weak tile
with such a pattern would, by Lemma 3, be a tile violating the necessary conditions of Coven and
Meyerowitz); only two are excluded by nothing: E_p = {1}, E_q = {2}, F = {(1,2),(2,1)} and the same with
(1,1) added (y₀ = pq; γ* = 1 at 0 and on class (1,2), 1/q on classes (1,0) and (2,0)). Regime B: 52 =
2 + 36 + 12 + 2, the same two patterns. For these two the proof rests on Lemma 3 alone, and Proposition 4 (2)
says that *every* set of size pq with exactly that zero set is a weak tile; at M = 36 there is no set of any
size up to 9 with either zero set (`t14_special.py`). (A sketch of mine, outside the brief: these two are
empty as well. With γ* as complement, Lemma 1 puts each of the p pieces inside one class mod q with q
distinct residues mod q², so the p×q arrays that decide Φ_{p²q} have a single non-zero column and cannot be
additive. `t15_sketch.py` confirms it on every set of that shape for (p,q) = (2,3), (2,5), (3,2) — 576,
25,600 and 5,832 sets — and on 60,000 random ones each for (3,5) and (2,7): p²q is a zero of none. If so,
and granting Lemma 3 and the necessity of (T1), (T2) for tiles, no R pattern is the pattern of a weak tile,
and Lemma 3 is only ever applied to an empty family. That does not weaken the proof; it explains why this
branch cannot be probed with examples.)

## 4. What I checked by computation

All code is mine (`/tmp/referee-p2q2/`); the note's scripts were not used, except that `check()` and
`sign()` of `check_p2q2.py` were imported for the attack in 4.7. Linear programmes: scipy/HiGHS; every
"feasible" answer was re-verified by substituting the solution.

**4.1 Λ formula** (`t1_lambda.py`). (p,q) = (2,3), (3,2), (3,5), (2,5), (5,3), (3,7), (5,7); 20 random real
step functions each; the DFT at *every* frequency of Z_M against Σγ_ij c_p(ℓ,i)c_q(m,j): largest
discrepancy 8.9·10⁻¹¹. Class sizes agree with row (0,0).

**4.2 Tiles against the categories** (`t2_tiles36.py`, `t2_tilesM.py`). Zero sets by FFT with a gap check,
confirmed by exact polynomial division on one representative per pattern.
- M = 36, regime A: *all* tiles containing 0, found by exact cover without digit sets: 383,806 (sizes
  1/2/3/4/6/9/12/18/36: 1, 27, 160, 729, 8,850, 65,536, 177,174, 131,328, 1). 64 patterns: 54 in category a,
  10 Lemma-2 patterns (32 tiles, every one inside 2Z or 3Z). None in b, H, N, RP, RQ.
- M = 100, regime B: 36,473 tiles (75 of size 2 and 15,625 of size 4 by brute force; random complements of
  digit sets and of earlier tiles for the other sizes); 57 patterns: 47 a, 10 Lemma 2. (An earlier run that
  included 160,256 tiles of size 5 found by brute force: 49 patterns, same conclusion.)
- M = 225, regime A with p = 3: 46,003 tiles; 40 patterns: 30 a, 10 Lemma 2.
- M = 196, regime B: 73,793 tiles; 52 patterns: 42 a, 10 Lemma 2.
- No inconsistency anywhere; every Lemma-2 tile lies in pZ or qZ; |A| = k for every tile with one of the
  192 patterns. See G9 for what this test cannot see.

**4.3 Lemma 2 at M = 36** (`t3_lemma2.py`, `t3b_lemma2_sample.py`, `t10_theoremC36.py`). Full LP in 36
unknowns.
- Exhaustive, 2 ≤ |A| ≤ 8, 0 ∈ A: 8,731,847 sets; 6,505,268 with neither 2 nor 3 a zero; the 430,555 of
  those that have some zero got an LP (a set with no zero at all is not a weak tile). Weak tiles found: 31
  (9 of size 2, 16 of size 3, 6 of size 6), all inside 2Z or 3Z. **Outside 2Z and 3Z: 0.**
- Sizes 9–24: 6,450 sets satisfying the hypotheses, outside 2Z and 3Z, with at least one zero (2,400 uniform
  by rejection, 2,400 unions of cyclotomic blocks, 1,650 direct sums; 1,806 of them with two to five zeros):
  0 weak tiles.
- Bonus, the theorem itself at M = 36: *all* sets of size 2–12 containing 0 (703.7 million), one LP per
  orbit under x ↦ u(x−a) for the sets that have a zero (1,470,081 LPs): 2,269 orbits of weak tiles, of sizes
  2, 3, 4, 6, 9, 12 only (6, 11, 29, 159, 673, 1,391), every one tiles (exact cover); those with neither 2
  nor 3 a zero all lie in 2Z or 3Z. These six numbers are exactly the numbers of orbits of *tiles* of these
  sizes in the complete list of 4.2 (`t16_orbits.py`): up to size 12, weak tiles and tiles of Z_36 are the
  same sets.

**4.4 Lemma 3, the Claim** (`t4_lemma3.py`, `t4b_lemma3_50.py`). Pairs of tiles of Z_{pq²} of equal size
with different sets of prime-power zeros; LP "common weak complement" (both convolution constraints).
- Z_18 (p=2,q=3), all tiles: size 3, {3} vs {9}: 36 × 4 = 144 pairs; size 6, {2,3} vs {2,9}: 243 × 3 = 729.
- Z_12 (p=3,q=2), all tiles: size 2: 6 × 3 = 18; size 6: 32 × 4 = 128.
- Z_20 (p=5,q=2), all tiles: size 2: 10 × 5 = 50; size 10: 512 × 16 = 8,192.
- Z_50 (p=2,q=5): size 5, all tiles (brute force over the sets with (T1)): 10,000 × 16 = 160,000 pairs;
  size 10: all 5 tiles with zeros {2,25}
  against 20,043 (first in search order) and 20,000 (uniform random) of the 1,953,125 with zeros {2,5}:
  200,215 pairs.
- **Pairs with a common weak complement: 0 of 369,476.** Control: 1,036 random pairs with *equal* zero sets,
  all 1,036 have one.

**4.5 Certificates at prime pairs** (`t5_cert_eval.py`, `t5b_cert_eval_extreme.py`; own whitelist parser,
`fractions.Fraction`, no sympy). For each of the 246 non-a entries: y has exactly the right rows; nine
reduced costs ≥ 0; b: y₀ > M/k; H: y₀ = M/k and the side conditions; RP/RQ/N: γ*₂₂ = 1, γ* ≥ 0, Λ(γ*) = 0 on
every row, σ(γ*) = y₀, support; N: value and non-integrality of M/y₀. For the 138 a-entries: (T2) and no
orphan.
- All 1,035 pairs p < q ≤ 200 (858 in regime A, 177 in B; includes (2,3), (2,5), (3,7), (3,11), (5,7),
  (5,29), (7,47), (7,53)): 127,305 checks, 0 failures, no division by zero.
- 124 extreme pairs (q the next primes after p, the last primes before p², the first after p², and q up to
  10¹⁶, for p up to 10,007): 15,252 checks, 0 failures.
- Smallest margin in category b: y₀/(M/k) = 1.0000000599 at (10007, 100140043) for E_p = {1,2}, E_q = {1},
  F = {(1,2),(2,2)} — the pattern that changes category at q = p², as it should.

**4.6 Certificates symbolically** (`t6_symbolic.py`, `t6b_denoms.py`). Own verifier: arithmetic in the
fraction field Q(p,q) (`sympy.polys.fields`, no `simplify`), own implementation of the two substitutions,
and *strict* non-vanishing demanded of every denominator, raw and reduced. All 384 entries pass in their
regime (A: 69 a, 70 b, 22 RP, 28 RQ, 2 H, 1 N; B: 69 a, 69 b, 22 RP, 30 RQ, 2 H); no factor undecided; no
weakly signed factor occurs anywhere in the file.

**4.7 Attack on `check_p2q2.py`** (`t7_mutations.py`). 27 malformed certificates, all rejected: a regime-A
certificate used in regime B and conversely (both patterns whose category changes), RQ relabelled RP and
conversely, b or RQ relabelled a, RP/RQ/H/N relabelled b, b relabelled H, a y-row removed, an extra y-row,
a y-row for an order inside Z, y₀ + 1 in b/RQ/H, y₀ inflated by 1 + (pq)⁻³ in b, a negated γ*, γ*₂₂ = 2,
γ* missing in RQ and N, unknown categories, y = (M, 0, …, 0). The only things that got through are in G4
and G6.

**4.8 Lemma 3 as a construction** (`t8_lemma3_assembly.py`). For every tile A of Z_36 and r ∈ {2, 3}: LP
for a weak complement supported in rZ. It exists for 316,866 tiles (r = 2) and 382,904 tiles (r = 3). In
every one of these 699,770 cases the pieces have the same prime-power zeros, each piece tiles Z_{36/r} with
the digit set B′, and A ⊕ rB′ = Z_36 (checked by counting).

**4.9 Lemma 5** (`t9_lemma5.py`). M = 36, all 324,632 six-element sets containing 0: with (p,q) = (2,3) the
hypotheses hold for 6 sets, with (p,q) = (3,2) for 36 sets; the conclusion holds for all 42. The hypothesis
|A| = pq is needed: for |A| = 4, 8 (p = 2) and 9 (p = 3) the conclusion fails for 8 of 9, 280 of 288 and 15
of 16 sets with the two zeros. M = 100 (`t9b_lemma5_100.py`), all 2,118,940 ten-element sets that are
additive in every box (that is, by fact (a) of G1, all with 100 a zero): with (p,q) = (2,5), 2 is a zero of
100 of them and 50 is a zero of all 100; with (p,q) = (5,2), 5 is a zero of 100,000 of them and 20 is a
zero of all 100,000.

**4.10 Value of the programme** (`t12_side.py`). LP(Z) solved numerically for all 123 non-a patterns at
(2,3), (3,5), (3,7), (5,7), (5,23), (7,47), (2,5), (2,7), (3,11), (5,29), (7,53), (2,199) (1,476 LPs): the
optimum equals y₀ to relative 10⁻¹⁵ in categories RP, RQ, H, N and is ≥ y₀ in category b.

**4.11 The unstated cyclotomic facts of G1** (`t11_cyclo.py`). (p,q) = (2,3), (3,2), (2,5), (3,5), (5,3):
7,934 random instances of the four equivalences, 0 disagreements (the zero is present in 497, 63, 679 and
38 of them).

**4.12 Proposition 4 on actual sets** (`t13_prop4.py`). M = 36, every orbit representative of size 2–7 that
has a zero (3,973 sets): "A is a weak tile" (LP in 36 unknowns) against "|A|·σ_min(Z(A)) = 36" (LP(Z) in 9
unknowns). The two agree on all 3,973 (205 weak tiles), and |A|·σ_min ≥ 36 for every set, as (2) says.

**4.13 The example after Lemma 2.** A = {0,1}×{0,1,5} = {0,1,5,9,28,32} ⊂ Z_36 lies in no proper subgroup;
the largest mass a weak complement can put on odd numbers is 4, on non-multiples of 3 it is 3, on units 0.
As the note says.

## 5. What I did not check

- (P1)–(P4) themselves and the Lean development (taken as given; I only read the statements, `CheckPnq.lean`,
  `Pnq/Main.lean` and the definitions in `Pqr/CM.lean` for G2).
- That the result is new.
- The exhaustive searches of `weak-agent2.md` at M = 100, 196, 225 quoted in §6. My own direct search of
  the theorem covers M = 36 and |A| ≤ 12 only (sizes 13–35, in particular a hypothetical weak tile of size
  18, are not covered).
- The scripts in `sands/` (the proof does not depend on them) and the two shipped output files; I did not
  re-run `check_p2q2.py` or `spotcheck_p2q2.py` end to end.
- Remarks 7.2 (periodicity) and 7.3 (folding) — 8.2 and 8.3 in the revision — and the sentence "works
  verbatim in Z_{p^a q^b}".
- Lemma 2 by brute force beyond M = 36; Lemma 5 by brute force beyond M = 36; Lemma 3's Claim beyond
  Z_12, Z_18, Z_20, Z_50.
- Positivity of the certificate polynomials by any method other than the two substitutions (mine is a
  separate implementation of the same idea) and exact evaluation at 1,112 prime pairs.
- Exactness of the "no weak complement" answers on sets: they are infeasibility verdicts of a floating-point
  solver (HiGHS), not exact Farkas certificates. Controls: every "feasible" answer was verified by
  substitution; the search of 4.3 found exactly as many orbits of weak tiles as there are orbits of tiles
  (so no tile was wrongly declared infeasible); all 1,036 control pairs of 4.4 were found feasible.

## 6. Addendum: the revision of 13:33–13:38 UTC

The note (now 20,405 bytes, SHA-256 7519a50a…) and `check_p2q2.py` (SHA-256 aba9ed9c…) changed while I was
computing. I re-read what changed; I found no error in it either.

- **Lemma 3, Claim: a new proof, steps (i)–(iv).** This replaces the argument I refereed in §2. It is
  correct: (i) equal size and (T1) give p ∈ S₁ ⇔ p ∈ S₂; (ii) no orphan zero for a weak tile of Z_{pq²} is
  what the paper's proof of Theorem A gives (F ⊆ E when the single prime is not a zero; nothing to prove
  when it is); (iii) a common zero d of two pieces is then exactly divisible by an element of S₁ ∩ S₂ (two
  different powers of q cannot both divide d exactly), so it is a zero of T = T_{S₁∩S₂}; (iv) 1_T ∗ g is the
  constant |T|/n ≥ g(0) = 1, so ∏_{S₁∩S₂} p_s ≥ ∏_{S₁} p_s and S₁ ⊆ S₂. The q-version is the same with "the
  only power of q dividing p²q is q". The statement of the Claim is unchanged, so 4.4 and 4.8 still test it.
  Step (ii) tested on every tile of Z_12 (88), Z_18 (551), Z_20 (924) and on 50,030 tiles of Z_50: no
  orphan zero (`t17_revision.py`).
- **(P5)** (answers G1). The identity pq·N_d + N_{d/pq} = q·N_{d/p} + p·N_{d/q} is the statement
  (1 − P_p)(1 − P_q)N_d = 0 for the two averaging projections, which is the kernel condition; for d = M it is
  additivity in every box. Checked by hand, and on 9,600 instances (635 with the zero present) for
  (p,q) = (2,3), (3,2), (2,5), (3,5) and all four orders p^a q^b: no disagreement.
- **Lemma 5, new last step.** A is a union of cosets of {0} × qZ_{q²}, and a character of order pq² is not
  trivial on that subgroup; so the transform vanishes there. Correct, and it no longer needs fact (b) of G1.
- **(P4)** now says what is used and names the Lean statements (G2); "no A^c is empty" (G3), y₀ > 0 (G7)
  and the description of the sign test (G5) are in the text.
- **`check_p2q2.py`** (G4): `sign()` now returns `'?'` when a denominator factor is only weakly signed. I
  re-ran my attack (`t7_mutations.py`) on the new file: the five pole expressions are now rejected, the 11
  unmodified entries still pass, the 27 malformed ones are still rejected.
- **Left over in the note.** Remark 8.1 still says "the 63 patterns of tiles" (§6 of the note now says 64).
  §6 of the note quotes two numbers of my draft that have changed (see the top of this report).
- **Not checked:** the new headline claim that Lean accepted `P2q2.weak_tiling_iff_tiling_p2q2`. I did not
  build it. All I did: the statement in `../lean-tiling/P2q2/Main.lean` is the one quoted in the note, and
  a text search of `P2q2/*.lean` (11,134 lines) finds no `sorry`, `admit`, `native_decide` or `axiom`.
  Nor did I check that the generated `Certs*.lean` files come from the JSON file I verified.
