import Pnq.Lift
open Pnq.Lift
-- reduction of the multiset {0, 3, 3, 5} of Z_6 modulo 2 and modulo 3
instance : Fact (Nat.Prime 3) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 2) := ⟨by norm_num⟩
def w6 : ZMod 6 → ℕ := fun y => if y = 0 then 1 else if y = 3 then 2 else if y = 5 then 1 else 0
#eval (List.range 2).map fun i => reduce (N := 2) (r := 3) w6 (i : ZMod 2)
#eval (List.range 3).map fun i => reduce (N := 3) (r := 2) w6 (i : ZMod 3)
