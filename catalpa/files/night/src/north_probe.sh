#!/bin/bash
# Which of the northern photometers never fetched here have monthly files in April and October of 2018 and 2019 on
# the STARS4ALL share: HEAD requests only (no file is fetched, no reading is seen), about three a second.
# Input: data/listing/north_new_candidates.txt (name, latitude, longitude). Output: data/listing/north_new_probe.txt
OUT=/home/agent1/night/data/listing/north_new_probe.txt; : > $OUT
while read -r st lat lon; do
  line="$st $lat $lon:"
  for ym in 2018-04 2018-10 2019-04 2019-10; do
    code=$(curl -s -o /dev/null -I -A "reading-check/1.0" -w "%{http_code}" --max-time 20 "https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/$st/${st}_$ym.dat")
    [ "$code" = "200" ] && line="$line $ym"; /bin/sleep 0.3
  done
  echo "$line" >> $OUT
done < /home/agent1/night/data/listing/north_new_candidates.txt
echo done >> $OUT
