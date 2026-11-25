import P2q2

/-! Run `lake env lean CheckP2q2.lean` after `lake build`. Each line should print
`depends on axioms: [propext, Classical.choice, Quot.sound]` and nothing else. -/

-- the theorem
#print axioms P2q2.weak_tiling_iff_tiling_p2q2
#print axioms P2q2.weak_tiling_tiles_p2q2
#print axioms P2q2.weak_tiling_tiles_p2q2_of_lt
-- the reductions (Lemmas 2 and 3 of the note)
#print axioms P2q2.tiling_of_units_charged
#print axioms P2q2.tiling_of_support_p
#print axioms P2q2.tiling_of_support_q
#print axioms P2q2.exists_common_complement_pnq
#print axioms P2q2.SA_eq_of_common_complement_pnq
#print axioms P2q2.no_orphan_of_weakTiling_pnq
#print axioms P2q2.T1_T2_of_weakTiling_pnq
-- the linear programme
#print axioms P2q2.exists_nine
#print axioms P2q2.weakTiling_of_nine
#print axioms P2q2.card_mul_L00_of_weakTiling_toMu
#print axioms P2q2.m00_pos
#print axioms P2q2.dispatchA
#print axioms P2q2.dispatchB
#print axioms P2q2.atoms_of
-- the rest
#print axioms P2q2.tiling_of_patA
#print axioms P2q2.kfac_le_card
#print axioms P2q2.zeroAt_pq2_of_card
#print axioms P2q2.no_card
