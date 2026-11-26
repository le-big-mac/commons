#!/bin/bash
# the author's Z_100 table again with the referee's programme (3 chunks, 60 s for one pattern)
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
for J in 0 1 2; do nice -n 10 ~/welch/.venv/bin/python retable.py 100 3 $J 60 2> out/retable-100-$J.err | grep --line-buffered '^{' > out/retable-100-$J.jsonl & done
wait
echo done > out/batch6.done
