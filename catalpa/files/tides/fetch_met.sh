#!/bin/bash
# Hourly air pressure and water temperature for every October on file at a gauge (NOAA CO-OPS API). usage: fetch_met.sh <station> <first year>
st=$1; cd ~/tides/data
for y in $(seq $2 2026); do
  for prod in air_pressure water_temperature; do
    f="${st}_${prod}_${y}10.csv"; [ -s "$f" ] && continue
    curl -s -A "tide-check/1.0" "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=${prod}&application=tide-check&begin_date=${y}1001&end_date=${y}1031&station=${st}&time_zone=gmt&units=metric&interval=h&format=csv" -o "$f"; sleep 0.3
  done
done
