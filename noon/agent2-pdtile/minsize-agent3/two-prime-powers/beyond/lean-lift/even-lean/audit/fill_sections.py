"""Puts the sections of the report into audit.md (text only; nothing is computed)."""
import sys
p = '/home/agent3/lean/even-audit/audit.md'
s = open(p).read()
sec = {}

sec['VERDICT'] = """- **I found no statement that is false, vacuous or weaker than the plan means, and no definition that is not what is
  meant.** No test disagrees with any of the fourteen: 0 violations of T on 6,108,783 enumerated and 330,000 random
  valued families (every signing, every K); 0 violations of M, S0′, S1′, S2′ on 186,900 + 85,300 instances and of L on
  306,500; E1 exact for every m ≤ 200; the sum of N1′ over ALL allowed t is 0.1185647 < 1/8; a 3-good signing for each
  of 105,949,207 multisets of three or more elements on 36 moduli prime to 3, a good signing for each of 101,278,905
  on 33 moduli; "a good splitting exists iff not an exceptional pair" for all 2,103,671 nonempty multisets tried on
  n ≤ 63.
- **The definitions.** `Bad3 e ε d` for `3 ∤ d` is "Φ_d divides the signed mask modulo 3": proved in Lean in my copy
  (no `sorry` used) and confirmed by a second program in GF(3^r). For `3 ∣ d` it holds for every signing and for d = 0
  it is another condition; no statement uses it there. `ExceptionalPair` is "two elements a, b with 2^k ∤ a − b": equal
  to those words for every pair on every n ≤ 64; two equal marks are not exceptional (proved). For n = 0 it would be
  wrong; n = 0 is excluded. `csum`, `levelBad` evaluate in Lean to what my program gives (78 families).
- **The two final statements against Corollary 3.** `exists_signs_all` is Corollary 3's statement of existence, clause
  for clause, in the form of this morning's `exists_signs_odd` (which is an instance of it: compiled). Two differences,
  neither a defect: (1) Corollary 3's shares of good signings (at least 1/2 for m = 3, 1/4 for m = 4, more than 0.075
  for m ≥ 5) are in no Lean statement; (2) `not_exists_signs_of_exceptionalPair` is NOT part of Corollary 3 as written
  in `theorem-twice.md` (which says only "Then B has a good signing"): it is the parenthesis of Conjecture E in
  `brief-even.md` ("Such a pair has no good signing"), "the 'only if'" of `even-result.md`. It is true and tested. The
  two together are Conjecture E as an "if and only if".
- **Against the plan.** The twelve other statements are the plan's parts; the differences are of form only (§3). One
  error in the plan's text, in a route and not in a statement: its last sentence names the wrong cyclotomic polynomial
  for the second final statement (Φ_(2^s), 2^s the power of 2 in the order of a − b; the one that works is
  Φ_d with d = 2^(v_2(a−b)+1); e.g. n = 4, {0, 2}). Brief F gives a correct argument, so no prover depends on it.
- **The parts fit.** L from T and S0′, and B from A′ and M: the derivations of `CheckEven.lean` are complete; as named
  theorems in my copy they have exactly the types of the fixed L and B. S2′ with the rank is S2′ with a pivot set
  plus the finished `exists_isPivot` (one line). The first final statement for three or more elements follows from B
  as `exists_signs_odd` did from `exists_not_badAt` (compiled); one and two elements need no other statement. A′ from
  S1′, S2′, E1, L, N1′ by the plan's argument: every step holds numerically on 120,300 families, the step-down is
  derived in Lean from S1′, the arithmetic is right. No statement is too weak for its use.
- Remarks, none a defect: `h3` in S0′ follows from `hη`; `h3` is not needed for the truth of S1′ and of L (the
  skeleton's report says L needs it; for 3 ∣ d the right side of L is 2·2^m); `hd` of L is not needed for truth as far
  as tested (even d: 12,000 instances) but the derivation from S0′ needs it; M needs `h3` only to exclude d = 0;
  `3 ≤ card` in A′ and B also excludes one-element families and non-exceptional pairs, where the conclusions hold
  (the final statement treats those by hand); the 1/8 of N1′ has the margin 0.0064 and A′ would do with any bound
  below 7/48."""

