/-
The statement on signs for every `n`: the slices modulo 3.  M (a signing that is bad at `3^i d`, `3 ∤ d`, is 3-bad at
`d`), S0′ (a signing that is 3-bad at `p^i d`, `p ≠ 3`, has equal sums in `F3` on the `p` classes of every group at
level `i` of `p`) and S1′ (step-down: if moreover the level `i` of `p` is not live, the signing is 3-bad at
`p^(i-1) d`).  S0′ and S1′ are S0 and S1 of `Pnq/SignSlice.lean` with `F3` for `ℂ` and `Bad3` for `BadAt`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenDefs
import Pnq.SignSlice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

namespace Slice3Aux

open Polynomial

/-- a root of unity of order `n` in `F3`, for `3 ∤ n` -/
theorem exists_isPrimitiveRoot {n : ℕ} (h : ¬ 3 ∣ n) : ∃ ζ : F3, IsPrimitiveRoot ζ n := by
  have : NeZero ((n : ℕ) : F3) := NeZero.of_not_dvd F3 h
  exact HasEnoughRootsOfUnity.exists_isPrimitiveRoot F3 n

/-- a power of a prime `p ≠ 3` is not divisible by `3` -/
theorem not_three_dvd_pow {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) (j : ℕ) : ¬ 3 ∣ p ^ j := fun h =>
  hp3 ((Nat.prime_dvd_prime_iff_eq Nat.prime_three hp).1 (Nat.prime_three.dvd_of_dvd_pow h)).symm

/-- the value in `F3` of the signed mask at `ω * η`, for `ω` with `ω ^ M = 1`, sorted by the classes
modulo `M` -/
theorem val3_mul (e : ι → ℕ) (ε : ι → Bool) {M : ℕ} (hM : 0 < M) {ω : F3} (hω : ω ^ M = 1)
    (η : F3) : val3 e ε (ω * η) = ∑ r ∈ range M, classSum3 e ε η M r * ω ^ r := by
  have h1 : val3 e ε (ω * η) = ∑ k, (sg (ε k) : F3) * η ^ e k * ω ^ (e k % M) := by
    unfold val3
    refine Finset.sum_congr rfl fun k _ => ?_
    rw [mul_pow, pow_eq_pow_mod (e k) hω]
    ring
  rw [h1]
  unfold classSum3
  simp only [Finset.sum_mul]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [Finset.sum_eq_single (e k % M)]
  · rw [ite_eq_left rfl]
  · intro r _ hr
    rw [ite_eq_right (Ne.symm hr), zero_mul]
  · intro h
    exact absurd (Finset.mem_range.2 (Nat.mod_lt _ hM)) h

/-- the product of two roots of unity of coprime orders `a`, `b` has order `a * b` -/
theorem isPrimitiveRoot_mul {ω η : F3} {a b : ℕ} (hω : IsPrimitiveRoot ω a)
    (hη : IsPrimitiveRoot η b) (hco : a.Coprime b) : IsPrimitiveRoot (ω * η) (a * b) := by
  have e1 : orderOf ω = a := hω.eq_orderOf.symm
  have e2 : orderOf η = b := hη.eq_orderOf.symm
  rw [IsPrimitiveRoot.iff_orderOf,
    (Commute.all ω η).orderOf_mul_eq_mul_orderOf_of_coprime (by rw [e1, e2]; exact hco), e1, e2]

