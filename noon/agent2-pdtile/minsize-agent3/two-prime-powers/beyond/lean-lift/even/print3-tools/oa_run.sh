#!/bin/bash
# usage: oa_run.sh PREFIX "param-string" ...  -- OpenAlex works listing; param-string is e.g. search=... or filter=cites:W...
set -u
tools=/home/agent3/lean/lift-check/even/print3-tools
prefix="$1"; shift 1
i=0
for q in "$@"; do
  i=$((i+1))
  key="${q%%=*}"; val="${q#*=}"
  enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$val")
  "$tools/get.sh" "oa-$prefix-$i" "https://api.openalex.org/works?$key=$enc&per-page=50" r.json >/dev/null
  echo "QUERY [OpenAlex]: $q"
  bash ~/bin/cap2g.sh python3 -I "$tools/oa_show.py" "/home/agent3/lean/lift-check/even/print3/oa-$prefix-$i/r.json"
  sleep 1
done
