import Pnq.LiftAll
/-! Audit: (1) a fingerprint of the eight statements as elaborated (structural hash of the type, and the number of characters of
its fully explicit print), to be compared with the same file run in a project where the proofs are filled in;
(2) spot values of the rule checked by the kernel (`decide`), against the `#eval` values used by the search programs;
(3) the Mathlib facts that pin down `Polynomial.cyclotomic`. -/
open Lean Meta Elab Command

def auditNames6 : List Name := [``Pnq.Lift.exists_signs, ``Pnq.Lift.exists_lift_two, ``Pnq.Lift.sizes_eq_two,
  ``Pnq.Lift.sizes_eq_odd, ``Pnq.Lift.sizes_eq_mul, ``Pnq.Lift.minsize_unbalanced_mul,
  ``Pnq.Lift.minsize_balanced_all_mul, ``Pnq.Lift.minsize_balanced_mul, ``Pnq.Lift.reduce, ``Pnq.maskW, ``Pnq.minU,
  ``Pnq.minB, ``Pnq.xOf, ``Pnq.gOf, ``Pnq.Lift.instNeZeroMul, ``Pnq.instNeZeroNatHMulHPow_pnq]

run_cmd liftTermElabM do
  let env ← getEnv
  for nm in auditNames6 do
    let some ci := env.find? nm | throwError "missing {nm}"
    let s ← withOptions (fun o => ((o.setBool `pp.explicit true).setBool `pp.proofs true).setBool `pp.fullNames true) do
      pure (toString (← ppExpr ci.type))
    let vh := match ci with
      | .defnInfo d => s!" value hash {d.value.hash}"
      | _ => ""
    IO.println s!"{nm}: type hash {ci.type.hash}, explicit print {s.length} characters{vh}"

-- (2) values of the rule, by the kernel
example : Pnq.minU 2 3 ∅ ∅ = 1 := by decide
example : Pnq.minU 2 3 ∅ {1} = 5 := by decide
example : Pnq.minU 2 3 {1} {2} = 10 := by decide
example : Pnq.minU 3 2 ∅ {1, 2} = 11 := by decide
example : Pnq.minU 2 3 {1, 2} {3} = 20 := by decide
example : Pnq.minB 2 3 ∅ ∅ 1 = 3 := by decide
example : Pnq.minB 2 3 {1} {2} 1 = 18 := by decide
example : Pnq.minB 2 3 ∅ {2, 3} 1 = 15 := by decide
example : Pnq.minB 2 3 {1} {2, 3} 1 = 30 := by decide
example : Pnq.minB 2 3 {1, 2} {2, 3} 1 = 36 := by decide
example : Pnq.minB 2 3 {2} {1, 3} 2 = 18 := by decide
example : Pnq.minB 3 2 {1} {2} 1 = 18 := by decide
example : Pnq.minB 2 5 {1} {2} 1 = 30 := by decide
example : Pnq.minB 2 5 ∅ {2} 1 = 15 := by decide
example : (3 : ℕ) * 2 ^ ({1, 2} : Finset ℕ).card = 12 := by decide

-- (3) what fixes Mathlib's cyclotomic polynomials
#check @Polynomial.prod_cyclotomic_eq_X_pow_sub_one   -- the product over the divisors of n is X^n - 1
#check @Polynomial.cyclotomic.monic
#check @Polynomial.natDegree_cyclotomic               -- degree = totient
#check @Polynomial.cyclotomic_prime                   -- Φ_p = 1 + X + ... + X^(p-1)
