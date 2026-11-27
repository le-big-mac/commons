"""Third pass: do the changes to the site builder (site.py against site.py.before-visit-2) change any word of any page,
and where do the new links to sections lead?
The whole notebook is built twice into this folder from the same sources.  The source of the page under test is the folder that
would be published with it (visit-4-page/minsize/files) without the HTML files the builder itself makes.
The built trees are deleted at the end; only this output is kept.     usage: builder_check2.py"""
import os, sys, re, shutil, subprocess, html, difflib, filecmp
E = os.path.dirname(os.path.abspath(__file__))
B = '/home/agent3/site/build'
V3 = '/home/agent3/door/visit-4-page'
PY = os.path.expanduser('~/welch/.venv/bin/python'); CAP = os.path.expanduser('~/bin/cap2g.sh')
stage, old, new = (os.path.join(E, x) for x in ('tmp-stage', 'tmp-built-old', 'tmp-built-new'))
for d in (stage, old, new):
    if os.path.exists(d): shutil.rmtree(d)
shutil.copytree(os.path.join(V3, 'minsize', 'files'), stage, ignore=shutil.ignore_patterns('*.html'))
print('staged source: files', sum(len(fs) for _, _, fs in os.walk(stage)))
env = dict(os.environ, DOOR_SRC=stage)
# the builder of before the second visit cannot build this version of the page (it wants a section "Why anyone asks" to fold),
# so with it only the four other studies are built; the page under test is compared with the candidate and with the author's build
for script, out, only in (('site.py.before-visit-2', old, ['antikythera,hemispheres,handshake,wikipedia']), ('site.py', new, [])):
    r = subprocess.run(['bash', CAP, PY, '-I', '-B', os.path.join(B, script), out] + only, env=env, capture_output=True, text=True)
    print(f'--- build with {script}: exit {r.returncode}'); print(r.stdout.strip()); print(r.stderr.strip()[-1500:])
    assert r.returncode == 0

def read(p): return open(p, encoding='utf-8', errors='replace').read()
def words(t):
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', t, flags=re.S)
    alts = re.findall(r'alt="([^"]*)"', t)
    return html.unescape(re.sub(r'<[^>]+>', ' ', t)).split(), alts
