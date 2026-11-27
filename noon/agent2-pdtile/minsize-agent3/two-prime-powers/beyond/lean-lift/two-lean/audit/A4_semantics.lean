import Pnq.LiftAll
/-! Audit: small facts, proved in Lean, about how the eight statements are to be read; and the paper's wording derived from them.
Nothing here is used by anything else.  The eight theorems are `sorry` in this copy, so every `example` that uses one of them
depends on `sorryAx`; what is checked is that the statements fit together as the paper's wording needs. -/
open Finset

namespace AuditTwo

/-! ### The types -/

-- `p ^ n * q * s` is `(p ^ n * q) * s`, and `2 ^ k * (p ^ a * q ^ b)` is as bracketed
example (p q n s : ℕ) : p ^ n * q * s = (p ^ n * q) * s := rfl
-- every `NeZero` and `Fact` argument is a proof of a proposition, so which instance Lean found cannot matter
example (n : ℕ) (h₁ h₂ : NeZero n) : h₁ = h₂ := rfl
example (h₁ h₂ : Fact (Nat.Prime 2)) : h₁ = h₂ := rfl
example : Nat.fact_prime_two = (⟨Nat.prime_two⟩ : Fact (Nat.Prime 2)) := rfl

/-! ### `d = 0`, `d = 1`, the empty multiset -/

example : Polynomial.cyclotomic 0 ℤ = 1 := Polynomial.cyclotomic_zero ℤ
example : Polynomial.cyclotomic 1 ℤ = Polynomial.X - 1 := Polynomial.cyclotomic_one ℤ
-- `d = 0` is never a divisor of the orders in the statements
example (N : ℕ) [NeZero N] : ¬ (0 ∣ N * 2) := by
  intro h
  have := Nat.eq_zero_of_zero_dvd h
  have hN := NeZero.ne N
  omega
example (p q a b : ℕ) [Fact p.Prime] [Fact q.Prime] : ¬ (0 ∣ p ^ a * q ^ b) := by
  intro h
  exact NeZero.ne (p ^ a * q ^ b) (Nat.eq_zero_of_zero_dvd h)
-- the mask of the empty multiset is 0, and every polynomial divides it
theorem maskW_zero {M : ℕ} [NeZero M] : Pnq.maskW (fun _ : ZMod M => 0) = 0 := by
  simp [Pnq.maskW]
example {M : ℕ} [NeZero M] (d : ℕ) : Polynomial.cyclotomic d ℤ ∣ Pnq.maskW (fun _ : ZMod M => 0) := by
  rw [maskW_zero]; exact dvd_zero _
-- the value of the mask at 1 is the number of elements
theorem eval_one_maskW {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    (Pnq.maskW w).eval 1 = ((∑ a, w a : ℕ) : ℤ) := by
  unfold Pnq.maskW
  rw [← Polynomial.coe_evalRingHom, map_sum]
  simp
-- `Φ_1` divides the mask only of the empty multiset
theorem cyclotomic_one_dvd_iff {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    Polynomial.cyclotomic 1 ℤ ∣ Pnq.maskW w ↔ ∑ a, w a = 0 := by
  have h1 : (Polynomial.X - 1 : Polynomial ℤ) = Polynomial.X - Polynomial.C 1 := by simp
  rw [Polynomial.cyclotomic_one, h1, Polynomial.dvd_iff_isRoot, Polynomial.IsRoot.def, eval_one_maskW]
  exact_mod_cast Iff.rfl
-- so in `exists_signs` the clause for `d = 1` says exactly: the numbers of `+` and of `-` differ
theorem signs_at_one {M : ℕ} [NeZero M] (u v : ZMod M → ℕ) :
    ¬ Polynomial.cyclotomic 1 ℤ ∣ Pnq.maskW u - Pnq.maskW v ↔ ∑ a, u a ≠ ∑ a, v a := by
  have h1 : (Polynomial.X - 1 : Polynomial ℤ) = Polynomial.X - Polynomial.C 1 := by simp
  rw [Polynomial.cyclotomic_one, h1, Polynomial.dvd_iff_isRoot, Polynomial.IsRoot.def, Polynomial.eval_sub,
    eval_one_maskW, eval_one_maskW, sub_eq_zero]
  exact_mod_cast Iff.rfl

/-! ### The statements can be used: no hypothesis is contradictory -/

instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩

example (w : ZMod (3 ^ 2 * 5 ^ 1) → ℕ) (hw : ∃ x, w x ≠ 0) :=
  Pnq.Lift.exists_signs 3 5 (by decide) (by decide) (by decide) 2 1 w hw
example (w : ZMod (3 ^ 0 * 5 ^ 0) → ℕ) (hw : ∃ x, w x ≠ 0) :=
  Pnq.Lift.exists_signs 3 5 (by decide) (by decide) (by decide) 0 0 w hw
-- N = 12 = 2^2 * (3^1 * 5^0): the prime 5 is only a place-holder
example (w : ZMod 12 → ℕ) (hw : ∃ x, w x ≠ 0) :=
  Pnq.Lift.exists_lift_two (N := 12) 3 5 (by decide) (by decide) (by decide) 2 1 0 (by norm_num) w hw
example (w : ZMod 1 → ℕ) (hw : ∃ x, w x ≠ 0) :=
  Pnq.Lift.exists_lift_two (N := 1) 3 5 (by decide) (by decide) (by decide) 0 0 0 (by norm_num) w hw
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 12) :=
  Pnq.Lift.sizes_eq_two (N := 12) 3 5 (by decide) (by decide) (by decide) 2 1 0 (by norm_num) P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 30) := Pnq.Lift.sizes_eq_odd (N := 30) 15 (by decide) P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 30) := Pnq.Lift.sizes_eq_odd (N := 30) 1 (by decide) P hP
