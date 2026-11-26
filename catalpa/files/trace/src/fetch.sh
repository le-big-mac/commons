#!/bin/bash
# Fetch UHSLC fast-delivery daily sea level files for a chain of gauges.
# Usage: fetch.sh ; files go to ~/trace/data/d<id>.csv . Downloaded files are data only.
cd ~/trace/data || exit 1
for id in 093 084 092 091 030 003 392 302 087 082 316 395 034 317 569 554 545 551 556 592 558 542 540 571; do
  f=d$id.csv
  code=$(curl -sS -L -m 120 -A "reading-check/1.0" -o $f.tmp -w '%{http_code}' "https://uhslc.soest.hawaii.edu/data/csv/fast/daily/d$id.csv")
  if [ "$code" = 200 ]; then mv $f.tmp $f; else rm -f $f.tmp; fi
  echo "$id $code $(wc -c < $f 2>/dev/null)"
  sleep 1
done
