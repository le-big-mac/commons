#!/bin/bash
# Run lag over a file of openings in ten interleaved parts.   usage: par.sh NAME OPENINGS n k d Q mode [options]
name=$1; file=$2; shift 2
mkdir -p out/parts; rm -f out/parts/$name.*
split -n r/10 -d "$file" out/parts/$name.in.
for i in 0 1 2 3 4 5 6 7 8 9; do nice -n 15 ${PROG:-./lag} "$@" < out/parts/$name.in.0$i > out/parts/$name.out.0$i 2>&1 & done
wait
cat out/parts/$name.out.0? > out/$name.out
echo "$name: $(grep -c '^yes' out/$name.out) openings work, $(grep -c '^no' out/$name.out) do not, of $(wc -l < "$file")"
