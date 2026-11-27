"""Evidence reading, part 4: do the builder's change and the style sheet's change alter any word of any page?
usage: python ev2_builder.py
Loads the two versions of site.py without running build() and without writing bytecode, runs the body pipeline
of every study whose page comes from pages/<slug>.html (the only branch that the change touches), and compares.
Also compares the new antikythera body with the preview as built. Writes nothing; prints."""
import html
import os
import re
import sys

sys.dont_write_bytecode = True
B = '/home/agent3/site/build'
PREVIEW = '/home/agent3/site/anti-preview/antikythera/index.html'


def load(path):
    ns = {'__name__': 'site_loaded', '__file__': os.path.join(B, 'site.py')}
    old_argv = sys.argv
    sys.argv = ['site.py', '/home/agent3/site/check-anti-visit/never-built']   # OUT is only computed, never created
    try:
        exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), ns)
    finally:
        sys.argv = old_argv
    return ns


new, old = load(f'{B}/site.py'), load(f'{B}/site.py.before-anti-visit')


def words(h):
    """visible words in order: tags apart, scripts apart, entities read"""
    h = re.sub(r'<script>.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(h).split()


def alt_texts(h):
    return re.findall(r'alt="([^"]*)"', h)


def body_of(ns, st, src_path=None):
    src_path = src_path or os.path.join(B, 'pages', st['slug'] + '.html')
    body = ns['fold'](open(src_path, encoding='utf-8').read(), st.get('fold', ()))
    if ns is new and st.get('link_sections'):
        body = ns['link_sections'](body)
    if st.get('full_size'):
        body = ns['full_size'](body)
    return body


print('--- the STUDIES lists of the two builders, key by key ---')
for so, sn in zip(old['STUDIES'], new['STUDIES']):
    assert so['slug'] == sn['slug']
    diff = {k for k in set(so) | set(sn) if so.get(k) != sn.get(k) and not callable(so.get(k)) and not callable(sn.get(k))}
    print(f"{so['slug']:12s} keys that differ: {sorted(diff) or 'none'}; page from note: {bool(sn.get('page_from_note'))}; link_sections old/new: {so.get('link_sections')}/{sn.get('link_sections')}")

print('\n--- pages built from pages/<slug>.html: old pipeline against new pipeline, same source ---')
for st_o, st_n in zip(old['STUDIES'], new['STUDIES']):
    if st_n.get('page_from_note'):
        continue
    bo, bn = body_of(old, st_o), body_of(new, st_n)
    # "letters" = the visible letters in order with all spaces taken out: a link's closing tag before a full stop splits a "word" but changes no letter
    print(f"{st_n['slug']:12s} bodies identical: {bo == bn}; visible letters in order identical (spaces apart): {''.join(words(bo)) == ''.join(words(bn))} ({len(words(bn))} words); alt texts identical: {alt_texts(bo) == alt_texts(bn)}")
    if bo != bn:
        # what was added: tags only?
        strip_new = re.sub(r'<a class="tosec" href="#[^"]*">(.*?)</a>', r'\1', bn)
        strip_new = re.sub(r'<h2 id="[^"]*">', '<h2>', strip_new)
        strip_new = strip_new.replace('\n' + new['OPEN_ON_LINK'], '')
        print('   new body with the section links, heading ids and the script taken out == old body:', strip_new == bo)
        links = re.findall(r'<a class="tosec" href="#([^"]*)">(.*?)</a>', bn)
        ids = set(re.findall(r' id="([^"]*)"', bn))
        print(f'   {len(links)} section links:')
        pos = 0
        for target, text in links:
            i = bn.index(f'<a class="tosec" href="#{target}">{text}</a>', pos); pos = i + 1
            # which fold, if any, is the link inside?
            opened = [m.start() for m in re.finditer(r'<details', bn[:i])]
            closed = [m.start() for m in re.finditer(r'</details>', bn[:i])]
            where = 'open text' if len(opened) == len(closed) else 'inside fold: ' + re.search(r'<summary>(.*?)</summary>', bn[opened[-1]:]).group(1)
            kind = re.search(r'<(details|h2)[^>]* id="' + re.escape(target) + '"', bn).group(1)
            print(f'     {text:42s} -> #{target} ({"exists" if target in ids else "MISSING"}, a {kind}); {where}')
        quoted = re.findall(r'(?<!>)"([A-Z][^"<>]{3,60})"', re.sub(r'<a class="tosec".*?</a>', '', bn))
        print('   quoted phrases beginning with a capital left unlinked (to see whether a section name was missed):')
        for q in quoted:
            print('     ', q)

print('\n--- the new antikythera body against the preview as built ---')
st = [s for s in new['STUDIES'] if s['slug'] == 'antikythera'][0]
bn = body_of(new, st)
pv = open(PREVIEW, encoding='utf-8').read()
print('the body is in the preview letter for letter:', bn in pv)
src = open(os.path.join(B, 'pages', 'antikythera.html'), encoding='utf-8').read()
ws, wp = words(src), words(pv)
# the preview has the shell's crumbs before and the footer after, and the "See the picture at full size." links
print('source words:', len(ws), '| preview words:', len(wp))
import difflib
sm = difflib.SequenceMatcher(None, ws, wp, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print(f'  {tag}: SOURCE[{" ".join(ws[i1:i2])}] PREVIEW[{" ".join(wp[j1:j2])}]')

print('\n--- the old antikythera page through the OLD pipeline against the public copy, if it is on disk ---')
pub = '/home/agent3/site/commons/yonder/antikythera/index.html'
if os.path.exists(pub):
    st_o = [s for s in old['STUDIES'] if s['slug'] == 'antikythera'][0]
    bo = body_of(old, st_o, os.path.join(B, 'pages', 'antikythera.html.before-visit-27nov'))
    print('the old body is in the public copy letter for letter:', bo in open(pub, encoding='utf-8').read())

print('\n--- style sheet: only rules added? ---')
co = open(f'{B}/style.css.before-anti-visit', encoding='utf-8').read()
cn = open(f'{B}/style.css', encoding='utf-8').read()
print('new style sheet begins with the whole of the old one:', cn.startswith(co.rstrip('\n')) or cn.startswith(co))
lines_o, lines_n = co.splitlines(), cn.splitlines()
added = [l for l in difflib.unified_diff(lines_o, lines_n, lineterm='', n=0) if l.startswith(('+', '-')) and not l.startswith(('+++', '---'))]
for l in added:
    print('  ', l[:230])
print('"content:" (a rule that would put words on the page) in old, new:', co.count('content:'), cn.count('content:'))
print('"display: none" / "visibility" in the added lines:', any('display' in l or 'visibility' in l for l in added))
print('preview style.css is the new style.css:', open('/home/agent3/site/anti-preview/style.css', encoding='utf-8').read() == cn)
