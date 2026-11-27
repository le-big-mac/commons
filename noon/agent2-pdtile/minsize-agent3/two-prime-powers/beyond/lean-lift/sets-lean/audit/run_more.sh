#!/bin/bash
# Second batch, one process at a time, each under the 2 GB cap:
#  (1) censuses for the controls (M not of the form p^n q; Z_24 complete);
#  (2) the set-lift test for r = 2 (excluded by the statement) and with fewer random tries;
#  (3) lifts of multisets to sets on groups too large for a census (t4_lift_sets.py).
cd /home/agent3/lean/sets-audit
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
# (1)
for mt in "1 27" "4 16" "8 12" "9 12" "16 8" "25 8" "27 8" "30 8"; do
  set -- $mt; $PY t2_census.py multi $1 $2 2>&1 | tail -1
done
$PY t2_census.py set 24 24 2>&1 | tail -1
# (2)
OUT=t1_setlift_control.out
: > $OUT
for N in 1 2 3 4 5 6 7 8 9 10; do T1_K=300 $PY t1_setlift.py $N 2 1 >> $OUT 2>&1; done
for N in 1 2 3 4 5; do T1_K=300 $PY t1_setlift.py $N 2 2 >> $OUT 2>&1; done
for N in 1 2; do T1_K=300 $PY t1_setlift.py $N 2 3 >> $OUT 2>&1; done
echo ALL DONE >> $OUT
# (3)  arguments: M s [tmax|0] [sample per size|0]
OUT=t4_lift_sets.out
: > $OUT
run4() { $PY t4_lift_sets.py "$@" >> $OUT 2>&1; }
for s in 9 25 27 49 81 125; do run4 2 $s; done
for s in 9 25 27 49 81; do run4 3 $s; done
for s in 9 25 27 49; do run4 5 $s 0 3000; done
for s in 9 25 49; do run4 7 $s 0 3000; done
run4 6 9; run4 6 18; run4 6 15; run4 6 21; run4 6 45 0 5000; run4 6 25 0 3000; run4 6 27 0 3000; run4 6 49 0 1500
run4 10 9; run4 10 18 0 5000; run4 10 27 0 2000; run4 10 25 0 2000
run4 12 9 0 20000; run4 12 15; run4 12 18 0 10000; run4 12 25 0 1500; run4 12 27 0 1500
run4 15 9 0 10000; run4 15 7 0 20000; run4 15 25 0 1500
run4 18 5; run4 18 9 0 10000; run4 18 25 0 1000
run4 20 9 0 10000; run4 20 7 0 10000
run4 24 9 0 6000; run4 24 5
run4 28 9 0 5000; run4 45 7 0 4000; run4 50 9 0 3000; run4 54 5; run4 40 9 0 3000
echo ALL DONE >> $OUT