sec['DIFFERENCES'] = """**From the plan (statements).** None in substance. In form:
1. No separate `d ≠ 0` / `n ≠ 0` where a non-divisibility gives it: M and S2′ (`¬ 3 ∣ d`), S0′, S1′, S2′ (`¬ p ∣ d`), L
   (`¬ 2 ∣ d`; the plan lists "d ≠ 0"), A′ (`¬ 3 ∣ n`; the plan lists "n ≠ 0"). B keeps `n ≠ 0`, the final statements
   `[NeZero n]`.
2. E1, first half: `(3 : ℤ) ∣ ∑ k, sg (ε k)` for "≡ 0 (mod 3)". E1, count: one equation with two `if`s and no
   subtraction for "2^m + 2 if m is even, 2^m − 2 if m is odd".
3. N1′: "t > 1 prime to 6" is `¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t`.
4. S0′, S1′, both S2′: as text they are this morning's S0, S1, S2 (a), S2 with `F3` for ℂ, `Bad3`, `bad3Set`,
   `classSum3` for `BadAt`, `badSet`, `classSum`, and the two added hypotheses `(hp3 : p ≠ 3)`, `(h3 : ¬ 3 ∣ d)`:
   identical after that substitution (`a7_textdiff.out`).
5. `ExceptionalPair` and the two final statements: identical to the plan's block, whitespace apart
   (`a7_textdiff.out`).
6. Six proved lemmas that the plan does not list: `mem_bad3Set`, `val3_eq_aeval`, `val3_eq_eval₂`,
   `val3_eq_eval_map`, `levelBad_zero`, `levelBad_succ` (none depends on `sorryAx`).

**From the plan (routes; the plan had been read by nobody, so I checked what I could compute).**
- T: the facts (a), (b), (c), (d) of the route hold on 2,500 random valued families, word-for-word definitions
  (`t1b_route.out`).
- N1′: b(0..19) are as listed; W6(19) = 63653689/536870912; (5/2)(5/7)^19 = 0.004183 < 0.0042; the total 0.122747 is
  below 0.1228 and below 1/8; b(u)·(1 + u) = a(u) and a(u)/4^u ≤ (5/7)^u for u < 400 (`t3_n1.out`).
- A′: the arithmetic is right (m = 3: 4 < 8; m = 4: 12 < 16; m ≥ 5: 2/3 + 4/(3·2^m) + 1/4 < 1), and the steps hold
  on 120,300 families (§6).
- **One error.** The last sentence of the plan: "if the order of a − b is 2^s·odd with s ≥ 1, then Φ_(2^s) divides
  X^a + X^b". That is false in general: n = 4, {0, 2}: the order is 2 and Φ_2 = X + 1 does not divide 1 + X² (Φ_4
  does); n = 4, {0, 1}: the order is 4 and Φ_4 does not divide 1 + X (Φ_2 does). Of the 15,600 exceptional pairs with
  n ≤ 64, Φ_(2^s) divides X^a + X^b for 6,192; Φ_d with d = 2^(v_2(a−b)+1) divides it, and d divides n, for all 15,600
  (`t6b_plan_hint.out`). The plan hedges ("to be worked out by the prover"), the skeleton's report names the right
  d, and brief F argues with ζ^(o/2), ζ of order n, which is right. The statement itself is true.

**From Corollary 3 (`theorem-twice.md`) and Conjecture E (`brief-even.md`).**
- `exists_signs_all`, clause by clause: "n ≥ 1" is `[NeZero n]`; "B a nonempty multiset of Z_n" is `w : ZMod n → ℕ`
  with `∃ x, w x ≠ 0`; "not {a, b} with 2^k ∤ a − b" is `¬ ExceptionalPair w` (even additive order of a − b; the same
  for every pair on every n ≤ 64; in both wordings two equal elements are not excepted); "has a good signing" is the
  splitting u + v = w (equal elements may get different signs: u x of the w x copies of x get +) with no Φ_d, d ∣ n,
  d = 1 and d = n included, dividing `maskW u − maskW v = ∑ (u x − v x) X^x`, exponents 0 ≤ x < n ("good" as defined
  in `brief-even.md`: "divisible by no cyclotomic polynomial Φ_d, d | n (d = 1 included)").
- Not in Lean: the shares of Corollary 3 (at least 1/2 for m = 3, at least 1/4 for m = 4, more than
  p_(m−1) − 0.2372 > 0.075 for m ≥ 5), and "3-good" as a notion for multisets on Z_n. A′ and B say "there is one".
- Not in Corollary 3 as written: the second final statement. Corollary 3 states one direction. That an exceptional
  pair has no good signing is in Conjecture E ("EXCEPT exactly when", with its proof in a parenthesis) and in
  `even-result.md` ("iff … The 'only if' is in the brief"). A text that says "Corollary 3, in Lean" should say that
  the second Lean statement is that remark.
- The proof in Lean follows Corollary 3's (modulo 3 for every n; T for the prime 2; no contraction), with W(no 3)
  bounded by 1/8 where the paper has 0.118569, and without the paper's values of the shares."""

