#!/bin/bash
cd /home/agent2/web
export NODE_PATH=/home/agent2/web/node_modules LD_LIBRARY_PATH=/home/agent2/web/sysroot/usr/lib/x86_64-linux-gnu
R=/home/agent2/gospel/referee/page; G=/home/agent2/gospel
for n in 6 7; do
  nice -n 15 timeout 150 node shot-gospel.js $R/mutant-$n/double.html $R/mutant-$n-shots $G/core.js $G/table.json $G/gospel.sealed-run.out $G/more.sealed-run.out > $R/mutant-$n.out 2>&1
done
echo finished
