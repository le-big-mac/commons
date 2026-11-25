#!/bin/sh
# batchN1.sh: the third sheet (expectations-3.md): discs by the first study's own generator, four sizes.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch N1 began %H:%M:%S UTC"
$P -I own.py disc   3000 400000 100000000 runs-after/n3-disc-3000.jsonl 14
$P -I own.py disc  10000 400000 101000000 runs-after/n3-disc-10000.jsonl 14
$P -I own.py disc  30000 400000 102000000 runs-after/n3-disc-30000.jsonl 14
$P -I own.py disc 100000 300000 103000000 runs-after/n3-disc-100000.jsonl 14
date -u +"batch N1 ended %H:%M:%S UTC"
