"""Fetch the ballot files of ten PrefLib datasets (public; no account).   usage: python -I fetch.py OUTDIR"""
import sys, os, json, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
OUT = sys.argv[1]
SETS = ["00005 - burlington", "00016 - aspen", "00017 - berkley", "00018 - minneapolis", "00019 - oakland", "00020 - pierce", "00021 - sf", "00022 - sl",
        "00023 - takomapark", "00058 - nswla"]
API = "https://api.github.com/repos/PrefLib/PrefLib-Data/contents/datasets/"
jobs = []
for d in SETS:
    with urllib.request.urlopen(API + urllib.parse.quote(d), timeout=60) as r:
        for x in json.load(r):
            if x['name'].split('.')[-1] in ('soi', 'toi', 'soc', 'toc') or x['name'] == 'info.txt':
                jobs.append((d.split(' - ')[1], x['name'], x['download_url']))
def get(job):
    d, name, url = job
    os.makedirs(f"{OUT}/{d}", exist_ok=True)
    path = f"{OUT}/{d}/{name}"
    if not os.path.exists(path):
        with urllib.request.urlopen(url, timeout=120) as r:
            data = r.read()
        with open(path, 'wb') as f:
            f.write(data)
    return os.path.getsize(path)
with ThreadPoolExecutor(8) as ex:
    sizes = list(ex.map(get, jobs))
print("files:", len(jobs), "bytes:", sum(sizes))
