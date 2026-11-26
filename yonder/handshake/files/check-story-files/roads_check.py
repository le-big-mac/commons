"""How does the machine get into a bed of defectors? A rerun of the study's own tracing (src/roads2.py: its function and its seeds)
for beds of 100 at 2% and 5% slips, 10 runs of 200,000 generations each: every journey from an all-defect majority to a majority
of the three-state machine (any entry state), and what majorities the bed passed through on the way.
usage: WELCH_LOGCAP=1000000 roads_check.py     (with the default cap of 60 logged changes only 3 journeys are seen: roads_check_capped.out; imports /srv/commons/welch/src/roads2.py and evolve.py; writes nothing but its printout)"""
import sys
sys.path.insert(0, '/srv/commons/welch/src')
from collections import Counter
from multiprocessing import Pool
import statistics
from roads2 import one, jobs
import os
CAP = int(os.environ.get('WELCH_LOGCAP', '60'))     # evolve.py reads the same variable; run this with WELCH_LOGCAP=1000000 to see every journey
todo = [j for j in jobs if j[4] == 100]
if __name__ == '__main__':
    with Pool(14) as p: res = p.map(one, todo, chunksize=1)
    FAM = {"0:D[0,1] 1:D[0,2] 2:C[2,0]", "0:D[1,2] 1:D[1,0] 2:C[2,1]", "0:C[0,1] 1:D[1,2] 2:D[1,0]"}
    N_ = {"0:D[0,0]": "alld", "0:D[1,0] 1:C[0,0]": "echo", "0:C[0,1] 1:D[0,1]": "tft", "0:C[0,1] 1:D[1,1]": "grim", "0:C[0,0]": "allc"}
    body = lambda d: d[d.index("0:"):-1] if "0:" in d else d
    for cond in sorted({(r[0], r[1]) for r in res}):
        first = Counter(); via = Counter(); lens = []; n = 0; runs = 0; capped = 0
        for e, N, log in res:
            if (e, N) != cond: continue
            runs += 1; capped += len(log) >= CAP
            seq = ["alld"] + [N_.get(body(d), "FAM" if body(d) in FAM else "x") for g, d in log]
            last = 0
            for i, x in enumerate(seq):
                if x == "alld": last = i
                elif x == "FAM" and last is not None:
                    path = seq[last + 1:i]; n += 1
                    first[path[0] if path else "(direct: no other majority between)"] += 1
                    via["echo"] += "echo" in path; via["tft or grim"] += ("tft" in path or "grim" in path); via["allc"] += "allc" in path
                    lens.append(len(path)); last = None
        print(f"\nslips {cond[0]}, bed of {cond[1]}: {n} journeys from an all-defect majority to a majority of the machine, in {runs} runs (the study's code logs at most {CAP} changes of majority a run; {capped} runs reached that, and journeys after it are not seen)")
        if n == 0: continue
        print("   first majority after all-defect:", ", ".join(f"{k} {v} ({100*v/n:.0f}%)" for k, v in first.most_common(6)), "  (x = a machine without a name here)")
        print(f"   journeys passing through echo-once: {via['echo']}; through tit-for-tat or grim: {via['tft or grim']}; through all-cooperate: {via['allc']}; straight from all-defect with no other majority between: {sum(1 for l in lens if l == 0)}")
        print(f"   other majorities passed through per journey: median {statistics.median(lens)}, range {min(lens)}-{max(lens)}")
