#!/bin/bash
# bounded: 256 patterns, 150 s each, 6 processes: at most 107 minutes of solving; each process is stopped at 115 minutes whatever happens
cd ~/pq2/rule; mkdir -p out225
export OMP_NUM_THREADS=1
for j in 0 1 2 3 4 5; do nice -n 12 timeout 115m ~/welch/.venv/bin/python run225.py 6 $j 150 > out225/z225-$j.jsonl 2> out225/z225-$j.err & done
wait
echo done > out225/z225.done
