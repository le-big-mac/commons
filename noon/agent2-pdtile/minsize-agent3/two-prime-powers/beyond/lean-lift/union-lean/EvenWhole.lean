/-
"Twice" for the whole of `Z_n` (Corollary U of the note of the evening of 27 November 2026).
`n'` odd, `k` any natural number, `n = 2^k * n'`.  For elements with exponents `e : ι → ℕ`, the signings whose signed
mask `P e ε = ∑ ± X^(e i)` is divisible by the cyclotomic polynomial `Φ_d` for SOME divisor `d` of `2^k * n'` number
at most twice those whose signed mask is divisible by `Φ_d` for some divisor `d` of `n'`.
(Statement fixed before any Lean proof of it.)
-/
import Pnq.EvenUnion
import Pnq.SignSlice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-! Lemmas for the proof of Corollary U (`card_exists_badAt_le`), in the namespace `Pnq.WholeAux`. -/

namespace WholeAux

/-- a complex root of unity of order `c` (for `c ≠ 0`), chosen once for each `c` -/
noncomputable def eta (c : ℕ) : ℂ := Complex.exp (2 * Real.pi * Complex.I / c)

/-- `eta c` has order `c` -/
theorem eta_isPrimitiveRoot {c : ℕ} (hc : c ≠ 0) : IsPrimitiveRoot (eta c) c :=
  Complex.isPrimitiveRoot_exp c hc

/-- the values of U for the divisor `c`: the element `k` has the value `(eta c) ^ e k` -/
noncomputable def val (e : ι → ℕ) (c : ℕ) (k : ι) : ℂ := eta c ^ e k

/-- the signed sum of all the values is the value of the signed mask at `eta c` -/
theorem sum_eq_aeval (e : ι → ℕ) (ε : ι → Bool) (c : ℕ) :
    ∑ k, sg (ε k) • val e c k = Polynomial.aeval (eta c) (P e ε) := by
  unfold P val
  rw [map_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [map_mul, Polynomial.aeval_C, map_pow, Polynomial.aeval_X, eq_intCast, zsmul_eq_mul]

/-- the class sum `csum` of U, for the values of `c`, is `classSum e ε (eta c)` -/
theorem csum_eq (e : ι → ℕ) (ε : ι → Bool) (c M r : ℕ) :
    csum e (val e c) ε M r = classSum e ε (eta c) M r := by
  unfold csum classSum
  refine Finset.sum_congr rfl fun k _ => ?_
  split_ifs
  · rw [zsmul_eq_mul, val]
  · rfl

/-- level `0` of U, for the values of `c ≥ 1`, is bad exactly when the signing is bad at `c` -/
theorem levelBad_zero_iff (e : ι → ℕ) (ε : ι → Bool) {c : ℕ} (hc : 0 < c) :
    levelBad e (val e c) ε 0 ↔ BadAt e ε c := by
  rw [levelBad_zero, sum_eq_aeval]
  constructor
  · intro h
    exact Lift.TwoAux.cyclotomic_dvd_of_aeval_eq_zero _ hc (eta_isPrimitiveRoot hc.ne') h
  · intro h
    exact SliceAux.aeval_eq_zero_of_badAt e ε hc h (eta_isPrimitiveRoot hc.ne')

/-- a signing that is bad at `2 ^ (j + 1) * c`, `c` odd, has level `j + 1` of U bad for the values of `c`:
S0 with `p = 2`, `i = j + 1`, `t = 0`, `t' = 1`, at `eta c` -/
theorem levelBad_succ_of_badAt (e : ι → ℕ) (ε : ι → Bool) {c : ℕ} (hc : ¬ 2 ∣ c) (j : ℕ)
    (hbad : BadAt e ε (2 ^ (j + 1) * c)) : levelBad e (val e c) ε (j + 1) := by
  rw [levelBad_succ]
  intro r hr
  have hc0 : c ≠ 0 := fun h => hc (h ▸ dvd_zero 2)
  have h := classSum_eq_of_badAt e ε Nat.prime_two (i := j + 1) (by omega) hc
    (eta_isPrimitiveRoot hc0) hbad r 0 1 (by norm_num) (by norm_num)
  rw [Nat.add_sub_cancel, Nat.mod_eq_of_lt hr, zero_mul, add_zero, one_mul] at h
  rw [csum_eq, csum_eq]
  exact h

/-- a divisor of `2 ^ k * n'` is `2 ^ j * c` with `j ≤ k` and `c ∣ n'` -/
theorem exists_of_dvd {k n' d : ℕ} (hd : d ∣ 2 ^ k * n') :
    ∃ j c, j ≤ k ∧ c ∣ n' ∧ d = 2 ^ j * c := by
  obtain ⟨a, c, ha, hc, rfl⟩ := Nat.dvd_mul.mp hd
  obtain ⟨j, hj, rfl⟩ := (Nat.dvd_prime_pow Nat.prime_two).mp ha
  exact ⟨j, c, hj, hc, rfl⟩

end WholeAux

open Classical in
/-- **Corollary U (the whole of `Z_n`).**  `n'` odd (so `n' ≥ 1`).  The number of signings that are bad at some
divisor of `2^k * n'` is at most twice the number of signings that are bad at some divisor of `n'`. -/
theorem card_exists_badAt_le (e : ι → ℕ) (k : ℕ) {n' : ℕ} (hn' : ¬ 2 ∣ n') :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k * n' ∧ BadAt e ε d).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ n' ∧ BadAt e ε d).card := by
  have hn0 : 0 < n' := Nat.pos_of_ne_zero fun h => hn' (h ▸ dvd_zero 2)
  have hU := card_exists_exists_levelBad_le (κ := {c : ℕ // c ∣ n'}) e
    (fun c => WholeAux.val e c.val) k
  refine le_trans (Finset.card_le_card ?_) (le_trans hU ?_)
  · intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε ⊢
    obtain ⟨d, hd, hb⟩ := hε
    obtain ⟨j, c, hj, hc, rfl⟩ := WholeAux.exists_of_dvd hd
    refine ⟨⟨c, hc⟩, j, hj, ?_⟩
    cases j with
    | zero =>
      rw [pow_zero, one_mul] at hb
      exact (WholeAux.levelBad_zero_iff e ε (Nat.pos_of_dvd_of_pos hc hn0)).mpr hb
    | succ j => exact WholeAux.levelBad_succ_of_badAt e ε (fun h => hn' (h.trans hc)) j hb
  · refine Nat.mul_le_mul_left 2 (Finset.card_le_card ?_)
    intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε ⊢
    obtain ⟨c, hc⟩ := hε
    exact ⟨c.val, c.property,
      (WholeAux.levelBad_zero_iff e ε (Nat.pos_of_dvd_of_pos c.property hn0)).mp hc⟩

end Pnq
