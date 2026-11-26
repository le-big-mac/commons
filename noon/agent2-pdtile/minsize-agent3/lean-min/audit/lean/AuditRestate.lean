import Pnq.MinGroup

/-
Audit scratch.  Nothing here is part of the project.  These lemmas restate, in elementary terms,
what the three theorems of Pnq/MinGroup.lean and the definitions under them say, and Lean checks
that the restatements follow from the originals.
-/

open Pnq

namespace Audit

/-! ### 1. The Lean notions, unfolded -/

/-- `IsLeast S m` is: `m ∈ S` and `m ≤ s` for every `s ∈ S`. -/
example (S : Set ℕ) (m : ℕ) : IsLeast S m ↔ m ∈ S ∧ ∀ s ∈ S, m ≤ s := Iff.rfl

/-- membership in a set-builder is the predicate -/
example (P : ℕ → Prop) (s : ℕ) : s ∈ {s | P s} ↔ P s := Iff.rfl

/-- `Es ⊆ Finset.Icc 1 n` is: every member of `Es` is between `1` and `n` -/
example (Es : Finset ℕ) (n : ℕ) : Es ⊆ Finset.Icc 1 n ↔ ∀ ℓ ∈ Es, 1 ≤ ℓ ∧ ℓ ≤ n := by
  simp [Finset.subset_iff]

/-- for `n = 0` the interval `1..n` is empty -/
example : Finset.Icc 1 0 = (∅ : Finset ℕ) := by decide

/-- the group has `p^n q` elements -/
example (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] : Fintype.card (ZMod (p ^ n * q)) = p ^ n * q :=
  ZMod.card _

/-- `a.val` is a natural number below `M` that represents `a` -/
example (M : ℕ) [NeZero M] (a : ZMod M) : a.val < M ∧ ((a.val : ℕ) : ZMod M) = a :=
  ⟨ZMod.val_lt a, ZMod.natCast_zmod_val a⟩

/-- the mask polynomial, by definition -/
example (M : ℕ) [NeZero M] (w : ZMod M → ℕ) :
    maskW w = ∑ a : ZMod M, Polynomial.C (w a : ℤ) * Polynomial.X ^ a.val := rfl