sec['TESTS'] = """Programs of mine, written for this audit from the Lean text; exact integer arithmetic; every signing of each family.
`ecore.py`: Φ_d by exact division (equal to sympy's for d ≤ 200; ∏_{d|n} Φ_d = X^n − 1 for n ≤ 80), the remainders of
X^x modulo Φ_d, "bad at d" (equal to a separate long division on 94,296 signings), "3-bad at d" for 3 ∤ d as "the
remainder modulo Φ_d has all coefficients divisible by 3" (equal to the definition taken literally in GF(3^r), §1),
class sums in Z[x]/(Φ_d, 3) (equality there is equality at every primitive d-th root of `F3`), and `live`, `rank`,
`IsPivot`, `μ` transcribed from `SignDefs.lean` (the largest pivot set by all subsets equals "occupied classes minus
full groups" on 3,016 cases). `t0_selftest.out`.

**T** (`t1_twice.py`; `t1_twice_A/B/C.out`, `t1_twice_slow.out`). `csum` and `levelBad` word for word; the fast code
equals a slow transcription on 154,097 (family, signing, level) triples.
- Complete enumerations, every multiset of pairs (position, value), each family once: 6,108,783 valued families.
  V = ℤ with values −2 … 2 (2,245,428: positions below 2, 4, 8, 16 with up to 8, 7, 5, 3 elements); ℤ/2 (706,729: up
  to 11, 9, 7, 5); ℤ/3 (998,478: up to 10, 8, 6, 4); ℤ/4 (328,372: positions below 2, 4, 8 with up to 9, 7, 4);
  ℤ/6 (914,888: up to 7, 6, 4); ℤ² with six values (914,888: up to 7, 6, 4). The value 0, repeated positions and
  the empty family are among them.
- Random: 330,000 families of 1 to 11 elements, positions up to 55, in the same six groups.
- For every family every K from 0 to k0 + 2, where 2^k0 exceeds every position (from level k0 + 1 on the levels say
  the same thing, so this is every K): 34,356,078 + 2,208,508 inequalities, **0 violations**.
- The factor 2 is attained: equality for some K in 2,234,869 of the enumerated families (the least: positions 0, 1,
  values v, v, K ≥ 1: 4 = 2·2); never in ℤ/2, where signs do not matter (largest ratio 1). In 311,174 enumerated
  families a level beyond the largest position is bad for some signing. K = 0: `x ≤ 2x`. Empty family: 1 ≤ 2.

**M, S0′, S1′, S2′** (`t2_parts.py slices`; `t2_slices_s2.out`, a smaller first run in `t2_slices_s1.out`). 98
configurations (p, i, d): p = 2 (i ≤ 4), 5 and 7 (i ≤ 3), 11 (i ≤ 2), 13 (i = 1); d in 1, 2, 4, 5, 7, 8, 10, 11, 14, 20,
22, 35, 55, 70 prime to p, p^i·d ≤ 1400; families of up to 9 elements: random, exponents up to 3·p^i·d (not reduced),
full groups, one class modulo d, few values, a full set of residues modulo p repeated.
- 186,900 instances (family, p, i, d); 72,231 have a 3-bad signing, 1,253,905 3-bad signings in all; 159,600 with
  d > 1, 56,400 with d of two primes (19,046 of these with a 3-bad signing); p = 2: 47,700 instances.
- S0′: every 3-bad signing on every group, 5,210,006 pairs: 0 violations. (The converse, flat on every group ⟹ 3-bad,
  which is not a statement, held everywhere too.)
- S1′: 132,003 instances whose level is not live (48,073 with a 3-bad signing): 0 violations.
- S2′ with the largest pivot set (which gives it for every pivot set): 0 violations; equality in 34,678 instances,
  21,175 of them with a nonempty pivot set (the bound is tight; e.g. a full set of residues modulo p).
- S2′ with the rank: 54,897 live instances (24,158 with a 3-bad signing): 0 violations; equality in 15,644.
- M: 85,300 instances (family, i = 0 … 3, d in 1, 2, 4, 5, 7, 8, 10, 14, 16, 20, 25, 35), 21,912 with a signing bad at
  3^i·d, 242,723 bad signings (97,369, 60,314, 44,549, 40,491 for i = 0, 1, 2, 3): 0 violations.
- p = 3, which `hp3` excludes (`t2_three.out`, and in Lean `S0_false_for_three`, `hyp_for_three`): as Lean has `Bad3`,
  every signing is 3-bad at 3^i·d, so the hypotheses would hold for every signing and the conclusions fail: S0′ would
  be false for 600 of 600 random families (in Lean: one element, exponent 0: class sums 1 and 0), S1′ with i = 1 for
  190 of 190 whose level 1 of 3 is not live, S2′ for every family with a nonempty pivot set. (With the paper's kind
  of hypothesis, "remainder modulo Φ_(3^i d) divisible by 3", flatness did hold in this run: 698 signings.)
- `¬ p ∣ d` is needed in S0′ and S1′ (e = (0, 2), all +, p = 2, i = 1, d = 2: 3-bad at 4, class sums 2 and 0, level 1
  not live, not 3-bad at 2); `hlive` is needed in S1′ (e = (0, 1), all +: 3-bad at 2, not at 1). `t2b_evend.out`.

**E1** (`t2_e1.out`). m = 0 … 14, every signing: "3-bad at 1" equals "3 divides the sum of the signs", and the count
satisfies the equation (1, 0, 2, 2, 6, 10, 22, 42, 86, 170, …); by the recursion on the three residues for every
m ≤ 200.

**L** (`t2_parts.py ladder`, `ladder2`). d in 1, 5, 7, 11, 13, 25, 35, 49, 55, 65, 77; exponents up to 2^(k+1)·d;
K = 0 … k + 2 (2^K·d ≤ 1300): 224,000 instances, 1,088,000 inequalities, 0 violations; 137,728 instances have a signing
3-bad at d; equality for some K in 53,769; largest ratio 2 (`t2_ladder_s2.out`; a smaller first run in
`t2_ladder_s1.out`). Far beyond the power of 2 that matters: exponents below 16, d in 1, 5, 7, 11, 13, K = 0 … 7:
82,500 instances, 660,000 inequalities, 0 violations; in 35,246 instances some signing is still 3-bad at 2^7·d
(`t2_ladder2_s1.out`, `t2_ladder2_s2.out`).

**N1′** (`t3_n1.out`). The supremum of the left side over all allowed T is W, the sum over all t > 1 prime to 6. With
A(s) = ∏ over the primes p ≥ 5, p − 1 ≤ s, of (1 + ⌊s/(p − 1)⌋) (equal to a count over all t ≤ 2,000,000 for s ≤ 12):
partial sum up to μ = 400 is 0.118564698205555, the tail after it is below 3.6·10^(−37) by a bound proved in the
program's header (A(s) ≤ (1 + s/4)·2^(2s/3); also checked for s ≤ 4000). So **0.118564 < W < 0.118565 < 1/8**: 1/8 is
right, the margin is 0.0064353 (W is 94.9% of 1/8), and no T that the hypothesis allows reaches 1/8: T is a set, so
its members are distinct, and they are among the t > 1 prime to 6. Each of the three conditions is needed: t = 1
adds 1, t = 3 adds 1/4, t = 2 adds 1/2; the largest single term allowed is 1/16 (t = 5).

**A′ and B** (`t4_all.py`; `t4_A.out`, `t4_B.out`; `t4b_small.out`). Signings tried in a fixed order until one works.
- A′, multisets containing 0 (one from each class of translates), 3 elements up to the size given: n = 2 (14), 4 (12),
  5 (10), 7 (9), 8 (10), 10 (9), 11, 13, 14, 16, 20 (8), 22, 25, 26, 28, 32, 35, 40 (7), 44, 49, 50, 52, 55, 56, 64, 70
  (6), 77, 80, 100, 140 (5), 175, 200, 280 (4), 385, 560, 700 (3): **105,949,207 multisets, none without a 3-good
  signing**; "all +" fails for 71,270,557; at most 48 signings tried.
- B, the same: n = 4 (12), 6, 8 (10), 9, 10, 12 (9), 15, 18, 20 (8), 21, 24, 27, 28, 30, 36, 40 (7), 42, 45, 48, 54, 60,
  63, 72 (6), 84, 90, 96, 105, 120 (5), 180, 210, 240 (4), 420, 840 (3): **101,278,905 multisets, none without a good
  signing**; "all +" fails for 23,194,936; at most 18 signings tried.
- The moduli of the brief: A′ for 4, 8, 10, 20, 28, 40 and B for 4, 8, 10, 12, 20, 24, 28, 40, 60, all with 3 to 6
  elements and more.
- Every multiset, without the reduction by translation (to test that reduction): A′ for n = 2, 4, 5, 8, 10, 20, 28,
  40 up to 12, 9, 7, 7, 6, 5, 4, 4 elements (239,202 multisets of three or more), B for n = 2, 4, 6, 8, 10, 12, 20, 24,
  28, 40, 60 up to 12, 9, 7, 7, 6, 6, 5, 5, 4, 4, 4 (1,010,507): none without.
- `3 ≤ card` is needed. For 24 moduli each: the empty family has no 3-good (good) signing (the mask is 0); every
  one-element family has one; of the pairs exactly those with a − b of even order have none (22,054 of 30,147 for A′,
  18,421 of 24,875 for B). In Lean: `A_false_pair` ({0, 1}, n = 2), `A_false_empty`.

**The two final statements** (`t5_final.py`, `t5_final_*.out`). Every multiset w on Z_n (no reduction), every
splitting u + v = w, divisibility of Σ (u_x − v_x) X^x by every Φ_d, d | n, by long division; `ExceptionalPair` from its
definition: all a, b with w = single(a) + single(b), the order of a − b by repeated addition. For every n ≤ 6 up to
10 elements, n = 7 … 10 up to 7, n = 11 … 16 up to 6, n = 17 … 24 up to 5, n = 25 … 36 up to 4, n = 37 … 63 up to 3:
**2,103,671 nonempty multisets; 13,584 are exceptional pairs and have no good splitting; the other 2,090,087 have
one; 0 mismatches**; the definition and "two elements with 2^k ∤ a − b" agree on all of them; every doubled mark is
not exceptional and has a good splitting. The empty multiset is not exceptional and has no good splitting, so `hw`
is needed. (The brief asked for n ≤ 16 and up to 4 elements.)"""

