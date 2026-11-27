import Pnq.EvenFinal

/-! Tests of the definitions of `Pnq/EvenDefs.lean`, `Pnq/EvenTwice.lean` and `Pnq/EvenFinal.lean` on small data, and
checks that the fixed statements fit together.  The expected values, in the comments, were worked out outside Lean (by
hand and by a Python program written from the plan, all signings).  `val3`, `Bad3`, `bad3Set`, `classSum3` cannot be
evaluated (the algebraic closure is not computable); `csum`, `levelBad`, `μ` can.  The theorems of the eight files are
still `sorry` when this file is written: nothing here is evidence for them, only for the definitions and the forms. -/

open Pnq

/-! ### part T: `csum`, `levelBad`, and the two cardinalities of the theorem, by brute force -/

/-- `levelBad` can be decided when equality in `V` can (for this test file only) -/
instance levelBadDecidable {ι V : Type} [Fintype ι] [AddCommGroup V] [DecidableEq V]
    (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) : (j : ℕ) → Decidable (levelBad pos val ε j)
  | 0 => inferInstanceAs (Decidable (∑ k, sg (ε k) • val k = 0))
  | j + 1 => inferInstanceAs (Decidable (∀ r, r < 2 ^ j →
      csum pos val ε (2 ^ (j + 1)) r = csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j)))

/-- the left side of T: the number of signings with some level `j ≤ K` bad -/
def cntSome {m : ℕ} {V : Type} [AddCommGroup V] [DecidableEq V] (pos : Fin m → ℕ) (val : Fin m → V)
    (K : ℕ) : ℕ :=
  (Finset.univ.filter fun ε : Fin m → Bool => ∃ j, j ≤ K ∧ levelBad pos val ε j).card

/-- the number of signings with level `j` bad (`j = 0`: half the right side of T) -/
def cntAt {m : ℕ} {V : Type} [AddCommGroup V] [DecidableEq V] (pos : Fin m → ℕ) (val : Fin m → V)
    (j : ℕ) : ℕ :=
  (Finset.univ.filter fun ε : Fin m → Bool => levelBad pos val ε j).card

-- the pair with positions 0, 1 and values 1, 1 in ℤ, K = 1: all 4 signings bad somewhere, 2 at level 0 (equality in T)
#eval (cntSome ![0, 1] ![(1 : ℤ), 1] 1, cntAt ![0, 1] ![(1 : ℤ), 1] 0)   -- expected (4, 2)
example : cntSome ![0, 1] ![(1 : ℤ), 1] 1 = 4 := by decide
example : cntAt ![0, 1] ![(1 : ℤ), 1] 0 = 2 := by decide

-- three elements, positions 0, 1, 2, values 1 in ℤ, K = 2
#eval (cntSome ![0, 1, 2] ![(1 : ℤ), 1, 1] 2, cntAt ![0, 1, 2] ![(1 : ℤ), 1, 1] 0)   -- expected (0, 0)
-- three elements, a repeated position, values v, -v, v in ZMod 3, K = 2
#eval (cntSome ![0, 0, 1] ![(1 : ZMod 3), 2, 1] 2, cntAt ![0, 0, 1] ![(1 : ZMod 3), 2, 1] 0)   -- expected (4, 2)
-- four elements, positions 0, 1, 2, 3, values 1 in ℤ, K = 3; the numbers at the levels 0, 1, 2, 3
#eval (cntSome ![0, 1, 2, 3] ![(1 : ℤ), 1, 1, 1] 3,
  (List.range 4).map (cntAt ![0, 1, 2, 3] ![(1 : ℤ), 1, 1, 1]))   -- expected (8, [6, 6, 4, 0])
-- four elements, a repeated position, a pair v, -v, a value 0, in ℤ, K = 3
#eval (cntSome ![0, 0, 2, 5] ![(1 : ℤ), -1, 0, 2] 3,
  (List.range 4).map (cntAt ![0, 0, 2, 5] ![(1 : ℤ), -1, 0, 2]))   -- expected (8, [4, 4, 0, 0])
-- four elements, a repeated position, values in ZMod 3, K = 3
#eval (cntSome ![3, 3, 1, 5] ![(1 : ZMod 3), 1, 2, 2] 3,
  (List.range 4).map (cntAt ![3, 3, 1, 5] ![(1 : ZMod 3), 1, 2, 2]))   -- expected (12, [6, 6, 6, 4])
