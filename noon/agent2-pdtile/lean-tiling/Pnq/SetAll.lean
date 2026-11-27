/-
Sets on larger groups.  If `s` is divisible by `r^j`, `r` an odd prime, then for every size `t < r^j` a SET of `t` elements on
`ZMod (p^n * q * s)` with exactly a given pattern of divisors of `p^n * q` exists exactly when a multiset of `t` elements with that
pattern exists on `ZMod (p^n * q)`.  So when the least size that the theorem gives is below `r^j`, it is also the least size of a set
on `ZMod (p^n * q * s)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  On paper: lift a multiset along the factors
2 of `s`, then along `r^j` to a set, then along the other odd prime factors; a lift of a set is a set.)
-/
import Pnq.LiftAll
import Pnq.SetLift

open Finset

namespace Pnq

namespace Lift

namespace SetAllAux

/-- the numbers of elements of the nonempty SETS on `ZMod M` whose mask is divisible by `Φ_d`, for `d ∣ M`, `d ≠ 1`, exactly
when `d ∈ P` (as `AllAux.sizes`, with sets in place of multisets) -/
def setSizes (M : ℕ) [NeZero M] (P : Finset ℕ) : Set ℕ :=
  {t | ∃ A : Finset (ZMod M), A.card = t ∧ 0 < t ∧
      ∀ d, d ∣ M → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW (indW A) ↔ d ∈ P)}

/-- equal moduli, equal sets of sizes of sets -/
theorem setSizes_congr {M M' : ℕ} [NeZero M] [NeZero M'] (h : M = M') (P : Finset ℕ) :
    setSizes M P = setSizes M' P := by
  subst h
  rfl

/-- the multiset of a set has as many elements as the set -/
theorem sum_indW {M : ℕ} [NeZero M] (A : Finset (ZMod M)) : ∑ x, indW A x = A.card := by
  simp only [indW]
  rw [Fintype.sum_ite_mem, Finset.sum_const, smul_eq_mul, mul_one]

/-- a set is a multiset: every size of a set with exactly the pattern `P` is a size of a multiset with exactly `P` -/
theorem setSizes_subset_sizes (M : ℕ) [NeZero M] (P : Finset ℕ) : setSizes M P ⊆ AllAux.sizes M P := by
  rintro t ⟨A, hc, hpos, hpat⟩
  exact ⟨indW A, (sum_indW A).trans hc, hpos, hpat⟩

/-- **From a multiset to a set, along `r^j`.**  `r` an odd prime, `P` a set of divisors of `N`, `t < r^j`.  If a multiset of
`t` elements on `ZMod N` has exactly the pattern `P`, so has a set of `t` elements on `ZMod (N * r^j)`.  (By
`exists_set_lift`: every multiplicity is at most `t < r^j`, and some multiplicity is not `0`.) -/
theorem setSizes_of_sizes {N r : ℕ} [NeZero N] [Fact r.Prime] (hr : r ≠ 2) (j : ℕ) (P : Finset ℕ)
    (hP : ∀ d ∈ P, d ∣ N) {t : ℕ} (ht : t < r ^ j) (h : t ∈ AllAux.sizes N P) :
    t ∈ setSizes (N * r ^ j) P := by
  obtain ⟨w, hsum, hpos, hpat⟩ := h
  have hlt : ∀ x, w x < r ^ j := fun x =>
    lt_of_le_of_lt
      ((Finset.single_le_sum (fun _ _ => Nat.zero_le _) (Finset.mem_univ x)).trans hsum.le) ht
  obtain ⟨x₀, hx₀⟩ := Aux.exists_ne_zero_of_sum_pos w (lt_of_lt_of_eq hpos hsum.symm)
  obtain ⟨A, hfib, hdiv⟩ := exists_set_lift hr j w (fun x => (hlt x).le) ⟨x₀, hx₀, (hlt x₀).ne⟩
  refine ⟨A, ?_, hpos, fun d hd hd1 => ?_⟩
  · rw [Finset.card_eq_sum_card_fiberwise
      (f := fun y => ZMod.castHom (Nat.dvd_mul_right N (r ^ j)) (ZMod N) y) (t := Finset.univ)
      (fun _ _ => Finset.mem_univ _), Finset.sum_congr rfl fun x _ => hfib x]
    exact hsum
  · rw [hdiv d hd]
    by_cases hdN : d ∣ N
    · rw [and_iff_right hdN]
      exact hpat d hdN hd1
    · exact iff_of_false (fun hc => hdN hc.1) fun hc => hdN (hP d hc)

section Up

variable (p q n s r j : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] [NeZero s]

/-- **From a multiset on `ZMod (p^n * q)` to a set on `ZMod (p^n * q * s)`**, `r^j ∣ s`, `t < r^j`: write `s = r^j * s₁`, go
to a multiset on `ZMod (p^n * q * s₁)` by `sizes_eq_mul`, then to a set on `ZMod (p^n * q * s₁ * r^j)` by
`setSizes_of_sizes`. -/
theorem mem_setSizes_mul (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s) (P : Finset ℕ)
    (hP : ∀ d ∈ P, d ∣ p ^ n * q) {t : ℕ} (ht : t < r ^ j) (h : t ∈ AllAux.sizes (p ^ n * q) P) :
    t ∈ setSizes (p ^ n * q * s) P := by
  obtain ⟨s₁, rfl⟩ := hs
  have hs₁ : s₁ ≠ 0 := by
    rintro rfl
    exact NeZero.ne (r ^ j * 0) (mul_zero _)
  have : NeZero s₁ := ⟨hs₁⟩
  have h1 : t ∈ AllAux.sizes (p ^ n * q * s₁) P := by
    rw [show AllAux.sizes (p ^ n * q * s₁) P = AllAux.sizes (p ^ n * q) P from
      sizes_eq_mul p q n s₁ hpq P hP]
    exact h
  have h2 : t ∈ setSizes (p ^ n * q * s₁ * r ^ j) P :=
    setSizes_of_sizes hr j P (fun d hd => Dvd.dvd.mul_right (hP d hd) s₁) ht h1
  rw [← setSizes_congr (show p ^ n * q * s₁ * r ^ j = p ^ n * q * (r ^ j * s₁) by ring) P]
  exact h2

/-- **Going up to a set.**  A nonempty multiset on `ZMod (p^n * q)` with fewer than `r^j` elements has a companion SET on
`ZMod (p^n * q * s)`, `r^j ∣ s`, with the same number of elements, the same `Φ_d` for the divisors `d ≠ 1` of `p^n * q`, and
no `Φ_d` for a divisor `d` of `p^n * q * s` that does not divide `p^n * q`.  (As `AllAux.exists_up`: take for the pattern
the set of the divisors `d` of `p^n * q` with `Φ_d` dividing the mask.) -/
theorem exists_up_set (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s) (w : ZMod (p ^ n * q) → ℕ)
    (hpos : 0 < ∑ x, w x) (hlt : ∑ x, w x < r ^ j) :
    ∃ A : Finset (ZMod (p ^ n * q * s)), A.card = ∑ x, w x ∧
      (∀ d, d ∣ p ^ n * q → d ≠ 1 →
        (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ Polynomial.cyclotomic d ℤ ∣ maskW (indW A))) ∧
      ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW (indW A) := by
  classical
  let P : Finset ℕ := (Nat.divisors (p ^ n * q)).filter fun d => Polynomial.cyclotomic d ℤ ∣ maskW w
  have hP : ∀ d ∈ P, d ∣ p ^ n * q := fun d hd => Nat.dvd_of_mem_divisors (Finset.mem_filter.1 hd).1
  have hmem : ∀ d, d ∣ p ^ n * q → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P) := fun d hd =>
    ⟨fun hc => Finset.mem_filter.2 ⟨Nat.mem_divisors.2 ⟨hd, NeZero.ne (p ^ n * q)⟩, hc⟩,
      fun hc => (Finset.mem_filter.1 hc).2⟩
  have hin : (∑ x, w x) ∈ AllAux.sizes (p ^ n * q) P := ⟨w, rfl, hpos, fun d hd _ => hmem d hd⟩
  obtain ⟨A, hc, -, hpat⟩ := mem_setSizes_mul p q n s r j hpq hr hs P hP hlt hin
  refine ⟨A, hc,
    fun d hd hd1 => (hmem d hd).trans (hpat d (Dvd.dvd.mul_right hd s) hd1).symm,
    fun d hd hnd hc' => ?_⟩
  have hd1 : d ≠ 1 := by
    rintro rfl
    exact hnd (one_dvd (p ^ n * q))
  exact hnd (hP d ((hpat d hd hd1).1 hc'))

end Up

end SetAllAux

section Sets

variable (p q n s r j : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] [NeZero s]

/-- **Sizes below `r^j`: sets on `ZMod (p^n * q * s)` against multisets on `ZMod (p^n * q)`.** -/
theorem set_sizes_iff_mul (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ p ^ n * q)
    (t : ℕ) (ht : t < r ^ j) :
    (∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW (indW A) ↔ d ∈ P)) ↔
    (∃ w : ZMod (p ^ n * q) → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)) := by
  constructor
  · intro h
    have hin : t ∈ AllAux.sizes (p ^ n * q * s) P := SetAllAux.setSizes_subset_sizes (p ^ n * q * s) P h
    rw [show AllAux.sizes (p ^ n * q * s) P = AllAux.sizes (p ^ n * q) P from
      sizes_eq_mul p q n s hpq P hP] at hin
    exact hin
  · intro h
    exact SetAllAux.mem_setSizes_mul p q n s r j hpq hr hs P hP ht h

/-- **Unbalanced patterns, sets on `ZMod (p^n * q * s)`.** -/
theorem minsize_unbalanced_set (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (hm : minU p q Es Fs < r ^ j) :
    IsLeast {t | ∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW (indW A) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW (indW A)}
      (minU p q Es Fs) := by
  have hold := minsize_unbalanced_zmod p q n hpq Es Fs hE hF
  constructor
  · obtain ⟨w, hsum, h0, hEw, hFw⟩ := hold.1
    obtain ⟨A, hc, hsame, hnew⟩ := SetAllAux.exists_up_set p q n s r j hpq hr hs w
      (AllAux.sum_pos_of_exists (Aux.exists_ne_zero_of_not_dvd h0)) (lt_of_eq_of_lt hsum hm)
    exact ⟨A, hc.trans hsum, fun h => h0 ((AllAux.dvd_q_iff hsame).2 h),
      (AllAux.levelsE_iff hsame hE).1 hEw, (AllAux.levelsF_iff hsame hF).1 hFw, hnew⟩
  · rintro t ⟨A, hc, h0, hEw, hFw, hnew⟩
    exact (minsize_unbalanced_mul p q n s hpq Es Fs hE hF).2
      ⟨indW A, (SetAllAux.sum_indW A).trans hc, h0, hEw, hFw, hnew⟩

/-- **Balanced patterns with every `Φ_{p^ℓ q}`, sets on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_all_set (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hm : q * p ^ Es.card < r ^ j) :
    IsLeast {t | ∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ 0 < t ∧ Polynomial.cyclotomic q ℤ ∣ maskW (indW A) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW (indW A)) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW (indW A)}
      (q * p ^ Es.card) := by
  have hold := minsize_balanced_all_zmod p q n hpq Es hE
  constructor
  · obtain ⟨w, hsum, hpos, h0, hEw, hFw⟩ := hold.1
    obtain ⟨A, hc, hsame, hnew⟩ := SetAllAux.exists_up_set p q n s r j hpq hr hs w
      (lt_of_lt_of_eq hpos hsum.symm) (lt_of_eq_of_lt hsum hm)
    exact ⟨A, hc.trans hsum, hpos, (AllAux.dvd_q_iff hsame).1 h0,
      (AllAux.levelsE_iff hsame hE).1 hEw, (AllAux.levelsF_all_iff hsame).1 hFw, hnew⟩
  · rintro t ⟨A, hc, hpos, h0, hEw, hFw, hnew⟩
    exact (minsize_balanced_all_mul p q n s hpq Es hE).2
      ⟨indW A, (SetAllAux.sum_indW A).trans hc, hpos, h0, hEw, hFw, hnew⟩

/-- **Balanced patterns with a first level `a0` at which `Φ_{p^a0 q} ∤ A(X)`, sets on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_set (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) (hm : minB p q Es Fs a0 < r ^ j) :
    IsLeast {t | ∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ Polynomial.cyclotomic q ℤ ∣ maskW (indW A) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW (indW A)}
      (minB p q Es Fs a0) := by
  have hold := minsize_balanced_zmod p q n hpq Es Fs hE hF a0 ha1 han hlow hna
  constructor
  · obtain ⟨w, hsum, h0, hEw, hFw⟩ := hold.1
    have hnd : ¬ Polynomial.cyclotomic (p ^ a0 * q) ℤ ∣ maskW w := fun h =>
      hna (((Aux.levelsFW_eq_iff w hF).1 hFw a0 (Finset.mem_Icc.2 ⟨ha1, han⟩)).1 h)
    obtain ⟨A, hc, hsame, hnew⟩ := SetAllAux.exists_up_set p q n s r j hpq hr hs w
      (AllAux.sum_pos_of_exists (Aux.exists_ne_zero_of_not_dvd hnd)) (lt_of_eq_of_lt hsum hm)
    exact ⟨A, hc.trans hsum, (AllAux.dvd_q_iff hsame).1 h0,
      (AllAux.levelsE_iff hsame hE).1 hEw, (AllAux.levelsF_iff hsame hF).1 hFw, hnew⟩
  · rintro t ⟨A, hc, h0, hEw, hFw, hnew⟩
    exact (minsize_balanced_mul p q n s hpq Es Fs hE hF a0 ha1 han hlow hna).2
      ⟨indW A, (SetAllAux.sum_indW A).trans hc, h0, hEw, hFw, hnew⟩

end Sets

end Lift

end Pnq
