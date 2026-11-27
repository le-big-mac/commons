/-
Lifting to a set.  For an odd prime `r`, a nonempty multiset on `ZMod N` whose multiplicities are at most `r^j` and not all equal to
`r^j` is the reduction modulo `N` of a SET on `ZMod (N * r^j)` whose mask polynomial has exactly the same cyclotomic divisors: for
`d ∣ N * r^j`, `Φ_d` divides the mask of the set exactly when `d ∣ N` and `Φ_d` divides the mask of the multiset.
(Statement fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of it.  On paper: the copies of each element are spread
over its lifts, one prime step at a time, and the count of roots of the lemma on lifts shows that no new divisor comes in.)
-/
import Pnq.Lift

open Finset

namespace Pnq

namespace Lift

/-! Helper lemmas live in the namespace `Pnq.Lift.SetAux`.  The plan:

* `shift_sum_eq` (the criterion): if `Φ_{e r^(k+1)}` divides the mask of a multiset on `ZMod M`, `r ∤ e`, and `ω` is a root of
  unity of order `e`, then the sum of `ω^y` over the elements `y` (with multiplicity) with residue `b` modulo `r^(k+1)` is the
  same for `b` and for `b + r^k` (modulo `r^(k+1)`).  It is proved by a count of roots, as the key lemma of `Pnq/Lift1.lean`,
  without dividing by a cyclotomic polynomial.
* `exists_dist_eq`, `exists_dist_ne`: how the copies of one element are dealt to its `r` lifts ("slots" `0, …, r - 1`).
* `spread`: the lift given by such numbers, and what is needed about it.
* `exists_step`: one prime step, from `ZMod N` to `ZMod (N * r)`, multiplicities at most `r * B` becoming at most `B`.  The
  chosen element `x₁` is any element whose multiplicity is neither `0` nor `r * B`; its copies are dealt by `exists_dist_ne`
  (two cases, by whether `r` divides the multiplicity of `x₁` itself), those of every other element by `exists_dist_eq`.
* `exists_multi_lift`: `j` steps, by induction on `j`, on `ZMod M` for any `M = N * r^j`. -/

namespace SetAux

open Polynomial

