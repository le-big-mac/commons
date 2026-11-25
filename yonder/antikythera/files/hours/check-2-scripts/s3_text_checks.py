"""Second reading: checks on the files and the text. Nothing is written outside this folder; apply_check.py and apply_after.py are read, not run.
 A. README-as-read.md with the first reader's 31 changes gives check-scripts/README.proposed.md; that with the replacements of apply_after.py
    (taken from its source by parsing, not by running it) gives README.md.
 B. The quotations in README.md from Carman and Evans, Jones and Iversen and Jones, looked for in the saved texts of the papers (white space and
    line-end hyphens removed).
 C. hours_after.py against hours_after.py.first; the lines of hours_after.out against check-scripts/c6b_author_fix.out.
 D. Which of the first reader's new figures after_check.out holds.
usage: s3_text_checks.py   (under -I -B)"""
import os, re, json, ast, difflib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); DL = '/home/agent3/downloads'
rd = lambda *p: open(os.path.join(*p), encoding='utf-8', errors='replace').read()

print('A. the pasting')
t = rd(ROOT, 'README-as-read.md'); ch = json.load(open(os.path.join(ROOT, 'check-scripts', 'changes.json'), encoding='utf-8'))
for c in ch:
    assert t.count(c['old']) == 1, c['id']; t = t.replace(c['old'], c['new'])
prop = rd(ROOT, 'check-scripts', 'README.proposed.md')
print(f'   changes: {len(ch)} ({sum(1 for c in ch if c.get("must"))} must); README-as-read.md with them equals README.proposed.md: {t == prop}')
tree = ast.parse(rd(ROOT, 'apply_after.py')); reps = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'rep':
        reps.append((ast.literal_eval(node.args[0]), ast.literal_eval(node.args[1])))
reps.sort(key=lambda r: prop.find(r[0]))
u = prop
for old, new in reps:
    assert u.count(old) == 1, old[:40]; u = u.replace(old, new)
now = rd(ROOT, 'README.md')
print(f'   replacements in apply_after.py: {len(reps)}; README.proposed.md with them equals README.md: {u == now}')
if u != now:
    for line in list(difflib.unified_diff(u.splitlines(), now.splitlines(), lineterm='', n=0))[:20]: print('     ', line[:200])
added = [l for l in difflib.ndiff(prop.split(), now.split()) if l.startswith('+ ')]
print(f'   words in README.md: {len(now.split())}; words added after the reader\'s version: {len(added)}')

print('\nB. quotations')
def norm(s):
    s = s.replace('­', '').replace('−', '-').replace('–', '-').replace('’', "'").replace('“', '"').replace('”', '"')
    s = re.sub(r'-\s*\n\s*', '', s)            # line-end hyphens
    return re.sub(r'\s+', ' ', s).lower()
src = {'Carman and Evans': norm(rd(DL, 'carman-evans-2014', 'paper.txt')), 'Jones 2020': norm(rd(DL, 'jones-2020-isaw17', 'page.txt')),
       'Iversen and Jones': norm(rd(DL, 'iversen-jones-2019', 'paper.txt'))}
Q = [('Carman and Evans', 'may be used to restrict the solutions to a single Saros eclipse series'), ('Carman and Evans', 'rule of 8 h'),
     ('Carman and Evans', 'with the exeligmos dial set at 0'), ('Carman and Evans', 'the solar eclipse times are of lower quality'),
     ('Carman and Evans', 'are -257 and -149 so far from the bottom of the well that they must be excluded?'),
     ('Carman and Evans', 'no part of the Greek world of the eastern Mediterranean may be safely ruled out on the basis of the eclipse times alone'),
     ('Carman and Evans', 'the Aegean Sea with an uncertainty of about an hour of longitude'),
     ('Jones 2020', 'on average about as good'), ('Jones 2020', 'many more'), ('Iversen and Jones', 'n[ighttime], at the 2nd hour')]
for who, q in Q:
    n = src[who].count(norm(q))
    if n == 0:   # try without hyphen handling differences
        n = re.sub(r'[^a-z0-9]', '', src[who]).count(re.sub(r'[^a-z0-9]', '', norm(q)))
        tag = f'{n} (letters and figures only)'
    else: tag = str(n)
    print(f'   {who}: "{q}": found {tag}')
ij = rd(DL, 'iversen-jones-2019', 'paper.txt').splitlines()
for n, line in enumerate(ij):
    if line.startswith('Cell 72 '):
        print('   Iversen and Jones, the edition\'s entry for cell 72 (right-hand column):', ' / '.join(x.split('  ')[-1].strip() for x in ij[n:n + 3]))