sec['VACUITY'] = """- **No hypothesis is contradictory.** Each of the fourteen is applied in Lean to data that satisfy its hypotheses
  (`A3_fit.lean`): M to {0, 1, 2}, all +, i = 1, d = 1 (Φ_3 divides 1 + X + X²); S0′ to {0, 1}, + +, p = 2, i = 1, d = 1,
  η = 1 (`bad3_two`: 3-bad at 2, proved); S1′ to {0, 0}, + −, with p = 2, d = 1 and with p = 5, d = 4; S2′ with the
  pivot set {0} of {0, 1} (p = 2, d = 5), and with the rank for {0, 1} (p = 2, d = 7) and {0, …, 4} (p = 5, d = 14);
  L with d = 35, K = 3; N1′ with T = {5, 7, 35}; A′ with n = 20 and n = 1; B with n = 12; the final statements with
  n = 12 and n = 1. The Lean lemmas of §1 show that `Bad3` is neither always true nor always false at d prime to 3.
- **No conclusion is trivially satisfiable.** "All +" fails for 71 million of the multisets of A′ and 23 million of
  those of B; the parts were tested on 72,231 + 21,912 instances that have bad signings, with equality in S2′ (34,678
  instances), in T (2,234,869 families) and in L (53,769 instances).
- **Hypotheses, needed or not.** T: none. M: `h3` is needed only to exclude d = 0 (for 3 ∣ d, d ≠ 0, the conclusion
  holds for every signing). S0′: `hp3` needed (false without: Lean, `S0_false_for_three`); `¬ p ∣ d` needed; `h3`
  follows from `hη`. S1′: `hp3`, `¬ p ∣ d`, `hlive` needed; `h3` not needed for truth (for 3 ∣ d the conclusion is
  empty). S2′: `hp3` and `h3` needed (otherwise `bad3Set` is everything); whether `¬ p ∣ d` and, in the form with the
  rank, `hlive` are needed I did not test. E1: none. L: `h3` is not needed for truth (for 3 ∣ d the right side is
  2·2^m; the skeleton's report says it is needed), `hd` not as far as tested (d in 2, 4, 8, 10, 14, 20, 28, 40: 12,000
  instances, 0 violations, `t2b_evend.out`); both are harmless, A′ has them, and the derivation of L from S0′ needs
  `hd`. N1′: all three conditions needed. A′: `hn` needed (for 3 ∣ n every signing is 3-bad at 3); `hm` needed for 0
  and 2 elements, not for 1. B: `hn` needed (Φ_0 = 1); `hm` as in A′. Final statements: `hw`, `hpair` needed;
  `[NeZero n]` is needed for the type (and for n = 0 `ExceptionalPair` would be wrong).
- **Weaker than it could be, by design:** A′ and B say nothing for one element and for the pairs that are not
  exceptional, where their conclusions hold; the first final statement treats those by hand. S0′ is one direction
  of Lemma S3. T is Theorem T′ without its term −P(F_k). None of this is needed.
- **Decidability instances** (`A1_instances.out`, printed with `pp.all`): the two filtered sets of T, the filtered set
  of L and `bad3Set` all use `Classical.propDecidable` for the predicate (inside `Nat.decidableExistsLE` for
  `∃ j, j ≤ K ∧ …`) and `Pi.instFintype` with `Classical.propDecidable` for equality on ι: the same instances. The
  derivation of L from T, with `bad3Set` on the right, compiles and has the type of the fixed L.
- **Universe levels.** A′ and B are polymorphic in the universe of ι; T in those of ι and V. A′ applied to
  `Σ x : ZMod n, Fin (w x)` (the type the final statement needs) and T applied to an ι in `Type 5` with V the functions
  on the primitive roots: both compile (`A1_instances.lean`).
- **`[NeZero n]` against `n ≠ 0`.** B takes `hn : n ≠ 0`; the final statements carry `[NeZero n]`; `NeZero.ne n` is
  the bridge (compiled in `final_of_three_le`)."""

