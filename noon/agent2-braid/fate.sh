#!/bin/bash
# fate.sh -- four runs of 4,000,000 steps on the page's bed (64 x 256, water in every head cell)
cd ~/braid
run() { nice -n 15 node fate.js 4000000 "$2" fate/$1 > fate/$1.out 2>&1; }
export -f run
xargs -P 4 -L 1 bash -c 'run "$0" "$1"' <<'LIST'
kl02 KL=0.2
kl04 KL=0.4
kl08 KL=0.8
kl04s2 KL=0.4,seed=2
LIST
