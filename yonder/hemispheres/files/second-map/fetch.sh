#!/bin/bash
# Fetch seven global population mosaics from WorldPop, one at a time, each into its own new directory.
# usage: fetch.sh    (writes fetch-log.txt beside this script)
set -u
UA="research-script/1.0"; LOG=~/hemi2/fetch-log.txt
get() {   # name url
  d=~/downloads/$1; mkdir -p "$d"
  if [ -n "$(ls -A "$d")" ]; then echo "$(date -u +%FT%TZ) | $1 | directory not empty, skipped" >> $LOG; return; fi
  code=$(curl -s -L -m 3000 -A "$UA" -o "$d/data.tif" -w "%{http_code} %{size_download}" "$2")
  echo "$(date -u +%FT%TZ) | $1 | $2 | $code | sha256 $(sha256sum "$d/data.tif" | cut -c1-64)" >> $LOG
  sleep 3
}
for y in 2015 2020 2025 2030; do
  get wp-g2-$y "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/$y/0_Mosaicked/v1/1km_ua/constrained/global_pop_${y}_CN_1km_R2025A_UA_v1.tif"
done
for y in 2000 2010 2020; do
  get wp-g1-$y "https://data.worldpop.org/GIS/Population/Global_2000_2020/$y/0_Mosaicked/ppp_${y}_1km_Aggregated.tif"
done
echo "$(date -u +%FT%TZ) | done" >> $LOG
