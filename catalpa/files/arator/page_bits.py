# Makes the tables and number lists of arator.html from the program's output files, so that no figure is typed by hand.
# Prints each block between the markers it replaces; with "apply" it writes them into ~/site/arator.html between <!--BEGIN name--> and <!--END name-->.
import json, re, sys
A = '/home/agent1/arator/'
M = json.load(open(A + 'metrics.json')); M2 = json.load(open(A + 'late2_metrics.json')); out = open(A + 'run_all.out').read(); cross = open(A + 'crosscheck.out').read()
PATS = [''.join(p) for p in __import__('itertools').product('DS', repeat=4)]
ROWS = [('geo', 'Virgil, Georgics', '29 BC', 'Georgics'), ('aen', 'Virgil, Aeneid', '19 BC', 'Aeneid'), ('met', 'Ovid, Metamorphoses', 'AD 8', 'Metamorphoses'), ('lucan', 'Lucan', 'c. 65', 'Lucan'),
        ('vflaccus', 'Valerius Flaccus', 'c. 80', 'Valerius Flaccus'), ('thebaid', 'Statius, Thebaid', 'c. 92', 'Thebaid'), ('achilleid', 'Statius, Achilleid', 'c. 95', 'Achilleid'), ('juvenal', 'Juvenal', 'c. 120', 'Juvenal'),
        ('juvencus', 'Juvencus', 'c. 330', None), ('ausonius', 'Ausonius, Mosella', 'c. 371', None), ('claudian', 'Claudian', 'c. 400', 'Claudian (c. 400)'), ('prudentius', 'Prudentius, Psychomachia', 'c. 405', None),
        ('sedulius', 'Sedulius', 'c. 430', 'Sedulius (5th c.)'), ('dracontius', 'Dracontius', 'c. 490', None), ('arator', 'Arator', '544', 'Arator'), ('corippus', 'Corippus', 'c. 550', None)]
NEW = ('juvencus', 'ausonius', 'prudentius', 'dracontius', 'corippus')
def m(k): return M2[k] if k in NEW else M[k]
ref = {}
for line in out.split('\n'):
    mm = re.match(r'\s+(\S.*?)\s+(\d+)\s+([\d.]+)%\s+\(.*?\)\s+(\w{4})\s+([\d.]+)%.*\[([\d.]+)%, (\w{4}) ([\d.]+)%, ([\d.]+)\]', line)
    if mm: ref[mm.group(1)] = (mm.group(6), mm.group(7), mm.group(8), mm.group(9))
B = {}
rows = ['<tr><th>poem</th><th>date</th><th class="n">lines scanned</th><th class="n">dactyls in feet 1 to 4</th><th class="n">in each foot</th><th>commonest pattern</th><th class="n">elisions per 100 lines</th></tr>']
for k, name, date, rname in ROWS:
    x = m(k); r = ref.get(rname) if rname else None; b = ('<strong>', '</strong>') if k == 'arator' else ('', '')
    d = f'{100 * x["dact"]:.1f}%' + (f' [{r[0]}]' if r else ''); c = f'{x["first"][0]} {100 * x["first"][1] / x["n"]:.1f}%' + (f' [{r[2]}]' if r else ''); e = f'{x["el"]:.1f}' + (f' [{r[3]}]' if r else '')
    rows.append(f'<tr><td>{b[0]}{name}{b[1]}</td><td>{date}</td><td class="n">{x["n"]:,}</td><td class="n">{b[0]}{d}{b[1]}</td><td class="n">{", ".join(f"{100 * f:.0f}" for f in x["feet"])}</td><td>{c}</td><td class="n">{b[0]}{e}{b[1]}</td></tr>')
B['numbers'] = '\n'.join(rows)
def pats(k): return ', '.join(f'{p} {100 * v:.1f}' for p, v in sorted(zip(PATS, m(k)['dist']), key=lambda t: -t[1]))
B['patterns_arator'] = pats('arator'); B['patterns_aeneid'] = pats('aen')
agree = dict(re.findall(r'\n\s+(\S.*?)\s+(\d+) regular lines; same pattern as the reference\s+([\d.]+)%', out) and [(a, (b, c)) for a, b, c in re.findall(r'\n\s+(\S.*?)\s+(\d+) regular lines; same pattern as the reference\s+([\d.]+)%', out)])
own = {a: c for a, b, c in re.findall(r'\n(\w+): \d+ lines, (\d+) with a regular reference pattern; scanned \d+ \([\d.]+%\); same pattern as the reference \d+ = ([\d.]+)% of all', '\n' + cross)}
old = open(A + 'run_all_before_26nov_mends.out').read()
agree_old = {a: c for a, b, c in re.findall(r'\n\s+(\S.*?)\s+(\d+) regular lines; same pattern as the reference\s+([\d.]+)%', old)}
rows = ['<tr><th>poem</th><th class="n">regular lines in the answer sheet</th><th class="n">same feet, learning from the eleven poems together</th><th class="n">the same before the mends of 26 November</th><th class="n">learning from the poem alone</th></tr>']
for k, name, date, rname in ROWS[:8]:
    rows.append(f'<tr><td>{name}</td><td class="n">{int(agree[rname][0]):,}</td><td class="n">{agree[rname][1]}%</td><td class="n">{agree_old[rname]}%</td><td class="n">{own[k]}%</td></tr>')
