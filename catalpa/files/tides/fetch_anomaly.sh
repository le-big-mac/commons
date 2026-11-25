#!/bin/bash
# The data behind anomaly.py, analogues.py, neighbours.py: six-minute levels and predictions from 15 Sep 2026 at five more West Coast gauges,
# NOAA's monthly mean sea levels (whole record) at four, and NOAA CPC's table of the Oceanic Nino Index.
cd ~/tides/data
for st in 9410170 9447130 9432780 9410230 9410660; do ../fetch.sh $st 20260915 3 $1; done
for st in 9410170 9447130 9432780 9414290; do
  curl -s -A "tide-check/1.0" "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=monthly_mean&application=tide-check&begin_date=18500101&end_date=$(date -u +%Y%m%d)&datum=MSL&station=${st}&time_zone=gmt&units=metric&format=csv" -o "${st}_monthly_mean.csv"; sleep 0.4
done
curl -s -A "tide-check/1.0" "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt" -o oni.ascii.txt
curl -s -A "tide-check/1.0" "https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt" -o roni.ascii.txt      # the relative index (the region against the whole tropics)
