# Wind at six shore gauges, 22 September to 5 October 2026: daily mean of the component blowing along the coast
# towards the north-west (positive = from the south-east, the direction that raises the sea at this coast), m/s,
# with the September mean (1-21 Sep) for comparison. Shore anemometers are sheltered and are a poor guide to the wind
# over the shelf; this is a first look only. Exploration, made after a reader asked what the wind did.
import csv, datetime as dt, math
import numpy as np
ST = [("9410230", "La Jolla", 325), ("9411340", "Santa Barbara", 280), ("9414290", "San Francisco", 330), ("9416841", "Arena Cove", 325), ("9418767", "North Spit", 5), ("9419750", "Crescent City", 350)]
# the third number is the compass bearing of the coast's poleward direction near the gauge (my estimate from a map)
def load(sid, brg):
    d = {}
    for r in csv.reader(open(f'/home/agent1/trace/data/coops/wind/w{sid}.csv')):
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); sp = float(r[1]); di = float(r[2])
        except (ValueError, IndexError): continue
        # direction is where the wind comes from; the air moves towards di + 180
        along = sp * math.cos(math.radians((di + 180) - brg))
        d.setdefault(t.date(), []).append(along)
    return {k: float(np.mean(v)) for k, v in d.items() if len(v) >= 18}
S = {name: load(sid, brg) for sid, name, brg in ST}
print("alongshore wind, m/s (positive = blowing towards the pole)")
print("date         " + "".join(f"{n[:12]:>14}" for _, n, _ in ST))
print("1-21 Sep mean" + "".join(f"{np.mean([v for d, v in S[n].items() if d < dt.date(2026, 9, 22)]):14.1f}" for _, n, _ in ST))
day = dt.date(2026, 9, 22)
while day <= dt.date(2026, 10, 12):
    print(f"{day}   " + "".join(f"{S[n][day]:14.1f}" if day in S[n] else "             -" for _, n, _ in ST))
    day += dt.timedelta(days=1)
