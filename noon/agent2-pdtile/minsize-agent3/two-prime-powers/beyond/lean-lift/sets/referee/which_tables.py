"""Which solver tables give the line 'steps j used' of spread_lift.out?  For each n = 2 table: the number of witnesses, and
how many need j = 2 with r = 3 (a multiplicity above 3, or all equal to 3) and with r = 5."""
import glob
from thm import read_table, parse_witness
O = '/srv/commons/agent2-pdtile/minsize-agent3/out/'
def jneeded(mult, r):
    j = 0
    while not (max(mult.values()) <= r ** j and not all(m == r ** j for m in mult.values())): j += 1
    return j
for f in sorted(glob.glob(O + 'n2-*-multi-cpsat.jsonl')):
    rows = read_table(f); out = {}
    for r in (3, 5):
        c = {}
        for o in rows:
            j = jneeded(parse_witness(o['witness']), r); c[j] = c.get(j, 0) + 1
        out[r] = dict(sorted(c.items()))
    mx = max(max(parse_witness(o['witness']).values()) for o in rows)
    print(f.split('/')[-1], 'witnesses:', len(rows), ' j needed with r = 3:', out[3], ' with r = 5:', out[5], ' largest multiplicity in the table:', mx)
