#!/bin/bash
# six sizes, two processes of two threads at a time, 240 s each at most
cd /home/agent3/pq2/referee/two-powers/second
export OMP_NUM_THREADS=1
printf '%s\n' 6 12 18 24 30 36 42 | xargs -P 2 -I{} sh -c 'nice -n 10 ~/welch/.venv/bin/python -B cpsat_42.py {} 240 2 >> out/cpsat_42.jsonl 2>> out/cpsat_42.err'
echo done > out/cpsat_42.done
