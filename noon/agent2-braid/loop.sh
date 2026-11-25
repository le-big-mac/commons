#!/bin/bash
# loop.sh -- the bed joined end to end: three runs of 2,000,000 steps (sideways constant 0.2, 0.4, 0.8)
cd ~/braid
nice -n 15 node fate.js 2000000 LOOP=1,KL=0.2 loop/kl02 > loop/kl02.out 2>&1 &
nice -n 15 node fate.js 2000000 LOOP=1,KL=0.4 loop/kl04 > loop/kl04.out 2>&1 &
nice -n 15 node fate.js 2000000 LOOP=1,KL=0.8 loop/kl08 > loop/kl08.out 2>&1 &
wait
