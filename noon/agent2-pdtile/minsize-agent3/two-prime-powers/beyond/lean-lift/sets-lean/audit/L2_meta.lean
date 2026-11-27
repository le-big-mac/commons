import Pnq.SetAll
/-! Audit: for each of the five statements, the constants its type uses (with the module each comes from) and every instance
argument given to `Pnq.maskW`, `Pnq.indW`, `Finset.univ` (the `Fintype` behind every sum), `Finset.filter` (its decidability
argument), `Finset.card`, `ZMod.castHom`.  Then the instances Lean finds for the `NeZero` goals, and a structural hash of each type
(to be compared with the same file run where the proofs are filled in). -/
open Lean Meta Elab Command

def auditNames : List Name := [``Pnq.Lift.exists_set_lift, ``Pnq.Lift.set_sizes_iff_mul, ``Pnq.Lift.minsize_unbalanced_set,
  ``Pnq.Lift.minsize_balanced_all_set, ``Pnq.Lift.minsize_balanced_set]

partial def collectApps (e : Expr) (acc : IO.Ref (Array String)) : MetaM Unit := do
  let rec go (e : Expr) : MetaM Unit := do
    match e with
    | .forallE n t b bi =>
        go t
        withLocalDecl n bi t fun x => go (b.instantiate1 x)
    | .lam n t b bi =>
        go t
        withLocalDecl n bi t fun x => go (b.instantiate1 x)
    | .letE n t v b _ =>
        go t; go v
        withLetDecl n t v fun x => go (b.instantiate1 x)
    | .mdata _ b => go b
    | .proj _ _ b => go b
    | .app .. =>
        let f := e.getAppFn
        let args := e.getAppArgs
        if let .const c _ := f then
          let k : Option Nat :=
            if c == ``Pnq.maskW then some 2          -- M, NeZero
            else if c == ``Pnq.indW then some 1      -- M
            else if c == ``Finset.univ then some args.size
            else if c == ``Finset.filter then some 3 -- α, p, DecidablePred
            else if c == ``ZMod.castHom then some 6  -- n m h R Ring CharP
            else if c == ``Finset.card then some 1
            else if c == ``IsLeast then some 2
            else none
          if let some k := k then
            let hd := mkAppN f (args.extract 0 (min k args.size))
            let s ← withOptions (fun o => (o.setBool `pp.explicit true).setBool `pp.proofs true |>.setBool `pp.fullNames true) do
              let fmt ← ppExpr hd
              pure (toString fmt)
            acc.modify fun a => if a.contains s then a else a.push s
        go f
        for a in args do go a
    | _ => pure ()
  go e

run_cmd liftTermElabM do
  let env ← getEnv
  for nm in auditNames do
    let some ci := env.find? nm | throwError "missing {nm}"
    IO.println s!"=== {nm}"
    IO.println s!"kind: {if ci.isTheorem then "theorem" else "other"}; universe params: {ci.levelParams}"
    let consts := ci.type.getUsedConstants
    let mut byMod : Std.HashMap Name (Array Name) := {}
    for c in consts do
      let m := match env.getModuleIdxFor? c with
        | some i => env.header.moduleNames[i.toNat]!
        | none => `«(this file)»
      byMod := byMod.insert m ((byMod.getD m #[]).push c)
    let mods := byMod.toArray.qsort (fun a b => a.1.toString < b.1.toString)
    for (m, cs) in mods do
      IO.println s!"  {m}: {cs.qsort (fun a b => a.toString < b.toString)}"
    let acc ← IO.mkRef (#[] : Array String)
    collectApps ci.type acc
    IO.println "  instance arguments:"
    for s in (← acc.get) do
      IO.println s!"    {s.replace "\n" " "}"
    let s ← withOptions (fun o => ((o.setBool `pp.explicit true).setBool `pp.proofs true).setBool `pp.fullNames true) do
      pure (toString (← ppExpr ci.type))
    IO.println s!"  type hash {ci.type.hash}, explicit print {s.length} characters"
  for nm in [``Pnq.maskW, ``Pnq.indW, ``Pnq.minU, ``Pnq.minB, ``Pnq.xOf, ``Pnq.gOf] do
    let some ci := env.find? nm | throwError "missing {nm}"
    let vh := match ci with
      | .defnInfo d => s!" value hash {d.value.hash}"
      | _ => ""
    IO.println s!"{nm}: type hash {ci.type.hash}{vh}"

section
variable (p q n s N r j : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] [NeZero s] [NeZero N]
set_option pp.explicit true in
#synth NeZero (N * r ^ j)
set_option pp.explicit true in
#synth NeZero (p ^ n * q * s)
set_option pp.explicit true in
#synth NeZero (p ^ n * q)
end
#print instNeZeroNatHMul
#print Nat.instNeZeroHPow
#check @NeZero.of_gt'
#check @Nat.Prime.one_lt'
#print Pnq.instNeZeroNatHMulHPow_pnq
#print NeZero
#print Fact
#print IsLeast
#print lowerBounds
