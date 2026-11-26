# The origin server now needs about 0.75 s for each daily step and its proxy gives up after 20 s, so the points still
# missing their 19 Sep - 25 Nov file are fetched in groups of up to five neighbours (one box) and in pieces of 14 days.
# Usage: python3 -I src/regroup.py plan   -> writes data/alt/requests_groups.txt
#        python3 -I src/regroup.py split  -> writes the missing p*_2026b.csv files from the group files
import json, os, sys, csv
A = '/home/agent1/trace/data/alt/'
pts = json.load(open(A + 'points.json'))
missing = [p for p in pts if not os.path.exists(A + f"p{p['km']:+05d}_2026b.csv")]
groups = []
for p in missing:
    if groups and len(groups[-1]) < 5 and p['km'] - groups[-1][-1]['km'] == 100: groups[-1].append(p)
    else: groups.append([p])
chunks = [("2026-09-19", "2026-10-02"), ("2026-10-03", "2026-10-16"), ("2026-10-17", "2026-10-30"), ("2026-10-31", "2026-11-13"), ("2026-11-14", "2026-11-25")]
if sys.argv[1] == 'plan':
    out = []
    for g in groups:
        la = (min(p['box'][0][0] for p in g), max(p['box'][0][1] for p in g)); lo = (min(p['box'][1][0] for p in g), max(p['box'][1][1] for p in g))
        for i, (a, b) in enumerate(chunks):
            out.append(f"g{g[0]['km']:+05d}_{i}.csv https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsshDaily.csv?sla[({a}T00:00:00Z):1:({b}T00:00:00Z)][({la[0]}):1:({la[1]})][({lo[0]}):1:({lo[1]})]")
    open(A + 'requests_groups.txt', 'w').write("\n".join(out) + "\n")
    print(len(missing), "points missing;", len(groups), "groups;", len(out), "requests; largest box (cells):",
          max(round((max(p['box'][0][1] for p in g) - min(p['box'][0][0] for p in g)) / 0.25 + 1) * round((max(p['box'][1][1] for p in g) - min(p['box'][1][0] for p in g)) / 0.25 + 1) for g in groups))
else:
    for g in groups:
        rows = []
        for i in range(len(chunks)):
            fn = A + f"g{g[0]['km']:+05d}_{i}.csv"
            if not os.path.exists(fn): print("missing piece", fn); rows = None; break
            rows += [r for r in csv.reader(open(fn)) if len(r) >= 4 and r[0][:1].isdigit()]
        if rows is None: continue
        for p in g:
            cells = {tuple(c) for c in p['cells']}
            with open(A + f"p{p['km']:+05d}_2026b.csv", 'w') as f:
                f.write("time,latitude,longitude,sla\nUTC,degrees_north,degrees_east,m\n")
                n = 0
                for r in rows:
                    if (float(r[1]), float(r[2])) in cells: f.write(",".join(r[:4]) + "\n"); n += 1
            print(p['km'], n, "rows")
