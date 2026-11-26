#!/bin/bash
# bounded: 'smaller' (12 patterns, 120 s each, 2 processes) then 'undecided' (24 patterns, 1500 s each, 6 processes: at most 100 minutes)
cd ~/pq2
export OMP_NUM_THREADS=1
for j in 0 1; do nice -n 10 ~/welch/.venv/bin/python finish100.py 100 2 $j 120 smaller > out2/z100-smaller-$j.jsonl 2> out2/z100-smaller-$j.err & done
for j in 0 1 2 3 4 5; do nice -n 10 timeout 105m ~/welch/.venv/bin/python finish100.py 100 6 $j 1500 undecided > out2/z100-undecided-$j.jsonl 2> out2/z100-undecided-$j.err & done
wait
echo done > out2/finish100.done
