#!/bin/bash
# Part T: two chains of short runs (each run stops itself after 270 s); usage: run_t1.sh A|B
cd /home/agent3/lean/even-audit
PY="bash /home/agent3/bin/cap2g.sh /home/agent3/welch/.venv/bin/python -I t1_twice.py"
if [ "$1" = A ]; then
  out=t1_twice_A.out; : > $out
  $PY exh Z 1 8 >> $out 2>&1
  $PY exh Z 2 6 >> $out 2>&1
  $PY exh Z 3 4 >> $out 2>&1
  $PY exh Z 4 3 >> $out 2>&1
  $PY exh Z2g 1 11 >> $out 2>&1
  $PY exh Z2g 2 9 >> $out 2>&1
  $PY exh Z2g 3 6 >> $out 2>&1
  $PY exh Z2g 4 5 >> $out 2>&1
  $PY exh Z3g 1 10 >> $out 2>&1
  $PY exh Z3g 2 7 >> $out 2>&1
  $PY exh Z3g 3 5 >> $out 2>&1
  $PY exh Z3g 4 4 >> $out 2>&1
  for g in Z Z2g Z3g; do $PY rand $g 15000 1 >> $out 2>&1; done
else
  out=t1_twice_B.out; : > $out
  $PY exh Z4g 1 9 >> $out 2>&1
  $PY exh Z4g 2 6 >> $out 2>&1
  $PY exh Z4g 3 4 >> $out 2>&1
  $PY exh Z6g 1 7 >> $out 2>&1
  $PY exh Z6g 2 5 >> $out 2>&1
  $PY exh Z6g 3 4 >> $out 2>&1
  $PY exh ZxZ 1 7 >> $out 2>&1
  $PY exh ZxZ 2 5 >> $out 2>&1
  $PY exh ZxZ 3 4 >> $out 2>&1
  for g in Z4g Z6g ZxZ; do $PY rand $g 15000 2 >> $out 2>&1; done
fi
echo "chain $1 done" >> $out
