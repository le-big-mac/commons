#!/bin/bash
# usage: run_regrid.sh NAME...   (e.g. g2-2020 g1-2000); runs the checker's regrid.py on each, in parallel
PY=/home/agent3/welch/.venv/bin/python
C=/home/agent3/hemi2/check
for n in "$@"; do
  $PY -I $C/regrid.py $n /home/agent3/downloads/wp-$n/data.tif /home/agent3/hemi2/grids/$n.npy $C/grids/$n.npy $C/out/regrid-$n.json > $C/out/regrid-$n.out 2>&1 &
done
wait