sec['USABILITY'] = """In Lean, in my copy (`A3_fit.lean`, `A6_dump.lean`; all compile; `sorryAx` enters only through the fixed statements):
- **L from T and S0′** (`L_derived`): the derivation of `CheckEven.lean`, as a named theorem. It is complete, and
  `example : type_of% @Pnq.card_exists_bad3_le := @L_derived` compiles: the derived statement is the fixed one,
  instances included. V is the functions from the primitive d-th roots of `F3` to `F3`; level 0 is `Bad3 e ε d` by
  unfolding; level j + 1 is S0′ with p = 2, c = r, t = 0, t′ = 1.
- **B from A′ and M** (`B_derived`): complete; has the type of the fixed B.
- **S2′ with the rank from S2′ with a pivot set** and the finished `exists_isPivot` (`S2rank_derived`): one line; has
  the type of the fixed statement.
- **The first final statement from B** for three or more elements (`final_of_three_le`): the proof of
  `exists_signs_odd` with B in the place of `exists_not_badAt`, unchanged otherwise. One element (a monomial) and two
  elements (X^a + X^b with a − b of odd order, or 2X^a) use no other statement; the case split "1, 2, ≥ 3" with
  `¬ ExceptionalPair` is complete. I did not write those two cases in Lean.
- **The new final statement contains this morning's** (`auditOddFromAll`: for odd n nothing is an exceptional pair,
  proved without `sorry`; the result has the type of `exists_signs_odd`).
- **A′ from S1′, S2′, E1, L, N1′.** By hand, following the plan: (i) by S1′ a signing 3-bad at d = 2^j·d′ is 3-bad at
  2^j or at 2^j·t for a live t | d′ (the factor 2^j stays in the "d" of S1′, which only asks `¬ p ∣ d`, `¬ 3 ∣ d`:
  `step_down3`, derived in Lean from S1′); (ii) for live t, S2′ with the rank at the best prime gives
  #bad3(t)·2^μ(t*) ≤ 2^m, t ↦ t* is injective with t* > 1 prime to 6 (finished lemmas of `SignAll`), and no t is live
  for m ≤ 4 (finished `rank_lt_card`); (iii) by L with K = v_2(n), E1 (`three_mul_card_bad3Set_one_le`, derived) and
  N1′ the signings 3-bad somewhere number at most 2·#bad3(1) + 2·2^m·Σ 2^(−μ(t*)) < 2^m. Numerically
  (`t7_fit.py`, three runs): 120,300 families of 3 to 10 elements on 26 moduli prime to 3 (2 … 280), 21,182 of them
  with a live t; step (i) on 745,207 pairs (family, d); injectivity; #bad3(t)·2^μ(t*) ≤ 2^m (equality 2,771 times);
  the covering by the ladders; each ladder ≤ 2·#bad3(t); the sum of 2^(−μ(t*)) (largest met 3/32); the final bound
  below 2^m and above the true count: 0 failures of any step. The largest share of signings 3-bad somewhere met is
  3/4 (m = 4 … 10), 1/2 for m = 3. Every hypothesis can be supplied at its place of use; no statement is too weak."""