/-- **The criterion.**  `r` a prime, `r ∤ e`, `ω` a root of unity of order `e`.  If `Φ_{e r^(k+1)}` divides the mask of `w`,
then for every `c` the sum of `w(y) ω^y` over the `y` whose residue modulo `r^(k+1)`, moved up by `r^k` (modulo `r^(k+1)`),
is `c`, equals the sum over the `y` whose residue is `c`.  (The polynomial
`∑_y w(y) ω^y (Y^((y mod r^(k+1) + r^k) mod r^(k+1)) - Y^(y mod r^(k+1)))` has degree below `r^(k+1)` and vanishes at every
`r^(k+1)`-th root of unity `η`: its value there is `(η^(r^k) - 1)` times the value of the mask at `ω η`, and either
`η^(r^k) = 1` or `ω η` is a primitive `e r^(k+1)`-th root of unity.  So it is `0`; the difference of the two sums is its
coefficient at `c`.) -/
theorem shift_sum_eq {M : ℕ} [NeZero M] (w : ZMod M → ℕ) {r : ℕ} (hr : r.Prime) (k e : ℕ)
    (he0 : e ≠ 0) (he : ¬ r ∣ e) (hdvd : cyclotomic (e * r ^ (k + 1)) ℤ ∣ maskW w) {ω : ℂ}
    (hω : IsPrimitiveRoot ω e) (c : ℕ) :
    ∑ y : ZMod M, (w y : ℂ) *
        (if (y.val % r ^ (k + 1) + r ^ k) % r ^ (k + 1) = c then ω ^ y.val else 0) =
      ∑ y : ZMod M, (w y : ℂ) * (if y.val % r ^ (k + 1) = c then ω ^ y.val else 0) := by
  have hRpos : 0 < r ^ (k + 1) := pow_pos hr.pos _
  have hco : e.Coprime (r ^ (k + 1)) :=
    Nat.Coprime.pow_right _ (Nat.Coprime.symm ((Nat.Prime.coprime_iff_not_dvd hr).2 he))
  -- the polynomial in `Y`
  set ℓ : ℂ[X] := ∑ y : ZMod M, C ((w y : ℂ) * ω ^ y.val) *
    (X ^ ((y.val % r ^ (k + 1) + r ^ k) % r ^ (k + 1)) - X ^ (y.val % r ^ (k + 1))) with hℓ
  -- it vanishes at every `r^(k+1)`-th root of unity
  have hroot : ∀ η ∈ nthRootsFinset (r ^ (k + 1)) (1 : ℂ), ℓ.eval η = 0 := by
    intro η hη
    rw [mem_nthRootsFinset hRpos] at hη
    have hmod : ∀ n : ℕ, η ^ (n % r ^ (k + 1)) = η ^ n := by
      intro n
      conv_rhs => rw [← Nat.div_add_mod n (r ^ (k + 1)), pow_add, pow_mul, hη, one_pow, one_mul]
    have hterm : ∀ y : ZMod M, eval η (C ((w y : ℂ) * ω ^ y.val) *
        (X ^ ((y.val % r ^ (k + 1) + r ^ k) % r ^ (k + 1)) - X ^ (y.val % r ^ (k + 1))))
        = (η ^ r ^ k - 1) * ((w y : ℂ) * (ω * η) ^ y.val) := by
      intro y
      have e1 : η ^ ((y.val % r ^ (k + 1) + r ^ k) % r ^ (k + 1)) = η ^ y.val * η ^ r ^ k := by
        rw [hmod, pow_add, hmod]
      rw [eval_mul, eval_C, eval_sub, eval_pow, eval_pow, eval_X, e1, hmod, mul_pow]
      ring
    rw [hℓ, eval_finsetSum, Finset.sum_congr rfl fun y _ => hterm y, ← Finset.mul_sum]
    by_cases h1 : η ^ r ^ k = 1
    · rw [h1, sub_self, zero_mul]
    · have hfact : Fact r.Prime := ⟨hr⟩
      have hord : orderOf η = r ^ (k + 1) := orderOf_eq_prime_pow h1 hη
      have hprim : IsPrimitiveRoot (ω * η) (e * r ^ (k + 1)) := by
        have e1 : orderOf ω = e := hω.eq_orderOf.symm
        rw [IsPrimitiveRoot.iff_orderOf,
          (Commute.all ω η).orderOf_mul_eq_mul_orderOf_of_coprime (by rw [e1, hord]; exact hco),
          e1, hord]
      rw [Aux.sum_eq_zero_of_cyclotomic_dvd w (Nat.mul_pos (Nat.pos_of_ne_zero he0) hRpos) hdvd
        hprim, mul_zero]
  -- its degree is below the number of these roots
  have hdeg : ℓ.natDegree < (nthRootsFinset (r ^ (k + 1)) (1 : ℂ)).card := by
    rw [(Complex.isPrimitiveRoot_exp _ hRpos.ne').card_nthRootsFinset]
    have hle : ℓ.natDegree ≤ r ^ (k + 1) - 1 := by
      refine natDegree_sum_le_of_forall_le _ _ fun y _ => ?_
      refine (natDegree_C_mul_le _ _).trans ((natDegree_sub_le _ _).trans ?_)
      rw [natDegree_X_pow, natDegree_X_pow]
      exact max_le (Nat.le_sub_one_of_lt (Nat.mod_lt _ hRpos))
        (Nat.le_sub_one_of_lt (Nat.mod_lt _ hRpos))
    omega
  have hzero : ℓ = 0 := eq_zero_of_natDegree_lt_card_of_eval_eq_zero' ℓ _ hroot hdeg
  -- the difference of the two sums is its coefficient at `c`
  have hcoeff : ℓ.coeff c = ∑ y : ZMod M, (w y : ℂ) *
        (if (y.val % r ^ (k + 1) + r ^ k) % r ^ (k + 1) = c then ω ^ y.val else 0) -
      ∑ y : ZMod M, (w y : ℂ) * (if y.val % r ^ (k + 1) = c then ω ^ y.val else 0) := by
    have e1 : ∀ n : ℕ, (if c = n then (1 : ℂ) else 0) = if n = c then 1 else 0 :=
      fun n => if_congr eq_comm rfl rfl
    rw [hℓ, finsetSum_coeff, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [coeff_C_mul, coeff_sub, coeff_X_pow, coeff_X_pow, e1, e1]
    split_ifs <;> ring
  rw [hzero, coeff_zero] at hcoeff
  exact sub_eq_zero.1 hcoeff.symm

/-- the arithmetic of the slots, for the left side of the criterion: the residue `m + t r^k` (slot `t` of the class `m`
modulo `r^k`), moved up by `r^k`, is `c < r^k` exactly when `t = r - 1` and `m = c` -/
theorem shift_mod_eq_iff {r k m c t : ℕ} (hm : m < r ^ k) (hc : c < r ^ k) (ht : t < r) :
    (m + t * r ^ k + r ^ k) % r ^ (k + 1) = c ↔ t = r - 1 ∧ m = c := by
  rw [pow_succ' r k]
  generalize r ^ k = P at hm hc ⊢
  by_cases h : t + 1 = r
  · have e1 : m + t * P + P = m + r * P := by
      rw [← h]
      ring
    have e2 : m < r * P := lt_of_lt_of_le hm (Nat.le_mul_of_pos_left P (by omega))
    rw [e1, Nat.add_mod_right, Nat.mod_eq_of_lt e2]
    exact ⟨fun h' => ⟨by omega, h'⟩, fun h' => h'.2⟩
  · have h2 : (t + 2) * P ≤ r * P := Nat.mul_le_mul_right P (by omega)
    have e3 : (t + 2) * P = t * P + P + P := by ring
    have e1 : m + t * P + P < r * P := by omega
    rw [Nat.mod_eq_of_lt e1]
    constructor
    · intro h'
      omega
    · rintro ⟨h', -⟩
      omega

/-- the arithmetic of the slots, for the right side of the criterion: the residue `m + t P` is `c < P` exactly when
`t = 0` and `m = c` -/
theorem slot_eq_iff {P m c t : ℕ} (hc : c < P) : m + t * P = c ↔ t = 0 ∧ m = c := by
  constructor
  · intro h
    rcases Nat.eq_zero_or_pos t with h0 | h0
    · subst h0
      exact ⟨rfl, by omega⟩
    · have h1 : P ≤ t * P := Nat.le_mul_of_pos_left P h0
      omega
  · rintro ⟨rfl, rfl⟩
    omega

/-- the number of slots in a set `S` of slots -/
theorem sum_indicator (r : ℕ) (S : Finset ℕ) (hS : S ⊆ range r) :
    ∑ t ∈ range r, (if t ∈ S then 1 else 0) = S.card := by
  rw [Finset.sum_ite_mem, Finset.inter_eq_right.2 hS, Finset.sum_const, smul_eq_mul, mul_one]

/-- `r q + ρ ≤ r B` copies dealt to `r` slots: `q` to each, and one more to the slots of a set `S` of `ρ` slots; no slot
gets more than `B` -/
theorem dist_of_subset {r : ℕ} (hr : 0 < r) (q ρ B : ℕ) (hm : r * q + ρ ≤ r * B) (S : Finset ℕ)
    (hS : S ⊆ range r) (hcard : S.card = ρ) :
    ∑ t ∈ range r, (q + if t ∈ S then 1 else 0) = r * q + ρ ∧
      ∀ t, (q + if t ∈ S then 1 else 0) ≤ B := by
  constructor
  · rw [Finset.sum_add_distrib, Finset.sum_const, Finset.card_range, smul_eq_mul,
      sum_indicator r S hS, hcard]
  · intro t
    split_ifs with ht
    · have h1 : 0 < S.card := Finset.card_pos.2 ⟨t, ht⟩
      have h2 : r * q < r * B := by omega
      have h3 : q < B := Nat.lt_of_mul_lt_mul_left h2
      omega
    · have h2 : r * q ≤ r * B := by omega
      have h3 : q ≤ B := Nat.le_of_mul_le_mul_left h2 hr
      omega

/-- **Dealing the copies of an ordinary element.**  `r ≥ 3`, `m ≤ r B`: the `m` copies can be dealt to the slots
`0, …, r - 1`, at most `B` to each, with as many in the slot `0` as in the slot `r - 1`.  (With `m = r q + ρ`: `q` to each
slot and one more to the slots `1, …, ρ` if `ρ ≤ r - 2`, to all slots but the slot `1` if `ρ = r - 1`.) -/
theorem exists_dist_eq {r : ℕ} (hr3 : 3 ≤ r) (m B : ℕ) (hm : m ≤ r * B) :
    ∃ f : ℕ → ℕ, ∑ t ∈ range r, f t = m ∧ (∀ t, f t ≤ B) ∧ f 0 = f (r - 1) := by
  obtain ⟨q, ρ, rfl, hlt⟩ : ∃ q ρ, m = r * q + ρ ∧ ρ < r :=
    ⟨m / r, m % r, (Nat.div_add_mod m r).symm, Nat.mod_lt m (by omega)⟩
  by_cases hρ : ρ = r - 1
  · -- all slots but the slot `1`
    have hcard : ((range r).erase 1).card = ρ := by
      rw [Finset.card_erase_of_mem (Finset.mem_range.2 (by omega)), Finset.card_range, hρ]
    obtain ⟨h1, h2⟩ :=
      dist_of_subset (by omega) q ρ B hm _ (Finset.erase_subset 1 (range r)) hcard
    have e0 : 0 ∈ (range r).erase 1 :=
      Finset.mem_erase.2 ⟨by omega, Finset.mem_range.2 (by omega)⟩
    have e1 : r - 1 ∈ (range r).erase 1 :=
      Finset.mem_erase.2 ⟨by omega, Finset.mem_range.2 (by omega)⟩
    refine ⟨fun t => q + if t ∈ (range r).erase 1 then 1 else 0, h1, h2, ?_⟩
    change q + (if 0 ∈ (range r).erase 1 then 1 else 0)
      = q + (if r - 1 ∈ (range r).erase 1 then 1 else 0)
    rw [ite_eq_left e0, ite_eq_left e1]
  · -- the slots `1, …, ρ`
    have hS : Finset.Icc 1 ρ ⊆ range r := fun t ht =>
      Finset.mem_range.2 (lt_of_le_of_lt (Finset.mem_Icc.1 ht).2 hlt)
    have hcard : (Finset.Icc 1 ρ).card = ρ := by
      rw [Nat.card_Icc]
      exact Nat.add_sub_cancel _ _
    obtain ⟨h1, h2⟩ := dist_of_subset (by omega) q ρ B hm _ hS hcard
    have e0 : 0 ∉ Finset.Icc 1 ρ := fun h => by
      have := (Finset.mem_Icc.1 h).1
      omega
    have e1 : r - 1 ∉ Finset.Icc 1 ρ := fun h => by
      have := (Finset.mem_Icc.1 h).2
      omega
    refine ⟨fun t => q + if t ∈ Finset.Icc 1 ρ then 1 else 0, h1, h2, ?_⟩
    change q + (if 0 ∈ Finset.Icc 1 ρ then 1 else 0) = q + (if r - 1 ∈ Finset.Icc 1 ρ then 1 else 0)
    rw [ite_eq_right e0, ite_eq_right e1]

/-- **Dealing the copies of the chosen element.**  `r ≥ 3`, `0 < m < r B`: the `m` copies can be dealt to the slots
`0, …, r - 1`, at most `B` to each, with different numbers in the slot `0` and in the slot `r - 1`, and, if `B ≥ 2`, with
a slot that gets a number of copies other than `0` and `B`.  (With `m = r q + ρ`: if `ρ ≥ 1`, `q + 1` to the slots
`0, …, ρ - 1` and `q` to the others; if `ρ = 0`, `q + 1` to the slot `0`, `q - 1` to the slot `r - 1` and `q` to the
others.) -/
theorem exists_dist_ne {r : ℕ} (hr3 : 3 ≤ r) (m B : ℕ) (hm0 : m ≠ 0) (hm : m ≤ r * B)
    (hmB : m ≠ r * B) :
    ∃ f : ℕ → ℕ, ∑ t ∈ range r, f t = m ∧ (∀ t, f t ≤ B) ∧ f 0 ≠ f (r - 1) ∧
      (2 ≤ B → ∃ t, t < r ∧ f t ≠ 0 ∧ f t ≠ B) := by
  obtain ⟨q, ρ, rfl, hlt⟩ : ∃ q ρ, m = r * q + ρ ∧ ρ < r :=
    ⟨m / r, m % r, (Nat.div_add_mod m r).symm, Nat.mod_lt m (by omega)⟩
  by_cases hρ : ρ = 0
  · -- `m = r (q' + 1)` with `q' + 1 < B`: `q'` to each slot, one more to all slots but the last, and one more to the
    -- slot `0`
    subst hρ
    rw [add_zero] at hm0 hm hmB ⊢
    obtain ⟨q', rfl⟩ : ∃ q', q = q' + 1 := Nat.exists_eq_add_one_of_ne_zero (by
      rintro rfl
      exact hm0 (mul_zero r))
    have hqB : q' + 1 < B := Nat.lt_of_mul_lt_mul_left (lt_of_le_of_ne hm hmB)
    have hsub1 : range (r - 1) ⊆ range r := Finset.range_subset_range.2 (by omega)
    have hsub0 : ({0} : Finset ℕ) ⊆ range r :=
      Finset.singleton_subset_iff.2 (Finset.mem_range.2 (by omega))
    have hf : ∀ t, q' + (if t ∈ range (r - 1) then 1 else 0)
        + (if t ∈ ({0} : Finset ℕ) then 1 else 0)
        = if t = 0 then q' + 2 else if t < r - 1 then q' + 1 else q' := by
      intro t
      simp only [Finset.mem_range, Finset.mem_singleton]
      split_ifs <;> omega
    -- the numbers in the slots `0`, `1` and `r - 1`
    have hf0 : q' + (if 0 ∈ range (r - 1) then 1 else 0)
        + (if 0 ∈ ({0} : Finset ℕ) then 1 else 0) = q' + 2 := by
      rw [hf 0, ite_eq_left rfl]
    have hf1 : q' + (if 1 ∈ range (r - 1) then 1 else 0)
        + (if 1 ∈ ({0} : Finset ℕ) then 1 else 0) = q' + 1 := by
      rw [hf 1, ite_eq_right one_ne_zero, ite_eq_left (by omega)]
    have hfl : q' + (if r - 1 ∈ range (r - 1) then 1 else 0)
        + (if r - 1 ∈ ({0} : Finset ℕ) then 1 else 0) = q' := by
      rw [hf (r - 1), ite_eq_right (by omega), ite_eq_right (lt_irrefl _)]
    refine ⟨fun t => q' + (if t ∈ range (r - 1) then 1 else 0)
      + (if t ∈ ({0} : Finset ℕ) then 1 else 0), ?_, fun t => ?_, ?_,
      fun _ => ⟨1, by omega, ?_, ?_⟩⟩
    · rw [Finset.sum_add_distrib, Finset.sum_add_distrib, Finset.sum_const, Finset.card_range,
        smul_eq_mul, sum_indicator r _ hsub1, sum_indicator r _ hsub0, Finset.card_range,
        Finset.card_singleton, mul_add, mul_one]
      omega
    · change q' + (if t ∈ range (r - 1) then 1 else 0)
        + (if t ∈ ({0} : Finset ℕ) then 1 else 0) ≤ B
      rw [hf t]
      split_ifs <;> omega
    · change q' + (if 0 ∈ range (r - 1) then 1 else 0) + (if 0 ∈ ({0} : Finset ℕ) then 1 else 0)
        ≠ q' + (if r - 1 ∈ range (r - 1) then 1 else 0)
          + (if r - 1 ∈ ({0} : Finset ℕ) then 1 else 0)
      rw [hf0, hfl]
      omega
    · change q' + (if 1 ∈ range (r - 1) then 1 else 0)
        + (if 1 ∈ ({0} : Finset ℕ) then 1 else 0) ≠ 0
      rw [hf1]
      omega
    · change q' + (if 1 ∈ range (r - 1) then 1 else 0)
        + (if 1 ∈ ({0} : Finset ℕ) then 1 else 0) ≠ B
      rw [hf1]
      omega
  · -- `r ∤ m`: `q` to each slot and one more to the slots `0, …, ρ - 1`
    have hS : range ρ ⊆ range r := Finset.range_subset_range.2 hlt.le
    obtain ⟨h1, h2⟩ := dist_of_subset (by omega) q ρ B hm _ hS (Finset.card_range _)
    have hq : q + 1 ≤ B := by
      have h3 : r * q < r * B := by omega
      have h4 : q < B := Nat.lt_of_mul_lt_mul_left h3
      omega
    have hf : ∀ t, (q + if t ∈ range ρ then 1 else 0) = if t < ρ then q + 1 else q := by
      intro t
      simp only [Finset.mem_range]
      split_ifs <;> rfl
    refine ⟨fun t => q + if t ∈ range ρ then 1 else 0, h1, h2, ?_, fun hB => ?_⟩
    · change (q + if 0 ∈ range ρ then 1 else 0) ≠ (q + if r - 1 ∈ range ρ then 1 else 0)
      rw [hf 0, hf (r - 1)]
      split_ifs <;> omega
    · by_cases hqB : q + 1 = B
      · refine ⟨r - 1, by omega, ?_, ?_⟩
        · change (q + if r - 1 ∈ range ρ then 1 else 0) ≠ 0
          rw [hf (r - 1)]
          split_ifs <;> omega
        · change (q + if r - 1 ∈ range ρ then 1 else 0) ≠ B
          rw [hf (r - 1)]
          split_ifs <;> omega
      · refine ⟨0, by omega, ?_, ?_⟩
        · change (q + if 0 ∈ range ρ then 1 else 0) ≠ 0
          rw [hf 0]
          split_ifs <;> omega
        · change (q + if 0 ∈ range ρ then 1 else 0) ≠ B
          rw [hf 0]
          split_ifs <;> omega

/-- a sum against `Aux.push L v` is a sum over the points `L x` (as `TwoAux.sum_push` of `Pnq/Lift2.lean`) -/
theorem sum_push {N r : ℕ} [NeZero N] [Fact r.Prime] {L : ZMod N → ZMod (N * r)}
    (hL : ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L x) = x) (v : ZMod N → ℕ)
    (g : ZMod (N * r) → ℂ) :
    ∑ y, (Aux.push L v y : ℂ) * g y = ∑ x, (v x : ℂ) * g (L x) := by
  have h : ∀ y : ZMod (N * r), (Aux.push L v y : ℂ) * g y
      = ∑ x, if y = L x then (v x : ℂ) * g (L x) else 0 := by
    intro y
    rw [Finset.sum_eq_single (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)]
    · unfold Aux.push
      split_ifs with h1
      · rw [← h1]
      · simp
    · intro x _ hx
      rw [ite_eq_right]
      intro hy
      apply hx
      rw [hy, hL]
    · intro h
      exact absurd (Finset.mem_univ _) h
  rw [Finset.sum_congr rfl fun y _ => h y, Finset.sum_comm]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [Finset.sum_ite_eq' Finset.univ (L x), ite_eq_left (Finset.mem_univ _)]

/-- **The lift given by the numbers `a x t`**: the multiset on `ZMod (N * r)` that has `a x t` elements at the point
`L t x`, for each `x` in `ZMod N` and each slot `t < r` (meaningful when the `L t x`, `t < r`, are different lifts of
`x`). -/
def spread {N r : ℕ} (L : ℕ → ZMod N → ZMod (N * r)) (a : ZMod N → ℕ → ℕ) : ZMod (N * r) → ℕ :=
  fun y => ∑ t ∈ range r, Aux.push (L t) (fun x => a x t) y

/-- the reduction of `spread L a` has `∑_t a x t` elements at `x` -/
theorem reduce_spread {N r : ℕ} [NeZero N] [Fact r.Prime] {L : ℕ → ZMod N → ZMod (N * r)}
    (hL : ∀ t, t < r → ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L t x) = x)
    (a : ZMod N → ℕ → ℕ) (x : ZMod N) :
    reduce (spread L a) x = ∑ t ∈ range r, a x t := by
  have h : ∀ t ∈ range r, a x t = reduce (Aux.push (L t) fun x => a x t) x := fun t ht => by
    rw [Aux.reduce_push (hL t (Finset.mem_range.1 ht))]
  rw [Finset.sum_congr rfl h]
  change (∑ y : ZMod (N * r), if ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x
      then ∑ t ∈ range r, Aux.push (L t) (fun x => a x t) y else 0)
    = ∑ t ∈ range r, ∑ y : ZMod (N * r), if ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x
      then Aux.push (L t) (fun x => a x t) y else 0
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun y _ => ?_
  by_cases hy : ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x
  · simp only [ite_eq_left hy]
  · simp only [ite_eq_right hy, Finset.sum_const_zero]

/-- `spread L a` has `a x t` elements at the point `L t x`, when the lifts `L t x`, `t < r`, have the residues
`x mod r^k + t r^k` modulo `r^(k+1)` (so that they are different) -/
theorem spread_apply {N r k : ℕ} {L : ℕ → ZMod N → ZMod (N * r)}
    (hL : ∀ t, t < r → ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L t x) = x)
    (hβ : ∀ t, t < r → ∀ x, (L t x).val % r ^ (k + 1) = x.val % r ^ k + t * r ^ k)
    (a : ZMod N → ℕ → ℕ) {t : ℕ} (ht : t < r) (x : ZMod N) :
    spread L a (L t x) = a x t := by
  unfold spread
  rw [Finset.sum_eq_single t]
  · exact Aux.push_apply_self (hL t ht) _ x
  · intro t' ht' hne
    by_contra h0
    have h1 := (Aux.push_ne_zero h0).1
    rw [hL t ht x] at h1
    have h2 := hβ t ht x
    rw [h1, hβ t' (Finset.mem_range.1 ht') x] at h2
    exact hne (Nat.eq_of_mul_eq_mul_right (pow_pos (by omega : 0 < r) k) (by omega))
  · intro h
    exact absurd (Finset.mem_range.2 ht) h

