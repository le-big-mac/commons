#!/bin/bash
cd "$(dirname "$0")"
PY="$HOME/welch/.venv/bin/python"
cat <<LIST | xargs -P 3 -L 1 bash -c 'name="tS0_$(echo "$@" | tr " " "_").out"; timeout 290 bash ~/bin/cap2g.sh '"$PY"' tS0.py "$@" > "$name" 2>&1; echo "exit $?" >> "$name"' _
exh 6 6
exh 12 4
exh 12 6
exh 14 4
exh 14 6
exh 24 4
exh 24 5
exh 28 4
exh 30 4
exh 30 5
exh 36 4
exh 60 4
exh 56 4
rand 2 15000
rand 3 15000
LIST
