#!/bin/bash
# Sum each fetched mosaic onto the 0.05-degree grid and run the analysis.  usage: process.sh NAME...   (e.g. g2-2020 g1-2000)
set -u
PY=~/welch/.venv/bin/python
for n in "$@"; do
  f=~/downloads/wp-$n/data.tif
  [ -f "$f" ] || { echo "$n: no file"; continue; }
  [ -f ~/hemi2/grids/$n.npy ] || $PY -I ~/hemi2/popgrid2.py "$f" ~/hemi2/grids/$n.npy 0.05 > ~/hemi2/out/$n.popgrid.out 2>&1 || { echo "$n: popgrid failed"; tail -3 ~/hemi2/out/$n.popgrid.out; continue; }
  tail -2 ~/hemi2/out/$n.popgrid.out
  $PY ~/hemi2/run_people2.py "$n" ~/hemi2/grids/$n.npy ~/hemi2/out/$n.json | tee ~/hemi2/out/$n.out
done
