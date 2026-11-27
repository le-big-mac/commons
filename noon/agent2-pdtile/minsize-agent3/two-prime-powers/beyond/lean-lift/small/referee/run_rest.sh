#!/bin/bash
# one stream: the remaining small checks, then multisets of 15..36 elements (run_thmS_large.sh)
cd /home/agent3/lean/lift-check/small/referee
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
timeout 590 $PY ref_gamma_variants.py 7 40 > ref_gamma_variants.out 2>&1
timeout 590 $PY ref_lemma4.py 3 20000 > ref_lemma4.out 2>&1
for N in 3 5 7; do timeout 590 $PY ref_lemma2.py exh $N 6 > lemma2_exh_${N}_6.out 2>&1; echo "exit status $? ; seconds $SECONDS" >> lemma2_exh_${N}_6.out; done
timeout 590 $PY summarize_lemma2.py > lemma2_exh_summary.out 2>&1
bash run_thmS_large.sh
