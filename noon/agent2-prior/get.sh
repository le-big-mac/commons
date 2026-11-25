#!/bin/sh
# usage: get.sh LINE NAME URL     saves the page or PDF into ~/prior-data/LINE/NAME/ and prints the size of its text
d=$HOME/prior-data/$1/$2; mkdir -p "$d"; cd "$d" || exit 1
code=$(curl -sS -L --max-time 60 -A "research-script/1.0" -o raw "$3" -w "%{http_code}"); kind=$(file -b raw | cut -c1-40)
case "$kind" in PDF*) pdftotext raw text.txt 2>/dev/null;; *) "$HOME/vuza/.venv/bin/python" -I "$HOME/kit/html2text.py" raw > text.txt 2>/dev/null;; esac
echo "$3" > url.txt; echo "$code $kind; text: $(wc -c < text.txt) characters in $d/text.txt"
