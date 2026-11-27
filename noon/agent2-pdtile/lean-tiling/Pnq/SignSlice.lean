/-
The statement on signs for every odd `n`: the slices.  S0 (a signing that is bad at `p^i d` has equal sums on the `p`
classes of every group at level `i` of `p`) and S1 (step-down: if moreover the level `i` of `p` is not live, the
signing is bad at `p^(i-1) d`).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignDefs
import Pnq.Lift2

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

namespace SliceAux

open Polynomial

/-- the value of the signed mask at `ω * η`, for `ω` with `ω ^ M = 1`, sorted by the classes
modulo `M` -/
theorem aeval_P_mul (e : ι → ℕ) (ε : ι → Bool) {M : ℕ} (hM : 0 < M) {ω : ℂ} (hω : ω ^ M = 1)
    (η : ℂ) : aeval (ω * η) (P e ε) = ∑ r ∈ range M, classSum e ε η M r * ω ^ r := by
  have h1 : aeval (ω * η) (P e ε) = ∑ k, (sg (ε k) : ℂ) * η ^ e k * ω ^ (e k % M) := by
    unfold P
    rw [map_sum]
    refine Finset.sum_congr rfl fun k _ => ?_
    rw [map_mul, aeval_C, map_pow, aeval_X, eq_intCast, mul_pow, pow_eq_pow_mod (e k) hω]
    ring
  rw [h1]
  unfold classSum
  simp only [Finset.sum_mul]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [Finset.sum_eq_single (e k % M)]
  · rw [ite_eq_left rfl]
  · intro r _ hr
    rw [ite_eq_right (Ne.symm hr), zero_mul]
  · intro h
    exact absurd (Finset.mem_range.2 (Nat.mod_lt _ hM)) h

/-- a signing that is bad at `n` has signed mask `0` at every root of unity of order `n` -/
theorem aeval_eq_zero_of_badAt (e : ι → ℕ) (ε : ι → Bool) {n : ℕ} (hn : 0 < n) (hbad : BadAt e ε n)
    {z : ℂ} (hz : IsPrimitiveRoot z n) : aeval z (P e ε) = 0 := by
  obtain ⟨Q, hQ⟩ := hbad
  have h0 : aeval z (cyclotomic n ℤ) = 0 := by
    have h1 : IsRoot (cyclotomic n ℂ) z := hz.isRoot_cyclotomic hn
    rw [← map_cyclotomic n (algebraMap ℤ ℂ), IsRoot.def, eval_map_algebraMap] at h1
    exact h1
  rw [hQ, map_mul, h0, zero_mul]

/-- the product of two roots of unity of coprime orders `a`, `b` has order `a * b` -/
theorem isPrimitiveRoot_mul {ω η : ℂ} {a b : ℕ} (hω : IsPrimitiveRoot ω a)
    (hη : IsPrimitiveRoot η b) (hco : a.Coprime b) : IsPrimitiveRoot (ω * η) (a * b) := by
  have e1 : orderOf ω = a := hω.eq_orderOf.symm
  have e2 : orderOf η = b := hη.eq_orderOf.symm
  rw [IsPrimitiveRoot.iff_orderOf,
    (Commute.all ω η).orderOf_mul_eq_mul_orderOf_of_coprime (by rw [e1, e2]; exact hco), e1, e2]

