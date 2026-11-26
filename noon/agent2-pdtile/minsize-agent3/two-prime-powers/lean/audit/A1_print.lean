import Pnq.Upset
/-! Audit file 1: print the two definitions, the instance and the three statements with nothing hidden. -/
open Lean Meta Elab Command

#print Pnq.Upset.IsUpSet
#print Pnq.Upset.corners
#print Pnq.Upset.instNeZeroPowMulPow
#print Pnq.maskW

section
set_option pp.explicit true
set_option pp.proofs true
set_option pp.coercions false
set_option pp.funBinderTypes true
set_option pp.numericTypes true
#print Pnq.Upset.IsUpSet
#print Pnq.Upset.corners
#print Pnq.maskW
#check @Pnq.Upset.instNeZeroPowMulPow
#check @Pnq.Upset.structure_iff
#check @Pnq.Upset.lower_bound
#check @Pnq.Upset.least_size
end

section
set_option pp.all true
set_option pp.proofs true
#print Pnq.Upset.IsUpSet
#print Pnq.Upset.corners
#print Pnq.maskW
#check @Pnq.Upset.structure_iff
#check @Pnq.Upset.lower_bound
#check @Pnq.Upset.least_size
end

-- raw expressions and their hashes (to compare with the skeleton)
def showRaw (n : Name) : MetaM Unit := do
  let c ← getConstInfo n
  IO.println s!"RAW {n} : hash {c.type.hash}"
  IO.println (toString c.type)
  match c.value? with
  | some v => if !(← isProp c.type) then
                IO.println s!"RAWVAL {n} : hash {v.hash}"
                IO.println (toString v)
  | none => pure ()

#eval showRaw ``Pnq.Upset.IsUpSet
#eval showRaw ``Pnq.Upset.corners
#eval showRaw ``Pnq.Upset.instNeZeroPowMulPow
#eval showRaw ``Pnq.Upset.structure_iff
#eval showRaw ``Pnq.Upset.lower_bound
#eval showRaw ``Pnq.Upset.least_size

#print axioms Pnq.Upset.structure_iff
#print axioms Pnq.Upset.lower_bound
#print axioms Pnq.Upset.least_size
#print axioms Pnq.Upset.instNeZeroPowMulPow
