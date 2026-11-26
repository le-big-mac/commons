#!/bin/bash
# random multisets not built from cosets, and linear-programme vertices; 5 processes
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
printf '%s\n' "12 2000 200" "18 2000 200" "36 1000 200" "72 400 100" "108 300 100" "30 300 100" | xargs -P 5 -L 1 sh -c 'nice -n 10 ~/welch/.venv/bin/python random_S.py $0 $1 $2 20261126 > out/random-$0.jsonl 2> out/random-$0.err'
echo done > out/random.done
