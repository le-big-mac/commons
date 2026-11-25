#!/bin/bash
# capped.sh -- (1), (2) smooth and gently rough starts with the length of a step capped, so that the smooth bed does not jitter;
# (3) the page's run again with steps a third as long (LIMIT 0.01), to see whether the measures depend on the step
cd ~/braid
nice -n 15 node fate.js 400000 NOISE=0.2,DTMAX=5 fate/smooth-capped > fate/smooth-capped.out 2>&1 &
nice -n 15 node fate.js 400000 NOISE=1,DTMAX=5 fate/gentle-capped > fate/gentle-capped.out 2>&1 &
nice -n 15 node fate.js 2000000 LIMIT=0.01 fate/limit01 > fate/limit01.out 2>&1 &
wait
