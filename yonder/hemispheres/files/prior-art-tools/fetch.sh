#!/bin/bash
# usage: fetch.sh NAME URL OUTFILE
# Downloads URL into a new, empty directory /home/agent3/downloads/hemi-prior-NAME/ as OUTFILE.
# Refuses to reuse an existing directory. Sends only the user agent "research-script/1.0"
# (no cookies, no referrer, no contact details). Appends one line to the fetch log.
set -u
d="/home/agent3/downloads/hemi-prior-$1"
if [ -e "$d" ]; then echo "exists: $d" >&2; exit 2; fi
mkdir "$d" || exit 2
code=$(curl -sS -L --max-time 120 -A "research-script/1.0" -o "$d/$3" -w "%{http_code} | %{content_type} | %{size_download} bytes | %{url_effective}" "$2")
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | FETCH | $1 | $2 | $code" | tee -a /home/agent3/prior/hemi/fetch-log.txt
