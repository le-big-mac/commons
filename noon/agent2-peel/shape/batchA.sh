#!/bin/sh
# batchA.sh: one of the three batches of the sheet (expectations.md, "The design"). Run with nice, one batch at a time.
cd /home/agent2/peel/shape && mkdir -p runs
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch A began %H:%M:%S UTC"
$P -I smake.py triangle  exact 100000 50000 41000000 runs/exact-triangle-100000.jsonl 14
$P -I smake.py rtriangle exact 100000 50000 42000000 runs/exact-rtriangle-100000.jsonl 14
date -u +"batch A ended %H:%M:%S UTC"
