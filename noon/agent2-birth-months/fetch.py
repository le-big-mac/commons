"""Fetch dates of birth from Wikidata's query service, one group at a time.   usage: python -I fetch.py OUTDIR
Each row: person, date of birth (best-ranked statement, given to the day), sex if stated."""
import sys, os, time, urllib.request, urllib.parse
OUT = sys.argv[1]
GROUPS = {                       # name: (occupation, country of citizenship)
    'football-spain': ('Q937857', 'Q29'), 'football-uk': ('Q937857', 'Q145'), 'football-japan': ('Q937857', 'Q17'),
    'football-germany': ('Q937857', 'Q183'), 'football-brazil': ('Q937857', 'Q155'),
    'hockey-canada': ('Q11774891', 'Q16'), 'baseball-usa': ('Q10871364', 'Q30'), 'politicians-spain': ('Q82955', 'Q29'),
    # added after the registered run, as controls for each country's ordinary seasons of birth
    'politicians-uk': ('Q82955', 'Q145'), 'politicians-japan': ('Q82955', 'Q17'),
    # American politicians as a whole are too many for the service (the reply broke off after a minute and was discarded);
    # members of the House of Representatives (position held, P39) stand in for them
    'house-usa': '?p wdt:P39 wd:Q13218630.',
    'politicians-germany': ('Q82955', 'Q183'), 'politicians-brazil': ('Q82955', 'Q155'), 'politicians-canada': ('Q82955', 'Q16'),
}
Q = """SELECT ?p ?d ?sex WHERE {
  %s
  ?p p:P569 ?st. ?st a wikibase:BestRank; psv:P569 ?v.
  ?v wikibase:timeValue ?d; wikibase:timePrecision 11 .
  OPTIONAL { ?p wdt:P21 ?sex }
}"""
for name, spec in GROUPS.items():
    who = spec if isinstance(spec, str) else '?p wdt:P106 wd:%s; wdt:P27 wd:%s.' % spec
    path = f"{OUT}/{name}.csv"
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(name, "already there:", sum(1 for _ in open(path)) - 1, "rows")
        continue
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({'query': Q % who})
    req = urllib.request.Request(url, headers={'User-Agent': 'research-script/1.0', 'Accept': 'text/csv'})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except Exception as e:
        print(name, "FAILED:", repr(e)[:200]); time.sleep(65)
        continue
    if b'Exception' in data[-3000:] or not data.rstrip().endswith((b'Q6581097', b'Q6581072', b'Z,')) and b'\tat ' in data[-3000:]:
        print(name, 'BROKEN REPLY, not saved'); time.sleep(65); continue
    open(path, 'wb').write(data)
    print(f"{name}: {data.count(b'\\n') - 1} rows, {len(data)} bytes, {time.time() - t:.0f} s")
    time.sleep(65)                                  # the service asks for one request a minute at present
