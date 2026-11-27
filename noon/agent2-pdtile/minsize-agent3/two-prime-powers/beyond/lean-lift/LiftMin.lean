/-
The least-size theorem for `Z_{pⁿq}` on the larger group `Z_{pⁿq·r}`, `r` an odd prime (`r` may be `p` or `q`): among the
multisets on `ZMod (p^n * q * r)` whose cyclotomic divisors are a given pattern of divisors of `p^n * q` and no others, the
least number of elements is the one the theorem gives on `ZMod (p^n * q)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.)
-/
import Pnq.MinGroup
import Pnq.Lift

open Finset

namespace Pnq

namespace Lift

namespace Aux

section Levels

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

/-- the mask of the empty multiset is `0` -/
theorem maskW_eq_zero {M : ℕ} [NeZero M] {w : ZMod M → ℕ} (h : ∀ x, w x = 0) : maskW w = 0 := by
  rw [maskW]
  refine Finset.sum_eq_zero fun a _ => ?_
  rw [h a, Nat.cast_zero, Polynomial.C_0, zero_mul]

/-- a multiset whose mask is not divisible by some polynomial is not empty -/
theorem exists_ne_zero_of_not_dvd {M : ℕ} [NeZero M] {w : ZMod M → ℕ} {f : Polynomial ℤ}
    (h : ¬ f ∣ maskW w) : ∃ x, w x ≠ 0 := by
  by_contra h'
  have h0 : ∀ x, w x = 0 := fun x => by_contra fun hx => h' ⟨x, hx⟩
  exact h (by rw [maskW_eq_zero h0]; exact dvd_zero f)

/-- `levelsEW w = Es`, written out -/
theorem levelsEW_eq_iff (w : ZMod (p ^ n * q) → ℕ) {Es : Finset ℕ} (hE : Es ⊆ Finset.Icc 1 n) :
    levelsEW w = Es ↔
      ∀ ℓ ∈ Finset.Icc 1 n, (Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) := by
  classical
  constructor
  · rintro rfl ℓ hℓ
    rw [levelsEW, Finset.mem_filter]
    exact ⟨fun h => ⟨hℓ, h⟩, fun h => h.2⟩
  · intro h
    ext ℓ
    rw [levelsEW, Finset.mem_filter]
    exact ⟨fun hh => (h ℓ hh.1).1 hh.2, fun hℓ => ⟨hE hℓ, (h ℓ (hE hℓ)).2 hℓ⟩⟩

/-- `levelsFW w = Fs`, written out -/
theorem levelsFW_eq_iff (w : ZMod (p ^ n * q) → ℕ) {Fs : Finset ℕ} (hF : Fs ⊆ Finset.Icc 1 n) :
    levelsFW w = Fs ↔
      ∀ ℓ ∈ Finset.Icc 1 n, (Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) := by
  classical
  constructor
  · rintro rfl ℓ hℓ
    rw [levelsFW, Finset.mem_filter]
    exact ⟨fun h => ⟨hℓ, h⟩, fun h => h.2⟩
  · intro h
    ext ℓ
    rw [levelsFW, Finset.mem_filter]
    exact ⟨fun hh => (h ℓ hh.1).1 hh.2, fun hℓ => ⟨hF hℓ, (h ℓ (hF hℓ)).2 hℓ⟩⟩

variable {r : ℕ} [Fact r.Prime]

/-- `Φ_q` and the reduction modulo `p^n q` -/
theorem dvd_q_iff (w' : ZMod (p ^ n * q * r) → ℕ) :
    Polynomial.cyclotomic q ℤ ∣ maskW (reduce (N := p ^ n * q) (r := r) w') ↔
      Polynomial.cyclotomic q ℤ ∣ maskW w' :=
  cyclotomic_dvd_reduce_iff (N := p ^ n * q) (r := r) w' q MinGroupAux.q_dvd

/-- the levels `ℓ` with `Φ_{p^ℓ}`, and the reduction modulo `p^n q` -/
theorem levelsE_iff (w' : ZMod (p ^ n * q * r) → ℕ) {Es : Finset ℕ} (hE : Es ⊆ Finset.Icc 1 n) :
    levelsEW (reduce (N := p ^ n * q) (r := r) w') = Es ↔
      ∀ ℓ ∈ Finset.Icc 1 n, (Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w' ↔ ℓ ∈ Es) := by
  rw [levelsEW_eq_iff _ hE]
  refine forall₂_congr fun ℓ hℓ => ?_
  rw [cyclotomic_dvd_reduce_iff (N := p ^ n * q) (r := r) w' (p ^ ℓ)
    (MinGroupAux.pow_dvd (Finset.mem_Icc.1 hℓ).2)]

/-- the levels `ℓ` with `Φ_{p^ℓ q}`, and the reduction modulo `p^n q` -/
theorem levelsF_iff (w' : ZMod (p ^ n * q * r) → ℕ) {Fs : Finset ℕ} (hF : Fs ⊆ Finset.Icc 1 n) :
    levelsFW (reduce (N := p ^ n * q) (r := r) w') = Fs ↔
      ∀ ℓ ∈ Finset.Icc 1 n, (Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w' ↔ ℓ ∈ Fs) := by
  rw [levelsFW_eq_iff _ hF]
  refine forall₂_congr fun ℓ hℓ => ?_
  rw [cyclotomic_dvd_reduce_iff (N := p ^ n * q) (r := r) w' (p ^ ℓ * q)
    (MinGroupAux.pow_mul_q_dvd (Finset.mem_Icc.1 hℓ).2)]

/-- every level `ℓ` with `Φ_{p^ℓ q}`, and the reduction modulo `p^n q` -/
theorem levelsF_all_iff (w' : ZMod (p ^ n * q * r) → ℕ) :
    levelsFW (reduce (N := p ^ n * q) (r := r) w') = Finset.Icc 1 n ↔
      ∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w' := by
  rw [levelsF_iff w' (Finset.Subset.refl _)]
  exact forall₂_congr fun ℓ hℓ => iff_true_right hℓ

end Levels

end Aux

/-- **Unbalanced patterns, lifted.**  `r` an odd prime.  Among the multisets on `ZMod (p^n * q * r)` with `Φ_q ∤ A(X)`,
with `Φ_{p^ℓ} ∣ A(X)` exactly for the levels `ℓ ∈ Es`, with `Φ_{p^ℓ q} ∣ A(X)` exactly for the levels `ℓ ∈ Fs`, and with
no `Φ_d ∣ A(X)` for a divisor `d` of `p^n q r` that does not divide `p^n q`, the least size is `minU p q Es Fs`. -/
theorem minsize_unbalanced_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minU p q Es Fs) := by
  have hold := minsize_unbalanced_zmod p q n hpq Es Fs hE hF
  constructor
  · obtain ⟨w, hs, h0, hEw, hFw⟩ := hold.1
    obtain ⟨w', hred, hnew⟩ := exists_lift (N := p ^ n * q) (r := r) hr w (Aux.exists_ne_zero_of_not_dvd h0)
    subst hred
    exact ⟨w', (sum_reduce w').symm.trans hs, fun h => h0 ((Aux.dvd_q_iff w').2 h),
      (Aux.levelsE_iff w' hE).1 hEw, (Aux.levelsF_iff w' hF).1 hFw, hnew⟩
  · rintro s ⟨w', hs, h0, hEw, hFw, -⟩
    exact hold.2 ⟨reduce (N := p ^ n * q) (r := r) w', (sum_reduce w').trans hs,
      fun h => h0 ((Aux.dvd_q_iff w').1 h), (Aux.levelsE_iff w' hE).2 hEw, (Aux.levelsF_iff w' hF).2 hFw⟩

/-- **Balanced patterns with every `Φ_{p^ℓ q}`, lifted.** -/
theorem minsize_balanced_all_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ 0 < s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (q * p ^ Es.card) := by
  have hold := minsize_balanced_all_zmod p q n hpq Es hE
  constructor
  · obtain ⟨w, hs, hpos, h0, hEw, hFw⟩ := hold.1
    obtain ⟨w', hred, hnew⟩ := exists_lift (N := p ^ n * q) (r := r) hr w
      (Aux.exists_ne_zero_of_sum_pos w (hs ▸ hpos))
    subst hred
    exact ⟨w', (sum_reduce w').symm.trans hs, hpos, (Aux.dvd_q_iff w').1 h0,
      (Aux.levelsE_iff w' hE).1 hEw, (Aux.levelsF_all_iff w').1 hFw, hnew⟩
  · rintro s ⟨w', hs, hpos, h0, hEw, hFw, -⟩
    exact hold.2 ⟨reduce (N := p ^ n * q) (r := r) w', (sum_reduce w').trans hs, hpos,
      (Aux.dvd_q_iff w').2 h0, (Aux.levelsE_iff w' hE).2 hEw, (Aux.levelsF_all_iff w').2 hFw⟩

/-- **Balanced patterns with a first level `a0` at which `Φ_{p^a0 q} ∤ A(X)`, lifted.** -/
theorem minsize_balanced_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minB p q Es Fs a0) := by
  have hold := minsize_balanced_zmod p q n hpq Es Fs hE hF a0 ha1 han hlow hna
  constructor
  · obtain ⟨w, hs, h0, hEw, hFw⟩ := hold.1
    have hnd : ¬ Polynomial.cyclotomic (p ^ a0 * q) ℤ ∣ maskW w := fun h =>
      hna (((Aux.levelsFW_eq_iff w hF).1 hFw a0 (Finset.mem_Icc.2 ⟨ha1, han⟩)).1 h)
    obtain ⟨w', hred, hnew⟩ := exists_lift (N := p ^ n * q) (r := r) hr w (Aux.exists_ne_zero_of_not_dvd hnd)
    subst hred
    exact ⟨w', (sum_reduce w').symm.trans hs, (Aux.dvd_q_iff w').1 h0,
      (Aux.levelsE_iff w' hE).1 hEw, (Aux.levelsF_iff w' hF).1 hFw, hnew⟩
  · rintro s ⟨w', hs, h0, hEw, hFw, -⟩
    exact hold.2 ⟨reduce (N := p ^ n * q) (r := r) w', (sum_reduce w').trans hs,
      (Aux.dvd_q_iff w').2 h0, (Aux.levelsE_iff w' hE).2 hEw, (Aux.levelsF_iff w' hF).2 hFw⟩

end Lift

end Pnq
