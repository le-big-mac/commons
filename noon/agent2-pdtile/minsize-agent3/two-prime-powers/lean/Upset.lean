/-
Two prime powers: the patterns that are up-sets.  For `M = p^n * q^m` and an up-set `D` of the divisors of `M`,
a multiset on `ZMod M` whose mask polynomial is divisible by `Φ_d` for every `d ∈ D` is a sum of functions
periodic under the subgroups `c · ZMod M`, `c` a corner of `D` (a maximal divisor of `M` not in `D`); and the
least size of a multiset whose cyclotomic divisors are exactly `D` is the sum of `M / c` over the corners.
(Definitions and statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.
The proof on paper is a fresh instance's, on top of Proposition 6.3 of Kiss, Łaba, Marshall and Somlai.)
-/
import Pnq.Weighted
import Pnq.Upset1

open Finset

namespace Pnq

namespace Upset

/-- `D` is an up-set of the divisors of `M` that does not contain `1`: every element of `D` is a divisor of `M`
other than `1`, and with `d` it contains every multiple of `d` that divides `M`. -/
def IsUpSet (M : ℕ) (D : Finset ℕ) : Prop :=
  (∀ d ∈ D, d ∣ M ∧ d ≠ 1) ∧ ∀ d ∈ D, ∀ e, d ∣ e → e ∣ M → e ∈ D

/-- the corners of `D`: the maximal divisors of `M` that are not in `D` (maximal for divisibility) -/
def corners (M : ℕ) (D : Finset ℕ) : Finset ℕ :=
  (M.divisors \ D).filter (fun c => ∀ e ∈ M.divisors \ D, c ∣ e → e = c)

variable {p q n m : ℕ} [Fact p.Prime] [Fact q.Prime]

instance instNeZeroPowMulPow : NeZero (p ^ n * q ^ m) :=
  ⟨Nat.mul_ne_zero (pow_ne_zero _ (Fact.out : p.Prime).ne_zero) (pow_ne_zero _ (Fact.out : q.Prime).ne_zero)⟩

/-! Lemmas of the proof live in the namespace `Pnq.Upset.Aux` (here and in `Pnq/Upset1.lean`). -/

namespace Aux

/-! ### Corners -/

theorem mem_corners {M : ℕ} {D : Finset ℕ} {c : ℕ} :
    c ∈ corners M D ↔ c ∈ M.divisors \ D ∧ ∀ e ∈ M.divisors \ D, c ∣ e → e = c := by
  rw [corners, Finset.mem_filter]

theorem corner_dvd {M : ℕ} {D : Finset ℕ} {c : ℕ} (hc : c ∈ corners M D) : c ∣ M :=
  Nat.dvd_of_mem_divisors (Finset.mem_sdiff.1 (mem_corners.1 hc).1).1

theorem corner_not_mem {M : ℕ} {D : Finset ℕ} {c : ℕ} (hc : c ∈ corners M D) : c ∉ D :=
  (Finset.mem_sdiff.1 (mem_corners.1 hc).1).2

/-- `1` is a divisor of `M` that is not in the up-set -/
theorem one_mem {M : ℕ} (hM : M ≠ 0) {D : Finset ℕ} (hD : IsUpSet M D) : 1 ∈ M.divisors \ D :=
  Finset.mem_sdiff.2 ⟨Nat.mem_divisors.2 ⟨one_dvd _, hM⟩, fun h => (hD.1 1 h).2 rfl⟩

/-- every divisor of `M` that is not in `D` divides a corner -/
theorem exists_corner {M : ℕ} (D : Finset ℕ) (c : ℕ) (hc : c ∈ M.divisors \ D) :
    ∃ c' ∈ corners M D, c ∣ c' := by
  have hne : ((M.divisors \ D).filter (fun e => c ∣ e)).Nonempty :=
    ⟨c, Finset.mem_filter.2 ⟨hc, dvd_rfl⟩⟩
  have hmem := Finset.max'_mem _ hne
  refine ⟨_, ?_, (Finset.mem_filter.1 hmem).2⟩
  rw [mem_corners]
  refine ⟨(Finset.mem_filter.1 hmem).1, fun e he hdiv => ?_⟩
  have h1 : e ≤ Finset.max' _ hne :=
    Finset.le_max' _ e (Finset.mem_filter.2 ⟨he, (Finset.mem_filter.1 hmem).2.trans hdiv⟩)
  have hepos : 0 < e := Nat.pos_of_mem_divisors (Finset.mem_sdiff.1 he).1
  exact le_antisymm h1 (Nat.le_of_dvd hepos hdiv)

/-! ### Sums of functions periodic under the corners -/

/-- `A` is a sum, over the corners `c` of `D`, of functions with values in `ℕ` periodic under `c` -/
def Rep (M : ℕ) (D : Finset ℕ) (A : ZMod M → ℕ) : Prop :=
  ∃ g : ℕ → ZMod M → ℕ, (∀ c ∈ corners M D, ∀ x, g c (x + (c : ZMod M)) = g c x) ∧
    ∀ a, A a = ∑ c ∈ corners M D, g c a

/-- a function periodic under a divisor of `M` that is not in `D` is periodic under a corner -/
theorem rep_of_periodic {M : ℕ} (D : Finset ℕ) (c : ℕ) (hc : c ∈ M.divisors \ D) (A : ZMod M → ℕ)
    (hA : ∀ x, A (x + (c : ZMod M)) = A x) : Rep M D A := by
  obtain ⟨c', hc', hdvd⟩ := exists_corner D c hc
  refine ⟨fun e => if e = c' then A else 0, ?_, ?_⟩
  · intro e _ x
    by_cases h : e = c'
    · simp only [h, ite_true]
      exact periodic_of_dvd A c c' hdvd hA x
    · simp only [h, ite_false, Pi.zero_apply]
  · intro a
    rw [Finset.sum_eq_single_of_mem c' hc']
    · simp only [ite_true]
    · intro e _ he
      simp only [he, ite_false, Pi.zero_apply]

theorem rep_add {M : ℕ} {D : Finset ℕ} {A B : ZMod M → ℕ} (hA : Rep M D A) (hB : Rep M D B)
    (C : ZMod M → ℕ) (hC : ∀ x, C x = A x + B x) : Rep M D C := by
  obtain ⟨g, hg, hgA⟩ := hA
  obtain ⟨g', hg', hgB⟩ := hB
  refine ⟨fun c x => g c x + g' c x, ?_, ?_⟩
  · intro c hc x
    change g c (x + (c : ZMod M)) + g' c (x + (c : ZMod M)) = g c x + g' c x
    rw [hg c hc x, hg' c hc x]
  · intro a
    rw [hC a, hgA a, hgB a, ← Finset.sum_add_distrib]

/-! ### The induction, for any `M` with a chain of periods -/

/-- Let the divisors of `N₁` that do not divide `N₀` form a chain.  Then there is a divisor `t` of `M` not in
`D` such that every divisor of `N₁` that is not in `D` divides `N₀` or `t`. -/
theorem exists_top {M : ℕ} (hM : M ≠ 0) (D : Finset ℕ) (hD : IsUpSet M D) (N₁ N₀ : ℕ) (hN : N₁ ∣ M)
    (hchain : ∀ d d', d ∣ N₁ → d' ∣ N₁ → ¬ d ∣ N₀ → ¬ d' ∣ N₀ → d ∣ d' ∨ d' ∣ d) :
    ∃ t, t ∈ M.divisors \ D ∧ ∀ d, d ∣ N₁ → d ∉ D → d ∣ N₀ ∨ d ∣ t := by
  have hN0 : N₁ ≠ 0 := by
    intro h
    rw [h] at hN
    exact hM (Nat.eq_zero_of_zero_dvd hN)
  -- the divisors of `N₁` that are not in `D` and do not divide `N₀`
  obtain ⟨T, hT⟩ : ∃ T : Finset ℕ, ∀ d, d ∈ T ↔ d ∈ N₁.divisors ∧ d ∉ D ∧ ¬ d ∣ N₀ :=
    ⟨(N₁.divisors).filter (fun d => d ∉ D ∧ ¬ d ∣ N₀), fun d => Finset.mem_filter⟩
  by_cases hne : T.Nonempty
  · -- `t` is the largest of them
    obtain ⟨hm1, hm2, hm3⟩ := (hT _).1 (Finset.max'_mem T hne)
    have hm1' := Nat.dvd_of_mem_divisors hm1
    refine ⟨T.max' hne, Finset.mem_sdiff.2 ⟨Nat.mem_divisors.2 ⟨hm1'.trans hN, hM⟩, hm2⟩,
      fun d hd hdD => ?_⟩
    by_cases hd0 : d ∣ N₀
    · exact Or.inl hd0
    · right
      have hle := Finset.le_max' T d ((hT d).2 ⟨Nat.mem_divisors.2 ⟨hd, hN0⟩, hdD, hd0⟩)
      rcases hchain d _ hd hm1' hd0 hm3 with h | h
      · exact h
      · have h2 := Nat.le_of_dvd (Nat.pos_of_dvd_of_pos hd (Nat.pos_of_ne_zero hN0)) h
        rw [← le_antisymm hle h2]
  · -- there is none: `t = 1` will do
    refine ⟨1, one_mem hM hD, fun d hd hdD => Or.inl ?_⟩
    by_contra hd0
    exact hne ⟨d, (hT d).2 ⟨Nat.mem_divisors.2 ⟨hd, hN0⟩, hdD, hd0⟩⟩

/-- **The induction.**  Let `N 0 = 1`, and for `k < K` let `N (k + 1)` be a divisor of `M` whose divisors
that do not divide `N k` form a chain.  If `k ≤ K`, a function with values in `ℕ` that is periodic under
`N k` and has no Fourier mass at the frequencies whose order is in the up-set `D` is a sum of functions with
values in `ℕ` periodic under the corners of `D`. -/
theorem rep_of_filtration {M : ℕ} [NeZero M] (D : Finset ℕ) (hD : IsUpSet M D) (N : ℕ → ℕ)
    (h0 : N 0 = 1) (K : ℕ) (hdvd : ∀ k < K, N (k + 1) ∣ M)
    (hchain : ∀ k < K, ∀ d d', d ∣ N (k + 1) → d' ∣ N (k + 1) → ¬ d ∣ N k → ¬ d' ∣ N k →
      d ∣ d' ∨ d' ∣ d) :
    ∀ k ≤ K, ∀ A : ZMod M → ℕ, (∀ x, A (x + (N k : ZMod M)) = A x) →
      (∀ ξ : ZMod M, Pqr.ord ξ ∈ D → hatW A ξ = 0) → Rep M D A := by
  have hM : M ≠ 0 := NeZero.ne M
  intro k
  induction k with
  | zero =>
    intro _ A hA _
    rw [h0] at hA
    exact rep_of_periodic D 1 (one_mem hM hD) A hA
  | succ k ih =>
    intro hk A hA hz
    have hk' : k < K := hk
    obtain ⟨t, ht, htop⟩ := exists_top hM D hD (N (k + 1)) (N k) (hdvd k hk') (hchain k hk')
    have htM : t ∣ M := Nat.dvd_of_mem_divisors (Finset.mem_sdiff.1 ht).1
    have htD : t ∉ D := (Finset.mem_sdiff.1 ht).2
    -- the double difference of `A` along `N k` and `t` vanishes
    have hdd := dd_eq_zero A (N k : ZMod M) (t : ZMod M) (fun ξ => by
      by_cases hξD : Pqr.ord ξ ∈ D
      · exact Or.inl (hz ξ hξD)
      · by_cases hξN : Pqr.ord ξ ∣ N (k + 1)
        · rcases htop _ hξN hξD with h | h
          · exact Or.inr (Or.inl ((Pqr.Bridge.mul_natCast_eq_zero_iff ξ _).2 h))
          · exact Or.inr (Or.inr ((Pqr.Bridge.mul_natCast_eq_zero_iff ξ _).2 h))
        · exact Or.inl (hatW_eq_zero_of_periodic A _ ξ hA
            (fun h => hξN ((Pqr.Bridge.mul_natCast_eq_zero_iff ξ _).1 h))))
    obtain ⟨μ, ν, hμ, hν, hAμν⟩ := split A _ _ hdd
    -- `ν` is periodic under `t`, which is not in `D`
    have hνz : ∀ ξ : ZMod M, Pqr.ord ξ ∈ D → hatW ν ξ = 0 := fun ξ hξ =>
      hatW_eq_zero_of_periodic ν _ ξ hν
        (fun h => htD (hD.2 _ hξ t ((Pqr.Bridge.mul_natCast_eq_zero_iff ξ _).1 h) htM))
    -- so `μ`, periodic under `N k`, has the Fourier zeros of `A`
    have hμz : ∀ ξ : ZMod M, Pqr.ord ξ ∈ D → hatW μ ξ = 0 := by
      intro ξ hξ
      have h1 := hz ξ hξ
      rw [hatW_add μ ν A hAμν ξ, hνz ξ hξ, add_zero] at h1
      exact h1
    exact rep_add (ih (Nat.le_of_lt hk') μ hμ hμz) (rep_of_periodic D t ht ν hν) A hAμν

/-! ### The chain of periods of `ZMod (p^n * q^m)` -/

/-- the periods of the induction: `1`, then `p^k * q^m` for `k = 0, 1, …` -/
def per (p q m : ℕ) : ℕ → ℕ
  | 0 => 1
  | k + 1 => p ^ k * q ^ m

/-- a divisor of `p^k * q^m` that does not divide the period before it is `p^k * q^i` -/
theorem form_of_dvd {p q m : ℕ} (hp : p.Prime) (hq : q.Prime) (k d : ℕ) (hd : d ∣ p ^ k * q ^ m)
    (h : ¬ d ∣ per p q m k) : ∃ i, d = p ^ k * q ^ i := by
  obtain ⟨d₁, d₂, h1, h2, rfl⟩ := (Nat.dvd_mul).1 hd
  obtain ⟨a, ha, rfl⟩ := (Nat.dvd_prime_pow hp).1 h1
  obtain ⟨i, hi, rfl⟩ := (Nat.dvd_prime_pow hq).1 h2
  refine ⟨i, ?_⟩
  cases k with
  | zero =>
    rw [Nat.le_zero.1 ha]
  | succ k =>
    by_cases hak : a ≤ k
    · exact absurd (Nat.mul_dvd_mul (pow_dvd_pow p hak) (pow_dvd_pow q hi)) h
    · rw [show a = k + 1 by omega]

/-- the divisors of a period that do not divide the period before it form a chain -/
theorem chain {p q m : ℕ} (hp : p.Prime) (hq : q.Prime) (k d d' : ℕ) (hd : d ∣ per p q m (k + 1))
    (hd' : d' ∣ per p q m (k + 1)) (h : ¬ d ∣ per p q m k) (h' : ¬ d' ∣ per p q m k) :
    d ∣ d' ∨ d' ∣ d := by
  obtain ⟨i, rfl⟩ := form_of_dvd hp hq k d hd h
  obtain ⟨j, rfl⟩ := form_of_dvd hp hq k d' hd' h'
  rcases le_total i j with hij | hij
  · exact Or.inl (Nat.mul_dvd_mul_left _ (pow_dvd_pow q hij))
  · exact Or.inr (Nat.mul_dvd_mul_left _ (pow_dvd_pow q hij))

/-- every multiset on `ZMod (p^n * q^m)` without Fourier mass at the orders of the up-set `D` is a sum of
functions periodic under the corners -/
theorem rep_all (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D) (w : ZMod (p ^ n * q ^ m) → ℕ)
    (hz : ∀ ξ : ZMod (p ^ n * q ^ m), Pqr.ord ξ ∈ D → hatW w ξ = 0) : Rep (p ^ n * q ^ m) D w := by
  refine rep_of_filtration D hD (per p q m) rfl (n + 1)
    (fun k hk => Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.lt_succ_iff.1 hk)) _)
    (fun k _ => chain (Fact.out : p.Prime) (Fact.out : q.Prime) k) (n + 1) le_rfl w (fun x => ?_) hz
  change w (x + ((p ^ n * q ^ m : ℕ) : ZMod (p ^ n * q ^ m))) = w x
  rw [ZMod.natCast_self, add_zero]

end Aux

/-- **The structure theorem.** For an up-set `D`, the mask polynomial of `w` is divisible by `Φ_d` for every
`d ∈ D` if and only if `w` is a sum, over the corners `c` of `D`, of functions `g c` with values in `ℕ` that are
periodic under adding `c` (that is, constant on the cosets of the subgroup `c · ZMod M`, so each `g c` is a sum
of such cosets). -/
theorem structure_iff (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D)
    (w : ZMod (p ^ n * q ^ m) → ℕ) :
    (∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW w) ↔
      ∃ g : ℕ → ZMod (p ^ n * q ^ m) → ℕ,
        (∀ c ∈ corners (p ^ n * q ^ m) D, ∀ x, g c (x + (c : ZMod (p ^ n * q ^ m))) = g c x) ∧
        ∀ a, w a = ∑ c ∈ corners (p ^ n * q ^ m) D, g c a := by
  constructor
  · intro h
    exact Aux.rep_all D hD w
      (fun ξ hξ => (zeroAtW_iff_cyclotomic_dvd w _ (hD.1 _ hξ).1).2 (h _ hξ) ξ rfl)
  · rintro ⟨g, hg, hw⟩ d hd
    rw [← zeroAtW_iff_cyclotomic_dvd w d (hD.1 d hd).1]
    intro ξ hξ
    rw [Aux.hatW_sum _ g w hw ξ]
    refine Finset.sum_eq_zero fun c hc => ?_
    refine Aux.hatW_eq_zero_of_periodic (g c) _ ξ (hg c hc) ?_
    rw [Ne, Pqr.Bridge.mul_natCast_eq_zero_iff, hξ]
    exact fun hdc => Aux.corner_not_mem hc (hD.2 d hd c hdc (Aux.corner_dvd hc))

/-- **The lower bound.** If the mask polynomial of `w` is divisible by `Φ_d` for every `d` of the up-set `D` and
by `Φ_c` for no corner `c` of `D`, then `w` has at least `∑ M / c` elements, the sum over the corners. -/
theorem lower_bound (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D)
    (w : ZMod (p ^ n * q ^ m) → ℕ) (hdiv : ∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW w)
    (hcor : ∀ c ∈ corners (p ^ n * q ^ m) D, ¬ Polynomial.cyclotomic c ℤ ∣ maskW w) :
    ∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c ≤ ∑ a, w a := by
  obtain ⟨g, hg, hw⟩ := (structure_iff hpq D hD w).1 hdiv
  -- the part `g c` of every corner `c` is not zero, so it has at least `M / c` elements
  have key : ∀ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c ≤ ∑ a, g c a := by
    intro c hc
    have hcM := Aux.corner_dvd hc
    by_contra hlt
    have hzero : ∀ x, g c x = 0 := by
      intro x
      by_contra hx
      exact hlt (Aux.div_le_sum_of_periodic c hcM (g c) (hg c hc) x hx)
    apply hcor c hc
    rw [← zeroAtW_iff_cyclotomic_dvd w c hcM]
    intro ξ hξ
    rw [Aux.hatW_sum _ g w hw ξ]
    refine Finset.sum_eq_zero fun c' hc' => ?_
    by_cases hcc : c' = c
    · rw [hcc, hatW]
      refine Finset.sum_eq_zero fun a _ => ?_
      rw [hzero a, Nat.cast_zero, zero_mul]
    · refine Aux.hatW_eq_zero_of_periodic (g c') _ ξ (hg c' hc') ?_
      rw [Ne, Pqr.Bridge.mul_natCast_eq_zero_iff, hξ]
      exact fun hdvd => hcc ((Aux.mem_corners.1 hc).2 c' (Aux.mem_corners.1 hc').1 hdvd)
  calc ∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c
      ≤ ∑ c ∈ corners (p ^ n * q ^ m) D, ∑ a, g c a := Finset.sum_le_sum key
    _ = ∑ a, w a := by
        rw [Finset.sum_comm]
        exact Finset.sum_congr rfl fun a _ => (hw a).symm

/-- **Least size for an up-set pattern.** Among the multisets on `ZMod (p^n * q^m)` that are not empty and whose
mask polynomial is divisible by `Φ_d`, for `d ∣ p^n q^m`, `d ≠ 1`, exactly when `d ∈ D`, the least number of
elements is the sum of `M / c` over the corners of `D`. -/
theorem least_size (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q ^ m) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
        ∀ d, d ∣ p ^ n * q ^ m → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)}
      (∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c) := by
  have hM : p ^ n * q ^ m ≠ 0 := NeZero.ne _
  have hpos : ∀ c ∈ corners (p ^ n * q ^ m) D, 0 < p ^ n * q ^ m / c := fun c hc =>
    Nat.div_pos (Nat.le_of_dvd (Nat.pos_of_ne_zero hM) (Aux.corner_dvd hc))
      (Nat.pos_of_dvd_of_pos (Aux.corner_dvd hc) (Nat.pos_of_ne_zero hM))
  constructor
  · -- attained by the sum of the subgroups `c · ZMod M`, `c` a corner
    refine ⟨fun a => ∑ c ∈ corners (p ^ n * q ^ m) D, if c ∣ a.val then 1 else 0, ?_, ?_, ?_⟩
    · rw [Finset.sum_comm]
      exact Finset.sum_congr rfl fun c hc => Aux.sum_dvd_val_one c (Aux.corner_dvd hc)
    · obtain ⟨c, hc, -⟩ := Aux.exists_corner D 1 (Aux.one_mem hM hD)
      exact Finset.sum_pos hpos ⟨c, hc⟩
    · intro d hd _
      rw [← zeroAtW_iff_cyclotomic_dvd _ d hd]
      constructor
      · intro hz
        by_contra hdD
        obtain ⟨c, hc, hdc⟩ := Aux.exists_corner D d
          (Finset.mem_sdiff.2 ⟨Nat.mem_divisors.2 ⟨hd, hM⟩, hdD⟩)
        have h1 := hz _ (Pqr.ord_natCast_div' hd)
        rw [Aux.hatW_multiples _ (fun c hc => Aux.corner_dvd hc), Pqr.ord_natCast_div' hd] at h1
        have h2 : (∑ c ∈ corners (p ^ n * q ^ m) D, if d ∣ c then p ^ n * q ^ m / c else 0) = 0 := by
          exact_mod_cast h1
        have h3 := (Finset.sum_eq_zero_iff.1 h2) c hc
        rw [ite_eq_left hdc] at h3
        exact (hpos c hc).ne' h3
      · intro hdD ξ hξ
        rw [Aux.hatW_multiples _ (fun c hc => Aux.corner_dvd hc), hξ, Finset.sum_eq_zero, Nat.cast_zero]
        intro c hc
        exact ite_eq_right fun hdc => Aux.corner_not_mem hc (hD.2 d hdD c hdc (Aux.corner_dvd hc))
  · rintro s ⟨w, rfl, hs, hw⟩
    refine lower_bound hpq D hD w (fun d hd => (hw d (hD.1 d hd).1 (hD.1 d hd).2).2 hd)
      (fun c hc hdiv => ?_)
    by_cases hc1 : c = 1
    · rw [hc1] at hdiv
      have hz := (zeroAtW_iff_cyclotomic_dvd w 1 (one_dvd _)).2 hdiv 0 ((Pqr.ord_eq_one_iff 0).2 rfl)
      rw [Aux.hatW_zero] at hz
      have h0 : ∑ a, w a = 0 := by exact_mod_cast hz
      exact hs.ne' h0
    · exact Aux.corner_not_mem hc ((hw c (Aux.corner_dvd hc) hc1).1 hdiv)

end Upset

end Pnq
