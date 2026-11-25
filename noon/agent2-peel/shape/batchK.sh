#!/bin/sh
# batchK.sh: fresh discs and quarter discs, made after the scoring (after.py, K). In no verdict.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch K began %H:%M:%S UTC"
$P -I smake.py disc    exact 100000 30000 61000000 runs-after/exact-disc-100000.jsonl 14
$P -I smake.py quarter exact 100000 16000 62000000 runs-after/exact-quarter-100000.jsonl 14
date -u +"batch K ended %H:%M:%S UTC"
