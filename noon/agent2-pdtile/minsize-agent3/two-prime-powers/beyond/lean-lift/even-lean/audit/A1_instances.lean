import Pnq.EvenFinal
/-! Audit: the statements that contain a filtered set, printed with every instance (`pp.all`), and the universe
levels of all fourteen. -/
open Pnq
set_option pp.all true in
#check @Pnq.card_exists_levelBad_le
set_option pp.all true in
#check @Pnq.card_exists_bad3_le
set_option pp.all true in
#print Pnq.bad3Set
set_option pp.all true in
#print Pnq.ExceptionalPair
set_option pp.universes true in
#check @Pnq.exists_not_bad3
set_option pp.universes true in
#check @Pnq.exists_not_badAt_of_three_le
set_option pp.universes true in
#check @Pnq.card_exists_levelBad_le
set_option pp.universes true in
#check @Pnq.card_exists_bad3_le
-- A′ and T at the types the later statements need
example (n : ℕ) [NeZero n] (w : ZMod n → ℕ) := @Pnq.exists_not_bad3 n
example (n : ℕ) [NeZero n] (w : ZMod n → ℕ) (hn : ¬ 3 ∣ n) (h : 3 ≤ Fintype.card (Σ x : ZMod n, Fin (w x))) :=
  Pnq.exists_not_bad3 n hn (ι := Σ x : ZMod n, Fin (w x)) h (fun k => k.1.val)
example {ι : Type 5} [Fintype ι] (e : ι → ℕ) (d K : ℕ) :=
  Pnq.card_exists_levelBad_le e (fun k => fun η : {η : F3 // IsPrimitiveRoot η d} => η.1 ^ e k) K
#print axioms Pnq.mem_bad3Set
#print axioms Pnq.val3_eq_aeval
#print axioms Pnq.val3_eq_eval₂
#print axioms Pnq.val3_eq_eval_map
#print axioms Pnq.levelBad_zero
#print axioms Pnq.levelBad_succ
#print axioms Pnq.card_exists_levelBad_le
#print axioms Pnq.exists_signs_all
