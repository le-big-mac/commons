# Was the rise of mid-October 2004 a storm in the north? NOAA's daily summaries for San Francisco's and Arcata's airports.
# Run: python3 -I src/oct2004.py > oct2004.out
import csv
for st in ("72494023234", "72594524283"):
    rows = list(csv.DictReader(open(f'/home/agent1/trace/data/gsod_other/g{st}_2004.csv')))
    o = [r for r in rows if r['DATE'].startswith('2004-10')]; slp = [float(r['SLP']) for r in o if float(r['SLP']) < 9000]
    print(f"{rows[0]['NAME']}: October 2004 mean sea-level pressure {sum(slp) / len(slp):.1f} hPa")
    for r in o:
        if '2004-10-14' <= r['DATE'] <= '2004-10-22':
            g = r['GUST'].strip(); print(f"   {r['DATE']}  pressure {float(r['SLP']):7.1f}  mean wind {float(r['WDSP']):4.1f} kt  gust {'-' if g.startswith('999') else g:>5} kt  rain {float(r['PRCP']):.2f} in")
    low = min(o, key=lambda r: float(r['SLP'])); print(f"   lowest: {float(low['SLP']):.1f} on {low['DATE']}, {sum(slp) / len(slp) - float(low['SLP']):.1f} below the month's mean")
