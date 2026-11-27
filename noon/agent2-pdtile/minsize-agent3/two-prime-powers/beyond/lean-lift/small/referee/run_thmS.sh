#!/bin/bash
# Theorem S on very large groups: three streams, every invocation capped at 2 GB and stopped after 590 seconds.
cd /home/agent3/lean/lift-check/small/referee
run() { # GROUP KIND SEED COUNT [nold]
  out=thmS_$1_$2.out
  timeout 590 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python ref_thmS.py "$@" > $out 2>&1
  echo "exit status $? ; seconds since the stream began $SECONDS" >> $out
}
( for k in random pool; do run A $k 21 10; done
  for k in fibres subgroup product caterpillar lift; do run A $k 22 20; done
  run E caterpillar 23 30; run E lift 23 10
  for k in random pool fibres subgroup product caterpillar lift; do run H $k 24 15; done ) &
( for k in caterpillar product subgroup lift fibres pool random; do run G $k 31 15; done
  for k in caterpillar product subgroup lift fibres; do run I $k 32 5; done ) &
( for k in fibres subgroup product lift; do run B $k 41 6; done
  for k in fibres subgroup product lift; do run C $k 42 6; done
  for k in fibres subgroup product lift caterpillar; do run D $k 43 5; done
  for k in caterpillar product subgroup lift fibres pool random; do run J $k 44 8 nold; done ) &
wait
