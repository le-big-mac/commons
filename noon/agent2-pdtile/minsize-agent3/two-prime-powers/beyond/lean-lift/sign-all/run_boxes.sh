#!/bin/bash
# run_boxes.sh stream  -- the box tests of tree_box.py, in three streams (a, b, c); writes tbx_<stream>.out here.
cd "$(dirname "$0")" || exit 1
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
case "$1" in
a) : > tbx_a.out
   $PY tree_box.py 3 2 3 1 5 800 7 3 >> tbx_a.out 2>&1; $PY tree_box.py 3 2 3 1 0 800 7 3 >> tbx_a.out 2>&1
   $PY tree_box.py 3 2 5 1 7 800 7 5 >> tbx_a.out 2>&1; $PY tree_box.py 3 2 5 1 0 800 7 5 >> tbx_a.out 2>&1
   $PY tree_box.py 3 2 3 2 5 800 7 6 >> tbx_a.out 2>&1 ;;
b) : > tbx_b.out
   $PY tree_box.py 3 3 5 1 7 800 7 5 >> tbx_b.out 2>&1; $PY tree_box.py 3 3 7 1 5 800 7 6 >> tbx_b.out 2>&1
   $PY tree_box.py 3 3 5 2 7 800 7 6 >> tbx_b.out 2>&1; $PY tree_box.py 3 3 3 2 5 800 7 6 >> tbx_b.out 2>&1 ;;
c) : > tbx_c.out
   $PY tree_box.py 5 2 3 2 7 800 7 6 >> tbx_c.out 2>&1; $PY tree_box.py 5 2 3 3 7 800 7 6 >> tbx_c.out 2>&1
   $PY tree_box.py 7 1 3 3 5 800 7 6 >> tbx_c.out 2>&1; $PY tree_box.py 5 3 3 3 7 600 7 6 >> tbx_c.out 2>&1 ;;
esac
