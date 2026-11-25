#!/bin/bash
# longer.sh -- eight trials of 1,200,000 steps: is there a steady braided state?
cd ~/braid
run() { nice -n 15 node try.js 1200000 "NX=48,NY=200,$2" longer/$1 3 > longer/$1.out 2>&1; }
export -f run
xargs -P 8 -L 1 bash -c 'run "$0" "$1"' <<'LIST'
b1 NOISE=3,CS=0.05,KL=0.4
b2 NOISE=3,CS=0.05,KL=0.4,seed=2
e1 NOISE=10,CS=0.05,KL=0.1
e4 NOISE=10,CS=0.05,KL=0.4
k8 NOISE=3,CS=0.05,KL=0.8
n1 NOISE=1,CS=0.05,KL=0.4
k0 NOISE=3,CS=0.05,KL=0
m1 NOISE=3,CS=0.05,KL=0.4,M=1
LIST
