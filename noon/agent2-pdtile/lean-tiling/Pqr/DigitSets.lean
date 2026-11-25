/-
Digit sets in a cyclic group `ZMod M`: for a set `S` of prime powers dividing `M`, the set of all sums
`∑_{s ∈ S} c_s · gen M s` with `0 ≤ c_s < p_s`, where `s = p_s ^ a` and `gen M s = p_s^(a-1) · (M / p_s^{v_p(M)})`.
(These are the sets with mask polynomial `∏_{s ∈ S} Φ_{p_s}(X^{gen M s})` of Coven and Meyerowitz.)
Their cardinality is `∏_{s ∈ S} p_s` and their Fourier zeros are the orders `d` exactly divisible by some `s ∈ S`.
-/
import Pqr.TilingCriterion
import Pqr.Bridge

open Finset

namespace Pqr

/-- the prime powers `p^a`, `a ≥ 1`, dividing `M` -/
def primePowers (M : ℕ) : Finset ℕ := M.divisors.filter IsPrimePow

/-- for a prime power `s = p^a` dividing `M`: `p^(a-1) · (M / p^{v_p(M)})` -/
def gen (M s : ℕ) : ℕ := (s / s.minFac) * (M / s.minFac ^ M.factorization s.minFac)

/-- the digit set attached to a set `S` of prime powers dividing `M` -/
noncomputable def digitSet (M : ℕ) (S : Finset ℕ) : Finset (ZMod M) :=
  (Fintype.piFinset (fun s : S => Finset.range (s : ℕ).minFac)).image
    (fun c => ∑ s : S, ((c s * gen M s : ℕ) : ZMod M))

/-- `s` divides `d` exactly: `s ∣ d` and `s` is coprime to `d / s` -/
def ExactDiv (s d : ℕ) : Prop := s ∣ d ∧ Nat.Coprime s (d / s)

/-! Helper lemmas live in the namespace `Pqr.DigitSets`, so that their names cannot clash with those of the
other files of the project. -/

namespace DigitSets

/-! ### Arithmetic of prime powers dividing `M` -/

/-- For `d ∣ p^n · m` with `p ∤ m`: `d ∣ p^c · m` iff `v_p(d) ≤ c`. -/
theorem dvd_pow_mul_iff {p : ℕ} (hp : p.Prime) {m n c d : ℕ} (hm : ¬ p ∣ m)
    (hd : d ∣ p ^ n * m) : d ∣ p ^ c * m ↔ d.factorization p ≤ c := by
  have hm0 : m ≠ 0 := fun h => hm (h ▸ dvd_zero p)
  have hd0 : d ≠ 0 := by
    rintro rfl
    exact (mul_ne_zero (pow_ne_zero n hp.ne_zero) hm0) (zero_dvd_iff.1 hd)
  have hcop : Nat.Coprime p m := (Nat.Prime.coprime_iff_not_dvd hp).2 hm
  constructor
  · intro h
    have h1 : p ^ d.factorization p ∣ p ^ c * m := (Nat.ordProj_dvd d p).trans h
    have h2 : p ^ d.factorization p ∣ p ^ c :=
      (Nat.Coprime.pow_left _ hcop).dvd_of_dvd_mul_right h1
    exact (Nat.pow_dvd_pow_iff_le_right hp.one_lt).1 h2
  · intro h
    have h1 : Nat.Coprime (p ^ n) (d / p ^ d.factorization p) :=
      (Nat.coprime_ordCompl hp hd0).pow_left n
    have h2 : d / p ^ d.factorization p ∣ m := by
      have h3 : d / p ^ d.factorization p ∣ p ^ n * m :=
        (Nat.div_dvd_of_dvd (Nat.ordProj_dvd d p)).trans hd
      exact (Nat.Coprime.symm h1).dvd_of_dvd_mul_left h3
    have h4 := Nat.mul_dvd_mul (pow_dvd_pow p h) h2
    rwa [Nat.ordProj_mul_ordCompl_eq_self] at h4

