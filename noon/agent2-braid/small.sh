#!/bin/bash
# small.sh -- (added after the referee, not refereed) the constant added to the slope made smaller: 0.3 of the slope and a
# tenth of it, from rough sand, 2,000,000 steps each, the page's setting otherwise
cd ~/braid
nice -n 15 node fate.js 2000000 CS=0.015 fate/cs03 > fate/cs03.out 2>&1 &
nice -n 15 node fate.js 2000000 CS=0.005 fate/cs01 > fate/cs01.out 2>&1 &
wait
