#!/bin/sh
# batchM1b.sh: one of the three batches of the second sheet (expectations-2.md): quarter discs, to settle them.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch M1b began %H:%M:%S UTC"
$P -I npq.py 100000 120000 91000000 runs-after/q2-numpy-quarter-100000.jsonl 14
date -u +"batch M1b ended %H:%M:%S UTC"
