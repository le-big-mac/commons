#!/bin/bash
# second, larger round of the exhaustive tests of the level bound; three processes at a time, 2 GB cap each
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { $PY test_levels.py "$@" > "levels2_$1_$6_$5.out" 2>&1; }
run 225 9 15 400 21 full &  run 675 9 15 300 22 full &  run 315 7 15 400 23 full & wait
run 945 7 14 200 24 full &  run 1575 9 14 150 25 full &  run 135 7 15 400 28 full & wait
run 4725 9 14 80 26 full &  run 2025 9 14 100 27 full &  run 405 9 15 300 29 full & wait
run 81 9 15 300 30 full &  run 243 11 15 200 31 full &  run 1125 13 15 80 33 full & wait
run 3375 13 14 40 32 full &  run 11025 13 14 40 34 full &  run 3465 11 13 60 37 full & wait
run 45 5 15 400 35 mixed &  run 675 4 14 300 36 mixed &  run 315 4 14 300 38 coset & wait
