#!/bin/sh
# batchN2.sh: the third sheet: discs of 300,000 points by the first study's own generator.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch N2 began %H:%M:%S UTC"
$P -I own.py disc 300000 150000 104000000 runs-after/n3-disc-300000.jsonl 14
date -u +"batch N2 ended %H:%M:%S UTC"
