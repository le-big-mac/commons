#!/bin/bash
# balanced ("interval") shapes: all signings for 14 to 18 elements, sampled signings for 37 to 50 elements;
# three processes at a time, each under the 2 GB cap
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
ev() { $PY even_exact.py "$@" > "even_$1_$2_$5.out" 2>&1; }
run() { $PY test_big.py run "$@" > "big_$1_$2_$5.out" 2>&1; }
ev 45045 14 6 1 interval &  ev 45045 16 3 2 interval &  ev 675 16 6 3 interval & wait
ev 675 18 4 4 interval &  ev 4725 16 4 5 interval &  ev 315 18 4 6 interval & wait
ev 675 16 6 7 full &  ev 3465 16 3 8 interval &  ev 1575 18 2 9 interval & wait
run 37 intervalperm 8 21 31 &  run 38 intervalperm 8 21 32 &  run 40 intervalperm 8 21 33 & wait
run 44 intervalperm 6 21 34 &  run 50 intervalperm 4 21 35 &  run 41 interval 1 41 36 & wait
run 37 interval 1 41 37 &  run 38 interval 1 41 38 &  run 49 interval 1 41 39 & wait
