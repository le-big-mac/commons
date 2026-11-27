import Pnq.SignFinal
/-! Audit: (1) a fingerprint of the ten definitions and the fifteen statements as elaborated (structural hash of the type,
the number of characters of its fully explicit print, and for a definition the hash of its value), to be compared with
the same file run in a project where the proofs are filled in;
(2) the three final statements have the audited statements of `Pnq/Sign.lean` and `Pnq/Lift2.lean` as instances;
(3) some values of `live` and `rank` checked by the kernel (`decide`);
(4) the Mathlib facts that pin down `Polynomial.cyclotomic`. -/
open Lean Meta Elab Command

def auditNamesSigns : List Name := [``Pnq.sg, ``Pnq.P, ``Pnq.BadAt, ``Pnq.badSet, ``Pnq.classSum, ``Pnq.live, ``Pnq.rank,
  ``Pnq.IsPivot, ``Pnq.μ, ``Pnq.lhsN1,
  ``Pnq.classSum_eq_of_badAt, ``Pnq.badAt_of_not_live, ``Pnq.card_badSet_mul_two_pow_card_le, ``Pnq.badAt_one_iff,
  ``Pnq.card_badSet_one, ``Pnq.rank_lt_card_image, ``Pnq.exists_isPivot, ``Pnq.card_badSet_mul_two_pow_rank_le,
  ``Pnq.rank_lt_card, ``Pnq.card_badSet_three_pow_mul_le, ``Pnq.lhsN1_lt_one, ``Pnq.exists_not_badAt,
  ``Pnq.exists_signs_odd, ``Pnq.exists_lift_two_all, ``Pnq.sizes_eq_two_all, ``Pnq.mem_badSet, ``Pnq.live_iff,
  ``Pnq.maskW, ``Pnq.Lift.reduce, ``Pnq.Lift.TwoAux.exists_lift_two_aux]

run_cmd liftTermElabM do
  let env ← getEnv
  for nm in auditNamesSigns do
    let some ci := env.find? nm | throwError "missing {nm}"
    let s ← withOptions (fun o => ((o.setBool `pp.explicit true).setBool `pp.proofs true).setBool `pp.fullNames true) do
      pure (toString (← ppExpr ci.type))
    let vh := match ci with
      | .defnInfo d => s!" value hash {d.value.hash}"
      | _ => ""
    IO.println s!"{nm}: type hash {ci.type.hash}, explicit print {s.length} characters{vh}"

-- (2) the audited statements for `p^a * q^b` are instances of the new ones
example (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (_hpq : p ≠ q) (a b : ℕ)
    (w : ZMod (p ^ a * q ^ b) → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ u v : ZMod (p ^ a * q ^ b) → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ p ^ a * q ^ b → ¬ Polynomial.cyclotomic d ℤ ∣ Pnq.maskW u - Pnq.maskW v := by
  have hpp : p.Prime := Fact.out
  have hqp : q.Prime := Fact.out
  have hN' : ¬ 2 ∣ p ^ a * q ^ b := by
    intro h
    rcases (Nat.Prime.dvd_mul Nat.prime_two).1 h with h | h
    · exact hp ((Nat.prime_dvd_prime_iff_eq Nat.prime_two hpp).1 (Nat.prime_two.dvd_of_dvd_pow h)).symm
    · exact hq ((Nat.prime_dvd_prime_iff_eq Nat.prime_two hqp).1 (Nat.prime_two.dvd_of_dvd_pow h)).symm
  exact Pnq.exists_signs_odd (p ^ a * q ^ b) hN' w hw

example {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (_hp : p ≠ 2) (_hq : q ≠ 2) (_hpq : p ≠ q)
    (k a b : ℕ) (_hN : N = 2 ^ k * (p ^ a * q ^ b)) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, Pnq.Lift.reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w' :=
  Pnq.exists_lift_two_all w hw

example {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (_hp : p ≠ 2) (_hq : q ≠ 2) (_hpq : p ≠ q)
    (k a b : ℕ) (_hN : N = 2 ^ k * (p ^ a * q ^ b)) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * 2 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w ↔ d ∈ P)} :=
  Pnq.sizes_eq_two_all P hP

-- the types of the two pairs that differ only by hypotheses: the conclusions are the same expressions
example : ∀ {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (_ : p ≠ 2) (_ : q ≠ 2) (_ : p ≠ q)
    (k a b : ℕ) (_ : N = 2 ^ k * (p ^ a * q ^ b)) (w : ZMod N → ℕ) (_ : ∃ x, w x ≠ 0),
    ∃ w' : ZMod (N * 2) → ℕ, Pnq.Lift.reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w' := @Pnq.Lift.exists_lift_two

-- (3) values by the kernel
example : Pnq.live (ι := Fin 5) ![0, 1, 2, 3, 6] 3 1 = true := by decide
example : Pnq.live (ι := Fin 5) ![0, 1, 2, 3, 6] 3 2 = true := by decide
example : Pnq.live (ι := Fin 5) ![0, 1, 2, 3, 6] 3 3 = false := by decide
example : Pnq.live (ι := Fin 5) ![0, 1, 2, 3, 6] 3 0 = false := by decide
example : Pnq.rank (ι := Fin 5) ![0, 1, 2, 3, 6] 3 3 = 2 := by decide
example : Pnq.live (ι := Fin 5) ![0, 1, 2, 3, 6] 2 2 = true := by decide
example : Pnq.live (ι := Fin 2) ![0, 2] 2 1 = false := by decide
example : Pnq.live (ι := Fin 2) ![0, 2] 2 2 = true := by decide
example : Pnq.rank (ι := Fin 2) ![0, 2] 2 2 = 1 := by decide
example : Pnq.live (ι := Fin 0) ![] 3 1 = false := by decide
example : Pnq.rank (ι := Fin 7) ![0, 3, 5, 6, 9, 10, 12] 5 2 = 1 := by decide

-- (4) what fixes Mathlib's cyclotomic polynomials
#check @Polynomial.prod_cyclotomic_eq_X_pow_sub_one   -- the product over the divisors of n is X^n - 1
#check @Polynomial.cyclotomic.monic
#check @Polynomial.natDegree_cyclotomic               -- degree = totient
#check @Polynomial.cyclotomic_prime                   -- Φ_p = 1 + X + ... + X^(p-1)
#check @Polynomial.cyclotomic_prime_pow_eq_geom_sum
#check @Polynomial.isRoot_cyclotomic_iff
