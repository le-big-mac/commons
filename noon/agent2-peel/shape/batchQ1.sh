#!/bin/sh
# batchQ1.sh: the fifth sheet (expectations-5.md), first command: small discs by the first study's generator, and the 1,000-point shapes through cloud.c.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch Q1 began %H:%M:%S UTC"
$P -I own.py disc  83 200000 114000000 runs-after/n5-disc-83.jsonl 14
$P -I own.py disc  90 200000 115000000 runs-after/n5-disc-90.jsonl 14
$P -I own.py disc  98 200000 116000000 runs-after/n5-disc-98.jsonl 14
$P -I own.py disc 105 200000 117000000 runs-after/n5-disc-105.jsonl 14
$P -I own.py disc 113 200000 118000000 runs-after/n5-disc-113.jsonl 14
$P -I own.py disc 120 200000 119000000 runs-after/n5-disc-120.jsonl 14
$P -I smake.py disc      exact 1000 400000 130000000 runs-after/n5-cdisc-1000.jsonl 14
$P -I smake.py triangle  exact 1000 400000 131000000 runs-after/n5-triangle-1000.jsonl 14
$P -I smake.py rtriangle exact 1000 400000 132000000 runs-after/n5-rtriangle-1000.jsonl 14
date -u +"batch Q1 ended %H:%M:%S UTC"
