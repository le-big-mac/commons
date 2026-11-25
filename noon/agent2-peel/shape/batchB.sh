#!/bin/sh
# batchB.sh: one of the three batches of the sheet (expectations.md, "The design"). Run with nice, one batch at a time.
cd /home/agent2/peel/shape && mkdir -p runs
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch B began %H:%M:%S UTC"
$P -I smake.py disc     exact 100000 30000 43000000 runs/exact-disc-100000.jsonl 14
$P -I smake.py square   exact 100000 16000 44000000 runs/exact-square-100000.jsonl 14
$P -I smake.py hexagon  exact 100000 16000 45000000 runs/exact-hexagon-100000.jsonl 14
$P -I smake.py ellipse  exact 100000  8000 46000000 runs/exact-ellipse-100000.jsonl 14
$P -I smake.py halfdisc exact 100000  8000 47000000 runs/exact-halfdisc-100000.jsonl 14
$P -I smake.py quarter  exact 100000  8000 48000000 runs/exact-quarter-100000.jsonl 14
$P -I smake.py disc0    exact 100000 20000 49000000 runs/exact-disc0-100000.jsonl 14
date -u +"batch B ended %H:%M:%S UTC"