/-- the coefficient of `X^k` in the mask polynomial is the multiplicity of the residue `k` for `k < M`,
and `0` for `k ≥ M` -/
theorem maskW_coeff {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (k : ℕ) :
    (maskW w).coeff k = if k < M then (w (k : ZMod M) : ℤ) else 0 := by
  rw [maskW, Polynomial.finsetSum_coeff]
  simp only [Polynomial.coeff_C_mul_X_pow]
  split_ifs with h
  · rw [Finset.sum_eq_single (k : ZMod M)]
    · simp [ZMod.val_natCast_of_lt h]
    · intro b _ hb
      rw [if_neg]
      rintro rfl
      exact hb (ZMod.natCast_zmod_val b).symm
    · simp
  · apply Finset.sum_eq_zero
    intro a _
    rw [if_neg]
    rintro rfl
    exact h (ZMod.val_lt a)

/-- the mask polynomial as a sum over the exponents `0 ≤ k < M` -/
theorem maskW_eq_sum_range {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    maskW w = ∑ k ∈ Finset.range M, Polynomial.C (w (k : ZMod M) : ℤ) * Polynomial.X ^ k := by
  ext k
  rw [maskW_coeff, Polynomial.finsetSum_coeff]
  simp only [Polynomial.coeff_C_mul_X_pow]
  simp [Finset.mem_range]

/-- the value of the mask polynomial at `1` is the number of elements -/
theorem maskW_eval_one {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    (maskW w).eval 1 = ((∑ a, w a : ℕ) : ℤ) := by
  simp [maskW, Polynomial.eval_finsetSum]

/-- membership in `levelsEW w` -/
theorem mem_levelsEW {p q n : ℕ} [Fact p.Prime] [Fact q.Prime] (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) :
    ℓ ∈ levelsEW w ↔ (1 ≤ ℓ ∧ ℓ ≤ n) ∧ Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w := by
  simp [levelsEW]

/-- membership in `levelsFW w` -/
theorem mem_levelsFW {p q n : ℕ} [Fact p.Prime] [Fact q.Prime] (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) :
    ℓ ∈ levelsFW w ↔ (1 ≤ ℓ ∧ ℓ ≤ n) ∧ Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w := by
  simp [levelsFW]

/-- `levelsEW w = Es`, for `Es ⊆ 1..n`, says exactly: for every level `ℓ` of `1..n`,
`Φ_{p^ℓ} ∣ A` if and only if `ℓ ∈ Es`. -/
theorem levelsEW_eq_iff {p q n : ℕ} [Fact p.Prime] [Fact q.Prime] (w : ZMod (p ^ n * q) → ℕ)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    levelsEW w = Es ↔ ∀ ℓ, 1 ≤ ℓ → ℓ ≤ n → (Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) := by
  constructor
  · rintro rfl ℓ h1 hn
    rw [mem_levelsEW]
    exact ⟨fun h => ⟨⟨h1, hn⟩, h⟩, fun h => h.2⟩
  · intro h
    ext ℓ
    rw [mem_levelsEW]
    constructor
    · rintro ⟨⟨h1, hn⟩, hd⟩
      exact (h ℓ h1 hn).1 hd
    · intro hℓ
      have hI := Finset.mem_Icc.1 (hE hℓ)
      exact ⟨hI, (h ℓ hI.1 hI.2).2 hℓ⟩

/-- the same for `levelsFW` -/
theorem levelsFW_eq_iff {p q n : ℕ} [Fact p.Prime] [Fact q.Prime] (w : ZMod (p ^ n * q) → ℕ)
    (Fs : Finset ℕ) (hF : Fs ⊆ Finset.Icc 1 n) :
    levelsFW w = Fs ↔ ∀ ℓ, 1 ≤ ℓ → ℓ ≤ n → (Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) := by
  constructor
  · rintro rfl ℓ h1 hn
    rw [mem_levelsFW]
    exact ⟨fun h => ⟨⟨h1, hn⟩, h⟩, fun h => h.2⟩
  · intro h
    ext ℓ
    rw [mem_levelsFW]
    constructor
    · rintro ⟨⟨h1, hn⟩, hd⟩
      exact (h ℓ h1 hn).1 hd
    · intro hℓ
      have hI := Finset.mem_Icc.1 (hF hℓ)
      exact ⟨hI, (h ℓ hI.1 hI.2).2 hℓ⟩

/-! ### 2. The empty multiset -/

/-- a multiset with no element is the zero function -/
theorem eq_zero_of_sum_eq_zero {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (h : ∑ a, w a = 0) :
    ∀ a, w a = 0 := by
  intro a
  exact (Finset.sum_eq_zero_iff.1 h) a (Finset.mem_univ a)

/-- its mask polynomial is `0` -/
theorem maskW_eq_zero_of_sum_eq_zero {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (h : ∑ a, w a = 0) :
    maskW w = 0 := by
  have h0 := eq_zero_of_sum_eq_zero w h
  simp [maskW, h0]

/-- so the empty multiset has the pattern "every `Φ_d` divides": `Φ_q`, every level in `E`, every level in `F` -/
theorem empty_pattern {p q n : ℕ} [Fact p.Prime] [Fact q.Prime] (w : ZMod (p ^ n * q) → ℕ)
    (h : ∑ a, w a = 0) :
    Polynomial.cyclotomic q ℤ ∣ maskW w ∧ levelsEW w = Finset.Icc 1 n ∧ levelsFW w = Finset.Icc 1 n := by
  have h0 := maskW_eq_zero_of_sum_eq_zero w h
  refine ⟨h0 ▸ dvd_zero _, ?_, ?_⟩
  · ext ℓ
    rw [mem_levelsEW, h0, Finset.mem_Icc]
    simp
  · ext ℓ
    rw [mem_levelsFW, h0, Finset.mem_Icc]
    simp

/-! ### 3. The level `a0` of the third theorem is forced -/

/-- the hypotheses on `a0` hold for at most one number -/
theorem a0_unique (Fs : Finset ℕ) (a0 a0' : ℕ)
    (ha1 : 1 ≤ a0) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs)
    (ha1' : 1 ≤ a0') (hlow' : ∀ ℓ, 1 ≤ ℓ → ℓ < a0' → ℓ ∈ Fs) (hna' : a0' ∉ Fs) : a0 = a0' := by
  rcases lt_trichotomy a0 a0' with h | h | h
  · exact absurd (hlow' a0 ha1 h) hna
  · exact h
  · exact absurd (hlow a0' ha1' h) hna'

/-- and they hold for some number as soon as `Fs` is not all of `1..n` -/
theorem a0_exists (n : ℕ) (Fs : Finset ℕ) (hne : Fs ≠ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    ∃ a0, 1 ≤ a0 ∧ a0 ≤ n ∧ (∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) ∧ a0 ∉ Fs := by
  have hne' : (Finset.Icc 1 n \ Fs).Nonempty := by
    rw [← Finset.ne_empty_iff_nonempty, Ne, Finset.sdiff_eq_empty_iff_subset]
    exact fun h => hne (Finset.Subset.antisymm hF h)
  have hmem := Finset.min'_mem _ hne'
  rw [Finset.mem_sdiff, Finset.mem_Icc] at hmem
  refine ⟨(Finset.Icc 1 n \ Fs).min' hne', hmem.1.1, hmem.1.2, ?_, hmem.2⟩
  intro ℓ h1 hlt
  by_contra hℓ
  have : ℓ ∈ Finset.Icc 1 n \ Fs :=
    Finset.mem_sdiff.2 ⟨Finset.mem_Icc.2 ⟨h1, hlt.le.trans hmem.1.2⟩, hℓ⟩
  exact absurd (Finset.min'_le _ ℓ this) (not_le.2 hlt)

/-- when `Fs` is all of `1..n` no number satisfies them: the second and third theorems never both apply -/
theorem no_a0_of_all (n : ℕ) (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ n) : a0 ∈ Finset.Icc 1 n :=
  Finset.mem_Icc.2 ⟨ha1, han⟩

/-! ### 4. One statement for every pattern

`Pat p q n b Es Fs` is the set of sizes of the multisets on `Z_{p^n q}` that are NOT EMPTY and have exactly
the pattern: `Φ_q ∣ A` iff `b`; for every `ℓ` in `1..n`, `Φ_{p^ℓ} ∣ A` iff `ℓ ∈ Es`, and `Φ_{p^ℓ q} ∣ A` iff
`ℓ ∈ Fs`.  It is written without `levelsEW`, `levelsFW`. -/
def Pat (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (b : Prop) (Es Fs : Finset ℕ) : Set ℕ :=
  {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
      (Polynomial.cyclotomic q ℤ ∣ maskW w ↔ b) ∧
      (∀ ℓ, 1 ≤ ℓ → ℓ ≤ n → (Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es)) ∧
      (∀ ℓ, 1 ≤ ℓ → ℓ ≤ n → (Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs))}

/-- From `minsize_unbalanced_zmod`: `Φ_q ∤ A`. -/
theorem least_unbalanced (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast (Pat p q n False Es Fs) (minU p q Es Fs) := by
  have h := minsize_unbalanced_zmod p q n hpq Es Fs hE hF
  have key : Pat p q n False Es Fs = {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧
      ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧ levelsEW w = Es ∧ levelsFW w = Fs} := by
    ext s
    constructor
    · rintro ⟨w, hs, _, hq, hEw, hFw⟩
      exact ⟨w, hs, fun hd => hq.1 hd, (levelsEW_eq_iff w Es hE).2 hEw, (levelsFW_eq_iff w Fs hF).2 hFw⟩
    · rintro ⟨w, hs, hq, hEw, hFw⟩
      refine ⟨w, hs, ?_, ⟨fun hd => hq hd, False.elim⟩, (levelsEW_eq_iff w Es hE).1 hEw,
        (levelsFW_eq_iff w Fs hF).1 hFw⟩
      rcases Nat.eq_zero_or_pos s with h0 | h0
      · exact absurd (empty_pattern w (hs.trans h0)).1 hq
      · exact h0
  rw [key]
  exact h

/-- From `minsize_balanced_all_zmod`: `Φ_q ∣ A` and every level of `1..n` in `F`. -/
theorem least_balanced_all (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast (Pat p q n True Es (Finset.Icc 1 n)) (q * p ^ Es.card) := by
  have h := minsize_balanced_all_zmod p q n hpq Es hE
  have key : Pat p q n True Es (Finset.Icc 1 n) = {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
      Polynomial.cyclotomic q ℤ ∣ maskW w ∧ levelsEW w = Es ∧ levelsFW w = Finset.Icc 1 n} := by
    ext s
    constructor
    · rintro ⟨w, hs, hpos, hq, hEw, hFw⟩
      exact ⟨w, hs, hpos, hq.2 trivial, (levelsEW_eq_iff w Es hE).2 hEw,
        (levelsFW_eq_iff w _ (Finset.Subset.refl _)).2 hFw⟩
    · rintro ⟨w, hs, hpos, hq, hEw, hFw⟩
      exact ⟨w, hs, hpos, ⟨fun _ => trivial, fun _ => hq⟩, (levelsEW_eq_iff w Es hE).1 hEw,
        (levelsFW_eq_iff w _ (Finset.Subset.refl _)).1 hFw⟩
  rw [key]
  exact h

/-- From `minsize_balanced_zmod`: `Φ_q ∣ A` and `a0` the least level of `1..n` not in `F`. -/
theorem least_balanced (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast (Pat p q n True Es Fs) (minB p q Es Fs a0) := by
  have h := minsize_balanced_zmod p q n hpq Es Fs hE hF a0 ha1 han hlow hna
  have key : Pat p q n True Es Fs = {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧
      Polynomial.cyclotomic q ℤ ∣ maskW w ∧ levelsEW w = Es ∧ levelsFW w = Fs} := by
    ext s
    constructor
    · rintro ⟨w, hs, _, hq, hEw, hFw⟩
      exact ⟨w, hs, hq.2 trivial, (levelsEW_eq_iff w Es hE).2 hEw, (levelsFW_eq_iff w Fs hF).2 hFw⟩
    · rintro ⟨w, hs, hq, hEw, hFw⟩
      refine ⟨w, hs, ?_, ⟨fun _ => trivial, fun _ => hq⟩, (levelsEW_eq_iff w Es hE).1 hEw,
        (levelsFW_eq_iff w Fs hF).1 hFw⟩
      rcases Nat.eq_zero_or_pos s with h0 | h0
      · have hall := (empty_pattern w (hs.trans h0)).2.2
        rw [hFw] at hall
        exact absurd (hall ▸ Finset.mem_Icc.2 ⟨ha1, han⟩) hna
      · exact h0
  rw [key]
  exact h

/-- **Every pattern, once.**  For every `b` and every `Es, Fs ⊆ 1..n` there is exactly one number that is
the least size of a nonempty multiset with exactly that pattern (so in particular some multiset has it),
and exactly one of the three cases gives it. -/
theorem every_pattern (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q) (b : Prop)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    (¬ b ∧ IsLeast (Pat p q n b Es Fs) (minU p q Es Fs)) ∨
    (b ∧ Fs = Finset.Icc 1 n ∧ IsLeast (Pat p q n b Es Fs) (q * p ^ Es.card)) ∨
    (b ∧ Fs ≠ Finset.Icc 1 n ∧ ∃ a0, (1 ≤ a0 ∧ a0 ≤ n ∧ (∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) ∧ a0 ∉ Fs) ∧
      (∀ a, (1 ≤ a ∧ a ≤ n ∧ (∀ ℓ, 1 ≤ ℓ → ℓ < a → ℓ ∈ Fs) ∧ a ∉ Fs) → a = a0) ∧
      IsLeast (Pat p q n b Es Fs) (minB p q Es Fs a0)) := by
  by_cases hb : b
  · have hbT : b = True := propext ⟨fun _ => trivial, fun _ => hb⟩
    subst hbT
    by_cases hall : Fs = Finset.Icc 1 n
    · right; left
      subst hall
      exact ⟨trivial, rfl, least_balanced_all p q n hpq Es hE⟩
    · right; right
      obtain ⟨a0, ha1, han, hlow, hna⟩ := a0_exists n Fs hall hF
      refine ⟨trivial, hall, a0, ⟨ha1, han, hlow, hna⟩, ?_, least_balanced p q n hpq Es Fs hE hF a0 ha1 han hlow hna⟩
      rintro a ⟨h1, _, hl, hn⟩
      exact a0_unique Fs a a0 h1 hl hn ha1 hlow hna
  · left
    have hbF : b = False := propext ⟨fun h => hb h, False.elim⟩
    subst hbF
    exact ⟨hb, least_unbalanced p q n hpq Es Fs hE hF⟩

/-! ### 5. The rule, unfolded -/

theorem mem_gOf (Es Fs : Finset ℕ) (a0 g : ℕ) : g ∈ gOf Es Fs a0 ↔ g ∈ Fs ∧ g ∉ Es ∧ a0 < g := by
  simp [gOf, and_assoc]

theorem minU_of_subset (p q : ℕ) (Es Fs : Finset ℕ) (h : Fs ⊆ Es) : minU p q Es Fs = p ^ Es.card := by
  simp [minU, h]

theorem minU_of_not_subset (p q : ℕ) (Es Fs : Finset ℕ) (h : ¬ Fs ⊆ Es) :
    minU p q Es Fs = p ^ Es.card * (p ^ (Fs \ Es).card + q) := by
  simp [minU, h]

/-- `xOf` is `0` exactly when one of the four clauses holds, and `1` otherwise -/
theorem xOf_eq_zero_iff (p : ℕ) (Es Fs : Finset ℕ) (a0 : ℕ) :
    xOf p Es Fs a0 = 0 ↔
      (gOf Es Fs a0 = ∅ ∨ (∃ ℓ ∈ Es, ℓ < a0) ∨ (a0 ∈ Es ∧ 3 ≤ p) ∨
        (a0 ∈ Es ∧ p = 2 ∧ ∃ b ∈ Es \ Fs, a0 < b ∧ ∀ g ∈ gOf Es Fs a0, b < g)) := by
  by_cases h : (gOf Es Fs a0 = ∅ ∨ (∃ ℓ ∈ Es, ℓ < a0) ∨ (a0 ∈ Es ∧ 3 ≤ p) ∨
        (a0 ∈ Es ∧ p = 2 ∧ ∃ b ∈ Es \ Fs, a0 < b ∧ ∀ g ∈ gOf Es Fs a0, b < g))
  · have hx : xOf p Es Fs a0 = 0 := if_pos h
    exact ⟨fun _ => h, fun _ => hx⟩
  · have hx : xOf p Es Fs a0 = 1 := if_neg h
    exact ⟨fun h1 => absurd (hx ▸ h1) one_ne_zero, fun h1 => absurd h1 h⟩

theorem xOf_eq_one_iff (p : ℕ) (Es Fs : Finset ℕ) (a0 : ℕ) :
    xOf p Es Fs a0 = 1 ↔
      ¬ (gOf Es Fs a0 = ∅ ∨ (∃ ℓ ∈ Es, ℓ < a0) ∨ (a0 ∈ Es ∧ 3 ≤ p) ∨
        (a0 ∈ Es ∧ p = 2 ∧ ∃ b ∈ Es \ Fs, a0 < b ∧ ∀ g ∈ gOf Es Fs a0, b < g)) := by
  by_cases h : (gOf Es Fs a0 = ∅ ∨ (∃ ℓ ∈ Es, ℓ < a0) ∨ (a0 ∈ Es ∧ 3 ≤ p) ∨
        (a0 ∈ Es ∧ p = 2 ∧ ∃ b ∈ Es \ Fs, a0 < b ∧ ∀ g ∈ gOf Es Fs a0, b < g))
  · have hx : xOf p Es Fs a0 = 0 := if_pos h
    exact ⟨fun h1 => absurd (hx ▸ h1) zero_ne_one, fun h1 => absurd h h1⟩
  · have hx : xOf p Es Fs a0 = 1 := if_neg h
    exact ⟨fun _ => h, fun _ => hx⟩

/-- Clause (4) in the words of the note: when some level beyond `a0` is in `Fs` and not in `Es`, and `g1` is
the first such level, "`∀ g ∈ gOf, b < g`" is "`b < g1`". -/
theorem clause4_first (Es Fs : Finset ℕ) (a0 g1 b : ℕ) (hg1 : g1 ∈ gOf Es Fs a0)
    (hfirst : ∀ g ∈ gOf Es Fs a0, g1 ≤ g) : (∀ g ∈ gOf Es Fs a0, b < g) ↔ b < g1 :=
  ⟨fun h => h g1 hg1, fun h g hg => lt_of_lt_of_le h (hfirst g hg)⟩

/-! ### 6. Mathlib's cyclotomic polynomials are the usual ones -/

-- monic, integer coefficients
#check @Polynomial.cyclotomic.monic
-- the product over the divisors of `n` is `X^n - 1`  (with monicity this determines them, by induction)
#check @Polynomial.prod_cyclotomic_eq_X_pow_sub_one
-- roots in a field of characteristic `0`: exactly the primitive `n`-th roots of unity
#check @Polynomial.isRoot_cyclotomic_iff
-- for a prime: `1 + X + ... + X^(p-1)`
#check @Polynomial.cyclotomic_prime
#check @Polynomial.cyclotomic_prime_pow_eq_geom_sum
-- the project's own bridge to Fourier zeros
#check @Pnq.zeroAtW_iff_cyclotomic_dvd

/-- `Φ_d ∣ f` in `ℤ[X]` is: `f` vanishes at a primitive `d`-th root of unity (any one of them) -/
theorem cyclotomic_dvd_iff_aeval (d : ℕ) (hd : 0 < d) (f : Polynomial ℤ) (ζ : ℂ) (hζ : IsPrimitiveRoot ζ d) :
    Polynomial.cyclotomic d ℤ ∣ f ↔ Polynomial.aeval ζ f = 0 := by
  have hint : IsIntegral ℤ ζ := hζ.isIntegral hd
  rw [Polynomial.cyclotomic_eq_minpoly hζ hd]
  constructor
  · rintro ⟨Q, rfl⟩
    rw [map_mul, minpoly.aeval, zero_mul]
  · intro h
    exact minpoly.isIntegrallyClosed_dvd hint h

/-- in particular at `e^{2πi/d}` -/
theorem cyclotomic_dvd_iff_exp (d : ℕ) (hd : 0 < d) (f : Polynomial ℤ) :
    Polynomial.cyclotomic d ℤ ∣ f ↔
      Polynomial.aeval (Complex.exp (2 * Real.pi * Complex.I / d)) f = 0 :=
  cyclotomic_dvd_iff_aeval d hd f _ (Complex.isPrimitiveRoot_exp d hd.ne')

/-- the value of the mask polynomial at a complex number -/
theorem aeval_maskW {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (ζ : ℂ) :
    Polynomial.aeval ζ (maskW w) = ∑ a : ZMod M, (w a : ℂ) * ζ ^ a.val := by
  simp [maskW]

/-- So "`Φ_d ∣ A(X)`" in the three theorems is: `∑ w(a) e^{2πi a/d} = 0`, the sum over the residues `a`
with their representatives in `[0, M)`. -/
theorem cyclotomic_dvd_maskW_iff {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (d : ℕ) (hd : 0 < d) :
    Polynomial.cyclotomic d ℤ ∣ maskW w ↔
      ∑ a : ZMod M, (w a : ℂ) * Complex.exp (2 * Real.pi * Complex.I / d) ^ a.val = 0 := by
  rw [cyclotomic_dvd_iff_exp d hd, aeval_maskW]

#print axioms Audit.cyclotomic_dvd_maskW_iff
#print axioms Audit.every_pattern
#print axioms Audit.maskW_coeff
#print axioms Audit.empty_pattern

/-! ### 7. An instance, to see that the hypotheses can be met: `Z_12`, `E = {1}`, `F = {2}`, `Φ_3 ∣ A` -/

instance : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩
instance : Fact (Nat.Prime 3) := ⟨Nat.prime_three⟩

example : IsLeast (Pat 2 3 2 True {1} {2}) 18 := by
  have h := least_balanced 2 3 2 (by decide) {1} {2} (by decide) (by decide) 1 (by decide) (by decide)
    (by intro ℓ h1 h2; omega) (by decide)
  have hv : minB 2 3 {1} {2} 1 = 18 := by decide
  rw [hv] at h
  exact h

end Audit
