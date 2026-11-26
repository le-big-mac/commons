import Pnq.MinGroup
import Lean

-- Audit scratch: for the three theorems, walk the STATEMENT (the type), and the bodies of
-- every definition reached that is declared in this project (modules Pnq.*, Pqr.*, P2q2.*),
-- and print for each constant met the module that declares it.  A constant with a Mathlib-like
-- name declared in a project module would show up here.

open Lean Elab Command Meta

def projMod (m : Name) : Bool :=
  let r := m.getRoot
  r == `Pnq || r == `Pqr || r == `P2q2

partial def walk (env : Environment) (todo : List Name) (seen : NameSet)
    (acc : Array (Name × Name)) : Array (Name × Name) :=
  match todo with
  | [] => acc
  | c :: rest =>
    if seen.contains c then walk env rest seen acc else
    let seen := seen.insert c
    let modName : Name := match env.getModuleIdxFor? c with
      | some idx => env.header.moduleNames[idx.toNat]!
      | none => `_this_file_
    let acc := acc.push (c, modName)
    if projMod modName then
      match env.find? c with
      | some ci =>
        let used := match ci with
          | .defnInfo d => d.type.getUsedConstants ++ d.value.getUsedConstants
          | .thmInfo t => t.type.getUsedConstants   -- statement only
          | .inductInfo i => i.type.getUsedConstants ++ i.ctors.toArray
          | .ctorInfo i => i.type.getUsedConstants
          | .recInfo i => i.type.getUsedConstants
          | .opaqueInfo o => o.type.getUsedConstants ++ o.value.getUsedConstants
          | .axiomInfo a => a.type.getUsedConstants
          | .quotInfo q => q.type.getUsedConstants
        walk env (used.toList ++ rest) seen acc
      | none => walk env rest seen acc
    else walk env rest seen acc

elab "#audit_modules " ids:ident+ : command => do
  let env ← getEnv
  let names := ids.toList.map (·.getId)
  let res := walk env names {} #[]
  let proj := res.filter (fun (_, m) => projMod m)
  let other := res.filter (fun (_, m) => !projMod m)
  logInfo m!"declared in this project ({proj.size}):"
  for (c, m) in proj do
    let kind := match env.find? c with
      | some (.defnInfo _) => "def"
      | some (.thmInfo _) => "theorem"
      | some (.inductInfo _) => "inductive"
      | some (.ctorInfo _) => "constructor"
      | some (.recInfo _) => "recursor"
      | some (.opaqueInfo _) => "opaque"
      | some (.axiomInfo _) => "AXIOM"
      | some (.quotInfo _) => "quot"
      | none => "?"
    logInfo m!"  {kind} {c}  [{m}]"
  logInfo m!"declared outside this project ({other.size}):"
  let sorted := other.qsort (fun a b => a.1.toString < b.1.toString)
  for (c, m) in sorted do
    logInfo m!"  {c}  [{m}]"

#audit_modules Pnq.minsize_unbalanced_zmod Pnq.minsize_balanced_all_zmod Pnq.minsize_balanced_zmod
