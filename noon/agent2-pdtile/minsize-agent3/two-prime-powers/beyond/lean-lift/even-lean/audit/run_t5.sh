#!/bin/bash
# the two final statements, literally: a chain of short runs (each stops itself after 270 s)
cd /home/agent3/lean/even-audit
PY="bash /home/agent3/bin/cap2g.sh /home/agent3/welch/.venv/bin/python -I t5_final.py"
$PY 1 6 10 > t5_final_6_10.out 2>&1
$PY 7 10 7 > t5_final_10_7.out 2>&1
$PY 11 16 6 > t5_final_16_6.out 2>&1
$PY 17 24 5 > t5_final_24_5.out 2>&1
$PY 25 36 4 > t5_final_36_4.out 2>&1
$PY 37 60 3 > t5_final_60_3.out 2>&1
echo done > t5_done
