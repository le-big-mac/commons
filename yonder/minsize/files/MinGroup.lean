/-
The least size of a multiset on `ZMod (p^n * q)`, not empty, whose mask polynomial is divisible by exactly a
given set of the cyclotomic polynomials `Φ_d`, `d ∣ p^n q`, `d > 1`.  (The empty multiset has mask polynomial
`0`, which every `Φ_d` divides; it is excluded by `0 < s` in the second theorem and by the pattern itself in
the first and the third.)
(Definitions and statements fixed by agent3 / Yonder, 26 November 2026.)

The divisors `d > 1` of `p^n q` are `p^ℓ` (`1 ≤ ℓ ≤ n`), `q`, and `p^ℓ q` (`1 ≤ ℓ ≤ n`).  A pattern is: the set
`Es` of levels `ℓ` with `Φ_{p^ℓ} ∣ A(X)`, the set `Fs` of levels `ℓ ≥ 1` with `Φ_{p^ℓ q} ∣ A(X)`, and whether
`Φ_q ∣ A(X)`.  The three theorems below cover every pattern.
-/
import Pnq.MinTree
import Pnq.Weighted

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ} ∣ A(X)` -/
noncomputable def levelsEW (w : ZMod (p ^ n * q) → ℕ) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w)

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ q} ∣ A(X)` -/
noncomputable def levelsFW (w : ZMod (p ^ n * q) → ℕ) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w)

namespace MinGroupAux

omit [Fact p.Prime] [Fact q.Prime] in
theorem pow_dvd {ℓ : ℕ} (hn : ℓ ≤ n) : p ^ ℓ ∣ p ^ n * q :=
  Dvd.dvd.mul_right (pow_dvd_pow p hn) q

omit [Fact p.Prime] [Fact q.Prime] in
theorem q_dvd : q ∣ p ^ n * q := dvd_mul_left q (p ^ n)

omit [Fact p.Prime] [Fact q.Prime] in
theorem pow_mul_q_dvd {ℓ : ℕ} (hn : ℓ ≤ n) : p ^ ℓ * q ∣ p ^ n * q :=
  Nat.mul_dvd_mul_right (pow_dvd_pow p hn) q

