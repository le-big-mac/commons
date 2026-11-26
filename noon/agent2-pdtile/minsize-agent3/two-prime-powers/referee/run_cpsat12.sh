#!/bin/bash
# the remaining eight of the twelve, four processes of two threads each, 400 s for one pattern
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
for J in 0 1 2 3; do nice -n 10 ~/welch/.venv/bin/python cpsat12.py $J 4 400 4 > out/cpsat12-rest-$J.jsonl 2> out/cpsat12-rest-$J.err & done
wait
echo done > out/cpsat12.done