/-- a root of unity `ζ` of order `L * d`, with `L` and `d` coprime, is `y * η` with `y ^ L = 1` and
`η` of order `d` -/
theorem exists_split {L d : ℕ} (hL : 0 < L) (hd : 0 < d) (hco : L.Coprime d) {ζ : F3}
    (hζ : IsPrimitiveRoot ζ (L * d)) :
    ∃ y η : F3, y ^ L = 1 ∧ IsPrimitiveRoot η d ∧ ζ = y * η := by
  obtain ⟨u, hu0, hu1⟩ := Nat.chineseRemainder hco 0 1
  obtain ⟨a, rfl⟩ : L ∣ u := (Nat.modEq_zero_iff_dvd).1 hu0
  have hca : a.Coprime d := by
    have h1 : Nat.gcd (L * a) d = Nat.gcd 1 d := hu1.gcd_eq
    rw [Nat.gcd_one_left] at h1
    exact Nat.Coprime.coprime_mul_left h1
  have hηL : IsPrimitiveRoot (ζ ^ L) d := hζ.pow (Nat.mul_pos hL hd) rfl
  have hη : IsPrimitiveRoot ((ζ ^ L) ^ a) d := hηL.pow_of_coprime a hca
  have hζ0 : ζ ≠ 0 := hζ.ne_zero (Nat.mul_pos hL hd).ne'
  refine ⟨ζ * ((ζ ^ L) ^ a)⁻¹, (ζ ^ L) ^ a, ?_, hη, ?_⟩
  · have h2 : ((ζ ^ L) ^ a) ^ L = ζ ^ L := by
      have h3 : L * (L * a) % (L * d) = L % (L * d) := by
        have h4 := Nat.ModEq.mul_left' L hu1
        rw [mul_one] at h4
        exact h4
      rw [← pow_mul, ← pow_mul, mul_comm a L, pow_eq_pow_mod (L * (L * a)) hζ.pow_eq_one, h3,
        ← pow_eq_pow_mod L hζ.pow_eq_one]
    rw [mul_pow, inv_pow, h2, mul_inv_cancel₀ (pow_ne_zero _ hζ0)]
  · rw [mul_assoc, inv_mul_cancel₀ (pow_ne_zero _ (pow_ne_zero _ hζ0)), mul_one]

/-- the coefficient of `(∑_{t' < p} (X^L)^t') * Q` at `c + t L` is the coefficient of `Q` at `c`,
when `c < L`, `t < p` and `Q` has no coefficient from `L` on -/
theorem coeff_geom_mul {K : Type*} [Field K] {L p : ℕ} (Q : K[X]) (hQ : ∀ n, L ≤ n → Q.coeff n = 0)
    {c t : ℕ} (hc : c < L) (ht : t < p) :
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

/-- **Flatness, for a function on the classes, over a field with a root of unity of order
`p^(j+1)`.**  If `∑_{r < p^(j+1)} s r ω^r = 0` for every root of unity `ω` of order `p^(j+1)`,
then `s (c + t p^j)`, for `c < p^j` and `t < p`, does not depend on `t`: it is the coefficient at
`c` of the quotient of `∑_r s r X^r` by `Φ_{p^(j+1)} = ∑_{t < p} X^(t p^j)`. -/
theorem flat_of_sum_eq_zero {K : Type*} [Field K] {p : ℕ} (hp : p.Prime) (j : ℕ) (s : ℕ → K)
    (hex : ∃ ζ : K, IsPrimitiveRoot ζ (p ^ (j + 1)))
    (h : ∀ ω : K, IsPrimitiveRoot ω (p ^ (j + 1)) → ∑ r ∈ range (p ^ (j + 1)), s r * ω ^ r = 0) :
    ∃ Q : K[X], ∀ c t, c < p ^ j → t < p → s (c + t * p ^ j) = Q.coeff c := by
  have hL : 0 < p ^ j := pow_pos hp.pos j
  have hN : 0 < p ^ (j + 1) := pow_pos hp.pos _
  -- the coefficients of `A = ∑_r s r X^r`
  have hcoeff : ∀ r, r < p ^ (j + 1) →
      (∑ r ∈ range (p ^ (j + 1)), C (s r) * X ^ r : K[X]).coeff r = s r := by
    intro r hr
    rw [finsetSum_coeff]
    simp only [coeff_C_mul_X_pow]
    rw [Finset.sum_ite_eq (range (p ^ (j + 1))) r, ite_eq_left (Finset.mem_range.2 hr)]
  -- its degree
  have hdeg : (∑ r ∈ range (p ^ (j + 1)), C (s r) * X ^ r : K[X]).natDegree ≤ p ^ (j + 1) - 1 := by
    refine natDegree_sum_le_of_forall_le _ _ fun r hr => ?_
    refine (natDegree_C_mul_X_pow_le _ _).trans ?_
    have := Finset.mem_range.1 hr
    omega
  -- `Φ_{p^(j+1)}` divides `A`
  obtain ⟨ζ, hζ⟩ := hex
  have hdvd : cyclotomic (p ^ (j + 1)) K ∣ ∑ r ∈ range (p ^ (j + 1)), C (s r) * X ^ r := by
    rw [cyclotomic_eq_prod_X_sub_primitiveRoots hζ]
    refine Finset.prod_dvd_of_coprime ?_ ?_
    · exact (pairwise_coprime_X_sub_C (K := K) (s := id) Function.injective_id).set_pairwise _
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

