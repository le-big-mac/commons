#!/bin/bash
# ex.sh -- a grid of trial settings, eight at a time
cd ~/braid
run() { nice -n 15 node try.js 30000 "$2" ex/$1 3 > ex/$1.out 2>&1; }
export -f run
{
for cs in 0.05 0.15 0.5; do for kl in 0.1 0.4; do for nz in 1 3; do
echo "cs$cs-kl$kl-nz$nz NX=48,NY=200,NOISE=$nz,CS=$cs,KL=$kl"
done; done; done
} | xargs -P 8 -L 1 bash -c 'run "$0" "$1"'
