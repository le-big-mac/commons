#!/bin/bash
# October profiles (temperature, salinity, pressure, and the depth-averaged current of each dive) from every Spray glider deployment off southern California, 2014-2026.
# Source: IOOS Glider DAC ERDDAP (gliders.ioos.us), deployments listed by glider/deployments.json (from the server's own search by box and time).
cd ~/tides/glider; mkdir -p oct
python3 -c "
import json
d = json.load(open('deployments.json'))
for y, ids in d.items():
    for i in ids:
        if i.startswith('sp'): print(y, i)
" | while read y id; do
  f=oct/${y}_${id}.csv; [ -s "$f" ] && continue
  for try in 1 2 3; do
    curl -sS -g -m 600 -A "tide-check/1.0" "https://gliders.ioos.us/erddap/tabledap/${id}.csv?profile_id,time,latitude,longitude,pressure,temperature,salinity,u,v&time>=${y}-10-01T00:00:00Z&time<${y}-11-01T00:00:00Z" -o "$f.tmp" 2>>fetch.log
    if head -1 "$f.tmp" | grep -q '^profile_id'; then mv "$f.tmp" "$f"; break; else echo "$(date -u +%T) $y $id try $try: $(head -c 120 "$f.tmp" | tr '\n' ' ')" >> fetch.log; rm -f "$f.tmp"; sleep 10; fi
  done
  echo "$(date -u +%T) $y $id $( [ -f "$f" ] && wc -l < "$f" || echo FAILED)" >> fetch.log; sleep 1.5
done
echo "$(date -u +%T) done" >> fetch.log
