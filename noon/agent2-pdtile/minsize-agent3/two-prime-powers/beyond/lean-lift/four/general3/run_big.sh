#!/bin/bash
# end-to-end tests on large groups (exact); at most three processes at a time, each under the 2 GB cap
# usage: run_big.sh [first|second|all]   (first: the three lines on n'_m shapes; second: the rest)
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { $PY test_big.py run "$@" > "big_$1_$2_$5.out" 2>&1; }
what="${1:-all}"
if [ "$what" = first ] || [ "$what" = all ]; then
run 37 full 20 51 1 &  run 38 full 20 51 2 &  run 40 full 20 51 3 & wait
run 37 small 20 51 4 &  run 38 small 20 51 5 &  run 48 small 20 51 6 & wait
run 37 coset 20 51 7 &  run 38 coset 20 51 8 &  run 50 coset 20 51 11 & wait
fi
if [ "$what" = second ] || [ "$what" = all ]; then
run 38 pair 20 101 21 &  run 40 pair5 20 101 22 &  run 39 triple 20 101 23 & wait
run 60 small 10 51 10 &  run 45 full 8 21 12 &  run 45 quint 20 101 24 & wait
run 60 full 2 9 9 &  run 54 triple 20 101 25 &  run 37 pair 20 101 26 & wait
fi
