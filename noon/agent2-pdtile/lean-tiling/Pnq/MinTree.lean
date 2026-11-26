/-
The least size of a multiset on `Z_{pⁿ} × Z_q` (a tree) with a given exact pattern.
(Statements fixed by agent3 / Yonder, 26 November 2026.)  Lower bounds: `Pnq/Tree.lean`, `Pnq/Sharp.lean`,
`Pnq/Balanced.lean`.  Constructions: `Pnq/BuildU.lean`, `Pnq/BuildB.lean`.
-/
import Pnq.BuildU
import Pnq.BuildB

open Finset

namespace Pnq

variable {p q : ℕ}

namespace MinTreeAux

/-- `gBeyond` of a tree is `gOf` of its two sets of levels -/
theorem gBeyond_eq_gOf {n : ℕ} (t : Tree p q n) (a0 : ℕ) :
    gBeyond t a0 = gOf (eSet t) (fSet t) a0 := by
  ext ℓ
  rw [mem_gBeyond, gOf, Finset.mem_filter, Finset.mem_sdiff]

/-- a level at which `E` holds is in `eSet` (if `p > 0`) -/
theorem mem_eSet_of_E (hp : 0 < p) {n : ℕ} (t : Tree p q n) {ℓ : ℕ} (h : E t ℓ) : ℓ ∈ eSet t :=
  (mem_eSet t ℓ).2 ⟨(E_range hp t ℓ h).1, (E_range hp t ℓ h).2, h⟩

/-- the lower bound when `Φ_q ∤ A`: from `pow_e_dvd_size` and `size_pos_of_not_F0` if `F ⊆ E`, and from
`sharp_lemma3` otherwise -/
theorem minU_le_size (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n)
    (h0 : ¬ F t 0) : minU p q (eSet t) (fSet t) ≤ size t := by
  by_cases hsub : fSet t ⊆ eSet t
  · have hval : minU p q (eSet t) (fSet t) = p ^ (eSet t).card := ite_eq_left hsub
    rw [hval]
    exact Nat.le_of_dvd (size_pos_of_not_F0 t h0) (pow_e_dvd_size t)
  · have hval : minU p q (eSet t) (fSet t) = p ^ (eSet t).card * (p ^ (fSet t \ eSet t).card + q) :=
      ite_eq_right hsub
    rw [hval]
    have hne : (fSet t \ eSet t).Nonempty :=
      Finset.ne_empty_iff_nonempty.1 (fun h => hsub (Finset.sdiff_eq_empty_iff_subset.1 h))
    exact sharp_lemma3 hp hq hpq t h0 hne

/-- the lower bound when `Φ_q ∣ A` and the multiset is not empty: from `pow_e_mul_q_dvd_size` -/
theorem q_mul_pow_le_size (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n) (h0 : F t 0)
    (hs : 0 < size t) : q * p ^ (eSet t).card ≤ size t := by
  have h : p ^ (eSet t).card * q ≤ size t := Nat.le_of_dvd hs (pow_e_mul_q_dvd_size hpq t h0)
  rw [mul_comm]
  exact h

