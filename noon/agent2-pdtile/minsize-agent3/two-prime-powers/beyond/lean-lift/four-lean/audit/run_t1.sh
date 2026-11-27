#!/bin/bash
# The parts S0 .. S5 on families with every signing: the batches, one after the other (one process at a time).
# usage: bash run_t1.sh
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t1_parts.py"
$P 11 2500 12 > t1_parts_s11.out 2>&1
$P 12 6000 10 > t1_parts_s12.out 2>&1
$P 23 400 14 > t1_parts_s23.out 2>&1
$P 24 1500 14 0.85 > t1_parts_s24_caterpillars.out 2>&1
$P 25 2000 12 0.3 > t1_parts_s25_cosets.out 2>&1