sec['NOTCHECKED'] = """- The proofs, and anything in the provers' copies. I read no file of theirs.
- The paper's lemmas as mathematics (Lemma M, S3, L3, Theorem T′): I tested the Lean statements, I did not referee
  the proofs. Corollary 3's shares.
- In Lean: "Φ_d ∣ mask in (ℤ/3)[X] iff the remainder modulo Φ_d is divisible by 3" (by hand); the converse of
  `val3_zero_of_bad3_zero`; the first final statement for one and two elements; A′ from the parts (by hand and
  numerically only).
- Sizes beyond those listed: T beyond 11 elements or positions above 55; the parts beyond 9 elements (10 for L),
  primes above 13, moduli p^i·d above 1400, d with three primes; A′ and B beyond the sizes of §4 (more than 6 elements
  only for n ≤ 40; n above 700 and 840); the final statements beyond n = 63 and beyond the sizes listed; the
  argument of A′ beyond 10 elements and n = 280.
- Whether `¬ p ∣ d` is needed in S2′ and `hlive` in S2′ with the rank.
- Mathlib's `Polynomial.cyclotomic`, `AlgebraicClosure`, `IsPrimitiveRoot`, `addOrderOf` are taken to be what
  their names say (my Φ_d agree with sympy's; `ZMod.addOrderOf_coe` gives n / gcd).
- Values by `#eval` rest on Lean's compiler, not the kernel; kernel checks are the `decide` examples and the proved
  lemmas."""