/-- the lower bound when `Φ_q ∣ A` and `a0` is the first level missing from `F`: from `balanced_base` if
`xOf` is `0`, and from `balanced_plus` if `xOf` is `1` -/
theorem minB_le_size (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n) (a0 : ℕ)
    (h0 : F t 0) (ha1 : 1 ≤ a0) (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ fSet t)
    (hna : a0 ∉ fSet t) : minB p q (eSet t) (fSet t) a0 ≤ size t := by
  have hp0 : 0 < p := by omega
  have hlow' : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → F t ℓ := fun ℓ h1 h2 => ((mem_fSet t ℓ).1 (hlow ℓ h1 h2)).2.2
  have hna' : ¬ F t a0 := fun h => hna ((mem_fSet t a0).2 ⟨ha1, han, h⟩)
  have hg : gBeyond t a0 = gOf (eSet t) (fSet t) a0 := gBeyond_eq_gOf t a0
  by_cases hx : gOf (eSet t) (fSet t) a0 = ∅ ∨ (∃ ℓ ∈ eSet t, ℓ < a0) ∨ (a0 ∈ eSet t ∧ 3 ≤ p) ∨
      (a0 ∈ eSet t ∧ p = 2 ∧ ∃ b ∈ eSet t \ fSet t, a0 < b ∧ ∀ g ∈ gOf (eSet t) (fSet t) a0, b < g)
  · -- `xOf = 0`
    have hx0 : xOf p (eSet t) (fSet t) a0 = 0 := ite_eq_left hx
    have h := balanced_base hp hq hpq t a0 h0 hlow' ha1 han hna'
    rw [hg] at h
    calc minB p q (eSet t) (fSet t) a0
        = q * p ^ ((eSet t).card + (gOf (eSet t) (fSet t) a0).card) := by
          unfold minB
          rw [hx0]
          ring
      _ ≤ size t := h
  · -- `xOf = 1`: none of the four clauses holds
    have hx1 : xOf p (eSet t) (fSet t) a0 = 1 := ite_eq_right hx
    have hc1 : gOf (eSet t) (fSet t) a0 ≠ ∅ := fun h => hx (Or.inl h)
    have hc2 : ¬ ∃ ℓ ∈ eSet t, ℓ < a0 := fun h => hx (Or.inr (Or.inl h))
    have hc3 : ¬ (a0 ∈ eSet t ∧ 3 ≤ p) := fun h => hx (Or.inr (Or.inr (Or.inl h)))
    have hc4 : ¬ (a0 ∈ eSet t ∧ p = 2 ∧
        ∃ b ∈ eSet t \ fSet t, a0 < b ∧ ∀ g ∈ gOf (eSet t) (fSet t) a0, b < g) :=
      fun h => hx (Or.inr (Or.inr (Or.inr h)))
    have hk : (gBeyond t a0).Nonempty := by
      rw [hg]
      exact Finset.ne_empty_iff_nonempty.1 hc1
    have h2 : ∀ ℓ, ℓ < a0 → ¬ E t ℓ := fun ℓ hℓ hEℓ => hc2 ⟨ℓ, mem_eSet_of_E hp0 t hEℓ, hℓ⟩
    have h34 : ¬ E t a0 ∨ (p = 2 ∧ ∀ b, a0 < b → (∀ g ∈ gBeyond t a0, b < g) → E t b → F t b) := by
      by_cases ha : a0 ∈ eSet t
      · right
        have hp2 : p = 2 := by
          have h3 : ¬ 3 ≤ p := fun h => hc3 ⟨ha, h⟩
          omega
        refine ⟨hp2, fun b hab hbg hEb => ?_⟩
        by_contra hFb
        have hbE : b ∈ eSet t := mem_eSet_of_E hp0 t hEb
        have hbF : b ∉ fSet t := fun h => hFb ((mem_fSet t b).1 h).2.2
        exact hc4 ⟨ha, hp2, b, Finset.mem_sdiff.2 ⟨hbE, hbF⟩, hab,
          fun g hgm => hbg g (by rw [hg]; exact hgm)⟩
      · left
        exact fun h => ha (mem_eSet_of_E hp0 t h)
    have h := balanced_plus hp hq hpq t a0 h0 hlow' ha1 han hna' hk h2 h34
    rw [hg] at h
    calc minB p q (eSet t) (fSet t) a0
        = q * p ^ e t * (p ^ (gOf (eSet t) (fSet t) a0).card + 1) := by
          unfold minB e
          rw [hx1]
      _ ≤ size t := h

end MinTreeAux

/-- **Least size, `Φ_q ∤ A`.** -/
theorem isLeast_unbalanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ t : Tree p q n, size t = s ∧ ¬ F t 0 ∧ eSet t = Es ∧ fSet t = Fs} (minU p q Es Fs) := by
  constructor
  · obtain ⟨t, h0, hEt, hFt, hs⟩ := exists_unbalanced hp hq hpq n Es Fs hE hF
    exact ⟨t, hs, h0, hEt, hFt⟩
  · rintro s ⟨t, rfl, h0, rfl, rfl⟩
    exact MinTreeAux.minU_le_size hp hq hpq t h0

/-- **Least size, `Φ_q ∣ A`, every level in `F`** (among multisets that are not empty). -/
theorem isLeast_balanced_all (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ t : Tree p q n, size t = s ∧ 0 < s ∧ F t 0 ∧ eSet t = Es ∧ fSet t = Finset.Icc 1 n}
      (q * p ^ Es.card) := by
  constructor
  · obtain ⟨t, h0, hEt, hFt, hs⟩ := exists_balanced_all hp hq hpq n Es hE
    exact ⟨t, hs, Nat.mul_pos (by omega) (pow_pos (by omega) _), h0, hEt, hFt⟩
  · rintro s ⟨t, rfl, hs, h0, rfl, -⟩
    exact MinTreeAux.q_mul_pow_le_size hpq t h0 hs

/-- **Least size, `Φ_q ∣ A`, `a0` the first level missing from `F`.** -/
theorem isLeast_balanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ t : Tree p q n, size t = s ∧ F t 0 ∧ eSet t = Es ∧ fSet t = Fs} (minB p q Es Fs a0) := by
  constructor
  · obtain ⟨t, h0, hEt, hFt, hs⟩ := exists_balanced hp hq hpq n Es Fs hE hF a0 ha1 han hlow hna
    exact ⟨t, hs, h0, hEt, hFt⟩
  · rintro s ⟨t, rfl, h0, rfl, rfl⟩
    exact MinTreeAux.minB_le_size hp hq hpq t a0 h0 ha1 han hlow hna

end Pnq
