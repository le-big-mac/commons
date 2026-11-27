#!/bin/bash
# Makes data/ida<YEAR>p: links to the monthly files of data/ida<YEAR> whose header gives a position in numbers.
# (amendment-stars.md: a file that does not say where the photometer was is not used.) Usage: with_position.sh 2022 2023
for y in "$@"; do
  src=/home/agent1/night/data/ida$y; dst=/home/agent1/night/data/ida${y}p; mkdir -p $dst
  for f in $src/*.dat; do
    if grep -a -m1 -q '^# Position: -\?[0-9]' "$f"; then ln -sf "$f" "$dst/$(basename $f)"; else echo "left out: $(basename $f) ($(grep -a -m1 '^# Position:' "$f"))"; fi
  done
  echo "$y: $(ls $dst | wc -l) files with a position of $(ls $src/*.dat | wc -l)"
done