sec['HOW'] = """- Lean: twelve jobs, each through `lean1.sh` in my copy, in the foreground, one at a time, 5 to 33 seconds each. No
  `lake build`, `update`, `clean`, `cache`. No file under `Pnq/`, `Pqr/`, `P2q2/` of my copy was written (none is newer
  than the copy; the eight `Even*.lean` still have the hashes of `SHA256-as-fixed`: `skeleton_sha256.txt`).
- Python: every program through `~/bin/cap2g.sh` with `-I`; never more than two at a time; chains of short runs,
  each with its own clock. No network; nothing posted; nothing is running now.
- **Departures.** (a) One run of `t3_n1.py` went over five minutes: it summed fractions with denominators up to
  2^(2,000,000), a mistake of mine; I stopped it after about five and a quarter minutes, corrected the program (the
  terms with μ > 200 are now bounded, not summed), and the run kept takes 2.4 seconds. Stopping it with `pkill` also
  ended the shell command of mine that had started it; nothing else. (b) Two runs of `t5_final.py` took 289 seconds
  (they stop by their own clock; the limit was five minutes). (c) Shell tools for reading and copying (`cat`, `tail`,
  `grep`, `sed`, `cp`, `cmp`, `sha256sum`, `ps`) were run directly, and four short Python snippets that patched my own
  scripts ran without `cap2g.sh` while no computation was running. (d) A file of 676 bytes written by mistake to the
  session's temporary folder was removed.
- The first runs of `t2_parts.py` (seed 1) are kept beside the larger ones (seed 2); `t5_final_16_4.out` is a first
  trial contained in the later runs; `summary.py` counts each enumerated family of T once (chain C repeats the smaller
  sizes of chains A and B)."""

