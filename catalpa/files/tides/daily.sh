#!/bin/bash
# One day's issue: fetch the latest observations (to a temporary file first, kept only if it looks whole), make the forecast, log its hashes, copy to the commons.
# usage: daily.sh            make today's issue (skipped if today's already exists)
#        daily.sh fetchonly  only refresh the observations (before scoring)
#        daily.sh test       everything but the issue itself: forecast to /tmp/issue_dry, nothing logged or copied
cd ~/tides || exit 1; PY=~/ipd/.venv/bin/python; id=$(date -u +%Y%m%d)
fetch_all() {
  for st in 9414290 8518750 1612340; do
    for b in 20261114 20261214; do
      e=$(date -u -d "$b + 29 days" +%Y%m%d)
      for prod in water_level predictions; do
        tmp=$(mktemp); curl -s -m 120 -A "tide-check/1.0" "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=${prod}&application=tide-check&begin_date=${b}&end_date=${e}&datum=MSL&station=${st}&time_zone=gmt&units=metric&interval=6&format=csv" -o "$tmp"
        f="data/${st}_${prod}_${b}.csv"; old=$(grep -c '^20' "$f" 2>/dev/null); old=${old:-0}; new=$(grep -c '^20' "$tmp"); new=${new:-0}
        if [ "$new" -gt 100 ] && [ "$new" -ge $((old - 50)) ]; then mv "$tmp" "$f"; else rm -f "$tmp"; [ "$b" = 20261114 ] && echo "$(date -u +%FT%TZ) kept old $f ($old rows; new had $new)"; fi
        sleep 0.4
      done
    done
  done
}
fetch_all
[ "$1" = fetchonly ] && exit 0
ls -d issues/${id}T* >/dev/null 2>&1 && { echo "$(date -u +%FT%TZ) issue for $id exists; nothing to do"; exit 0; }
# the newest observation must be less than 90 minutes old at every station, or the issue is not made (the loop tries again)
for st in 9414290 8518750 1612340; do
  last=$(grep '^20' data/${st}_water_level_20261114.csv | awk -F, '$2+0==$2 && $2!=""' | tail -1 | cut -d, -f1)
  age=$(( $(date -u +%s) - $(date -u -d "$last" +%s) )); [ "$age" -gt 5400 ] && { echo "$(date -u +%FT%TZ) $st newest observation $last is $age s old; no issue"; exit 2; }
done
[ "$1" = test ] && { $PY -I issue.py /tmp/issue_dry | cut -c1-150; echo "test only: nothing logged or copied"; exit 0; }
out=issues/${id}T$(date -u +%H%M); $PY -I issue.py $out > /dev/null || exit 3
{ echo "issue $(basename $out) made $(date -u +%FT%TZ)"; (cd $out && sha256sum forecast_*.csv meta.txt); } >> issues/LOG
mkdir -p /srv/commons/tides-agent1/issues && cp -r $out /srv/commons/tides-agent1/issues/ && cp issues/LOG /srv/commons/tides-agent1/issues/LOG
echo "$(date -u +%FT%TZ) issued $out"
