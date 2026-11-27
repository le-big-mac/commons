import Pnq.SetAll
/-! Audit: the fibre counts of `exists_set_lift`, evaluated by Lean on concrete sets (to compare with "number of elements y of
the set with y mod N = x" computed outside Lean), and `indW` on a concrete set. -/
open Pnq
instance : Fact (Nat.Prime 3) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩
/-- the fibre counts exactly as written in `exists_set_lift` -/
def auditFib (N r j : ℕ) [NeZero N] (A : Finset (ZMod (N * r ^ j))) : List ℕ :=
  (List.range N).map fun i =>
    (A.filter (fun y => ZMod.castHom (Nat.dvd_mul_right N (r ^ j)) (ZMod N) y = (i : ZMod N))).card
def auditSet (M : ℕ) (l : List ℕ) : Finset (ZMod M) := (l.map (fun k => (k : ZMod M))).toFinset
#eval auditFib 6 3 1 (auditSet _ [0, 1, 2, 4, 10])
#eval auditFib 2 3 2 (auditSet _ [0, 1, 2, 4, 10])
#eval auditFib 6 3 2 (auditSet _ [0, 6, 12, 18, 25, 31, 53, 47, 5, 40, 41])
#eval auditFib 4 5 1 (auditSet _ [0, 4, 8, 12, 16, 1, 5, 19, 18, 3])
#eval auditFib 1 3 2 (auditSet _ [0, 4, 8])
#eval auditFib 3 3 2 (auditSet _ [26, 25, 24, 23, 0, 3, 9])
#eval (List.range 18).map fun i => indW (auditSet 18 [0, 1, 2, 4, 10]) (i : ZMod 18)
