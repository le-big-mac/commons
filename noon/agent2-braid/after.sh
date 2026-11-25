#!/bin/bash
# after.sh -- from the grown river (600,000 steps): banks stop crumbling; the sand law made linear.  And a smooth start.
cd ~/braid
nice -n 15 node after.js wide/f100.bed 1500000 KL=0 fate/after-kl0 > fate/after-kl0.out 2>&1 &
nice -n 15 node after.js wide/f100.bed 1500000 M=1 fate/after-m1 > fate/after-m1.out 2>&1 &
nice -n 15 node after.js none 2000000 NOISE=0.2 fate/smooth > fate/smooth.out 2>&1 &
wait