/-- `p^a` (with `a ≥ 1`) divides `d` exactly iff `v_p(d) = a`. -/
theorem exactDiv_pow_iff {p : ℕ} (hp : p.Prime) {a d : ℕ} (ha : a ≠ 0) (hd : d ≠ 0) :
    ExactDiv (p ^ a) d ↔ d.factorization p = a := by
  constructor
  · rintro ⟨h1, h2⟩
    have h3 : a ≤ d.factorization p := (hp.pow_dvd_iff_le_factorization hd).1 h1
    have h4 : ¬ p ∣ d / p ^ a := by
      have : Nat.Coprime p (d / p ^ a) := Nat.Coprime.coprime_dvd_left (dvd_pow_self p ha) h2
      exact (Nat.Prime.coprime_iff_not_dvd hp).1 this
    have h5 : ¬ a + 1 ≤ d.factorization p := by
      intro h
      have h6 : p ^ a * p ∣ d := by
        rw [← pow_succ]
        exact (hp.pow_dvd_iff_le_factorization hd).2 h
      exact h4 (Nat.dvd_div_of_mul_dvd h6)
    omega
  · rintro rfl
    exact ⟨Nat.ordProj_dvd d p, (Nat.coprime_ordCompl hp hd).pow_left _⟩

theorem mem_primePowers_iff {M s : ℕ} (hM : M ≠ 0) :
    s ∈ primePowers M ↔ s ∣ M ∧ IsPrimePow s := by
  simp [primePowers, hM]

/-- the shape of an element of `primePowers M` -/
theorem primePowers_spec {M s : ℕ} (hM : M ≠ 0) (hs : s ∈ primePowers M) :
    ∃ p k : ℕ, p.Prime ∧ k + 1 ≤ M.factorization p ∧ s = p ^ (k + 1) ∧ s.minFac = p ∧
      gen M s = p ^ k * (M / p ^ M.factorization p) := by
  obtain ⟨hsM, hpp⟩ := (mem_primePowers_iff hM).1 hs
  obtain ⟨p, k, hp, hk, rfl⟩ := (isPrimePow_nat_iff s).1 hpp
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero hk.ne'
  have hmin : (p ^ (k + 1)).minFac = p := hp.pow_minFac (Nat.succ_ne_zero k)
  refine ⟨p, k, hp, (hp.pow_dvd_iff_le_factorization hM).1 hsM, rfl, hmin, ?_⟩
  rw [gen, hmin, pow_succ, Nat.mul_div_cancel _ hp.pos]

/-- exact divisibility by `s = p^a` in terms of the generator of `s` -/
theorem exactDiv_iff_dvd {M s d : ℕ} (hM : M ≠ 0) (hs : s ∈ primePowers M) (hd : d ∣ M) :
    ExactDiv s d ↔ d ∣ s.minFac * gen M s ∧ ¬ d ∣ gen M s := by
  obtain ⟨p, k, hp, hk, rfl, hmin, hgen⟩ := primePowers_spec hM hs
  have hd0 : d ≠ 0 := fun h => hM (zero_dvd_iff.1 (h ▸ hd))
  have hm : ¬ p ∣ M / p ^ M.factorization p := Nat.not_dvd_ordCompl hp hM
  have hd' : d ∣ p ^ M.factorization p * (M / p ^ M.factorization p) := by
    rwa [Nat.ordProj_mul_ordCompl_eq_self]
  rw [hmin, hgen, exactDiv_pow_iff hp (Nat.succ_ne_zero k) hd0, ← mul_assoc, ← pow_succ',
    dvd_pow_mul_iff hp hm hd', dvd_pow_mul_iff hp hm hd']
  omega

