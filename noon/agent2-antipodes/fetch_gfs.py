"""Fetch three fields of the GFS 0.25-degree analysis by byte range from the public archive (no account needed).

For each of the 72 sample times of 2025 (1st, 11th, 21st of each month, 00 and 12 UTC): the index file, then
PRMSL at mean sea level and TMP at the 0.995 sigma level; LAND at the surface once (from hour 0 of the first run:
the analysis file does not carry it).
If a time is missing, the same hour of the next day is taken (and reported).
usage: python -I fetch_gfs.py OUTDIR
"""
import sys, os, datetime, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

BASE = "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
OUT = sys.argv[1]
WANT = {"prmsl": ":PRMSL:mean sea level:anl:", "tmp": ":TMP:0.995 sigma level:anl:"}


def get(url, rng=None):
    req = urllib.request.Request(url, headers={"Range": f"bytes={rng[0]}-{rng[1]}"} if rng else {})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def offsets(idx, key):
    lines = idx.decode().splitlines()
    for n, line in enumerate(lines):
        if key in line + ":":
            start = int(line.split(":")[1])
            end = int(lines[n + 1].split(":")[1]) - 1 if n + 1 < len(lines) else ""
            return start, end
    raise KeyError(key)


def one(when):
    for shift in (0, 1):
        w = when + datetime.timedelta(days=shift)
        url = f"{BASE}/gfs.{w:%Y%m%d}/{w:%H}/atmos/gfs.t{w:%H}z.pgrb2.0p25.anl"
        try:
            idx = get(url + ".idx")
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                continue
            raise
        sizes = {}
        for name, key in WANT.items():
            path = f"{OUT}/gfs.{when:%Y%m%d%H}.{name}.grib2"
            if not os.path.exists(path):
                data = get(url, offsets(idx, key))
                with open(path + ".part", "wb") as f:
                    f.write(data)
                os.rename(path + ".part", path)
            sizes[name] = os.path.getsize(path)
        return when, shift, sizes
    return when, None, {}


TIMES = [datetime.datetime(2025, m, d, h) for m in range(1, 13) for d in (1, 11, 21) for h in (0, 12)]
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(f"{OUT}/land.grib2"):                         # the land mask is not in the .anl file; it is in hour 0 of the same run
        url = f"{BASE}/gfs.20250101/00/atmos/gfs.t00z.pgrb2.0p25.f000"
        data = get(url, offsets(get(url + ".idx"), ":LAND:surface:"))
        with open(f"{OUT}/land.grib2", "wb") as f:
            f.write(data)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(one, TIMES))
    ok = [r for r in res if r[1] is not None]
    print(f"times wanted {len(TIMES)}; fetched {len(ok)}; taken from the next day: {[f'{r[0]:%Y-%m-%d %H}' for r in ok if r[1] == 1]};"
          f" missing: {[f'{r[0]:%Y-%m-%d %H}' for r in res if r[1] is None]}")
    print("bytes: prmsl", min(r[2]['prmsl'] for r in ok), "to", max(r[2]['prmsl'] for r in ok), "; tmp", min(r[2]['tmp'] for r in ok), "to", max(r[2]['tmp'] for r in ok))