/-- level `ℓ` of `E`, `1 ≤ ℓ ≤ n`: `Φ_{p^ℓ}` divides the mask polynomial -/
theorem E_treeOfW_iff (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    E (treeOfW w) ℓ ↔ Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w :=
  (E_treeOfW w ℓ h1 hn).trans (zeroAtW_iff_cyclotomic_dvd w (p ^ ℓ) (pow_dvd hn))

/-- level `ℓ` of `F`, `1 ≤ ℓ ≤ n`: `Φ_{p^ℓ q}` divides the mask polynomial -/
theorem F_treeOfW_iff (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    F (treeOfW w) ℓ ↔ Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w :=
  (F_treeOfW hpq w ℓ h1 hn).trans (zeroAtW_iff_cyclotomic_dvd w (p ^ ℓ * q) (pow_mul_q_dvd hn))

/-- level `0` of `F`: `Φ_q` divides the mask polynomial -/
theorem F_treeOfW_zero_iff (w : ZMod (p ^ n * q) → ℕ) :
    F (treeOfW w) 0 ↔ Polynomial.cyclotomic q ℤ ∣ maskW w :=
  (F_treeOfW_zero w).trans (zeroAtW_iff_cyclotomic_dvd w q q_dvd)

theorem eSet_treeOfW (w : ZMod (p ^ n * q) → ℕ) : eSet (treeOfW w) = levelsEW w := by
  ext ℓ
  simp only [mem_eSet, levelsEW, Finset.mem_filter, Finset.mem_Icc]
  constructor
  · rintro ⟨h1, hn, hE⟩
    exact ⟨⟨h1, hn⟩, (E_treeOfW_iff w ℓ h1 hn).1 hE⟩
  · rintro ⟨⟨h1, hn⟩, hZ⟩
    exact ⟨h1, hn, (E_treeOfW_iff w ℓ h1 hn).2 hZ⟩

theorem fSet_treeOfW (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ) : fSet (treeOfW w) = levelsFW w := by
  ext ℓ
  simp only [mem_fSet, levelsFW, Finset.mem_filter, Finset.mem_Icc]
  constructor
  · rintro ⟨h1, hn, hF⟩
    exact ⟨⟨h1, hn⟩, (F_treeOfW_iff hpq w ℓ h1 hn).1 hF⟩
  · rintro ⟨⟨h1, hn⟩, hZ⟩
    exact ⟨h1, hn, (F_treeOfW_iff hpq w ℓ h1 hn).2 hZ⟩

end MinGroupAux

/-- **Least size, `Φ_q ∤ A(X)`.** Among the multisets on `Z_{p^n q}` whose mask polynomial is not divisible
by `Φ_q`, is divisible by `Φ_{p^ℓ}` exactly for `ℓ ∈ Es` and by `Φ_{p^ℓ q}` (`ℓ ≥ 1`) exactly for `ℓ ∈ Fs`,
the least number of elements is `p^|Es|` if `Fs ⊆ Es`, and `p^|Es| (p^|Fs \ Es| + q)` otherwise. -/
theorem minsize_unbalanced_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Fs}
      (minU p q Es Fs) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hT := isLeast_unbalanced hp.two_le hq.two_le ((Nat.coprime_primes hp hq).2 hpq) n Es Fs hE hF
  constructor
  · obtain ⟨t, hs, h0, hEt, hFt⟩ := hT.1
    obtain ⟨w, rfl⟩ := treeOfW_surjective hpq t
    refine ⟨w, ?_, ?_, ?_, ?_⟩
    · rw [← size_treeOfW]
      exact hs
    · exact fun h => h0 ((MinGroupAux.F_treeOfW_zero_iff w).2 h)
    · rw [← MinGroupAux.eSet_treeOfW]
      exact hEt
    · rw [← MinGroupAux.fSet_treeOfW hpq]
      exact hFt
  · rintro s ⟨w, hs, h0, hEw, hFw⟩
    refine hT.2 ⟨treeOfW w, ?_, ?_, ?_, ?_⟩
    · rw [size_treeOfW]
      exact hs
    · exact fun h => h0 ((MinGroupAux.F_treeOfW_zero_iff w).1 h)
    · rw [MinGroupAux.eSet_treeOfW]
      exact hEw
    · rw [MinGroupAux.fSet_treeOfW hpq]
      exact hFw

/-- **Least size, `Φ_q ∣ A(X)` and `Φ_{p^ℓ q} ∣ A(X)` for every `ℓ`.** Among the multisets that are not
empty, whose mask polynomial is divisible by `Φ_q`, by every `Φ_{p^ℓ q}` (`1 ≤ ℓ ≤ n`), and by `Φ_{p^ℓ}`
exactly for `ℓ ∈ Es`, the least number of elements is `q p^|Es|`. -/
theorem minsize_balanced_all_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ 0 < s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Finset.Icc 1 n}
      (q * p ^ Es.card) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hT := isLeast_balanced_all hp.two_le hq.two_le ((Nat.coprime_primes hp hq).2 hpq) n Es hE
  constructor
  · obtain ⟨t, hs, hpos, h0, hEt, hFt⟩ := hT.1
    obtain ⟨w, rfl⟩ := treeOfW_surjective hpq t
    refine ⟨w, ?_, hpos, ?_, ?_, ?_⟩
    · rw [← size_treeOfW]
      exact hs
    · exact (MinGroupAux.F_treeOfW_zero_iff w).1 h0
    · rw [← MinGroupAux.eSet_treeOfW]
      exact hEt
    · rw [← MinGroupAux.fSet_treeOfW hpq]
      exact hFt
  · rintro s ⟨w, hs, hpos, h0, hEw, hFw⟩
    refine hT.2 ⟨treeOfW w, ?_, hpos, ?_, ?_, ?_⟩
    · rw [size_treeOfW]
      exact hs
    · exact (MinGroupAux.F_treeOfW_zero_iff w).2 h0
    · rw [MinGroupAux.eSet_treeOfW]
      exact hEw
    · rw [MinGroupAux.fSet_treeOfW hpq]
      exact hFw

/-- **Least size, `Φ_q ∣ A(X)`, and `a0` the first level in `1..n` that is not in `Fs`.** Among the
multisets whose mask polynomial is divisible by `Φ_q`, by `Φ_{p^ℓ}` exactly for `ℓ ∈ Es` and by `Φ_{p^ℓ q}`
(`1 ≤ ℓ ≤ n`) exactly for `ℓ ∈ Fs`, the least number of elements is `q p^|Es| (p^k' + x)`, where `k'` is the
number of levels beyond `a0` that are in `Fs` and not in `Es`, and `x` is `0` or `1` by the four clauses of
`xOf`. The hypotheses on `a0` hold for exactly one number when `Fs` is not all of `1..n`, and for none when
it is. -/
theorem minsize_balanced_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Fs}
      (minB p q Es Fs a0) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hT := isLeast_balanced hp.two_le hq.two_le ((Nat.coprime_primes hp hq).2 hpq) n Es Fs hE hF
    a0 ha1 han hlow hna
  constructor
  · obtain ⟨t, hs, h0, hEt, hFt⟩ := hT.1
    obtain ⟨w, rfl⟩ := treeOfW_surjective hpq t
    refine ⟨w, ?_, ?_, ?_, ?_⟩
    · rw [← size_treeOfW]
      exact hs
    · exact (MinGroupAux.F_treeOfW_zero_iff w).1 h0
    · rw [← MinGroupAux.eSet_treeOfW]
      exact hEt
    · rw [← MinGroupAux.fSet_treeOfW hpq]
      exact hFt
  · rintro s ⟨w, hs, h0, hEw, hFw⟩
    refine hT.2 ⟨treeOfW w, ?_, ?_, ?_, ?_⟩
    · rw [size_treeOfW]
      exact hs
    · exact (MinGroupAux.F_treeOfW_zero_iff w).2 h0
    · rw [MinGroupAux.eSet_treeOfW]
      exact hEw
    · rw [MinGroupAux.fSet_treeOfW hpq]
      exact hFw

end Pnq