/-- every multiplicity of `spread L a` is `0` or one of the numbers `a x t`, `t < r` -/
theorem spread_eq_zero_or {N r k : ℕ} {L : ℕ → ZMod N → ZMod (N * r)}
    (hL : ∀ t, t < r → ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L t x) = x)
    (hβ : ∀ t, t < r → ∀ x, (L t x).val % r ^ (k + 1) = x.val % r ^ k + t * r ^ k)
    (a : ZMod N → ℕ → ℕ) (y : ZMod (N * r)) :
    spread L a y = 0 ∨ ∃ t, t < r ∧
      spread L a y = a (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y) t := by
  by_cases h : ∃ t ∈ range r, y = L t (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)
  · obtain ⟨t, ht, hy⟩ := h
    have h1 := spread_apply hL hβ a (Finset.mem_range.1 ht)
      (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)
    rw [← hy] at h1
    exact Or.inr ⟨t, Finset.mem_range.1 ht, h1⟩
  · left
    unfold spread
    refine Finset.sum_eq_zero fun t ht => ?_
    by_contra h0
    exact h ⟨t, ht, (Aux.push_ne_zero h0).1⟩

/-- a sum against `spread L a` is a sum over the points `L t x` -/
theorem sum_spread {N r : ℕ} [NeZero N] [Fact r.Prime] {L : ℕ → ZMod N → ZMod (N * r)}
    (hL : ∀ t, t < r → ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L t x) = x)
    (a : ZMod N → ℕ → ℕ) (g : ZMod (N * r) → ℂ) :
    ∑ y, (spread L a y : ℂ) * g y = ∑ x, ∑ t ∈ range r, (a x t : ℂ) * g (L t x) := by
  have h : ∀ y : ZMod (N * r), (spread L a y : ℂ) * g y
      = ∑ t ∈ range r, (Aux.push (L t) (fun x => a x t) y : ℂ) * g y := by
    intro y
    unfold spread
    rw [Nat.cast_sum, Finset.sum_mul]
  calc ∑ y, (spread L a y : ℂ) * g y
      = ∑ y, ∑ t ∈ range r, (Aux.push (L t) (fun x => a x t) y : ℂ) * g y :=
        Finset.sum_congr rfl fun y _ => h y
    _ = ∑ t ∈ range r, ∑ y, (Aux.push (L t) (fun x => a x t) y : ℂ) * g y := Finset.sum_comm
    _ = ∑ t ∈ range r, ∑ x, (a x t : ℂ) * g (L t x) :=
        Finset.sum_congr rfl fun t ht => sum_push (hL t (Finset.mem_range.1 ht)) _ g
    _ = ∑ x, ∑ t ∈ range r, (a x t : ℂ) * g (L t x) := Finset.sum_comm

