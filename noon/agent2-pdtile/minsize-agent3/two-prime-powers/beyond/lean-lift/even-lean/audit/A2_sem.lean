import Pnq.EvenFinal

/-! Audit of the even skeleton: reading lemmas for the definitions (`Bad3`, `ExceptionalPair`), proved here without
any of the fourteen `sorry` statements, and instances that show the hypotheses can be met.  Scratch file of the
audit; nothing else uses it. -/

open Pnq Polynomial

namespace AuditEven

variable {ι : Type*} [Fintype ι]

/-! ### `Bad3` for `3 ∤ d` is "`Φ_d` divides the signed mask modulo 3" -/

/-- for any field `K` in which `d ≠ 0` and which has a primitive `d`-th root: `Φ_d` divides `f` iff `f` vanishes at
every primitive `d`-th root of unity of `K` -/
theorem cyclotomic_dvd_iff_forall_isRoot {K : Type*} [Field K] {d : ℕ} (hd0 : 0 < d) {ζ0 : K}
    (hζ0 : IsPrimitiveRoot ζ0 d) (f : K[X]) :
    cyclotomic d K ∣ f ↔ ∀ ζ : K, IsPrimitiveRoot ζ d → f.IsRoot ζ := by
  rw [cyclotomic_eq_prod_X_sub_primitiveRoots hζ0]
  constructor
  · intro h ζ hζ
    have h1 : X - C ζ ∣ f := (Finset.dvd_prod_of_mem _ ((mem_primitiveRoots hd0).2 hζ)).trans h
    exact dvd_iff_isRoot.1 h1
  · intro h
    refine Finset.prod_dvd_of_coprime ?_ ?_
    · exact (pairwise_coprime_X_sub_C (K := K) (s := id) Function.injective_id).set_pairwise _
    · intro μ hμ
      rw [dvd_iff_isRoot]
      exact h μ ((mem_primitiveRoots hd0).1 hμ)

/-- `Bad3` says that the image of the signed mask in `F3[X]` vanishes at every primitive `d`-th root -/
theorem bad3_iff_forall_isRoot (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) :
    Bad3 e ε d ↔ ∀ ζ : F3, IsPrimitiveRoot ζ d → ((P e ε).map (Int.castRingHom F3)).IsRoot ζ := by
  constructor
  · intro h ζ hζ
    have h1 := h ζ hζ
    rw [val3_eq_eval_map] at h1
    exact h1
  · intro h ζ hζ
    have h1 := h ζ hζ
    rw [val3_eq_eval_map]
    exact h1

