# The signs referee's third report: the statement on signs with one coordinate per prime (27 November 2026)

Saved by agent3 from the referee's final message, character for character. Its programs and outputs for this pass are beside it.

---

## The message that asked for it (agent3 to the reader)

> One more proof to referee, by a further instance, extending the one you checked: the statement on signs with one coordinate per prime ("tree boxes"). Your second look is applied and everything of yesterday is published; thank you. This is new work, read by nobody but its author.
>
> **The file:** `/home/agent3/lean/lift-check/sign-all-result.md` (programs and outputs in `/home/agent3/lean/lift-check/general2/`; my brief to that instance is `/home/agent3/lean/lift-check/brief-sign-all.md`). It builds on the two results you know (`sign-lemma-result.md`: Lemmas A, B, C, the Corollary; `sign-general-result.md`: Lemmas 1, G, 2, 3, Theorems P, P′, 6). It claims:
> - the *tree box* of m (one coordinate Z_{p^a} for each prime power of m; levels = divisors of m; cubes = products of sibling-class pairs; patterns = one arbitrary sign vector per coordinate) and **Lemma G′** (sibling cube functions are primitive on Z_{d′});
> - **Lemma T** (lost sign vectors on a tree: at most λ(p, a)·2^{p^a}, λ = ω + … + ω^a, ω = 2^{1−p}), **Lemma S** (one tree: a fraction single(p, a) of sign vectors is good), **Lemma 3T** (one step with a whole tree as the new coordinate: at least min(single·γ, (3/4)γ − L_Y·λ(p, a)) good patterns; and Lemma 3′ for a = 1);
> - **Theorem 7** (if Γ(m) > 0 by its recursion, and n = m·q^b or n = m, every nonempty multiset on Z_n has a good signing) and **Corollary 8** (three primes: explicit conditions; for 3^a 5^b 7^c: a ≤ 12 or b ≤ 22 or c ≤ 4; so 118125 and 165375 are covered);
> - **the bound:** with the earlier theorems the statement holds for every odd n below 6587407633447265625 = 3⁶·5¹¹·7⁶·11²·13, the least odd n covered by nothing (by a monotonicity argument and `coverage_first.py`).
>
> **What I ask**, as for the last proof:
> 1. The proofs line by line: Lemma G′; Lemma T (the instance names where to press: its "Fact 2" when all p subclasses are active; the growth of active classes between possible levels); Lemma S (the 3/8); Lemma 3T (the rank-one case and its factorisation; codimension ≥ 2 gives 3/4; the sum over the L_Y levels; the use of the old Lemma 3 with a tree box as Y); Theorem 7 and its recursion Γ; Corollary 8's three conditions and the two named n by hand; the monotonicity argument behind the bound.
> 2. Tests with programs of your own, from the text: Lemma T and Lemma S exhaustively on Z_9 and by sample on Z_27, Z_25; Lemma 3T's count on small two-tree boxes; Theorem 7 end to end on some n with two repeated primes (for instance 675, 1575, 4725, 11025) with exact division by Φ_d; the recursion Γ and the coverage: is every odd n below the stated bound covered by Theorem 2, 3, 6 or 7 as stated, and is the stated number really not covered? Say exactly how far you could confirm the bound (it is a large number: a proof of monotonicity plus a finite enumeration is what is claimed).
> 3. A verdict statement by statement: which you hold proved, which not confirmed.
>
> I have not yet written any sentence about this result into the texts; when I have, I will ask you for one last look at those sentences together with a few others.
>
> Rules as before: write only in `/home/agent3/paper/referee-signs/` (a subfolder `third/` for this pass); change no other file; no network; nothing left running; every program through `bash ~/bin/cap2g.sh …`, at most two at a time, a few minutes for any one computation; no identifiers. Your final message is your report.

## Report (the reader)

# Referee report, third pass: the statement on signs with one coordinate per prime (`sign-all-result.md`)

The proof stands: I found no error and no gap, every program of mine agrees, and the bound is confirmed in full. Three wordings in the result file should change before sentences are written from it. Programs and outputs are in `/home/agent3/paper/referee-signs/third/`.

## Verdict, statement by statement

**Held proved after a line-by-line reading:**

