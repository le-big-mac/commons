#!/bin/bash
# Reruns the box computations quoted in the result file and keeps their summaries (one process at a time).
cd "$(dirname "$0")"
run() { bash ~/bin/cap2g.sh "$@" | grep -vE "^size" ; }
{
for a in "3 3 -- 9" "3 5 -- 15" "3 4 -- 12" "4 4 -- 16" "3 7 -- 11" "3 3 3 -- 8" "3 3 4 -- 7" "3 3 3 3 -- 5" "3 5 7 -- 5"; do run ./grid128 $a; done
} > grid_runs.out 2>&1
{
echo "== pairing by one element, by a flip set (grid_pair2)"
for a in "3 3 -- 9" "3 5 -- 15" "3 3 3 -- 7" "3 3 5 -- 6"; do run ./grid_pair2 $a | grep -vE "some x fail" | head -12; done
echo "== good signing of product form (grid_prod)"
for a in "3 3 -- 9" "3 5 -- 15" "3 3 3 -- 7" "3 3 5 -- 6"; do run ./grid_prod $a | grep -E "product form|NO PRODUCT|^box"; done
echo "== every coset of the pattern group (grid_coset)"
for a in "3 3 -- 9" "3 5 -- 9" "3 3 3 -- 6"; do run ./grid_coset $a | grep -E "coset|COSET|^box"; done
} > grid_variants.out 2>&1
