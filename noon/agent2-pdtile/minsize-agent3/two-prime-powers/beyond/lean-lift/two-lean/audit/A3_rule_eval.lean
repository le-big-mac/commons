import Pnq.Rule
/-! Audit: the values Lean computes for the right-hand sides of the three least-size statements: `minU p q Es Fs`,
`q * p ^ Es.card`, `minB p q Es Fs a0`, for every `Es, Fs ⊆ {1..n}` and every `a0` in `1..n`.  (Which `a0` satisfy the
hypotheses of the third statement is decided by the program that reads this output.)  The values do not depend on `s`. -/
open Pnq
/-- the subset of `1..n` whose members are the `ℓ` with bit `ℓ - 1` of `m` set -/
def auditLev (n m : ℕ) : Finset ℕ := (Finset.Icc 1 n).filter (fun ℓ => m.testBit (ℓ - 1))
/-- the members of a set of levels, listed by asking membership -/
def auditShow (n : ℕ) (S : Finset ℕ) : List ℕ := (List.range (n + 3)).filter (fun ℓ => decide (ℓ ∈ S))
def auditRun (p q n : ℕ) : IO Unit := do
  for mE in List.range (2 ^ n) do
    let Es := auditLev n mE
    IO.println s!"A {p} {q} {n} {auditShow n Es} {q * p ^ Es.card}"
    for mF in List.range (2 ^ n) do
      let Fs := auditLev n mF
      IO.println s!"U {p} {q} {n} {auditShow n Es} {auditShow n Fs} {minU p q Es Fs}"
      for a0 in List.range (n + 1) do
        if 1 ≤ a0 then
          IO.println s!"B {p} {q} {n} {auditShow n Es} {auditShow n Fs} {a0} {minB p q Es Fs a0}"
#eval do
  for (p, q) in [(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2), (3, 7), (7, 3), (5, 7), (7, 5)] do
    for n in [0, 1, 2, 3] do
      auditRun p q n
