import Pnq

/-! Run `lake env lean Check.lean` after `lake build`. Each line should print
`depends on axioms: [propext, Classical.choice, Quot.sound]` and nothing else. -/

#print axioms Pnq.pow_e_dvd_size
#print axioms Pnq.lemma3
#print axioms Pnq.lemma4
#print axioms Pnq.counting
#print axioms Pnq.tiles_sum
#print axioms Pnq.step_U1
#print axioms Pnq.step_U2
#print axioms Pnq.step_L2
#print axioms Pnq.step_structure
#print axioms Pnq.bounds_of_stepTiling
#print axioms Pnq.Tiles_node
