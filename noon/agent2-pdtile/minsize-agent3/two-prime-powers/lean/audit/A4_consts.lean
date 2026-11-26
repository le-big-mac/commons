import Pnq.Upset
/-! Audit file 4: every constant that occurs in the three statements, in the two definitions and in `maskW`,
with the module it comes from. Anything not from Lean core / Mathlib is listed first. -/
open Lean Meta

#eval show MetaM Unit from do
  let env ← getEnv
  let roots : List Name := [``Pnq.Upset.structure_iff, ``Pnq.Upset.lower_bound, ``Pnq.Upset.least_size]
  let defs : List Name := [``Pnq.Upset.IsUpSet, ``Pnq.Upset.corners, ``Pnq.maskW]
  let mut used : NameSet := {}
  for n in roots do
    let c ← getConstInfo n
    for k in c.type.getUsedConstants do used := used.insert k
  for n in defs do
    let c ← getConstInfo n
    for k in c.type.getUsedConstants do used := used.insert k
    for k in c.value!.getUsedConstants do used := used.insert k
  let modOf (n : Name) : String := match env.getModuleIdxFor? n with
    | some i => toString (env.header.moduleNames[i.toNat]!)
    | none => "?"
  let arr := used.toList.toArray.qsort (fun a b => a.toString < b.toString)
  IO.println s!"{arr.size} constants in all"
  IO.println "-- from the project (not Lean core, Std, Batteries, Mathlib):"
  for n in arr do
    let m := modOf n
    if !(m.startsWith "Mathlib" || m.startsWith "Init" || m.startsWith "Lean" || m.startsWith "Std" || m.startsWith "Batteries") then
      IO.println s!"  {n}   [{m}]"
  IO.println "-- from Lean core / Mathlib:"
  for n in arr do
    let m := modOf n
    if (m.startsWith "Mathlib" || m.startsWith "Init" || m.startsWith "Lean" || m.startsWith "Std" || m.startsWith "Batteries") then
      IO.println s!"  {n}   [{m}]"
