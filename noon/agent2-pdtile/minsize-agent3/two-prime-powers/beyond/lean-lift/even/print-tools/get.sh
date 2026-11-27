#!/bin/bash
# usage: get.sh NAME URL [outfile]   -- downloads URL into a new empty directory print/NAME
set -u
base=/home/agent3/lean/lift-check/even/print
name="$1"; url="$2"; out="${3:-page}"
d="$base/$name"
if [ -e "$d" ]; then echo "exists: $d"; exit 1; fi
mkdir -p "$d"
curl -sS -L --max-time 60 -A "literature-check/1.0" --compressed -o "$d/$out" "$url"
echo "$name: $(stat -c %s "$d/$out" 2>/dev/null) bytes"
