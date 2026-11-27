import Pnq.Lift
open Pnq.Lift
/-! Audit: `reduce` for r = 2 (the instance `Fact (Nat.Prime 2)` is whatever Lean finds, as in the statements). -/
set_option pp.explicit true in
#synth Fact (Nat.Prime 2)
def aw0 : ZMod 2 → ℕ := fun y => ([0, 1] : List ℕ).getD y.val 0
#eval ("case 0", (List.range 1).map fun i => reduce (N := 1) (r := 2) aw0 (i : ZMod 1))
def aw1 : ZMod 2 → ℕ := fun y => ([1, 2] : List ℕ).getD y.val 0
#eval ("case 1", (List.range 1).map fun i => reduce (N := 1) (r := 2) aw1 (i : ZMod 1))
def aw2 : ZMod 2 → ℕ := fun y => ([0, 3] : List ℕ).getD y.val 0
#eval ("case 2", (List.range 1).map fun i => reduce (N := 1) (r := 2) aw2 (i : ZMod 1))
def aw3 : ZMod 2 → ℕ := fun y => ([0, 0] : List ℕ).getD y.val 0
#eval ("case 3", (List.range 1).map fun i => reduce (N := 1) (r := 2) aw3 (i : ZMod 1))
def aw4 : ZMod 4 → ℕ := fun y => ([0, 1, 0, 0] : List ℕ).getD y.val 0
#eval ("case 4", (List.range 2).map fun i => reduce (N := 2) (r := 2) aw4 (i : ZMod 2))
def aw5 : ZMod 4 → ℕ := fun y => ([1, 2, 3, 4] : List ℕ).getD y.val 0
#eval ("case 5", (List.range 2).map fun i => reduce (N := 2) (r := 2) aw5 (i : ZMod 2))
def aw6 : ZMod 4 → ℕ := fun y => ([0, 3, 0, 0] : List ℕ).getD y.val 0
#eval ("case 6", (List.range 2).map fun i => reduce (N := 2) (r := 2) aw6 (i : ZMod 2))
def aw7 : ZMod 4 → ℕ := fun y => ([3, 1, 0, 3] : List ℕ).getD y.val 0
#eval ("case 7", (List.range 2).map fun i => reduce (N := 2) (r := 2) aw7 (i : ZMod 2))
def aw8 : ZMod 6 → ℕ := fun y => ([0, 0, 1, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 8", (List.range 3).map fun i => reduce (N := 3) (r := 2) aw8 (i : ZMod 3))
def aw9 : ZMod 6 → ℕ := fun y => ([1, 2, 3, 4, 5, 6] : List ℕ).getD y.val 0
#eval ("case 9", (List.range 3).map fun i => reduce (N := 3) (r := 2) aw9 (i : ZMod 3))
def aw10 : ZMod 6 → ℕ := fun y => ([1, 1, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 10", (List.range 3).map fun i => reduce (N := 3) (r := 2) aw10 (i : ZMod 3))
def aw11 : ZMod 6 → ℕ := fun y => ([0, 3, 0, 2, 1, 1] : List ℕ).getD y.val 0
#eval ("case 11", (List.range 3).map fun i => reduce (N := 3) (r := 2) aw11 (i : ZMod 3))
def aw12 : ZMod 8 → ℕ := fun y => ([0, 0, 0, 1, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 12", (List.range 4).map fun i => reduce (N := 4) (r := 2) aw12 (i : ZMod 4))
def aw13 : ZMod 8 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8] : List ℕ).getD y.val 0
#eval ("case 13", (List.range 4).map fun i => reduce (N := 4) (r := 2) aw13 (i : ZMod 4))
def aw14 : ZMod 8 → ℕ := fun y => ([0, 3, 3, 1, 0, 0, 1, 2] : List ℕ).getD y.val 0
#eval ("case 14", (List.range 4).map fun i => reduce (N := 4) (r := 2) aw14 (i : ZMod 4))
def aw15 : ZMod 8 → ℕ := fun y => ([3, 1, 0, 0, 1, 0, 3, 3] : List ℕ).getD y.val 0
#eval ("case 15", (List.range 4).map fun i => reduce (N := 4) (r := 2) aw15 (i : ZMod 4))
def aw16 : ZMod 10 → ℕ := fun y => ([0, 0, 0, 0, 0, 0, 1, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 16", (List.range 5).map fun i => reduce (N := 5) (r := 2) aw16 (i : ZMod 5))
def aw17 : ZMod 10 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10] : List ℕ).getD y.val 0
#eval ("case 17", (List.range 5).map fun i => reduce (N := 5) (r := 2) aw17 (i : ZMod 5))
def aw18 : ZMod 10 → ℕ := fun y => ([0, 2, 0, 3, 1, 0, 0, 1, 1, 2] : List ℕ).getD y.val 0
#eval ("case 18", (List.range 5).map fun i => reduce (N := 5) (r := 2) aw18 (i : ZMod 5))
def aw19 : ZMod 10 → ℕ := fun y => ([1, 0, 2, 1, 3, 2, 2, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 19", (List.range 5).map fun i => reduce (N := 5) (r := 2) aw19 (i : ZMod 5))
def aw20 : ZMod 12 → ℕ := fun y => ([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 20", (List.range 6).map fun i => reduce (N := 6) (r := 2) aw20 (i : ZMod 6))
def aw21 : ZMod 12 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] : List ℕ).getD y.val 0
#eval ("case 21", (List.range 6).map fun i => reduce (N := 6) (r := 2) aw21 (i : ZMod 6))
def aw22 : ZMod 12 → ℕ := fun y => ([3, 1, 1, 0, 3, 0, 0, 0, 0, 3, 3, 0] : List ℕ).getD y.val 0
#eval ("case 22", (List.range 6).map fun i => reduce (N := 6) (r := 2) aw22 (i : ZMod 6))
def aw23 : ZMod 12 → ℕ := fun y => ([0, 0, 0, 0, 0, 3, 0, 2, 1, 3, 1, 1] : List ℕ).getD y.val 0
#eval ("case 23", (List.range 6).map fun i => reduce (N := 6) (r := 2) aw23 (i : ZMod 6))
def aw24 : ZMod 14 → ℕ := fun y => ([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 24", (List.range 7).map fun i => reduce (N := 7) (r := 2) aw24 (i : ZMod 7))
def aw25 : ZMod 14 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] : List ℕ).getD y.val 0
#eval ("case 25", (List.range 7).map fun i => reduce (N := 7) (r := 2) aw25 (i : ZMod 7))
def aw26 : ZMod 14 → ℕ := fun y => ([0, 2, 0, 1, 0, 2, 0, 3, 1, 0, 0, 2, 1, 0] : List ℕ).getD y.val 0
#eval ("case 26", (List.range 7).map fun i => reduce (N := 7) (r := 2) aw26 (i : ZMod 7))
def aw27 : ZMod 14 → ℕ := fun y => ([1, 1, 1, 2, 3, 3, 1, 0, 3, 2, 1, 3, 0, 0] : List ℕ).getD y.val 0
#eval ("case 27", (List.range 7).map fun i => reduce (N := 7) (r := 2) aw27 (i : ZMod 7))
def aw28 : ZMod 18 → ℕ := fun y => ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0] : List ℕ).getD y.val 0
#eval ("case 28", (List.range 9).map fun i => reduce (N := 9) (r := 2) aw28 (i : ZMod 9))
def aw29 : ZMod 18 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] : List ℕ).getD y.val 0
#eval ("case 29", (List.range 9).map fun i => reduce (N := 9) (r := 2) aw29 (i : ZMod 9))
def aw30 : ZMod 18 → ℕ := fun y => ([0, 0, 3, 2, 0, 0, 3, 1, 1, 1, 1, 2, 1, 0, 1, 0, 3, 2] : List ℕ).getD y.val 0
#eval ("case 30", (List.range 9).map fun i => reduce (N := 9) (r := 2) aw30 (i : ZMod 9))
def aw31 : ZMod 18 → ℕ := fun y => ([1, 0, 2, 2, 3, 0, 0, 3, 0, 2, 0, 0, 2, 1, 2, 1, 1, 1] : List ℕ).getD y.val 0
#eval ("case 31", (List.range 9).map fun i => reduce (N := 9) (r := 2) aw31 (i : ZMod 9))
def aw32 : ZMod 20 → ℕ := fun y => ([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 32", (List.range 10).map fun i => reduce (N := 10) (r := 2) aw32 (i : ZMod 10))
def aw33 : ZMod 20 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] : List ℕ).getD y.val 0
#eval ("case 33", (List.range 10).map fun i => reduce (N := 10) (r := 2) aw33 (i : ZMod 10))
def aw34 : ZMod 20 → ℕ := fun y => ([0, 0, 0, 1, 2, 1, 1, 2, 0, 0, 2, 1, 0, 1, 1, 3, 2, 0, 0, 1] : List ℕ).getD y.val 0
#eval ("case 34", (List.range 10).map fun i => reduce (N := 10) (r := 2) aw34 (i : ZMod 10))
def aw35 : ZMod 20 → ℕ := fun y => ([0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 1, 3, 0, 1, 2, 0, 0, 3, 1, 2] : List ℕ).getD y.val 0
#eval ("case 35", (List.range 10).map fun i => reduce (N := 10) (r := 2) aw35 (i : ZMod 10))
def aw36 : ZMod 24 → ℕ := fun y => ([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 36", (List.range 12).map fun i => reduce (N := 12) (r := 2) aw36 (i : ZMod 12))
def aw37 : ZMod 24 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] : List ℕ).getD y.val 0
#eval ("case 37", (List.range 12).map fun i => reduce (N := 12) (r := 2) aw37 (i : ZMod 12))
def aw38 : ZMod 24 → ℕ := fun y => ([2, 1, 3, 3, 0, 2, 1, 3, 3, 1, 0, 1, 1, 1, 0, 1, 1, 3, 1, 1, 1, 3, 0, 0] : List ℕ).getD y.val 0
#eval ("case 38", (List.range 12).map fun i => reduce (N := 12) (r := 2) aw38 (i : ZMod 12))
def aw39 : ZMod 24 → ℕ := fun y => ([1, 0, 0, 1, 1, 3, 1, 2, 1, 0, 1, 0, 1, 0, 0, 2, 0, 1, 3, 0, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 39", (List.range 12).map fun i => reduce (N := 12) (r := 2) aw39 (i : ZMod 12))
def aw40 : ZMod 30 → ℕ := fun y => ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 40", (List.range 15).map fun i => reduce (N := 15) (r := 2) aw40 (i : ZMod 15))
def aw41 : ZMod 30 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30] : List ℕ).getD y.val 0
#eval ("case 41", (List.range 15).map fun i => reduce (N := 15) (r := 2) aw41 (i : ZMod 15))
def aw42 : ZMod 30 → ℕ := fun y => ([3, 1, 2, 2, 0, 0, 3, 1, 3, 0, 0, 0, 0, 0, 2, 1, 1, 0, 1, 0, 0, 2, 1, 2, 2, 1, 0, 0, 1, 1] : List ℕ).getD y.val 0
#eval ("case 42", (List.range 15).map fun i => reduce (N := 15) (r := 2) aw42 (i : ZMod 15))
def aw43 : ZMod 30 → ℕ := fun y => ([1, 2, 1, 2, 1, 1, 1, 0, 0, 0, 0, 2, 1, 0, 0, 3, 3, 1, 0, 2, 0, 0, 1, 0, 2, 0, 0, 3, 0, 0] : List ℕ).getD y.val 0
#eval ("case 43", (List.range 15).map fun i => reduce (N := 15) (r := 2) aw43 (i : ZMod 15))
def aw44 : ZMod 36 → ℕ := fun y => ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] : List ℕ).getD y.val 0
#eval ("case 44", (List.range 18).map fun i => reduce (N := 18) (r := 2) aw44 (i : ZMod 18))
def aw45 : ZMod 36 → ℕ := fun y => ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36] : List ℕ).getD y.val 0
#eval ("case 45", (List.range 18).map fun i => reduce (N := 18) (r := 2) aw45 (i : ZMod 18))
def aw46 : ZMod 36 → ℕ := fun y => ([0, 0, 2, 0, 3, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 2, 0, 1, 2, 3, 1, 3, 2, 0, 2, 3, 2, 0, 3, 2, 0, 3, 2] : List ℕ).getD y.val 0
#eval ("case 46", (List.range 18).map fun i => reduce (N := 18) (r := 2) aw46 (i : ZMod 18))
def aw47 : ZMod 36 → ℕ := fun y => ([2, 1, 2, 1, 0, 3, 1, 0, 0, 0, 3, 0, 3, 0, 0, 0, 2, 1, 1, 0, 1, 0, 2, 1, 0, 0, 2, 3, 0, 0, 1, 1, 0, 0, 0, 1] : List ℕ).getD y.val 0
#eval ("case 47", (List.range 18).map fun i => reduce (N := 18) (r := 2) aw47 (i : ZMod 18))