end Slice3Aux

/-- **M (reduce modulo 3).**  `3 ∤ d` (so `d ≥ 1`), `i` any exponent (`i = 0` allowed).  If the signing `ε` is bad at
`3^i * d` (`Φ_(3^i d)` divides the signed mask over `ℤ`), then `ε` is 3-bad at `d`. -/
theorem bad3_of_badAt (e : ι → ℕ) (ε : ι → Bool) (i : ℕ) {d : ℕ} (h3 : ¬ 3 ∣ d)
    (hbad : BadAt e ε (3 ^ i * d)) : Bad3 e ε d := by
  intro ζ hζ
  have hd0 : 0 < d := Nat.pos_of_ne_zero fun h => h3 (h ▸ dvd_zero 3)
  obtain ⟨Q, hQ⟩ := hbad
  have hroot : (Polynomial.cyclotomic d F3).eval ζ = 0 := hζ.isRoot_cyclotomic hd0
  rw [val3_eq_eval_map, hQ, Polynomial.map_mul, Polynomial.map_cyclotomic, Polynomial.eval_mul]
  rcases Nat.eq_zero_or_pos i with rfl | hi
  · rw [pow_zero, one_mul, hroot, zero_mul]
  · have : Fact (Nat.Prime 3) := ⟨Nat.prime_three⟩
    have hne : 3 ^ i - 3 ^ (i - 1) ≠ 0 := by
      have hlt : 3 ^ (i - 1) < 3 ^ i := Nat.pow_lt_pow_right (by norm_num) (by omega)
      omega
    rw [Polynomial.cyclotomic_mul_prime_pow_eq F3 h3 hi, Polynomial.eval_pow, hroot, zero_pow hne,
      zero_mul]

