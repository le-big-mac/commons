#!/bin/sh
# batchQ2.sh: the fifth sheet (expectations-5.md), second command: the 300-point and 3,000-point triangles through cloud.c.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch Q2 began %H:%M:%S UTC"
$P -I smake.py triangle  exact  300 400000 133000000 runs-after/n5-triangle-300.jsonl 14
$P -I smake.py rtriangle exact  300 400000 134000000 runs-after/n5-rtriangle-300.jsonl 14
$P -I smake.py triangle  exact 3000 200000 135000000 runs-after/n5-triangle-3000.jsonl 14
$P -I smake.py rtriangle exact 3000 200000 136000000 runs-after/n5-rtriangle-3000.jsonl 14
date -u +"batch Q2 ended %H:%M:%S UTC"
