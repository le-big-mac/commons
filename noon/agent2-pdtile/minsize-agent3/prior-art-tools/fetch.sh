#!/bin/bash
# usage: fetch.sh NAME URL OUTFILE [PAUSE_SECONDS]
#   -> /home/agent3/downloads/minsize-NAME/OUTFILE  (a new, empty directory holding one file)
# One request, fixed user agent, no cookies, no referrer; then a pause (default 3 s) so that calls
# made one after another stay under one request every three seconds.
set -u
name="$1"; url="$2"; out="$3"; pause="${4:-3}"
d="/home/agent3/downloads/minsize-$name"
log="/home/agent3/prior/minsize/fetch-log.txt"
if [ -e "$d" ]; then echo "EXISTS $d"; exit 2; fi
mkdir "$d" || exit 3
code=$(curl -sS -L --max-time 120 -A "research-script/1.0" -o "$d/$out" \
       -w '%{http_code} %{content_type} %{size_download} %{url_effective}' "$url")
echo "$(date -u +%FT%TZ) $name $url -> $d/$out : $code" | tee -a "$log"
sleep "$pause"
