import Pqr
import Pnq

/-! Run `lake env lean CheckPnq.lean` after `lake build Pqr Pnq`. Each line should print
`depends on axioms: [propext, Classical.choice, Quot.sound]` and nothing else. -/

#print axioms Pnq.weak_tiling_tiles_pnq
#print axioms Pnq.weak_tiling_iff_tiling_pnq
#print axioms Pnq.exists_stepTiling_tree
#print axioms Pnq.step_structure
#print axioms Pnq.bounds_of_stepTiling
#print axioms Pnq.counting
#print axioms Pnq.lemma3
#print axioms Pnq.lemma4
#print axioms Pnq.tiling_of_tree_T1_T2
#print axioms Pnq.E_treeOf
#print axioms Pnq.F_treeOf_zero
#print axioms Pnq.F_treeOf
#print axioms Pqr.IsTiling.pdTiling
#print axioms Pqr.tile_iff_pd_iff_weak_pnq
#print axioms Pqr.tile_iff_pd_iff_weak_pqr
#print axioms Pnq.pow_card_union_le_size
#print axioms Pnq.sharp_lemma3
#print axioms Pnq.pow_card_levels_le_card
#print axioms Pnq.sharp_lemma3_zmod
#print axioms Pnq.balanced_base
#print axioms Pnq.balanced_plus
#print axioms Pnq.balanced_base_zmod
#print axioms Pnq.balanced_plus_zmod
#print axioms Pnq.exists_unbalanced
#print axioms Pnq.exists_balanced_all
#print axioms Pnq.exists_balanced
#print axioms Pnq.isLeast_unbalanced
#print axioms Pnq.isLeast_balanced_all
#print axioms Pnq.isLeast_balanced
#print axioms Pnq.zeroAtW_indW
#print axioms Pnq.maskW_indW
#print axioms Pnq.zeroAtW_iff_cyclotomic_dvd
#print axioms Pnq.treeOfW_indW
#print axioms Pnq.size_treeOfW
#print axioms Pnq.E_treeOfW
#print axioms Pnq.F_treeOfW_zero
#print axioms Pnq.F_treeOfW
#print axioms Pnq.treeOfW_surjective
#print axioms Pnq.minsize_unbalanced_zmod
#print axioms Pnq.minsize_balanced_all_zmod
#print axioms Pnq.minsize_balanced_zmod
