#!/bin/bash
# usage: zb_run.sh PREFIX "search string" ...  -- zbMATH Open document search
set -u
tools=/home/agent3/lean/lift-check/even/print3-tools
prefix="$1"; shift 1
i=0
for q in "$@"; do
  i=$((i+1))
  enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$q")
  "$tools/get.sh" "zb-$prefix-$i" "https://api.zbmath.org/v1/document/_search?search_string=$enc&results_per_page=20" r.json >/dev/null
  echo "QUERY [zbMATH]: $q"
  bash ~/bin/cap2g.sh python3 -I "$tools/zb_show.py" "/home/agent3/lean/lift-check/even/print3/zb-$prefix-$i/r.json"
  sleep 1
done