-- p = 2, q = 2, n = 0, s = 1, s even, s a multiple of p and of q: all allowed
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 2 ^ 2 * 3) := Pnq.Lift.sizes_eq_mul 2 3 2 6 (by decide) P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 3 ^ 2 * 2) := Pnq.Lift.sizes_eq_mul 3 2 2 4 (by decide) P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 3 ^ 0 * 5) := Pnq.Lift.sizes_eq_mul 3 5 0 2 (by decide) P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 3 ^ 1 * 5) := Pnq.Lift.sizes_eq_mul 3 5 1 1 (by decide) P hP
example := Pnq.Lift.minsize_unbalanced_mul 2 3 2 6 (by decide) {1} {2} (by decide) (by decide)
example := Pnq.Lift.minsize_unbalanced_mul 3 2 0 4 (by decide) ∅ ∅ (by decide) (by decide)
example := Pnq.Lift.minsize_balanced_all_mul 3 2 2 4 (by decide) {1, 2} (by decide)
example := Pnq.Lift.minsize_balanced_all_mul 3 5 0 1 (by decide) ∅ (by decide)
example := Pnq.Lift.minsize_balanced_mul 2 3 2 6 (by decide) {1} {2} (by decide) (by decide) 1 (by decide) (by decide)
  (by decide) (by decide)
-- the third statement has no instance for n = 0: its hypotheses on a0 cannot hold
example (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ 0) : False := by omega
-- and for n ≥ 1 they hold for exactly one a0 when Fs is not everything (the first level missing from Fs)
example (Fs : Finset ℕ) (a a' : ℕ) (h1 : ∀ ℓ, 1 ≤ ℓ → ℓ < a → ℓ ∈ Fs) (h2 : a ∉ Fs) (ha : 1 ≤ a)
    (h1' : ∀ ℓ, 1 ≤ ℓ → ℓ < a' → ℓ ∈ Fs) (h2' : a' ∉ Fs) (ha' : 1 ≤ a') : a = a' := by
  rcases Nat.lt_trichotomy a a' with h | h | h
  · exact absurd (h1' a ha h) h2
  · exact h
  · exact absurd (h1 a' ha' h) h2'

/-! ### The paper's Lemma "lifting along 2", as worded, from `exists_lift_two` and two finished theorems -/

theorem paper_lift2 {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q)
    (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b)) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = ∑ x, w x ∧ Pnq.Lift.reduce w' = w ∧
      ∀ d, d ∣ N * 2 → (Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w' ↔
        (d ∣ N ∧ Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w)) := by
  obtain ⟨w', hred, hnew⟩ := Pnq.Lift.exists_lift_two p q hp hq hpq k a b hN w hw
  subst hred
  refine ⟨w', (Pnq.Lift.sum_reduce w').symm, rfl, fun d hd => ⟨fun h => ?_, fun h => ?_⟩⟩
  · have hdN : d ∣ N := by
      by_contra hc
      exact hnew d hd hc h
    exact ⟨hdN, (Pnq.Lift.cyclotomic_dvd_reduce_iff w' d hdN).2 h⟩
  · exact (Pnq.Lift.cyclotomic_dvd_reduce_iff w' d h.1).1 h.2

/-! ### The paper's Lemma "signs" in the wording "each element gets a sign": a splitting `u + v = w` is a signing -/

-- `u x` of the `w x` copies of `x` are signed `+`, the other `v x` are signed `-`; the signed mask has the integer
-- coefficient `u x - v x` at `X ^ x.val`
theorem signed_mask {M : ℕ} [NeZero M] (u v : ZMod M → ℕ) :
    Pnq.maskW u - Pnq.maskW v = ∑ a : ZMod M, Polynomial.C ((u a : ℤ) - (v a : ℤ)) * Polynomial.X ^ a.val := by
  simp [Pnq.maskW, ← Finset.sum_sub_distrib, sub_mul]

/-! ### In the sets of sizes, `1 ∈ P` makes no difference, and `0 < t` is what keeps the empty multiset out on the right -/

example {N : ℕ} [NeZero N] (P : Finset ℕ) (w : ZMod N → ℕ) :
    (∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w ↔ d ∈ P)) ↔
    (∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w ↔ d ∈ P.erase 1)) := by
  constructor
  · intro h d hd h1
    rw [h d hd h1, Finset.mem_erase]
    exact ⟨fun hh => ⟨h1, hh⟩, fun hh => hh.2⟩
  · intro h d hd h1
    rw [h d hd h1, Finset.mem_erase]
    exact ⟨fun hh => hh.2, fun hh => ⟨h1, hh⟩⟩

end AuditTwo

#print axioms AuditTwo.cyclotomic_one_dvd_iff
#print axioms AuditTwo.signs_at_one
#print axioms AuditTwo.signed_mask
#print axioms AuditTwo.paper_lift2
#print axioms Pnq.Lift.sum_reduce
#print axioms Pnq.Lift.cyclotomic_dvd_reduce_iff
#print axioms Pnq.Lift.exists_lift
#print axioms Pnq.Lift.sizes_eq
#print axioms Pnq.minsize_unbalanced_zmod
#print axioms Pnq.minsize_balanced_all_zmod
#print axioms Pnq.minsize_balanced_zmod
