"""Verdicts on the ten sealed expectations, by the letter ("between" includes its ends).   usage: python verdicts.py results.json verdicts.json"""
import sys, json
R = json.load(open(sys.argv[1])); V = {}; M = {}
mb, sh, st, sc = R['musket ball'], R['24-pound shot'], R['trebuchet stone'], R['shuttlecock']
V['J1'] = mb['at45']['range_fraction'] < 0.10; M['J1'] = f"{mb['at45']['range_fraction']:.4f} ({mb['at45']['range']:.0f} m)"
V['J2'] = 25 <= mb['best_elevation'] <= 38; M['J2'] = f"{mb['best_elevation']} degrees"
V['J3'] = mb['at45']['impact_angle'] > 65; M['J3'] = f"{mb['at45']['impact_angle']:.1f} degrees"
V['J4'] = mb['at45']['apex_fraction'] > 0.60; M['J4'] = f"{mb['at45']['apex_fraction']:.4f}"
V['J5'] = 0.15 <= sh['at45']['range_fraction'] <= 0.35; M['J5'] = f"{sh['at45']['range_fraction']:.4f} ({sh['at45']['range']:.0f} m)"
V['J6'] = 33 <= sh['best_elevation'] <= 43; M['J6'] = f"{sh['best_elevation']} degrees"
V['J7'] = st['at45']['range_fraction'] >= 0.90 and st['best_elevation'] in (43, 44, 45); M['J7'] = f"{st['at45']['range_fraction']:.4f}; {st['best_elevation']} degrees"
V['J8'] = sc['at45']['apex_fraction'] > 0.70 and sc['at45']['impact_angle'] > 80; M['J8'] = f"{sc['at45']['apex_fraction']:.4f}; {sc['at45']['impact_angle']:.1f} degrees"
V['J9'] = all(q['apex_fraction'] > 0.5 and q['impact_angle'] > q['elev'] for k in (mb, sh, st, sc) for q in k['sweep'])
M['J9'] = f"least apex fraction {min(q['apex_fraction'] for k in (mb, sh, st, sc) for q in k['sweep']):.4f}; least (impact angle - elevation) {min(q['impact_angle'] - q['elev'] for k in (mb, sh, st, sc) for q in k['sweep']):.3f} degrees"
V['J10'] = 0.90 <= mb['at45']['impact_over_vt'] <= 1.05; M['J10'] = f"{mb['at45']['impact_over_vt']:.4f}"
for k in sorted(V, key=lambda k: int(k[1:])): print(f"{k:4s} {'held  ' if V[k] else 'failed'}  {M[k]}")
json.dump(dict(verdicts={k: bool(v) for k, v in V.items()}, measured=M), open(sys.argv[2], 'w'), indent=1)
