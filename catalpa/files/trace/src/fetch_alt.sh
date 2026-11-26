#!/bin/bash
# Fetch the altimetry boxes listed in the file given as $1 (name and URL on each line), one at a time with a pause;
# skips files already there. The West Coast server (pfeg) holds the data to 28 September 2026 and answers long
# requests; the origin server holds it to 25 November and gave "502 Proxy Error" on requests of 200 days.
cd ~/trace/data/alt || exit 1
while read -r name url; do
  [ -s "$name" ] && continue
  for try in 1 2 3; do
    code=$(curl -sS -g -m 120 -A "reading-check/1.0" -o "$name.tmp" -w '%{http_code}' "$url")
    if [ "$code" = 200 ]; then mv "$name.tmp" "$name"; break; fi
    rm -f "$name.tmp"; echo "$(date -u +%H:%M:%S) $name $code try $try"; sleep 20
  done
  sleep 2
done < "$1"
echo "$(date -u +%H:%M:%S) done $1"
