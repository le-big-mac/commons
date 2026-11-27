import Pnq.SignFinal

/-! Tests of the definitions of `Pnq/SignDefs.lean` on small data.  The expected values, in the comments, were worked
out outside Lean (by hand and by exact integer arithmetic in Python: divisibility by the cyclotomic polynomial by long
division).  `P`, `BadAt`, `badSet` cannot be evaluated (polynomials over `ℤ` are not computable in Mathlib), so the
numbers of bad signings are computed here by a computable criterion that is NOT the definition (`badC` below); the
definition itself is tested only by the three `example`s at the end. -/

open Pnq

/-! ### `μ` -/

#eval [3, 5, 9, 15, 45, 7, 21, 27, 105, 11025].map μ   -- expected [2, 4, 4, 4, 4, 6, 6, 6, 6, 12]
#eval [0, 1].map μ                                      -- expected [0, 0]

/-! ### `live` and `rank` -/

def e5 : Fin 5 → ℕ := ![0, 1, 2, 3, 6]
def e7 : Fin 7 → ℕ := ![0, 1, 2, 3, 6, 9, 18]
def e15 : Fin 7 → ℕ := ![0, 3, 5, 6, 9, 10, 12]
def e6 : Fin 6 → ℕ := ![0, 1, 2, 3, 4, 5]
def e9 : Fin 6 → ℕ := ![0, 0, 1, 1, 2, 2]

#eval [0, 1, 2, 3].map (live e5 3)      -- expected [false, true, true, false]
#eval [0, 1, 2, 3].map (rank e5 3)      -- expected [0, 1, 2, 2]
#eval [1, 2, 3, 4].map (live e7 3)      -- expected [true, true, true, false]
#eval [0, 1, 2, 3, 4].map (rank e7 3)   -- expected [0, 1, 2, 3, 3]
#eval [1, 2].map (live e15 3)           -- expected [true, true]
#eval [1, 2].map (live e15 5)           -- expected [true, false]
#eval [1, 2].map (rank e15 3)           -- expected [1, 2]
#eval [1, 2].map (rank e15 5)           -- expected [1, 1]
#eval [1, 2].map (live e6 3)            -- expected [true, false]
#eval [1, 2].map (live e6 5)            -- expected [true, false]
#eval [1, 2].map (live e9 3)            -- expected [true, false]
#eval [1, 2].map (live e5 2)            -- expected [true, true]   (classes 0, 1 modulo 2; 0, 2 modulo 4)

/-! ### the left side of N1 -/

#eval [3, 5, 6, 14].map fun m => lhsN1 m {3}
-- expected [1/4, 1/4, 9/16, 813/2048]
#eval [3, 5, 6, 14].map fun m => lhsN1 m {3, 5, 9, 15, 45}
-- expected [1/2, 1/2, 13/16, 1325/2048]
#eval [1, 2, 4, 12, 14].map fun m => lhsN1 m ∅
-- expected [0, 1/2, 3/8, 231/1024, 429/2048]

/-! ### the numbers of bad signings, by a computable criterion

`Φ_d ∣ F` exactly when `X^d - 1` divides `F * ∏_{q ∣ d prime} (X^(d/q) - 1)`: fold the coefficients of `F` modulo
`X^d - 1`, multiply by the factors `X^(d/q) - 1` modulo `X^d - 1`, and test for `0`.  The signings of `Fin m` are
listed by the bits of the numbers below `2^m`. -/

/-- the coefficients of `P e ε` folded modulo `X^d - 1` -/
def foldC {m : ℕ} (e : Fin m → ℕ) (ε : Fin m → Bool) (d : ℕ) : List ℤ :=
  (List.range d).map fun r => ∑ k, if e k % d = r then sg (ε k) else 0

/-- multiplication by `X^s - 1` modulo `X^d - 1` -/
def mulC (d s : ℕ) (a : List ℤ) : List ℤ :=
  (List.range d).map fun r => a.getD ((r + d - s % d) % d) 0 - a.getD r 0

/-- the criterion -/
def badC {m : ℕ} (e : Fin m → ℕ) (ε : Fin m → Bool) (d : ℕ) : Bool :=
  (d.primeFactorsList.dedup.foldl (fun a q => mulC d (d / q) a) (foldC e ε d)).all fun z => z == 0

/-- the number of signings for which the criterion holds at `d` -/
def countC {m : ℕ} (e : Fin m → ℕ) (d : ℕ) : ℕ :=
  (List.range (2 ^ m)).countP fun j => badC e (fun k => j.testBit k) d

#eval [1, 3, 9].map (countC e5)          -- expected [0, 6, 0]
#eval [1, 3, 9, 27].map (countC e7)      -- expected [0, 20, 0, 0]
#eval [1, 3, 5, 15].map (countC e15)     -- expected [0, 20, 6, 0]
#eval [1, 3, 5, 15].map (countC e6)      -- expected [20, 10, 0, 0]
#eval [1, 3, 9].map (countC e9)          -- expected [20, 10, 8]

/-! ### the definition itself, on three cases; and S4 as stated (still `sorry`) on one -/

open Polynomial in
example : BadAt ![0, 1, 2] (fun _ => true) 3 := by
  refine ⟨1, ?_⟩
  simp [P, sg, Fin.sum_univ_three, cyclotomic_three]
  ring

open Polynomial in
example : BadAt ![0, 1] ![true, false] 1 := by
  refine ⟨-1, ?_⟩
  simp [P, sg, Fin.sum_univ_two, cyclotomic_one]
  ring

open Polynomial in
example : ¬ BadAt ![0, 1] ![true, true] 1 := by
  intro h
  have h1 : (P ![0, 1] ![true, true]).IsRoot 1 := by
    rw [BadAt, cyclotomic_one] at h
    exact (dvd_iff_isRoot (p := P ![0, 1] ![true, true]) (a := 1)).1 (by simpa using h)
  simp [P, sg, Fin.sum_univ_two, IsRoot] at h1

/-- from the statement S4 (`card_badSet_one`, not yet proved): two of the four signings of two elements are bad
at `1` -/
example : (badSet ![0, 1] 1).card = 2 := by
  rw [Pnq.card_badSet_one]
  simp

/-! ### the unfolding lemmas are proved -/

#print axioms Pnq.mem_badSet   -- expected: no `sorryAx`
#print axioms Pnq.live_iff     -- expected: no `sorryAx`
