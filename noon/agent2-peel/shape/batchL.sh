#!/bin/sh
# batchL.sh: after the referee: clouds from the first study's own generator (no cloud.c), and quarter discs from numpy's. In no verdict.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch L began %H:%M:%S UTC"
$P -I own.py disc     100000 75000 80000000 runs-after/own-disc-100000.jsonl 14
$P -I own.py square   100000 75000 81000000 runs-after/own-square-100000.jsonl 14
$P -I own.py triangle 100000 75000 82000000 runs-after/own-triangle-100000.jsonl 14
$P -I npq.py 100000 60000 83000000 runs-after/numpy-quarter-100000.jsonl 14
date -u +"batch L ended %H:%M:%S UTC"
