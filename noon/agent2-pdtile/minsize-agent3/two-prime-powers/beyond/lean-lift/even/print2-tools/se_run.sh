#!/bin/bash
# usage: se_run.sh SITE PREFIX "query" ...  -- excerpt search on a Stack Exchange site, one new directory per query
set -u
tools=/home/agent3/lean/lift-check/even/print2-tools
site="$1"; prefix="$2"; shift 2
i=0
for q in "$@"; do
  i=$((i+1))
  enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$q")
  "$tools/get.sh" "se-$prefix-$i" "https://api.stackexchange.com/2.3/search/excerpts?order=desc&sort=relevance&q=$enc&site=$site&pagesize=12" r.json >/dev/null
  echo "QUERY [$site]: $q"
  python3 -I "$tools/se_show.py" "/home/agent3/lean/lift-check/even/print2/se-$prefix-$i/r.json"
  sleep 1
done
