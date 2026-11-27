# After sheet 8 was scored, not sealed: how far the single timings and the averaged rise depend on my choices.
# Run: ~/ipd/.venv/bin/python -I src/north_hourly_look.py > north_hourly_look.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
H = load('north_hourly'); EV = H.EV; KM = H.KM; ST = H.ST
def cross(y, half, s0, s1, hold):
    for k in range(s0, s1):
        seg = y[k:k + hold]
        if not np.isnan(seg).any() and (seg >= half).all(): return k
    return None
def single(Y, h0, floor, hold):
    b0, b1, a0, a1, s0, s1 = h0 - 8 * 24, h0 - 24, h0 + 3 * 24, h0 + 8 * 24, h0 - 2 * 24, h0 + 8 * 24; rows = []
    for y in Y:
        if y is None or np.isnan(y[b0:a1]).mean() > 0.2: rows.append(None); continue
        B, A = np.nanmean(y[b0:b1]), np.nanmean(y[a0:a1]); k = cross(y, B + (A - B) / 2, s0, s1, hold) if A - B >= floor else None
        rows.append((A - B, k, k == s0))
    return rows
def classify(e, floor, hold, most=10.0):
    rows = single(e["Y"], (e["k"] // 24) * 24, floor, hold)
    ok = [(KM[i], r[1]) for i, r in enumerate(rows[:10]) if r and r[1] is not None and not r[2]]
    if len(ok) < 5: return None, None, None, len(ok)
    s, sc = H.line([o[0] for o in ok], [o[1] for o in ok]); sp = 24 / s if s > 0 else None
    if sc > most: c = "no order"
    elif sp and 150 <= sp <= 1000: c = "north in order"
    else: c = "at once"
    return c, sp, sc, len(ok)
print("A. EACH RISE BY THREE KINDS (scatter about its line over 10 hours = 'no order'; under that, 150-1000 km/day northward = 'north in order', else 'at once')")
print("   this split by scatter was made after seeing the table; the sealed line P5 used the speed alone")
for floor, hold in ((5, 12), (4, 12), (3, 12), (6, 12), (5, 6), (5, 24)):
    cl = [(e["D"], *classify(e, floor, hold)) for e in EV]; t = [c for c in cl if c[1]]
    print(f"   floor {floor} cm, held {hold} h: timed {len(t)} of {len(EV)}; north in order {sum(1 for c in t if c[1] == 'north in order')}, at once {sum(1 for c in t if c[1] == 'at once')}, no order {sum(1 for c in t if c[1] == 'no order')}")
    if (floor, hold) in ((5, 12), (3, 12)):
        for D, c, sp, sc, n in cl:
            if c: print(f"      {D}  {n:2d} gauges  {c:<15} " + (f"{sp:6.0f} km/day" if sp else "   not northward") + f"  scatter {sc:4.1f} h" + ("   hurricane near" if [e for e in EV if e['D'] == D][0]['hur'] else ""))
r26 = single(H.Y26, 27 * 24, 5, 12); ok = [(KM[i], r[1]) for i, r in enumerate(r26) if r and r[1] is not None and not r[2]]; s, sc = H.line([o[0] for o in ok], [o[1] for o in ok])
print(f"   2026 by the same sum: {len(ok)} gauges, {24 / s:.0f} km/day, scatter {sc:.1f} h -> north in order")
print("\nB. THE SIZE OF EACH RISE AT EACH GAUGE BY 2026'S RULE (cm; after = days D*+3..D*+7 less before = days D*-8..D*-2)")
print(f"   {'day D':<11} " + " ".join(f"{n[:5]:>5}" for s_, n, *_ in ST))
sizes = []
for e in EV:
    rows = single(e["Y"], (e["k"] // 24) * 24, 5, 12); sizes.append([None if r is None else r[0] for r in rows])
    print(f"   {e['D']}  " + " ".join("    -" if r is None else f"{r[0]:5.1f}" for r in rows))
r26s = [r[0] for r in r26]
print(f"   2026        " + " ".join(f"{v:5.1f}" for v in r26s))
for i in (4, 6, 9):
    v = [s_[i] for s_ in sizes if s_[i] is not None]
    print(f"   {ST[i][1]}: {len(v)} rises with a record; 5 cm or more in {sum(1 for x in v if x >= 5)}; middle value {np.median(v):.1f}; 2026: {r26s[i]:.1f}")
print("\nC. THE AVERAGED RISE: the mean, the middle value hour by hour, and the mean without 16 October 2004")
good = [e for e in EV if not e["edge"]]; z = 10 * 24
def curves(events, how):
    out = []
    for i in range(len(ST)):
        xs = []
        for e in events:
            y = e["Y"][i]
            if y is None: continue
            seg = y[e["k"] + H.TAU[0]: e["k"] + H.TAU[-1] + 1]; base = y[e["k"] - 8 * 24: e["k"] - 2 * 24]
            if np.isnan(seg).mean() > 0.1 or np.isnan(base).mean() > 0.2: continue
            xs.append(seg - np.nanmean(base))
        out.append(None if not xs else (np.nanmean(np.array(xs), axis=0) if how == "mean" else np.nanmedian(np.array(xs), axis=0)))
    return out
for tag, ev, how in (("mean of all", good, "mean"), ("middle value", good, "median"), ("mean without 16 Oct 2004", [e for e in good if e["D"] != dt.date(2004, 10, 16)], "mean")):
    cv = curves(ev, how); print(f"   {tag}:")
    pts = []
    for i, c in enumerate(cv):
        if c is None: continue
        A, k, st = H.timing(c)
        if i < 10 and k is not None: pts.append((KM[i], k))
        print(f"      {ST[i][1]:<14} rise {A:5.1f}; halfway {('  -' if k is None else f'{k:4d}')} h; days -2, 0, +1, +2, +3, +4, +5, +6, +8: " + " ".join(f"{c[z + d * 24]:+5.1f}" for d in (-2, 0, 1, 2, 3, 4, 5, 6, 8)))
    if len(pts) >= 6:
        s, sc = H.line([p[0] for p in pts], [p[1] for p in pts]); print(f"      line: {s * 1000:.1f} hours per 1000 km" + (f" = {24 / s:.0f} km/day" if s > 0 else " (not northward)") + f", scatter {sc:.1f} h, {len(pts)} gauges")
