#!/bin/sh
# batchK2.sh: more fresh quarter discs and half discs, made because the quarter disc stayed above its line in batch K. In no verdict.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch K2 began %H:%M:%S UTC"
$P -I smake.py quarter  exact 100000 60000 63000000 runs-after/exact-quarter-100000-b.jsonl 9
$P -I smake.py halfdisc exact 100000 40000 64000000 runs-after/exact-halfdisc-100000.jsonl 9
date -u +"batch K2 ended %H:%M:%S UTC"
