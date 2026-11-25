#!/bin/bash
# sand.sh -- a set feed of sand at the head (2, 4, 8, 16 times a sheet's), head row free: 2,000,000 steps each
cd ~/braid
for k in 2 4 8 16; do nice -n 15 node fate.js 2000000 SAND=$k sand/s$k > sand/s$k.out 2>&1 & done
wait
