/-
The statement on signs for every `n`: the assembly.  A′ (for `n` prime to 3 and a family of at least three exponents
there is a signing that is 3-bad at no `d ∣ n`) and B (for every `n ≠ 0` and a family of at least three exponents
there is a signing that is bad at no `d ∣ n`).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenCount
import Pnq.EvenLadder
import Pnq.EvenSum
import Pnq.SignAll

open Finset

namespace Pnq

namespace All3Aux

open AllAux

/-! ### Two facts on primes -/

/-- a prime other than `2` and `3` is at least `5` -/
theorem five_le_of_prime {p : ℕ} (hp : p.Prime) (h2 : p ≠ 2) (h3 : p ≠ 3) : 5 ≤ p := by
  have h4 : p ≠ 4 := by
    rintro rfl
    exact absurd hp (by norm_num)
  have := hp.two_le
  omega

/-- a prime other than `2` that does not divide `c` does not divide `2^j * c` -/
theorem not_dvd_two_pow_mul {p : ℕ} (hp : p.Prime) (h2 : p ≠ 2) (j : ℕ) {c : ℕ} (hc : ¬ p ∣ c) :
    ¬ p ∣ 2 ^ j * c := by
  intro h
  rcases hp.dvd_mul.mp h with h | h
  · exact h2 ((Nat.prime_dvd_prime_iff_eq hp Nat.prime_two).mp (hp.dvd_of_dvd_pow h))
  · exact hc h

section

variable {ι : Type*} [Fintype ι]

/-! ### (i) The reduction to the ladders over `1` and over `D*` -/

/-- **(i)** at a fixed power `2^j` of 2: for `t` odd and prime to 3 dividing `N`, a signing that is
3-bad at `2^j * t` is 3-bad at `2^j * 1` or at `2^j * t'` for some `t' ∈ D*` (of `N`) -/
theorem exists_bad3_one_or_Dstar (e : ι → ℕ) (ε : ι → Bool) {N : ℕ} (hN0 : N ≠ 0) (j : ℕ) :
    ∀ t, t ∣ N → ¬ 2 ∣ t → ¬ 3 ∣ t → Bad3 e ε (2 ^ j * t) →
      Bad3 e ε (2 ^ j * 1) ∨ ∃ t' ∈ Dstar e N, Bad3 e ε (2 ^ j * t') := by
  intro t
  induction t using Nat.strong_induction_on with
  | _ t ih =>
    intro htN h2 h3 hbad
    have ht0 : t ≠ 0 := by
      rintro rfl
      exact hN0 (Nat.eq_zero_of_zero_dvd htN)
    by_cases ht1 : t = 1
    · left
      rw [ht1] at hbad
      exact hbad
    by_cases hmem : t ∈ Dstar e N
    · exact Or.inr ⟨t, hmem, hbad⟩
    have hlt : 1 < t := by omega
    have hex : ∃ p ∈ t.primeFactors, live e p (t.factorization p) = false := by
      by_contra hcon
      apply hmem
      rw [mem_Dstar]
      refine ⟨⟨htN, hN0⟩, hlt, fun p hp => ?_⟩
      cases hl : live e p (t.factorization p) with
      | true => rfl
      | false => exact absurd ⟨p, hp, hl⟩ hcon
    obtain ⟨p, hp, hlive⟩ := hex
    have hpp : p.Prime := Nat.prime_of_mem_primeFactors hp
    have hpd : p ∣ t := Nat.dvd_of_mem_primeFactors hp
    have hp2 : p ≠ 2 := by
      rintro rfl
      exact h2 hpd
    have hp3 : p ≠ 3 := by
      rintro rfl
      exact h3 hpd
    -- `t = p^i * c` with `i ≥ 1`, `p ∤ c`, the level `i` of `p` not live
    obtain ⟨i, c, hi, hnd, hdec, hlive⟩ :
        ∃ i c, 1 ≤ i ∧ ¬ p ∣ c ∧ p ^ i * c = t ∧ live e p i = false :=
      ⟨t.factorization p, t / p ^ t.factorization p, hpp.factorization_pos_of_dvd ht0 hpd,
        Nat.not_dvd_ordCompl hpp ht0, Nat.ordProj_mul_ordCompl_eq_self t p, hlive⟩
    have hct : c ∣ t := Dvd.intro_left _ hdec
    have hc3 : ¬ 3 ∣ c := fun h => h3 (dvd_trans h hct)
    have hbad2 : Bad3 e ε (p ^ i * (2 ^ j * c)) := by
      have h : p ^ i * (2 ^ j * c) = 2 ^ j * t := by
        rw [← hdec]
        ring
      rw [h]
      exact hbad
    have hbad' := bad3_of_not_live e ε hpp hp3 hi (not_dvd_two_pow_mul hpp hp2 j hnd)
      (not_dvd_two_pow_mul Nat.prime_three (by norm_num) j hc3) hbad2 hlive
    have hbad'' : Bad3 e ε (2 ^ j * (p ^ (i - 1) * c)) := by
      have h : 2 ^ j * (p ^ (i - 1) * c) = p ^ (i - 1) * (2 ^ j * c) := by
        ring
      rw [h]
      exact hbad'
    have hpos : 0 < c := by
      rcases Nat.eq_zero_or_pos c with h | h
      · rw [h, mul_zero] at hdec
        exact absurd hdec.symm ht0
      · exact h
    have hlt' : p ^ (i - 1) * c < t := by
      have h1 : p ^ (i - 1) < p ^ i := Nat.pow_lt_pow_right hpp.one_lt (by omega)
      have h2 := Nat.mul_lt_mul_of_pos_right h1 hpos
      rwa [hdec] at h2
    have hdvd : p ^ (i - 1) * c ∣ t := by
      have h1 : p ^ (i - 1) * c ∣ p ^ i * c :=
        Nat.mul_dvd_mul (pow_dvd_pow p (Nat.sub_le _ _)) dvd_rfl
      rwa [hdec] at h1
    exact ih _ hlt' (dvd_trans hdvd htN) (fun h => h2 (dvd_trans h hdvd))
      (fun h => h3 (dvd_trans h hdvd)) hbad''