B['test'] = '\n'.join(rows)
if len(sys.argv) > 1 and sys.argv[1] == 'apply':
    p = '/home/agent1/site/arator.html'; s = open(p).read()
    for k, v in B.items():
        a, b = f'<!--BEGIN {k}-->', f'<!--END {k}-->'
        assert s.count(a) == 1 and s.count(b) == 1, k
        s = s[:s.index(a) + len(a)] + v + s[s.index(b):]
    open(p, 'w').write(s); print('applied', list(B))
else:
    for k, v in B.items(): print(f'=== {k}\n{v}\n')

# ---- the same tables in markdown, for README.md
def md_tables():
    T = {}
    rows = ['| poem | regular lines | learning from the eleven poems together | the same before the mends of 26 Nov | learning from the poem alone | the same before |', '|---|---|---|---|---|---|']
    own_old = {a: c for a, b, c in re.findall(r'\n(\w+): \d+ lines, (\d+) with a regular reference pattern; scanned \d+ \([\d.]+%\); same pattern as the reference \d+ = ([\d.]+)% of all', '\n' + open(A + 'crosscheck_before_26nov_mends.out').read())}
    for k, name, date, rname in ROWS[:8]:
        rows.append(f'| {name} | {int(agree[rname][0]):,} | {agree[rname][1]}% | {agree_old[rname]} | {own[k]} | {own_old.get(k, "")} |')
    T['test'] = '\n'.join(rows)
    rows = ['| poem | date | lines scanned | dactyls, feet 1–4 | by foot | commonest pattern | first eight patterns | elisions per 100 lines |', '|---|---|---|---|---|---|---|---|']
    for k, name, date, rname in ROWS:
        x = m(k); r = ref.get(rname) if rname else None; b = '**' if k == 'arator' else ''
        rows.append(f'| {b}{name}{b} | {date} | {x["n"]:,} | {b}{100 * x["dact"]:.1f}%{b}' + (f' [{r[0]}]' if r else '') + f' | {", ".join(f"{100 * f:.0f}" for f in x["feet"])} | {x["first"][0]} {100 * x["first"][1] / x["n"]:.1f}%' + (f' [{r[2]}]' if r else '') + f' | {100 * x["top8"]:.1f}% | {b}{x["el"]:.1f}{b}' + (f' [{r[3]}]' if r else '') + ' |')
    T['measures'] = '\n'.join(rows)
    E = {}
    for line in open(A + 'elision_kinds.out').read().split('\n')[1:]:
        f = line.replace('|', ' ').split()
        if len(f) >= 11: E[f[0]] = f
    rows = ['| poem | lines | places | per 100 lines | word in -que | before est/es | vowel + m | other | -que and est as share of all | per 100 without est/es | per 100, vowel + m and other only |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for k, name, date, rname in ROWS:
        f = E[k]; b = '**' if k == 'arator' else ''
        rows.append(f'| {b}{name}{b} | {int(f[1]):,} | {int(f[2]):,} | {f[3]} | {int(f[4]):,} | {f[5]} | {int(f[6]):,} | {int(f[7]):,} | {b}{f[10]}{b} | {f[8]} | {f[9]} |')
    T['elisions'] = '\n'.join(rows)
    return T
if len(sys.argv) > 1 and sys.argv[1] == 'apply':
    p = A + 'README.md'; s = open(p).read()
    for k, v in md_tables().items():
        a, b = f'<!--BEGIN {k}-->', f'<!--END {k}-->'
        assert s.count(a) == 1 and s.count(b) == 1, k
        s = s[:s.index(a) + len(a)] + '\n' + v + '\n' + s[s.index(b):]
    open(p, 'w').write(s); print('README tables applied')
