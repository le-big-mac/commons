/-
Lemmas for `Pnq/Upset.lean` that hold in any cyclic group `ZMod M` and do not mention up-sets or corners:

* `hatW_eq_zero_of_periodic` (F1): a function periodic under `c` has no Fourier mass at the frequencies `ξ`
  with `ξ * c ≠ 0`;
* `dd_eq_zero` (F1 and F2): if at every frequency `ξ` either the transform of `A` vanishes or `ξ * s = 0` or
  `ξ * t = 0`, then the double difference of `A` along `s` and `t` vanishes;
* `split` (F3): a function with values in `ℕ` whose double difference along `s` and `t` vanishes is the sum of
  a function periodic under `s` and a function periodic under `t`, both with values in `ℕ`;
* sums: the transform of a sum, the number of multiples of a divisor of `M`, the least size of a nonzero
  function periodic under a divisor of `M`, and the transform of a sum of indicators of subgroups.
-/
import Pnq.Weighted

open Finset

namespace Pnq

namespace Upset

namespace Aux

variable {M : ℕ} [NeZero M]

/-! ### The transform of a translate (F1) -/

/-- the transform of the translate of `f` by `c` is a character value times the transform of `f` -/
theorem sum_shift_mul_char (f : ZMod M → ℂ) (c ξ : ZMod M) :
    ∑ a : ZMod M, f (a + c) * ZMod.stdAddChar (ξ * a)
      = ZMod.stdAddChar (-(ξ * c)) * ∑ a : ZMod M, f a * ZMod.stdAddChar (ξ * a) := by
  rw [Finset.mul_sum, ← Equiv.sum_comp (Equiv.addRight c)
    (fun b => ZMod.stdAddChar (-(ξ * c)) * (f b * ZMod.stdAddChar (ξ * b)))]
  refine Finset.sum_congr rfl fun a _ => ?_
  have h : (ZMod.stdAddChar (ξ * a) : ℂ)
      = ZMod.stdAddChar (-(ξ * c)) * ZMod.stdAddChar (ξ * (a + c)) := by
    rw [← AddChar.map_add_eq_mul]
    congr 1
    ring
  rw [Equiv.coe_addRight, h]
  ring

/-- the character value at a nonzero element is not `1` -/
theorem stdAddChar_ne_one {y : ZMod M} (hy : y ≠ 0) : (ZMod.stdAddChar y : ℂ) ≠ 1 := by
  intro h1
  rw [← AddChar.map_zero_eq_one (ZMod.stdAddChar (N := M))] at h1
  exact hy (ZMod.injective_stdAddChar h1)

/-- (F1) a function periodic under `c` has no Fourier mass at the frequencies `ξ` with `ξ * c ≠ 0` -/
theorem hatW_eq_zero_of_periodic (A : ZMod M → ℕ) (c ξ : ZMod M) (hA : ∀ x, A (x + c) = A x)
    (hξ : ξ * c ≠ 0) : hatW A ξ = 0 := by
  have h := sum_shift_mul_char (fun a => (A a : ℂ)) c ξ
  simp only [hA] at h
  have hne : (ZMod.stdAddChar (-(ξ * c)) : ℂ) ≠ 1 := stdAddChar_ne_one (neg_ne_zero.2 hξ)
  have h2 : (1 - (ZMod.stdAddChar (-(ξ * c)) : ℂ)) * hatW A ξ = 0 := by
    rw [hatW]
    linear_combination h
  exact (mul_eq_zero.1 h2).resolve_left (sub_ne_zero.2 (Ne.symm hne))

/-! ### The double difference (F1 with F2) -/

/-- If at every frequency `ξ` the transform of `A` vanishes, or `ξ * s = 0`, or `ξ * t = 0`, then the double
difference of `A` along `s` and `t` vanishes. -/
theorem dd_eq_zero (A : ZMod M → ℕ) (s t : ZMod M)
    (h : ∀ ξ : ZMod M, hatW A ξ = 0 ∨ ξ * s = 0 ∨ ξ * t = 0) (x : ZMod M) :
    A (x + s + t) + A x = A (x + s) + A (x + t) := by
  have h0 := Pqr.Bridge.fourier_uniq_zmod
    (fun x => (A (x + s + t) : ℂ) + A x - A (x + s) - A (x + t)) (fun ξ => by
      have e1 := sum_shift_mul_char (fun a => (A a : ℂ)) s ξ
      have e2 := sum_shift_mul_char (fun a => (A a : ℂ)) t ξ
      have e3 := sum_shift_mul_char (fun a => (A a : ℂ)) (s + t) ξ
      have e4 : (ZMod.stdAddChar (-(ξ * (s + t))) : ℂ)
          = ZMod.stdAddChar (-(ξ * s)) * ZMod.stdAddChar (-(ξ * t)) := by
        rw [← AddChar.map_add_eq_mul]
        congr 1
        ring
      simp only [← add_assoc] at e3
      simp only [sub_mul, add_mul, Finset.sum_sub_distrib, Finset.sum_add_distrib]
      rw [e1, e2, e3, e4]
      have hF : ∑ a : ZMod M, (A a : ℂ) * ZMod.stdAddChar (ξ * a) = hatW A ξ := rfl
      rw [hF]
      rcases h ξ with h1 | h1 | h1
      · rw [h1]
        ring
      · rw [h1, neg_zero, AddChar.map_zero_eq_one]
        ring
      · rw [h1, neg_zero, AddChar.map_zero_eq_one]
        ring)
  have h1 : (A (x + s + t) : ℂ) + A x - A (x + s) - A (x + t) = 0 := congrFun h0 x
  have h2 : ((A (x + s + t) + A x : ℕ) : ℂ) = ((A (x + s) + A (x + t) : ℕ) : ℂ) := by
    push_cast
    linear_combination h1
  exact_mod_cast h2