/-! ### (ii) The rungs `t ∈ D*` -/

/-- **(ii)** for `N` prime to 6 and `t ∈ D*`: the signings 3-bad at `t` are at most
`2^(m - μ (t♭))`; and there are at least five elements -/
theorem card_bad3Set_le [Nonempty ι] {e : ι → ℕ} {N t : ℕ} (hN2 : ¬ 2 ∣ N) (hN3 : ¬ 3 ∣ N)
    (ht : t ∈ Dstar e N) :
    (bad3Set e t).card * 2 ^ μ (flat e t) ≤ 2 ^ Fintype.card ι ∧ 5 ≤ Fintype.card ι := by
  obtain ⟨⟨htN, -⟩, ht1, hl⟩ := mem_Dstar.mp ht
  have hne : t.primeFactors.Nonempty := Nat.nonempty_primeFactors.mpr ht1
  obtain ⟨p, hp, hsup⟩ := Finset.exists_mem_eq_sup t.primeFactors hne
    (fun p => (p - 1) * rank e p (t.factorization p))
  rw [mu_flat ht, hsup]
  have hpp := Nat.prime_of_mem_primeFactors hp
  have hpt : p ∣ t := Nat.dvd_of_mem_primeFactors hp
  have hp2 : p ≠ 2 := by
    rintro rfl
    exact hN2 (dvd_trans hpt htN)
  have hp3 : p ≠ 3 := by
    rintro rfl
    exact hN3 (dvd_trans hpt htN)
  have hp5 : 5 ≤ p := five_le_of_prime hpp hp2 hp3
  have ht0 : t ≠ 0 := by omega
  have hi : 1 ≤ t.factorization p := hpp.factorization_pos_of_dvd ht0 hpt
  have hdec : p ^ t.factorization p * (t / p ^ t.factorization p) = t :=
    Nat.ordProj_mul_ordCompl_eq_self t p
  have hnd : ¬ p ∣ t / p ^ t.factorization p := Nat.not_dvd_ordCompl hpp ht0
  have hc3 : ¬ 3 ∣ t / p ^ t.factorization p :=
    fun h => hN3 (dvd_trans (dvd_trans h (Dvd.intro_left _ hdec)) htN)
  have h2 := card_bad3Set_mul_two_pow_rank_le e hpp hp3 hi hnd hc3 (hl p hp)
  rw [hdec] at h2
  have hr : 1 ≤ rank e p (t.factorization p) := rank_pos e p hi (hl p hp)
  have hc : (p - 1) * rank e p (t.factorization p) + 1 ≤ Fintype.card ι :=
    rank_lt_card e hpp (t.factorization p)
  have h4 : 4 * 1 ≤ (p - 1) * rank e p (t.factorization p) := Nat.mul_le_mul (by omega) hr
  exact ⟨h2, by omega⟩

