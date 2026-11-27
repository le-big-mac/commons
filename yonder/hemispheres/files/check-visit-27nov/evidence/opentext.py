"""Open text of the public page against open text of the candidate, sentence by sentence.
"Open" = outside every <details> (what a reader sees without tapping a heading).
usage: python opentext.py OLD_BUILT NEW_BUILT
Prints: old open sentences that are nowhere in the new open text (and whether they are still on the page, behind which heading);
        new open sentences that are nowhere in the old open text (new or changed wording); headings of both."""
import re, sys, html

old_b = open(sys.argv[1], encoding='utf-8').read()
new_b = open(sys.argv[2], encoding='utf-8').read()


def body(s):
    i = s.index('<h1>'); j = s.index('<footer>')
    return re.sub(r'<script.*?</script>', ' ', s[i:j], flags=re.S)


def clean(s):
    s = re.sub(r' ?<a class="fullsize"[^>]*>See the picture at full size\.</a>', '', s)
    s = re.sub(r'<img[^>]*>', ' ', s)
    s = re.sub(r'</?(a|code|em|strong)\b[^>]*>', '', s)
    s = re.sub(r'</(p|li|h1|h2|summary|figcaption|td|th|tr)>', ' \u00b6\u00b6 ', s)   # block ends are sentence ends
    s = re.sub(r'<[^>]+>', ' ', s)
    return ' '.join(html.unescape(s).split())


def split_folds(s):
    """-> (open text, [(summary, text)])"""
    folds = []
    def take(m):
        inner = m.group(1)
        sm = re.match(r'\s*<summary>(.*?)</summary>', inner, re.S)
        folds.append((clean(sm.group(1)).replace('\u00b6\u00b6', '').strip(), clean(inner[sm.end():])))
        return ' \u00b6\u00b6 [[FOLD: ' + clean(sm.group(1)).replace('\u00b6\u00b6', '').strip() + ']] \u00b6\u00b6 '
    assert '<details' not in ''.join(re.findall(r'<details[^>]*>(.*?)</details>', s, re.S)), 'nested folds'
    o = re.sub(r'<details[^>]*>(.*?)</details>', take, s, flags=re.S)
    return clean(o), folds


def sentences(t):
    out = []
    for block in t.split('\u00b6\u00b6'):
        block = block.strip()
        if not block:
            continue
        # a sentence ends at . ? ! (with a closing quote or bracket after it) before a space and a capital, quote or bracket
        parts = re.split(r'(?<=[.?!])(?<!\bN\.)(?<!\bE\.)(?<!\bW\.)(?<!\bS\.)(?<! J\.)(?<!-G\.)["\')]*\s+(?=[A-Z"(\u00c0-\u00dc])', block)
        out += [p.strip() for p in parts if p.strip()]
    return out


oo, ofolds = split_folds(body(old_b))
no, nfolds = split_folds(body(new_b))
so, sn = sentences(oo), sentences(no)
print(f'old open text: {len(oo.replace(chr(0xb6), "").split())} words, {len(so)} sentences and headings; folds: {[f[0] for f in ofolds]}')
print(f'new open text: {len(no.replace(chr(0xb6), "").split())} words, {len(sn)} sentences and headings; folds: {[f[0] for f in nfolds]}')
for name, t in nfolds:
    print(f'    new fold {name!r}: {len(t.replace(chr(0xb6), "").split())} words')
for name, t in ofolds:
    print(f'    old fold {name!r}: {len(t.replace(chr(0xb6), "").split())} words')

no_flat = ' '.join(no.replace('\u00b6\u00b6', ' ').split())
oo_flat = ' '.join(oo.replace('\u00b6\u00b6', ' ').split())
print('\n=== A. sentences of the OLD open text that are nowhere in the NEW open text ===')
k = 0
for s in so:
    if s in no_flat:
        continue
    k += 1
    where = [name for name, t in nfolds if s in ' '.join(t.replace('\u00b6\u00b6', ' ').split())]
    print(f'\nA{k}. [{len(s.split())} words] now: {("behind " + repr(where[0])) if where else "NOWHERE on the page in these words"}')
    print('    ' + s)
print(f'\n{k} sentences')

print('\n=== B. sentences of the NEW open text that are nowhere in the OLD open text ===')
k = 0
for s in sn:
    if s in oo_flat:
        continue
    k += 1
    was = [name for name, t in ofolds if s in ' '.join(t.replace('\u00b6\u00b6', ' ').split())]
    print(f'\nB{k}. [{len(s.split())} words] {("was behind " + repr(was[0])) if was else "new wording"}')
    print('    ' + s)
print(f'\n{k} sentences')

print('\n=== C. names of the page\'s own sections in quotation marks: link or not (candidate, as built) ===')
heads = set(clean(x).replace('\u00b6\u00b6', '').strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', new_b, re.S)) | set(f[0] for f in nfolds)
b = body(new_b)
for h in sorted(heads):
    for m in re.finditer(re.escape('"' + html.escape(h, quote=False) + '"'), b):
        linked = b[max(0, m.start() - 80):m.start()].rstrip().endswith('>') and '<a class="tosec"' in b[max(0, m.start() - 80):m.start()]
        # which fold is it in
        pre = b[:m.start()]
        depth = len(re.findall(r'<details', pre)) - len(re.findall(r'</details>', pre))
        fold = clean(re.findall(r'<summary>(.*?)</summary>', pre, re.S)[-1]).replace('\u00b6\u00b6', '').strip() if depth else 'open text'
        print(f'    "{h}": {"LINK" if linked else "not a link"}; in {fold}; ...{clean(b[max(0, m.start() - 60):m.start()]).replace(chr(0xb6), "")[-45:]!r}')
