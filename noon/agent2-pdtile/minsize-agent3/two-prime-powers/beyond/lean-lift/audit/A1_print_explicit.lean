import Pnq.LiftMin
set_option pp.explicit true
set_option pp.fullNames true
set_option pp.proofs true
set_option pp.funBinderTypes true
set_option pp.width 200
#print Pnq.Lift.instNeZeroMul
#print Pnq.Lift.reduce
#print Pnq.maskW
#print Pnq.minU
#print Pnq.minB
#print Pnq.xOf
#print Pnq.gOf
#check @Pnq.Lift.sum_reduce
#check @Pnq.Lift.cyclotomic_dvd_reduce_iff
#check @Pnq.Lift.exists_lift
#check @Pnq.Lift.sizes_eq
#check @Pnq.Lift.minsize_unbalanced_lift
#check @Pnq.Lift.minsize_balanced_all_lift
#check @Pnq.Lift.minsize_balanced_lift
#check @Pnq.minsize_unbalanced_zmod
#check @Pnq.minsize_balanced_all_zmod
#check @Pnq.minsize_balanced_zmod
#print Pnq.levelsEW
#print Pnq.levelsFW
