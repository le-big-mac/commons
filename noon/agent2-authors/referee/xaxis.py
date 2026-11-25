# Sensitivity of the figure's rank correlation to the x-coordinates chosen for the authors and for Noon.
import re
from scipy.stats import spearmanr
pts = []
for line in open('/home/agent2/authors2/time.out'):
    m = re.match(r'(.+?)\s+sheet (\d)\s+([\d.]+) min\s+Brier ([\d.]+)', line)
    pts.append([m.group(1).strip(), m.group(2), float(m.group(3)), float(m.group(4))])
def rho(label, f):
    q = [f(list(p)) for p in pts]
    r = spearmanr([p[2] for p in q], [p[3] for p in q])
    q2 = [p for p in q if p[0] != 'quick reader']
    r2 = spearmanr([p[2] for p in q2], [p[3] for p in q2])
    print(f'{label}: all 17 rho {r.statistic:+.2f} (p {r.pvalue:.3f}); without quick readers rho {r2.statistic:+.2f} (p {r2.pvalue:.3f})')
rho('as typed in figure.py', lambda p: p)
def a(p):
    if p[0] == 'author, quick odds': p[2] = 0.02   # 1.2 s between sheet.md and odds-quick.json
    if p[0] == 'author, careful odds': p[2] = 8.15  # second pass only
    return p
rho('authors quick at 1.2 s after the sheet, careful pass at its own 8.15 min', a)
def b(p):
    if p[0] == 'outsider (Noon)': p[2] = 15.0       # as Noon wrote in both sealed mine.md
    return p
rho('Noon at the 15 min it wrote in mine.md', b)
def c(p):
    if p[0] == 'outsider (Noon)': p[2] = 2.69 + (6.87 if p[1] == '1' else 8.58)  # from the moment the sheet existed
    return p
rho('Noon from the moment each sheet existed (9.6 and 11.3 min)', c)
