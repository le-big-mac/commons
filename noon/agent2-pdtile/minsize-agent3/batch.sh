#!/bin/bash
# usage: batch.sh N TLIMIT "P Q" "P Q" ...   runs multisets and sets with CP-SAT and multisets with HiGHS for each pair, one pair at a time
set -u
PY=~/welch/.venv/bin/python; n=$1; tl=$2; shift 2
for pq in "$@"; do
  set -- $pq; p=$1; q=$2
  for kind in multi set; do
    f=~/minsize/out/n$n-p$p-q$q-$kind-cpsat.jsonl
    [ -s "$f" ] || $PY ~/minsize/minsize.py $p $q $n $kind --solver cpsat --tlimit $tl > "$f.part" 2> "$f.err" && mv "$f.part" "$f"
  done
  f=~/minsize/out/n$n-p$p-q$q-multi-highs.jsonl
  [ -s "$f" ] || $PY ~/minsize/minsize.py $p $q $n multi --solver highs --tlimit $tl > "$f.part" 2> "$f.err" && mv "$f.part" "$f"
  echo "$(date -u +%H:%M:%S) done n=$n p=$p q=$q" >> ~/minsize/out/batch.log
done
