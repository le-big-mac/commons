#!/bin/bash
# long.sh -- eight long trials: do streams sustain themselves?
cd ~/braid
run() { nice -n 15 node try.js 300000 "NX=48,NY=200,$2" long/$1 3 > long/$1.out 2>&1; }
export -f run
xargs -P 8 -L 1 bash -c 'run "$0" "$1"' <<'LIST'
a NOISE=3,CS=0.05,KL=0.1
b NOISE=3,CS=0.05,KL=0.4
c NOISE=3,CS=0.15,KL=0.1
d NOISE=3,CS=0.15,KL=0.4
e NOISE=10,CS=0.05,KL=0.1
f NOISE=10,CS=0.15,KL=0.1
g NOISE=10,CS=0.15,KL=0.4
h NOISE=3,CS=0.5,KL=0.2
LIST
