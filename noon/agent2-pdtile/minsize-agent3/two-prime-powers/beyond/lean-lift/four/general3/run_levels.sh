#!/bin/bash
# exhaustive tests of the level bound and the union bound; at most three processes at a time, each under the 2 GB cap
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { $PY test_levels.py "$@" > "levels_$1_$6_$5.out" 2>&1; }
run 9 2 9 300 1 mixed &  run 45 2 10 300 2 mixed &  run 27 3 10 200 3 mixed & wait
run 81 9 12 150 4 full &  run 225 9 13 200 5 full &  run 135 7 13 200 6 full & wait
run 315 7 13 200 7 full &  run 675 9 13 150 8 full &  run 405 9 13 150 9 full & wait
run 945 7 13 120 10 full &  run 1575 9 13 80 11 full &  run 105 7 13 200 12 mixed & wait
run 225 4 13 200 13 mixed &  run 315 4 13 200 14 mixed &  run 675 4 13 150 15 coset & wait
run 2025 9 13 60 16 full &  run 4725 9 13 40 17 full &  run 1155 11 13 60 18 mixed & wait