-- five elements, a repeated position, values in ZMod 5 with a pair v, -v, K = 3
#eval (cntSome ![0, 1, 1, 2, 7] ![(1 : ZMod 5), 2, 3, 4, 1] 3,
  (List.range 4).map (cntAt ![0, 1, 1, 2, 7] ![(1 : ZMod 5), 2, 3, 4, 1]))   -- expected (8, [6, 6, 4, 0])
-- five elements, a value 0, in ℤ, K = 3
#eval (cntSome ![0, 4, 2, 6, 1] ![(1 : ℤ), 1, 1, 1, 0] 3,
  (List.range 4).map (cntAt ![0, 4, 2, 6, 1] ![(1 : ℤ), 1, 1, 1, 0]))   -- expected (16, [12, 12, 12, 8])
-- the multiset {0, 0, 0, 1} with values 1 in ZMod 3, K = 2 (share 3/4 bad somewhere: equality in T)
#eval (cntSome ![0, 0, 0, 1] ![(1 : ZMod 3), 1, 1, 1] 2,
  (List.range 3).map (cntAt ![0, 0, 0, 1] ![(1 : ZMod 3), 1, 1, 1]))   -- expected (12, [6, 6, 0])

/-! `levelBad` at the levels 0, 1, 2, 3 by hand: positions 0, 1, 2, 3, values 1 in ℤ.
Signs `+ + - -`: level 0 bad (sum 0); level 1 bad (classes modulo 2: `{0, 2}` with sum 0, `{1, 3}` with sum 0);
level 2 not bad (classes 0 and 2 modulo 4 have sums 1 and -1); level 3 not bad (class 0 modulo 8 has sum 1, class 4
is empty).
Signs `+ - + -`: level 0 bad; level 1 not bad (sums 2 and -2); level 2 bad (classes 0, 2: 1 = 1; classes 1, 3:
-1 = -1); level 3 not bad. -/

#eval (List.range 4).map fun j =>
  decide (levelBad ![0, 1, 2, 3] ![(1 : ℤ), 1, 1, 1] ![true, true, false, false] j)
-- expected [true, true, false, false]
#eval (List.range 4).map fun j =>
  decide (levelBad ![0, 1, 2, 3] ![(1 : ℤ), 1, 1, 1] ![true, false, true, false] j)
-- expected [true, false, true, false]

/-! ### E1: the signings whose sum of signs is divisible by 3 (the right side of `bad3_one_iff`) -/

#eval (List.range 8).map fun m =>
  (Finset.univ.filter fun ε : Fin m → Bool => (3 : ℤ) ∣ ∑ k, sg (ε k)).card
-- expected [1, 0, 2, 2, 6, 10, 22, 42]   (three times: 3, 0, 6, 6, 18, 30, 66, 126)

-- the equation of `card_bad3Set_one` with this count in the place of `(bad3Set e 1).card`, for m = 0, …, 7
#eval (List.range 8).map fun m =>
  let c := (Finset.univ.filter fun ε : Fin m → Bool => (3 : ℤ) ∣ ∑ k, sg (ε k)).card
  decide (3 * c + (if Even m then 0 else 2) = 2 ^ m + (if Even m then 2 else 0))
-- expected [true, true, true, true, true, true, true, true]

/-- from the statement E1 (`card_bad3Set_one`, not yet proved): two of the four signings of two elements are 3-bad
at `1` -/
example : 3 * (bad3Set ![0, 1] 1).card = 6 := by
  simpa using card_bad3Set_one (![0, 1] : Fin 2 → ℕ)

/-! ### the definition `Bad3` itself, on three cases (`F3` has characteristic 3) -/

example : Bad3 ![0, 1] ![true, false] 1 := by
  intro ζ hζ
  rw [IsPrimitiveRoot.one_right_iff] at hζ
  subst hζ
  simp [val3, sg, Fin.sum_univ_two]

/-- three signs `+` add up to `3 = 0` in `F3` -/
example : Bad3 ![0, 1, 2] (fun _ => true) 1 := by
  intro ζ hζ
  rw [IsPrimitiveRoot.one_right_iff] at hζ
  subst hζ
  have h3 : ((3 : ℕ) : F3) = 0 := CharP.cast_eq_zero F3 3
  simp only [val3, sg, Fin.sum_univ_three, ite_true, one_pow, mul_one, Int.cast_one]
  push_cast at h3
  linear_combination h3

