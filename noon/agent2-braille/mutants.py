"""mutants.py: cells.py, study.py and speech.py broken on purpose, one fault at a time, and test.py run on each broken copy.
    /usr/bin/python3 -I mutants.py      (a control run of the true programs first; it must pass)"""
import os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
M = [
 ('cells.py', "out.append((core.lower(), b2[r2[i]:r2[i] + cells], sum(c1[i:j]) - cells, whole))", "out.append((core.lower(), b2[r2[i]:r2[i] + cells], sum(c1[i:j]), whole))", 'a unit saves all its uncontracted cells'),
 ('cells.py', "core = span.strip()", "core = span", 'the joined words of the American code are lost (the first run\'s fault)'),
 ('cells.py', "whole = (k0 == 0 or not par[k0 - 1].isalpha()) and (k1 == n or not par[k1].isalpha())", "whole = (k0 == 0 or not par[k0 - 1].isalpha()) or (k1 == n or not par[k1].isalpha())", 'a part at the head or foot of a word counts as a whole word'),
 ('cells.py', "if j - i > 1 and core.isalpha() and len(core) > 1:", "if j - i > 1 and core.isalpha() and len(core) > 2:", 'signs of two letters are dropped'),
 ('cells.py', ".replace('–', '-').replace('_', '')", ".replace('–', '-')", 'underscores are left in'),
 ('cells.py', "if a: t = t[a.end():]", "if a: t = t", 'the head of the file is not cut off'),
 ('cells.py', "if b: t = t[:t.index(b.group(0))] if b.group(0) in t else t", "if b: t = t", 'the foot of the file is not cut off'),
 ('cells.py', "t = re.sub(r'\\[Illustration[^\\]]*\\]', ' ', t)", "t = t", 'picture notes are left in'),
 ('cells.py', "out['in'] = len(re.findall(r'(?<!9)9(?!9)', b))", "out['in'] = b.count('9')", 'an asterisk counts as two of the sign for in'),
 ('cells.py', "out = {w: b.count(c) for w, c in STRONG.items()}", "out = {w: b.count(c + ' ') for w, c in STRONG.items()}", 'the five strong signs are counted only at the end of a word'),
 ('cells.py', "toks = re.findall(r\"[A-Za-z]+(?:'[A-Za-z]+)?\", par); words += len(toks)", "toks = re.findall(r\"[A-Za-z]+\", par); words += len(toks)", 'a word with an apostrophe is two words'),
 ('cells.py', "letters += sum(ch.isalpha() for ch in par)", "letters += sum(ch.isalnum() or ch == ' ' for ch in par)", 'spaces are counted as letters'),
 ('cells.py', "c1 = [(r1[i + 1] if i + 1 < n else len(b1)) - r1[i] for i in range(n)]", "c1 = [(r1[i + 1] if i + 1 < n else r1[i]) - r1[i] for i in range(n)]", 'the last character of a paragraph has no cells'),
 ('cells.py', "caps.update(w.lower() for w in toks if w[0].isupper())", "caps.update(w.lower() for w in toks if w.isupper())", 'only words all in capitals count as having a capital'),
 ('cells.py', "k = span + ('|w' if whole else '|p'); by[k][0] += 1; by[k][1] += saved", "k = span + ('|w' if whole else '|p'); by[k][0] += 1; by[k][1] += saved + 1", 'every unit saves one cell more'),
 ('study.py', "def S(rec, code='ueb'): r = rec[code]; return (r['U'] - r['C']) / r['U']", "def S(rec, code='ueb'): r = rec[code]; return (r['U'] - r['C']) / r['C']", 'the share is taken of the contracted cells'),
 ('study.py', "U += r['U']; C += r['C']; W += r['words']", "U += r['U']; C += r['C']; W = r['words']", 'pooled words are the last book\'s'),
 ('study.py', "for k, v in r['by'].items(): by[k][0] += v[0]; by[k][1] += v[1]", "for k, v in r['by'].items(): by[k][0] += v[0]; by[k][1] = v[1]", 'pooled savings are the last book\'s'),
 ('study.py', "return 1e5 * p['by'].get(label, [0, 0])[what] / p['words']", "return 1e6 * p['by'].get(label, [0, 0])[what] / p['words']", 'per million called per hundred thousand'),
 ('study.py', "if kind == 'shortform': return any(k.split('|')[0].startswith(sign) for k in p['by'])", "if kind == 'shortform': return any(k.split('|')[0] == sign for k in p['by'])", 'a shortform inside a longer word does not count'),
 ('study.py', "if kind in WORD_KINDS: return (sign + '|w') in p['by']", "if kind in WORD_KINDS: return (sign + '|w') in p['by'] or (sign + '|p') in p['by']", 'a wordsign occurs when its letters are part of a word'),
 ('study.py', "own = p['vocab'].get(w, 0) * (cost('x' + w) - 1 - 1)", "own = p['vocab'].get(w, 0) * (cost('x' + w) - 1)", 'a letter-word\'s worth forgets the cell its sign takes'),
 ('study.py', "worth = n * (cost(cand) - 1)", "worth = n * cost(cand)", 'a candidate word\'s worth forgets the cell a sign would take'),
 ('study.py', "if names_out is not None and cand in names_out: continue", "if names_out is not None and cand in names_out: pass", 'names are not set aside'),
 ('study.py', "if cand[0] != L or cand == w or len(cand) < 2 or not cand.isalpha(): continue", "if cand == w or len(cand) < 2 or not cand.isalpha(): continue", 'any word may stand for any letter'),
 ('story.py', "hits = [i for i, p in enumerate(paras) if re.search(end, p) and i > a[0]]; assert hits, ('the paragraph after the story is not found', folder); b = hits[-1]", "hits = [i for i, p in enumerate(paras) if re.search(end, p) and i > a[0]]; assert hits, ('the paragraph after the story is not found', folder); b = hits[0]", 'the story ends at the first paragraph like its end, not the last'),
 ('story.py', "hits = [i for i, p in enumerate(paras) if re.search(end, p) and i > a[0]]", "hits = [i for i, p in enumerate(paras) if re.search(end, p)]", 'an end mark before the story\'s start counts'),
 ('story.py', "return [re.sub(r'^=+ (.*?) =+$', r'\\1', p) for p in paras[a[0]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[')]", "return [re.sub(r'^=+ (.*?) =+$', r'\\1', p) for p in paras[a[0]:b] if not p.startswith('[[')]", 'rules and rows of stars are kept'),
 ('story.py', "return [re.sub(r'^=+ (.*?) =+$', r'\\1', p) for p in paras[a[0]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[')]", "return [re.sub(r'^=+ (.*?) =+$', r'\\1', p) for p in paras[a[0]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[This chapter')]", 'the bookshops\' addresses are kept'),
 ('story.py', "return [re.sub(r'^=+ (.*?) =+$', r'\\1', p) for p in paras[a[0]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[')]", "return [p for p in paras[a[0]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[')]", 'the rules of = stay on the headings'),
 ('story.py', "return [re.sub(r'^=+ (.*?) =+$', r'\\1', p) for p in paras[a[0]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[')]", "return [re.sub(r'^=+ (.*?) =+$', r'\\1', p) for p in paras[a[-1]:b] if any(ch.isalpha() for ch in p) and not p.startswith('[[')]", 'the story starts at the last paragraph like its start'),
 ('story.py', "if end is None: b = len(paras)", "if end is None: b = len(paras) - 1", 'a story that runs to the end loses its last paragraph'),
 ('cells.py', "    for par in (trim(clean(path)) if trim else clean(path)):", "    for par in clean(path):", 'the cut to the story is never made'),
 ('speech.py', "if ch == '\"': bins.append('mark'); inside = not inside", "if ch == '\"': bins.append('mark')", 'nothing is ever inside the marks'),
 ('speech.py', "if ch == '\"': bins.append('mark'); inside = not inside", "if ch == '\"': bins.append('in' if inside else 'out'); inside = not inside", 'the marks are counted with the text'),
 ('speech.py', "else: bins.append('in' if inside else 'out')", "else: bins.append('out' if inside else 'in')", 'inside and outside are exchanged'),
 ('speech.py', "out[bins[i]][2] += par[i].isalpha()", "out[bins[i]][2] += 1", 'every character counts as a letter'),
 ('speech.py', "out[bins[i]][1] += (r2[j] if j < n else len(b2)) - r2[i]; i = j", "out[bins[i]][1] += (r2[j] if j < n else len(b2)) - r2[i] + (bins[i] == 'in'); i = j", 'every group inside the marks takes a cell more'),
 ('speech.py', "out[bins[i]][0] += (r1[i + 1] if i + 1 < n else len(b1)) - r1[i]", "out[bins[i]][0] += (r1[i + 1] if i + 1 < n else r1[i]) - r1[i]", 'the last character has no uncontracted cells'),
]
def run(mut=None):
    with tempfile.TemporaryDirectory() as t:
        for f in ('cells.py', 'study.py', 'speech.py', 'run.py', 'story.py'):
            s = open(os.path.join(HERE, f), encoding='utf-8').read()
            if mut and mut[0] == f:
                assert s.count(mut[1]) == 1, 'this fault does not find its text exactly once: ' + mut[3]; s = s.replace(mut[1], mut[2])
            open(os.path.join(t, f), 'w', encoding='utf-8').write(s)
        r = subprocess.run(['/usr/bin/python3', '-I', os.path.join(HERE, 'test.py')], env=dict(os.environ, BRAILLE_CODE=t), capture_output=True, text=True, timeout=300)
        fails = [l for l in r.stdout.splitlines() if l.startswith('FAILED')]
        return r.returncode, fails, r.stderr.strip().splitlines()[-1:] 
if __name__ == '__main__':
    code, fails, err = run(); print('control (the true programs): %s' % ('passes' if code == 0 else 'FAILS %s %s' % (fails, err))); assert code == 0
    caught = 0
    for m in M:
        code, fails, err = run(m); caught += code != 0
        print('%-10s %-66s %s' % (m[0], m[3], ('caught: ' + (fails[0][8:80] if fails else 'the program stopped: ' + ' '.join(err)[:60])) if code else 'PASSED, not caught'))
    print('%d of %d broken copies caught' % (caught, len(M)))
