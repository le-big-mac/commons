import Pnq.LiftMin
/-! Small facts, proved by Lean, about the pieces the statements are made of.  (Audit file; nothing here is used by the project.) -/
open Finset
namespace AuditLift
open Pnq Pnq.Lift

section
variable {N r : ℕ} [NeZero N] [Fact r.Prime]

-- (1) the map used in `reduce` is "take the representative in [0, N*r) and reduce it modulo N"
example (y : ZMod (N * r)) :
    ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = ((y.val : ℕ) : ZMod N) := by
  rw [ZMod.castHom_apply, ZMod.natCast_val]
example (y : ZMod (N * r)) :
    (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y).val = y.val % N := by
  rw [ZMod.castHom_apply, ← ZMod.natCast_val, ZMod.val_natCast]
-- the representative is in [0, N*r)
example (y : ZMod (N * r)) : y.val < N * r := ZMod.val_lt y
-- every residue is hit by exactly r elements?  at least: the map is onto
example : Function.Surjective (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N)) :=
  ZMod.castHom_surjective (Nat.dvd_mul_right N r)

-- (2) `reduce` written with the representative: the multiplicity of x is the sum of w' over the y with y.val % N = x.val
example (w' : ZMod (N * r) → ℕ) (x : ZMod N) :
    reduce w' x = ∑ y : ZMod (N * r), if y.val % N = x.val then w' y else 0 := by
  unfold reduce
  refine Finset.sum_congr rfl fun y _ => ?_
  have h : (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x) ↔ (y.val % N = x.val) := by
    rw [← Aux.val_castHom]
    exact ⟨fun h => by rw [h], fun h => ZMod.val_injective N h⟩
  by_cases hx : ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x
  · rw [ite_eq_left hx, ite_eq_left (h.1 hx)]
  · rw [ite_eq_right hx, ite_eq_right (fun h' => hx (h.2 h'))]

-- (3) d = 0 never satisfies `d ∣ N * r`; so the clause `∀ d, d ∣ N * r → ...` speaks of true divisors only
example : ¬ (0 ∣ N * r) := by
  intro h
  exact (NeZero.ne (N * r)) (zero_dvd_iff.1 h)
-- N * r itself is a divisor of N * r that does not divide N
example : N * r ∣ N * r ∧ ¬ (N * r ∣ N) := by
  refine ⟨dvd_rfl, fun h => ?_⟩
  have hr : 2 ≤ r := (Fact.out : r.Prime).two_le
  have hN : 0 < N := Nat.pos_of_ne_zero (NeZero.ne N)
  have := Nat.le_of_dvd hN h
  nlinarith

