#!/bin/bash
# wide.sh -- six trials on the 64 x 256 bed with wider inflows, 600,000 steps
cd ~/braid
run() { nice -n 15 node try.js 600000 "NX=64,NY=256,$2" wide/$1 3 > wide/$1.out 2>&1; }
export -f run
xargs -P 6 -L 1 bash -c 'run "$0" "$1"' <<'LIST'
f100 FEED=1,NOISE=3,CS=0.05,KL=0.4
f050 FEED=0.5,NOISE=3,CS=0.05,KL=0.4
f025 FEED=0.25,NOISE=3,CS=0.05,KL=0.4
f100k8 FEED=1,NOISE=3,CS=0.05,KL=0.8
f050c15 FEED=0.5,NOISE=3,CS=0.15,KL=0.4
f100n10 FEED=1,NOISE=10,CS=0.05,KL=0.2
LIST