/-- two signs `+` add up to `2 ≠ 0` in `F3` -/
example : ¬ Bad3 ![0, 1] (fun _ => true) 1 := by
  intro h
  have h1 := h 1 IsPrimitiveRoot.one
  simp only [val3, sg, Fin.sum_univ_two, ite_true, one_pow, mul_one, Int.cast_one] at h1
  have h2 : ((2 : ℕ) : F3) = 0 := by push_cast; linear_combination h1
  have h3 := (CharP.cast_eq_zero_iff F3 3 2).mp h2
  omega

/-! ### N1′: the left side for three sets (`μ 5 = 4`, `μ 7 = μ 35 = 6`, `μ 25 = μ 175 = 8`) -/

#eval [({5} : Finset ℕ), {5, 7, 35}, {5, 7, 25, 35, 175}].map fun T => ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t
-- expected [1/16, 3/32, 13/128]   (1/16; 1/16 + 2/64; 1/16 + 2/64 + 2/256)
#eval [5, 7, 25, 35, 175].map μ   -- expected [4, 6, 8, 6, 8]

/-! ### `ExceptionalPair`

It cannot be decided in general.  What it should give (`w` the two marks `a`, `b`; the additive order of `a - b` in
`ZMod n` is `n / gcd n (a - b)`; exceptional exactly when the power of 2 in `n` does not divide `a - b`):
* `n = 2`: `{0, 1}` order 2, exceptional.
* `n = 4`: `{0, 1}` order 4, exceptional; `{0, 2}` order 2, exceptional; `{1, 1}` order 1, not exceptional.
* `n = 6`: `{0, 1}` order 6, exceptional; `{0, 3}` order 2, exceptional; `{0, 2}` and `{1, 3}` order 3, not.
* `n = 12`: `{0, 3}` order 4, `{0, 6}` order 2, `{0, 2}` order 6: exceptional; `{0, 4}`, `{0, 8}`, `{5, 1}` order 3: not.
* a multiset that is not two marks (one mark, three marks, …) is never exceptional. -/

theorem ord_6_3 : addOrderOf ((0 : ZMod 6) - 3) = 2 :=
  (congrArg addOrderOf (by decide : ((0 : ZMod 6) - 3) = ((3 : ℕ) : ZMod 6))).trans
    ((ZMod.addOrderOf_coe 3 (by norm_num)).trans (by norm_num))

theorem ord_6_2 : addOrderOf ((0 : ZMod 6) - 2) = 3 :=
  (congrArg addOrderOf (by decide : ((0 : ZMod 6) - 2) = ((4 : ℕ) : ZMod 6))).trans
    ((ZMod.addOrderOf_coe 4 (by norm_num)).trans (by norm_num))

/-- `{0, 3}` on `ZMod 6` is an exceptional pair -/
example : ExceptionalPair (Pi.single (0 : ZMod 6) 1 + Pi.single (3 : ZMod 6) 1) :=
  ⟨0, 3, rfl, by rw [ord_6_3]; decide⟩

/-! ### the fixed statements fit together (derivations at the level of statements; the parts are still `sorry`) -/

