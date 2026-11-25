#!/bin/sh
# batchM1a.sh: one of the three batches of the second sheet (expectations-2.md): quarter discs, to settle them.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch M1a began %H:%M:%S UTC"
$P -I smake.py quarter exact 100000 120000 90000000 runs-after/q2-cloud-quarter-100000.jsonl 14
date -u +"batch M1a ended %H:%M:%S UTC"
