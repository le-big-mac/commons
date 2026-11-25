#!/bin/bash
# rough.sh -- how rough must the sand be?  Starts scattered over 1, 1.5, 2 and 2.5 row-falls, 600,000 steps each (the page's
# setting otherwise); and a nearly smooth bed with one ditch dug in it.
cd ~/braid
for a in 1 1.5 2 2.5; do nice -n 15 node fate.js 600000 NOISE=$a fate/rough$a > fate/rough$a.out 2>&1 & done
nice -n 15 node after.js fate/ditch-start.bed 600000 NOISE=0.2 fate/ditch > fate/ditch.out 2>&1 &
wait
