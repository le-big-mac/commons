"""Look up the names of the species keys found by woodpeckers.py (K = 5) at GBIF and store each answer verbatim.

usage: gbif_names.py WOODPECKERS.json OUT_DIR
"""
import json
import os
import sys
import time
import urllib.request

keys = json.load(open(sys.argv[1]))['K5']['keys']
out = sys.argv[2]
for k in keys:
    path = os.path.join(out, f'{k}.json')
    if os.path.exists(path):
        continue
    req = urllib.request.Request(f'https://api.gbif.org/v1/species/{k}', headers={'User-Agent': 'python-urllib'})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    json.loads(body)
    with open(path, 'wb') as f:
        f.write(body)
    time.sleep(0.1)
print(len(keys), 'keys')
