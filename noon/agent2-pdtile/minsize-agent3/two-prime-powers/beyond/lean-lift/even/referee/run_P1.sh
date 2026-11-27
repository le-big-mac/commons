#!/bin/bash
# P_1 on Z_2 .. Z_32 and more Lemma V/Q runs; at most three at a time, 290 s each, 2 GB cap.
cd "$(dirname "$0")"
PY="$HOME/welch/.venv/bin/python"
cat <<LIST | xargs -P 3 -L 1 bash -c 'name="$1"; shift; timeout 290 bash ~/bin/cap2g.sh '"$PY"' "$@" > "$name" 2>&1; echo "exit $?" >> "$name"' _
tP1_2.out tP1.py 2 4 6 8 10 12 14 16 18
tP1_4.out tP1.py 4 4 6 8 10 12
tP1_8.out tP1.py 8 4 6 8
tP1_8_10.out tP1.py 8 10
tP1_16.out tP1.py 16 4 6
tP1_16_8.out tP1.py 16 8
tP1_32.out tP1.py 32 4
tP1_32_6.out tP1.py 32 6
tVQ_1.out tVQ.py 1 20000
tVQ_2.out tVQ.py 2 20000
LIST
