#!/bin/bash
# controls on the dying-out point (size, time, seed), on "hawks wander singly", and eight neighbours just below 7/9
cd /home/agent2/hawk/referee
{
echo "0 4 0.66 400 30000 41 25000"
echo "0 4 0.67 400 30000 41 25000"
echo "0 4 0.66 200 100000 42 90000"
echo "0 4 0.67 200 60000 42 50000"
echo "0 4 0.10 200 15000 43 10000"
echo "0 4 0.15 200 15000 43 10000"
echo "0 4 0.20 200 15000 43 10000"
echo "0 8 0.77 200 15000 43 10000"
echo "0 4 0.67 200 60000 44 50000"
} | xargs -P 6 -L 1 ./ref2 > ctl2.out
