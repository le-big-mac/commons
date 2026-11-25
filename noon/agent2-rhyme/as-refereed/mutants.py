# mutants.py -- can the tests fail?  Copies of the programs, each with one thing wrong; for each, the corpus is parsed and scored
# again by the broken copy and ptest.py is run on the result.   python -I mutants.py DATA_DIR
import os, sys, shutil, subprocess, filecmp
here = os.path.dirname(os.path.abspath(__file__)); data = sys.argv[1]; py = sys.executable
M = [
 ('short-stem-first-vowel', 'rhyme.py', "the stem is taken from the first vowel of the word, not the last (American)", "i = max(k for k, (p, s) in enumerate(pron) if s is not None); return tuple(p for p, s in pron[i:])", "i = min(k for k, (p, s) in enumerate(pron) if s is not None); return tuple(p for p, s in pron[i:])"),
 ('long-stem-is-short', 'rhyme.py', "the stem from the stressed vowel is taken from the last vowel whatever its stress", "i = one[-1] if one else two[-1] if two else v[0]; return tuple(p for p, s in pron[i:])", "i = v[-1]; return tuple(p for p, s in pron[i:])"),
 ('linking-r-kept', 'rhyme.py', "the British dictionary's linking r is kept as part of the word", "if ph[-1] == 'r' and len(ph) > 1 and ph[-2] in BEEP_V: ph = ph[:-1]", "pass"),
 ('british-stem-first-vowel', 'rhyme.py', "the British stem is taken from the first vowel", "return tuple(pron[v[-1]:]) if v else None", "return tuple(pron[v[0]:]) if v else None"),
 ('all-variants', 'rhyme.py', "a pair rhymes only if every listed pronunciation of the one matches the other's", "r['as'] = bool(set(x['sa']) & set(y['sa']));", "r['as'] = set(x['sa']) == set(y['sa']);"),
 ('first-is-last', 'rhyme.py', "'first-listed pronunciation' takes the last-listed", "r['a1'] = x['sa'][0] == y['sa'][0]", "r['a1'] = x['sa'][-1] == y['sa'][-1]"),
 ('old-flag-lost-in-judge', 'rhyme.py', "a word reached by an old spelling is not flagged (American)", "r['olda'] = x['ra'].startswith('old') or y['ra'].startswith('old')", "r['olda'] = False"),
 ('british-both-needed', 'rhyme.py', "the British verdict is given though one word is unknown there", "if x['b'] and y['b']:", "if x['b'] or y['b']:"),
 ('no-elisions', 'words.py', "crownd, drest, oer and their like are not respelt", "    for c, rule in elisions(w) + british(w):\n        if c in D: return c, rule", "    for c, rule in british(w):\n        if c in D: return c, rule"),
 ('old-called-elision', 'words.py', "an old spelling is reported as an elision, so its pairs are counted in the main figures", "if c in D: return c, 'old:' + rule\n", "if c in D: return c, 'elision:' + rule\n"),
 ('final-e-always-dropped', 'words.py', "a final e is dropped from any old spelling (clime becomes clim)", "if len(b) > 4 and re.search(r'([aeiou][aeiouwy][b-df-hj-np-tv-z]|[b-df-hj-np-tvxz][b-df-hj-np-tv-z])e$', b):", "if len(b) > 4 and b.endswith('e'):"),
 ('no-british-spellings', 'words.py', "offence, vigour and their like are not looked up by their American spellings", "    for c, rule in elisions(w) + british(w):", "    for c, rule in elisions(w):"),
 ('n-en-anywhere', 'words.py', "an e is put before any final n (mown becomes mowen)", "if len(w) > 3 and w.endswith('n') and w[-2] in 'vlsz':", "if len(w) > 3 and w.endswith('n'):"),
 ('adjacent-lines-only', 'score.py', "only lines next to each other are paired", "            for j in range(i + 1, len(ws)):\n                if sc[i] != sc[j]: continue\n                p = J.pair", "            for j in range(i + 1, min(i + 2, len(ws))):\n                if sc[i] != sc[j]: continue\n                p = J.pair"),
 ('both-dictionaries-must-agree', 'score.py', "a pair counts as rhyming only if it rhymes in both dictionaries", "ev = ea or eb; ok = (ea and p['as']) or (eb and p['bs'])", "ev = ea or eb; ok = (ea and p['as']) and (eb and p['bs'])"),
 ('evaluable-needs-both', 'score.py', "a pair is evaluable only if both dictionaries know it", "ev = ea or eb; ok", "ev = ea and eb; ok"),
 ('old-pairs-evaluable', 'score.py', "pairs reached by old spellings are counted as evaluable", "ea = p['as'] is not None and not p['olda']; eb = p['bs'] is not None and not p['oldb']", "ea = p['as'] is not None; eb = p['bs'] is not None"),
 ('family-great-seat-lost', 'families.py', "great : seat is not told from sea : way", "if 'ea' in iy and 'ea' in ey: return 'great : seat'", "pass"),
 ('family-little-words-lost', 'families.py', "have, are, said and their like have no family of their own", "LITTLE = {'have', 'hath', 'are', 'said', 'says', 'saith', 'shall', 'were', 'wert'}", "LITTLE = set()"),
 ('family-weak-endings-lost', 'families.py', "a full vowel rhymed with a weak ending is not a family", "if c != 'same vowel' and ((weak(a) and full(b)) or (weak(b) and full(a))): return 'dress : idleness'", "pass"),
 ('family-wa-everywhere', 'families.py', "every pair of those vowels is put with war : far, whatever its spelling", "and has_wa(a) != has_wa(b): return 'war : far'", ": return 'war : far'"),
 ('scheme-in-poem', 'parse.py', "the scheme in the context of the poem is used for the stanza's own", "'scheme': [int(x) for x in s1], 'inpoem': [int(x) for x in s2]", "'scheme': [int(x) for x in s2], 'inpoem': [int(x) for x in s1]"),
 ('bad-blocks-kept', 'parse.py', "blocks whose words and scheme differ in length are kept, cut to the shorter", "if len(words) != len(s1) or len(words) != len(s2): bad += 1; continue", "n_ = min(len(words), len(s1), len(s2)); words, s1, s2 = words[:n_], s1[:n_], s2[:n_]"),
 ('first-word-dropped', 'parse.py', "the first end-word of every stanza is lost", "head = b[0].split(); words = head[1:]; s1 = b[1].split(); s2 = b[2].split()", "head = b[0].split(); words = head[2:]; s1 = b[1].split()[1:]; s2 = b[2].split()[1:]"),
]
files = ['parse.py', 'lexicon.py', 'words.py', 'rhyme.py', 'score.py', 'families.py', 'poets.py', 'ptest.py', 'wyld-pairs.txt']
src = {f: open(os.path.join(here, f), encoding='utf-8').read() for f in files}
for name, f, what, a, b in M: assert src[f].count(a) == 1, name
root = os.path.join(here, 'mutants'); caught = 0; passed = []
for name, f, what, a, b in M:
    d = os.path.join(root, name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for g in files: open(os.path.join(d, g), 'w', encoding='utf-8').write(src[g].replace(a, b) if g == f else src[g])
    def run(args, t): return subprocess.run([py, '-I'] + args, cwd=d, capture_output=True, text=True, timeout=t)
    try:
        r1 = run(['parse.py', os.path.join(data, 'rhymedata', 'english_gold'), os.path.join(data, 'rhymedata', 'english_raw'), 'corpus.json'], 120)
        r2 = run(['score.py', data, 'corpus.json', 'out'], 400)
        r2b = run(['families.py', 'out'], 200)
        r3 = run(['ptest.py', data], 400)
        if r1.returncode or r2.returncode or r2b.returncode: res = 'caught: the program stops with an error'
        else:
            nf = [l for l in r3.stdout.split('\n') if l.startswith('FAIL')]
            res = ('caught: %d of the tests fail (%s)' % (len(nf), nf[0][6:70])) if nf or r3.returncode else 'NOT caught: every test passes'
            if not nf and not r3.returncode:
                same = filecmp.cmp(os.path.join(d, 'out', 'pairs.tsv'), os.path.join(here, 'out', 'pairs.tsv'), shallow=False)
                res += '; its pair table is ' + ('the true one, line for line' if same else 'NOT the true one'); passed.append((name, same))
    except subprocess.TimeoutExpired: res = 'caught: the run does not finish'
    caught += res.startswith('caught'); print('%-30s %s -- %s' % (name, what, res), flush=True)
print('\n%d of %d broken copies caught; %d pass the tests%s' % (caught, len(M), len(passed), (', of which %d give the true pair table line for line' % sum(1 for n, s in passed if s)) if passed else ''))
