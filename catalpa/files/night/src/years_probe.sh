#!/bin/bash
# Which monthly files the STARS4ALL share holds for the eleven southern photometers in 2019, 2020, 2025 and 2026:
# HEAD requests only (no file is fetched, no reading is seen), three a second at most. Output: data/listing/south_years.txt
OUT=/home/agent1/night/data/listing/south_years.txt; : > $OUT
for st in stars251 stars391 stars722 stars477 stars315 stars221 stars456 stars220 stars215 stars29 stars634; do
  for y in 2019 2020 2025 2026; do
    line="$st $y:"
    for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
      code=$(curl -s -o /dev/null -I -A "reading-check/1.0" -w "%{http_code}" --max-time 20 "https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/$st/${st}_$y-$m.dat")
      [ "$code" = "200" ] && line="$line $m" ; /bin/sleep 0.3
    done
    echo "$line" >> $OUT
  done
done
echo done >> $OUT
