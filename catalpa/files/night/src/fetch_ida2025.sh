#!/bin/bash
# The 2025 monthly files (a second year, for the replication) of sixteen STARS4ALL photometers, from the network's public share (ODbL 1.0).
# Stations chosen by rule from the share's own listing (see expectations.md): TESS-W, 150 MB or more on the share,
# coordinates in geolist.csv, latitude between 25 and 46 degrees north or south, one per site.
# One request every two seconds. Files are data: nothing in them is run.
cd /home/agent1/night/data/ida2025 || exit 1
for st in stars1 stars4 stars7 stars9 stars19 stars24 stars33 stars35 stars36 stars52 stars62 stars76 stars225 stars289 stars426 stars477; do
  for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
    f=${st}_2025-$m.dat
    [ -s $f ] && continue
    code=$(curl -sS -L -m 300 -A "reading-check/1.0" -o $f.tmp -w '%{http_code}' "https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/$st/$f")
    if [ "$code" = 200 ]; then mv $f.tmp $f; else rm -f $f.tmp; echo "$f http $code"; fi
    sleep 2
  done
done
echo "fetch done $(date -u +%H:%M:%S)"
