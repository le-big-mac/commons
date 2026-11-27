"""Evidence reading 1 of the page set out afresh: the folds against the old text, by program.
usage: python -I ev1_folds.py candidate.html README.md
Independent of the generator: the old text is cut here by my own rules, markup is stripped from both sides by
my own rules, and the two are compared token by token (tokens = runs of non-space characters)."""
import sys, re, html

cand = open(sys.argv[1], encoding='utf-8').read()
readme = open(sys.argv[2], encoding='utf-8').read()

INLINE = r'</?(em|strong|code|a|b|i|span)(\s[^>]*)?>'

def html_tokens(h):
    h = re.sub(INLINE, '', h)            # inline tags vanish
    h = re.sub(r'<[^>]+>', ' ', h)       # every other tag is a space
    return html.unescape(h).split()

def md_tokens(m):
    out = []
    for line in m.split('\n'):
        if re.fullmatch(r'\s*\|(\s*:?-+:?\s*\|)+\s*', line):   # table rule
            continue
        out.append(line)
    m = '\n'.join(out)
    m = m.replace('**', '').replace('*', '').replace('`', '').replace('|', ' ')
    return m.split()

# literal asterisks or pipes that are not markup would be lost by md_tokens: count what there is
print('asterisks in README:', readme.count('*'), ' (all must be emphasis marks; pairs:', readme.count('*') % 2 == 0, ')')
print('backticks in README:', readme.count('`'), ' pipes:', readme.count('|'))

# ---- the old text cut by headings
parts = re.split(r'^## ', readme, flags=re.M)
top = parts[0]
sec = {}
for p in parts[1:]:
    head, body = p.split('\n', 1)
    sec[head.strip()] = body
heads = list(sec)
print('old headings:', heads)
top_paras = [x.strip() for x in re.split(r'\n\s*\n', top) if x.strip()]
print('paragraphs of the old top:', len(top_paras))
for i, p in enumerate(top_paras):
    print('  top para', i, ':', p[:70].replace('\n', ' '), '...', len(p.split()), 'words')

# ---- the folds of the candidate
folds = re.findall(r'<details class="([^"]*)">\s*<summary>(.*?)</summary>(.*?)</details>', cand, flags=re.S)
print('\nfolds in the candidate:', len(folds), '; <details> opened:', cand.count('<details'), 'closed:', cand.count('</details>'))
for cls, summ, inner in folds:
    print('  [%s] %s  (%d tokens)' % (cls, html.unescape(summ), len(html_tokens(inner))))

def compare(name, fold_tok, old_tok):
    if fold_tok == old_tok:
        print('  %s: IDENTICAL, %d tokens' % (name, len(old_tok)))
        return True
    print('  %s: DIFFERENT (fold %d tokens, old %d)' % (name, len(fold_tok), len(old_tok)))
    import difflib
    sm = difflib.SequenceMatcher(None, old_tok, fold_tok, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            print('     ', tag, '| old:', ' '.join(old_tok[max(0, i1 - 4):i2 + 4]), '| fold:', ' '.join(fold_tok[max(0, j1 - 4):j2 + 4]))
    return False

def residue(name, fold_tok, old_tok_list):
    """the fold must be the old token runs, each whole and in the order given, plus other text; print the other text"""
    pos = 0; rest = []; ok = True
    for label, old in old_tok_list:
        n = len(old); found = -1
        for k in range(pos, len(fold_tok) - n + 1):
            if fold_tok[k:k + n] == old:
                found = k; break
        if found < 0:
            print('  %s: old part "%s" NOT found whole in the fold' % (name, label)); ok = False; continue
        if found > pos: rest.append(('before ' + label, fold_tok[pos:found]))
        print('  %s: old part "%s" found whole, %d tokens, at token %d' % (name, label, n, found))
        pos = found + n
    if pos < len(fold_tok): rest.append(('after the last old part', fold_tok[pos:]))
    for where, toks in rest:
        print('  %s: NEW TEXT (%s), %d tokens:\n      %s' % (name, where, len(toks), ' '.join(toks)))
    return ok

print('\n== the four notes')
note_folds = [f for f in folds if f[0] == 'fold']
assert len(note_folds) == 4, len(note_folds)
allok = True
for k in range(4):
    cls, summ, inner = note_folds[k]
    allok &= compare('note %d (old heading "%s")' % (k + 1, heads[k][:50]), html_tokens(inner), md_tokens(sec[heads[k]]))

small = {html.unescape(s): inner for c, s, inner in folds if c != 'fold'}
print('\n== the small folds:', list(small))
rules_old = [p for p in top_paras if p.startswith('**I have not edited Wikipedia and will not.**')]
checked_old = [p for p in top_paras if p.startswith('*How this page was checked.*')]
each_old = [p for p in top_paras if p.startswith('Each note names the revision I read.')]
assert len(rules_old) == len(checked_old) == len(each_old) == 1
allok &= residue('fold "The two rules"', html_tokens(small['The two rules']), [('rules paragraph', md_tokens(rules_old[0]))])
allok &= residue('fold "How this page was checked"', html_tokens(small['How this page was checked']),
                 [('How this page was checked paragraph', md_tokens(checked_old[0])), ('Each note names ... paragraph', md_tokens(each_old[0]))])
last = [s for s in small if s.startswith('Files')]
assert len(last) == 1
allok &= residue('fold "%s"' % last[0], html_tokens(small[last[0]]), [('Files section', md_tokens(sec['Files']))])

# what of the old top is in no fold?
print('\n== old top paragraphs and where they are')
alltok_folds = ' '.join(html_tokens(' '.join(i for c, s, i in folds)))
open_html = re.sub(r'<details.*?</details>', ' ', cand, flags=re.S)
alltok_open = ' '.join(html_tokens(open_html))
for i, p in enumerate(top_paras):
    t = ' '.join(md_tokens(p))
    print('  top para %d: whole in a fold: %s ; whole in the open text: %s' % (i, t in alltok_folds, t in alltok_open))
t = ' '.join(md_tokens(sec['What none of the notes covers']))
print('  "What none of the notes covers": whole in the open text:', t in alltok_open)
for k in range(4):
    print('  old heading %d in the candidate anywhere: %s' % (k + 1, ' '.join(md_tokens(heads[k])) in ' '.join(html_tokens(cand))))
print('\nALL FOLD CHECKS PASSED' if allok else '\nSOME FOLD CHECK FAILED')
