# rmutants.py -- broken copies of rcore.js, each run through rtest.js.   python -I rmutants.py
import os, subprocess, shutil
here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'rcore.js'), encoding='utf-8').read()
M = [
 ('partners-fewest-first', "a word's partners come the rarest first", "return b.n - a.n ||", "return a.n - b.n ||"),
 ('partners-same-word', "a word is given as its own partner", "D.words[p[0] === w ? p[1] : p[0]]", "D.words[p[0] === w ? p[0] : p[1]]"),
 ('tally-swapped', "rhymes that fail are tallied as rhyming", "if (list[i].ok === 1) t.still += list[i].n; else if (list[i].ok === 0) t.not += list[i].n;", "if (list[i].ok === 0) t.still += list[i].n; else if (list[i].ok === 1) t.not += list[i].n;"),
 ('fails-any-poet', "the list for a poet is the list for all poets", "if (poet >= 0 && p !== poet) continue;", ""),
 ('fails-any-family', "the list for a family is the list for all families", "if (fam >= 0 && f !== fam) continue;", ""),
 ('pair-one-way', "a pair is found only when its words are given in the order stored", "(X.failsPair[a < b ? a + '/' + b : b + '/' + a] || []).slice()", "(X.failsPair[a + '/' + b] || []).slice()"),
 ('rate-over-all-pairs', "the rate is taken over all a poet's pairs, not those that could be judged", "var ev = D.poets[poet].evaluable; return ev ? 1000 * D.families[fam].byPoet[poet] / ev : 0;", "var ev = D.poets[poet].pairs; return ev ? 1000 * D.families[fam].byPoet[poet] / ev : 0;"),
 ('group-rate-of-poet', "a group's rate is read from the poets' column", "1000 * D.families[fam].byGroup[g] / ev", "1000 * D.families[fam].byPoet[g] / ev"),
 ('clean-keeps-case', "capitals are kept", "String(s).toLowerCase().replace(/[^a-z]/g, '')", "String(s).replace(/[^a-zA-Z]/g, '')"),
 ('poets-off-by-one', "every poet of a pair is read as the next poet", "out.push(PCH.indexOf(s.charAt(i)))", "out.push(PCH.indexOf(s.charAt(i)) + 1)"),
 ('second-word-unindexed', "a pair is filed under its first word only", "if (p[1] !== p[0]) (byWord[p[1]] = byWord[p[1]] || []).push(i);", ""),
 ('fails-unsorted', "the failing pairs are listed family by family, not in the corpus's order", "out.sort(function (a, b) { return a - b; }); return out;", "return out;"),
 ('inherited-keys', "the word lists are ordinary objects, so 'constructor' looks like a word", "widx = Object.create(null),", "widx = {},"),
 ('pct-truncates', "percentages are cut, not rounded", "(Math.round(x * 10) / 10).toFixed(1)", "(Math.floor(x * 10) / 10).toFixed(1)"),
]
for name, what, a, b in M: assert src.count(a) == 1, name
d = os.path.join(here, 'mutants', 'rcore'); shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, 'out'))
for f in ['rtest.js', 'data.json', 'expect.json']: shutil.copy(os.path.join(here, f), d)
for f in ['score.json', 'families.json']: shutil.copy(os.path.join(here, 'out', f), os.path.join(d, 'out'))
caught = 0
for name, what, a, b in M:
    open(os.path.join(d, 'rcore.js'), 'w', encoding='utf-8').write(src.replace(a, b))
    try:
        r = subprocess.run(['node', 'rtest.js'], cwd=d, capture_output=True, text=True, timeout=120); nf = [l for l in r.stdout.split('\n') if l.startswith('FAIL')]
        res = ('caught: %d of the tests fail (%s)' % (len(nf), nf[0][6:66])) if nf else ('caught: the tests stop with an error' if r.returncode else 'NOT caught: every test passes')
    except subprocess.TimeoutExpired: res = 'caught: the tests do not finish'
    caught += res.startswith('caught'); print('%-24s %s -- %s' % (name, what, res), flush=True)
print('\n%d of %d broken copies of rcore.js caught' % (caught, len(M)))
