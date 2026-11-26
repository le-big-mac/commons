"""Read the twelve-run sweep kept with the field guide (/srv/commons/guide/data/habitat12.pkl; same settings as the study's
population table: games of 100 rounds on average, one mutant a generation, 200,000 generations) and print, for each population
size and share of slips: mean share of cooperative moves with its standard error, and the share of generations in which
all-defect, and the three-state machine at any of its three entry states, was the commonest machine.
usage: sweep_check.py   (reads only; the pickle holds plain lists, dicts, numbers and strings: checked with pickletools first)"""
import pickle, math, collections
rows = pickle.load(open('/srv/commons/guide/data/habitat12.pkl', 'rb'))
print(len(rows), 'runs; keys', sorted(rows[0].keys()))
print('example dom entries:', rows[0]['dom'][:3])
HAND = {'0:D[0,1] 1:D[0,2] 2:C[2,0]': 'handshake', '0:D[1,2] 1:D[1,0] 2:C[2,1]': 'shifty', '0:C[0,1] 1:D[1,2] 2:D[1,0]': 'wooer'}
ALLD = '0:D[0,0]'
def body(desc):   # "<fsm s0 0:D[0,0]>" -> "0:D[0,0]"
    return desc.split(' ', 2)[2].rstrip('>') if desc.startswith('<') else desc
cells = collections.defaultdict(list)
for r in rows: cells[(r['N'], r['eps'])].append(r)
print('\nN, slips: runs | cooperative moves mean +- se (min..max) | commonest machine, share of generations: all-defect; handshake; shifty; wooer; family')
for (N, e) in sorted(cells):
    rs = cells[(N, e)]; c = [r['coop'] for r in rs]; n = len(c); m = sum(c) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in c) / (n - 1)); se = sd / math.sqrt(n)
    tot = collections.Counter(); gens = 0
    for r in rs:
        g = sum(v for _, v in r['dom']); gens += 200000
        for d, v in r['dom']:
            b = body(d)
            tot['alld' if b == ALLD else HAND.get(b, 'other')] += v
    sh = {k: 100 * v / gens for k, v in tot.items()}
    fam = sh.get('handshake', 0) + sh.get('shifty', 0) + sh.get('wooer', 0)
    print(f'{N:5d} {100*e:4.1f}%: {n:2d} | {100*m:5.1f} +- {100*se:4.1f} ({100*min(c):.0f}..{100*max(c):.0f}) | all-defect {sh.get("alld",0):5.1f}; handshake {sh.get("handshake",0):5.1f}; shifty {sh.get("shifty",0):5.1f}; wooer {sh.get("wooer",0):5.1f}; family {fam:5.1f}   (top-10 lists cover {100*sum(tot.values())/gens:.0f}% of generations)')
