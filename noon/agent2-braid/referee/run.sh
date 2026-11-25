#!/bin/bash
# Referee step 1 driver. At most four processes at a time, all niced.
cd /home/agent2/braid/referee
B=./braid_n
# A carried straight on to 2,000,000 (= run E); bed saved at 600,000
nice -n 15 $B 3 20261123 2000000 100000 0.4 2.5 - A 600000 > A_E.txt 2> A_E.err &
PA=$!
nice -n 15 $B 0.2 77 600000 100000 0.4 2.5 - B 0 > B.txt 2> B.err &
P1=$!
nice -n 15 $B 3 5 600000 100000 0.4 2.5 - A2 600000 > A2.txt 2> A2.err &
P2=$!
nice -n 15 $B 0.2 6 600000 100000 0.4 2.5 - B2 0 > B2.txt 2> B2.err &
P3=$!
wait $P1 $P2 $P3
while [ "$(stat -c %s A_bed_600000.bin 2>/dev/null)" != "131072" ]; do sleep 2; done
nice -n 15 $B 3 0 600000 100000 0 2.5 A_bed_600000.bin C 0 600000 > C.txt 2> C.err &
P4=$!
nice -n 15 $B 3 0 20000 2000 0.4 1 A_bed_600000.bin D 0 600000 > D.txt 2> D.err &
P5=$!
wait $P4 $P5 $PA
echo done > DONE
