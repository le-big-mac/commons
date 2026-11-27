import Pnq.Rule
/-! Values of `Pnq.minU`, `Pnq.minB` and of `q * p ^ Es.card`, by `#eval`, for every `Es, Fs ⊆ {1..n}` and every `a0` in `1..n`
(whether `a0` satisfies the hypotheses of the third theorem is decided by the reader of this output, not here). -/
open Pnq
/-- the subset of `1..n` with bit pattern `m` (bit `ℓ - 1` for the level `ℓ`) -/
def lev (n m : ℕ) : Finset ℕ := (Finset.Icc 1 n).filter (fun ℓ => m.testBit (ℓ - 1))
/-- its elements, listed by membership (so the listing does not depend on how it was built) -/
def show' (n : ℕ) (S : Finset ℕ) : List ℕ := (List.range (n + 3)).filter (fun ℓ => decide (ℓ ∈ S))
def run (p q n : ℕ) : IO Unit := do
  for mE in List.range (2 ^ n) do
    let Es := lev n mE
    IO.println s!"A {p} {q} {n} {show' n Es} {q * p ^ Es.card}"
    for mF in List.range (2 ^ n) do
      let Fs := lev n mF
      IO.println s!"U {p} {q} {n} {show' n Es} {show' n Fs} {minU p q Es Fs}"
      for a0 in List.range (n + 1) do
        if 1 ≤ a0 then
          IO.println s!"B {p} {q} {n} {show' n Es} {show' n Fs} {a0} {minB p q Es Fs a0}"
#eval do
  for (p, q) in [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2), (3, 7), (7, 3)] do
    for n in [0, 1, 2, 3] do
      run p q n
