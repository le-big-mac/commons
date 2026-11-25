#!/bin/sh
# batchM2.sh: one of the three batches of the second sheet (expectations-2.md): quarter discs, to settle them.
cd /home/agent2/peel/shape && mkdir -p runs-after
P=/home/agent2/vuza/.venv/bin/python
export OMP_NUM_THREADS=1
date -u +"batch M2 began %H:%M:%S UTC"
$P -I smake.py quarter exact 30000 120000 92000000 runs-after/q2-cloud-quarter-30000.jsonl 14
$P -I npq.py 30000 120000 93000000 runs-after/q2-numpy-quarter-30000.jsonl 14
date -u +"batch M2 ended %H:%M:%S UTC"
