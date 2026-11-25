#!/bin/bash
# as run: the change from the other side (start nearly all dove), and one grid line redone with the author's own code
cd /home/agent2/hawk/referee
gcc -O2 -o hd_copy ../hd.c
./ref2 0 4 0.215 200 40000 51 30000 0.15 10000   # 10,000 generations at r = 0.15 first, then r = 0.215
./ref2 0 8 0.115 200 30000 51 20000 0.08 10000   # 10,000 generations at r = 0.08 first, then r = 0.115
./hd_copy lattice4 0.66 200 15000 1066 10000 50 | grep '^R'
