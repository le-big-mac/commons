#!/bin/bash
# controls on the first change: long runs just above 1/(k+1), and a run started from the low state
cd /home/agent2/hawk/referee
{
echo "0 4 0.210 200 100000 31 90000"
echo "0 4 0.205 200 100000 31 90000"
echo "0 4 0.215 200 60000 31 50000"
echo "0 8 0.112 200 60000 31 50000"
echo "0 8 0.110 200 60000 31 50000"
echo "0 4 0.210 200 60000 31 50000 0.22 3000"
} | xargs -P 6 -L 1 ./ref2 > ctl1.out