/-- **One step.**  `r` an odd prime, `w` a multiset on `ZMod N` with every multiplicity at most `r B`, and `x₁` an
element of it whose multiplicity is not `r B`.  Then `w` is the reduction of a multiset on `ZMod (N * r)` with every
multiplicity at most `B`, whose mask is divisible by no `Φ_d` with `d ∣ N * r`, `d ∤ N`, and which, if `B ≥ 2`, has an
element whose multiplicity is not `B`.  (With `N = r^k N'`, `r ∤ N'`: the copies of `x` are dealt to its `r` lifts, the
lift in the slot `t` being the one with residue `x mod r^k + t r^k` modulo `r^(k+1)`; the slots `0` and `r - 1` get equally
many copies of every `x ≠ x₁`, and different numbers of copies of `x₁`.  By the criterion a new divisor would make the sum of
`a x 0 ω^x` over the class of `x₁` modulo `r^k` equal to that of `a x (r - 1) ω^x`; but they differ by a nonzero multiple of
`ω^x₁`.) -/
theorem exists_step {N r : ℕ} [NeZero N] [Fact r.Prime] (hr2 : r ≠ 2) (B : ℕ) (w : ZMod N → ℕ)
    (hle : ∀ x, w x ≤ r * B) (x₁ : ZMod N) (hx0 : w x₁ ≠ 0) (hx1 : w x₁ ≠ r * B) :
    ∃ w₁ : ZMod (N * r) → ℕ, reduce w₁ = w ∧
      (∀ d, d ∣ N * r → ¬ d ∣ N → ¬ cyclotomic d ℤ ∣ maskW w₁) ∧
      (∀ y, w₁ y ≤ B) ∧ (2 ≤ B → ∃ y, w₁ y ≠ 0 ∧ w₁ y ≠ B) := by
  have hrp : r.Prime := Fact.out
  have hr3 : 3 ≤ r := by
    have := hrp.two_le
    omega
  obtain ⟨k, N', hN', hN⟩ := Nat.exists_eq_pow_mul_and_not_dvd (NeZero.ne N) r hrp.ne_one
  have hP : 0 < r ^ k := pow_pos hrp.pos k
  -- the lift of each element in each slot
  have hsec : ∀ t, ∃ L : ZMod N → ZMod (N * r), t < r →
      (∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L x) = x) ∧
        ∀ x, (L x).val % r ^ (k + 1) = x.val % r ^ k + t * r ^ k := by
    intro t
    by_cases ht : t < r
    · obtain ⟨L, h1, h2⟩ := Aux.exists_section (N := N) (r := r) k N' hN hN' t (by omega)
      exact ⟨L, fun _ => ⟨h1, h2⟩⟩
    · exact ⟨fun _ => 0, fun h => absurd h ht⟩
  choose L hL using hsec
  have hL1 : ∀ t, t < r → ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L t x) = x :=
    fun t ht => (hL t ht).1
  have hL2 : ∀ t, t < r → ∀ x, (L t x).val % r ^ (k + 1) = x.val % r ^ k + t * r ^ k :=
    fun t ht => (hL t ht).2
  -- the numbers of copies
  have ha : ∀ x : ZMod N, ∃ f : ℕ → ℕ, ∑ t ∈ range r, f t = w x ∧ (∀ t, f t ≤ B) ∧
      (x ≠ x₁ → f 0 = f (r - 1)) ∧
      (x = x₁ → f 0 ≠ f (r - 1) ∧ (2 ≤ B → ∃ t, t < r ∧ f t ≠ 0 ∧ f t ≠ B)) := by
    intro x
    by_cases hx : x = x₁
    · obtain ⟨f, hf1, hf2, hf3, hf4⟩ := exists_dist_ne hr3 (w x) B (by rw [hx]; exact hx0) (hle x)
        (by rw [hx]; exact hx1)
      exact ⟨f, hf1, hf2, fun h => absurd hx h, fun _ => ⟨hf3, hf4⟩⟩
    · obtain ⟨f, hf1, hf2, hf3⟩ := exists_dist_eq hr3 (w x) B (hle x)
      exact ⟨f, hf1, hf2, fun _ => hf3, fun h => absurd h hx⟩
  choose a ha1 ha2 ha3 ha4 using ha
  refine ⟨spread L a, ?_, fun d hd hnd hdvd => ?_, fun y => ?_, fun hB => ?_⟩
  · -- the reduction is `w`
    funext x
    rw [reduce_spread hL1 a x, ha1 x]
  · -- no new cyclotomic divisor
    have hd' : d ∣ r ^ k * N' * r := by
      rw [← hN]
      exact hd
    have hnd' : ¬ d ∣ r ^ k * N' := by
      rw [← hN]
      exact hnd
    obtain ⟨e, he0, he, rfl⟩ := Aux.exists_eq_mul_pow hrp hN' hd' hnd'
    have heN' : e ∣ N' := by
      have h : r ^ k * N' * r = N' * r ^ (k + 1) := by ring
      rw [h] at hd'
      exact Nat.dvd_of_mul_dvd_mul_right (pow_pos hrp.pos _) hd'
    have heN : e ∣ N := heN'.trans ⟨r ^ k, by rw [hN, mul_comm]⟩
    obtain ⟨ω, hω⟩ : ∃ ω : ℂ, IsPrimitiveRoot ω e := ⟨_, Complex.isPrimitiveRoot_exp e he0⟩
    have hωN : ω ^ N = 1 := by
      obtain ⟨f, hf⟩ := heN
      rw [hf, pow_mul, hω.pow_eq_one, one_pow]
    -- `ω^y = ω^x` when `y` lifts `x`
    have hωL : ∀ t, t < r → ∀ x : ZMod N, ω ^ (L t x).val = ω ^ x.val := by
      intro t ht x
      have m3 : (L t x).val % N = x.val := by
        rw [← Aux.val_castHom, hL1 t ht x]
      rw [← m3]
      exact pow_eq_pow_mod _ hωN
    have hmod : ∀ x : ZMod N, x.val % r ^ k < r ^ k := fun x => Nat.mod_lt _ hP
    -- the criterion, for the class of `x₁`
    have hkey := shift_sum_eq (spread L a) hrp k e he0 he hdvd hω (x₁.val % r ^ k)
    -- the left side: only the slot `r - 1` counts
    have hleft : ∀ x : ZMod N, ∑ t ∈ range r, (a x t : ℂ) *
        (if ((L t x).val % r ^ (k + 1) + r ^ k) % r ^ (k + 1) = x₁.val % r ^ k
          then ω ^ (L t x).val else 0)
        = (a x (r - 1) : ℂ) * (if x.val % r ^ k = x₁.val % r ^ k then ω ^ x.val else 0) := by
      intro x
      rw [Finset.sum_eq_single (r - 1)]
      · rw [hL2 (r - 1) (by omega) x, hωL (r - 1) (by omega) x,
          if_congr ((shift_mod_eq_iff (hmod x) (hmod x₁) (by omega : r - 1 < r)).trans
            (and_iff_right rfl)) rfl rfl]
      · intro t ht hne
        rw [hL2 t (Finset.mem_range.1 ht) x, ite_eq_right, mul_zero]
        intro h
        exact hne ((shift_mod_eq_iff (hmod x) (hmod x₁) (Finset.mem_range.1 ht)).1 h).1
      · intro h
        exact absurd (Finset.mem_range.2 (by omega)) h
    -- the right side: only the slot `0` counts
    have hright : ∀ x : ZMod N, ∑ t ∈ range r, (a x t : ℂ) *
        (if (L t x).val % r ^ (k + 1) = x₁.val % r ^ k then ω ^ (L t x).val else 0)
        = (a x 0 : ℂ) * (if x.val % r ^ k = x₁.val % r ^ k then ω ^ x.val else 0) := by
      intro x
      rw [Finset.sum_eq_single 0]
      · rw [hL2 0 (by omega) x, hωL 0 (by omega) x,
          if_congr ((slot_eq_iff (hmod x₁)).trans (and_iff_right rfl)) rfl rfl]
      · intro t ht hne
        rw [hL2 t (Finset.mem_range.1 ht) x, ite_eq_right, mul_zero]
        intro h
        exact hne ((slot_eq_iff (hmod x₁)).1 h).1
      · intro h
        exact absurd (Finset.mem_range.2 (by omega)) h
    rw [sum_spread hL1 a, sum_spread hL1 a, Finset.sum_congr rfl fun x _ => hleft x,
      Finset.sum_congr rfl fun x _ => hright x] at hkey
    -- the two sides differ by `(a x₁ 0 - a x₁ (r - 1)) ω^x₁`
    have hdiff : ∑ x : ZMod N, ((a x 0 : ℂ) - (a x (r - 1) : ℂ)) *
        (if x.val % r ^ k = x₁.val % r ^ k then ω ^ x.val else 0) = 0 := by
      simp only [sub_mul]
      rw [Finset.sum_sub_distrib, hkey, sub_self]
    rw [Finset.sum_eq_single x₁] at hdiff
    · rw [ite_eq_left rfl] at hdiff
      rcases mul_eq_zero.1 hdiff with h | h
      · exact (ha4 x₁ rfl).1 (Nat.cast_injective (sub_eq_zero.1 h))
      · exact pow_ne_zero _ (hω.ne_zero he0) h
    · intro x _ hx
      rw [ha3 x hx, sub_self, zero_mul]
    · intro h
      exact absurd (Finset.mem_univ _) h
  · -- every multiplicity is at most `B`
    rcases spread_eq_zero_or hL1 hL2 a y with h | ⟨t, -, h⟩
    · rw [h]
      exact Nat.zero_le _
    · rw [h]
      exact ha2 _ t
  · -- an element whose multiplicity is not `B`
    obtain ⟨t, ht, h1, h2⟩ := (ha4 x₁ rfl).2 hB
    refine ⟨L t x₁, ?_, ?_⟩
    · rw [spread_apply hL1 hL2 a ht x₁]
      exact h1
    · rw [spread_apply hL1 hL2 a ht x₁]
      exact h2

