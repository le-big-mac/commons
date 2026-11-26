import Pnq.Upset
/-! Audit file 3: what the modules `Pnq.Upset` and `Pnq.Upset1` add to the environment. -/
open Lean Meta Elab Command

def modsOfInterest : List Name := [`Pnq.Upset, `Pnq.Upset1]

def kindOf (c : ConstantInfo) : String :=
  match c with
  | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quot" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"

#eval show MetaM Unit from do
  let env ← getEnv
  for modName in modsOfInterest do
    let some idx := env.getModuleIdx? modName | throwError "module {modName} not found"
    IO.println s!"== constants of module {modName} (imports: {(env.header.moduleData[idx.toNat]!).imports.map (·.module)})"
    let names : Array Name := env.constants.fold (init := #[]) fun acc n _ =>
      if env.getModuleIdxFor? n == some idx then acc.push n else acc
    for n in names.qsort (fun a b => a.toString < b.toString) do
      let c ← getConstInfo n
      let inst ← isInstance n
      let simp := (← getSimpTheorems).isLemma (.decl n)
      let red ← isReducible n
      IO.println s!"  {kindOf c}  {n}{if inst then "  [INSTANCE]" else ""}{if simp then "  [SIMP]" else ""}{if red then "  [REDUCIBLE]" else ""}{if n.isInternal then "  (internal)" else ""}"

-- names anywhere in the environment whose last component could shadow a name used in the statements
#eval show MetaM Unit from do
  let env ← getEnv
  let targets : List String := ["maskW", "corners", "IsUpSet", "cyclotomic", "IsLeast", "divisors", "ZMod", "instNeZeroPowMulPow"]
  let hits : Array Name := env.constants.fold (init := #[]) fun acc n _ =>
    match n with
    | Name.str _ s => if targets.contains s then acc.push n else acc
    | _ => acc
  for n in hits.qsort (fun a b => a.toString < b.toString) do
    let m := match env.getModuleIdxFor? n with
      | some i => toString (env.header.moduleNames[i.toNat]!)
      | none => "?"
    IO.println s!"  name with last component {n.getString!}: {n}   (module {m})"

-- instances of NeZero / Fintype / NatCast that the statements could pick up: where do they come from?
set_option pp.explicit true in
#synth NeZero (2 ^ 2 * 3 ^ 1)
example {p q n m : ℕ} [Fact p.Prime] [Fact q.Prime] : NeZero (p ^ n * q ^ m) := inferInstance
set_option pp.explicit true in
#check (inferInstance : Fintype (ZMod (2 ^ 2 * 3 ^ 1)))

#print IsLeast
#print lowerBounds
#print Nat.divisors
#print Polynomial.cyclotomic
#print ZMod
#print ZMod.val
#check @Set.ofPred
#print Set.ofPred
#print axioms Pnq.Upset.structure_iff
#print axioms Pnq.Upset.lower_bound
#print axioms Pnq.Upset.least_size
