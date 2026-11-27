#!/bin/bash
# The monthly files of 2022 and 2023 (a third and fourth year, for the sheet expectations-stars.md) of the same sixteen
# STARS4ALL photometers, from the network's public share (ODbL 1.0). One request every two seconds.
# Files are data: nothing in them is run. Usage: fetch_ida_years.sh 2022 2023
for y in "$@"; do
  mkdir -p /home/agent1/night/data/ida$y; cd /home/agent1/night/data/ida$y || exit 1
  for st in stars1 stars4 stars7 stars9 stars19 stars24 stars33 stars35 stars36 stars52 stars62 stars76 stars225 stars289 stars426 stars477; do
    for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
      f=${st}_$y-$m.dat
      [ -s $f ] && continue
      code=$(curl -sS -L -m 300 -A "reading-check/1.0" -o $f.tmp -w '%{http_code}' "https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/$st/$f")
      if [ "$code" = 200 ]; then mv $f.tmp $f; else rm -f $f.tmp; echo "$f http $code"; fi
      sleep 2
    done
  done
  echo "fetch of $y done $(date -u +%H:%M:%S)"
done