-- (4) the "no new divisor" clause already excludes the empty multiset: `0 < s` is implied on the big group
theorem pos_of_no_new (w' : ZMod (N * r) → ℕ)
    (h : ∀ d, d ∣ N * r → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w') : 0 < ∑ y, w' y := by
  have hnd : ¬ (N * r ∣ N) := by
    intro h
    have hr : 2 ≤ r := (Fact.out : r.Prime).two_le
    have hN : 0 < N := Nat.pos_of_ne_zero (NeZero.ne N)
    have := Nat.le_of_dvd hN h
    nlinarith
  obtain ⟨x, hx⟩ := Aux.exists_ne_zero_of_not_dvd (h (N * r) dvd_rfl hnd)
  exact lt_of_lt_of_le (Nat.pos_of_ne_zero hx) (Finset.single_le_sum (fun _ _ => Nat.zero_le _) (Finset.mem_univ x))

-- (5) the empty multiset has mask 0, divisible by every Φ_d: this is why `hw` and `0 < s` are there
example (d : ℕ) : Polynomial.cyclotomic d ℤ ∣ maskW (fun _ : ZMod N => 0) := by
  rw [Aux.maskW_eq_zero (fun _ => rfl)]
  exact dvd_zero _

-- (6) Φ_1 divides the mask only of the empty multiset (so leaving d = 1 out of the pattern loses nothing)
example (w : ZMod N → ℕ) (h : Polynomial.cyclotomic 1 ℤ ∣ maskW w) : ∑ x, w x = 0 := by
  rw [Polynomial.cyclotomic_one] at h
  obtain ⟨Q, hQ⟩ := h
  have h1 : (maskW w).eval 1 = 0 := by rw [hQ]; simp
  have h2 : (maskW w).eval 1 = ((∑ x, w x : ℕ) : ℤ) := by
    simp [maskW, Polynomial.eval_finsetSum]
  rw [h2] at h1
  exact_mod_cast h1
end

-- (7) what Mathlib's cyclotomic is at 0 and 1, and on a prime
example : Polynomial.cyclotomic 0 ℤ = 1 := Polynomial.cyclotomic_zero ℤ
example : Polynomial.cyclotomic 1 ℤ = Polynomial.X - 1 := Polynomial.cyclotomic_one ℤ
example : Polynomial.cyclotomic 2 ℤ = Polynomial.X + 1 := Polynomial.cyclotomic_two ℤ
example (n : ℕ) (hn : 0 < n) : ∏ i ∈ n.divisors, Polynomial.cyclotomic i ℤ = Polynomial.X ^ n - 1 :=
  Polynomial.prod_cyclotomic_eq_X_pow_sub_one hn ℤ
example (n : ℕ) : (Polynomial.cyclotomic n ℤ).natDegree = n.totient := Polynomial.natDegree_cyclotomic n ℤ
example (n : ℕ) : (Polynomial.cyclotomic n ℤ).Monic := Polynomial.cyclotomic.monic n ℤ

-- (8) `⊆` on finsets, shown by the printer as `≤`, is inclusion; `IsLeast` is "belongs and is a lower bound"
example (A B : Finset ℕ) : A ⊆ B ↔ ∀ x ∈ A, x ∈ B := Finset.subset_iff
example (A B : Finset ℕ) : (A ≤ B) = (A ⊆ B) := rfl
example (S : Set ℕ) (a : ℕ) : IsLeast S a ↔ a ∈ S ∧ ∀ b ∈ S, a ≤ b := Iff.rfl
example (n ℓ : ℕ) : ℓ ∈ Finset.Icc 1 n ↔ 1 ≤ ℓ ∧ ℓ ≤ n := Finset.mem_Icc

-- (9) the group of the three theorems is ZMod ((p^n * q) * r), syntactically
example (p q n r : ℕ) : ZMod (p ^ n * q * r) = ZMod ((p ^ n * q) * r) := rfl
example (p q n r : ℕ) : (p ^ n * q * r) = (HMul.hMul (HMul.hMul (HPow.hPow p n) q) r) := rfl

-- (10) "levels" clauses: the written-out form is the old `levelsEW w = Es`, given `hE` (my own proof, not the file's)
example (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (w : ZMod (p ^ n * q) → ℕ) (Es : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) :
    levelsEW w = Es ↔ ∀ ℓ ∈ Finset.Icc 1 n, (Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) := by
  classical
  unfold levelsEW
  constructor
  · intro h ℓ hℓ
    rw [← h, Finset.mem_filter]
    tauto
  · intro h
    ext ℓ
    rw [Finset.mem_filter]
    constructor
    · rintro ⟨h1, h2⟩
      exact (h ℓ h1).1 h2
    · intro hℓ
      exact ⟨hE hℓ, (h ℓ (hE hℓ)).2 hℓ⟩
-- without `hE` the two differ: the written-out form does not see elements of Es outside 1..n
example (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (w : ZMod (p ^ 0 * q) → ℕ) :
    (∀ ℓ ∈ Finset.Icc 1 0, (Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ ({7} : Finset ℕ))) ∧
      levelsEW w ≠ ({7} : Finset ℕ) := by
  classical
  refine ⟨fun ℓ hℓ => absurd hℓ (by simp), ?_⟩
  unfold levelsEW
  simp

-- (11) the hypotheses can be met together: instances of each theorem (so none is empty of content for lack of cases)
instance : Fact (Nat.Prime 2) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 3) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩
example := minsize_unbalanced_lift 2 3 1 3 (by decide) (by decide) ∅ {1} (by simp) (by simp)
example := minsize_unbalanced_lift 2 3 0 3 (by decide) (by decide) ∅ ∅ (by simp) (by simp)
example := minsize_unbalanced_lift 3 2 2 3 (by decide) (by decide) {2} {1, 2} (by decide) (by decide)
example := minsize_balanced_all_lift 2 3 2 3 (by decide) (by decide) {1} (by decide)
example := minsize_balanced_all_lift 2 3 0 5 (by decide) (by decide) ∅ (by simp)
example := minsize_balanced_lift 2 3 2 3 (by decide) (by decide) {1} {2} (by decide) (by decide) 1 (le_refl 1) (by decide)
  (fun ℓ h1 h2 => absurd h2 (by omega)) (by decide)
example := minsize_balanced_lift 3 2 2 3 (by decide) (by decide) ∅ {1} (by decide) (by decide) 2 (by decide) (le_refl 2)
  (fun ℓ h1 h2 => by have : ℓ = 1 := by omega
                     subst this; simp) (by decide)
example := sizes_eq (N := 6) (r := 3) (by decide) {2, 3} (by decide)
example := sizes_eq (N := 1) (r := 3) (by decide) ∅ (by simp)
example := sizes_eq (N := 1) (r := 3) (by decide) {1} (by simp)
example := exists_lift (N := 1) (r := 3) (by decide) (fun _ => 2) ⟨0, by decide⟩
-- with n = 0 the third theorem has no instance: 1 ≤ a0 ≤ 0 is impossible (as for the old theorem)
example (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ 0) : False := by omega

-- (12) in `sizes_eq`, a `P` containing 1 gives the same two sets as `P` without it; a `P` containing 0 is excluded by `hP`
example {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) : 0 ∉ P := by
  intro h
  exact (NeZero.ne N) (zero_dvd_iff.1 (hP 0 h))
example {N : ℕ} [NeZero N] (P : Finset ℕ) (w : ZMod N → ℕ) :
    (∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)) ↔
    (∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P.erase 1)) := by
  refine forall_congr' fun d => forall_congr' fun _ => forall_congr' fun hd1 => ?_
  rw [Finset.mem_erase]
  tauto

end AuditLift
#print axioms AuditLift.pos_of_no_new