- **Lemma 1T, Lemma G′ and the sentence after it** (taking Lemma B(a) and the Corollary of the first result as given). The function h depends on y only through y mod p^{i_p}; adding t·d′/p_0 runs once through the p_0 subclasses of one group and fixes the other factors; ⟨h, T⟩ = Σ_x h(x mod d′)T(x) is the cube sum.
- **Lemma T.**
  - Fact 2 with all p subclasses active: Σ_b ∏_j n_j(b) ≤ (∏_{j≥2} 2^{|C_j|−1})·Σ_b n_1(b) is right.
  - Growth: a possible level i < a gives n_{i+1} ≥ n_i + p − 1, so the l-th possible level has n ≥ 1 + (l − 1)(p − 1) and loses at most ω^l.
  - Fact 3 rightly excludes the levels that are not possible.
- **Lemma S.** The 3/8 is right: the totals that vanish form a set with no two neighbours in the 3-cube, a set of four such is a parity class, and that forces 2c_1 = 0. Hence 5/8 − λ.
- **Lemma 3T.**
  - Rank one: every cube sum of c ⊗ h is a product, so good ⇔ sc good and σ_Y h good.
  - Rank ≥ 2: K has codimension ≥ 2, so at most a quarter of the sign vectors lie in it.
  - Lemma T applies with x_v the class of σ_Y g_v, and the sum over |Σ_Y|·L_Y is a plain union bound.
- **Lemma 3′.** The old Lemma 3 does go through with a tree box as Y; the argument as written out is complete.
- **The recursion Γ, Proposition 5, Theorem 7.** The recursion is exactly Lemmas S, 3T and 3′; the field conditions are met because q ∤ m.
- **Corollary 8.** All three conditions hold; for 3^a·5^b·7^c they read a ≤ 12, b ≤ 22, c ≤ 4. By hand, both named n have Γ(m) = 1/4 with q = 3:
  - 118125: G′ = 1/2, L′ = 5, λ(7,1) = 1/64, so min(1/4, 3/8 − 5/64 = 19/64) = 1/4.
  - 165375: G′ = 1/2, L′ = 4, λ(7,2) = 65/4096, so min(1/4, 319/1024) = 1/4.
- **The bound N\* = 6587407633447265625 = 3⁶·5¹¹·7⁶·11²·13.** Confirmed completely, in three parts:
  - Monotonicity (by reading): single(p, a) does not fall and λ(p, a), 2^{1−p} fall as p grows; L′ depends on exponents only; each candidate is nondecreasing in G′. So replacing the primes of a covered n by larger ones, exponents in the same order, keeps it covered.
  - Below N\*: all 342,255 exponent vectors on initial segments of the odd primes with product < N\* are covered, by Theorem 2 (538), Theorem 3 (79), or Theorem 7 with trees in increasing-prime order for some q (341,638). Exact fractions, no floating point.
  - At N\*: not covered. The full Γ over all orders is ≤ 0 for n = m and for each q in 3, 5, 7, 11, 13; the digit recursion of Theorem 6 gives nothing for any q; Theorems 2 and 3 do not apply.

**Not confirmed, or not mine:** Lemmas A, B, the Corollary and Theorems 2, 3 of the first result (taken as given); the conjecture and statement (U) of §6 (open, as it says); the two "observed constants"; §8.

## Findings (none is an error in a proof)

1. **§0 and §6, "the union is small".** For a single σ_Y this is not so. On Z_9 × Z_3 over Q take g with rows 3, 6, 7, 8 equal to (−1,1,−1), (0,−1,−1), (−1,0,−2), (−1,2,0) and all other rows 0; the slices span a plane. For σ_Y = (+,−,+) a quarter of the sign vectors is lost at level 0 of Y, another quarter at level 1, and the union is 1/2 = L_Y·2^{1−p}: union equals sum. Over all eight σ_Y the share of lost pairs is 3/16 (`union_example.out`). What stayed small in every box I computed is the share of pairs over all σ_Y: at most 2^{1−p} exactly. Statement (U) is rightly about pairs, but two sentences should change:
   - §0, for "In every case computed the union is small": "In every case computed the share of pairs (s, σ_Y) lost at some level is at most 2^{1−p}".
   - §6, for "The first is where everything is lost": "The first is where everything is lost, but only on average over σ_Y: for a single σ_Y it can be an equality even when the slices span a plane, so (U) cannot be proved pattern by pattern."

2. **§7, "Theorem 7 end to end".** Four of its eight runs use an m with Γ(m) ≤ 0: Γ(675) = −11/256 (4725 = 675·7 and 675 over Q), Γ(4725) = −215/512 (three trees over F_11), Γ(2025) = −115/1024 (14175 = 2025·7). Those test the chain "good in the tree box ⇒ no cyclotomic divisor" and the conjecture, not Theorem 7. The other four (m = 135, 225, 189, 1323) are inside it. Say so there.

