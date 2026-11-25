#!/bin/sh
# batchC.sh: one of the three batches of the sheet (expectations.md, "The design"). Run with nice, one batch at a time.
cd /home/agent2/peel/shape && mkdir -p runs
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch C began %H:%M:%S UTC"
$P -I smake.py disc      chance 100000 20000 51000000 runs/chance-disc-100000.jsonl 14
$P -I smake.py triangle  chance 100000 20000 52000000 runs/chance-triangle-100000.jsonl 14
$P -I smake.py square    chance 100000  8000 53000000 runs/chance-square-100000.jsonl 14
$P -I smake.py triangle  exact   30000 50000 54000000 runs/exact-triangle-30000.jsonl 14
$P -I smake.py rtriangle exact   30000 50000 55000000 runs/exact-rtriangle-30000.jsonl 14
$P -I smake.py disc      exact   30000 30000 56000000 runs/exact-disc-30000.jsonl 14
date -u +"batch C ended %H:%M:%S UTC"
