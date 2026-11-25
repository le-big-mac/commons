"""Fetch nine monthly series from the Bureau of Labor Statistics' public API (version 1, no key).   usage: python -I fetch.py OUTDIR
The sealed plan named FRED, which only redistributes these series; its download endpoint timed out from this machine."""
import sys, json, urllib.request
OUT = sys.argv[1]
SERIES = {  # name: BLS series id (JTS = JOLTS, seasonally adjusted, total nonfarm; LNS = household survey, seasonally adjusted; CES = payroll survey)
    'openings_rate': 'JTS000000000000000JOR', 'hires_rate': 'JTS000000000000000HIR', 'quits_rate': 'JTS000000000000000QUR',
    'layoffs_rate': 'JTS000000000000000LDR', 'separations_rate': 'JTS000000000000000TSR', 'openings_level': 'JTS000000000000000JOL',
    'unemployment_rate': 'LNS14000000', 'unemployed_level': 'LNS13000000', 'hourly_earnings': 'CES0500000003',
}
rows = {}
for y0, y1 in ((2000, 2009), (2010, 2019), (2020, 2026)):
    body = json.dumps({"seriesid": list(SERIES.values()), "startyear": str(y0), "endyear": str(y1)}).encode()
    req = urllib.request.Request("https://api.bls.gov/publicAPI/v1/timeseries/data/", data=body, headers={'Content-Type': 'application/json', 'User-Agent': 'research-script/1.0'})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    open(f"{OUT}/reply-{y0}-{y1}.json", 'wb').write(raw)
    d = json.loads(raw)
    print(y0, y1, d.get('status'), d.get('message'))
    for s in d['Results']['series']:
        for x in s['data']:
            if x['period'].startswith('M') and x['period'] != 'M13':
                rows.setdefault(s['seriesID'], {})[f"{x['year']}-{x['period'][1:]}"] = x['value']
inv = {v: k for k, v in SERIES.items()}
months = sorted(set(m for d in rows.values() for m in d))
with open(f"{OUT}/series.csv", 'w') as f:
    f.write("month," + ",".join(SERIES) + "\n")
    for m in months:
        f.write(m + "," + ",".join(rows.get(sid, {}).get(m, '') for sid in SERIES.values()) + "\n")
print("months:", len(months), months[0], "to", months[-1], "; values per series:", {inv[s]: len(d) for s, d in rows.items()})