/-- reduction in two stages: the sizes of the fibres of `ZMod M₂ → ZMod N` are the sums, over the fibres of
`ZMod M₁ → ZMod N`, of the sizes of the fibres of `ZMod M₂ → ZMod M₁` -/
theorem fibre_comp {N M₁ M₂ : ℕ} [NeZero M₁] [NeZero M₂] (h₀ : N ∣ M₁) (h₁ : M₁ ∣ M₂) (h : N ∣ M₂)
    (v : ZMod M₂ → ℕ) (x : ZMod N) :
    ∑ y' : ZMod M₁, (if ZMod.castHom h₀ (ZMod N) y' = x
        then ∑ y : ZMod M₂, (if ZMod.castHom h₁ (ZMod M₁) y = y' then v y else 0) else 0) =
      ∑ y : ZMod M₂, if ZMod.castHom h (ZMod N) y = x then v y else 0 := by
  have hc : ∀ y : ZMod M₂, ZMod.castHom h (ZMod N) y
      = ZMod.castHom h₀ (ZMod N) (ZMod.castHom h₁ (ZMod M₁) y) := fun y =>
    RingHom.congr_fun (RingHom.ext_zmod (ZMod.castHom h (ZMod N))
      ((ZMod.castHom h₀ (ZMod N)).comp (ZMod.castHom h₁ (ZMod M₁)))) y
  have h1 : ∀ y' : ZMod M₁, (if ZMod.castHom h₀ (ZMod N) y' = x
        then ∑ y : ZMod M₂, (if ZMod.castHom h₁ (ZMod M₁) y = y' then v y else 0) else 0)
      = ∑ y : ZMod M₂, (if ZMod.castHom h₀ (ZMod N) y' = x
        then (if ZMod.castHom h₁ (ZMod M₁) y = y' then v y else 0) else 0) := by
    intro y'
    by_cases hx : ZMod.castHom h₀ (ZMod N) y' = x
    · simp only [ite_eq_left hx]
    · simp only [ite_eq_right hx, Finset.sum_const_zero]
  rw [Finset.sum_congr rfl fun y' _ => h1 y', Finset.sum_comm]
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [Finset.sum_eq_single (ZMod.castHom h₁ (ZMod M₁) y)]
  · rw [ite_eq_left rfl, hc y]
  · intro y' _ hy'
    rw [ite_eq_right (Ne.symm hy'), ite_self]
  · intro h'
    exact absurd (Finset.mem_univ _) h'

/-- **`j` steps.**  `r` an odd prime, `M = N * r^j`, and `w` a multiset on `ZMod N` with every multiplicity at most
`r^(j+i)`, not every element having multiplicity `r^(j+i)`.  There is a multiset on `ZMod M` with every multiplicity at most
`r^i` (and, if `i ≥ 1`, not every element of multiplicity `r^i`), whose fibres over `ZMod N` have the sizes `w x`, and whose
mask is divisible by `Φ_d`, `d ∣ M`, exactly when `d ∣ N` and `Φ_d` divides the mask of `w`.  (Induction on `j`; the modulus
is a variable `M` with `M = N * r^j`, so that `ZMod (N * r^(j+1))` and `ZMod (N * r^j * r)` need no transport.) -/
theorem exists_multi_lift {N r : ℕ} [NeZero N] [Fact r.Prime] (hr2 : r ≠ 2) (j : ℕ) :
    ∀ (M : ℕ) [NeZero M] (hNM : N ∣ M), M = N * r ^ j → ∀ (i : ℕ) (w : ZMod N → ℕ),
      (∀ x, w x ≤ r ^ (j + i)) → (∃ x, w x ≠ 0 ∧ w x ≠ r ^ (j + i)) →
      ∃ w' : ZMod M → ℕ,
        (∀ x, ∑ y : ZMod M, (if ZMod.castHom hNM (ZMod N) y = x then w' y else 0) = w x) ∧
        (∀ d, d ∣ M → (cyclotomic d ℤ ∣ maskW w' ↔ d ∣ N ∧ cyclotomic d ℤ ∣ maskW w)) ∧
        (∀ y, w' y ≤ r ^ i) ∧ (i ≠ 0 → ∃ y, w' y ≠ 0 ∧ w' y ≠ r ^ i) := by
  have hrp : r.Prime := Fact.out
  induction j with
  | zero =>
    intro M _ hNM hM i w hle hne
    have hM' : M = N := by rw [hM, pow_zero, mul_one]
    subst hM'
    rw [zero_add] at hle hne
    refine ⟨w, fun x => ?_, fun d hd => ⟨fun h => ⟨hd, h⟩, fun h => h.2⟩, hle, fun _ => hne⟩
    have hid : ∀ y : ZMod M, ZMod.castHom hNM (ZMod M) y = y := fun y =>
      RingHom.congr_fun (RingHom.ext_zmod (ZMod.castHom hNM (ZMod M)) (RingHom.id _)) y
    simp only [hid]
    exact Fintype.sum_ite_eq' x w
  | succ j ih =>
    intro M _ hNM hM i w hle hne
    have hM' : M = N * r ^ j * r := by rw [hM, pow_succ, mul_assoc]
    subst hM'
    have : NeZero (N * r ^ j) := ⟨Nat.mul_ne_zero (NeZero.ne N) (pow_ne_zero j hrp.ne_zero)⟩
    have hexp : j + 1 + i = j + (i + 1) := by omega
    rw [hexp] at hle hne
    obtain ⟨w', hred', hdiv', hle', hne'⟩ :=
      ih (N * r ^ j) (Nat.dvd_mul_right N (r ^ j)) rfl (i + 1) w hle hne
    obtain ⟨x₁, hx0, hx1⟩ := hne' (Nat.succ_ne_zero i)
    have hpow : r ^ (i + 1) = r * r ^ i := pow_succ' r i
    obtain ⟨w'', hred'', hnew, hle'', hne''⟩ := exists_step (N := N * r ^ j) (r := r) hr2 (r ^ i) w'
      (fun y => by rw [← hpow]; exact hle' y) x₁ hx0 (by rw [← hpow]; exact hx1)
    refine ⟨w'', fun x => ?_, fun d hd => ?_, hle'', fun hi => hne'' (Nat.one_lt_pow hi hrp.one_lt)⟩
    · -- the sizes of the fibres
      rw [← hred' x, ← fibre_comp (Nat.dvd_mul_right N (r ^ j)) (Nat.dvd_mul_right (N * r ^ j) r)
        hNM w'' x]
      refine Finset.sum_congr rfl fun y' _ => ?_
      rw [← hred'']
      rfl
    · -- the divisors
      by_cases hdN : d ∣ N * r ^ j
      · rw [← hdiv' d hdN, ← hred'']
        exact (cyclotomic_dvd_reduce_iff w'' d hdN).symm
      · exact iff_of_false (hnew d hd hdN) fun h => hdN (Dvd.dvd.mul_right h.1 _)

end SetAux

/-- **Lifting to a set.** -/
theorem exists_set_lift {N r : ℕ} [NeZero N] [Fact r.Prime] (hr : r ≠ 2) (j : ℕ)
    (w : ZMod N → ℕ) (hle : ∀ x, w x ≤ r ^ j) (hne : ∃ x, w x ≠ 0 ∧ w x ≠ r ^ j) :
    ∃ A : Finset (ZMod (N * r ^ j)),
      (∀ x : ZMod N,
        (A.filter (fun y => ZMod.castHom (Nat.dvd_mul_right N (r ^ j)) (ZMod N) y = x)).card = w x) ∧
      ∀ d, d ∣ N * r ^ j →
        (Polynomial.cyclotomic d ℤ ∣ maskW (indW A) ↔ d ∣ N ∧ Polynomial.cyclotomic d ℤ ∣ maskW w) := by
  obtain ⟨w', hred, hdiv, hle', -⟩ := SetAux.exists_multi_lift hr j (N * r ^ j)
    (Nat.dvd_mul_right N (r ^ j)) rfl 0 w hle hne
  -- the multiplicities are `0` or `1`
  have h01 : ∀ y, w' y = 0 ∨ w' y = 1 := fun y => by
    have h := hle' y
    rw [pow_zero] at h
    omega
  -- the set of the elements
  obtain ⟨A, hA⟩ : ∃ A : Finset (ZMod (N * r ^ j)), ∀ y, y ∈ A ↔ w' y ≠ 0 :=
    ⟨Finset.univ.filter fun y => w' y ≠ 0, fun y => by
      rw [Finset.mem_filter, and_iff_right (Finset.mem_univ y)]⟩
  have hind : indW A = w' := by
    funext y
    unfold indW
    rcases h01 y with h | h
    · rw [ite_eq_right (fun hy => (hA y).1 hy h), h]
    · rw [ite_eq_left ((hA y).2 (by omega)), h]
  refine ⟨A, fun x => ?_, fun d hd => ?_⟩
  · -- the fibre of `A` over `x` has `w x` elements
    have h1 : ∑ y : ZMod (N * r ^ j),
          (if ZMod.castHom (Nat.dvd_mul_right N (r ^ j)) (ZMod N) y = x then w' y else 0)
        = ∑ y ∈ A,
          (if ZMod.castHom (Nat.dvd_mul_right N (r ^ j)) (ZMod N) y = x then w' y else 0) := by
      refine (Finset.sum_subset (Finset.subset_univ A) fun y _ hy => ?_).symm
      have h0 : w' y = 0 := by
        by_contra h
        exact hy ((hA y).2 h)
      rw [h0, ite_self]
    rw [← hred x, Finset.card_filter, h1]
    refine Finset.sum_congr rfl fun y hy => ?_
    have h2 : w' y = 1 := by
      rcases h01 y with h | h
      · exact absurd h ((hA y).1 hy)
      · exact h
    rw [h2]
  · rw [hind]
    exact hdiv d hd

end Lift

end Pnq
