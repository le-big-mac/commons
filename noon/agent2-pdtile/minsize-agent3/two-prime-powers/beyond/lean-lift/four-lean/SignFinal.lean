/-
The statement on signs for every odd `n`, and the lifting along the prime 2 for every `N`: the final statements.
The statement on signs for multisets on `ZMod n`, `n` odd (`Lift.exists_signs` of `Pnq/Sign.lean` with `p^a * q^b`
replaced by an odd `n`), the lemma on lifts for the prime 2 for every `N`, and the equality of the sets of sizes on
`ZMod (N * 2)` and on `ZMod N`.  All three from A1 (`exists_not_badAt` of `Pnq/SignAll.lean`).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignAll
import Pnq.Lift2

open Finset

namespace Pnq

/-! Helper lemmas live in the namespace `Pnq.FinalAux`, so that their names cannot clash with those of the other
files of the project. -/

namespace FinalAux

/-- among the values of `f`, the number of `true` and the number of `false` add up to the number of points -/
theorem card_true_add_card_false {α : Type*} [Fintype α] (f : α → Bool) :
    (Finset.univ.filter fun j => f j = true).card + (Finset.univ.filter fun j => f j = false).card
      = Fintype.card α := by
  rw [Finset.card_filter, Finset.card_filter, ← Finset.sum_add_distrib, Fintype.card_eq_sum_ones]
  refine Finset.sum_congr rfl fun j _ => ?_
  cases f j <;> simp

/-- the sum of the signs `sg (f j)` is the number of `true` minus the number of `false` -/
theorem sum_sg {α : Type*} [Fintype α] (f : α → Bool) :
    ∑ j, sg (f j) = ((Finset.univ.filter fun j => f j = true).card : ℤ)
      - ((Finset.univ.filter fun j => f j = false).card : ℤ) := by
  rw [Finset.card_filter, Finset.card_filter, Nat.cast_sum, Nat.cast_sum, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun j _ => ?_
  cases f j <;> simp [sg]

/-- The elements of a multiset `w` on `ZMod n`, one point `⟨x, j⟩` with `j < w x` for each element, with the
exponent `x.val`: the signed mask of a signing `ε` is `maskW u - maskW v`, where `u x` and `v x` are the numbers of
the elements at `x` with the sign `+` and with the sign `-`. -/
theorem P_sigma {n : ℕ} [NeZero n] (w : ZMod n → ℕ) (ε : (Σ x : ZMod n, Fin (w x)) → Bool) :
    P (fun k : Σ x : ZMod n, Fin (w x) => k.1.val) ε
      = maskW (fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card)
        - maskW (fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card) := by
  unfold P maskW
  rw [Fintype.sum_sigma, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun x _ => ?_
  change ∑ j : Fin (w x), Polynomial.C (sg (ε ⟨x, j⟩)) * Polynomial.X ^ x.val
      = Polynomial.C (((Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card : ℕ) : ℤ)
          * Polynomial.X ^ x.val
        - Polynomial.C (((Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card : ℕ) : ℤ)
          * Polynomial.X ^ x.val
  rw [← Finset.sum_mul, ← map_sum, sum_sg, map_sub, sub_mul]

end FinalAux

/-- **The statement on signs for every odd `n`** (the first final statement of the plan).  The elements of a nonempty
multiset `w` on `ZMod n`, `n` odd, can be split into two parts `u`, `v` so that no `Φ_d`, `d ∣ n`, divides
`maskW u - maskW v`. -/
theorem exists_signs_odd (n : ℕ) [NeZero n] (hn : ¬ 2 ∣ n) (w : ZMod n → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  obtain ⟨x₀, hx₀⟩ := hw
  -- one point for each element of the multiset
  have hne : Nonempty (Σ x : ZMod n, Fin (w x)) := ⟨⟨x₀, ⟨0, Nat.pos_of_ne_zero hx₀⟩⟩⟩
  obtain ⟨ε, hε⟩ := exists_not_badAt n hn (fun k : Σ x : ZMod n, Fin (w x) => k.1.val)
  refine ⟨fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card,
    fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card,
    fun x => ?_, fun d hd hdvd => hε d hd ?_⟩
  · change (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card
      + (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card = w x
    rw [FinalAux.card_true_add_card_false, Fintype.card_fin]
  · unfold BadAt
    rw [FinalAux.P_sigma]
    exact hdvd

/-- **The lemma on lifts for the prime 2, for every `N`** (the second final statement of the plan).  A nonempty
multiset `w` on `ZMod N` is the reduction of a multiset `w'` on `ZMod (N * 2)` whose mask is divisible by no `Φ_d`
with `d ∣ N * 2`, `d ∤ N`. -/
theorem exists_lift_two_all {N : ℕ} [NeZero N] (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, Lift.reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  -- `N = 2^k * N'` with `N'` odd
  obtain ⟨k, N', hodd, hN⟩ := Nat.exists_eq_two_pow_mul_odd (NeZero.ne N)
  have hN' : ¬ 2 ∣ N' := fun h => (Nat.not_even_iff_odd.2 hodd) (even_iff_two_dvd.2 h)
  have hN'0 : NeZero N' := ⟨fun h => hN' (h ▸ dvd_zero 2)⟩
  exact Lift.TwoAux.exists_lift_two_aux k N' hN hN'
    (fun B hB => exists_signs_odd N' hN' B hB) w hw

/-- **Sizes are the same, for the prime 2, for every `N`** (`Lift.sizes_eq_two` of `Pnq/Lift2.lean` without its
hypotheses on the odd part of `N`).  For a set `P` of divisors of `N`, the sizes of the nonempty multisets on
`ZMod (N * 2)` whose mask is divisible by `Φ_d`, `d ∣ N * 2`, `d ≠ 1`, exactly for `d ∈ P` are the sizes of the
nonempty multisets on `ZMod N` whose mask is divisible by `Φ_d`, `d ∣ N`, `d ≠ 1`, exactly for `d ∈ P`. -/
theorem sizes_eq_two_all {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * 2 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  ext s
  simp only [Set.mem_ofPred_eq]
  constructor
  · rintro ⟨w', hs, hpos, hpat⟩
    refine ⟨Lift.reduce w', (Lift.sum_reduce w').trans hs, hpos, fun d hd hd1 => ?_⟩
    rw [Lift.cyclotomic_dvd_reduce_iff w' d hd]
    exact hpat d (Dvd.dvd.mul_right hd 2) hd1
  · rintro ⟨w, hs, hpos, hpat⟩
    have hw : ∃ x, w x ≠ 0 := Lift.Aux.exists_ne_zero_of_sum_pos w (hs ▸ hpos)
    obtain ⟨w', hred, hnew⟩ := exists_lift_two_all w hw
    subst hred
    refine ⟨w', (Lift.sum_reduce w').symm.trans hs, hpos, fun d hd hd1 => ?_⟩
    by_cases hdN : d ∣ N
    · rw [← Lift.cyclotomic_dvd_reduce_iff w' d hdN]
      exact hpat d hdN hd1
    · exact iff_of_false (hnew d hd hdN) fun h => hdN (hP d h)

end Pnq
