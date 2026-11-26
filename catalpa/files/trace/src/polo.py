# Hurricane Polo and Hurricane Rachel, September-October 2026, from the public advisories of the National Hurricane
# Center saved in lit/nhc/ (read as text; nothing in them is run). Prints time in UTC, position, wind, distance from
# San Diego, and distance from the ocean-side coast line of Baja California (src/passages.py).
# Run: python3 -I src/polo.py > polo.out
import re, html, sys, datetime as dt, importlib.util
sys.path.insert(0, '/home/agent1/trace/src')
from coastline import gc
spec = importlib.util.spec_from_file_location('passages', '/home/agent1/trace/src/passages.py'); PS = importlib.util.module_from_spec(spec); spec.loader.exec_module(PS)
SD = (32.714, -117.174); OFF = {'MST': 7, 'PDT': 7, 'CST': 6, 'MDT': 6, 'PST': 8}
MON = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
def read(nm, k):
    s = open(f'/home/agent1/trace/lit/nhc/{nm}_public_{k:03d}.html', encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre[^>]*>([\s\S]*?)</pre>', s); t = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
    d = re.search(r'\n(\d{3,4}) (AM|PM) ([A-Z]{3}) [A-Za-z]{3} ([A-Za-z]{3}) (\d{1,2}) 2026', t); loc = re.search(r'LOCATION\.\.\.([\d.]+)N ([\d.]+)W', t); w = re.search(r'MAXIMUM SUSTAINED WINDS\.\.\.(\d+) MPH', t)
    hh = int(d.group(1)) // 100 % 12 + (12 if d.group(2) == 'PM' else 0)
    utc = dt.datetime(2026, MON[d.group(4)], int(d.group(5)), hh) + dt.timedelta(hours=OFF[d.group(3)])
    return utc, float(loc.group(1)), -float(loc.group(2)), int(w.group(1))
for nm, ks in (("POLO", range(20, 39)), ("RACHEL", list(range(14, 34)) + list(range(34, 59, 2)))):
    print(f"{nm}: advisory, time UTC, position, wind mph (km/h), km from San Diego, km from Baja California's ocean-side line")
    for k in ks:
        try: utc, lat, lon, mph = read(nm, k)
        except FileNotFoundError: continue
        dist, west = PS.near(lat, lon)
        q = "  <- first point at hurricane strength north of 22 N, west of the line and within 300 km of it" if nm == "POLO" and k == 30 else ""
        print(f"  {k:3d}  {utc.strftime('%d %b %H:%M')}  {lat:.1f}N {abs(lon):.1f}W  {mph:3d} ({mph * 1.609:.0f})  {gc(SD, (lat, lon)):5.0f}  {dist:4.0f} {'west' if west else 'east'}{q}")
    print()
