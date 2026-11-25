#!/bin/bash
# Referee step 2: four runs, niced.
cd /home/agent2/braid/referee
NB=/home/agent2/braid/fate/kl04-600k.bed
nice -n 15 ./braid_t 3 0 1500000 100000 0 2.5 $NB Cnoon 0 > Cnoon.txt 2>&1 &
nice -n 15 ./braid_t 0 0 600000 50000 0.4 2.5 rip_n1_a0.1.bin R1 0 > R1.txt 2>&1 &
nice -n 15 ./braid_t 0 0 600000 50000 0.4 2.5 rip_n4_L128_a0.1.bin R4 0 > R4.txt 2>&1 &
nice -n 15 ./braid_t 3 5 600000 50000 0.4 2.5 - A2t 0 > A2t.txt 2>&1 &
wait
echo done > DONE2
