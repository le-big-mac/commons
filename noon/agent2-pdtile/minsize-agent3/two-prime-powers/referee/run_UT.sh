#!/bin/bash
# Corollaries U and T on further groups; 6 processes; HiGHS, 300 s for one programme
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
printf '%s\n' 18 24 48 54 72 100 108 144 200 225 162 96 | xargs -P 6 -I{} sh -c 'nice -n 10 ~/welch/.venv/bin/python cor_UT.py {} highs 300 > out/UT-{}.jsonl 2> out/UT-{}.err'
echo done > out/UT.done
