#!/bin/bash
# blind runs, L=200, 15000 generations, mean over 10001..15000 every 50
cd /home/agent2/hawk/referee
{
for r in 0.10 0.20 0.22 0.50 0.66 0.68; do echo "0 4 $r 200 15000 11 10000"; done
echo "0 8 0.50 200 15000 11 10000"
echo "1 4 0.30 200 15000 11 10000"; echo "1 4 0.50 200 15000 11 10000"
for r in 0.2 0.5 0.8; do echo "2 4 $r 200 15000 11 10000"; done
} | xargs -P 6 -L 1 ./ref | sort > blind.out
