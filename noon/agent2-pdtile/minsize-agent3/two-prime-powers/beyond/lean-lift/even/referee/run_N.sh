#!/bin/bash
# Lemma N / Corollary N runs: at most three at a time, each under the 2 GB cap and a 290 s limit.
cd "$(dirname "$0")"
PY="$HOME/welch/.venv/bin/python"
jobs_list() {
cat <<LIST
exh 6 4
exh 6 6
exh 6 8
exh 6 3
exh 6 5
exh 6 7
exh 12 3
exh 12 4
exh 12 5
exh 12 6
exh 12 7
exh 14 4
exh 14 6
exh 14 8
exh 18 3
exh 18 4
exh 18 5
exh 18 6
exh 24 4
exh 24 5
exh 24 6
exh 28 4
exh 28 6
exh 30 3
exh 30 4
exh 30 5
exh 30 6
exh 36 4
exh 36 5
exh 42 4
exh 42 5
exh 56 4
exh 60 3
exh 60 4
exh 62 4
exh 90 4
exh 120 4
rand 1 20000
rand 2 20000
rand 3 20000
rand 4 12000 146 292 62 124 170 102 210 126
LIST
}
jobs_list | xargs -P 3 -L 1 bash -c 'name="tN_$(echo "$@" | tr " " "_").out"; timeout 290 bash ~/bin/cap2g.sh '"$PY"' tN.py "$@" > "$name" 2>&1; echo "exit $?" >> "$name"' _
