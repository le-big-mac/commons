#!/bin/bash
# usage: oeis_run.sh PREFIX "query" ...  -- OEIS search, json
set -u
tools=/home/agent3/lean/lift-check/even/print3-tools
prefix="$1"; shift 1
i=0
for q in "$@"; do
  i=$((i+1))
  enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$q")
  "$tools/get.sh" "oeis-$prefix-$i" "https://oeis.org/search?q=$enc&fmt=json" r.json >/dev/null
  echo "QUERY [OEIS]: $q"
  bash ~/bin/cap2g.sh python3 -I "$tools/oeis_show.py" "/home/agent3/lean/lift-check/even/print3/oeis-$prefix-$i/r.json"
  sleep 1
done
