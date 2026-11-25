#!/bin/bash
# Regenerates every number and figure of this folder from the four downloaded files.   usage: run.sh PYTHON DATADIR [DATADIR2024 [DATADIR20CR [GFSDIR]]]
# (GFSDIR is filled by fetch_gfs.py; sharp.py also needs the eccodes package.)
# (PYTHON needs numpy, h5py, matplotlib.  The data files are read, never executed; python runs with -I.)
set -euo pipefail
PY="$1"; D="$2"; HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
mkdir -p seeds coarse fig
"$PY" -I -B pairs.py "$D" pairs.npz > pairs.out
"$PY" -I -B pairs.py "$D" pairs-pres.npz --pressure pres > pairs-pres.out
for s in 1 2 3 4 5 6 7 8; do "$PY" -I -B pairs.py "$D" seeds/s$s.npz --seed $s > seeds/s$s.out & done
for k in 2 3 4 6 8 12; do for pv in slp pres; do "$PY" -I -B pairs.py "$D" coarse/$pv-$k.npz --pressure $pv --stride $k > coarse/$pv-$k.out & done; done
wait
"$PY" -I -B score.py pairs.npz "$D/land.nc" seeds/s*.npz > score.out
"$PY" -I -B score.py pairs-pres.npz "$D/land.nc" > score-pres.out
"$PY" -I -B check.py "$D" pairs.npz > check.out
"$PY" -I -B check.py "$D" pairs-pres.npz pres > check-pres.out
"$PY" -I -B kacrice.py "$D" pairs.npz > kacrice.out
"$PY" -I -B kacrice.py "$D" pairs-pres.npz pres > kacrice-pres.out
"$PY" -I -B resolution.py pairs.npz pairs-pres.npz coarse > resolution.out
if [ -n "${3:-}" ]; then
  "$PY" -I -B pairs.py "$3" pairs-2024.npz --year 2024 > pairs-2024.out
  "$PY" -I -B secondyear.py pairs.npz pairs-2024.npz > secondyear.out
  if [ -n "${4:-}" ]; then
    "$PY" -I -B finer.py "$4" finer-1980.npz > finer.out
    "$PY" -I -B finerscore.py finer-1980.npz pairs.npz > finerscore.out
    if [ -n "${5:-}" ]; then
      "$PY" -I -B sharp.py "$5" sharp-2025.npz > sharp.out
      "$PY" -I -B sharpscore.py sharp-2025.npz pairs.npz > sharpscore.out
      "$PY" -I -B figures.py "$D" pairs.npz pairs-pres.npz fig pairs-2024.npz finer-1980.npz coarse sharp-2025.npz > figures.out
    else
      "$PY" -I -B figures.py "$D" pairs.npz pairs-pres.npz fig pairs-2024.npz finer-1980.npz coarse > figures.out
    fi
  else
    "$PY" -I -B figures.py "$D" pairs.npz pairs-pres.npz fig pairs-2024.npz > figures.out
  fi
else
  "$PY" -I -B figures.py "$D" pairs.npz pairs-pres.npz fig > figures.out
fi
echo done
