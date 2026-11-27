#!/bin/bash
# one more stream: further seeds on the groups that none of Theorems 2, 3, 6, 7 covers
cd /home/agent3/lean/lift-check/small/referee
run() { # GROUP KIND SEED COUNT
  out=thmS_$1_$2_seed$3.out
  timeout 590 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python ref_thmS.py "$@" > $out 2>&1
  echo "exit status $? ; seconds since the stream began $SECONDS" >> $out
}
run H caterpillar 51 60; run H fibres 51 40; run H subgroup 51 40; run H product 51 30
run G caterpillar 52 30; run G fibres 52 20
