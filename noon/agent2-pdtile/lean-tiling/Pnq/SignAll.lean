/-
The statement on signs for every odd `n`: A1, the theorem in elements.  For an odd `n` and a nonempty finite family of
exponents there is a signing that is bad at no `d ∣ n`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignSlice
import Pnq.SignCount
import Pnq.SignPivot
import Pnq.SignThree
import Pnq.SignSum

open Finset

namespace Pnq

namespace AllAux

/-! ### Ranks on live levels -/

section

variable {ι : Type*} [Fintype ι]

/-- a live level `i ≥ 1` has rank at least `1` -/
theorem rank_pos (e : ι → ℕ) (p : ℕ) {i : ℕ} (hi : 1 ≤ i) (hlive : live e p i = true) :
    1 ≤ rank e p i := by
  unfold rank
  rw [Nat.succ_le_iff, Finset.card_pos]
  exact ⟨i, Finset.mem_filter.mpr ⟨Finset.mem_Icc.mpr ⟨hi, le_rfl⟩, hlive⟩⟩

/-- the rank goes up strictly at a live level -/
theorem rank_lt_rank (e : ι → ℕ) (p : ℕ) {i i' : ℕ} (h : i < i') (hlive : live e p i' = true) :
    rank e p i < rank e p i' := by
  unfold rank
  apply Finset.card_lt_card
  rw [Finset.ssubset_iff_of_subset]
  · refine ⟨i', Finset.mem_filter.mpr ⟨Finset.mem_Icc.mpr ⟨by omega, le_rfl⟩, hlive⟩, ?_⟩
    intro hmem
    have := (Finset.mem_Icc.mp (Finset.mem_filter.mp hmem).1).2
    omega
  · intro j hj
    rw [Finset.mem_filter, Finset.mem_Icc] at hj ⊢
    exact ⟨⟨hj.1.1, by omega⟩, hj.2⟩

/-- two live levels of the same rank are equal -/
theorem level_eq_of_rank_eq (e : ι → ℕ) (p : ℕ) {i i' : ℕ} (hl : live e p i = true)
    (hl' : live e p i' = true) (h : rank e p i = rank e p i') : i = i' := by
  rcases lt_trichotomy i i' with h1 | h1 | h1
  · exact absurd h (rank_lt_rank e p h1 hl').ne
  · exact h1
  · exact absurd h (rank_lt_rank e p h1 hl).ne'

end

/-! ### The factorization of a product of prime powers; `μ 3` -/

/-- the exponents of a product of powers of different primes -/
theorem factorization_prod_pow (S : Finset ℕ) (hS : ∀ p ∈ S, p.Prime) (r : ℕ → ℕ) (q : ℕ) :
    (∏ p ∈ S, p ^ r p).factorization q = if q ∈ S then r q else 0 := by
  rw [Nat.factorization_prod (fun p hp => pow_ne_zero _ (hS p hp).ne_zero),
    Finsupp.finsetSum_apply]
  rw [Finset.sum_congr rfl (fun p hp => by
    rw [(hS p hp).factorization_pow, Finsupp.single_apply])]
  exact Finset.sum_ite_eq' S q r

theorem mu_three : μ 3 = 2 := by
  simp [μ, Nat.Prime.primeFactors Nat.prime_three, Nat.Prime.factorization_self Nat.prime_three]

/-! ### The set `D*` and the map `d ↦ d♭` -/

section

variable {ι : Type*} [Fintype ι]

/-- `D*`: the divisors `d > 1` of `n` such that for every prime `p` of `d` the level `v_p(d)` of `p`
is live -/
def Dstar (e : ι → ℕ) (n : ℕ) : Finset ℕ :=
  n.divisors.filter fun d => 1 < d ∧ ∀ p ∈ d.primeFactors, live e p (d.factorization p) = true

theorem mem_Dstar {e : ι → ℕ} {n d : ℕ} :
    d ∈ Dstar e n ↔
      (d ∣ n ∧ n ≠ 0) ∧ 1 < d ∧ ∀ p ∈ d.primeFactors, live e p (d.factorization p) = true := by
  rw [Dstar, Finset.mem_filter, Nat.mem_divisors]

/-- `d♭`: the product of `p ^ rank e p (v_p d)` over the primes `p` of `d` -/
def flat (e : ι → ℕ) (d : ℕ) : ℕ :=
  ∏ p ∈ d.primeFactors, p ^ rank e p (d.factorization p)

theorem flat_ne_zero (e : ι → ℕ) (d : ℕ) : flat e d ≠ 0 :=
  Finset.prod_ne_zero_iff.mpr fun _ hp => pow_ne_zero _ (Nat.prime_of_mem_primeFactors hp).ne_zero

theorem factorization_flat (e : ι → ℕ) (d q : ℕ) :
    (flat e d).factorization q = if q ∈ d.primeFactors then rank e q (d.factorization q) else 0 :=
  factorization_prod_pow d.primeFactors (fun _ hp => Nat.prime_of_mem_primeFactors hp)
    (fun p => rank e p (d.factorization p)) q

/-- **(i)** a signing that is bad at a divisor of `n` is bad at `1` or at some `d ∈ D*` -/
theorem exists_badAt_one_or_Dstar (e : ι → ℕ) (ε : ι → Bool) {n : ℕ} (hn0 : n ≠ 0) :
    ∀ d, d ∣ n → BadAt e ε d → BadAt e ε 1 ∨ ∃ d' ∈ Dstar e n, BadAt e ε d' := by
  intro d
  induction d using Nat.strong_induction_on with
  | _ d ih =>
    intro hdn hbad
    have hd0 : d ≠ 0 := by
      rintro rfl
      exact hn0 (Nat.eq_zero_of_zero_dvd hdn)
    by_cases hd1 : d = 1
    · left
      rw [hd1] at hbad
      exact hbad
    by_cases hmem : d ∈ Dstar e n
    · exact Or.inr ⟨d, hmem, hbad⟩
    have hlt : 1 < d := by omega
    have hex : ∃ p ∈ d.primeFactors, live e p (d.factorization p) = false := by
      by_contra hcon
      apply hmem
      rw [mem_Dstar]
      refine ⟨⟨hdn, hn0⟩, hlt, fun p hp => ?_⟩
      cases hl : live e p (d.factorization p) with
      | true => rfl
      | false => exact absurd ⟨p, hp, hl⟩ hcon
    obtain ⟨p, hp, hlive⟩ := hex
    have hpp : p.Prime := Nat.prime_of_mem_primeFactors hp
    have hpd : p ∣ d := Nat.dvd_of_mem_primeFactors hp
    have hi : 1 ≤ d.factorization p := hpp.factorization_pos_of_dvd hd0 hpd
    have hdec : p ^ d.factorization p * (d / p ^ d.factorization p) = d :=
      Nat.ordProj_mul_ordCompl_eq_self d p
    have hnd : ¬ p ∣ d / p ^ d.factorization p := Nat.not_dvd_ordCompl hpp hd0
    have hbad2 : BadAt e ε (p ^ d.factorization p * (d / p ^ d.factorization p)) := by
      rw [hdec]
      exact hbad
    have hbad' := badAt_of_not_live e ε hpp hi hnd hbad2 hlive
    have hpos : 0 < d / p ^ d.factorization p := by
      rcases Nat.eq_zero_or_pos (d / p ^ d.factorization p) with h | h
      · rw [h, mul_zero] at hdec
        exact absurd hdec.symm hd0
      · exact h
    have hlt' : p ^ (d.factorization p - 1) * (d / p ^ d.factorization p) < d := by
      have h1 : p ^ (d.factorization p - 1) < p ^ d.factorization p :=
        Nat.pow_lt_pow_right hpp.one_lt (by omega)
      have h2 := Nat.mul_lt_mul_of_pos_right h1 hpos
      rwa [hdec] at h2
    have hdvd : p ^ (d.factorization p - 1) * (d / p ^ d.factorization p) ∣ d := by
      have h1 : p ^ (d.factorization p - 1) * (d / p ^ d.factorization p) ∣
          p ^ d.factorization p * (d / p ^ d.factorization p) :=
        Nat.mul_dvd_mul (pow_dvd_pow p (Nat.sub_le _ _)) dvd_rfl
      rwa [hdec] at h1
    exact ih _ hlt' (dvd_trans hdvd hdn) hbad'

/-- for `d ∈ D*`, `d♭` has the primes of `d` -/
theorem primeFactors_flat {e : ι → ℕ} {n d : ℕ} (hd : d ∈ Dstar e n) :
    (flat e d).primeFactors = d.primeFactors := by
  obtain ⟨-, hd1, hl⟩ := mem_Dstar.mp hd
  ext q
  rw [← Nat.support_factorization, Finsupp.mem_support_iff, factorization_flat]
  constructor
  · intro h
    by_contra hq
    exact h (ite_eq_right hq)
  · intro hq
    rw [ite_eq_left hq]
    have hqp := Nat.prime_of_mem_primeFactors hq
    have hi : 1 ≤ d.factorization q :=
      hqp.factorization_pos_of_dvd (by omega) (Nat.dvd_of_mem_primeFactors hq)
    have := rank_pos e q hi (hl q hq)
    omega

/-- for `d ∈ D*`, `μ (d♭)` is the largest `(p - 1) * rank e p (v_p d)` over the primes `p` of `d` -/
theorem mu_flat {e : ι → ℕ} {n d : ℕ} (hd : d ∈ Dstar e n) :
    μ (flat e d) = d.primeFactors.sup fun p => (p - 1) * rank e p (d.factorization p) := by
  unfold μ
  rw [primeFactors_flat hd]
  apply Finset.sup_congr rfl
  intro p hp
  rw [factorization_flat, ite_eq_left hp]

/-- for `d ∈ D*` and `n` odd, `d♭` is odd and greater than `1` -/
theorem flat_props {e : ι → ℕ} {n d : ℕ} (hn : ¬ 2 ∣ n) (hd : d ∈ Dstar e n) :
    ¬ 2 ∣ flat e d ∧ 1 < flat e d := by
  obtain ⟨⟨hdn, -⟩, hd1, -⟩ := mem_Dstar.mp hd
  constructor
  · intro h2
    have h : 2 ∈ (flat e d).primeFactors :=
      Nat.mem_primeFactors.mpr ⟨Nat.prime_two, h2, flat_ne_zero e d⟩
    rw [primeFactors_flat hd] at h
    exact hn (dvd_trans (Nat.dvd_of_mem_primeFactors h) hdn)
  · have h0 := flat_ne_zero e d
    have h1 : flat e d ≠ 1 := by
      intro h
      have h' : (flat e d).primeFactors = ∅ := by
        rw [h]
        exact Nat.primeFactors_one
      rw [primeFactors_flat hd, Nat.primeFactors_eq_empty] at h'
      omega
    omega

/-- `d ↦ d♭` is injective on `D*` -/
theorem flat_injOn (e : ι → ℕ) (n : ℕ) :
    ∀ d ∈ Dstar e n, ∀ d' ∈ Dstar e n, flat e d = flat e d' → d = d' := by
  intro d hd d' hd' h
  obtain ⟨-, hd1, hl⟩ := mem_Dstar.mp hd
  obtain ⟨-, hd1', hl'⟩ := mem_Dstar.mp hd'
  have hpf : d.primeFactors = d'.primeFactors := by
    rw [← primeFactors_flat hd, ← primeFactors_flat hd', h]
  apply Nat.eq_of_factorization_eq (by omega) (by omega)
  intro p
  by_cases hp : p ∈ d.primeFactors
  · have hp' : p ∈ d'.primeFactors := hpf ▸ hp
    have h1 := factorization_flat e d p
    have h2 := factorization_flat e d' p
    rw [ite_eq_left hp] at h1
    rw [ite_eq_left hp'] at h2
    rw [h] at h1
    exact level_eq_of_rank_eq e p (hl p hp) (hl' p hp') (h1.symm.trans h2)
  · have hp' : p ∉ d'.primeFactors := hpf ▸ hp
    rw [← Nat.support_factorization, Finsupp.notMem_support_iff] at hp hp'
    rw [hp, hp']

/-- **(ii)** for `d ∈ D*`: the signings bad at `d` are at most `2^(m - μ (d♭))`, and
`μ (d♭) ≤ m - 1` -/
theorem card_badSet_le [Nonempty ι] {e : ι → ℕ} {n d : ℕ} (hd : d ∈ Dstar e n) :
    (badSet e d).card * 2 ^ μ (flat e d) ≤ 2 ^ Fintype.card ι ∧
      μ (flat e d) + 1 ≤ Fintype.card ι := by
  obtain ⟨-, hd1, hl⟩ := mem_Dstar.mp hd
  have hne : d.primeFactors.Nonempty := Nat.nonempty_primeFactors.mpr hd1
  obtain ⟨p, hp, hsup⟩ := Finset.exists_mem_eq_sup d.primeFactors hne
    (fun p => (p - 1) * rank e p (d.factorization p))
  rw [mu_flat hd, hsup]
  have hpp := Nat.prime_of_mem_primeFactors hp
  have hd0 : d ≠ 0 := by omega
  have hi : 1 ≤ d.factorization p :=
    hpp.factorization_pos_of_dvd hd0 (Nat.dvd_of_mem_primeFactors hp)
  have hdec : p ^ d.factorization p * (d / p ^ d.factorization p) = d :=
    Nat.ordProj_mul_ordCompl_eq_self d p
  have hnd : ¬ p ∣ d / p ^ d.factorization p := Nat.not_dvd_ordCompl hpp hd0
  have h2 := card_badSet_mul_two_pow_rank_le e hpp hi hnd (hl p hp)
  rw [hdec] at h2
  exact ⟨h2, rank_lt_card e hpp _⟩

/-- **(ii), the prime 3** for `d ∈ D*` with `d♭ = 3` and `m ≥ 7`: the signings bad at `d` are at
most `(3/16) 2^m` -/
theorem card_badSet_three {e : ι → ℕ} {n d : ℕ} (hd : d ∈ Dstar e n) (h3 : flat e d = 3)
    (hm : 7 ≤ Fintype.card ι) : (badSet e d).card * 16 ≤ 3 * 2 ^ Fintype.card ι := by
  obtain ⟨-, hd1, hl⟩ := mem_Dstar.mp hd
  have hpf : d.primeFactors = {3} := by
    rw [← primeFactors_flat hd, h3, Nat.Prime.primeFactors Nat.prime_three]
  have h3mem : 3 ∈ d.primeFactors := by
    rw [hpf]
    exact Finset.mem_singleton_self 3
  have hrank : rank e 3 (d.factorization 3) = 1 := by
    have h := factorization_flat e d 3
    rw [ite_eq_left h3mem, h3, Nat.Prime.factorization_self Nat.prime_three] at h
    exact h.symm
  have hdeq : d.factorization.prod (fun p k => p ^ k) = 3 ^ d.factorization 3 := by
    rw [Finsupp.prod, Nat.support_factorization, hpf, Finset.prod_singleton]
  rw [Nat.prod_factorization_pow_eq_self (show d ≠ 0 by omega)] at hdeq
  have h5 := card_badSet_three_pow_mul_le e hm (hl 3 h3mem) hrank
  rw [← hdeq] at h5
  exact h5

/-- **(iii), in ℕ** if every signing is bad at some divisor of `n`, the sets `badSet e 1` and
`badSet e d`, `d ∈ D*`, cover all `2^m` signings -/
theorem two_pow_le_sum (e : ι → ℕ) {n : ℕ} (hn0 : n ≠ 0)
    (hcon : ∀ ε : ι → Bool, ∃ d, d ∣ n ∧ BadAt e ε d) :
    2 ^ Fintype.card ι ≤ (badSet e 1).card + ∑ d ∈ Dstar e n, (badSet e d).card := by
  classical
  have hsub : (Finset.univ : Finset (ι → Bool)) ⊆
      badSet e 1 ∪ (Dstar e n).biUnion (badSet e) := by
    intro ε _
    obtain ⟨d, hdn, hbad⟩ := hcon ε
    rcases exists_badAt_one_or_Dstar e ε hn0 d hdn hbad with h | ⟨d', hd', h⟩
    · exact Finset.mem_union_left _ ((mem_badSet e 1 ε).mpr h)
    · exact Finset.mem_union_right _
        (Finset.mem_biUnion.mpr ⟨d', hd', (mem_badSet e d' ε).mpr h⟩)
  have hcard : (Finset.univ : Finset (ι → Bool)).card = 2 ^ Fintype.card ι := by
    rw [Finset.card_univ, Fintype.card_fun, Fintype.card_bool]
  calc 2 ^ Fintype.card ι = (Finset.univ : Finset (ι → Bool)).card := hcard.symm
    _ ≤ (badSet e 1 ∪ (Dstar e n).biUnion (badSet e)).card := Finset.card_le_card hsub
    _ ≤ (badSet e 1).card + ((Dstar e n).biUnion (badSet e)).card := Finset.card_union_le _ _
    _ ≤ (badSet e 1).card + ∑ d ∈ Dstar e n, (badSet e d).card :=
        Nat.add_le_add_left Finset.card_biUnion_le _

/-- **(iii), in ℚ** the sizes of `badSet e 1` and of the `badSet e d`, `d ∈ D*`, add up to at most
`2^m * lhsN1 m T`, where `T` is the image of `D*` under `d ↦ d♭` -/
theorem sum_le [Nonempty ι] (e : ι → ℕ) {n : ℕ} :
    ((badSet e 1).card : ℚ) + ∑ d ∈ Dstar e n, ((badSet e d).card : ℚ) ≤
      2 ^ Fintype.card ι * lhsN1 (Fintype.card ι) ((Dstar e n).image (flat e)) := by
  have h1 : ((badSet e 1).card : ℚ) =
      2 ^ Fintype.card ι * (if Even (Fintype.card ι) then
        ((Fintype.card ι).choose (Fintype.card ι / 2) : ℚ) / 2 ^ Fintype.card ι else 0) := by
    rw [card_badSet_one]
    split_ifs with h
    · field_simp
    · simp
  have hsum : ∑ t ∈ (Dstar e n).image (flat e), (1 / 2 : ℚ) ^ μ t =
      ∑ d ∈ Dstar e n, (1 / 2 : ℚ) ^ μ (flat e d) :=
    Finset.sum_image (flat_injOn e n)
  have hterm : ∀ d ∈ Dstar e n,
      ((badSet e d).card : ℚ) ≤ 2 ^ Fintype.card ι * (1 / 2 : ℚ) ^ μ (flat e d) := by
    intro d hd
    have h := (card_badSet_le hd).1
    have hq : ((badSet e d).card : ℚ) * 2 ^ μ (flat e d) ≤ 2 ^ Fintype.card ι := by
      exact_mod_cast h
    have hpos : (0 : ℚ) < 2 ^ μ (flat e d) := by positivity
    rw [one_div, inv_pow, ← div_eq_mul_inv, le_div_iff₀ hpos]
    exact hq
  have key : ∑ d ∈ Dstar e n, ((badSet e d).card : ℚ) ≤
      2 ^ Fintype.card ι * (∑ d ∈ Dstar e n, (1 / 2 : ℚ) ^ μ (flat e d) -
        (if Even (Fintype.card ι) ∧ 3 ∈ (Dstar e n).image (flat e) ∧ 14 ≤ Fintype.card ι
          then 1 / 16 else 0)) := by
    split_ifs with hc
    · obtain ⟨-, h3, h14⟩ := hc
      obtain ⟨d₀, hd₀, hf⟩ := Finset.mem_image.mp h3
      have h5 : ((badSet e d₀).card : ℚ) * 16 ≤ 3 * 2 ^ Fintype.card ι := by
        exact_mod_cast card_badSet_three hd₀ hf (by omega)
      have hrest : ∑ d ∈ (Dstar e n).erase d₀, ((badSet e d).card : ℚ) ≤
          2 ^ Fintype.card ι * ∑ d ∈ (Dstar e n).erase d₀, (1 / 2 : ℚ) ^ μ (flat e d) := by
        rw [Finset.mul_sum]
        exact Finset.sum_le_sum fun d hd => hterm d (Finset.mem_of_mem_erase hd)
      have hmu3 : (1 / 2 : ℚ) ^ μ (flat e d₀) = 1 / 4 := by
        rw [hf, mu_three]
        norm_num
      have e1 := Finset.add_sum_erase (Dstar e n) (fun d => ((badSet e d).card : ℚ)) hd₀
      have e2 := Finset.add_sum_erase (Dstar e n) (fun d => (1 / 2 : ℚ) ^ μ (flat e d)) hd₀
      rw [← e1, ← e2, hmu3]
      generalize ∑ d ∈ (Dstar e n).erase d₀, ((badSet e d).card : ℚ) = R at hrest ⊢
      generalize ∑ d ∈ (Dstar e n).erase d₀, (1 / 2 : ℚ) ^ μ (flat e d) = S at hrest ⊢
      generalize (2 : ℚ) ^ Fintype.card ι = X at h5 hrest ⊢
      linarith
    · rw [sub_zero, Finset.mul_sum]
      exact Finset.sum_le_sum hterm
  unfold lhsN1
  rw [hsum, h1]
  have hring : ∀ X c S δ : ℚ, X * (c + S - δ) = X * c + X * (S - δ) := by
    intro X c S δ
    ring
  rw [hring]
  exact add_le_add le_rfl key

end

end AllAux

/-- **A1 (the theorem, in elements).**  `n` odd, `ι` finite and nonempty, `e : ι → ℕ` any exponents.  There is a
signing `ε` that is bad at no divisor `d` of `n`: no `Φ_d`, `d ∣ n`, divides `∑ k, sg (ε k) X ^ e k`. -/
theorem exists_not_badAt (n : ℕ) (hn : ¬ 2 ∣ n) {ι : Type*} [Fintype ι] [Nonempty ι] (e : ι → ℕ) :
    ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ BadAt e ε d := by
  by_contra hcon
  have hcon' : ∀ ε : ι → Bool, ∃ d, d ∣ n ∧ BadAt e ε d := by
    intro ε
    by_contra h
    exact hcon ⟨ε, fun d hdn hbad => h ⟨d, hdn, hbad⟩⟩
  have hn0 : n ≠ 0 := by
    rintro rfl
    exact hn (dvd_zero 2)
  have h1 := AllAux.two_pow_le_sum e hn0 hcon'
  have h2 := AllAux.sum_le e (n := n)
  have hm : 1 ≤ Fintype.card ι := Fintype.card_pos
  have hT : ∀ t ∈ (AllAux.Dstar e n).image (AllAux.flat e),
      ¬ 2 ∣ t ∧ 1 < t ∧ μ t + 1 ≤ Fintype.card ι := by
    intro t ht
    obtain ⟨d, hd, rfl⟩ := Finset.mem_image.mp ht
    exact ⟨(AllAux.flat_props hn hd).1, (AllAux.flat_props hn hd).2,
      (AllAux.card_badSet_le hd).2⟩
  have h3 := lhsN1_lt_one (Fintype.card ι) hm _ hT
  have h1q : (2 : ℚ) ^ Fintype.card ι ≤
      ((badSet e 1).card : ℚ) + ∑ d ∈ AllAux.Dstar e n, ((badSet e d).card : ℚ) := by
    exact_mod_cast h1
  have hpos : (0 : ℚ) < 2 ^ Fintype.card ι := by positivity
  have h4 := mul_lt_mul_of_pos_left h3 hpos
  linarith

end Pnq
