#!/bin/bash
# Part T, a third chain with larger sizes (each run stops itself after 270 s)
cd /home/agent3/lean/even-audit
PY="bash /home/agent3/bin/cap2g.sh /home/agent3/welch/.venv/bin/python -I t1_twice.py"
out=t1_twice_C.out; : > $out
$PY exh Z3g 2 8 >> $out 2>&1
$PY exh Z3g 3 6 >> $out 2>&1
$PY exh Z 2 7 >> $out 2>&1
$PY exh Z 3 5 >> $out 2>&1
$PY exh Z2g 3 7 >> $out 2>&1
$PY exh Z4g 2 7 >> $out 2>&1
$PY exh Z6g 2 6 >> $out 2>&1
$PY exh ZxZ 2 6 >> $out 2>&1
for g in Z Z2g Z3g Z4g Z6g ZxZ; do $PY rand $g 40000 7 >> $out 2>&1; done
echo "chain C done" >> $out
