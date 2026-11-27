import Pnq.EvenFinal
/-! Audit: (1) a fingerprint of the eight definitions and the fourteen statements as elaborated in the skeleton
(structural hash of the type, the number of characters of its fully explicit print, and for a definition the hash of
its value), to be compared with the same file run in a project where the proofs are filled in; the definitions and
finished statements they rest on are printed too;
(2) the new final statement contains this morning's `exists_signs_odd` (for odd `n` nothing is an exceptional pair). -/
open Lean Meta Elab Command

def auditNamesEven : List Name := [``Pnq.F3, ``Pnq.val3, ``Pnq.Bad3, ``Pnq.bad3Set, ``Pnq.classSum3, ``Pnq.csum,
  ``Pnq.levelBad, ``Pnq.ExceptionalPair,
  ``Pnq.card_exists_levelBad_le, ``Pnq.bad3_of_badAt, ``Pnq.classSum3_eq_of_bad3, ``Pnq.bad3_of_not_live,
  ``Pnq.card_bad3Set_mul_two_pow_card_le, ``Pnq.card_bad3Set_mul_two_pow_rank_le, ``Pnq.bad3_one_iff,
  ``Pnq.card_bad3Set_one, ``Pnq.card_exists_bad3_le, ``Pnq.sum_half_pow_mu_lt, ``Pnq.exists_not_bad3,
  ``Pnq.exists_not_badAt_of_three_le, ``Pnq.exists_signs_all, ``Pnq.not_exists_signs_of_exceptionalPair,
  ``Pnq.mem_bad3Set, ``Pnq.val3_eq_aeval, ``Pnq.val3_eq_eval₂, ``Pnq.val3_eq_eval_map, ``Pnq.levelBad_zero,
  ``Pnq.levelBad_succ,
  ``Pnq.sg, ``Pnq.P, ``Pnq.BadAt, ``Pnq.live, ``Pnq.rank, ``Pnq.IsPivot, ``Pnq.μ, ``Pnq.maskW,
  ``Pnq.exists_signs_odd, ``Pnq.exists_isPivot, ``Pnq.rank_lt_card]

run_cmd liftTermElabM do
  let env ← getEnv
  for nm in auditNamesEven do
    let some ci := env.find? nm | throwError "missing {nm}"
    let s ← withOptions (fun o => ((o.setBool `pp.explicit true).setBool `pp.proofs true).setBool `pp.fullNames true) do
      pure (toString (← ppExpr ci.type))
    let vh := match ci with
      | .defnInfo d => s!" value hash {d.value.hash}"
      | _ => ""
    IO.println s!"{nm}: type hash {ci.type.hash}, explicit print {s.length} characters{vh}"

open Pnq in
/-- for odd `n` nothing is an exceptional pair -/
theorem auditNotExceptionalOfOdd (n : ℕ) [NeZero n] (hn : ¬ 2 ∣ n) (w : ZMod n → ℕ) : ¬ ExceptionalPair w := by
  rintro ⟨a, b, -, hev⟩
  apply hn
  have h1 : addOrderOf (a - b) ∣ n := by
    have h := addOrderOf_dvd_card (x := a - b)
    rwa [ZMod.card] at h
  exact (even_iff_two_dvd.mp hev).trans h1

open Pnq in
/-- this morning's statement for odd `n` is the case `¬ 2 ∣ n` of the new first final statement -/
theorem auditOddFromAll (n : ℕ) [NeZero n] (hn : ¬ 2 ∣ n) (w : ZMod n → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v :=
  exists_signs_all n w hw (auditNotExceptionalOfOdd n hn w)

example : type_of% @Pnq.exists_signs_odd := @auditOddFromAll
#print axioms auditNotExceptionalOfOdd
#print axioms auditOddFromAll
