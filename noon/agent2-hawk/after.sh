#!/bin/bash
# Checks made after the sealed lines were scored.   usage: bash after.sh   (twelve at a time; about ten minutes)
cd "$(dirname "$0")"
{
 for r in 0.190 0.195 0.200 0.201 0.205 0.210; do echo "A lattice4 $r 200 15000 7 10000 50 0.5"; done
 for r in 0.100 0.105 0.110 0.112 0.115 0.120; do echo "A lattice8 $r 200 15000 7 10000 50 0.5"; done
 for r in 0.15 0.22 0.24 0.26 0.30; do echo "B lattice4 $r 200 15000 8 10000 50 0.99"; done
 for r in 0.10 0.20; do echo "C lattice4 $r 200 60000 9 55000 50 0.5"; done
 for sd in 11 12 13; do for r in 0.60 0.62 0.64 0.66 0.68 0.70 0.72 0.74 0.76; do echo "D$sd lattice4 $r 200 30000 $sd 25000 50 0.5"; done; done
 for r in 0.30 0.50 0.64; do echo "E lattice4 $r 400 15000 10 10000 50 0.5"; done
 for r in 0.22 0.30 0.50 0.64; do echo "F lattice4 $r 200 15000 21 10000 50 0.5"; echo "F lattice4 $r 200 15000 22 10000 50 0.5"; done
} > after-grid.txt
cat after-grid.txt | xargs -P 12 -L 1 bash -c 'HD_P0=$8 ./hd $1 $2 $3 $4 $5 $6 $7 > after/$0-$1-$2-L$3-s$5.out'
for f in after/*.out; do echo "$(basename $f .out) $(grep '^R' $f)"; done > after-results.txt; wc -l after-results.txt
