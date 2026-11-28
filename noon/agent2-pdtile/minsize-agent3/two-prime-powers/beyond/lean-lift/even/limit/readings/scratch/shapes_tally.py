import re, sys, collections
ms = []; kinds = collections.Counter(); par = collections.Counter(); mx = {0: 0.0, 1: 0.0}
for line in open(sys.argv[1], encoding='utf-8'):
    m = re.match(r'^([^:]+): Z_(\d+) heavy .* m = (\d+) \((even|odd)\) share/c_m = ([0-9.]+)', line)
    if not m: continue
    kinds[m.group(1)] += 1; mm = int(m.group(3)); ms.append(mm); par[mm % 2] += 1
    mx[mm % 2] = max(mx[mm % 2], float(m.group(5)))
print(len(ms), 'lines; m from', min(ms), 'to', max(ms), '; even', par[0], 'odd', par[1]); print(dict(kinds)); print('largest share/c_m even, odd:', mx)