/-- the coefficient of `(∑_{t' < p} (X^L)^t') * Q` at `c + t L` is the coefficient of `Q` at `c`,
when `c < L`, `t < p` and `Q` has no coefficient from `L` on -/
theorem coeff_geom_mul {L p : ℕ} (Q : ℂ[X]) (hQ : ∀ n, L ≤ n → Q.coeff n = 0) {c t : ℕ}
    (hc : c < L) (ht : t < p) :
    ((∑ t' ∈ range p, (X ^ L) ^ t') * Q).coeff (c + t * L) = Q.coeff c := by
  rw [Finset.sum_mul, finsetSum_coeff, Finset.sum_eq_single t]
  · rw [← pow_mul, coeff_X_pow_mul', ite_eq_left (by rw [mul_comm]; exact Nat.le_add_left _ _),
      mul_comm, Nat.add_sub_cancel]
  · intro t' _ ht'
    rw [← pow_mul, coeff_X_pow_mul']
    split_ifs with hle
    · apply hQ
      have h1 : t' < t := by
        by_contra hcon
        have h3 : t + 1 ≤ t' := by omega
        have h4 := Nat.mul_le_mul_left L h3
        rw [Nat.mul_succ, mul_comm L t] at h4
        omega
      have h2 := Nat.mul_le_mul_left L (Nat.succ_le_of_lt h1)
      rw [Nat.mul_succ, mul_comm L t] at h2
      omega
    · rfl
  · intro h
    exact absurd (Finset.mem_range.2 ht) h

/-- **Flatness, for a function on the classes.**  If `∑_{r < p^(j+1)} s r ω^r = 0` for every root
of unity `ω` of order `p^(j+1)`, then `s (c + t p^j)`, for `c < p^j` and `t < p`, does not depend
on `t`: it is the coefficient at `c` of the quotient of `∑_r s r X^r` by
`Φ_{p^(j+1)} = ∑_{t < p} X^(t p^j)`. -/
theorem flat_of_sum_eq_zero {p : ℕ} (hp : p.Prime) (j : ℕ) (s : ℕ → ℂ)
    (h : ∀ ω : ℂ, IsPrimitiveRoot ω (p ^ (j + 1)) → ∑ r ∈ range (p ^ (j + 1)), s r * ω ^ r = 0) :
    ∃ Q : ℂ[X], ∀ c t, c < p ^ j → t < p → s (c + t * p ^ j) = Q.coeff c := by
  have hL : 0 < p ^ j := pow_pos hp.pos j
  have hN : 0 < p ^ (j + 1) := pow_pos hp.pos _
  -- the coefficients of `A = ∑_r s r X^r`
  have hcoeff : ∀ r, r < p ^ (j + 1) →
      (∑ r ∈ range (p ^ (j + 1)), C (s r) * X ^ r : ℂ[X]).coeff r = s r := by
    intro r hr
    rw [finsetSum_coeff]
    simp only [coeff_C_mul_X_pow]
    rw [Finset.sum_ite_eq (range (p ^ (j + 1))) r, ite_eq_left (Finset.mem_range.2 hr)]
  -- its degree
  have hdeg : (∑ r ∈ range (p ^ (j + 1)), C (s r) * X ^ r : ℂ[X]).natDegree ≤ p ^ (j + 1) - 1 := by
    refine natDegree_sum_le_of_forall_le _ _ fun r hr => ?_
    refine (natDegree_C_mul_X_pow_le _ _).trans ?_
    have := Finset.mem_range.1 hr
    omega
  -- `Φ_{p^(j+1)}` divides `A`
  obtain ⟨ζ, hζ⟩ : ∃ ζ : ℂ, IsPrimitiveRoot ζ (p ^ (j + 1)) :=
    ⟨_, Complex.isPrimitiveRoot_exp (p ^ (j + 1)) hN.ne'⟩
  have hdvd : cyclotomic (p ^ (j + 1)) ℂ ∣ ∑ r ∈ range (p ^ (j + 1)), C (s r) * X ^ r := by
    rw [cyclotomic_eq_prod_X_sub_primitiveRoots hζ]
    refine Finset.prod_dvd_of_coprime ?_ ?_
    · exact (pairwise_coprime_X_sub_C (K := ℂ) (s := id) Function.injective_id).set_pairwise _
    · intro ω hω
      rw [dvd_iff_isRoot, IsRoot.def, eval_finsetSum, ← h ω ((mem_primitiveRoots hN).1 hω)]
      refine Finset.sum_congr rfl fun r _ => ?_
      rw [eval_mul, eval_C, eval_pow, eval_X]
  obtain ⟨Q, hQ⟩ := hdvd
  -- the quotient has degree below `p^j`
  have hQdeg : ∀ n, p ^ j ≤ n → Q.coeff n = 0 := by
    intro n hn
    by_cases hQ0 : Q = 0
    · rw [hQ0, coeff_zero]
    · apply coeff_eq_zero_of_natDegree_lt
      have h1 := hdeg
      rw [hQ, natDegree_mul (cyclotomic_ne_zero _ _) hQ0, natDegree_cyclotomic,
        Nat.totient_prime_pow_succ hp] at h1
      have h2 : p ^ j * (p - 1) + p ^ j = p ^ (j + 1) := by
        rw [← Nat.mul_succ, Nat.succ_eq_add_one, Nat.sub_add_cancel hp.pos, pow_succ]
      omega
  refine ⟨Q, fun c t hc ht => ?_⟩
  have hlt : c + t * p ^ j < p ^ (j + 1) := by
    have h3 := Nat.mul_le_mul_right (p ^ j) (Nat.succ_le_of_lt ht)
    rw [Nat.succ_mul] at h3
    rw [pow_succ, mul_comm (p ^ j) p]
    omega
  rw [← hcoeff _ hlt, hQ, cyclotomic_prime_pow_eq_geom_sum hp]
  exact coeff_geom_mul Q hQdeg hc ht

end SliceAux

/-- **S0 (flatness).**  `p` prime, `i ≥ 1`, `p ∤ d` (so `d ≥ 1`), `η` a complex root of unity of order `d`.  If the
signing `ε` is bad at `p^i * d`, then in every group at level `i` (the `p` classes `c % p^(i-1) + t p^(i-1)`, `t < p`,
modulo `p^i`) the signed sums `classSum e ε η (p^i) r = ∑_{e k % p^i = r} sg (ε k) η^(e k)` of the `p` classes are
equal. -/
theorem classSum_eq_of_badAt (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i)
    {d : ℕ} (hd : ¬ p ∣ d) {η : ℂ} (hη : IsPrimitiveRoot η d) (hbad : BadAt e ε (p ^ i * d))
    (c t t' : ℕ) (ht : t < p) (ht' : t' < p) :
    classSum e ε η (p ^ i) (c % p ^ (i - 1) + t * p ^ (i - 1)) =
      classSum e ε η (p ^ i) (c % p ^ (i - 1) + t' * p ^ (i - 1)) := by
  obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
  have hN : 0 < p ^ (j + 1) := pow_pos hp.pos _
  have hd0 : 0 < d := Nat.pos_of_ne_zero fun h => hd (h ▸ dvd_zero p)
  have hco : (p ^ (j + 1)).Coprime d :=
    Nat.Coprime.pow_left _ ((Nat.Prime.coprime_iff_not_dvd hp).2 hd)
  obtain ⟨Q, hQ⟩ := SliceAux.flat_of_sum_eq_zero hp j (classSum e ε η (p ^ (j + 1))) (fun ω hω => by
    rw [← SliceAux.aeval_P_mul e ε hN hω.pow_eq_one η]
    exact SliceAux.aeval_eq_zero_of_badAt e ε (Nat.mul_pos hN hd0) hbad
      (SliceAux.isPrimitiveRoot_mul hω hη hco))
  have hc : c % p ^ j < p ^ j := Nat.mod_lt _ (pow_pos hp.pos j)
  rw [Nat.add_sub_cancel, hQ _ t hc ht, hQ _ t' hc ht']

/-- **S1 (step-down).**  `p` prime, `i ≥ 1`, `p ∤ d` (so `d ≥ 1`).  If the signing `ε` is bad at `p^i * d` and the
level `i` of `p` is not live, then `ε` is bad at `p^(i-1) * d`. -/
theorem badAt_of_not_live (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i)
    {d : ℕ} (hd : ¬ p ∣ d) (hbad : BadAt e ε (p ^ i * d)) (hlive : live e p i = false) :
    BadAt e ε (p ^ (i - 1) * d) := by
  obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
  have hL : 0 < p ^ j := pow_pos hp.pos j
  have hN : 0 < p ^ (j + 1) := pow_pos hp.pos _
  have hd0 : 0 < d := Nat.pos_of_ne_zero fun h => hd (h ▸ dvd_zero p)
  have hco : (p ^ j).Coprime d :=
    Nat.Coprime.pow_left _ ((Nat.Prime.coprime_iff_not_dvd hp).2 hd)
  -- a root of unity of order `d` and one of order `p^j`
  obtain ⟨η, hη⟩ : ∃ η : ℂ, IsPrimitiveRoot η d := ⟨_, Complex.isPrimitiveRoot_exp d hd0.ne'⟩
  obtain ⟨ω, hω⟩ : ∃ ω : ℂ, IsPrimitiveRoot ω (p ^ j) :=
    ⟨_, Complex.isPrimitiveRoot_exp (p ^ j) hL.ne'⟩
  have hω1 : ω ^ p ^ (j + 1) = 1 := by rw [pow_succ, pow_mul, hω.pow_eq_one, one_pow]
  -- no group at the level `j + 1` is full
  have hnl : ¬ ∃ c, c < p ^ (j + 1 - 1) ∧
      ∀ t, t < p → ∃ k, e k % p ^ (j + 1) = c + t * p ^ (j + 1 - 1) := by
    intro hex
    rw [← live_iff, hlive] at hex
    exact Bool.false_ne_true hex
  rw [Nat.add_sub_cancel] at hnl
  -- so the sum of every class modulo `p^(j+1)` is `0`
  have hzero : ∀ r, r < p ^ (j + 1) → classSum e ε η (p ^ (j + 1)) r = 0 := by
    intro r hr
    have hex : ∃ t, t < p ∧ ∀ k, e k % p ^ (j + 1) ≠ r % p ^ j + t * p ^ j := by
      by_contra hcon
      apply hnl
      refine ⟨r % p ^ j, Nat.mod_lt _ hL, fun t ht => ?_⟩
      by_contra hk
      exact hcon ⟨t, ht, fun k hk' => hk ⟨k, hk'⟩⟩
    obtain ⟨t₀, ht₀, hk⟩ := hex
    have hdiv : r / p ^ j < p := Nat.div_lt_of_lt_mul (by rw [← pow_succ]; exact hr)
    have hflat := classSum_eq_of_badAt e ε hp hi hd hη hbad r (r / p ^ j) t₀ hdiv ht₀
    rw [Nat.add_sub_cancel, Nat.mod_add_div' r (p ^ j)] at hflat
    rw [hflat]
    unfold classSum
    exact Finset.sum_eq_zero fun k _ => ite_eq_right (hk k)
  -- the signed mask vanishes at `ω * η`, of order `p^j * d`
  rw [Nat.add_sub_cancel]
  refine Lift.TwoAux.cyclotomic_dvd_of_aeval_eq_zero _ (Nat.mul_pos hL hd0)
    (SliceAux.isPrimitiveRoot_mul hω hη hco) ?_
  rw [SliceAux.aeval_P_mul e ε hN hω1 η]
  exact Finset.sum_eq_zero fun r hr => by rw [hzero r (Finset.mem_range.1 hr), zero_mul]

end Pnq
