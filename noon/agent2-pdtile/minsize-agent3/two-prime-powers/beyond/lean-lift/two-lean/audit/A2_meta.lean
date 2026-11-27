import Pnq.LiftAll
/-! Audit: for each of the eight statements, the constants its type uses (with the module each comes from) and every instance
argument given to `Pnq.maskW`, `Pnq.Lift.reduce`, `Finset.univ` (hence the `Fintype` behind every sum), `ZMod.val`. -/
open Lean Meta Elab Command

def auditNames : List Name := [``Pnq.Lift.exists_signs, ``Pnq.Lift.exists_lift_two, ``Pnq.Lift.sizes_eq_two,
  ``Pnq.Lift.sizes_eq_odd, ``Pnq.Lift.sizes_eq_mul, ``Pnq.Lift.minsize_unbalanced_mul,
  ``Pnq.Lift.minsize_balanced_all_mul, ``Pnq.Lift.minsize_balanced_mul]

/-- collect (with duplicates removed, as strings) the applications of the head constants of interest, inside binders -/
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
          if c == ``Pnq.maskW || c == ``Pnq.Lift.reduce || c == ``Finset.univ || c == ``ZMod.val then
            -- print head with the non-last arguments (types, instances), fully explicit and with proofs
            let k := if c == ``Finset.univ then args.size else args.size - 1
            let hd := mkAppN f (args.extract 0 k)
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

-- the instances Lean finds for the three kinds of goals named in the brief
section
variable (p q n s N a b : ℕ) [Fact p.Prime] [Fact q.Prime] [NeZero s] [NeZero N]
set_option pp.explicit true in
#synth NeZero (p ^ n * q * s)
set_option pp.explicit true in
#synth NeZero (p ^ n * q)
set_option pp.explicit true in
#synth NeZero (p ^ a * q ^ b)
set_option pp.explicit true in
#synth NeZero (N * 2)
set_option pp.explicit true in
#synth NeZero (N * s)
set_option pp.explicit true in
#synth Fact (Nat.Prime 2)
end
#print Pnq.Lift.instNeZeroMul
#print Pnq.instNeZeroNatHMulHPow_pnq
#check @Nat.fact_prime_two
#print NeZero
#print Fact