/-- every divisor `d ≠ 1` of `M` is exactly divisible by a prime power -/
theorem exists_exactDiv {M d : ℕ} (hM : M ≠ 0) (hd : d ∣ M) (hd1 : d ≠ 1) :
    ∃ s ∈ primePowers M, ExactDiv s d := by
  have hd0 : d ≠ 0 := fun h => hM (zero_dvd_iff.1 (h ▸ hd))
  have hp : d.minFac.Prime := Nat.minFac_prime hd1
  have ha : 0 < d.factorization d.minFac := hp.factorization_pos_of_dvd hd0 (Nat.minFac_dvd d)
  refine ⟨d.minFac ^ d.factorization d.minFac, ?_, (exactDiv_pow_iff hp ha.ne' hd0).2 rfl⟩
  rw [mem_primePowers_iff hM]
  exact ⟨(Nat.ordProj_dvd d _).trans hd, hp.isPrimePow.pow ha.ne'⟩

/-- `∏_{p^a ∣ M} p = M` -/
theorem prod_minFac_primePowers {M : ℕ} (hM : M ≠ 0) : ∏ s ∈ primePowers M, s.minFac = M := by
  have h := ArithmeticFunction.vonMangoldt_sum (n := M)
  simp only [ArithmeticFunction.vonMangoldt_apply] at h
  rw [← Finset.sum_filter] at h
  have hpos : ∀ s ∈ primePowers M, ((s.minFac : ℕ) : ℝ) ≠ 0 := fun s _ =>
    Nat.cast_ne_zero.2 (Nat.minFac_pos s).ne'
  have h2 : Real.log ((∏ s ∈ primePowers M, s.minFac : ℕ) : ℝ) = Real.log M := by
    rw [Nat.cast_prod, Real.log_prod hpos]
    exact h
  have h3 : ((∏ s ∈ primePowers M, s.minFac : ℕ) : ℝ) = M := by
    refine Real.log_injOn_pos (Set.mem_Ioi.2 ?_) (Set.mem_Ioi.2 ?_) h2
    · exact Nat.cast_pos.2 (Finset.prod_pos fun s _ => Nat.minFac_pos s)
    · exact Nat.cast_pos.2 (Nat.pos_of_ne_zero hM)
  exact_mod_cast h3

/-! ### One factor -/

variable {M : ℕ} [NeZero M]

/-- the factor of the Fourier transform of a digit set attached to the prime power `s` -/
noncomputable def phi (M : ℕ) [NeZero M] (s : ℕ) (ξ : ZMod M) : ℂ :=
  ∑ c ∈ range s.minFac, ZMod.stdAddChar (ξ * ((c * gen M s : ℕ) : ZMod M))

theorem stdAddChar_eq_one_iff (x : ZMod M) : (ZMod.stdAddChar x : ℂ) = 1 ↔ x = 0 := by
  constructor
  · intro h
    rw [← AddChar.map_zero_eq_one (ZMod.stdAddChar (N := M))] at h
    exact ZMod.injective_stdAddChar h
  · rintro rfl
    exact AddChar.map_zero_eq_one _

theorem phi_eq_geom (s : ℕ) (ξ : ZMod M) :
    phi M s ξ = ∑ c ∈ range s.minFac, (ZMod.stdAddChar (ξ * (gen M s : ZMod M)) : ℂ) ^ c := by
  refine Finset.sum_congr rfl fun c _ => ?_
  rw [← AddChar.map_nsmul_eq_pow, nsmul_eq_mul]
  congr 1
  push_cast
  ring

/-- **(1)** the factor attached to `s` vanishes at `ξ` iff `s` divides the order of `ξ` exactly -/
theorem phi_eq_zero_iff (s : ℕ) (hs : s ∈ primePowers M) (ξ : ZMod M) :
    phi M s ξ = 0 ↔ ExactDiv s (ord ξ) := by
  have hM : M ≠ 0 := NeZero.ne M
  rw [exactDiv_iff_dvd hM hs (ord_dvd ξ), ← Bridge.mul_natCast_eq_zero_iff,
    ← Bridge.mul_natCast_eq_zero_iff, phi_eq_geom]
  set ζ : ℂ := ZMod.stdAddChar (ξ * (gen M s : ZMod M)) with hζ
  have h1 : ζ = 1 ↔ ξ * (gen M s : ZMod M) = 0 := stdAddChar_eq_one_iff _
  have hp : ζ ^ s.minFac = 1 ↔ ξ * ((s.minFac * gen M s : ℕ) : ZMod M) = 0 := by
    rw [hζ, ← AddChar.map_nsmul_eq_pow, stdAddChar_eq_one_iff, nsmul_eq_mul]
    have : (s.minFac : ZMod M) * (ξ * (gen M s : ZMod M))
        = ξ * ((s.minFac * gen M s : ℕ) : ZMod M) := by
      push_cast
      ring
    rw [this]
  rw [← h1, ← hp]
  have hgeom := geom_sum_mul ζ s.minFac
  constructor
  · intro h0
    refine ⟨?_, ?_⟩
    · rw [h0, zero_mul] at hgeom
      exact sub_eq_zero.1 hgeom.symm
    · intro hζ1
      rw [hζ1] at h0
      simp only [one_pow, sum_const, card_range, nsmul_eq_mul, mul_one, Nat.cast_eq_zero] at h0
      exact (Nat.minFac_pos s).ne' h0
  · rintro ⟨hp1, hne⟩
    rw [hp1, sub_self] at hgeom
    exact (mul_eq_zero.1 hgeom).resolve_right (sub_ne_zero.2 hne)

/-! ### The product formula -/

/-- the digit vectors -/
def digits (S : Finset ℕ) : Finset (S → ℕ) :=
  Fintype.piFinset (fun s : S => Finset.range (s : ℕ).minFac)

/-- the value of a digit vector -/
def digit (M : ℕ) (S : Finset ℕ) (c : S → ℕ) : ZMod M := ∑ s : S, ((c s * gen M s : ℕ) : ZMod M)

omit [NeZero M] in
theorem digitSet_eq (S : Finset ℕ) : digitSet M S = (digits S).image (digit M S) := rfl

theorem map_sum_eq_prod {ι : Type*} (s : Finset ι) (f : ι → ZMod M) :
    (ZMod.stdAddChar (∑ i ∈ s, f i) : ℂ) = ∏ i ∈ s, ZMod.stdAddChar (f i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih => rw [Finset.sum_insert ha, Finset.prod_insert ha, AddChar.map_add_eq_mul, ih]

/-- **(2)** the product formula, with multiplicity -/
theorem sum_digits_char (S : Finset ℕ) (ξ : ZMod M) :
    ∑ c ∈ digits S, (ZMod.stdAddChar (ξ * digit M S c) : ℂ) = ∏ s ∈ S, phi M s ξ := by
  rw [← Finset.prod_coe_sort S (fun s => phi M s ξ)]
  unfold phi
  rw [Finset.prod_univ_sum]
  refine Finset.sum_congr rfl fun c _ => ?_
  rw [digit, Finset.mul_sum, map_sum_eq_prod]

/-! ### Injectivity of the digit map -/

/-- **(3)** for the set of all prime powers dividing `M`, the digit map is injective -/
theorem digit_injOn_full :
    Set.InjOn (digit M (primePowers M)) (digits (primePowers M) : Set (primePowers M → ℕ)) := by
  classical
  have hM : M ≠ 0 := NeZero.ne M
  have key : (fun v : ZMod M =>
      ((((digits (primePowers M)).filter (fun c => digit M (primePowers M) c = v)).card : ℂ) - 1))
        = 0 := by
    apply zmod_fourier_uniq
    intro ξ
    simp only [sub_mul, one_mul, Finset.sum_sub_distrib]
    rw [sum_stdAddChar_mul]
    have h1 : ∑ v : ZMod M,
        (((digits (primePowers M)).filter (fun c => digit M (primePowers M) c = v)).card : ℂ)
          * ZMod.stdAddChar (ξ * v)
        = ∑ c ∈ digits (primePowers M), (ZMod.stdAddChar (ξ * digit M (primePowers M) c) : ℂ) := by
      rw [← Finset.sum_fiberwise (digits (primePowers M)) (digit M (primePowers M))]
      refine Finset.sum_congr rfl fun v _ => ?_
      have h2 : ∀ c ∈ (digits (primePowers M)).filter (fun c => digit M (primePowers M) c = v),
          (ZMod.stdAddChar (ξ * digit M (primePowers M) c) : ℂ) = ZMod.stdAddChar (ξ * v) := by
        intro c hc
        rw [(Finset.mem_filter.1 hc).2]
      rw [Finset.sum_congr rfl h2, Finset.sum_const, nsmul_eq_mul]
    rw [h1, sum_digits_char]
    by_cases hξ : ξ = 0
    · subst hξ
      rw [ite_eq_left rfl, sub_eq_zero]
      have h3 : ∀ s ∈ primePowers M, phi M s (0 : ZMod M) = ((s.minFac : ℕ) : ℂ) := by
        intro s _
        simp [phi]
      rw [Finset.prod_congr rfl h3, ← Nat.cast_prod, prod_minFac_primePowers hM]
    · rw [ite_eq_right hξ, sub_zero]
      obtain ⟨s, hs, hsd⟩ :=
        exists_exactDiv hM (ord_dvd ξ) (fun h => hξ ((ord_eq_one_iff ξ).1 h))
      exact Finset.prod_eq_zero hs ((phi_eq_zero_iff s hs ξ).2 hsd)
  intro c hc c' hc' h
  have h1 := congrFun key (digit M (primePowers M) c)
  simp only [Pi.zero_apply, sub_eq_zero] at h1
  have h2 : ((digits (primePowers M)).filter
      (fun x => digit M (primePowers M) x = digit M (primePowers M) c)).card = 1 := by
    exact_mod_cast h1
  exact Finset.card_le_one.1 h2.le c (Finset.mem_filter.2 ⟨hc, rfl⟩) c'
    (Finset.mem_filter.2 ⟨hc', h.symm⟩)

/-- for every set of prime powers dividing `M`, the digit map is injective (extend by zeros) -/
theorem digit_injOn (S : Finset ℕ) (hS : S ⊆ primePowers M) :
    Set.InjOn (digit M S) (digits S : Set (S → ℕ)) := by
  classical
  -- the extension of a digit vector by zeros
  let E : (S → ℕ) → ℕ → ℕ := fun c n => if h : n ∈ S then c ⟨n, h⟩ else 0
  have hE : ∀ c : S → ℕ, digit M (primePowers M) (fun t => E c t) = digit M S c := by
    intro c
    unfold digit
    rw [Finset.sum_coe_sort (primePowers M) (fun n => ((E c n * gen M n : ℕ) : ZMod M)),
      ← Finset.sum_subset hS (fun n _ hn => by simp [E, hn]),
      ← Finset.sum_coe_sort S (fun n => ((E c n * gen M n : ℕ) : ZMod M))]
    refine Finset.sum_congr rfl fun s _ => ?_
    simp [E]
  have hmem : ∀ c ∈ digits S, (fun t : primePowers M => E c t) ∈ digits (primePowers M) := by
    intro c hc
    rw [digits, Fintype.mem_piFinset] at hc ⊢
    intro t
    by_cases ht : (t : ℕ) ∈ S
    · simp only [E, dite_eq_left ht]
      exact hc ⟨t, ht⟩
    · simp only [E, dite_eq_right ht, mem_range]
      exact Nat.minFac_pos _
  intro c hc c' hc' h
  have h3 := digit_injOn_full (hmem c hc) (hmem c' hc') (by rw [hE, hE]; exact h)
  funext s
  have h4 := congrFun h3 ⟨s, hS s.2⟩
  simpa [E] using h4

/-- the Fourier transform of a digit set is the product of its factors -/
theorem hat_digitSet (S : Finset ℕ) (hS : S ⊆ primePowers M) (ξ : ZMod M) :
    hat (digitSet M S) ξ = ∏ s ∈ S, phi M s ξ := by
  classical
  rw [hat, digitSet_eq, Finset.sum_image (digit_injOn S hS), sum_digits_char]

/-- the element `M / d` of `ZMod M` has order `d` -/
theorem ord_natCast_div {d : ℕ} (hd : d ∣ M) : ord ((M / d : ℕ) : ZMod M) = d := by
  have hM : M ≠ 0 := NeZero.ne M
  rw [ord, ZMod.val_natCast, ← Nat.gcd_rec, Nat.gcd_eq_right (Nat.div_dvd_of_dvd hd),
    Nat.div_div_self hd hM]

end DigitSets

open DigitSets

variable {M : ℕ} [NeZero M]

theorem card_digitSet (S : Finset ℕ) (hS : S ⊆ primePowers M) :
    (digitSet M S).card = ∏ s ∈ S, s.minFac := by
  classical
  rw [digitSet_eq, Finset.card_image_of_injOn (digit_injOn S hS), digits, Fintype.card_piFinset]
  simp only [card_range]
  exact Finset.prod_coe_sort S (fun s => s.minFac)

theorem zeroAt_digitSet (S : Finset ℕ) (hS : S ⊆ primePowers M) (d : ℕ) (hd : d ∣ M) :
    ZeroAt (digitSet M S) d ↔ ∃ s ∈ S, ExactDiv s d := by
  constructor
  · intro h
    have h1 := h _ (ord_natCast_div hd)
    rw [hat_digitSet S hS, Finset.prod_eq_zero_iff] at h1
    obtain ⟨s, hs, hs0⟩ := h1
    refine ⟨s, hs, ?_⟩
    have h2 := (phi_eq_zero_iff s (hS hs) _).1 hs0
    rwa [ord_natCast_div hd] at h2
  · rintro ⟨s, hs, hsd⟩ ξ hξ
    rw [hat_digitSet S hS]
    exact Finset.prod_eq_zero hs ((phi_eq_zero_iff s (hS hs) ξ).2 (hξ ▸ hsd))

end Pqr
