"""Fetch, for every 5 x 5 degree box, the number of GBIF records of each woodpecker species (family Picidae, key 9333).

usage: gbif_fetch.py OUT_DIR [LAT_FROM LAT_TO]

One request per box to the public occurrence-search API with limit=0 and a facet on speciesKey, so that only counts
come back, never records. Responses are stored verbatim as OUT_DIR/box_<south>_<west>.json; a box already stored is
not asked for again. Filters: coordinates present, no flagged geospatial issue, occurrenceStatus PRESENT,
basisOfRecord HUMAN_OBSERVATION or PRESERVED_SPECIMEN.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

out = sys.argv[1]
lat_from = int(sys.argv[2]) if len(sys.argv) > 2 else -90
lat_to = int(sys.argv[3]) if len(sys.argv) > 3 else 90
BASE = 'https://api.gbif.org/v1/occurrence/search'
n = 0
for south in range(lat_from, lat_to, 5):
    for west in range(-180, 180, 5):
        path = os.path.join(out, f'box_{south}_{west}.json')
        if os.path.exists(path):
            continue
        q = [('familyKey', '9333'), ('hasCoordinate', 'true'), ('hasGeospatialIssue', 'false'), ('occurrenceStatus', 'PRESENT'),
             ('basisOfRecord', 'HUMAN_OBSERVATION'), ('basisOfRecord', 'PRESERVED_SPECIMEN'),
             ('decimalLatitude', f'{south},{south + 5}'), ('decimalLongitude', f'{west},{west + 5}'),
             ('facet', 'speciesKey'), ('facetLimit', '1000'), ('limit', '0')]
        url = BASE + '?' + urllib.parse.urlencode(q)
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'python-urllib'})
                with urllib.request.urlopen(req, timeout=120) as r:
                    body = r.read()
                json.loads(body)
                break
            except Exception as e:   # wait and try again
                print('retry', south, west, repr(e)[:100], flush=True)
                time.sleep(5 * (attempt + 1))
        else:
            raise SystemExit(f'gave up on box {south},{west}')
        with open(path + '.tmp', 'wb') as f:
            f.write(body)
        os.replace(path + '.tmp', path)
        n += 1
        time.sleep(0.15)
    print('latitude band', south, 'done;', n, 'requests so far', flush=True)