/-! ### Splitting (F3) -/

omit [NeZero M] in
/-- a function periodic under `c` is periodic under the multiples of `c` -/
theorem periodic_nsmul {α : Type*} (A : ZMod M → α) (c : ZMod M) (hA : ∀ x, A (x + c) = A x) (j : ℕ)
    (x : ZMod M) : A (x + j • c) = A x := by
  induction j with
  | zero => simp
  | succ j ih => rw [succ_nsmul, ← add_assoc, hA, ih]

omit [NeZero M] in
/-- a function periodic under a number `c` is periodic under the multiples of `c` -/
theorem periodic_of_dvd {α : Type*} (A : ZMod M → α) (c c' : ℕ) (h : c ∣ c')
    (hA : ∀ x, A (x + (c : ZMod M)) = A x) (x : ZMod M) : A (x + (c' : ZMod M)) = A x := by
  obtain ⟨j, rfl⟩ := h
  have h1 := periodic_nsmul A (c : ZMod M) hA j x
  have h2 : ((c * j : ℕ) : ZMod M) = j • (c : ZMod M) := by
    rw [nsmul_eq_mul, Nat.cast_mul, mul_comm]
  rw [h2, h1]

/-- (F3) A function with values in `ℕ` whose double difference along `s` and `t` vanishes is the sum of a
function periodic under `s` and a function periodic under `t`, both with values in `ℕ`.  The first is the
minimum of `A` over the coset `x + ⟨s⟩`. -/
theorem split (A : ZMod M → ℕ) (s t : ZMod M)
    (h : ∀ x, A (x + s + t) + A x = A (x + s) + A (x + t)) :
    ∃ μ ν : ZMod M → ℕ, (∀ x, μ (x + s) = μ x) ∧ (∀ x, ν (x + t) = ν x) ∧ ∀ x, A x = μ x + ν x := by
  -- the difference along `t` is the same at `x` and at `x + k • s`
  have hk : ∀ (k : ℕ) (x : ZMod M), A (x + k • s + t) + A x = A (x + k • s) + A (x + t) := by
    intro k
    induction k with
    | zero =>
      intro x
      rw [zero_nsmul, add_zero, add_comm]
    | succ k ih =>
      intro x
      have h1 := h (x + k • s)
      have h2 := ih x
      have e : x + (k + 1) • s = x + k • s + s := by
        rw [succ_nsmul, add_assoc]
      rw [e]
      omega
  have key : ∀ (x i : ZMod M), A (x + t + i * s) + A x = A (x + i * s) + A (x + t) := by
    intro x i
    have h1 := hk i.val x
    rw [nsmul_eq_mul, ZMod.natCast_zmod_val] at h1
    have e : x + t + i * s = x + i * s + t := by ring
    rw [e]
    exact h1
  -- the minimum over the coset
  obtain ⟨μ, hle, hex⟩ : ∃ μ : ZMod M → ℕ, (∀ x i : ZMod M, μ x ≤ A (x + i * s)) ∧
      ∀ x, ∃ i : ZMod M, μ x = A (x + i * s) := by
    refine ⟨fun x => Finset.univ.inf' Finset.univ_nonempty (fun i : ZMod M => A (x + i * s)), ?_, ?_⟩
    · intro x i
      exact Finset.inf'_le (fun i : ZMod M => A (x + i * s)) (Finset.mem_univ i)
    · intro x
      obtain ⟨i, -, hi⟩ := Finset.exists_mem_eq_inf' Finset.univ_nonempty
        (fun i : ZMod M => A (x + i * s))
      exact ⟨i, hi⟩
  have hμs : ∀ x, μ (x + s) = μ x := by
    intro x
    apply le_antisymm
    · obtain ⟨i, hi⟩ := hex x
      have h1 := hle (x + s) (i - 1)
      have e : x + s + (i - 1) * s = x + i * s := by ring
      rw [e] at h1
      omega
    · obtain ⟨i, hi⟩ := hex (x + s)
      have h1 := hle x (i + 1)
      have e : x + (i + 1) * s = x + s + i * s := by ring
      rw [e] at h1
      omega
  have hμA : ∀ x, μ x ≤ A x := by
    intro x
    have h1 := hle x 0
    rw [zero_mul, add_zero] at h1
    exact h1
  have hμt : ∀ x, μ (x + t) + A x = μ x + A (x + t) := by
    intro x
    apply le_antisymm
    · obtain ⟨i, hi⟩ := hex x
      have h1 := hle (x + t) i
      have h2 := key x i
      omega
    · obtain ⟨i, hi⟩ := hex (x + t)
      have h1 := hle x i
      have h2 := key x i
      omega
  refine ⟨μ, fun x => A x - μ x, hμs, ?_, ?_⟩
  · intro x
    have h1 := hμt x
    have h2 := hμA x
    have h3 := hμA (x + t)
    change A (x + t) - μ (x + t) = A x - μ x
    omega
  · intro x
    have h2 := hμA x
    change A x = μ x + (A x - μ x)
    omega

/-! ### Sums -/

/-- the transform of a sum of two functions -/
theorem hatW_add (A B C : ZMod M → ℕ) (h : ∀ x, C x = A x + B x) (ξ : ZMod M) :
    hatW C ξ = hatW A ξ + hatW B ξ := by
  rw [hatW, hatW, hatW, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [h a]
  push_cast
  ring

/-- the transform of a finite sum of functions -/
theorem hatW_sum {ι : Type*} (S : Finset ι) (g : ι → ZMod M → ℕ) (w : ZMod M → ℕ)
    (h : ∀ a, w a = ∑ c ∈ S, g c a) (ξ : ZMod M) : hatW w ξ = ∑ c ∈ S, hatW (g c) ξ := by
  simp only [hatW]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [h a, Nat.cast_sum, Finset.sum_mul]

/-- the transform at the frequency `0` is the number of elements -/
theorem hatW_zero (w : ZMod M → ℕ) : hatW w 0 = ((∑ a, w a : ℕ) : ℂ) := by
  simp [hatW]

/-- the number of multiples of a divisor `c` of `M` in `ZMod M` -/
theorem sum_dvd_val_one (c : ℕ) (hc : c ∣ M) :
    ∑ a : ZMod M, (if c ∣ a.val then 1 else 0) = M / c := by
  have h := Pqr.Bridge.sum_dvd_val c hc (fun _ : ZMod M => (1 : ℂ))
  rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one] at h
  have h2 : ((∑ a : ZMod M, (if c ∣ a.val then 1 else 0) : ℕ) : ℂ) = ((M / c : ℕ) : ℂ) := by
    rw [← h, Nat.cast_sum]
    refine Finset.sum_congr rfl fun a _ => ?_
    split_ifs <;> simp
  exact_mod_cast h2

/-- a function with values in `ℕ` that is periodic under a divisor `c` of `M` and is not zero has at least
`M / c` elements -/
theorem div_le_sum_of_periodic (c : ℕ) (hc : c ∣ M) (g : ZMod M → ℕ)
    (hg : ∀ x, g (x + (c : ZMod M)) = g x) (x : ZMod M) (hx : g x ≠ 0) : M / c ≤ ∑ a, g a := by
  rw [← sum_dvd_val_one c hc, ← Equiv.sum_comp (Equiv.addLeft x) g]
  refine Finset.sum_le_sum fun a _ => ?_
  split_ifs with h
  · obtain ⟨j, hj⟩ := h
    have ha : a = j • (c : ZMod M) := by
      rw [← ZMod.natCast_zmod_val a, hj, nsmul_eq_mul, Nat.cast_mul, mul_comm]
    rw [Equiv.coe_addLeft, ha, periodic_nsmul g _ hg]
    exact Nat.one_le_iff_ne_zero.2 hx
  · exact Nat.zero_le _

/-- the transform of the sum of the indicators of the subgroups `c · ZMod M`, `c ∈ S` -/
theorem hatW_multiples (S : Finset ℕ) (hS : ∀ c ∈ S, c ∣ M) (ξ : ZMod M) :
    hatW (fun a : ZMod M => ∑ c ∈ S, if c ∣ a.val then 1 else 0) ξ
      = ((∑ c ∈ S, if Pqr.ord ξ ∣ c then M / c else 0 : ℕ) : ℂ) := by
  simp only [hatW]
  rw [Nat.cast_sum]
  simp only [Nat.cast_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun c hc => ?_
  have h := Pqr.Bridge.sum_char_multiples c (hS c hc) ξ
  simp only [Pqr.Bridge.mul_natCast_eq_zero_iff] at h
  have h2 : ((if Pqr.ord ξ ∣ c then M / c else 0 : ℕ) : ℂ)
      = if Pqr.ord ξ ∣ c then ((M / c : ℕ) : ℂ) else 0 := by
    split_ifs <;> simp
  rw [h2, ← h]
  refine Finset.sum_congr rfl fun a _ => ?_
  split_ifs <;> simp

end Aux

end Upset

end Pnq
