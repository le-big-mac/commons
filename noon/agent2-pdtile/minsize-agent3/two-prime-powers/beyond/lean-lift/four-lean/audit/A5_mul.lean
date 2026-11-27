/-
The lifting for every `N` and every `s`: the sets of sizes on `ZMod (N * s)` and on `ZMod N` are the same.
`Lift.sizes_eq_odd` of `Pnq/LiftAll.lean` without its hypothesis that `s` is odd; from it and `sizes_eq_two_all` of
`Pnq/SignFinal.lean`.
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignFinal
import Pnq.LiftAll

open Finset

namespace Pnq

/-- **Sizes are the same on `ZMod (N * s)`, every `N`, every `s ≥ 1`.**  For a set `P` of divisors of `N`, the sizes of
the nonempty multisets on `ZMod (N * s)` whose mask is divisible by `Φ_d`, `d ∣ N * s`, `d ≠ 1`, exactly for `d ∈ P` are
the sizes of the nonempty multisets on `ZMod N` whose mask is divisible by `Φ_d`, `d ∣ N`, `d ≠ 1`, exactly for
`d ∈ P`. -/
theorem sizes_eq_mul_all {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  sorry

end Pnq

/-! Audit of the sixteenth statement.  Everything above this comment is `SignMul.as-fixed.lean`, byte for byte (the
statement with `sorry`).  Below: its print, its comparison with `Lift.sizes_eq_odd` as elaborated, reading lemmas,
instances, and its derivation from `sizes_eq_two_all` and finished theorems. -/

#check @Pnq.sizes_eq_mul_all
#check @Pnq.Lift.sizes_eq_odd
#print axioms Pnq.sizes_eq_mul_all
#print axioms Pnq.Lift.sizes_eq_odd
#print axioms Pnq.Lift.sizes_eq

namespace AuditMul
open Pnq

/-! ### The audited statements are instances of the sixteenth -/

-- `Lift.sizes_eq_odd` (any `N`, odd `s`)
example {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (_hs : Odd s) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} :=
  sizes_eq_mul_all s P hP

-- `sizes_eq_two_all` (any `N`, `s = 2`)
example {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * 2 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} :=
  sizes_eq_mul_all 2 P hP

-- `Lift.sizes_eq_mul` (`N = p^n * q`, any `s`)
example (p q n s : ℕ) [Fact p.Prime] [Fact q.Prime] [NeZero s] (_hpq : p ≠ q) (P : Finset ℕ)
    (hP : ∀ d ∈ P, d ∣ p ^ n * q) :
    {t | ∃ w' : ZMod (p ^ n * q * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} :=
  sizes_eq_mul_all s P hP

/-! ### The sixteenth from the fifteenth and finished theorems -/

/-- the same statement, derived from `sizes_eq_two_all` (the factors 2 of `s`) and the finished `Lift.sizes_eq` (its
odd prime factors), by induction on `s` -/
theorem derived {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  have key : ∀ (s : ℕ) [NeZero s], Lift.AllAux.sizes (N * s) P = Lift.AllAux.sizes N P := by
    intro s
    induction s using Nat.strong_induction_on with
    | _ s ih =>
      intro _
      by_cases h1 : s = 1
      · subst h1
        exact Lift.AllAux.sizes_congr (mul_one N) P
      · obtain ⟨r, hr, s', rfl⟩ := Nat.exists_prime_and_dvd h1
        have hs'0 : s' ≠ 0 := by
          rintro rfl
          exact NeZero.ne (r * 0) (mul_zero r)
        have : NeZero s' := ⟨hs'0⟩
        have : Fact r.Prime := ⟨hr⟩
        have hlt : s' < r * s' := lt_mul_of_one_lt_left (Nat.pos_of_ne_zero hs'0) hr.one_lt
        have e1 : Lift.AllAux.sizes (N * (r * s')) P = Lift.AllAux.sizes (N * s' * r) P :=
          Lift.AllAux.sizes_congr (by ring) P
        have e2 : Lift.AllAux.sizes (N * s' * r) P = Lift.AllAux.sizes (N * s') P := by
          by_cases hr2 : r = 2
          · subst hr2
            exact sizes_eq_two_all (N := N * s') P fun d hd => Dvd.dvd.mul_right (hP d hd) s'
          · exact Lift.sizes_eq (N := N * s') (r := r) hr2 P fun d hd => Dvd.dvd.mul_right (hP d hd) s'
        exact e1.trans (e2.trans (ih s' hlt))
  exact key s

/-! ### Reading lemmas (they use no statement of the skeleton) -/

/-- For `P` a set of divisors of `N`: "divisible by `Φ_d`, among the `d ≠ 1` that divide `N * s`, exactly for `d ∈ P`"
says "exactly for `d ∈ P` among the `d ≠ 1` that divide `N`, and by no `Φ_d` with `d ∣ N * s`, `d ∤ N`". -/
theorem pattern_iff {N s : ℕ} [NeZero N] [NeZero s] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N)
    (w' : ZMod (N * s) → ℕ) :
    (∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)) ↔
    ((∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)) ∧
      ∀ d, d ∣ N * s → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w') := by
  constructor
  · intro h
    refine ⟨fun d hd hd1 => h d (Dvd.dvd.mul_right hd s) hd1, fun d hd hdN hdiv => ?_⟩
    have hd1 : d ≠ 1 := by
      rintro rfl
      exact hdN (one_dvd N)
    exact hdN (hP d ((h d hd hd1).1 hdiv))
  · rintro ⟨h1, h2⟩ d hd hd1
    by_cases hdN : d ∣ N
    · exact h1 d hdN hd1
    · exact iff_of_false (h2 d hd hdN) fun hm => hdN (hP d hm)

/-- whether `1 ∈ P` makes no difference -/
theorem erase_one {M : ℕ} [NeZero M] (P : Finset ℕ) (w : ZMod M → ℕ) :
    (∀ d, d ∣ M → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)) ↔
    (∀ d, d ∣ M → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P.erase 1)) := by
  constructor
  · intro h d hd h1
    rw [h d hd h1, Finset.mem_erase]
    exact ⟨fun hh => ⟨h1, hh⟩, fun hh => hh.2⟩
  · intro h d hd h1
    rw [h d hd h1, Finset.mem_erase]
    exact ⟨fun hh => hh.2, fun hh => ⟨h1, hh⟩⟩

/-- a multiset that satisfies the clause for some `P` (on any group) with `0 < t` is not empty, and the size is the
number of elements: `t = ∑ x, w x` is in the statement itself -/
example {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (t : ℕ) (h : ∑ x, w x = t) (ht : 0 < t) : ∃ x, w x ≠ 0 :=
  Lift.Aux.exists_ne_zero_of_sum_pos w (h ▸ ht)

/-- `s = 1`: the two groups are the same, and the statement is true by rewriting `N * 1 = N` -/
example {N : ℕ} [NeZero N] (P : Finset ℕ) : Lift.AllAux.sizes (N * 1) P = Lift.AllAux.sizes N P :=
  Lift.AllAux.sizes_congr (mul_one N) P

/-- `d = 0` never divides the orders -/
example (N s : ℕ) [NeZero N] [NeZero s] : ¬ (0 ∣ N * s) := by
  intro h
  exact Nat.mul_ne_zero (NeZero.ne N) (NeZero.ne s) (Nat.eq_zero_of_zero_dvd h)

/-! ### Instances: no hypothesis is contradictory -/

example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 105) := sizes_eq_mul_all (N := 105) 12 P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 36) := sizes_eq_mul_all (N := 36) 4 P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 1) := sizes_eq_mul_all (N := 1) 8 P hP
example {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) := sizes_eq_mul_all (N := N) 1 P hP
example := sizes_eq_mul_all (N := 210) 6 ∅ (by simp)
example := sizes_eq_mul_all (N := 30) 4 {1, 2, 15} (by decide)

end AuditMul

#print axioms AuditMul.derived
#print axioms AuditMul.pattern_iff
#print axioms AuditMul.erase_one

/-! ### The statement as elaborated: fingerprint, and comparison with `Lift.sizes_eq_odd` -/

open Lean Meta Elab Command in
run_cmd liftTermElabM do
  let env ← getEnv
  let some a := env.find? ``Pnq.sizes_eq_mul_all | throwError "missing sizes_eq_mul_all"
  let some b := env.find? ``Pnq.Lift.sizes_eq_odd | throwError "missing sizes_eq_odd"
  let some c := env.find? ``AuditMul.derived | throwError "missing derived"
  let pr (e : Expr) : MetaM String :=
    withOptions (fun o => ((o.setBool `pp.explicit true).setBool `pp.proofs true).setBool `pp.fullNames true) do
      pure (toString (← ppExpr e))
  IO.println s!"Pnq.sizes_eq_mul_all: type hash {a.type.hash}, explicit print {(← pr a.type).length} characters"
  IO.println s!"Pnq.Lift.sizes_eq_odd: type hash {b.type.hash}, explicit print {(← pr b.type).length} characters"
  IO.println s!"AuditMul.derived against Pnq.sizes_eq_mul_all: same expression {c.type == a.type}, same hash {c.type.hash == a.type.hash}"
  forallBoundedTelescope b.type (some 5) fun xs body => do
    let hs := xs[4]!
    IO.println s!"the fifth argument of sizes_eq_odd: {← ppExpr (← inferType hs)}"
    IO.println s!"the rest of sizes_eq_odd mentions it: {body.containsFVar hs.fvarId!}"
    let t ← mkForallFVars (xs.extract 0 4) body
    IO.println s!"sizes_eq_odd with that argument removed, against sizes_eq_mul_all: same expression {t == a.type}, same hash {t.hash == a.type.hash}, same explicit print {(← pr t) == (← pr a.type)}, definitionally equal {← isDefEq t a.type}"

set_option pp.explicit true
set_option pp.fullNames true
set_option pp.proofs true
#check @Pnq.sizes_eq_mul_all
#check @Pnq.Lift.sizes_eq_odd
