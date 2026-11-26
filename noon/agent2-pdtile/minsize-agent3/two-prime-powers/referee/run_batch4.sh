#!/bin/bash
# the author's Z_36 table again with the referee's programme (4 chunks), and two more three-prime cases
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
for J in 0 1 2 3; do nice -n 10 ~/welch/.venv/bin/python retable.py 36 4 $J 120 > out/retable-36-$J.jsonl 2> out/retable-36-$J.err & done
wait
echo done > out/batch4.done
