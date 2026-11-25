#!/bin/bash
# full model, two stages: 1 solver thread x many patterns with a short limit, then many threads on the leftovers
cd ~/pdflat
for M in "$@"; do
  TAG=full FORM=counts FORBID=1 LIMIT=${L1:-90} PROCS=${P1:-10} WORKERS=1 ~/vuza/.venv/bin/python decide2.py $M >> special.log 2>&1
  if grep "^M=$M \[full\]" summary.txt | tail -1 | grep -q UNKNOWN; then
    TAG=full FORM=counts FORBID=1 LIMIT=${L2:-2400} PROCS=2 WORKERS=6 ~/vuza/.venv/bin/python decide2.py $M >> special.log 2>&1
  fi
done
echo "two_stage done: $@" >> special.log
