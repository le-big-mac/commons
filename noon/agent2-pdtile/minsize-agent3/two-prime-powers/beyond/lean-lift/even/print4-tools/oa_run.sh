#!/bin/bash
# usage: oa_run.sh PREFIX "search words" ...  -- OpenAlex works search, one new directory per query
set -u
tools=/home/agent3/lean/lift-check/even/print4-tools
prefix="$1"; shift 1
i=0
for q in "$@"; do
  i=$((i+1))
  enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$q")
  "$tools/get.sh" "oa-$prefix-$i" "https://api.openalex.org/works?search=$enc&per-page=15" r.json >/dev/null
  echo "QUERY [OpenAlex]: $q"
  bash ~/bin/cap2g.sh python3 -I "$tools/oa_show.py" "/home/agent3/lean/lift-check/even/print4/oa-$prefix-$i/r.json"
  sleep 1
done
