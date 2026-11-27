import Pnq.LiftMin
/-! Referee's checks of the lifting files (read-only; nothing here is part of the library).
1. the statements as Lean prints them, and their axioms;
2. the paper's Lemma (lifting), in the paper's own form, derived from the three fixed statements only;
3. the plain page's example (36 hours, balance at 12 only, least number 5) as an instance of `minsize_unbalanced_lift`;
4. the remark on r = p: the value for "balanced, every level" at n equals `minB` at n + 1 with a0 = n + 1, on small cases. -/
open Pnq Pnq.Lift

#print Pnq.Lift.reduce
#check @Pnq.Lift.sum_reduce
#check @Pnq.Lift.cyclotomic_dvd_reduce_iff
#check @Pnq.Lift.exists_lift
#check @Pnq.Lift.sizes_eq
#check @Pnq.Lift.minsize_unbalanced_lift
#check @Pnq.Lift.minsize_balanced_all_lift
#check @Pnq.Lift.minsize_balanced_lift
#print axioms Pnq.Lift.sum_reduce
#print axioms Pnq.Lift.cyclotomic_dvd_reduce_iff
#print axioms Pnq.Lift.exists_lift
#print axioms Pnq.Lift.sizes_eq
#print axioms Pnq.Lift.minsize_unbalanced_lift
#print axioms Pnq.Lift.minsize_balanced_all_lift
#print axioms Pnq.Lift.minsize_balanced_lift

namespace Referee

/-- The paper's Lemma (lifting) as the paper words it: a lift with the same number of elements, whose reduction is the
multiset, and for every divisor d of N·r: Φ_d divides the lifted mask iff d ∣ N and Φ_d divides the mask. -/
theorem paper_lemma {N r : ℕ} [NeZero N] [Fact r.Prime] (hr : r ≠ 2) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * r) → ℕ, ∑ y, w' y = ∑ x, w x ∧ reduce w' = w ∧
      ∀ d, d ∣ N * r →
        (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∣ N ∧ Polynomial.cyclotomic d ℤ ∣ maskW w) := by
  obtain ⟨w', hred, hnew⟩ := exists_lift hr w hw
  subst hred
  refine ⟨w', (sum_reduce w').symm, rfl, fun d hd => ?_⟩
  constructor
  · intro h
    by_cases hdN : d ∣ N
    · exact ⟨hdN, (cyclotomic_dvd_reduce_iff w' d hdN).2 h⟩
    · exact absurd h (hnew d hd hdN)
  · rintro ⟨hdN, h⟩
    exact (cyclotomic_dvd_reduce_iff w' d hdN).1 h

#print axioms Referee.paper_lemma

/-- The plain page's example: on the clock of 36 = 2^2·3·3 hours, balance at 12 and at no other divisor > 1 of 36
(not at 3; not at 2, 4; not at 6; at 12; not at 9, 18, 36): the least number of marks is `minU 2 3 ∅ {2}`. -/
example :
    IsLeast {s | ∃ w : ZMod (2 ^ 2 * 3 * 3) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic 3 ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 2, Polynomial.cyclotomic (2 ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ (∅ : Finset ℕ)) ∧
        (∀ ℓ ∈ Finset.Icc 1 2, Polynomial.cyclotomic (2 ^ ℓ * 3) ℤ ∣ maskW w ↔ ℓ ∈ ({2} : Finset ℕ)) ∧
        ∀ d, d ∣ 2 ^ 2 * 3 * 3 → ¬ d ∣ 2 ^ 2 * 3 → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minU 2 3 ∅ {2}) :=
  minsize_unbalanced_lift 2 3 2 3 (by norm_num) (by norm_num) ∅ {2} (by simp) (by decide)

#eval minU 2 3 ∅ {2}
#eval (2 ^ 2 * 3 * 3 : ℕ)

-- r = p: "balanced, every level" at n against minB at n + 1 with a0 = n + 1, all Es ⊆ [1, n], n ≤ 4, a few (p, q)
#eval ([(3, 2), (3, 5), (5, 2), (5, 3), (7, 2), (2, 3)] : List (ℕ × ℕ)).all fun pq =>
  (List.range 5).all fun n =>
    (List.sublists (List.range' 1 n)).all fun L =>
      minB pq.1 pq.2 L.toFinset (Finset.Icc 1 n) (n + 1) == pq.2 * pq.1 ^ L.toFinset.card
-- and how many cases that was
#eval (6 * ((List.range 5).map fun n => (List.sublists (List.range' 1 n)).length).sum : ℕ)

end Referee
