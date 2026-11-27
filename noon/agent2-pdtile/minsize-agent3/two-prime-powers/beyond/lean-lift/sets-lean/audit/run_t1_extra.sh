#!/bin/bash
# Random samples of w with supports of every size (t1_setlift.py N r j 0 sample), on larger N, including N with three prime
# factors.  One process at a time, under the 2 GB cap.
cd /home/agent3/lean/sets-audit
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
OUT=t1_setlift_extra.out
: > $OUT
for a in "12 3 1" "20 3 1" "30 3 1" "45 3 1" "12 3 2" "20 3 2" "30 3 2" "8 3 3" "15 5 1" "30 5 1" "42 5 1" "10 5 2" "12 5 2" "12 7 1" "30 7 1" "60 7 1" "6 7 2" "10 7 2" "30 11 1" "24 13 1"; do
  $PY t1_setlift.py $a 0 20000 >> $OUT 2>&1
done
echo ALL DONE >> $OUT
