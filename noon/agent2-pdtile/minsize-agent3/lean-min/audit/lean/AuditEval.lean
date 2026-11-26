import Pnq.Rule

/-
Audit scratch: Lean's own values of `Pnq.minU`, `q * p ^ Es.card`, `Pnq.minB` (with `Pnq.xOf`, `Pnq.gOf`)
for every pattern of a list of triples (p, q, n), one line per pattern:

  p q n bal emask fmask kind a0 kprime x value ok

`emask`, `fmask`: bit (ℓ-1) set iff level ℓ is in Es, Fs.  `bal` = 1 iff Φ_q ∣ A.
kind 0: `minsize_unbalanced_zmod` applies, value `minU p q Es Fs`.
kind 1: `minsize_balanced_all_zmod` applies (Fs = Icc 1 n), value `q * p ^ Es.card`.
kind 2: `minsize_balanced_zmod` applies with `a0` = the first level of 1..n not in Fs (found here by search),
        value `minB p q Es Fs a0`; `kprime` = `(gOf Es Fs a0).card`, `x` = `xOf p Es Fs a0`.
`ok` = 1 iff the hypotheses of that theorem on Es, Fs, a0 are decided true by Lean.
-/

open Pnq

def setOfMask (n m : ℕ) : Finset ℕ := (Finset.Icc 1 n).filter (fun ℓ => Nat.testBit m (ℓ - 1))

def a0Of (n : ℕ) (Fs : Finset ℕ) : Option ℕ :=
  ((List.range n).map (· + 1)).find? (fun ℓ => decide (ℓ ∉ Fs))

/-- the hypotheses of `minsize_balanced_zmod` on `a0`: `1 ≤ a0`, `a0 ≤ n`, every `ℓ` with `1 ≤ ℓ < a0` is in
`Fs` (as `a0 ≤ n`, those `ℓ` are among `1..n`), and `a0 ∉ Fs` -/
def hypOK (n : ℕ) (Fs : Finset ℕ) (a0 : ℕ) : Bool :=
  decide (1 ≤ a0) && decide (a0 ≤ n) &&
    ((List.range n).map (· + 1)).all (fun ℓ => decide (a0 ≤ ℓ) || decide (ℓ ∈ Fs)) && decide (a0 ∉ Fs)

/-- the number of `a0` in `0..n+1` that satisfy the hypotheses of the third theorem -/
def countA0 (n : ℕ) (Fs : Finset ℕ) : ℕ :=
  ((List.range (n + 2)).filter (fun a => hypOK n Fs a)).length

def b2n (b : Bool) : ℕ := if b then 1 else 0

def line (p q n : ℕ) (bal : Bool) (em fm : ℕ) : String :=
  let Es := setOfMask n em
  let Fs := setOfMask n fm
  let sub := decide (Es ⊆ Finset.Icc 1 n ∧ Fs ⊆ Finset.Icc 1 n)
  let pre := s!"{p} {q} {n} {b2n bal} {em} {fm}"
  if !bal then s!"{pre} 0 0 0 0 {minU p q Es Fs} {b2n sub}"
  else if Fs = Finset.Icc 1 n then s!"{pre} 1 0 0 0 {q * p ^ Es.card} {b2n (sub && countA0 n Fs == 0)}"
  else match a0Of n Fs with
    | some a0 =>
      s!"{pre} 2 {a0} {(gOf Es Fs a0).card} {xOf p Es Fs a0} {minB p q Es Fs a0} {b2n (sub && hypOK n Fs a0 && countA0 n Fs == 1)}"
    | none => s!"{pre} 3 0 0 0 0 0"

def dump (p q n : ℕ) : IO Unit := do
  for bal in [false, true] do
    for em in List.range (2 ^ n) do
      for fm in List.range (2 ^ n) do
        IO.println (line p q n bal em fm)

def primes : List ℕ := [2, 3, 5, 7, 11]

#eval show IO Unit from do
  for p in primes do
    for q in primes do
      if p ≠ q then
        for n in List.range 6 do
          dump p q n
  -- n = 6 for the pairs among 2, 3, 5
  for p in [2, 3, 5] do
    for q in [2, 3, 5] do
      if p ≠ q then dump p q 6
