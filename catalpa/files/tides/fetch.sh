#!/bin/bash
# NOAA CO-OPS public API: six-minute observed water levels (MSL, metres, GMT) in 31-day pieces, and NOAA's own predictions
# usage: fetch.sh <station> <first day YYYYMMDD> <number of 30-day pieces>
st=$1; d0=$2; n=$3; cd ~/tides/data
for i in $(seq 0 $((n-1))); do
  b=$(date -u -d "$d0 + $((i*30)) days" +%Y%m%d); e=$(date -u -d "$d0 + $((i*30+29)) days" +%Y%m%d)
  for prod in water_level predictions; do
    f="${st}_${prod}_${b}.csv"; [ -s "$f" ] && [ "$4" != "force" ] && continue
    curl -s -A "tide-check/1.0" "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=${prod}&application=tide-check&begin_date=${b}&end_date=${e}&datum=MSL&station=${st}&time_zone=gmt&units=metric&interval=6&format=csv" -o "$f"; sleep 0.4
  done
done