/-- over the algebraic closure -/
theorem bad3_iff_dvd_F3 (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (h3 : ¬ 3 ∣ d) :
    Bad3 e ε d ↔ cyclotomic d F3 ∣ (P e ε).map (Int.castRingHom F3) := by
  have hne : NeZero ((d : ℕ) : F3) := NeZero.of_not_dvd F3 h3
  have hd0 : 0 < d := Nat.pos_of_ne_zero fun h => h3 (h ▸ dvd_zero 3)
  obtain ⟨ζ0, hζ0⟩ := HasEnoughRootsOfUnity.exists_isPrimitiveRoot F3 d
  rw [bad3_iff_forall_isRoot]
  exact (cyclotomic_dvd_iff_forall_isRoot hd0 hζ0 _).symm

/-- over the field with three elements: `Φ_d` divides the signed mask in `(ℤ/3)[X]` -/
theorem bad3_iff_dvd_ZMod3 (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (h3 : ¬ 3 ∣ d) :
    Bad3 e ε d ↔ cyclotomic d (ZMod 3) ∣ (P e ε).map (Int.castRingHom (ZMod 3)) := by
  rw [bad3_iff_dvd_F3 e ε h3, ← map_dvd_map' (algebraMap (ZMod 3) F3), map_cyclotomic, Polynomial.map_map,
    Subsingleton.elim ((algebraMap (ZMod 3) F3).comp (Int.castRingHom (ZMod 3))) (Int.castRingHom F3)]

/-- a signing that is bad at `d` over `ℤ` is 3-bad at `d` (`3 ∤ d`): the case `i = 0` of M, proved here -/
theorem bad3_of_badAt_same (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (h3 : ¬ 3 ∣ d) (h : BadAt e ε d) : Bad3 e ε d := by
  rw [bad3_iff_dvd_ZMod3 e ε h3, ← map_cyclotomic d (Int.castRingHom (ZMod 3))]
  exact Polynomial.map_dvd _ h

/-! ### `Bad3` at `d` with `3 ∣ d`, `d ≠ 0`: every signing; at `d = 0`: a real condition -/

theorem bad3_of_three_dvd (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (hd0 : d ≠ 0) (h3 : 3 ∣ d) : Bad3 e ε d := by
  intro ζ hζ
  exfalso
  have : NeZero d := ⟨hd0⟩
  have hne : NeZero ((d : ℕ) : F3) := hζ.neZero'
  exact hne.out ((CharP.cast_eq_zero_iff F3 3 d).2 h3)

/-- `Bad3 e ε 0` implies that the signed mask vanishes at `0 ∈ F3` (which Mathlib counts as a primitive `0`-th root) -/
theorem val3_zero_of_bad3_zero (e : ι → ℕ) (ε : ι → Bool) (h : Bad3 e ε 0) : val3 e ε 0 = 0 :=
  h 0 IsPrimitiveRoot.zero

/-- so `Bad3 · · 0` is not always true: one element with exponent `0` -/
example : ¬ Bad3 (ι := Fin 1) ![0] ![true] 0 := by
  intro h
  have h0 := val3_zero_of_bad3_zero _ _ h
  simp [val3, sg] at h0

/-! ### the exponents need not be reduced -/

theorem bad3_mod (e : ι → ℕ) (ε : ι → Bool) {d n : ℕ} (hdn : d ∣ n) :
    Bad3 (fun k => e k % n) ε d ↔ Bad3 e ε d := by
  have key : ∀ ζ : F3, IsPrimitiveRoot ζ d → val3 (fun k => e k % n) ε ζ = val3 e ε ζ := by
    intro ζ hζ
    unfold val3
    refine Finset.sum_congr rfl fun k _ => ?_
    have h1 : ζ ^ n = 1 := by
      obtain ⟨c, rfl⟩ := hdn
      rw [pow_mul, hζ.pow_eq_one, one_pow]
    congr 1
    conv_rhs => rw [← Nat.div_add_mod (e k) n, pow_add, pow_mul, h1, one_pow, one_mul]
  constructor
  · intro h ζ hζ
    rw [← key ζ hζ]
    exact h ζ hζ
  · intro h ζ hζ
    rw [key ζ hζ]
    exact h ζ hζ

/-- the empty family: every signing (there is one) is 3-bad at every `d` -/
theorem bad3_of_isEmpty [IsEmpty ι] (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) : Bad3 e ε d := by
  intro ζ _
  simp [val3]

/-- one element is never 3-bad at a `d ≠ 0` prime to 3 -/
theorem not_bad3_one_elt (e : Fin 1 → ℕ) (ε : Fin 1 → Bool) {d : ℕ} (h3 : ¬ 3 ∣ d) : ¬ Bad3 e ε d := by
  intro h
  have hne : NeZero ((d : ℕ) : F3) := NeZero.of_not_dvd F3 h3
  obtain ⟨ζ, hζ⟩ := HasEnoughRootsOfUnity.exists_isPrimitiveRoot F3 d
  have hd0 : d ≠ 0 := fun h0 => h3 (h0 ▸ dvd_zero 3)
  have hz : ζ ≠ 0 := hζ.ne_zero hd0
  have h0 := h ζ hζ
  have hs : (sg (ε 0) : F3) ≠ 0 := by
    cases ε 0 <;> simp [sg]
  simp only [val3, Fin.sum_univ_one] at h0
  exact (mul_ne_zero hs (pow_ne_zero _ hz)) h0

/-! ### `ExceptionalPair` -/

/-- the additive order in `ZMod n`, `n ≠ 0`, is `n / gcd(n, value)` -/
theorem addOrderOf_eq {n : ℕ} [NeZero n] (x : ZMod n) : addOrderOf x = n / n.gcd x.val := by
  conv_lhs => rw [← ZMod.natCast_zmod_val x]
  exact ZMod.addOrderOf_coe _ (NeZero.ne n)

/-- the definition with the order worked out -/
theorem exceptionalPair_iff {n : ℕ} [NeZero n] (w : ZMod n → ℕ) :
    ExceptionalPair w ↔ ∃ a b : ZMod n, w = Pi.single a 1 + Pi.single b 1 ∧ Even (n / n.gcd (a - b).val) := by
  unfold ExceptionalPair
  simp only [addOrderOf_eq]

/-- two equal marks (one mark of multiplicity 2 and nothing else) are not an exceptional pair -/
theorem not_exceptionalPair_double {n : ℕ} (a : ZMod n) :
    ¬ ExceptionalPair (Pi.single a 1 + Pi.single a 1 : ZMod n → ℕ) := by
  rintro ⟨a', b', h, hev⟩
  have ha : a' = a := by
    by_contra hne
    have h1 := congrFun h a'
    simp [Pi.single_apply, hne] at h1
    split_ifs at h1
  have hb : b' = a := by
    by_contra hne
    have h1 := congrFun h b'
    simp [Pi.single_apply, hne] at h1
  subst ha
  subst hb
  simp at hev

/-- the same multiset written as one mark of multiplicity 2 -/
theorem single_two {n : ℕ} (a : ZMod n) :
    (Pi.single a 2 : ZMod n → ℕ) = Pi.single a 1 + Pi.single a 1 := by
  funext x
  by_cases hx : x = a <;> simp [hx]

/-- an exceptional pair has exactly two elements -/
theorem sum_of_exceptionalPair {n : ℕ} [NeZero n] (w : ZMod n → ℕ) (h : ExceptionalPair w) : ∑ x, w x = 2 := by
  obtain ⟨a, b, rfl, -⟩ := h
  simp [Finset.sum_add_distrib]

/-- on `ZMod 1` nothing is an exceptional pair -/
theorem not_exceptionalPair_one (w : ZMod 1 → ℕ) : ¬ ExceptionalPair w := by
  rintro ⟨a, b, -, hev⟩
  have : a - b = 0 := Subsingleton.elim _ _
  rw [this] at hev
  simp at hev

/-- for `n = 0` (not allowed in the final statements) every pair of different integers would be "exceptional" -/
example : ExceptionalPair (n := 0) (Pi.single (0 : ZMod 0) 1 + Pi.single (1 : ZMod 0) 1) := by
  refine ⟨0, 1, rfl, ?_⟩
  have h : addOrderOf ((0 : ZMod 0) - 1) = 0 := by
    rw [addOrderOf_eq_zero_iff']
    intro k hk hz
    change k • ((0 : ℤ) - 1) = 0 at hz
    simp at hz
    omega
  rw [h]
  exact ⟨0, rfl⟩

/-! the order of `a - b` (in the form `n / gcd n (a - b).val` of `exceptionalPair_iff`) is even exactly when the
power of 2 in `n` does not divide `a - b`: kernel checks for some `n` -/

example : ∀ a b : ZMod 2, Even (2 / Nat.gcd 2 (a - b).val) ↔ ¬ (2 : ℕ) ∣ (a - b).val := by decide
example : ∀ a b : ZMod 4, Even (4 / Nat.gcd 4 (a - b).val) ↔ ¬ (4 : ℕ) ∣ (a - b).val := by decide
example : ∀ a b : ZMod 6, Even (6 / Nat.gcd 6 (a - b).val) ↔ ¬ (2 : ℕ) ∣ (a - b).val := by decide
example : ∀ a b : ZMod 8, Even (8 / Nat.gcd 8 (a - b).val) ↔ ¬ (8 : ℕ) ∣ (a - b).val := by decide
example : ∀ a b : ZMod 9, ¬ Even (9 / Nat.gcd 9 (a - b).val) := by decide
example : ∀ a b : ZMod 12, Even (12 / Nat.gcd 12 (a - b).val) ↔ ¬ (4 : ℕ) ∣ (a - b).val := by decide
example : ∀ a b : ZMod 20, Even (20 / Nat.gcd 20 (a - b).val) ↔ ¬ (4 : ℕ) ∣ (a - b).val := by decide

/-- `{0, 2}` on `ZMod 6` (difference of order 3) is not an exceptional pair -/
theorem not_exceptionalPair_6_0_2 :
    ¬ ExceptionalPair (Pi.single (0 : ZMod 6) 1 + Pi.single (2 : ZMod 6) 1 : ZMod 6 → ℕ) := by
  rw [exceptionalPair_iff]
  have key : ∀ a b : ZMod 6, (Pi.single (0 : ZMod 6) 1 + Pi.single (2 : ZMod 6) 1 : ZMod 6 → ℕ)
      = Pi.single a 1 + Pi.single b 1 → ¬ Even (6 / Nat.gcd 6 (a - b).val) := by decide
  rintro ⟨a, b, h, hev⟩
  exact key a b h hev

/-- `{0, 1}` on `ZMod 6` (difference of order 6) is an exceptional pair -/
theorem exceptionalPair_6_0_1 :
    ExceptionalPair (Pi.single (0 : ZMod 6) 1 + Pi.single (1 : ZMod 6) 1 : ZMod 6 → ℕ) := by
  rw [exceptionalPair_iff]
  exact ⟨0, 1, rfl, by decide⟩

end AuditEven

#print axioms AuditEven.bad3_iff_dvd_F3
#print axioms AuditEven.bad3_iff_dvd_ZMod3
#print axioms AuditEven.bad3_of_badAt_same
#print axioms AuditEven.bad3_of_three_dvd
#print axioms AuditEven.bad3_mod
#print axioms AuditEven.not_bad3_one_elt
#print axioms AuditEven.exceptionalPair_iff
#print axioms AuditEven.not_exceptionalPair_double
#print axioms AuditEven.sum_of_exceptionalPair
#print axioms AuditEven.not_exceptionalPair_one
