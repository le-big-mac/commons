"""Afterwards: hires and total separations as levels (thousands), to see what rounding the rates to one decimal does.   usage: python -I fetch2.py OUTDIR"""
import sys, json, urllib.request
OUT = sys.argv[1]
SERIES = {'hires_level': 'JTS000000000000000HIL', 'separations_level': 'JTS000000000000000TSL'}
rows = {}
for y0, y1 in ((2000, 2009), (2010, 2019), (2020, 2026)):
    body = json.dumps({"seriesid": list(SERIES.values()), "startyear": str(y0), "endyear": str(y1)}).encode()
    req = urllib.request.Request("https://api.bls.gov/publicAPI/v1/timeseries/data/", data=body, headers={'Content-Type': 'application/json', 'User-Agent': 'research-script/1.0'})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    open(f"{OUT}/levels-{y0}-{y1}.json", 'wb').write(raw)
    for s in json.loads(raw)['Results']['series']:
        for x in s['data']:
            if x['period'].startswith('M') and x['period'] != 'M13':
                rows.setdefault(s['seriesID'], {})[f"{x['year']}-{x['period'][1:]}"] = x['value']
months = sorted(set(m for d in rows.values() for m in d))
with open(f"{OUT}/levels.csv", 'w') as f:
    f.write("month," + ",".join(SERIES) + "\n")
    for m in months:
        f.write(m + "," + ",".join(rows.get(sid, {}).get(m, '') for sid in SERIES.values()) + "\n")
print("months:", len(months), months[0], "to", months[-1])
