"""Referee step 3: compare the author's results.json with my own integrator, entry by entry; reproduce the first-run failure
with the author's own fly(); a few extra numbers.  Run with -B so that no bytecode is written outside referee/."""
import sys, json, math
sys.path.insert(0, "/home/agent2/impetus/referee")
import step2_lib as S

R = json.load(open("/home/agent2/impetus/results.json"))
names = {"musket ball": "musket", "24-pound shot": "shot24", "trebuchet stone": "stone", "shuttlecock": "shuttle"}
print("== A. every sweep entry (4 x 81) and the 45-degree entries: largest disagreement between results.json and my integrator")
worst = dict(range_rel=0, apex=0, ang=0, vl=0)
for n, k in names.items():
    assert abs(R[n]["vt"] - S.VT[k]) < 1e-9 and R[n]["v0"] == S.V0[k]
    mybest = None
    for q in R[n]["sweep"] + [R[n]["at45"]]:
        m = S.fly(S.RAT[k], q["elev"])
        worst["range_rel"] = max(worst["range_rel"], abs(m["R"] * S.L[k] / q["range"] - 1))
        worst["apex"] = max(worst["apex"], abs(m["af"] - q["apex_fraction"]))
        worst["ang"] = max(worst["ang"], abs(m["ang"] - q["impact_angle"]))
        worst["vl"] = max(worst["vl"], abs(m["vl"] - q["impact_over_vt"]))
    best = max(R[n]["sweep"], key=lambda q: q["range"])["elev"]
    assert best == R[n]["best_elevation"]
    print(f"   {n}: vt {R[n]['vt']:.4f}, best {best}, at45 range {R[n]['at45']['range']:.6f} apex {R[n]['at45']['apex_fraction']:.6f} impact {R[n]['at45']['impact_angle']:.5f} lands {R[n]['at45']['impact_over_vt']:.5f}")
print("   worst:", {k: f"{v:.2e}" for k, v in worst.items()})
print("== B. family in results.json against mine (45 degrees and best whole degree)")
wf = 0
for f in R["family"]:
    m = S.fly(f["ratio"], 45); b = S.best_whole(f["ratio"], 5, 85)
    wf = max(wf, abs(m["rf"] - f["range_fraction"]), abs(m["af"] - f["apex_fraction"]), abs(m["ang"] - f["impact_angle"]) / 100)
    if b != f["best_elevation"]: print("   BEST ELEVATION DIFFERS at ratio", f["ratio"], b, f["best_elevation"])
print(f"   worst disagreement in range fraction / apex fraction / impact angle (per 100 deg): {wf:.2e}; best elevations all agree unless listed above")
print("== C. the first-run failure, with the author's own fly() as the first run called it: fly(ratio, 1.0, elevation)")
sys.path.insert(0, "/home/agent2/impetus")
import impetus as I
for ratio in [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 4, 5, 6.6, 8.8, 12, 20, 40]:
    bad = []
    for e in [45] + list(range(5, 86)):
        try:
            I.fly(ratio, 1.0, e)
        except IndexError:
            bad.append(e)
    if bad: print(f"   ratio {ratio}: IndexError at elevations {bad[:6]}{'...' if len(bad) > 6 else ''} ({len(bad)} of 82 calls)")
print("   and the four sealed projectiles through the same fly(), default max_step: no error; ranges at 45:",
      ", ".join(f"{I.fly(p['v0'], p['vt'], 45)['range']:.6f}" for p in I.SHOTS.values()))
print("   same with a ceiling on the step (flight time / 400): ",
      ", ".join(f"{I.fly(p['v0'], p['vt'], 45, max_step=R[n]['at45']['time'] / 400)['range']:.6f}" for n, p in I.SHOTS.items()))
print("== D. extra numbers")
for k in ("musket", "shot24", "stone", "shuttle"):
    b = S.best_whole(S.RAT[k], 5, 85); q = S.fly(S.RAT[k], b)
    print(f"   {k} at its best whole degree {b}: range {q['R'] * S.L[k]:.1f} m, impact {q['ang']:.1f} deg, lands at {q['vl']:.2f} vt, apex fraction {q['af']:.3f}")
lo, hi = 50.0, 60.0
for _ in range(40):
    mid = (lo + hi) / 2
    if S.fly(mid / 6.8, 45)["af"] > 0.70: hi = mid
    else: lo = mid
print(f"   shuttlecock launch speed at which the apex fraction at 45 degrees is exactly 0.70: {lo:.2f} m/s")
from math import atan2, radians
def ev(t, s): return atan2(s[3], s[2]) - radians(35)
ev.direction = -1
for k in ("stone", "shot24", "musket", "shuttle"):
    q = S.fly(S.RAT[k], 45, extra_events=[ev]); print(f"   {k}: share of range before direction falls to 35 deg: {q['sol'].y_events[2][0][0] / q['R']:.5f}")
q = S.fly(40.0, 45, extra_events=[ev]); print(f"   ratio 40: {q['sol'].y_events[2][0][0] / q['R']:.5f}")