/-- for `N` prime to 6 and `t ∈ D*`, `t♭` is prime to 6 and greater than `1` -/
theorem flat_props3 {e : ι → ℕ} {N t : ℕ} (hN2 : ¬ 2 ∣ N) (hN3 : ¬ 3 ∣ N) (ht : t ∈ Dstar e N) :
    ¬ 2 ∣ flat e t ∧ ¬ 3 ∣ flat e t ∧ 1 < flat e t := by
  obtain ⟨⟨htN, -⟩, -, -⟩ := mem_Dstar.mp ht
  refine ⟨(flat_props hN2 ht).1, ?_, (flat_props hN2 ht).2⟩
  intro h3
  have h : 3 ∈ (flat e t).primeFactors :=
    Nat.mem_primeFactors.mpr ⟨Nat.prime_three, h3, flat_ne_zero e t⟩
  rw [primeFactors_flat ht] at h
  exact hN3 (dvd_trans (Nat.dvd_of_mem_primeFactors h) htN)

/-! ### (iii) The count -/

/-- **(iii), in ℕ** if every signing is 3-bad at some divisor of `n` (`n ≠ 0`, `3 ∤ n`), then `2^m`
is at most twice the size of `bad3Set e 1` plus twice the sizes of the `bad3Set e t`, `t ∈ D*` of
the odd part of `n`: each divisor of `n` is `2^j * t` with `j ≤ v_2(n)` and `t` an odd divisor,
(i) brings `t` to `1` or into `D*`, and the ladder L over each such `t` holds at most
`2 * (bad3Set e t).card` signings -/
theorem two_pow_le_sum (e : ι → ℕ) {n : ℕ} (hn0 : n ≠ 0) (hn3 : ¬ 3 ∣ n)
    (hcon : ∀ ε : ι → Bool, ∃ d, d ∣ n ∧ Bad3 e ε d) :
    2 ^ Fintype.card ι ≤ 2 * (bad3Set e 1).card +
      2 * ∑ t ∈ Dstar e (n / 2 ^ n.factorization 2), (bad3Set e t).card := by
  classical
  have hdecn : 2 ^ n.factorization 2 * (n / 2 ^ n.factorization 2) = n :=
    Nat.ordProj_mul_ordCompl_eq_self n 2
  have hN2 : ¬ 2 ∣ n / 2 ^ n.factorization 2 := Nat.not_dvd_ordCompl Nat.prime_two hn0
  generalize n / 2 ^ n.factorization 2 = N at hdecn hN2 ⊢
  have hN0 : N ≠ 0 := by
    intro h
    rw [h, mul_zero] at hdecn
    exact hn0 hdecn.symm
  have hNn : N ∣ n := Dvd.intro_left _ hdecn
  have hN3 : ¬ 3 ∣ N := fun h => hn3 (dvd_trans h hNn)
  -- the ladder over `t`
  let lad : ℕ → Finset (ι → Bool) := fun t =>
    Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ n.factorization 2 ∧ Bad3 e ε (2 ^ j * t)
  have hlad : ∀ t, ¬ 2 ∣ t → ¬ 3 ∣ t → (lad t).card ≤ 2 * (bad3Set e t).card :=
    fun t h2 h3 => card_exists_bad3_le e h2 h3 (n.factorization 2)
  have hmemlad : ∀ (ε : ι → Bool) (j t : ℕ), j ≤ n.factorization 2 → Bad3 e ε (2 ^ j * t) →
      ε ∈ lad t :=
    fun ε j t hj h => Finset.mem_filter.mpr ⟨Finset.mem_univ _, j, hj, h⟩
  have hsub : (Finset.univ : Finset (ι → Bool)) ⊆ lad 1 ∪ (Dstar e N).biUnion lad := by
    intro ε _
    obtain ⟨d, hdn, hbad⟩ := hcon ε
    have hd0 : d ≠ 0 := by
      rintro rfl
      exact hn0 (Nat.eq_zero_of_zero_dvd hdn)
    obtain ⟨j, t, htodd, rfl⟩ := Nat.exists_eq_two_pow_mul_odd hd0
    have ht2 : ¬ 2 ∣ t := htodd.not_two_dvd_nat
    have hjn : 2 ^ j ∣ n := dvd_trans (Dvd.intro _ rfl) hdn
    have hjK : j ≤ n.factorization 2 :=
      (Nat.prime_two.pow_dvd_iff_le_factorization hn0).mp hjn
    have htn : t ∣ 2 ^ n.factorization 2 * N := by
      rw [hdecn]
      exact dvd_trans (Dvd.intro_left _ rfl) hdn
    have hco : Nat.Coprime t (2 ^ n.factorization 2) :=
      Nat.Coprime.pow_right _ ((Nat.Prime.coprime_iff_not_dvd Nat.prime_two).2 ht2).symm
    have htN : t ∣ N := hco.dvd_of_dvd_mul_left htn
    have ht3 : ¬ 3 ∣ t := fun h => hN3 (dvd_trans h htN)
    rcases exists_bad3_one_or_Dstar e ε hN0 j t htN ht2 ht3 hbad with h | ⟨t', ht', h⟩
    · exact Finset.mem_union_left _ (hmemlad ε j 1 hjK h)
    · exact Finset.mem_union_right _ (Finset.mem_biUnion.mpr ⟨t', ht', hmemlad ε j t' hjK h⟩)
  have hcard : (Finset.univ : Finset (ι → Bool)).card = 2 ^ Fintype.card ι := by
    rw [Finset.card_univ, Fintype.card_fun, Fintype.card_bool]
  have hD : ∀ t ∈ Dstar e N, (lad t).card ≤ 2 * (bad3Set e t).card := by
    intro t ht
    obtain ⟨⟨htN, -⟩, -, -⟩ := mem_Dstar.mp ht
    exact hlad t (fun h => hN2 (dvd_trans h htN)) (fun h => hN3 (dvd_trans h htN))
  calc 2 ^ Fintype.card ι = (Finset.univ : Finset (ι → Bool)).card := hcard.symm
    _ ≤ (lad 1 ∪ (Dstar e N).biUnion lad).card := Finset.card_le_card hsub
    _ ≤ (lad 1).card + ((Dstar e N).biUnion lad).card := Finset.card_union_le _ _
    _ ≤ (lad 1).card + ∑ t ∈ Dstar e N, (lad t).card :=
        Nat.add_le_add_left Finset.card_biUnion_le _
    _ ≤ 2 * (bad3Set e 1).card + ∑ t ∈ Dstar e N, 2 * (bad3Set e t).card :=
        Nat.add_le_add (hlad 1 (by norm_num) (by norm_num)) (Finset.sum_le_sum hD)
    _ = 2 * (bad3Set e 1).card + 2 * ∑ t ∈ Dstar e N, (bad3Set e t).card := by
        rw [Finset.mul_sum]

/-- **(iii), in ℚ** for `N` prime to 6, the sizes of the `bad3Set e t`, `t ∈ D*`, add up to at most
`2^m` times the sum of `(1/2)^(μ s)` over the image of `D*` under `t ↦ t♭` -/
theorem sum_le [Nonempty ι] (e : ι → ℕ) {N : ℕ} (hN2 : ¬ 2 ∣ N) (hN3 : ¬ 3 ∣ N) :
    ∑ t ∈ Dstar e N, ((bad3Set e t).card : ℚ) ≤
      2 ^ Fintype.card ι * ∑ s ∈ (Dstar e N).image (flat e), (1 / 2 : ℚ) ^ μ s := by
  have hsum : ∑ s ∈ (Dstar e N).image (flat e), (1 / 2 : ℚ) ^ μ s =
      ∑ t ∈ Dstar e N, (1 / 2 : ℚ) ^ μ (flat e t) :=
    Finset.sum_image (flat_injOn e N)
  rw [hsum, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro t ht
  have h := (card_bad3Set_le hN2 hN3 ht).1
  have hq : ((bad3Set e t).card : ℚ) * 2 ^ μ (flat e t) ≤ 2 ^ Fintype.card ι := by
    exact_mod_cast h
  have hpos : (0 : ℚ) < 2 ^ μ (flat e t) := by positivity
  rw [one_div, inv_pow, ← div_eq_mul_inv, le_div_iff₀ hpos]
  exact hq

end

end All3Aux

/-- **A′ (assembly, in elements, modulo 3).**  `3 ∤ n` (so `n ≥ 1`), `ι` finite with at least three points,
`e : ι → ℕ` any exponents.  There is a signing `ε` that is 3-bad at no divisor `d` of `n`. -/
theorem exists_not_bad3 (n : ℕ) (hn : ¬ 3 ∣ n) {ι : Type*} [Fintype ι] (hm : 3 ≤ Fintype.card ι)
    (e : ι → ℕ) : ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ Bad3 e ε d := by
  by_contra hcon
  have hcon' : ∀ ε : ι → Bool, ∃ d, d ∣ n ∧ Bad3 e ε d := by
    intro ε
    by_contra h
    exact hcon ⟨ε, fun d hdn hbad => h ⟨d, hdn, hbad⟩⟩
  have hn0 : n ≠ 0 := by
    rintro rfl
    exact hn (dvd_zero 3)
  have : Nonempty ι := Fintype.card_pos_iff.mp (by omega)
  have hN2 : ¬ 2 ∣ n / 2 ^ n.factorization 2 := Nat.not_dvd_ordCompl Nat.prime_two hn0
  have hN3 : ¬ 3 ∣ n / 2 ^ n.factorization 2 :=
    fun h => hn (dvd_trans h (Nat.ordCompl_dvd n 2))
  -- the count: all `2^m` signings lie on the ladders over `1` and over `D*`
  have h1 := All3Aux.two_pow_le_sum e hn0 hn hcon'
  -- the rung `1`
  have hE := card_bad3Set_one e
  have hE' : 3 * (bad3Set e 1).card ≤ 2 ^ Fintype.card ι + 2 := by
    split_ifs at hE <;> omega
  by_cases hD : AllAux.Dstar e (n / 2 ^ n.factorization 2) = ∅
  · -- no live `t > 1`: `2^m ≤ 2 * (2^m + 2) / 3`, so `2^m ≤ 4`
    rw [hD, Finset.sum_empty] at h1
    have h8 : 8 ≤ 2 ^ Fintype.card ι :=
      le_trans (by norm_num : 8 ≤ 2 ^ 3) (Nat.pow_le_pow_right (by norm_num) hm)
    omega
  · -- some live `t > 1`: then `m ≥ 5`, and `2^m < 2 * (2^m + 2) / 3 + 2^m / 4`, so `2^m < 16`
    obtain ⟨t₀, ht₀⟩ := Finset.ne_empty_iff_nonempty.mp hD
    have hm5 : 5 ≤ Fintype.card ι := (All3Aux.card_bad3Set_le hN2 hN3 ht₀).2
    have h32 : 32 ≤ 2 ^ Fintype.card ι :=
      le_trans (by norm_num : 32 ≤ 2 ^ 5) (Nat.pow_le_pow_right (by norm_num) hm5)
    have h2 := All3Aux.sum_le e hN2 hN3
    have h3 := sum_half_pow_mu_lt
      ((AllAux.Dstar e (n / 2 ^ n.factorization 2)).image (AllAux.flat e))
      (fun s hs => by
        obtain ⟨t, ht, rfl⟩ := Finset.mem_image.mp hs
        exact All3Aux.flat_props3 hN2 hN3 ht)
    have h1q : (2 : ℚ) ^ Fintype.card ι ≤ 2 * ((bad3Set e 1).card : ℚ) +
        2 * ∑ t ∈ AllAux.Dstar e (n / 2 ^ n.factorization 2), ((bad3Set e t).card : ℚ) := by
      exact_mod_cast h1
    have hEq : (3 : ℚ) * ((bad3Set e 1).card : ℚ) ≤ 2 ^ Fintype.card ι + 2 := by
      exact_mod_cast hE'
    have h32q : (32 : ℚ) ≤ 2 ^ Fintype.card ι := by
      exact_mod_cast h32
    have hpos : (0 : ℚ) < 2 ^ Fintype.card ι := by positivity
    have h4 := mul_lt_mul_of_pos_left h3 hpos
    linarith

/-- **B (back to `ℤ`).**  `n ≠ 0`, `ι` finite with at least three points, `e : ι → ℕ` any exponents.  There is a
signing `ε` that is bad at no divisor `d` of `n`: no `Φ_d`, `d ∣ n`, divides `∑ k, sg (ε k) X ^ e k`. -/
theorem exists_not_badAt_of_three_le (n : ℕ) (hn : n ≠ 0) {ι : Type*} [Fintype ι]
    (hm : 3 ≤ Fintype.card ι) (e : ι → ℕ) : ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ BadAt e ε d := by
  -- `n = 3^a * n3` with `3 ∤ n3`; a signing from A′ for `n3`
  obtain ⟨a, n3, hn3, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hn 3 (by norm_num)
  obtain ⟨ε, hε⟩ := exists_not_bad3 n3 hn3 hm e
  refine ⟨ε, fun d hd hbad => ?_⟩
  have hd0 : d ≠ 0 := fun h => hn (zero_dvd_iff.mp (h ▸ hd))
  -- `d = 3^i * d'` with `3 ∤ d'`; then `d' ∣ n3`, and M makes the signing 3-bad at `d'`
  obtain ⟨i, d', hd', rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hd0 3 (by norm_num)
  have h1 : d' ∣ 3 ^ a * n3 := (Dvd.intro_left _ rfl).trans hd
  have hco : Nat.Coprime d' (3 ^ a) :=
    Nat.Coprime.pow_right _ ((Nat.Prime.coprime_iff_not_dvd Nat.prime_three).2 hd').symm
  exact hε d' (hco.dvd_of_dvd_mul_left h1) (bad3_of_badAt e ε i hd' hbad)

end Pnq
