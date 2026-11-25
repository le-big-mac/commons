#!/bin/bash
# Make an issue every day at 18:05 UTC until the end date.  Start detached:  nohup setsid ~/tides/daily_loop.sh >> ~/tides/issues/loop.log 2>&1 &
# Safe to start again: only one copy runs (lock), and a day that already has an issue is skipped.
exec 9> ~/tides/issues/.lock; flock -n 9 || { echo "$(date -u +%FT%TZ) another loop holds the lock"; exit 0; }
END=$(date -u -d "2026-12-10 00:00" +%s)
while [ $(date -u +%s) -lt $END ]; do
  now=$(date -u +%s); next=$(date -u -d "$(date -u +%F) 18:05" +%s); [ $now -ge $((next + 3300)) ] && next=$((next + 86400))
  [ $now -lt $next ] && sleep $((next - now))
  for try in 1 2 3 4 5; do ~/tides/daily.sh; rc=$?; [ $rc -eq 0 ] && break; sleep 600; done
  sleep 3400
done
