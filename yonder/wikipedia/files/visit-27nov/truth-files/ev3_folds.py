"""Evidence reading 3 (third candidate): the folds against the old text, by program.
usage: python -I ev3_folds.py candidate-3.html README.md
The old text is cut here by my own rules; markup is stripped from both sides; comparison is token by token
(tokens = runs of non-space characters), so paragraph breaks put into an old paragraph do not count as changes."""
import sys, re, html

cand = open(sys.argv[1], encoding='utf-8').read()
readme = open(sys.argv[2], encoding='utf-8').read()
INLINE = r'</?(em|strong|code|a|b|i|span)(\s[^>]*)?>'
def html_tokens(h):
    h = re.sub(r'<br\s*/?>', ' ', h)
    h = re.sub(INLINE, '', h); h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(h).split()
def md_tokens(m):
    m = '\n'.join(l for l in m.split('\n') if not re.fullmatch(r'\s*\|(\s*:?-+:?\s*\|)+\s*', l))
    return m.replace('**', '').replace('*', '').replace('`', '').replace('|', ' ').split()

parts = re.split(r'^## ', readme, flags=re.M)
top = parts[0]; sec = {}
for p in parts[1:]:
    head, body = p.split('\n', 1); sec[head.strip()] = body
heads = list(sec)
top_paras = [x.strip() for x in re.split(r'\n\s*\n', top) if x.strip()]
rules_old = [p for p in top_paras if p.startswith('**I have not edited Wikipedia and will not.**')][0]
checked_old = [p for p in top_paras if p.startswith('*How this page was checked.*')][0]
each_old = [p for p in top_paras if p.startswith('Each note names the revision I read.')][0]

folds = re.findall(r'<details class="([^"]*)">\s*<summary>(.*?)</summary>(.*?)</details>', cand, flags=re.S)
print('folds in the candidate:', len(folds), '; <details> opened:', cand.count('<details'), 'closed:', cand.count('</details>'))
F = {}
for cls, summ, inner in folds:
    s = html.unescape(summ); F[s] = inner
    print('  [%s] %s  (%d tokens, %d paragraphs)' % (cls, s, len(html_tokens(inner)), inner.count('<p>')))

def find_run(T, R, start=0):
    n = len(R)
    for k in range(start, len(T) - n + 1):
        if T[k:k + n] == R: return k
    return -1
def residue(name, fold_tok, old_list):
    pos = 0; ok = True; rest = []
    for label, old in old_list:
        k = find_run(fold_tok, old, pos)
        if k < 0:
            print('  %s: old part "%s" (%d tokens) NOT found whole and in order' % (name, label, len(old))); ok = False; continue
        if k > pos: rest.append(('before "%s"' % label, fold_tok[pos:k]))
        print('  %s: old part "%s" found whole, %d tokens' % (name, label, len(old)))
        pos = k + len(old)
    if pos < len(fold_tok): rest.append(('after the last old part', fold_tok[pos:]))
    for where, toks in rest:
        print('      OTHER TEXT (%s), %d tokens: %s' % (where, len(toks), ' '.join(toks)))
    return ok

ok = True
print('\n== the four notes')
for k in range(4):
    name = [s for s in F if re.match(r'More on note %d\b' % (k + 1), s)]
    assert len(name) == 1, name
    ok &= residue('note %d' % (k + 1), html_tokens(F[name[0]]), [('the old note, whole', md_tokens(sec[heads[k]]))])
print('   old headings:', [h for h in heads[:4]])

print('\n== "The two rules"')
rt = md_tokens(rules_old)
a = find_run(rt, 'Its talk-page guideline says'.split()); b = find_run(rt, 'If you are an editor'.split())
print('  the old paragraph has %d tokens; the sentences on the rules are tokens %d to %d; before them: "%s"; after them: "%s"' % (len(rt), a, b - 1, ' '.join(rt[:a]), ' '.join(rt[b:])))
ok &= residue('fold "The two rules"', html_tokens(F['The two rules']), [('old sentences on the two rules, less their first word "Its"', rt[a + 1:b])])

print('\n== "How this page was checked"')
ct = md_tokens(checked_old)
title = 'How this page was checked.'.split()
assert ct[:len(title)] == title
ok &= residue('fold "How this page was checked"', html_tokens(F['How this page was checked']),
              [('old paragraph less its run-in title', ct[len(title):]), ('Each note names ...', md_tokens(each_old))])
inner = F['How this page was checked']
paras = [html_tokens(p) for p in re.findall(r'<p>(.*?)</p>', inner, flags=re.S)]
print('  paragraphs in the fold: %d ; first words of each: %s' % (len(paras), [' '.join(p[:6]) for p in paras]))
# does every break fall at a sentence end?
for p in paras: print('     ends: ...%s' % ' '.join(p[-4:]))

print('\n== the last fold')
last = [s for s in F if s.startswith('Files')][0]
ok &= residue('fold "%s"' % last, html_tokens(F[last]), [('old section "What none of the notes covers"', md_tokens(sec['What none of the notes covers'])), ('old section "Files"', md_tokens(sec['Files']))])

print('\n== old text that stands in no fold of the second candidate')
alltok = html_tokens(' '.join(i for c, s, i in folds))
openhtml = re.sub(r'<details.*?</details>', ' ', cand, flags=re.S); opentok = html_tokens(openhtml)
def sentences(md_text):
    t = ' '.join(md_tokens(md_text))
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z("\'])', t) if s.strip()]
for label, text in [('old top, paragraph 2 (byline)', top_paras[1]), ('old top, rules paragraph', rules_old)]:
    for s in sentences(text):
        st = s.split()
        print('  [%s] in a fold: %-5s in the open: %-5s | %s' % (label, find_run(alltok, st) >= 0, find_run(opentok, st) >= 0, s[:110]))
print('\nALL FOLD CHECKS PASSED' if ok else '\nSOME FOLD CHECK FAILED')
