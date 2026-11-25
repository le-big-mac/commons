#!/bin/bash
# The referee's controls, redone.   usage: bash after2.sh   (ten at a time; about five minutes)
cd "$(dirname "$0")"
{
 echo "a4 lattice4 0.205 200 100000 31 95000 50 0.5 -"; echo "a4 lattice4 0.210 200 100000 31 95000 50 0.5 -"; echo "a4 lattice4 0.215 200 60000 31 55000 50 0.5 -"; echo "a4dove lattice4 0.215 200 40000 32 35000 50 0.995 -"
 echo "a8 lattice8 0.110 200 60000 33 55000 50 0.5 -"; echo "a8 lattice8 0.112 200 60000 33 55000 50 0.5 -"; echo "a8dove lattice8 0.115 200 30000 34 25000 50 0.99 -"
 echo "d lattice4 0.67 200 60000 41 55000 50 0.5 -"; echo "d lattice4 0.67 200 60000 42 55000 50 0.5 -"; echo "d lattice4 0.66 200 100000 43 95000 50 0.5 -"; echo "d8 lattice8 0.77 200 30000 44 25000 50 0.5 -"
 for r in 0.10 0.15 0.20; do echo "p lattice4 $r 200 15000 51 10000 50 0.5 snap"; done
} > after2-grid.txt
cat after2-grid.txt | xargs -P 10 -L 1 bash -c 'if [ "$9" = snap ]; then HD_P0=$8 HD_SNAPLIST=snap15000.txt ./hd $1 $2 $3 $4 $5 $6 $7 after2/$0-$1-$2-s$5.bin 1 > after2/$0-$1-$2-s$5.out; else HD_P0=$8 ./hd $1 $2 $3 $4 $5 $6 $7 > after2/$0-$1-$2-s$5.out; fi'
ls after2 | wc -l
