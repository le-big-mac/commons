#!/bin/bash
# The monthly files of the years before 2022 and of 2026 that the share's listing shows for the sixteen photometers
# (data/fetch_more.list: station, year, month), for the fourth and fifth sheets. STARS4ALL network, public share,
# Open Database License 1.0. One request every two seconds. Files are data: nothing in them is run.
while read st y m; do
  d=/home/agent1/night/data/ida$y; mkdir -p $d; f=${st}_$y-$m.dat
  [ -s $d/$f ] && continue
  code=$(curl -sS -L -m 300 -A "reading-check/1.0" -o $d/$f.tmp -w '%{http_code}' "https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/$st/$f")
  if [ "$code" = 200 ]; then mv $d/$f.tmp $d/$f; else rm -f $d/$f.tmp; echo "$f http $code"; fi
  sleep 2
done < /home/agent1/night/data/fetch_more.list
echo "fetch done $(date -u +%H:%M:%S)"
