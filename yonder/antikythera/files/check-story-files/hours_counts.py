"""Recount what the page says about the hours from the note's hours_run.json (read only)."""
import json, statistics
d = json.load(open('/srv/commons/antikythera-agent3/hours/hours_run.json'))
print('keys', list(d.keys()), list(d['18'].keys()))
S16 = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
for key in ('18', '22'):
    R = d[key]['scores']
    sc = {int(k): v for k, v in R.items()}
    print('==', key, 'hours; starts', len(sc))
    med = statistics.median(v[0] for v in sc.values())
    print(' median', round(med, 3))
    s0 = sc[0][0]
    print(' 205 BC', [round(x, 3) for x in sc[0]], ' starts strictly better:', sum(1 for v in sc.values() if v[0] < s0))
    four = [223, 205, 187, 169]
    for bc in four: print('  ', bc, 'BC', round(sc[S16[bc]][0], 3), 'h at', round(sc[S16[bc]][1], 2))
    others = [sc[S16[bc]][0] for bc in S16 if bc not in four]
    print(' other twelve:', round(min(others), 3), 'to', round(max(others), 3))
    better = [k for k, v in sc.items() if v[0] < s0]
    print(' of the better ones, among the sixteen:', [bc for bc, k in S16.items() if k in better])
    print(' under 3.0 h:', sum(1 for v in sc.values() if v[0] < 3.0))
    for cyc in range(-5, 4):
        k = 223 * cyc
        if k in sc: print('   cycle', cyc, round(sc[k][0], 2), 'h at', round(sc[k][1], 1))
    lon = [sc[S16[bc]][1] for bc in four]
    print(' longitude steps:', [round(((lon[i + 1] - lon[i] + 180) % 360) - 180, 2) for i in range(3)])
    for k in (340, 341, 342, 343): print('   k', k, round(sc[k][0], 2), round(sc[k][1], 1))
# pointers: ratios
rms_then = {'mercury': 4.2271, 'venus': 1.4818, 'mars': 9.5623, 'jupiter': 3.6651, 'saturn': 4.9654}
rms_now = {'mercury': 4.690, 'venus': 10.437, 'mars': 11.669, 'jupiter': 4.418, 'saturn': 9.260}
print('ratios now/then:', {b: round(rms_now[b] / rms_then[b], 3) for b in rms_then})
print('Moon: 262.154/360 =', round(262.154 / 360, 3), '; 105.314/360 =', round(105.314 / 360, 3), '; 1.035/0.11753 =', round(1.035 / 0.11753, 1), 'years; 0.11753*2230.528 =', round(0.11753 * 2230.528, 1))
print('115/360 =', round(115 / 360, 3), '; 35.27/360 =', round(35.27 / 360, 3))
