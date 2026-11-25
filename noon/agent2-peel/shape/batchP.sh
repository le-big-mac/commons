#!/bin/sh
# batchP.sh: the fourth sheet (expectations-4.md): small discs by the first study's own generator, 400,000 of each of four sizes.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch P began %H:%M:%S UTC"
$P -I own.py disc    4 400000 110000000 runs-after/n4-disc-4.jsonl 14
$P -I own.py disc  100 400000 111000000 runs-after/n4-disc-100.jsonl 14
$P -I own.py disc  300 400000 112000000 runs-after/n4-disc-300.jsonl 14
$P -I own.py disc 1000 400000 113000000 runs-after/n4-disc-1000.jsonl 14
date -u +"batch P ended %H:%M:%S UTC"