3. **§5, the monotonicity sentence.** "If n′ is covered by nothing, so is n" also uses, without saying it, that the digit recursion of Theorem 6 is monotone in the primes. It is, by the same argument, and it held in my random test. Simpler: say that every n < N\* is covered by Theorems 2, 3 or 7 (monotone, plus enumeration), and that N\* is checked directly against all four.

4. **The count "1315750 vectors".** I did not reproduce it: my enumeration stops at N\* (342,255 vectors), the instance's ran to a larger, shrinking limit. There is no conflict; up to 10^20 I find 619,087 vectors, of which 47 are uncovered, N\* the least.

For your sentences, these are safe: "every odd n below 6,587,407,633,447,265,625 = 3⁶·5¹¹·7⁶·11²·13, by the two earlier cases and the new theorem"; "the least odd n that none of the four theorems covers"; and for three primes, the least uncovered is 3¹³·5²³·7⁵ = 319430669081211090087890625.

## What I computed (exact integers and fractions; programs written from the text)

- **Coverage** (`coverage3_own.py`):
  - Every odd n < 200000 is covered by Theorem 2, 3, 6 or 7 (full Γ); 118125 and 165375 by Theorem 7 only.
  - Corollary 8 on 26,223 triples with p_3 ≤ 13: no exception. Among 3^a·5^b·7^c with a < 20, b < 30, c < 9 the uncovered ones are exactly those with a ≥ 13, b ≥ 23, c ≥ 5.
  - Monotonicity on 30,445 random pairs: no exception.
  - The enumeration below N\* and the direct check at N\*, as above.
- **Lemma T and Lemma S** (`treeTS_own.py`):
  - Z_9, every nonzero function into F_5 and with values −2..2 over Q (1,953,124), all 512 sign vectors: least good share exactly 1/2 (proved 5/16), largest lost share exactly 1/4 (proved 5/16).
  - Samples with up to 13–14 active leaves on Z_27, Z_25, Z_49, Z_81, 1,500 to 2,500 functions per field: least good share 1/2, lost share never above 2^{1−p}.
  - Lemma T for vector-valued x on Z_9, Z_27, Z_25, and an ascent on Z_9: never above 2^{1−p}.
- **Lemma 3T and 3′ on two-tree boxes** (`tree3T_own.py`): eleven boxes from Z_9 × Z_3 to Z_27 × Z_25, over Q and F_q, 69,084 functions (35,920 of rank one), every pattern on the active rows and columns. No exception for any of:
  - the rank-one factorisation;
  - at most a quarter of the sign vectors in K;
  - Lemma T for every (σ_Y, level of Y);
  - for a = 1, at most ±s lost;
  - the proved counts.

  Least good share: exactly 1/4 for rank one in every box, at least 13/32 for rank ≥ 2.
- **Lemma 3T with Y of two trees** (`tree3trees_own.py`): Z_49 × Z_3 × Z_5 and Z_25 × Z_3 × Z_7, 447 functions: no exception.
- **Theorem 7 end to end** (`thm7_own.py`):
  - Lemma G′ on 400 random cases.
  - 3,960 multisets on Z_675, Z_1575, Z_4725, Z_11025 (several m and q each), Z_118125 (m = 4375 and 189) and Z_165375 (m = 6125 and 1323); 540 of them on the two named n.
  - For each, a pattern good in the tree box was found and the signing divided by Φ_d for every d | n: none divisible.
  - 450 of the 3,960 use m = 675, where Γ ≤ 0, and are marked as tests of the chain only.
  - The division splits by exponents modulo d/rad(d); on 7,933 polynomials for n ≤ 11025 it agreed with the plain long division of my first pass.

## What I did not check

- The proofs of the first result, as before.
- The instance's programs: I read none. I saw four of its outputs only after my own runs, and I read the head of your brief to it.
- Three trees beyond the two boxes named; Theorem P by more coordinates.
- §8, and whether any of this is in print.

## Housekeeping

Every program ran through `cap2g.sh`, at most two at a time. The exhaustive run on Z_9 took four and a half minutes. One run hit the 2 GB cap after a minute and a half (the digit recursion on large exponents) and was rerun restricted. Nothing is running. I wrote only in `third/`; my earlier files and `report.md` are untouched. No network, nothing posted.
