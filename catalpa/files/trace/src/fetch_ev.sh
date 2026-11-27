#!/bin/bash
# NOAA's verified hourly heights round each of the eighteen quick rises of rises.out: day D - 30 to D + 25,
# eleven gauges from San Diego to Crescent City. Station datum, metres, UTC. One request a second.
cd /home/agent1/trace/data/coops/ev || exit 1
for D in $(grep -oE '^  (19|20)[0-9]{2}-[0-9]{2}-[0-9]{2}' /home/agent1/trace/rises.out | tr -d ' ' | sort -u); do
  b=$(date -u -d "$D -30 days" +%Y%m%d); e=$(date -u -d "$D +25 days" +%Y%m%d)
  for sid in 9410170 9410230 9410660 9411340 9412110 9413450 9414290 9415020 9416841 9418767 9419750; do
    f=h${sid}_$D.csv
    [ -s $f ] && continue
    code=$(curl -sS -L -m 120 -A "reading-check/1.0" -o $f.tmp -w '%{http_code}' "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=$b&end_date=$e&station=$sid&product=hourly_height&datum=STND&units=metric&time_zone=gmt&application=reading-check&format=csv")
    if [ "$code" = 200 ]; then mv $f.tmp $f; else rm -f $f.tmp; echo "$sid $D http $code"; fi
    sleep 1
  done
done
echo "fetch done $(date -u +%H:%M:%S)"
