"""Second evidence reading: the second candidate as built, and the builder and style sheet as they now stand.
usage: python ev9_second_built.py
Loads the two versions of site.py without running build() and without writing bytecode. Prints; writes nothing."""
import html
import os
import re
import sys

sys.dont_write_bytecode = True
B = '/home/agent3/site/build'
PREVIEW = '/home/agent3/site/anti-preview2/antikythera/index.html'
PUBLIC = '/home/agent3/site/commons/yonder/antikythera/index.html'


def load(path):
    ns = {'__name__': 'site_loaded', '__file__': os.path.join(B, 'site.py')}
    old_argv = sys.argv
    sys.argv = ['site.py', '/home/agent3/site/check-anti-visit/never-built']
    try:
        exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), ns)
    finally:
        sys.argv = old_argv
    return ns


new, old = load(f'{B}/site.py'), load(f'{B}/site.py.before-anti-visit')


def letters(h):
    h = re.sub(r'<script>.*?</script>', ' ', h, flags=re.S)
    return ''.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())


def body_of(ns, st, src_path=None, use_links=None):
    src_path = src_path or os.path.join(B, 'pages', st['slug'] + '.html')
    body = ns['fold'](open(src_path, encoding='utf-8').read(), st.get('fold', ()))
    if (st.get('link_sections') if use_links is None else use_links) and ns is new:
        body = ns['link_sections'](body)
    if st.get('full_size'):
        body = ns['full_size'](body)
    return body


print('--- functions of the builder that differ between the pre-visit copy and now (by their source text) ---')
src_new, src_old = open(f'{B}/site.py', encoding='utf-8').read(), open(f'{B}/site.py.before-anti-visit', encoding='utf-8').read()
def defs(s):
    parts = re.split(r'^(?=def |[A-Z_]+ = )', s, flags=re.M)
    return {re.match(r'(def (\w+)|([A-Z_]+) = )', p).group(2) or re.match(r'([A-Z_]+) = ', p).group(1): p for p in parts if re.match(r'(def \w+|[A-Z_]+ = )', p)}
dn, do = defs(src_new), defs(src_old)
print('   differ:', sorted(k for k in set(dn) | set(do) if dn.get(k) != do.get(k)))

print('\n--- pages built from pages/<slug>.html: the pre-visit builder against the builder now ---')
for st_o, st_n in zip(old['STUDIES'], new['STUDIES']):
    diff = sorted(k for k in set(st_o) | set(st_n) if st_o.get(k) != st_n.get(k) and not callable(st_o.get(k)))
    if st_n.get('page_from_note'):
        print(f"{st_n['slug']:12s} built from its note; keys of its entry that differ: {diff or 'none'}; link_sections: {st_n.get('link_sections')}")
        continue
    if st_n['slug'] == 'antikythera':
        continue
    bo, bn = body_of(old, st_o), body_of(new, st_n)
    print(f"{st_n['slug']:12s} bodies identical: {bo == bn}; keys that differ: {diff or 'none'}")

print('\n--- the second candidate through the builder, against the preview as built ---')
st = [s for s in new['STUDIES'] if s['slug'] == 'antikythera'][0]
src = open(os.path.join(B, 'pages', 'antikythera.html'), encoding='utf-8').read()
bn = body_of(new, st)
pv = open(PREVIEW, encoding='utf-8').read()
print('the body is in the preview letter for letter:', bn in pv)
plain = body_of(new, st, use_links=False)
strip = re.sub(r'<a class="tosec" href="#[^"]*">(.*?)</a>', r'\1', bn)
strip = re.sub(r'<h2 id="[^"]*">', '<h2>', strip).replace('\n' + new['OPEN_ON_LINK'], '')
print('the body with section links, heading ids and the script taken out == the body without link_sections:', strip == plain)
print('letters in order, source against built body (the full-size links apart):', letters(src) == letters(bn).replace('Seethepictureatfullsize.', ''))

links = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r'<a class="tosec" href="#([^"]*)">(.*?)</a>', bn)]


def where(i):
    stack = []
    for m in re.finditer(r'<details[^>]*>\n?<summary>(.*?)</summary>|</details>', bn[:i], flags=re.S):
        if m.group(0).startswith('</'):
            stack.pop()
        else:
            stack.append(m.group(1))
    return ' > '.join(stack) or 'open text'


print(f'{len(links)} section links:')
for i, target, txt in links:
    tm = re.search(r'<(details|h2)[^>]* id="' + re.escape(target) + '"', bn)
    print(f'   {txt:40s} -> a {tm.group(1) if tm else "MISSING"}; the target lies in: {where(tm.start()) if tm else "-"}; the link stands in: {where(i)}')
names = set(re.findall(r'<h2[^>]*>(.*?)</h2>', bn)) | set(re.findall(r'<summary>(.*?)</summary>', bn))
unlinked = [(m.start(), m.group(1)) for m in re.finditer(r'(?<!>)"([^"<>]{3,60})"', re.sub(r'<a class="tosec".*?</a>', lambda m: ' ' * len(m.group(0)), bn)) if m.group(1) in names]
print('names of the page\'s own sections that stand in quotation marks and are NOT links:')
for i, nm in unlinked:
    print(f'   "{nm}" in: {where(i)}')

print('\nfolds in the built body:', re.findall(r'<details class="([^"]*)" id="([^"]*)"', bn))
print('placeholder left:', re.findall(r'TODO[^<]*', bn))

print('\n--- the kept folds, built: public copy against the preview ---')
pub = open(PUBLIC, encoding='utf-8').read()
def folds(h):
    return {m.group(1): m.group(2) for m in re.finditer(r'<details class="fold" id="[^"]*">\n<summary>(.*?)</summary>(.*?)</details>', h, flags=re.S)} | \
           {m.group(1): m.group(2) for m in re.finditer(r'<details class="fold">\n<summary>(.*?)</summary>(.*?)</details>', h, flags=re.S)}
fp, fn = folds(pub), folds(pv)
for name in fp:
    a, b = letters(fp[name]), letters(fn[name])
    import difflib
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']
    print(f'"{name}": places where the letters differ: {len(ops)}', [(o[0], a[o[1]:o[2]], b[o[3]:o[4]]) for o in ops])

print('\n--- words that the builder and the style sheet put on a page themselves ---')
print('in the script (shown only after a section link is followed):', re.findall(r'textContent = "([^"]*)"', new['OPEN_ON_LINK']))
css_n, css_o = open(f'{B}/style.css', encoding='utf-8').read(), open(f'{B}/style.css.before-anti-visit', encoding='utf-8').read()
print('style sheet, "content:" rules now:   ', re.findall(r'([^{}\n]*)\{[^{}]*content:\s*("[^"]*")', css_n))
print('style sheet, "content:" rules before:', re.findall(r'([^{}\n]*)\{[^{}]*content:\s*("[^"]*")', css_o))
print('preview style.css is the style.css now:', open('/home/agent3/site/anti-preview2/style.css', encoding='utf-8').read() == css_n)
print('rules that hide anything, added:', [l for l in css_n.splitlines() if l not in css_o.splitlines() and re.search(r'display:\s*none|visibility', l)])
