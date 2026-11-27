#!/bin/bash
# usage: ax_run.sh PREFIX "search_query" ...  -- arXiv listing API, one new directory per query
set -u
tools=/home/agent3/lean/lift-check/even/print3-tools
prefix="$1"; shift 1
i=0
for q in "$@"; do
  i=$((i+1))
  enc=$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$q")
  "$tools/get.sh" "ax-$prefix-$i" "http://export.arxiv.org/api/query?search_query=$enc&start=0&max_results=40&sortBy=submittedDate&sortOrder=descending" r.xml >/dev/null
  echo "QUERY [arXiv]: $q"
  bash ~/bin/cap2g.sh python3 -I "$tools/arxiv_show.py" "/home/agent3/lean/lift-check/even/print3/ax-$prefix-$i/r.xml"
  sleep 3
done
