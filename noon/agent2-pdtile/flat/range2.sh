#!/bin/bash
# usage: FORM=counts|residues ./range2.sh lo hi   (resumable)
cd ~/pdflat
F=${FORM:-counts}
for M in $(seq $1 $2); do
  if grep -q "^M=$M \[$F\]" summary.txt 2>/dev/null; then continue; fi
  FORM=$F LIMIT=${LIMIT:-300} PROCS=${PROCS:-6} ~/vuza/.venv/bin/python decide2.py $M >> range_$F.log 2>&1
done
echo "range $1-$2 done ($F)" >> range_$F.log