/-- **S0′ (flatness modulo 3).**  `p` prime, `p ≠ 3` (`p = 2` allowed), `i ≥ 1`, `p ∤ d` (so `d ≥ 1`), `3 ∤ d`, `η ∈ F3`
a root of unity of order `d`.  If the signing `ε` is 3-bad at `p^i * d`, then in every group at level `i` (the `p`
classes `c % p^(i-1) + t p^(i-1)`, `t < p`, modulo `p^i`) the signed sums
`classSum3 e ε η (p^i) r = ∑_{e k % p^i = r} sg (ε k) η^(e k)` of the `p` classes are equal. -/
theorem classSum3_eq_of_bad3 (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) {η : F3} (hη : IsPrimitiveRoot η d)
    (hbad : Bad3 e ε (p ^ i * d)) (c t t' : ℕ) (ht : t < p) (ht' : t' < p) :
    classSum3 e ε η (p ^ i) (c % p ^ (i - 1) + t * p ^ (i - 1)) =
      classSum3 e ε η (p ^ i) (c % p ^ (i - 1) + t' * p ^ (i - 1)) := by
  obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
  have hN : 0 < p ^ (j + 1) := pow_pos hp.pos _
  have hco : (p ^ (j + 1)).Coprime d :=
    Nat.Coprime.pow_left _ ((Nat.Prime.coprime_iff_not_dvd hp).2 hd)
  obtain ⟨Q, hQ⟩ := Slice3Aux.flat_of_sum_eq_zero hp j (classSum3 e ε η (p ^ (j + 1)))
    (Slice3Aux.exists_isPrimitiveRoot (Slice3Aux.not_three_dvd_pow hp hp3 (j + 1))) (fun ω hω => by
      rw [← Slice3Aux.val3_mul e ε hN hω.pow_eq_one η]
      exact hbad _ (Slice3Aux.isPrimitiveRoot_mul hω hη hco))
  have hc : c % p ^ j < p ^ j := Nat.mod_lt _ (pow_pos hp.pos j)
  rw [Nat.add_sub_cancel, hQ _ t hc ht, hQ _ t' hc ht']

/-- **S1′ (step-down modulo 3).**  `p` prime, `p ≠ 3` (`p = 2` allowed), `i ≥ 1`, `p ∤ d` (so `d ≥ 1`), `3 ∤ d`.  If the
signing `ε` is 3-bad at `p^i * d` and the level `i` of `p` is not live, then `ε` is 3-bad at `p^(i-1) * d`. -/
theorem bad3_of_not_live (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) (hbad : Bad3 e ε (p ^ i * d))
    (hlive : live e p i = false) : Bad3 e ε (p ^ (i - 1) * d) := by
  obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
  have hL : 0 < p ^ j := pow_pos hp.pos j
  have hN : 0 < p ^ (j + 1) := pow_pos hp.pos _
  have hd0 : 0 < d := Nat.pos_of_ne_zero fun h => hd (h ▸ dvd_zero p)
  have hco : (p ^ j).Coprime d :=
    Nat.Coprime.pow_left _ ((Nat.Prime.coprime_iff_not_dvd hp).2 hd)
  -- no group at the level `j + 1` is full
  have hnl : ¬ ∃ c, c < p ^ (j + 1 - 1) ∧
      ∀ t, t < p → ∃ k, e k % p ^ (j + 1) = c + t * p ^ (j + 1 - 1) := by
    intro hex
    rw [← live_iff, hlive] at hex
    exact Bool.false_ne_true hex
  rw [Nat.add_sub_cancel] at hnl
  -- so the sum of every class modulo `p^(j+1)` is `0`, at every root of unity `η` of order `d`
  have hzero : ∀ η : F3, IsPrimitiveRoot η d → ∀ r, r < p ^ (j + 1) →
      classSum3 e ε η (p ^ (j + 1)) r = 0 := by
    intro η hη r hr
    have hex : ∃ t, t < p ∧ ∀ k, e k % p ^ (j + 1) ≠ r % p ^ j + t * p ^ j := by
      by_contra hcon
      apply hnl
      refine ⟨r % p ^ j, Nat.mod_lt _ hL, fun t ht => ?_⟩
      by_contra hk
      exact hcon ⟨t, ht, fun k hk' => hk ⟨k, hk'⟩⟩
    obtain ⟨t₀, ht₀, hk⟩ := hex
    have hdiv : r / p ^ j < p := Nat.div_lt_of_lt_mul (by rw [← pow_succ]; exact hr)
    have hflat := classSum3_eq_of_bad3 e ε hp hp3 hi hd h3 hη hbad r (r / p ^ j) t₀ hdiv ht₀
    rw [Nat.add_sub_cancel, Nat.mod_add_div' r (p ^ j)] at hflat
    rw [hflat]
    unfold classSum3
    exact Finset.sum_eq_zero fun k _ => ite_eq_right (hk k)
  -- every root of unity `ζ` of order `p^j * d` is `y * η` with `y ^ p^j = 1` and `η` of order `d`
  rw [Nat.add_sub_cancel]
  intro ζ hζ
  obtain ⟨y, η, hy, hη, rfl⟩ := Slice3Aux.exists_split hL hd0 hco hζ
  have hy1 : y ^ p ^ (j + 1) = 1 := by rw [pow_succ, pow_mul, hy, one_pow]
  rw [Slice3Aux.val3_mul e ε hN hy1 η]
  exact Finset.sum_eq_zero fun r hr => by rw [hzero η hη r (Finset.mem_range.1 hr), zero_mul]

end Pnq