/-- L, level `j + 1`: S0′ with `p = 2`, `i = j + 1`, `c = r`, `t = 0`, `t' = 1` gives `levelBad` at `j + 1`, with `V`
the functions on the primitive `d`-th roots of unity -/
theorem fit_succ {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (hd : ¬ 2 ∣ d) (h3 : ¬ 3 ∣ d) (j : ℕ)
    (hbad : Bad3 e ε (2 ^ (j + 1) * d)) :
    levelBad e (fun k => fun η : {η : F3 // IsPrimitiveRoot η d} => η.1 ^ e k) ε (j + 1) := by
  intro r hr
  funext η
  have h := classSum3_eq_of_bad3 e ε Nat.prime_two (by norm_num) (by omega : 1 ≤ j + 1) hd h3
    η.2 hbad r 0 1 (by norm_num) (by norm_num)
  rw [Nat.add_sub_cancel, Nat.mod_eq_of_lt hr, zero_mul, add_zero, one_mul] at h
  simp only [csum, classSum3] at h ⊢
  rw [Finset.sum_apply, Finset.sum_apply]
  convert h using 2 <;> split_ifs <;> simp [zsmul_eq_mul]

/-- L, level `0`: `levelBad` at `0` for these values is `Bad3 e ε d` -/
theorem fit_zero {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} :
    levelBad e (fun k => fun η : {η : F3 // IsPrimitiveRoot η d} => η.1 ^ e k) ε 0 ↔ Bad3 e ε d := by
  rw [levelBad_zero]
  constructor
  · intro h ζ hζ
    have := congrFun h ⟨ζ, hζ⟩
    simpa [val3, Finset.sum_apply, zsmul_eq_mul] using this
  · intro h
    funext η
    have := h η.1 η.2
    simpa [val3, Finset.sum_apply, zsmul_eq_mul] using this

open Classical in
/-- L from T and the two facts above: the two filtered sets of T and of L, and `bad3Set`, fit together (the
decidability and the `Fintype (ι → Bool)` that `open Classical in` brings are the same in the three statements) -/
example {ι : Type*} [Fintype ι] (e : ι → ℕ) {d : ℕ} (hd : ¬ 2 ∣ d) (h3 : ¬ 3 ∣ d) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ Bad3 e ε (2 ^ j * d)).card ≤
      2 * (bad3Set e d).card := by
  have hT := card_exists_levelBad_le e
    (fun k => fun η : {η : F3 // IsPrimitiveRoot η d} => η.1 ^ e k) K
  refine le_trans (Finset.card_le_card ?_) (le_trans hT ?_)
  · intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε ⊢
    obtain ⟨j, hj, hb⟩ := hε
    refine ⟨j, hj, ?_⟩
    cases j with
    | zero => exact (fit_zero e ε).mpr (by simpa using hb)
    | succ j => exact fit_succ e ε hd h3 j hb
  · refine Nat.mul_le_mul_left 2 (Finset.card_le_card ?_)
    intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε
    exact (mem_bad3Set e d ε).mpr ((fit_zero e ε).mp hε)

/-- B from A′ and M -/
example (n : ℕ) (hn : n ≠ 0) {ι : Type*} [Fintype ι] (hm : 3 ≤ Fintype.card ι) (e : ι → ℕ) :
    ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ BadAt e ε d := by
  obtain ⟨a, n3, hn3, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hn 3 (by norm_num)
  obtain ⟨ε, hε⟩ := exists_not_bad3 n3 hn3 hm e
  refine ⟨ε, fun d hd hbad => ?_⟩
  have hd0 : d ≠ 0 := fun h => hn (zero_dvd_iff.mp (h ▸ hd))
  obtain ⟨i, d', hd', rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hd0 3 (by norm_num)
  have h1 : d' ∣ 3 ^ a * n3 := (Dvd.intro_left _ rfl).trans hd
  have hco : Nat.Coprime d' (3 ^ a) :=
    Nat.Coprime.pow_right _ ((Nat.Prime.coprime_iff_not_dvd Nat.prime_three).2 hd').symm
  exact hε d' (hco.dvd_of_dvd_mul_left h1) (bad3_of_badAt e ε i hd' hbad)

/-- the first final statement for three or more elements, from B, as `exists_signs_odd` was drawn from
`exists_not_badAt` (the type of the elements and its number of points) -/
example {n : ℕ} [NeZero n] (w : ZMod n → ℕ) (h3 : 3 ≤ ∑ x, w x) :
    ∃ ε : (Σ x : ZMod n, Fin (w x)) → Bool, ∀ d, d ∣ n →
      ¬ BadAt (fun k : Σ x : ZMod n, Fin (w x) => k.1.val) ε d :=
  exists_not_badAt_of_three_le n (NeZero.ne n) (by simpa [Fintype.card_sigma] using h3) _

/-! ### the unfolding lemmas are proved -/

#print axioms Pnq.mem_bad3Set        -- expected: no `sorryAx`
#print axioms Pnq.val3_eq_aeval      -- expected: no `sorryAx`
#print axioms Pnq.val3_eq_eval₂      -- expected: no `sorryAx`
#print axioms Pnq.val3_eq_eval_map   -- expected: no `sorryAx`
#print axioms Pnq.levelBad_zero      -- expected: no `sorryAx`
#print axioms Pnq.levelBad_succ      -- expected: no `sorryAx`
