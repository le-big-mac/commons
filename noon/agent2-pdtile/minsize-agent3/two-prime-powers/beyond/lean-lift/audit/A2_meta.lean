import Pnq.LiftMin
open Lean Meta Elab Command

def auditNames : List Name := [
  ``Pnq.Lift.instNeZeroMul, ``Pnq.Lift.reduce,
  ``Pnq.Lift.sum_reduce, ``Pnq.Lift.cyclotomic_dvd_reduce_iff, ``Pnq.Lift.exists_lift, ``Pnq.Lift.sizes_eq,
  ``Pnq.Lift.minsize_unbalanced_lift, ``Pnq.Lift.minsize_balanced_all_lift, ``Pnq.Lift.minsize_balanced_lift]

def modOf (env : Environment) (n : Name) : String :=
  match env.getModuleIdxFor? n with
  | some i => toString (env.header.moduleNames[i.toNat]!)
  | none => "<this file>"

/- constants used in the TYPE of each audited declaration (and in the VALUE for defs), with the module of each -/
run_cmd do
  let env ← getEnv
  for n in auditNames do
    let ci ← getConstInfo n
    logInfo m!"=== {n} : kind {match ci with | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque" | _ => "other"}; type hash {ci.type.hash}; levelParams {ci.levelParams}"
    let used := ci.type.getUsedConstants
    let mut lines : Array String := #[]
    for c in used do
      lines := lines.push s!"{c}  [{modOf env c}]"
    logInfo m!"constants in type:\n{"\n".intercalate (lines.qsort (· < ·)).toList}"
    if let .defnInfo d := ci then
      let usedV := d.value.getUsedConstants
      let mut l2 : Array String := #[]
      for c in usedV do
        l2 := l2.push s!"{c}  [{modOf env c}]"
      logInfo m!"constants in value of {n}:\n{"\n".intercalate (l2.qsort (· < ·)).toList}"

/- every declaration added by the three modules: kind, instance?, simp?, reducibility -/
run_cmd do
  let env ← getEnv
  let mods := [`Pnq.Lift1, `Pnq.Lift, `Pnq.LiftMin]
  let simpThms ← liftCoreM <| getSimpTheorems
  for m in mods do
    let some idx := env.getModuleIdx? m | throwError "no module {m}"
    let names := env.header.moduleData[idx.toNat]!.constNames
    let mut out : Array String := #[]
    for n in names do
      let some ci := env.find? n | continue
      let kind := match ci with
        | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .axiomInfo _ => "AXIOM" | .opaqueInfo _ => "opaque"
        | .ctorInfo _ => "ctor" | .inductInfo _ => "inductive" | .recInfo _ => "rec" | .quotInfo _ => "quot"
      let isInst ← liftCoreM <| Meta.isInstance n
      let isSimp := simpThms.lemmaNames.contains (.decl n)
      let red := match getReducibilityStatusCore env n with
        | .reducible => "REDUCIBLE" | .semireducible => "semireducible" | .irreducible => "IRREDUCIBLE" | _ => "other-red"
      out := out.push s!"{n} | {kind} | instance={isInst} | simp={isSimp} | {red}"
    logInfo m!"--- module {m}: {names.size} constants\n{"\n".intercalate out.toList}"

/- names that could shadow: does anything called maskW / reduce / minU / minB / IsLeast / cyclotomic / ZMod / castHom exist
    under more than one namespace? -/
run_cmd do
  let env ← getEnv
  let targets := ["maskW", "reduce", "minU", "minB", "xOf", "gOf", "IsLeast", "cyclotomic", "ZMod", "castHom", "Icc", "instNeZeroMul"]
  let mut out : Array String := #[]
  for (n, _) in env.constants.toList do
    if n.isInternal then continue
    match n with
    | .str pre s =>
      if targets.contains s then
        -- only report those that could be seen from namespace Pnq.Lift with `open Finset`: root, Pnq, Pnq.Lift, Finset
        if pre == .anonymous || pre == `Pnq || pre == `Pnq.Lift || pre == `Finset || pre == `Pnq.Lift.Aux || pre == `Polynomial || pre == `ZMod || pre == `Nat then
          out := out.push s!"{n}  [{modOf env n}]"
    | _ => pure ()
  logInfo m!"candidates for name resolution:\n{"\n".intercalate (out.qsort (· < ·)).toList}"

#print axioms Pnq.Lift.sum_reduce
#print axioms Pnq.Lift.cyclotomic_dvd_reduce_iff
#print axioms Pnq.Lift.exists_lift
#print axioms Pnq.Lift.sizes_eq
#print axioms Pnq.Lift.minsize_unbalanced_lift
#print axioms Pnq.Lift.minsize_balanced_all_lift
#print axioms Pnq.Lift.minsize_balanced_lift
#print axioms Pnq.Lift.reduce
#print axioms Pnq.Lift.instNeZeroMul
#print axioms Pnq.maskW
#print axioms Pnq.minU
#print axioms Pnq.minB