print('\nC. the rerun with 72S of the night')
a = rd(ROOT, 'hours_after.py.first').splitlines(); b = rd(ROOT, 'hours_after.py').splitlines()
d = [(x, y) for x, y in zip(a, b) if x != y]
print(f'   lines: {len(a)} and {len(b)}; lines that differ: {len(d)}; every difference is "72S 2d" to "72S 2n" or (72, \'S\', 2, \'d\') to \'n\':',
      all(x.replace("72S 2d", "72S 2n").replace("(72, 'S', 2, 'd')", "(72, 'S', 2, 'n')") == y for x, y in d))
out = rd(ROOT, 'hours_after.out'); c6 = rd(ROOT, 'check-scripts', 'c6b_author_fix.out')
for label in ('72S 2n added (26 hours)', 'the same with 8S 4d'):
    line = [l for l in out.splitlines() if label in l][0]
    nums = re.findall(r'(\d+) BC (\d\.\d\d) h at ([+-]\d+)', line) + re.findall(r'twelve (\d\.\d\d)', line)
    ok = all(f'{bc} BC {s} h at {lon}' in c6 for bc, s, lon in nums[:4]) and f'twelve {nums[4]} h' in c6
    print(f'   "{label}": {nums}; the same figures stand in c6b_author_fix.out: {ok}')
mine = re.findall(r'at 205 BC, (\w+): engraved \d+ h, real [\d.]+ h, difference ([+-][\d.]+)', out)
theirs = re.findall(r'at 205 BC \([^)]*\), (\w+): engraved \d+ h, difference ([+-][\d.]+)', c6)
print(f'   glyph-by-glyph differences printed for the 26 hours: {len(mine[2:])} in hours_after.out, {len(theirs)} in c6b_author_fix.out; equal: {mine[2:] == theirs}')

print('\nD. the first reader\'s new figures, and where a recomputation by the author stands')
ac = rd(ROOT, 'after_check.out'); ha = out
F = [('101 under 3.0 h, one start in 37', 'under 3.0 h: 101' in ac and 'one in 36.7' in ac, 'after_check.out'),
     ('259, 205, 151 BC at 26 E: 3.37, 2.56, 3.01', all(x in ac for x in ('18 3.37', '18 2.56', '18 3.01')), 'after_check.out'),
     ('259 BC free: 3.20 at 10 E, 3.67 at 20 E', '3.20 h at +10.25' in ac and '3.67 h at +19.75' in ac, 'after_check.out'),
     ('with 8 or 16 h added: 21, 31, 36 E', all(x in ac for x in ('with 16 h +21.00', 'the longitude is +31.00', 'with 16 h +35.75')), 'after_check.out'),
     ('187 BC ahead by 0.03 h', '2.556' in ac and '2.523' in ac, 'after_check.out'),
     ('26 hours: 3.33, 3.46, 3.70, 3.87; 4.64', '223 BC 3.33 h' in ha and 'twelve 4.64' in ha, 'hours_after.out'),
     ('the six differences at 26 E (-1.6, +6.3, -1.6, +1.3 or +4.3, -0.1, -4.0)', '-1.61' in ac or '-1.61' in ha, 'neither (only check-scripts/c6b_author_fix.out)'),
     ('thirty starts: 185.4 and 181.5', '185.4' in ac or '185.4' in ha, 'neither (173.3 + 12.1 and 161.5 + 20.0 from hours_after.out)')]
for name, ok, where in F: print(f'   {name}: {"in " + where if ok else "NOT recomputed by the author: " + where}')
print('   figures that rest on the reader\'s own code and other data, cited to the reader\'s files and not recomputable with this folder\'s code:')
for name, f, pat in (('1,435 eclipses, within 19 minutes', 'c3_phases.out', r'1435'), ('Delta T 66 s and 49 s above the catalogue', 'c3_phases.out', r'\b66\b|\b49\b'),
                     ('24 under 3.0 h with the catalogue\'s Delta T', 'c4c_greek.out', r'\b24\b'), ('0.12 h rms against Table 16', 'c2_ruler.out', r'0\.12'),
                     ('Jones\'s full moons 17 minutes earlier', 'c2b_jones_table1.out', r'17\.\d'), ('205 BC at 25.5 E by JPL and the catalogue', 'c2_ruler.out', r'\+ *25\.50')):
    s = rd(ROOT, 'check-scripts', f); hit = [l.strip()[:150] for l in s.splitlines() if re.search(pat, l)]
    print(f'     {name}: {f}: {len(hit)} line(s), e.g. {hit[0] if hit else "NONE"}')