sec['FILES'] = """Lean (each `.lean` with its `.out`): `A1_print_copy.out` (`PrintEven.lean` in my copy), `A1_instances` (T, L,
`bad3Set`, `ExceptionalPair` with every instance; universe levels; axioms), `A0_checkeven.out` (the skeleton's
`CheckEven.lean` in my copy) with `a0_checkeven.py/.out` (its expected values recomputed: all right), `A2_sem`
(reading lemmas for `Bad3` and `ExceptionalPair`), `A3_fit` (derivations, instances, counterexamples without
hypotheses), `A4_eval` with `a4_gen.py`, `a4_cmp.py/.out`, `a4_expected.txt` (`csum`, `levelBad`), `A5_live` with
`a5_gen.py`, `a5_cmp.out`, `a5_expected.txt` (`live`, `rank`, `μ`), `A6_dump` (fingerprints of the eight definitions
and fourteen statements as elaborated, for comparison with the finished project; the odd case from the new final
statement). Text: `a7_textdiff.py/.out`, `skeleton_sha256.txt`. Tests: `ecore.py`, `t0_selftest`, `t1_twice`
(`run_t1.sh`, `run_t1c.sh`; A, B, C, slow), `t1b_route`, `t2_parts` (slices, ladder, ladder2, e1, three), `t2b_evend`,
`t3_n1`, `t4_all` (`run_t4.sh`; A, B), `t4b_small`, `t5_final` (`run_t5.sh`), `t6_exc`, `t6b_plan_hint`, `t7_fit`.
Totals: `summary.py/.out`. `fill_sections.py` put the sections of this report together (text only)."""

for k, v in sec.items():
    key = '«' + k + '»'
    assert key in s, k
    s = s.replace(key, v)
assert '«' not in s
open(p, 'w').write(s)
print("sections written:", list(sec))
