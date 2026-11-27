#!/bin/bash
# The set-lift test, one case after another (one process at a time), each under the 2 GB cap.
# Arguments of t1_setlift.py: N r j [maxsupp|0] [sample|0].  One JSON line per case.
cd /home/agent3/lean/sets-audit
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
OUT=t1_setlift_main.out
: > $OUT
run() { $PY t1_setlift.py "$@" >> $OUT 2>&1; }
# r = 3, j = 1
for N in 1 2 3 4 5 6 7 8 9; do run $N 3 1; done
run 10 3 1 4; run 12 3 1 4; for N in 15 18 20 24 30; do run $N 3 1 3; done
# r = 3, j = 2
for N in 1 2 3 4 5; do run $N 3 2; done
run 6 3 2 4; run 6 3 2 0 30000; for N in 7 8 9 10 12; do run $N 3 2 3; done
# r = 3, j = 3, 4
run 1 3 3; run 2 3 3; run 3 3 3; run 4 3 3 2; run 4 3 3 0 5000; run 6 3 3 2; run 1 3 4; run 2 3 4
# r = 5, j = 1
for N in 1 2 3 4 5 6 7; do run $N 5 1; done
for N in 8 10 12 15 20; do run $N 5 1 3; done
# r = 5, j = 2, 3
run 1 5 2; run 2 5 2; run 3 5 2; run 4 5 2 3; run 5 5 2 2; run 5 5 2 0 5000; run 6 5 2 2; run 10 5 2 2; run 1 5 3; run 2 5 3
# r = 7, j = 1
for N in 1 2 3 4 5 6; do run $N 7 1; done
for N in 7 8 10 12 14; do run $N 7 1 3; done
# r = 7, j = 2
run 1 7 2; run 2 7 2; run 3 7 2 2; run 3 7 2 0 5000; run 4 7 2 2; run 6 7 2 2; run 7 7 2 2
# r = 11, 13, j = 1
for N in 1 2 3 4; do run $N 11 1; done
run 6 11 1 3; run 11 11 1 2
for N in 1 2 3; do run $N 13 1; done
run 4 13 1 3
echo ALL DONE >> $OUT
