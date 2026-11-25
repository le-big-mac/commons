"""Scores the eight sealed lines (expectations.md) from hours_run.json, by their letter. usage: hours_score.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(H, 'hours_run.json')))
S16 = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
s18 = {int(k): v for k, v in R['18']['scores'].items()}; s22 = {int(k): v for k, v in R['22']['scores'].items()}
r2 = lambda x: round(x, 2)
best18 = min(r2(s18[k][0]) for k in S16.values()); who18 = [bc for bc, k in S16.items() if r2(s18[k][0]) == best18]
best22 = min(r2(s22[k][0]) for k in S16.values()); who22 = [bc for bc, k in S16.items() if r2(s22[k][0]) == best22]
others = [bc for bc in S16 if bc not in (223, 205, 187, 169)]
lower = sum(v[0] < s18[0][0] for v in s18.values())
lines = [
 ('H1', 0.80, 2.2 <= s18[0][0] <= 2.9 and 15 <= s18[0][1] <= 35, f'205 BC with the 18: {s18[0][0]:.2f} h at {s18[0][1]:+.1f} E (sealed: 2.2 to 2.9 h, 15 to 35 E)'),
 ('H2', 0.88, any(b in (223, 205, 187) for b in who18), f'best of the sixteen with the 18: {who18} BC at {best18:.2f} h (sealed: one of 223, 205, 187)'),
 ('H3', 0.45, 205 in who18, f'best of the sixteen with the 18 is 205 BC itself: {205 in who18} (205 BC has {s18[0][0]:.2f} h)'),
 ('H4', 0.78, all(s18[S16[bc]][0] > 4.0 for bc in others), f'the other twelve with the 18: lowest {min(s18[S16[bc]][0] for bc in others):.2f} h (sealed: all above 4.0)'),
 ('H5', 0.70, lower <= 29, f'starts scoring strictly lower than 205 BC with the 18: {lower} of {len(s18)} (sealed: at most 29)'),
 ('H6', 0.70, abs(s18[767][0] - s18[0][0]) <= 0.5, f'767 months after 205 BC: {s18[767][0]:.2f} h against {s18[0][0]:.2f} (sealed: within 0.5)'),
 ('H7', 0.75, any(b in (223, 205, 187) for b in who22), f'best of the sixteen with all 22: {who22} BC at {best22:.2f} h (sealed: one of 223, 205, 187)'),
 ('H8', 0.60, 3.0 <= s22[0][0] <= 4.6, f'205 BC with all 22: {s22[0][0]:.2f} h (sealed: 3.0 to 4.6)'),
]
for name, p, ok, what in lines: print(f'{name}  {int(round(p * 100))}%  {"held  " if ok else "FAILED"}  {what}')
print(f'{sum(ok for _, _, ok, _ in lines)} of {len(lines)} held; Brier {sum((p - ok) ** 2 for _, p, ok, _ in lines) / len(lines):.4f} (always saying 50%: 0.2500)')
