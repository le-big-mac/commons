# Reference figures for the eighth sheet ("the months between"), from the months already in hand (January, March, ...,
# November of 2021 to 2024). Nothing here reads an even month. The ten southern photometers of the sheet are the eleven
# of the page less Arkaroola (stars477), whose every month is in hand from the dawn page.
import importlib.util, io, contextlib
import numpy as np
spec = importlib.util.spec_from_file_location('tonga_page', '/home/agent1/night/src/tonga_page.py'); TP = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(TP)
S = TP.S; TEN = [st for st in sorted(TP.south, key=lambda s: S[s]['lat']) if st != 'stars477']; NORTH5 = ['stars246', 'stars347', 'stars47', 'stars602', 'stars489']
ODD = [(y, m) for y in (2021, 2022, 2023, 2024) for m in (1, 3, 5, 7, 9, 11)]
def nb(k, step=2):
    i = k[0] * 12 + k[1] - 1; return ((i - step) // 12, (i - step) % 12 + 1), ((i + step) // 12, (i + step) % 12 + 1)
print('the ten southern photometers: ' + ', '.join(f"{TP.PLACE[st].split(',')[0]} ({S[st]['lat']:+.1f})" for st in TEN))
print('\nA. how often an odd month lies between its two odd neighbours (two months on each side), widened by 0.10 magnitude; months March 2022 to September 2023')
tot = 0; inside = 0
for st in TEN:
    a = S[st]['a']; n = 0; i = 0
    for k in ODD:
        if not ((2022, 3) <= k <= (2023, 9)): continue
        p, q = nb(k)
        if k in a and p in a and q in a:
            n += 1; lo, hi = min(a[p], a[q]) - 0.10, max(a[p], a[q]) + 0.10; i += lo <= a[k] <= hi
    tot += n; inside += i; print(f"   {TP.PLACE[st].split(',')[0]:<22} {i} of {n}")
print(f'   all ten: {inside} of {tot} ({100 * inside / tot:.0f} in 100)')
tot = 0; inside = 0
for st in TP.north:
    a = S[st]['a']
    for k in ODD:
        if not ((2022, 3) <= k <= (2023, 9)): continue
        p, q = nb(k)
        if k in a and p in a and q in a: tot += 1; lo, hi = min(a[p], a[q]) - 0.10, max(a[p], a[q]) + 0.10; inside += lo <= a[k] <= hi
print(f'   the northern photometers, the same rule: {inside} of {tot} ({100 * inside / tot:.0f} in 100)')
print('\nB. the ten, month by month: the middle (magnitudes), how many have the month, how many are brighter by 0.10 or more')
for k in ODD:
    v = [S[st]['a'][k] for st in TEN if k in S[st]['a']]
    if k[0] in (2022, 2023) and v: print(f"   {k[0]}-{k[1]:02d}  {np.median(v):+.2f}  ({len(v)})  {sum(1 for x in v if x <= -0.10)} of {len(v)}")
print('   south of 25 degrees south only, brighter by 0.10 or more: ' + ', '.join(f"{k[0]}-{k[1]:02d} {sum(1 for st in TEN if S[st]['lat'] < -25 and k in S[st]['a'] and S[st]['a'][k] <= -0.10)} of {sum(1 for st in TEN if S[st]['lat'] < -25 and k in S[st]['a'])}" for k in ODD if k[0] == 2022))
print('   Réunion, 2022: ' + ', '.join(f"{m:02d} {S['stars251']['a'][(2022, m)]:+.2f}" for m in (1, 3, 5, 7, 9, 11) if (2022, m) in S['stars251']['a']) + '; San Pedro de Atacama, 2022: ' + ', '.join(f"{m:02d} {S['stars391']['a'][(2022, m)]:+.2f}" for m in (1, 3, 5, 7, 9, 11) if (2022, m) in S['stars391']['a']))
print('\nC. the five northern photometers of the seventh sheet, odd months of 2022 and 2023: the middle and how many give it')
for k in ODD:
    v = [S[st]['a'][k] for st in NORTH5 if st in S and k in S[st]['a']]
    if k[0] in (2022, 2023) and v: print(f"   {k[0]}-{k[1]:02d}  {np.median(v):+.2f}  ({len(v)})   each: " + ' '.join(f'{x:+.2f}' for x in v))
w = [abs(np.median([S[st]['a'][k] for st in NORTH5 if st in S and k in S[st]['a']])) <= 0.08 for k in ODD if k[0] == 2022 and sum(1 for st in NORTH5 if st in S and k in S[st]['a']) >= 3]
print(f'   odd months of 2022 with three or more of the five: {len(w)}; the middle within 0.08 of nothing in {sum(w)}')
print('\nD. is July 2022 the brightest month of the middle of the ten? ' + ', '.join(f"{k[1]:02d} {np.median([S[st]['a'][k] for st in TEN if k in S[st]['a']]):+.2f}" for k in ODD if k[0] == 2022))
