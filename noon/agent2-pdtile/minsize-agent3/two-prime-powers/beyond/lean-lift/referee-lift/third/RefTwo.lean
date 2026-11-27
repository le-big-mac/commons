import Pnq.LiftAll
/-! Referee's third-pass checks of the files for the prime 2 and every s (read-only; nothing here is part of the library).
1. axioms of the eight fixed theorems;
2. the paper's Lemma 18 in the paper's own wording, derived from `exists_lift_two`, `sum_reduce`, `cyclotomic_dvd_reduce_iff`;
3. the paper's Lemma 17 at d = 1: the numbers of + and of - differ (so "d = 1 included" has content);
4. instances: the note's case Z_18 -> Z_36 (pattern {18} inside 18, lift along 2) as an instance of `minsize_balanced_all_mul`;
   N = 12 = 2^2 * (3^1 * 5^0) for the lift along 2; `sizes_eq_mul` with s = 12;
5. the remark after Corollary 19 is NOT one of the eight: it is derived here for one prime step from the two reduction theorems, to
   see that it is true and what it needs (unbalanced case, r any prime, 2 included, no clause on the new divisors). -/
open Pnq Pnq.Lift

#print axioms Pnq.Lift.exists_signs
#print axioms Pnq.Lift.exists_lift_two
#print axioms Pnq.Lift.sizes_eq_two
#print axioms Pnq.Lift.sizes_eq_odd
#print axioms Pnq.Lift.sizes_eq_mul
#print axioms Pnq.Lift.minsize_unbalanced_mul
#print axioms Pnq.Lift.minsize_balanced_all_mul
#print axioms Pnq.Lift.minsize_balanced_mul
#check @Pnq.Lift.TwoAux.exists_lift_two_aux

namespace Referee3

/-- Lemma 18 as the paper words it. -/
theorem paper_lemma18 {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q)
    (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b)) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = ∑ x, w x ∧ reduce w' = w ∧
      ∀ d, d ∣ N * 2 →
        (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∣ N ∧ Polynomial.cyclotomic d ℤ ∣ maskW w) := by
  obtain ⟨w', hred, hnew⟩ := exists_lift_two p q hp hq hpq k a b hN w hw
  subst hred
  refine ⟨w', (sum_reduce w').symm, rfl, fun d hd => ?_⟩
  constructor
  · intro h
    by_cases hdN : d ∣ N
    · exact ⟨hdN, (cyclotomic_dvd_reduce_iff w' d hdN).2 h⟩
    · exact absurd h (hnew d hd hdN)
  · rintro ⟨hdN, h⟩
    exact (cyclotomic_dvd_reduce_iff w' d hdN).1 h

#print axioms Referee3.paper_lemma18

instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩

/-- the lift along 2 on Z_12, written 12 = 2^2 * (3^1 * 5^0) -/
example (w : ZMod 12 → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (12 * 2) → ℕ, reduce w' = w ∧
      ∀ d, d ∣ 12 * 2 → ¬ d ∣ 12 → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' :=
  exists_lift_two 3 5 (by norm_num) (by norm_num) (by norm_num) 2 1 0 (by norm_num) w hw

/-- the note's case: on Z_36 = Z_{3^2 * 2 * 2}, the patterns inside 18.  Here: balanced (Φ_2), Φ_3 and Φ_9 not, Φ_6 and Φ_18 yes, and
none of Φ_4, Φ_12, Φ_36: the least size is `2 * 3 ^ 0`. -/
example :
    IsLeast {t | ∃ w : ZMod (3 ^ 2 * 2 * 2) → ℕ, ∑ a, w a = t ∧ 0 < t ∧ Polynomial.cyclotomic 2 ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 2, Polynomial.cyclotomic (3 ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ (∅ : Finset ℕ)) ∧
        (∀ ℓ ∈ Finset.Icc 1 2, Polynomial.cyclotomic (3 ^ ℓ * 2) ℤ ∣ maskW w) ∧
        ∀ d, d ∣ 3 ^ 2 * 2 * 2 → ¬ d ∣ 3 ^ 2 * 2 → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (2 * 3 ^ (∅ : Finset ℕ).card) :=
  minsize_balanced_all_mul 3 2 2 2 (by norm_num) ∅ (by simp)

/-- `sizes_eq_mul` with s = 12 on top of Z_{2^1 * 3}: the group is Z_72 -/
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 2 ^ 1 * 3) :
    {t | ∃ w' : ZMod (2 ^ 1 * 3 * 12) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ 2 ^ 1 * 3 * 12 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod (2 ^ 1 * 3) → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ 2 ^ 1 * 3 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} :=
  sizes_eq_mul 2 3 1 12 (by norm_num) P hP

/-- The remark after Corollary 19, for one prime step r (any prime, 2 included) and the unbalanced case: a multiset on Z_{p^n q r} with the
pattern (Es, Fs, not Φ_q) among the divisors of p^n q, WHATEVER new divisors it has, has at least `minU p q Es Fs` elements. -/
theorem remark_one_step (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n)
    (w' : ZMod (p ^ n * q * r) → ℕ) (h0 : ¬ Polynomial.cyclotomic q ℤ ∣ maskW w')
    (hEw : ∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w' ↔ ℓ ∈ Es)
    (hFw : ∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w' ↔ ℓ ∈ Fs) :
    minU p q Es Fs ≤ ∑ a, w' a := by
  have hold := (minsize_unbalanced_zmod p q n hpq Es Fs hE hF).2
  exact hold ⟨reduce (N := p ^ n * q) (r := r) w', (sum_reduce w'),
    fun h => h0 ((Aux.dvd_q_iff w').1 h), (Aux.levelsE_iff w' hE).2 hEw, (Aux.levelsF_iff w' hF).2 hFw⟩

#print axioms Referee3.remark_one_step

end Referee3
