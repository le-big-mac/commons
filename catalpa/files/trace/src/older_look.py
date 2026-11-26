# Exploration after K1 and K2 failed: the filtered sea level day by day (noon UTC) around Kay 2022 and Nora 1997
# at five gauges, each minus its mean over days D-8 to D-2, cm; and the storms' positions from the best tracks.
import sys, io, contextlib, importlib.util, csv, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
W = load('wave')
G = [("9410170", "San Diego"), ("9410660", "Los Angeles"), ("9412110", "Port San Luis"), ("9414290", "San Francisco"), ("9416841", "Arena Cove")]
def track(code):
    out = {}; on = False
    for l in open('/home/agent1/trace/data/hurdat/nepac.txt'):
        w = [x.strip() for x in l.split(',')]
        if len(w[0]) == 8 and w[0][:2] in ('EP', 'CP'): on = (w[0] == code); continue
        if on and len(w) > 6 and w[1] == '1200': out[dt.datetime.strptime(w[0], '%Y%m%d').date()] = f"{w[4]} {w[5]} {w[6]}kt {w[3]}"
    return out
for tag, year, D, t0, code in (("KAY 2022", 2022, dt.date(2022, 9, 8), dt.datetime(2022, 8, 16), "EP122022"), ("NORA 1997", 1997, dt.date(1997, 9, 24), dt.datetime(1997, 9, 2), "EP161997")):
    NN = 24 * 46; ser = {}
    for sid, name in G:
        x = np.full(NN, np.nan)
        for r in csv.reader(open(f'/home/agent1/trace/data/coops/old/h{sid}_{year}.csv')):
            try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
            except (ValueError, IndexError): continue
            k = int((t - t0).total_seconds() // 3600)
            if 0 <= k < NN: x[k] = v * 100
        y = W.godin(x); hh = lambda day: int((dt.datetime(day.year, day.month, day.day) - t0).total_seconds() // 3600)
        ser[name] = y - np.nanmean(y[hh(D - dt.timedelta(days=8)):hh(D - dt.timedelta(days=1))])
    tr = track(code)
    print(f"{tag} (D = {D}); storm's position at 12:00 UTC from the best track")
    print("date        " + "".join(f"{g[:12]:>14}" for _, g in G) + "   storm")
    day = D - dt.timedelta(days=10)
    while day <= D + dt.timedelta(days=10):
        k = int((dt.datetime(day.year, day.month, day.day, 12) - t0).total_seconds() // 3600)
        print(f"{day}  " + "".join(f"{ser[g][k]:14.1f}" if 0 <= k < NN and not np.isnan(ser[g][k]) else "             -" for _, g in G) + f"   {tr.get(day, '')}")
        day += dt.timedelta(days=1)
    print()
