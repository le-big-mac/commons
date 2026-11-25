#!/bin/bash
# Regenerates the runs, the measurements and the figures.   usage: run.sh PYTHON   (numpy, scipy, matplotlib, scikit-image; about two minutes on 14 cores)
set -euo pipefail
PY="$1"; cd "$(cd "$(dirname "$0")" && pwd)"
for c in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do "$PY" trails.py triangle 3 run-c$c.npz 64 0.12 0 $c > run-c$c.out & done
for sd in 1 2; do "$PY" trails.py triangle 3 run-c0.6-seed$sd.npz 64 0.12 $sd 0.6 > run-c0.6-seed$sd.out & done
for c in 0.3 0.5 0.8; do "$PY" trails.py two 3 two-c$c.npz 64 0.12 0 $c > two-c$c.out & done      # the control: two gates, one straight trail
wait
"$PY" measure.py calibrate > calibrate.out 2>/dev/null
"$PY" measure.py run-c0.1.npz run-c0.2.npz run-c0.3.npz run-c0.4.npz run-c0.5.npz run-c0.6.npz run-c0.6-seed1.npz run-c0.6-seed2.npz run-c0.7.npz run-c0.8.npz run-c0.9.npz two-c0.3.npz two-c0.5.npz two-c0.8.npz > measure.out 2>/dev/null
"$PY" figures.py fig > /dev/null
echo done
