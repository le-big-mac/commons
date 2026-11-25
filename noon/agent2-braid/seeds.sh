#!/bin/bash
# seeds.sh -- six more draws of the page's setting from rough sand, 600,000 steps each (after the referee: how far do draws differ?)
cd ~/braid
for s in 3 4 5 6 7 8; do nice -n 15 node fate.js 600000 seed=$s seeds/s$s > seeds/s$s.out 2>&1 & done
wait
