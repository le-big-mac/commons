/-
Lifting.  For an odd prime `r`, a nonempty multiset on `ZMod N` can be lifted to `ZMod (N * r)` with the same number of elements and
exactly the same cyclotomic divisors of its mask polynomial: every `Φ_d` with `d ∣ N` divides the one mask exactly when it divides
the other, and no `Φ_d` with `d ∣ N * r`, `d ∤ N` divides the lifted one.  Reduction modulo `N` goes the other way.  So the sizes
of the multisets with exactly a given pattern of divisors of `N` are the same on `ZMod N` and on `ZMod (N * r)`.
(Definitions and statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  The lemma on lifts is
due to a fresh instance that read a note of mine; the proof on paper is by counting roots.)
-/
import Pnq.Weighted
import Pnq.Lift1

open Finset

namespace Pnq

namespace Lift

variable {N r : ℕ} [NeZero N] [Fact r.Prime]

instance instNeZeroMul : NeZero (N * r) :=
  ⟨Nat.mul_ne_zero (NeZero.ne N) (Fact.out : r.Prime).ne_zero⟩

/-- Reduction modulo `N` of a multiset on `ZMod (N * r)`: the multiplicity of `x` is the number of elements, counted with
multiplicity, whose residue modulo `N` is `x`. -/
def reduce (w' : ZMod (N * r) → ℕ) : ZMod N → ℕ :=
  fun x => ∑ y : ZMod (N * r), if ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x then w' y else 0

/-- reduction keeps the number of elements -/
theorem sum_reduce (w' : ZMod (N * r) → ℕ) : ∑ x, reduce w' x = ∑ y, w' y := by
  unfold reduce
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun y _ => Fintype.sum_ite_eq _ fun _ => w' y

namespace Aux

/-- the residue modulo `N` of `y`, as a number -/
theorem val_castHom (y : ZMod (N * r)) :
    (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y).val = y.val % N := by
  rw [ZMod.castHom_apply, ← ZMod.natCast_val, ZMod.val_natCast]

/-- the mask of the reduced multiset: the exponents are reduced modulo `N` -/
theorem maskW_reduce (w' : ZMod (N * r) → ℕ) :
    maskW (reduce w') =
      ∑ y : ZMod (N * r), Polynomial.C (w' y : ℤ) * Polynomial.X ^ (y.val % N) := by
  have h : ∀ x : ZMod N, Polynomial.C ((reduce w' x : ℕ) : ℤ) * Polynomial.X ^ x.val
      = ∑ y : ZMod (N * r), if ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x
          then Polynomial.C (w' y : ℤ) * Polynomial.X ^ (y.val % N) else 0 := by
    intro x
    unfold reduce
    rw [Nat.cast_sum, map_sum, Finset.sum_mul]
    refine Finset.sum_congr rfl fun y _ => ?_
    split_ifs with hy
    · rw [← val_castHom, hy]
    · simp
  rw [maskW, Finset.sum_congr rfl fun x _ => h x, Finset.sum_comm]
  refine Finset.sum_congr rfl fun y _ => ?_
  simp

end Aux

/-- for `d ∣ N`, `Φ_d` divides the mask of the reduced multiset exactly when it divides the mask of the multiset -/
theorem cyclotomic_dvd_reduce_iff (w' : ZMod (N * r) → ℕ) (d : ℕ) (hd : d ∣ N) :
    Polynomial.cyclotomic d ℤ ∣ maskW (reduce w') ↔ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  have h1 : Polynomial.cyclotomic d ℤ ∣ (Polynomial.X ^ N - 1 : Polynomial ℤ) := by
    obtain ⟨c, hc⟩ := hd
    rw [hc]
    exact (Polynomial.cyclotomic.dvd_X_pow_sub_one d ℤ).trans
      (pow_one_sub_dvd_pow_mul_sub_one Polynomial.X d c)
  have h2 : (Polynomial.X ^ N - 1 : Polynomial ℤ) ∣ maskW (reduce w') - maskW w' := by
    rw [Aux.maskW_reduce, maskW, ← Finset.sum_sub_distrib]
    refine Finset.dvd_sum fun y _ => ?_
    obtain ⟨g, hg⟩ := sub_one_dvd_pow_sub_one ((Polynomial.X : Polynomial ℤ) ^ N) (y.val / N)
    have h3 : (Polynomial.X : Polynomial ℤ) ^ y.val
        = Polynomial.X ^ (y.val % N) * (Polynomial.X ^ N) ^ (y.val / N) := by
      rw [← pow_mul, ← pow_add, Nat.mod_add_div]
    refine ⟨-(Polynomial.C (w' y : ℤ) * Polynomial.X ^ (y.val % N) * g), ?_⟩
    rw [h3]
    linear_combination (-(Polynomial.C (w' y : ℤ) * Polynomial.X ^ (y.val % N))) * hg
  exact dvd_iff_dvd_of_dvd_sub (h1.trans h2)

namespace Aux

/-- the multiset on `ZMod (N * r)` that has `v x` elements at the point `L x`, for each `x`, and nothing elsewhere
(meaningful when `L x` has residue `x` modulo `N`) -/
def push (L : ZMod N → ZMod (N * r)) (v : ZMod N → ℕ) : ZMod (N * r) → ℕ :=
  fun y => if y = L (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)
    then v (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y) else 0

omit [NeZero N] [Fact r.Prime] in
theorem push_ne_zero {L : ZMod N → ZMod (N * r)} {v : ZMod N → ℕ} {y : ZMod (N * r)}
    (h : push L v y ≠ 0) :
    y = L (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y) ∧
      v (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y) ≠ 0 := by
  unfold push at h
  split_ifs at h with h1
  · exact ⟨h1, h⟩
  · exact absurd rfl h

omit [NeZero N] [Fact r.Prime] in
theorem push_apply_self {L : ZMod N → ZMod (N * r)}
    (hL : ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L x) = x) (v : ZMod N → ℕ) (x : ZMod N) :
    push L v (L x) = v x := by
  unfold push
  rw [hL x, ite_eq_left rfl]

/-- the reduction of `push L v` is `v` -/
theorem reduce_push {L : ZMod N → ZMod (N * r)}
    (hL : ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L x) = x) (v : ZMod N → ℕ) :
    reduce (push L v) = v := by
  funext x
  unfold reduce
  rw [Finset.sum_eq_single (L x)]
  · rw [ite_eq_left (hL x), push_apply_self hL]
  · intro y _ hy
    by_cases h : ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x
    · rw [ite_eq_left h]
      by_contra h0
      have h1 := (push_ne_zero h0).1
      rw [h] at h1
      exact hy h1
    · rw [ite_eq_right h]
  · intro h
    exact absurd (Finset.mem_univ _) h

/-- reduction is additive -/
theorem reduce_add (a b : ZMod (N * r) → ℕ) : reduce (a + b) = reduce a + reduce b := by
  funext x
  simp only [reduce, Pi.add_apply]
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun y _ => ?_
  split_ifs <;> rfl

theorem add_ne_zero_cases {a b : ℕ} (h : a + b ≠ 0) : a ≠ 0 ∨ b ≠ 0 := by
  omega

/-- For `N = r^k N'`, `r ∤ N'`, and `t < r`: a choice, for every `x` in `ZMod N`, of an element of `ZMod (N * r)` with
residue `x` modulo `N` whose residue modulo `r^(k+1)` is `x mod r^k + t r^k`. -/
theorem exists_section (k N' : ℕ) (hN : N = r ^ k * N') (hN' : ¬ r ∣ N') (t : ℕ) (ht : t + 1 ≤ r) :
    ∃ L : ZMod N → ZMod (N * r),
      (∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L x) = x) ∧
        ∀ x, (L x).val % r ^ (k + 1) = x.val % r ^ k + t * r ^ k := by
  have hr : r.Prime := Fact.out
  have key : ∀ x : ZMod N, ∃ y : ZMod (N * r),
      ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x ∧
        y.val % r ^ (k + 1) = x.val % r ^ k + t * r ^ k := by
    intro x
    obtain ⟨c, hc1, hc2⟩ := exists_crt hr k hN' x.val t ht
    rw [← hN] at hc1
    refine ⟨(c : ZMod (N * r)), ?_, ?_⟩
    · rw [map_natCast]
      exact ((ZMod.natCast_eq_natCast_iff c x.val N).2 hc1).trans (ZMod.natCast_zmod_val x)
    · have hdvd : r ^ (k + 1) ∣ N * r := ⟨N', by rw [hN]; ring⟩
      rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ hdvd, hc2]
  choose L hL1 hL2 using key
  exact ⟨L, hL1, hL2⟩

/-- **The lift.**  `r` an odd prime, `N = r^k N'`, `r ∤ N'`.  A multiset `w` on `ZMod N` with an element `x₀` is the
reduction of a multiset `w'` on `ZMod (N * r)` whose elements all have residue modulo `r^(k+1)` below `(r - 1) r^k`, one
of them being the only one with its residue.  (Every element goes to its lift with residue below `r^k`, except one copy
of `x₀`, which goes to its lift with residue in `[r^k, 2 r^k)`.) -/
theorem exists_lift_aux (hr2 : r ≠ 2) (k N' : ℕ) (hN : N = r ^ k * N') (hN' : ¬ r ∣ N')
    (w : ZMod N → ℕ) (x₀ : ZMod N) (hx₀ : w x₀ ≠ 0) :
    ∃ w' : ZMod (N * r) → ℕ, reduce w' = w ∧
      (∀ y, w' y ≠ 0 → y.val % r ^ (k + 1) < (r - 1) * r ^ k) ∧
      ∃ y₀, w' y₀ ≠ 0 ∧ ∀ y, w' y ≠ 0 → y.val % r ^ (k + 1) = y₀.val % r ^ (k + 1) → y = y₀ := by
  have hr : r.Prime := Fact.out
  have hr3 : 3 ≤ r := by
    have := hr.two_le
    omega
  obtain ⟨L₀, hL₀, hβ₀⟩ := exists_section (N := N) (r := r) k N' hN hN' 0 (by omega)
  obtain ⟨L₁, hL₁, hβ₁⟩ := exists_section (N := N) (r := r) k N' hN hN' 1 (by omega)
  have hrk : 0 < r ^ k := pow_pos hr.pos k
  have hb1 : r ^ k ≤ (r - 1) * r ^ k := Nat.le_mul_of_pos_left _ (by omega)
  have hb2 : 2 * r ^ k ≤ (r - 1) * r ^ k := Nat.mul_le_mul_right _ (by omega)
  have hmod : ∀ x : ZMod N, x.val % r ^ k < r ^ k := fun x => Nat.mod_lt _ hrk
  refine ⟨push L₀ (Function.update w x₀ (w x₀ - 1)) + push L₁ (Pi.single x₀ 1), ?_, ?_, L₁ x₀, ?_, ?_⟩
  · -- the reduction is `w`
    rw [reduce_add, reduce_push hL₀, reduce_push hL₁]
    funext x
    by_cases hx : x = x₀
    · rw [hx, Pi.add_apply, Function.update_self, Pi.single_eq_same]
      omega
    · rw [Pi.add_apply, Function.update_of_ne hx, Pi.single_eq_of_ne hx, add_zero]
  · -- every residue modulo `r^(k+1)` is below `(r - 1) r^k`
    intro y hy
    rw [Pi.add_apply] at hy
    rcases add_ne_zero_cases hy with h | h
    · have h1 := (push_ne_zero h).1
      have hβ := hβ₀ (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)
      rw [← h1] at hβ
      rw [hβ, zero_mul, add_zero]
      exact (hmod _).trans_le hb1
    · have h1 := (push_ne_zero h).1
      have hβ := hβ₁ (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)
      rw [← h1] at hβ
      rw [hβ, one_mul]
      have := hmod (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)
      omega
  · -- the moved element is there
    rw [Pi.add_apply, push_apply_self hL₁, Pi.single_eq_same]
    omega
  · -- and it is the only one with its residue
    intro y hy hβy
    rw [hβ₁ x₀, one_mul] at hβy
    rw [Pi.add_apply] at hy
    rcases add_ne_zero_cases hy with h | h
    · exfalso
      have h1 := (push_ne_zero h).1
      have hβ := hβ₀ (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)
      rw [← h1, zero_mul, add_zero] at hβ
      have h4 : x₀.val % r ^ k + r ^ k < r ^ k := by
        rw [← hβy, hβ]
        exact hmod _
      exact Nat.not_lt.2 (Nat.le_add_left _ _) h4
    · obtain ⟨h1, h2⟩ := push_ne_zero h
      have h3 : ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x₀ := by
        by_contra hne
        exact h2 (Pi.single_eq_of_ne hne 1)
      rw [h3] at h1
      exact h1

theorem exists_ne_zero_of_sum_pos {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (h : 0 < ∑ x, w x) :
    ∃ x, w x ≠ 0 := by
  by_contra h'
  have h0 : ∀ x, w x = 0 := fun x => by_contra fun hx => h' ⟨x, hx⟩
  rw [Finset.sum_eq_zero fun x _ => h0 x] at h
  exact lt_irrefl 0 h

end Aux

/-- **The lemma on lifts.** If `r` is odd, a nonempty multiset on `ZMod N` is the reduction of a multiset on `ZMod (N * r)`
whose mask is divisible by no `Φ_d` with `d ∣ N * r`, `d ∤ N`. -/
theorem exists_lift (hr : r ≠ 2) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * r) → ℕ, reduce w' = w ∧
      ∀ d, d ∣ N * r → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  have hrp : r.Prime := Fact.out
  obtain ⟨x₀, hx₀⟩ := hw
  obtain ⟨k, N', hN', hN⟩ := Nat.exists_eq_pow_mul_and_not_dvd (NeZero.ne N) r hrp.ne_one
  obtain ⟨w', hred, h1, y₀, hy₀, h2⟩ := Aux.exists_lift_aux hr k N' hN hN' w x₀ hx₀
  refine ⟨w', hred, fun d hd hnd => ?_⟩
  have hd' : d ∣ r ^ k * N' * r := by
    rw [← hN]
    exact hd
  have hnd' : ¬ d ∣ r ^ k * N' := by
    rw [← hN]
    exact hnd
  obtain ⟨e, he0, he, rfl⟩ := Aux.exists_eq_mul_pow hrp hN' hd' hnd'
  exact Aux.not_cyclotomic_dvd_of_single w' hrp k e he0 he h1 y₀ hy₀ h2

/-- **Sizes are the same.** If `r` is odd and `P` is a set of divisors of `N`, the numbers of elements of the nonempty
multisets on `ZMod (N * r)` whose mask is divisible by `Φ_d`, for `d ∣ N * r`, `d ≠ 1`, exactly when `d ∈ P`, are the numbers
of elements of the nonempty multisets on `ZMod N` whose mask is divisible by `Φ_d`, for `d ∣ N`, `d ≠ 1`, exactly when
`d ∈ P`. -/
theorem sizes_eq (hr : r ≠ 2) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * r) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * r → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  ext s
  simp only [Set.mem_ofPred_eq]
  constructor
  · rintro ⟨w', hs, hpos, hpat⟩
    refine ⟨reduce w', (sum_reduce w').trans hs, hpos, fun d hd hd1 => ?_⟩
    rw [cyclotomic_dvd_reduce_iff w' d hd]
    exact hpat d (Dvd.dvd.mul_right hd r) hd1
  · rintro ⟨w, hs, hpos, hpat⟩
    have hw : ∃ x, w x ≠ 0 := Aux.exists_ne_zero_of_sum_pos w (hs ▸ hpos)
    obtain ⟨w', hred, hnew⟩ := exists_lift hr w hw
    subst hred
    refine ⟨w', (sum_reduce w').symm.trans hs, hpos, fun d hd hd1 => ?_⟩
    by_cases hdN : d ∣ N
    · rw [← cyclotomic_dvd_reduce_iff w' d hdN]
      exact hpat d hdN hd1
    · exact iff_of_false (hnew d hd hdN) fun h => hdN (hP d h)

end Lift

end Pnq
