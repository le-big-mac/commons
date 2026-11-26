import Pnq.Upset
/-!
Audit file 6: evaluate `corners` and (the bounded form of) `IsUpSet` on every subset of a universe, for several M.
One line per subset:   M|members of D|is up-set|members of corners M D|sum of M / c over the corners
The bounded form is the text of `IsUpSet` with `∀ e, … → e ∣ M → …` replaced by `∀ e ∈ M.divisors, …`;
`Audit.isUpSet_iff_B` in A5_facts.lean proves the two equivalent for M ≠ 0.
-/
open Pnq.Upset

def bform (M : ℕ) (D : Finset ℕ) : Bool :=
  decide ((∀ d ∈ D, d ∣ M ∧ d ≠ 1) ∧ ∀ d ∈ D, ∀ e ∈ M.divisors, d ∣ e → e ∈ D)

def members (B : ℕ) (s : Finset ℕ) : List ℕ := (List.range B).filter (· ∈ s)

def rowsFor (M : ℕ) (U : List ℕ) : List String :=
  U.sublists.map fun S =>
    let D := S.toFinset
    let cs := corners M D
    s!"{M}|{members (M + 8) D}|{bform M D}|{members (M + 8) cs}|{∑ c ∈ cs, M / c}"

def divs (M : ℕ) : List ℕ := (List.range (M + 1)).filter (fun d => d ≠ 0 ∧ M % d = 0)

def run (M : ℕ) (U : List ℕ) : IO Unit := do
  for r in rowsFor M U do IO.println r

-- every subset of the divisors
#eval run 1 (divs 1)
#eval run 5 (divs 5)
#eval run 8 (divs 8)
#eval run 27 (divs 27)
#eval run 12 (divs 12)
#eval run 18 (divs 18)
#eval run 36 (divs 36)
#eval run 100 (divs 100)
#eval run 72 (divs 72)
#eval run 108 (divs 108)
#eval run 144 (divs 144)
-- every subset of {0, …, M + 2}: non-divisors, 0 and 1 included
#eval run 1 (List.range 4)
#eval run 5 (List.range 8)
#eval run 8 (List.range 11)
#eval run 12 (List.range 15)
