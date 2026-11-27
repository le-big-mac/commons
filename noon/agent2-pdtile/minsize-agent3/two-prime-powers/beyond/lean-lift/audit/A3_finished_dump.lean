import Pnq.LiftMin

open Lean Meta Elab Command in
run_cmd do
  for n in [``Pnq.Lift.instNeZeroMul, ``Pnq.Lift.reduce,
      ``Pnq.Lift.sum_reduce, ``Pnq.Lift.cyclotomic_dvd_reduce_iff, ``Pnq.Lift.exists_lift, ``Pnq.Lift.sizes_eq,
      ``Pnq.Lift.minsize_unbalanced_lift, ``Pnq.Lift.minsize_balanced_all_lift, ``Pnq.Lift.minsize_balanced_lift] do
    let ci ← getConstInfo n
    IO.println s!"### {n} TYPE hash={ci.type.hash} levelParams={ci.levelParams}"
    IO.println (toString (repr ci.type))
    if let .defnInfo d := ci then
      IO.println s!"### {n} VALUE hash={d.value.hash}"
      IO.println (toString (repr d.value))
    if n == ``Pnq.Lift.instNeZeroMul then
      if let .thmInfo d := ci then
        IO.println s!"### {n} VALUE hash={d.value.hash}"
        IO.println (toString (repr d.value))