def files(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs)
fo, fn = files(old), files(new)
print(f'\nfiles in old build (four studies): {len(fo)}; in new build: {len(fn)}; only in old: {sorted(set(fo) - set(fn))}; only in new, outside minsize/ and front-files/: {sorted(f for f in set(fn) - set(fo) if not f.startswith(("minsize/", "front-files/")))}')
differ = [f for f in fn if f in set(fo) and not filecmp.cmp(os.path.join(old, f), os.path.join(new, f), shallow=False)]
print(f'HTML files in new build: {sum(1 for f in fn if f.endswith(".html"))};  files that differ in bytes between the two builds: {len(differ)}')
OLD_T = 'How few marks on a clock can balance in exactly a given set of ways? A theorem, checked by machine'
NEW_T = 'Balancing marks on a clock face: how few are needed? A theorem, checked by machine'
summary = {}
for f in differ:
    if not f.endswith('.html'):
        print(f'   differs (not HTML): {f}'); continue
    a, b = read(os.path.join(old, f)), read(os.path.join(new, f))
    (wo, ao), (wn, an) = words(a), words(b)
    # the same comparison with the title put back, and with the files note put back
    b2 = b.replace(html.escape(NEW_T), html.escape(OLD_T)).replace(NEW_T, OLD_T)
    wn2, _ = words(b2)
    kinds = []
    if wo == wn and ao == an: kinds.append('no word changed')
    elif wo == wn2: kinds.append('only the title')
    else:
        sm = difflib.SequenceMatcher(None, wo, wn2, autojunk=False)
        ch = [(' '.join(wo[i1:i2])[:200], ' '.join(wn2[j1:j2])[:200]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
        kinds.append('title and other words' if wn != wn2 else 'other words'); kinds.append(ch)
    raw = set()
    for l in difflib.unified_diff(a.split('\n'), b.split('\n'), lineterm='', n=0):
        if l.startswith('+') and not l.startswith('+++'):
            if 'id="' in l and '<details class="fold"' in l: raw.add('id on a fold')
            if 'class="tosec"' in l: raw.add('link to a section')
            if '<h2 id=' in l: raw.add('id on a heading')
            if '<script>' in l or 'openFold' in l or '</script>' in l or 'a link to a folded section' in l: raw.add('script')
            if 'small-fold' in l: raw.add('checking paragraph folded')
    summary.setdefault((str(kinds[0]), tuple(sorted(raw))), []).append(f)
    if len(kinds) > 1: print(f'   {f}: {kinds[0]}: {kinds[1]}')
print()
for (k, raw), fl in sorted(summary.items()):
    print(f'   {len(fl)} page(s): {k}; kinds of change in the HTML: {list(raw)}')
    for f in fl[:40]: print('        ', f)
print('pages outside minsize/ that differ:', [f for f in differ if not f.startswith('minsize/')])

print('\n--- the new build against the author\'s build (visit-4-page)')
vf, nf = files(os.path.join(V3, 'minsize')), files(os.path.join(new, 'minsize'))
print('   files of the page only in the author\'s build:', sorted(set(vf) - set(nf)), ' only in mine:', sorted(set(nf) - set(vf)))
print('   differing among the common ones:', [f for f in vf if f in set(nf) and not filecmp.cmp(os.path.join(V3, 'minsize', f), os.path.join(new, 'minsize', f), shallow=False)])
print('   style.css same bytes:', filecmp.cmp(os.path.join(V3, 'style.css'), os.path.join(new, 'style.css'), shallow=False))

print('\n--- the page: words of the built page against the candidate Markdown')
pg = read(os.path.join(new, 'minsize/index.html'))
wp, alts = words(pg)
md = read('/home/agent3/door/README.visit-candidate-3.md')
md2 = re.sub(r'!\[([^\]]*)\]\([^)]*\)', ' ', md)
md2 = re.sub(r'(?m)^\|[-|]+\|\s*$', ' ', md2).replace('|', ' ')
md2 = re.sub(r'\[([^\]]*)\]\((https?://[^)]*)\)', r'\1', md2)
md2 = re.sub(r'(?m)^#+ ', '', md2); md2 = re.sub(r'(?m)^(\s*)- ', r'\1', md2)
md2 = md2.replace('**', '').replace('`', '')
md2 = re.sub(r'(?<![\w*])\*(?=\S)|(?<=\S)\*(?![\w*])', '', md2)
squeeze = lambda ws: ''.join(ws)
wm = md2.split()
i = squeeze(wp).find(squeeze(wm[:30]));
sm = difflib.SequenceMatcher(None, wm, wp, autojunk=False)
n_other = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal': continue
    a_, b_ = ''.join(wm[i1:i2]), ''.join(wp[j1:j2])
    if a_ == b_: continue                         # only the spacing round a file name or a link differs
    n_other += 1; print(f'   {tag}: MARKDOWN[{" ".join(wm[i1:i2])[:200]}] -> PAGE[{" ".join(wp[j1:j2])[:300]}]')
print('   differences other than spacing:', n_other, ';  alt text equal:', alts == re.findall(r'!\[([^\]]*)\]', md))
print('   <h1>:', re.findall(r'<h1>(.*?)</h1>', pg, re.S), '  <title>:', re.findall(r'<title>(.*?)</title>', pg))
print('   open headings, with ids:', re.findall(r'<h2 id="([^"]*)">(.*?)</h2>', pg))
print('   folds, with ids:', re.findall(r'<details class="fold[^"]*" id="([^"]*)">\n<summary>(.*?)</summary>', pg))
ids = re.findall(r'\bid="([^"]*)"', pg); print('   ids on the page:', len(ids), '; all different:', len(ids) == len(set(ids)))

print('\n--- every link to a section on the page: where it stands, its words, where it leads')
# walk the page in order, tracking the section we are in
pos = [(m.start(), 'open: ' + m.group(2)) for m in re.finditer(r'<h2 id="([^"]*)">(.*?)</h2>', pg)]
pos += [(m.start(), 'fold: ' + m.group(2)) for m in re.finditer(r'<details class="fold[^"]*" id="([^"]*)">\n<summary>(.*?)</summary>', pg)]
pos.sort()
def where(p):
    w = 'top'
    for q, name in pos:
        if q <= p: w = name
    return w
target_kind = {}
for m in re.finditer(r'<h2 id="([^"]*)">', pg): target_kind[m.group(1)] = 'open section'
for m in re.finditer(r'<details class="fold[^"]*" id="([^"]*)">', pg): target_kind[m.group(1)] = 'folded section'
text = lambda h: ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())
links = list(re.finditer(r'<a class="tosec" href="#([^"]*)">(.*?)</a>', pg))
for m in links:
    before = text(pg[max(0, m.start() - 260):m.start()])[-110:]; after = text(pg[m.end():m.end() + 160])[:60]
    print(f'   in [{where(m.start())}]  {m.group(2)} -> #{m.group(1)} ({target_kind.get(m.group(1), "NO SUCH ID")})')
    print(f'        …{before} «{text(m.group(2))}» {after}…')
print('   links to sections:', len(links), '; with a target on the page:', sum(1 for m in links if m.group(1) in target_kind))
# quoted names of sections that did not become links
names = [n for _, n in re.findall(r'<h2 id="([^"]*)">(.*?)</h2>', pg)] + [n for _, n in re.findall(r'<details class="fold[^"]*" id="([^"]*)">\n<summary>(.*?)</summary>', pg)]
plain = re.sub(r'<a class="tosec"[^>]*>.*?</a>', ' LINK ', pg)
for n in names:
    c = len(re.findall('"' + re.escape(n) + '"', plain))
    if c: print(f'   the name "{n}" stands {c} time(s) in quotation marks without a link')
print('   the script at the end of the page:'); print('      ' + '\n      '.join(re.findall(r'<script>.*?</script>', pg, re.S)[0].split('\n')))

print('\n--- the new rule: inside a folded section the name of an open section is not a link')
open_ids = set(i for i, _ in re.findall(r'<h2 id="([^"]*)">(.*?)</h2>', pg))
inside = [(where(m.start()), m.group(1)) for m in links if where(m.start()).startswith('fold: ')]
print('   links standing inside folded sections:', len(inside), '; of them to an open section:', [x for x in inside if x[1] in open_ids])
print('   links standing in the open text:', len(links) - len(inside), '; of them to a folded section:', sum(1 for m in links if not where(m.start()).startswith('fold: ') and target_kind.get(m.group(1)) == 'folded section'))
print('\n--- "(tap or click to open)": the style sheet now shows it only on the first of a run of folded sections')
css = read(os.path.join(new, 'style.css'))
print('   rules of the style sheet about the label:', [l.strip() for l in css.split('\n') if 'summary::after' in l])
for slug in ('antikythera', 'hemispheres', 'handshake', 'wikipedia', 'minsize'):
    t_ = read(os.path.join(new, slug, 'index.html'))
    fl = [(m.start(), m.end(), re.sub(r'<[^>]+>', '', m.group(1))) for m in re.finditer(r'<details class="fold[^"]*"[^>]*>\s*<summary>(.*?)</summary>', t_, re.S)]
    ends = [m.end() for m in re.finditer(r'</details>', t_)]
    lost = []
    for a, b, name in fl:
        before_ = t_[:a].rstrip()
        if before_.endswith('</details>'):          # the element just before is a details; is it a fold?
            k = before_.rfind('<details'); 
            if 'class="fold' in before_[k:k + 60]: lost.append(name)
    print(f'   {slug}: folded sections {[n for _, _, n in fl]}; those that no longer show the label (they follow another fold directly): {lost}')
print('\n--- the titles on the built pages')
for rel in ('index.html', 'minsize/index.html', 'minsize/files/index.html'):
    t = read(os.path.join(new, rel))
    print(f'   {rel}: old title {t.count(OLD_T) + t.count(html.escape(OLD_T))} time(s), new title {t.count(NEW_T) + t.count(html.escape(NEW_T))} time(s)')
cnt_old = sum(1 for f in fn if f.endswith('.html') and (OLD_T in read(os.path.join(new, f)) or html.escape(OLD_T) in read(os.path.join(new, f))))
print('   pages of the new build that still carry the old title (in their text, e.g. a visitor\'s report quoting it):', cnt_old)
print('   ', [f for f in fn if f.endswith('.html') and (OLD_T in read(os.path.join(new, f)) or html.escape(OLD_T) in read(os.path.join(new, f)))][:12])
fr = read(os.path.join(new, 'index.html')); k = fr.find(html.escape(NEW_T)) if html.escape(NEW_T) in fr else fr.find(NEW_T)
print('   the card on the front page:', text(fr[k - 80:k + 900])[:700])
print('   files note on the files page:', text(re.findall(r'<p>(The paper and its source.*?)</p>', read(os.path.join(new, 'minsize/files/index.html')), re.S)[0]))
print('   README.before-visit: kept as', [f for f in nf if 'before-visit' in f], '; in the old build:', [f for f in files(os.path.join(old, 'minsize')) if 'before-visit' in f])
for d in (stage, old, new): shutil.rmtree(d)
print('\nbuilt trees and the staged copy deleted')
